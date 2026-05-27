from PyQt6.QtWidgets import QWidget, QApplication, QInputDialog
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QPen, QColor, QFont

from core.constants import Tool
from core.tools import Stroke
from core.shapes import ShapeItem


class OverlayWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)

        self.current_tool = Tool.PEN
        self.current_color = QColor("red")
        self.pen_size = 4

        self.drawing = False
        self.current_points = []

        self.strokes = []
        self.shapes = []
        self.text_items = []

        self.shape_start = None
        self.shape_end = None

        self.showFullScreen()

    def set_tool(self, tool):
        self.current_tool = tool

    def set_color(self, color):
        self.current_color = color

    def set_pen_size(self, size):
        self.pen_size = size

    def clear_all(self):
        self.strokes.clear()
        self.shapes.clear()
        self.text_items.clear()
        self.update()

    def mousePressEvent(self, event):

        if event.button() != Qt.MouseButton.LeftButton:
            return

        pos = event.position().toPoint()

        if self.current_tool in [Tool.PEN, Tool.HIGHLIGHTER]:
            self.drawing = True
            self.current_points = [pos]

        elif self.current_tool in [Tool.RECTANGLE, Tool.ELLIPSE, Tool.LINE]:
            self.shape_start = pos
            self.shape_end = pos
            self.drawing = True

        elif self.current_tool == Tool.ERASER:
            self.erase_stroke(pos)

        elif self.current_tool == Tool.TEXT:
            text, ok = QInputDialog.getText(self, "Text", "Enter Text")
            if ok and text:
                self.text_items.append({
                    "text": text,
                    "position": pos,
                    "color": self.current_color,
                    "size": self.pen_size * 4
                })
                self.update()

    def mouseMoveEvent(self, event):

        pos = event.position().toPoint()

        if self.drawing:

            if self.current_tool in [Tool.PEN, Tool.HIGHLIGHTER]:
                self.current_points.append(pos)
                self.update()

            elif self.current_tool in [Tool.RECTANGLE, Tool.ELLIPSE, Tool.LINE]:
                self.shape_end = pos
                self.update()

    def mouseReleaseEvent(self, event):

        if event.button() != Qt.MouseButton.LeftButton:
            return

        if self.current_tool in [Tool.PEN, Tool.HIGHLIGHTER]:

            stroke = Stroke(
                points=self.current_points.copy(),
                color=self.current_color,
                width=self.pen_size,
                tool=self.current_tool
            )

            self.strokes.append(stroke)

        elif self.current_tool in [Tool.RECTANGLE, Tool.ELLIPSE, Tool.LINE]:

            shape = ShapeItem(
                start=self.shape_start,
                end=self.shape_end,
                color=self.current_color,
                width=self.pen_size,
                shape_type=self.current_tool
            )

            self.shapes.append(shape)

        self.drawing = False
        self.current_points = []
        self.shape_start = None
        self.shape_end = None

        self.update()

    def erase_stroke(self, pos):

        for stroke in list(self.strokes):
            for point in stroke.points:
                if abs(point.x() - pos.x()) < 20 and abs(point.y() - pos.y()) < 20:
                    self.strokes.remove(stroke)
                    self.update()
                    return

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        for stroke in self.strokes:

            color = QColor(stroke.color)

            if stroke.tool == Tool.HIGHLIGHTER:
                color.setAlpha(90)

            pen = QPen(color, stroke.width)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)

            painter.setPen(pen)

            for i in range(1, len(stroke.points)):
                painter.drawLine(stroke.points[i - 1], stroke.points[i])

        if self.drawing and self.current_tool in [Tool.PEN, Tool.HIGHLIGHTER]:

            temp_color = QColor(self.current_color)

            if self.current_tool == Tool.HIGHLIGHTER:
                temp_color.setAlpha(90)

            pen = QPen(temp_color, self.pen_size)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)

            painter.setPen(pen)

            for i in range(1, len(self.current_points)):
                painter.drawLine(self.current_points[i - 1], self.current_points[i])

        for shape in self.shapes:

            pen = QPen(shape.color, shape.width)
            painter.setPen(pen)

            rect = QRect(shape.start, shape.end)

            if shape.shape_type == Tool.RECTANGLE:
                painter.drawRect(rect)

            elif shape.shape_type == Tool.ELLIPSE:
                painter.drawEllipse(rect)

            elif shape.shape_type == Tool.LINE:
                painter.drawLine(shape.start, shape.end)

        for item in self.text_items:

            painter.setPen(QPen(item["color"]))

            font = QFont()
            font.setPointSize(item["size"])

            painter.setFont(font)

            painter.drawText(item["position"], item["text"])