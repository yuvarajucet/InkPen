"""
InkPen - Main Application Controller
Coordinates toolbar and drawing canvas
"""
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QTimer, QSettings
from PyQt5.QtGui import QColor

from tools import Tool, Shape
from toolbar import InkPenToolbar
from canvas import DrawingCanvas


class InkPenApp:
    """Main application controller."""

    def __init__(self):
        self.toolbar = InkPenToolbar()
        self.canvas = DrawingCanvas()
        self.settings = QSettings("InkPen", "InkPen")

        # Load saved settings
        self._load_settings()

        # Connect signals
        self._connect_signals()

        # Position toolbar in corner
        self.toolbar.move(100, 100)

    def _connect_signals(self):
        """Connect all signal/slot pairs."""
        # Tool changes
        self.toolbar.tool_changed.connect(self._on_tool_changed)
        self.toolbar.shape_changed.connect(self._on_shape_changed)

        # Color changes
        self.toolbar.pen_color_changed.connect(self._on_pen_color_changed)
        self.toolbar.hl_color_changed.connect(self._on_hl_color_changed)

        # Size changes
        self.toolbar.pen_size_changed.connect(self._on_pen_size_changed)

        # Actions
        self.toolbar.clear_all_requested.connect(self.canvas.clear_all)
        self.toolbar.undo_requested.connect(self.canvas.undo)
        self.toolbar.close_requested.connect(self._on_close_requested)

        # Canvas feedback
        self.canvas.stroke_added.connect(self._on_stroke_added)

    def _on_tool_changed(self, tool: Tool):
        """Handle tool selection change."""
        self.canvas.set_tool(tool)
        self.settings.setValue("current_tool", tool.name)

    def _on_shape_changed(self, shape: Shape):
        """Handle shape selection change."""
        self.canvas.current_shape = shape
        self.settings.setValue("current_shape", shape.name)

    def _on_pen_color_changed(self, color: QColor):
        """Handle pen color change."""
        self.canvas.pen_color = color
        self.settings.setValue("pen_color", color.name())

    def _on_hl_color_changed(self, color: QColor):
        """Handle highlighter color change."""
        self.canvas.highlighter_color = color
        self.settings.setValue("hl_color", color.name())

    def _on_pen_size_changed(self, size: int):
        """Handle pen size change."""
        self.canvas.pen_size = size
        self.canvas.highlighter_size = size
        self.settings.setValue("pen_size", size)

    def _on_stroke_added(self):
        """Called when a new stroke is added."""
        pass  # Could add analytics or autosave here

    def _on_close_requested(self):
        """Handle close button click."""
        self._save_settings()
        QApplication.instance().quit()

    def _load_settings(self):
        """Load saved settings from QSettings."""
        # Tool
        tool_name = self.settings.value("current_tool", "CURSOR")
        try:
            tool = Tool[tool_name]
            self.canvas.current_tool = tool
        except KeyError:
            pass

        # Shape
        shape_name = self.settings.value("current_shape", "RECTANGLE")
        try:
            shape = Shape[shape_name]
            self.canvas.current_shape = shape
        except KeyError:
            pass

        # Colors
        pen_color = self.settings.value("pen_color", "#E74C3C")
        self.canvas.pen_color = QColor(pen_color)
        self.toolbar._color_indicator.set_pen_color(self.canvas.pen_color)

        hl_color = self.settings.value("hl_color", "#FFF176")
        self.canvas.highlighter_color = QColor(hl_color)
        self.toolbar._color_indicator.set_hl_color(self.canvas.highlighter_color)

        # Pen size
        pen_size = int(self.settings.value("pen_size", 3))
        self.canvas.pen_size = pen_size
        self.canvas.highlighter_size = pen_size

        # Toolbar position
        toolbar_pos = self.settings.value("toolbar_pos", None)
        if toolbar_pos:
            try:
                x, y = toolbar_pos.split(",")
                self.toolbar.move(int(x), int(y))
            except (ValueError, AttributeError):
                pass

    def _save_settings(self):
        """Save settings to QSettings."""
        # Toolbar position
        pos = self.toolbar.pos()
        self.settings.setValue("toolbar_pos", f"{pos.x()},{pos.y()}")

    def show(self):
        """Show the application."""
        self.canvas.show()
        self.toolbar.show()

    def hide(self):
        """Hide the application."""
        self.canvas.hide()
        self.toolbar.hide()
