"""Toolbar widget for InkPen"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QSpinBox, QColorDialog, QComboBox, QSlider, QLabel, QFrame)
from PyQt5.QtGui import QIcon, QColor, QPixmap, QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QTimer
from PyQt5.QtCore import QTimer as QtTimer

from .utils import create_tool_icon
from .tools import ToolType, ShapeType
from .drawing import DrawingCanvas


class ToolBar(QWidget):
    """Always-on-top toolbar for drawing tools"""
    
    tool_selected = pyqtSignal(ToolType)
    pen_size_changed = pyqtSignal(int)
    color_changed = pyqtSignal(QColor)
    shape_selected = pyqtSignal(ShapeType)
    
    def __init__(self, canvas: DrawingCanvas):
        super().__init__()
        self.canvas = canvas
        self.current_color = QColor(0, 0, 0)
        self.current_pen_size = 2
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the toolbar UI"""
        self.setWindowTitle("InkPen - Toolbar")
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #444;
            }
            QPushButton {
                background-color: #3c3c3c;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 6px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4c4c4c;
                border: 1px solid #666;
            }
            QPushButton:pressed {
                background-color: #1c1c1c;
            }
            QPushButton:checked {
                background-color: #0078d4;
                border: 2px solid #0078d4;
            }
            QComboBox {
                background-color: #3c3c3c;
                color: white;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 4px;
            }
            QComboBox QAbstractItemView {
                background-color: #3c3c3c;
                color: white;
                selection-background-color: #0078d4;
            }
            QSpinBox {
                background-color: #3c3c3c;
                color: white;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 4px;
            }
            QSlider::groove:horizontal {
                background-color: #555;
                height: 6px;
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background-color: #0078d4;
                width: 14px;
                margin: -4px 0;
                border-radius: 7px;
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # Tool buttons
        tools_group = QFrame()
        tools_layout = QHBoxLayout()
        tools_layout.setContentsMargins(0, 0, 0, 0)
        tools_layout.setSpacing(4)
        
        # Cursor button
        btn_cursor = QPushButton()
        btn_cursor.setIcon(create_tool_icon(QColor(200, 200, 200), "cursor", 32))
        btn_cursor.setIconSize(QSize(28, 28))
        btn_cursor.setToolTip("Cursor (C)")
        btn_cursor.setCheckable(True)
        btn_cursor.clicked.connect(lambda: self.select_tool(ToolType.CURSOR))
        tools_layout.addWidget(btn_cursor)
        self.btn_cursor = btn_cursor
        
        # Pen button
        btn_pen = QPushButton()
        btn_pen.setIcon(create_tool_icon(QColor(200, 200, 200), "pen", 32))
        btn_pen.setIconSize(QSize(28, 28))
        btn_pen.setToolTip("Pen (P)")
        btn_pen.setCheckable(True)
        btn_pen.setChecked(True)
        btn_pen.clicked.connect(lambda: self.select_tool(ToolType.PEN))
        tools_layout.addWidget(btn_pen)
        self.btn_pen = btn_pen
        
        # Eraser button
        btn_eraser = QPushButton()
        btn_eraser.setIcon(create_tool_icon(QColor(200, 200, 200), "eraser", 32))
        btn_eraser.setIconSize(QSize(28, 28))
        btn_eraser.setToolTip("Eraser (E)")
        btn_eraser.setCheckable(True)
        btn_eraser.clicked.connect(lambda: self.select_tool(ToolType.ERASER))
        tools_layout.addWidget(btn_eraser)
        self.btn_eraser = btn_eraser
        
        # Highlighter button
        btn_highlighter = QPushButton()
        btn_highlighter.setIcon(create_tool_icon(QColor(255, 255, 0), "highlighter", 32))
        btn_highlighter.setIconSize(QSize(28, 28))
        btn_highlighter.setToolTip("Highlighter (H)")
        btn_highlighter.setCheckable(True)
        btn_highlighter.clicked.connect(lambda: self.select_tool(ToolType.HIGHLIGHTER))
        tools_layout.addWidget(btn_highlighter)
        self.btn_highlighter = btn_highlighter
        
        # Color picker button
        btn_color = QPushButton()
        btn_color.setIcon(create_tool_icon(QColor(200, 200, 200), "color", 32))
        btn_color.setIconSize(QSize(28, 28))
        btn_color.setToolTip("Color Picker")
        btn_color.clicked.connect(self.pick_color)
        tools_layout.addWidget(btn_color)
        
        # Shapes button
        btn_shapes = QPushButton()
        btn_shapes.setIcon(create_tool_icon(QColor(200, 200, 200), "shapes", 32))
        btn_shapes.setIconSize(QSize(28, 28))
        btn_shapes.setToolTip("Shapes (S)")
        btn_shapes.setCheckable(True)
        btn_shapes.clicked.connect(lambda: self.select_tool(ToolType.SHAPES))
        tools_layout.addWidget(btn_shapes)
        self.btn_shapes = btn_shapes
        
        # Text button
        btn_text = QPushButton()
        btn_text.setIcon(create_tool_icon(QColor(200, 200, 200), "text", 32))
        btn_text.setIconSize(QSize(28, 28))
        btn_text.setToolTip("Text (T)")
        btn_text.setCheckable(True)
        btn_text.clicked.connect(lambda: self.select_tool(ToolType.TEXT))
        tools_layout.addWidget(btn_text)
        self.btn_text = btn_text
        
        # Delete button
        btn_delete = QPushButton("🗑️ Clear")
        btn_delete.setToolTip("Delete All (Ctrl+D)")
        btn_delete.clicked.connect(self.delete_all)
        tools_layout.addWidget(btn_delete)
        
        tools_group.setLayout(tools_layout)
        layout.addWidget(tools_group)
        
        # Pen size controls
        size_group = QFrame()
        size_layout = QHBoxLayout()
        size_layout.setContentsMargins(0, 0, 0, 0)
        size_layout.setSpacing(6)
        
        size_layout.addWidget(QLabel("Pen Size:"))
        
        size_slider = QSlider(Qt.Horizontal)
        size_slider.setMinimum(1)
        size_slider.setMaximum(50)
        size_slider.setValue(2)
        size_slider.setMaximumWidth(120)
        size_slider.valueChanged.connect(self.on_pen_size_changed)
        size_layout.addWidget(size_slider)
        
        size_spinbox = QSpinBox()
        size_spinbox.setMinimum(1)
        size_spinbox.setMaximum(50)
        size_spinbox.setValue(2)
        size_spinbox.setMaximumWidth(60)
        size_spinbox.valueChanged.connect(lambda v: size_slider.setValue(v))
        size_slider.valueChanged.connect(lambda v: size_spinbox.setValue(v))
        size_layout.addWidget(size_spinbox)
        
        size_group.setLayout(size_layout)
        layout.addWidget(size_group)
        
        # Shape selector
        shape_group = QFrame()
        shape_layout = QHBoxLayout()
        shape_layout.setContentsMargins(0, 0, 0, 0)
        shape_layout.setSpacing(6)
        
        shape_layout.addWidget(QLabel("Shape:"))
        
        shape_combo = QComboBox()
        shape_combo.addItem("Line", ShapeType.LINE)
        shape_combo.addItem("Rectangle", ShapeType.RECTANGLE)
        shape_combo.addItem("Circle", ShapeType.CIRCLE)
        shape_combo.addItem("Ellipse", ShapeType.ELLIPSE)
        shape_combo.currentIndexChanged.connect(
            lambda: self.shape_selected.emit(shape_combo.currentData())
        )
        shape_layout.addWidget(shape_combo)
        
        shape_group.setLayout(shape_layout)
        layout.addWidget(shape_group)
        
        # Color display
        color_group = QFrame()
        color_layout = QHBoxLayout()
        color_layout.setContentsMargins(0, 0, 0, 0)
        color_layout.setSpacing(6)
        
        color_layout.addWidget(QLabel("Color:"))
        
        self.color_preview = QPushButton()
        self.color_preview.setMinimumWidth(60)
        self.color_preview.setMinimumHeight(30)
        self.color_preview.setStyleSheet(
            f"background-color: {self.current_color.name()}; "
            "border: 2px solid #0078d4; border-radius: 4px;"
        )
        self.color_preview.clicked.connect(self.pick_color)
        color_layout.addWidget(self.color_preview)
        
        color_group.setLayout(color_layout)
        layout.addWidget(color_group)
        
        self.setLayout(layout)
        self.setMinimumWidth(350)
        self.adjustSize()
        
        # Position toolbar at top right
        from PyQt5.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        geom = screen.geometry()
        self.move(geom.right() - self.width() - 10, 10)
        
        # Store button references for toggling
        self.tool_buttons = {
            ToolType.CURSOR: btn_cursor,
            ToolType.PEN: btn_pen,
            ToolType.ERASER: btn_eraser,
            ToolType.HIGHLIGHTER: btn_highlighter,
            ToolType.SHAPES: btn_shapes,
            ToolType.TEXT: btn_text,
        }
        
    def select_tool(self, tool_type: ToolType):
        """Select a tool"""
        # Uncheck all tool buttons
        for btn in self.tool_buttons.values():
            btn.setChecked(False)
            
        # Check the selected tool (if it's checkable)
        if tool_type in self.tool_buttons:
            btn = self.tool_buttons[tool_type]
            if btn.isCheckable():
                btn.setChecked(True)
                
        self.canvas.set_tool(tool_type)
        self.tool_selected.emit(tool_type)
        
    def on_pen_size_changed(self, size: int):
        """Handle pen size change"""
        self.current_pen_size = size
        self.canvas.set_pen_size(size)
        self.pen_size_changed.emit(size)
        
    def pick_color(self):
        """Open color picker dialog"""
        color = QColorDialog.getColor(self.current_color, self, "Pick Color")
        if color.isValid():
            self.current_color = color
            self.update_color_preview()
            self.canvas.set_pen_color(color)
            self.color_changed.emit(color)
            
    def update_color_preview(self):
        """Update color preview button"""
        self.color_preview.setStyleSheet(
            f"background-color: {self.current_color.name()}; "
            "border: 2px solid #0078d4; border-radius: 4px;"
        )
        
    def delete_all(self):
        """Delete all drawings"""
        self.canvas.clear_canvas()
