"""
InkPen - Transparent Drawing Canvas Overlay
Full-screen transparent window that captures drawing input
"""
import ctypes
import ctypes.wintypes
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import math

from PyQt5.QtWidgets import QWidget, QApplication, QInputDialog
from PyQt5.QtCore import Qt, QPoint, QPointF, QRectF, pyqtSignal, QTimer
from PyQt5.QtGui import (
    QPainter, QPainterPath, QPen, QColor, QFont, QBrush,
    QFontMetrics, QCursor, QPixmap
)

from tools import Tool, Shape


@dataclass
class Stroke:
    """Represents a single drawn stroke."""
    tool: Tool
    points: List[QPointF] = field(default_factory=list)
    color: QColor = field(default_factory=lambda: QColor("#E74C3C"))
    size: int = 3
    opacity: int = 255
    shape: Optional[Shape] = None
    # For shapes: start and end points
    start: Optional[QPointF] = None
    end: Optional[QPointF] = None
    # For text
    text: str = ""
    font_size: int = 18
    # Bounding box cache
    _path_cache: Optional[QPainterPath] = field(default=None, repr=False)

    def get_path(self) -> QPainterPath:
        """Get the painter path for this stroke."""
        if self.tool == Tool.PEN or self.tool == Tool.HIGHLIGHTER:
            if len(self.points) < 2:
                return QPainterPath()
            path = QPainterPath()
            path.moveTo(self.points[0])
            if len(self.points) == 2:
                path.lineTo(self.points[1])
            else:
                # Smooth curve through points
                for i in range(1, len(self.points) - 1):
                    mid = QPointF(
                        (self.points[i].x() + self.points[i+1].x()) / 2,
                        (self.points[i].y() + self.points[i+1].y()) / 2
                    )
                    path.quadTo(self.points[i], mid)
                path.lineTo(self.points[-1])
            return path
        return QPainterPath()

    def hit_test(self, point: QPointF, tolerance: float = 15.0) -> bool:
        """Check if a point hits this stroke."""
        if self.tool in (Tool.PEN, Tool.HIGHLIGHTER):
            path = self.get_path()
            if path.isEmpty():
                return False
            stroker_path = QPainterPath()
            # Check distance to path
            for i in range(len(self.points) - 1):
                p1 = self.points[i]
                p2 = self.points[i + 1]
                dist = point_to_segment_distance(point, p1, p2)
                if dist <= tolerance + self.size / 2:
                    return True
            return False
        elif self.tool == Tool.SHAPE and self.start and self.end:
            # Hit test on shape outline
            rect = QRectF(self.start, self.end).normalized()
            hit_tolerance = tolerance
            if self.shape == Shape.LINE or self.shape == Shape.ARROW:
                return point_to_segment_distance(point, self.start, self.end) <= hit_tolerance
            # For rectangle / ellipse check near border
            expanded = rect.adjusted(-hit_tolerance, -hit_tolerance, hit_tolerance, hit_tolerance)
            shrunk = rect.adjusted(hit_tolerance, hit_tolerance, -hit_tolerance, -hit_tolerance)
            return expanded.contains(point) and not shrunk.contains(point)
        elif self.tool == Tool.TEXT and self.start:
            # Hit test near text position
            font = QFont("Arial", self.font_size)
            fm = QFontMetrics(font)
            text_rect = QRectF(self.start.x(), self.start.y() - self.font_size,
                               fm.horizontalAdvance(self.text) + 10, self.font_size + 10)
            return text_rect.contains(point)
        return False


def point_to_segment_distance(p: QPointF, a: QPointF, b: QPointF) -> float:
    """Compute minimum distance from point p to segment [a, b]."""
    dx = b.x() - a.x()
    dy = b.y() - a.y()
    if dx == 0 and dy == 0:
        return math.hypot(p.x() - a.x(), p.y() - a.y())
    t = ((p.x() - a.x()) * dx + (p.y() - a.y()) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    nearest_x = a.x() + t * dx
    nearest_y = a.y() + t * dy
    return math.hypot(p.x() - nearest_x, p.y() - nearest_y)


class DrawingCanvas(QWidget):
    """
    Full-screen transparent overlay widget for drawing.
    Sits above all windows; mouse events are captured when drawing tools are active.
    """
    stroke_added = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Drawing state
        self.strokes: List[Stroke] = []
        self.undo_stack: List[List[Stroke]] = []
        self.current_stroke: Optional[Stroke] = None
        self.is_drawing = False

        # Tool settings
        self.current_tool = Tool.CURSOR
        self.pen_color = QColor("#E74C3C")
        self.pen_size = 3
        self.highlighter_color = QColor("#FFF176")
        self.highlighter_size = 20
        self.current_shape = Shape.RECTANGLE
        self.text_font_size = 18

        # Text input
        self.text_input_pos: Optional[QPointF] = None
        self.text_cursor_visible = True
        self.text_cursor_timer = QTimer(self)
        self.text_cursor_timer.timeout.connect(self._blink_cursor)
        self.current_text = ""

        self._setup_window()
        self._apply_click_through(False)

    def _setup_window(self):
        screen = QApplication.primaryScreen().geometry()
        # Span all screens
        all_screens = QApplication.screens()
        if all_screens:
            combined = all_screens[0].geometry()
            for s in all_screens[1:]:
                combined = combined.united(s.geometry())
            self.setGeometry(combined)
        else:
            self.setGeometry(screen)

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool |
            Qt.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_AcceptTouchEvents, False)
        self.setMouseTracking(True)

    def _apply_click_through(self, passthrough: bool):
        """Toggle Windows click-through via extended window style."""
        try:
            hwnd = int(self.winId())
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x00080000
            WS_EX_TRANSPARENT = 0x00000020

            user32 = ctypes.windll.user32
            ex_style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)

            if passthrough:
                ex_style |= (WS_EX_LAYERED | WS_EX_TRANSPARENT)
            else:
                ex_style &= ~WS_EX_TRANSPARENT
                ex_style |= WS_EX_LAYERED

            user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex_style)
        except Exception:
            pass  # Non-Windows fallback

    def set_tool(self, tool: Tool):
        self.current_tool = tool
        self.text_cursor_timer.stop()

        if tool == Tool.CURSOR:
            self._apply_click_through(True)
            self.setCursor(Qt.ArrowCursor)
        elif tool == Tool.ERASER:
            self._apply_click_through(False)
            self.setCursor(self._make_eraser_cursor())
        elif tool == Tool.TEXT:
            self._apply_click_through(False)
            self.setCursor(Qt.IBeamCursor)
        else:
            self._apply_click_through(False)
            self.setCursor(self._make_pen_cursor())
        self.update()

    def _make_eraser_cursor(self) -> QCursor:
        size = max(self.pen_size * 2 + 4, 20)
        pix = QPixmap(size, size)
        pix.fill(Qt.transparent)
        p = QPainter(pix)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(QPen(QColor(200, 200, 200, 220), 2))
        p.setBrush(QBrush(QColor(255, 255, 255, 60)))
        p.drawEllipse(1, 1, size - 2, size - 2)
        p.end()
        return QCursor(pix, size // 2, size // 2)

    def _make_pen_cursor(self) -> QCursor:
        pix = QPixmap(20, 20)
        pix.fill(Qt.transparent)
        p = QPainter(pix)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(QPen(QColor(255, 255, 255), 1.5))
        # Draw crosshair
        p.drawLine(10, 2, 10, 18)
        p.drawLine(2, 10, 18, 10)
        p.setPen(QPen(QColor(0, 0, 0), 0.5))
        p.drawLine(10, 2, 10, 18)
        p.drawLine(2, 10, 18, 10)
        p.end()
        return QCursor(pix, 10, 10)

    def _blink_cursor(self):
        self.text_cursor_visible = not self.text_cursor_visible
        self.update()

    # ── Drawing Inputs ─────────────────────────────────────────────────────

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return

        pos = QPointF(event.pos())

        if self.current_tool == Tool.CURSOR:
            return

        if self.current_tool == Tool.ERASER:
            self._erase_at(pos)
            self.is_drawing = True
            return

        if self.current_tool == Tool.TEXT:
            self._start_text_input(pos)
            return

        # Save undo state
        self.undo_stack.append([s for s in self.strokes])

        color = self.highlighter_color if self.current_tool == Tool.HIGHLIGHTER else self.pen_color
        size = self.highlighter_size if self.current_tool == Tool.HIGHLIGHTER else self.pen_size
        opacity = 120 if self.current_tool == Tool.HIGHLIGHTER else 255

        self.current_stroke = Stroke(
            tool=self.current_tool,
            color=QColor(color),
            size=size,
            opacity=opacity,
            shape=self.current_shape if self.current_tool == Tool.SHAPE else None,
            start=pos,
            end=pos,
        )
        self.current_stroke.points.append(pos)
        self.is_drawing = True
        self.update()

    def mouseMoveEvent(self, event):
        pos = QPointF(event.pos())

        if self.current_tool == Tool.ERASER and self.is_drawing:
            self._erase_at(pos)
            return

        if not self.is_drawing or not self.current_stroke:
            return

        if self.current_tool in (Tool.PEN, Tool.HIGHLIGHTER):
            self.current_stroke.points.append(pos)
        elif self.current_tool == Tool.SHAPE:
            self.current_stroke.end = pos

        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() != Qt.LeftButton:
            return

        if self.current_tool == Tool.ERASER:
            self.is_drawing = False
            return

        if self.is_drawing and self.current_stroke:
            if self.current_tool == Tool.SHAPE:
                self.current_stroke.end = QPointF(event.pos())
            self.strokes.append(self.current_stroke)
            self.current_stroke = None
            self.stroke_added.emit()

        self.is_drawing = False
        self.update()

    # ── Eraser Logic ───────────────────────────────────────────────────────

    def _erase_at(self, pos: QPointF):
        """Remove entire strokes that the eraser touches."""
        to_remove = []
        for stroke in self.strokes:
            if stroke.hit_test(pos, tolerance=max(self.pen_size * 2, 12)):
                to_remove.append(stroke)

        if to_remove:
            # Save undo snapshot
            if not self.is_drawing:
                self.undo_stack.append([s for s in self.strokes])
            for s in to_remove:
                self.strokes.remove(s)
            self.update()

    # ── Text Input ─────────────────────────────────────────────────────────

    def _start_text_input(self, pos: QPointF):
        """Begin text input at given position."""
        self.text_input_pos = pos
        self.current_text = ""
        self.text_cursor_visible = True
        self.text_cursor_timer.start(500)

        # Use dialog for text input
        text, ok = QInputDialog.getText(
            self, "Insert Text", "Enter text:",
        )
        self.text_cursor_timer.stop()
        self.text_input_pos = None
        self.current_text = ""

        if ok and text.strip():
            self.undo_stack.append([s for s in self.strokes])
            stroke = Stroke(
                tool=Tool.TEXT,
                color=QColor(self.pen_color),
                size=self.pen_size,
                opacity=255,
                text=text,
                font_size=self.text_font_size,
                start=pos,
            )
            self.strokes.append(stroke)
            self.stroke_added.emit()
            self.update()

    # ── Actions ────────────────────────────────────────────────────────────

    def clear_all(self):
        """Remove all strokes from the canvas."""
        if self.strokes:
            self.undo_stack.append([s for s in self.strokes])
            self.strokes.clear()
            self.update()

    def undo(self):
        """Undo last drawing action."""
        if self.undo_stack:
            self.strokes = self.undo_stack.pop()
            self.update()

    # ── Painting ───────────────────────────────────────────────────────────

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        # Draw committed strokes
        for stroke in self.strokes:
            self._draw_stroke(painter, stroke)

        # Draw in-progress stroke
        if self.current_stroke:
            self._draw_stroke(painter, self.current_stroke)

        painter.end()

    def _draw_stroke(self, painter: QPainter, stroke: Stroke):
        color = QColor(stroke.color)
        color.setAlpha(stroke.opacity)

        if stroke.tool in (Tool.PEN, Tool.HIGHLIGHTER):
            if len(stroke.points) < 2:
                if len(stroke.points) == 1:
                    pen = QPen(color, stroke.size, Qt.SolidLine, Qt.RoundCap)
                    painter.setPen(pen)
                    p = stroke.points[0]
                    painter.drawPoint(p.toPoint())
                return

            if stroke.tool == Tool.HIGHLIGHTER:
                pen = QPen(color, stroke.size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            else:
                pen = QPen(color, stroke.size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            path = stroke.get_path()
            painter.drawPath(path)

        elif stroke.tool == Tool.SHAPE and stroke.start and stroke.end:
            pen = QPen(color, stroke.size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

            rect = QRectF(stroke.start, stroke.end).normalized()

            if stroke.shape == Shape.LINE:
                painter.drawLine(stroke.start, stroke.end)

            elif stroke.shape == Shape.ARROW:
                self._draw_arrow(painter, stroke.start, stroke.end, color, stroke.size)

            elif stroke.shape == Shape.RECTANGLE:
                painter.drawRoundedRect(rect, 3, 3)

            elif stroke.shape == Shape.ELLIPSE:
                painter.drawEllipse(rect)

            elif stroke.shape == Shape.TRIANGLE:
                cx = (stroke.start.x() + stroke.end.x()) / 2
                top = QPointF(cx, min(stroke.start.y(), stroke.end.y()))
                bl = QPointF(min(stroke.start.x(), stroke.end.x()),
                             max(stroke.start.y(), stroke.end.y()))
                br = QPointF(max(stroke.start.x(), stroke.end.x()),
                             max(stroke.start.y(), stroke.end.y()))
                path = QPainterPath()
                path.moveTo(top)
                path.lineTo(bl)
                path.lineTo(br)
                path.closeSubpath()
                painter.drawPath(path)

        elif stroke.tool == Tool.TEXT and stroke.start and stroke.text:
            font = QFont("Segoe UI", stroke.font_size, QFont.Normal)
            painter.setFont(font)
            painter.setPen(QPen(color))
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            painter.drawText(stroke.start.toPoint(), stroke.text)

    def _draw_arrow(self, painter: QPainter, start: QPointF, end: QPointF,
                    color: QColor, size: int):
        """Draw a line with an arrowhead."""
        painter.drawLine(start, end)

        # Arrowhead
        angle = math.atan2(end.y() - start.y(), end.x() - start.x())
        arrow_len = max(size * 4, 16)
        arrow_angle = math.pi / 7

        p1 = QPointF(
            end.x() - arrow_len * math.cos(angle - arrow_angle),
            end.y() - arrow_len * math.sin(angle - arrow_angle)
        )
        p2 = QPointF(
            end.x() - arrow_len * math.cos(angle + arrow_angle),
            end.y() - arrow_len * math.sin(angle + arrow_angle)
        )

        path = QPainterPath()
        path.moveTo(end)
        path.lineTo(p1)
        path.moveTo(end)
        path.lineTo(p2)
        painter.drawPath(path)
