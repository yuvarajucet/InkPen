"""
InkPen - Floating Always-On-Top Toolbar
"""
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QFrame, QLabel, QSlider, QSizePolicy, QMenu, QAction,
    QWidgetAction, QApplication, QToolTip, QColorDialog,
    QGraphicsDropShadowEffect
)
from PyQt5.QtCore import (
    Qt, QPoint, QSize, pyqtSignal, QPropertyAnimation,
    QEasingCurve, QTimer, QRect, QEvent
)
from PyQt5.QtGui import (
    QColor, QPainter, QPainterPath, QBrush, QPen,
    QPixmap, QFont, QLinearGradient, QIcon, QCursor,
    QFontMetrics
)

from tools import Tool, Shape, PRESET_COLORS, HIGHLIGHTER_COLORS, PEN_SIZES
from icons import (
    svg_to_icon, svg_to_pixmap,
    ICON_CURSOR, ICON_PEN, ICON_HIGHLIGHTER, ICON_SHAPE,
    ICON_ERASER, ICON_TEXT, ICON_COLOR_PICKER, ICON_TRASH,
    ICON_PEN_SIZE, ICON_MINIMIZE, ICON_CLOSE, ICON_UNDO,
    ICON_LINE, ICON_ARROW, ICON_RECT, ICON_ELLIPSE, ICON_TRIANGLE,
    ICON_DRAG
)


# ── Color Swatch Widget ────────────────────────────────────────────────────

class ColorSwatch(QPushButton):
    """A small circular color swatch button."""
    color_selected = pyqtSignal(QColor)

    def __init__(self, color: str, size: int = 22, parent=None):
        super().__init__(parent)
        self._color = QColor(color)
        self._size = size
        self._selected = False
        self.setFixedSize(size + 4, size + 4)
        self.setToolTip(color)
        self.clicked.connect(lambda: self.color_selected.emit(self._color))
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("background: transparent; border: none;")

    def set_selected(self, val: bool):
        self._selected = val
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        r = self.rect().adjusted(2, 2, -2, -2)
        if self._selected:
            p.setPen(QPen(QColor(255, 255, 255), 2.5))
            p.setBrush(Qt.NoBrush)
            p.drawEllipse(r.adjusted(-2, -2, 2, 2))
        p.setPen(QPen(QColor(0, 0, 0, 40), 1))
        p.setBrush(QBrush(self._color))
        p.drawEllipse(r)
        p.end()


# ── Tool Button ────────────────────────────────────────────────────────────

class ToolButton(QPushButton):
    """A stylized tool button for the toolbar."""

    def __init__(self, icon_svg: str, tooltip: str, parent=None):
        super().__init__(parent)
        self._icon_svg = icon_svg
        self._active = False
        self._hovered = False
        self.setFixedSize(42, 42)
        self.setToolTip(tooltip)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("background: transparent; border: none;")
        self.installEventFilter(self)

    def set_active(self, val: bool):
        self._active = val
        self.update()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter:
            self._hovered = True
            self.update()
        elif event.type() == QEvent.Leave:
            self._hovered = False
            self.update()
        return super().eventFilter(obj, event)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(3, 3, -3, -3)

        if self._active:
            # Glowing active state
            glow = QPainterPath()
            glow.addRoundedRect(rect.x() - 1, rect.y() - 1,
                                rect.width() + 2, rect.height() + 2, 10, 10)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(QColor(99, 179, 237, 50)))
            p.drawPath(glow)

            bg = QPainterPath()
            bg.addRoundedRect(rect.x(), rect.y(),
                              rect.width(), rect.height(), 9, 9)
            grad = QLinearGradient(rect.topLeft(), rect.bottomRight())
            grad.setColorAt(0, QColor(59, 130, 246))
            grad.setColorAt(1, QColor(37, 99, 235))
            p.setBrush(QBrush(grad))
            p.drawPath(bg)
            icon_color = "#FFFFFF"

        elif self._hovered:
            bg = QPainterPath()
            bg.addRoundedRect(rect.x(), rect.y(),
                              rect.width(), rect.height(), 9, 9)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(QColor(255, 255, 255, 25)))
            p.drawPath(bg)
            icon_color = "#E2E8F0"
        else:
            icon_color = "#94A3B8"

        # Draw icon
        pix = svg_to_pixmap(self._icon_svg, 22, icon_color)
        icon_x = (self.width() - 22) // 2
        icon_y = (self.height() - 22) // 2
        p.drawPixmap(icon_x, icon_y, pix)
        p.end()


# ── Separator ─────────────────────────────────────────────────────────────

class ToolbarSeparator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(2, 28)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setPen(QPen(QColor(255, 255, 255, 25), 1))
        p.drawLine(1, 2, 1, self.height() - 2)
        p.end()


# ── Pen Size Popup ─────────────────────────────────────────────────────────

class PenSizePopup(QWidget):
    size_selected = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent, Qt.Popup | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)

        for size in PEN_SIZES:
            btn = QPushButton(self)
            btn.setFixedSize(size * 2 + 16, size * 2 + 16)
            btn.setCursor(Qt.PointingHandCursor)

            s = size  # Capture for lambda
            dot_size = min(size * 2, 24)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    border: none;
                    border-radius: {(dot_size + 16) // 2}px;
                }}
                QPushButton:hover {{
                    background: rgba(255,255,255,20);
                }}
            """)
            btn.clicked.connect(lambda checked, sz=s: self.size_selected.emit(sz))
            layout.addWidget(btn, alignment=Qt.AlignCenter)

            # Draw dot preview
            btn._dot_size = dot_size

        self.setMinimumHeight(56)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # Background
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 12, 12)
        p.setPen(QPen(QColor(255, 255, 255, 20), 1))
        p.setBrush(QBrush(QColor(15, 23, 42, 230)))
        p.drawPath(path)

        # Draw size dots
        layout = self.layout()
        if layout:
            for i, size in enumerate(PEN_SIZES):
                item = layout.itemAt(i)
                if item and item.widget():
                    btn = item.widget()
                    geom = btn.geometry()
                    cx = geom.center().x()
                    cy = geom.center().y()
                    dot_r = min(size, 12)
                    p.setPen(Qt.NoPen)
                    p.setBrush(QBrush(QColor(226, 232, 240)))
                    p.drawEllipse(cx - dot_r, cy - dot_r, dot_r * 2, dot_r * 2)
        p.end()


# ── Shape Popup ────────────────────────────────────────────────────────────

class ShapePopup(QWidget):
    shape_selected = pyqtSignal(Shape)

    def __init__(self, parent=None):
        super().__init__(parent, Qt.Popup | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(4)

        shapes = [
            (Shape.LINE, ICON_LINE, "Line"),
            (Shape.ARROW, ICON_ARROW, "Arrow"),
            (Shape.RECTANGLE, ICON_RECT, "Rectangle"),
            (Shape.ELLIPSE, ICON_ELLIPSE, "Ellipse"),
            (Shape.TRIANGLE, ICON_TRIANGLE, "Triangle"),
        ]

        for shape, icon_svg, tip in shapes:
            btn = ToolButton(icon_svg, tip, self)
            btn.setFixedSize(38, 38)
            btn.clicked.connect(lambda checked, s=shape: self.shape_selected.emit(s))
            layout.addWidget(btn)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 12, 12)
        p.setPen(QPen(QColor(255, 255, 255, 20), 1))
        p.setBrush(QBrush(QColor(15, 23, 42, 230)))
        p.drawPath(path)
        p.end()


# ── Color Popup ────────────────────────────────────────────────────────────

class ColorPopup(QWidget):
    color_selected = pyqtSignal(QColor)
    highlight_color_selected = pyqtSignal(QColor)

    def __init__(self, parent=None):
        super().__init__(parent, Qt.Popup | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._swatches = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Pen colors
        pen_label = QLabel("Pen Color")
        pen_label.setStyleSheet("color: #94A3B8; font-size: 10px; font-family: 'Segoe UI';")
        layout.addWidget(pen_label)

        pen_row = QHBoxLayout()
        pen_row.setSpacing(5)
        for c in PRESET_COLORS:
            sw = ColorSwatch(c, 20, self)
            sw.color_selected.connect(self.color_selected.emit)
            self._swatches.append(sw)
            pen_row.addWidget(sw)

        # Custom color button
        custom_btn = QPushButton("+ Custom")
        custom_btn.setStyleSheet("""
            QPushButton {
                color: #63B3ED; font-size: 10px; font-family: 'Segoe UI';
                background: transparent; border: none; padding: 2px 4px;
            }
            QPushButton:hover { color: #90CDF4; }
        """)
        custom_btn.setCursor(Qt.PointingHandCursor)
        custom_btn.clicked.connect(self._pick_custom_color)
        pen_row.addWidget(custom_btn)
        pen_row.addStretch()
        layout.addLayout(pen_row)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: rgba(255,255,255,15);")
        layout.addWidget(sep)

        # Highlighter colors
        hl_label = QLabel("Highlighter Color")
        hl_label.setStyleSheet("color: #94A3B8; font-size: 10px; font-family: 'Segoe UI';")
        layout.addWidget(hl_label)

        hl_row = QHBoxLayout()
        hl_row.setSpacing(5)
        for c in HIGHLIGHTER_COLORS:
            sw = ColorSwatch(c, 20, self)
            sw.color_selected.connect(self.highlight_color_selected.emit)
            hl_row.addWidget(sw)
        hl_row.addStretch()
        layout.addLayout(hl_row)

    def _pick_custom_color(self):
        color = QColorDialog.getColor(parent=self)
        if color.isValid():
            self.color_selected.emit(color)
        self.close()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 14, 14)
        p.setPen(QPen(QColor(255, 255, 255, 20), 1))
        p.setBrush(QBrush(QColor(15, 23, 42, 240)))
        p.drawPath(path)
        p.end()


# ── Active Color Indicator ─────────────────────────────────────────────────

class ColorIndicator(QWidget):
    """Shows the currently selected pen and highlight color."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pen_color = QColor("#E74C3C")
        self.hl_color = QColor("#FFF176")
        self.setFixedSize(36, 36)
        self.setToolTip("Active colors")

    def set_pen_color(self, c: QColor):
        self.pen_color = c
        self.update()

    def set_hl_color(self, c: QColor):
        self.hl_color = c
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        # Highlight swatch (background)
        hl = QColor(self.hl_color)
        hl.setAlpha(180)
        p.setPen(QPen(QColor(255, 255, 255, 30), 1))
        p.setBrush(QBrush(hl))
        p.drawEllipse(10, 10, 22, 22)
        # Pen swatch (foreground)
        p.setPen(QPen(QColor(255, 255, 255, 60), 1.5))
        p.setBrush(QBrush(self.pen_color))
        p.drawEllipse(2, 2, 22, 22)
        p.end()


# ── Main Toolbar ───────────────────────────────────────────────────────────

class InkPenToolbar(QWidget):
    """Floating always-on-top toolbar for InkPen."""

    tool_changed = pyqtSignal(Tool)
    shape_changed = pyqtSignal(Shape)
    pen_color_changed = pyqtSignal(QColor)
    hl_color_changed = pyqtSignal(QColor)
    pen_size_changed = pyqtSignal(int)
    clear_all_requested = pyqtSignal()
    undo_requested = pyqtSignal()
    close_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._drag_pos = None
        self._current_tool = Tool.CURSOR
        self._tool_buttons: dict[Tool, ToolButton] = {}

        self._setup_window()
        self._setup_ui()
        self._set_tool(Tool.CURSOR)

    def _setup_window(self):
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        # Shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 120))
        self.setGraphicsEffect(shadow)

    def _setup_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Main container
        self._container = QWidget(self)
        self._container.setObjectName("container")
        outer.addWidget(self._container)

        main_layout = QVBoxLayout(self._container)
        main_layout.setContentsMargins(8, 6, 8, 8)
        main_layout.setSpacing(4)

        # Title bar
        title_bar = QHBoxLayout()
        title_bar.setSpacing(4)

        # Drag handle
        drag_lbl = QLabel()
        drag_pix = svg_to_pixmap(ICON_DRAG, 16, "#475569")
        drag_lbl.setPixmap(drag_pix)
        drag_lbl.setFixedSize(20, 20)
        drag_lbl.setToolTip("Drag to move")
        title_bar.addWidget(drag_lbl)

        # App name
        title = QLabel("InkPen")
        title.setStyleSheet("""
            color: #CBD5E1;
            font-family: 'Segoe UI', sans-serif;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 1px;
        """)
        title_bar.addWidget(title)
        title_bar.addStretch()

        # Undo button
        undo_btn = QPushButton()
        undo_btn.setFixedSize(22, 22)
        undo_btn.setIcon(svg_to_icon(ICON_UNDO, 14, "#64748B"))
        undo_btn.setIconSize(QSize(14, 14))
        undo_btn.setToolTip("Undo (Ctrl+Z)")
        undo_btn.setCursor(Qt.PointingHandCursor)
        undo_btn.setStyleSheet("""
            QPushButton { background: transparent; border: none; border-radius: 4px; }
            QPushButton:hover { background: rgba(255,255,255,15); }
        """)
        undo_btn.clicked.connect(self.undo_requested.emit)
        title_bar.addWidget(undo_btn)

        # Close button
        close_btn = QPushButton()
        close_btn.setFixedSize(22, 22)
        close_btn.setIcon(svg_to_icon(ICON_CLOSE, 12, "#64748B"))
        close_btn.setIconSize(QSize(12, 12))
        close_btn.setToolTip("Exit InkPen")
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton { background: transparent; border: none; border-radius: 4px; }
            QPushButton:hover { background: rgba(239,68,68,180); }
        """)
        close_btn.clicked.connect(self.close_requested.emit)
        title_bar.addWidget(close_btn)

        main_layout.addLayout(title_bar)

        # Divider
        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setFixedHeight(1)
        div.setStyleSheet("background: rgba(255,255,255,12); margin: 0 2px;")
        main_layout.addWidget(div)

        # ── Tool Row ────────────────────────────────────────────────────────
        tool_row = QHBoxLayout()
        tool_row.setSpacing(2)
        tool_row.setContentsMargins(0, 4, 0, 0)

        def add_btn(tool, icon_svg, tip):
            btn = ToolButton(icon_svg, tip, self._container)
            btn.clicked.connect(lambda: self._set_tool(tool))
            self._tool_buttons[tool] = btn
            tool_row.addWidget(btn)
            return btn

        add_btn(Tool.CURSOR, ICON_CURSOR, "Cursor (select/click-through)")
        tool_row.addWidget(ToolbarSeparator())

        add_btn(Tool.PEN, ICON_PEN, "Pen")
        add_btn(Tool.HIGHLIGHTER, ICON_HIGHLIGHTER, "Highlighter")

        # Pen size
        size_btn = ToolButton(ICON_PEN_SIZE, "Pen Size", self._container)
        size_btn.clicked.connect(self._show_size_popup)
        tool_row.addWidget(size_btn)
        self._size_btn = size_btn

        tool_row.addWidget(ToolbarSeparator())

        add_btn(Tool.TEXT, ICON_TEXT, "Text Tool")

        # Shape selector
        shape_btn = ToolButton(ICON_SHAPE, "Shape", self._container)
        shape_btn.clicked.connect(self._show_shape_popup)
        self._tool_buttons[Tool.SHAPE] = shape_btn
        shape_btn.clicked.connect(lambda: self._set_tool(Tool.SHAPE))
        tool_row.addWidget(shape_btn)

        tool_row.addWidget(ToolbarSeparator())
        add_btn(Tool.ERASER, ICON_ERASER, "Eraser (removes full strokes)")

        tool_row.addWidget(ToolbarSeparator())

        # Color indicator + color picker
        self._color_indicator = ColorIndicator(self._container)
        self._color_indicator.setCursor(Qt.PointingHandCursor)
        self._color_indicator.mousePressEvent = lambda e: self._show_color_popup()
        tool_row.addWidget(self._color_indicator)

        color_btn = ToolButton(ICON_COLOR_PICKER, "Colors", self._container)
        color_btn.clicked.connect(self._show_color_popup)
        tool_row.addWidget(color_btn)

        tool_row.addWidget(ToolbarSeparator())

        # Delete all
        trash_btn = ToolButton(ICON_TRASH, "Clear All (delete everything)", self._container)
        trash_btn.clicked.connect(self._confirm_clear)
        tool_row.addWidget(trash_btn)

        main_layout.addLayout(tool_row)

        # Adjust size
        self.adjustSize()
        self.setMinimumWidth(460)

    # ── Tool Selection ─────────────────────────────────────────────────────

    def _set_tool(self, tool: Tool):
        self._current_tool = tool
        for t, btn in self._tool_buttons.items():
            btn.set_active(t == tool)
        self.tool_changed.emit(tool)

    # ── Popups ─────────────────────────────────────────────────────────────

    def _show_size_popup(self):
        popup = PenSizePopup(self)
        popup.size_selected.connect(self._on_size_selected)
        popup.size_selected.connect(popup.close)
        btn_pos = self._size_btn.mapToGlobal(
            QPoint(self._size_btn.width() // 2, self._size_btn.height() + 4))
        popup.adjustSize()
        popup.move(btn_pos.x() - popup.width() // 2, btn_pos.y())
        popup.show()

    def _on_size_selected(self, size: int):
        self.pen_size_changed.emit(size)

    def _show_shape_popup(self):
        btn = self._tool_buttons[Tool.SHAPE]
        popup = ShapePopup(self)
        popup.shape_selected.connect(self._on_shape_selected)
        popup.shape_selected.connect(popup.close)
        btn_pos = btn.mapToGlobal(QPoint(btn.width() // 2, btn.height() + 4))
        popup.adjustSize()
        popup.move(btn_pos.x() - popup.width() // 2, btn_pos.y())
        popup.show()

    def _on_shape_selected(self, shape: Shape):
        self.shape_changed.emit(shape)
        self._set_tool(Tool.SHAPE)

    def _show_color_popup(self):
        popup = ColorPopup(self)
        popup.color_selected.connect(self._on_pen_color_selected)
        popup.color_selected.connect(lambda: popup.close())
        popup.highlight_color_selected.connect(self._on_hl_color_selected)
        popup.highlight_color_selected.connect(lambda: popup.close())

        # Position below toolbar
        tb_pos = self.mapToGlobal(QPoint(self.width() // 2, self.height() + 4))
        popup.adjustSize()
        popup.move(tb_pos.x() - popup.width() // 2, tb_pos.y())
        popup.show()

    def _on_pen_color_selected(self, color: QColor):
        self._color_indicator.set_pen_color(color)
        self.pen_color_changed.emit(color)

    def _on_hl_color_selected(self, color: QColor):
        self._color_indicator.set_hl_color(color)
        self.hl_color_changed.emit(color)

    def _confirm_clear(self):
        """Show a small confirm popup before clearing."""
        popup = QWidget(self, Qt.Popup | Qt.FramelessWindowHint)
        popup.setAttribute(Qt.WA_TranslucentBackground)
        popup.setFixedSize(200, 72)

        layout = QVBoxLayout(popup)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)

        lbl = QLabel("Clear all drawings?")
        lbl.setStyleSheet("color: #E2E8F0; font-size: 11px; font-family: 'Segoe UI';")
        layout.addWidget(lbl)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)

        cancel = QPushButton("Cancel")
        cancel.setStyleSheet("""
            QPushButton { background: rgba(255,255,255,15); color: #94A3B8;
                          border: none; border-radius: 5px; padding: 4px 10px;
                          font-size: 10px; font-family: 'Segoe UI'; }
            QPushButton:hover { background: rgba(255,255,255,25); }
        """)
        cancel.setCursor(Qt.PointingHandCursor)
        cancel.clicked.connect(popup.close)
        btn_row.addWidget(cancel)

        confirm = QPushButton("Clear All")
        confirm.setStyleSheet("""
            QPushButton { background: rgba(239,68,68,180); color: white;
                          border: none; border-radius: 5px; padding: 4px 10px;
                          font-size: 10px; font-family: 'Segoe UI'; font-weight: 600; }
            QPushButton:hover { background: rgba(239,68,68,220); }
        """)
        confirm.setCursor(Qt.PointingHandCursor)
        confirm.clicked.connect(popup.close)
        confirm.clicked.connect(self.clear_all_requested.emit)
        btn_row.addWidget(confirm)
        layout.addLayout(btn_row)

        # Paint background
        def paint_bg(event):
            p = QPainter(popup)
            p.setRenderHint(QPainter.Antialiasing)
            path = QPainterPath()
            path.addRoundedRect(0, 0, popup.width(), popup.height(), 12, 12)
            p.setPen(QPen(QColor(255, 255, 255, 20), 1))
            p.setBrush(QBrush(QColor(15, 23, 42, 240)))
            p.drawPath(path)
            p.end()
        popup.paintEvent = paint_bg

        trash_pos = self.mapToGlobal(QPoint(self.width() - 50, self.height() + 4))
        popup.move(trash_pos.x() - popup.width() // 2, trash_pos.y())
        popup.show()

    # ── Paint ──────────────────────────────────────────────────────────────

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(4, 4, -4, -4)

        # Glass background
        path = QPainterPath()
        path.addRoundedRect(rect.x(), rect.y(),
                            rect.width(), rect.height(), 16, 16)

        # Dark glass fill
        grad = QLinearGradient(0, 0, 0, rect.height())
        grad.setColorAt(0, QColor(15, 23, 42, 220))
        grad.setColorAt(1, QColor(8, 15, 30, 235))
        p.setBrush(QBrush(grad))
        p.setPen(Qt.NoPen)
        p.drawPath(path)

        # Border
        p.setPen(QPen(QColor(255, 255, 255, 25), 1))
        p.setBrush(Qt.NoBrush)
        p.drawPath(path)

        # Top highlight line
        p.setPen(QPen(QColor(255, 255, 255, 40), 1))
        p.drawLine(rect.x() + 18, rect.y() + 1,
                   rect.x() + rect.width() - 18, rect.y() + 1)
        p.end()

    # ── Drag to Move ───────────────────────────────────────────────────────

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self._drag_pos:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Z and event.modifiers() & Qt.ControlModifier:
            self.undo_requested.emit()
        super().keyPressEvent(event)
