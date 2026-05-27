"""Drawing canvas and rendering for InkPen"""

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import (QPainter, QPen, QColor, QImage, QBrush, QFont, 
                         QPolygon, QCursor)
from PyQt5.QtCore import Qt, QPoint, QRect, pyqtSignal, QTimer, QSize
from PyQt5.QtCore import QTimer as QtTimer
import math
from typing import Optional, Tuple, List

from .tools import Stroke, ToolType, DrawingState, ShapeType
from .utils import point_to_line_distance


class DrawingCanvas(QWidget):
    """The main drawing canvas overlay"""
    
    stroke_updated = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.drawing_state = DrawingState()
        self.current_stroke: Optional[Stroke] = None
        self.canvas_image = QImage()
        self.is_drawing = False
        self.last_point = QPoint()
        self.current_shape_start = None
        self.eraser_radius = 10
        self.shape_type = ShapeType.LINE
        self.text_input = ""
        self.last_text_pos = None
        
        # Performance optimization
        self.dirty_rect = QRect()
        self.update_timer = QtTimer()
        self.update_timer.timeout.connect(self.on_update_timer)
        self.update_timer.start(16)  # ~60 FPS
        
        # Set transparent background
        self.setStyleSheet("background-color: transparent;")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.set_tool(self.drawing_state.current_tool)
        
    def clear_canvas(self):
        """Clear all drawn content"""
        self.drawing_state.clear_all()
        self.canvas_image.fill(Qt.transparent)
        self.update()
        
    def set_tool(self, tool_type: ToolType):
        """Set the current drawing tool"""
        self.drawing_state.current_tool = tool_type
        # Cursor mode is browse-only; draw tools must capture mouse input.
        self.setAttribute(
            Qt.WA_TransparentForMouseEvents,
            tool_type == ToolType.CURSOR
        )
        self.update_cursor(tool_type)
        
    def set_pen_size(self, size: int):
        """Set the pen size"""
        self.drawing_state.pen_size = max(1, min(50, size))
        
    def set_pen_color(self, color: QColor):
        """Set the pen color"""
        self.drawing_state.pen_color = color
        
    def set_shape_type(self, shape_type: ShapeType):
        """Set the shape type for shape tool"""
        self.shape_type = shape_type
        
    def update_cursor(self, tool_type: ToolType):
        """Update the cursor based on current tool"""
        if tool_type == ToolType.PEN:
            self.setCursor(QCursor(Qt.CrossCursor))
        elif tool_type == ToolType.ERASER:
            self.setCursor(QCursor(Qt.CrossCursor))
        elif tool_type == ToolType.COLOR_PICKER:
            self.setCursor(QCursor(Qt.CrossCursor))
        elif tool_type == ToolType.TEXT:
            self.setCursor(QCursor(Qt.IBeamCursor))
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))
            
    def mousePressEvent(self, event):
        """Handle mouse press"""
        if event.button() != Qt.LeftButton:
            return
            
        pos = event.pos()
        tool = self.drawing_state.current_tool
        
        if tool == ToolType.COLOR_PICKER:
            self.pick_color(pos)
            return
            
        if tool == ToolType.TEXT:
            self.last_text_pos = pos
            return
            
        self.is_drawing = True
        self.last_point = pos
        self.current_shape_start = pos
        
        if tool in [ToolType.PEN, ToolType.HIGHLIGHTER]:
            stroke = Stroke(0, tool)
            stroke.color = self.drawing_state.pen_color if tool == ToolType.PEN else self.drawing_state.highlighter_color
            stroke.pen_size = self.drawing_state.pen_size
            stroke.add_point((pos.x(), pos.y()))
            self.current_stroke = stroke
            
    def mouseMoveEvent(self, event):
        """Handle mouse move"""
        if not self.is_drawing:
            return
            
        pos = event.pos()
        tool = self.drawing_state.current_tool
        
        if tool == ToolType.PEN or tool == ToolType.HIGHLIGHTER:
            if self.current_stroke:
                self.current_stroke.add_point((pos.x(), pos.y()))
                self.dirty_rect = QRect(
                    min(self.last_point.x(), pos.x()) - self.drawing_state.pen_size,
                    min(self.last_point.y(), pos.y()) - self.drawing_state.pen_size,
                    abs(pos.x() - self.last_point.x()) + self.drawing_state.pen_size * 2,
                    abs(pos.y() - self.last_point.y()) + self.drawing_state.pen_size * 2
                )
                self.update(self.dirty_rect)
                
        elif tool == ToolType.ERASER:
            self.erase_at(pos)
            
        self.last_point = pos
        
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if event.button() != Qt.LeftButton:
            return
            
        tool = self.drawing_state.current_tool
        
        if tool in [ToolType.PEN, ToolType.HIGHLIGHTER] and self.current_stroke:
            self.drawing_state.add_stroke(self.current_stroke)
            self.current_stroke = None
            
        elif tool == ToolType.SHAPES and self.current_shape_start:
            pos = event.pos()
            self.draw_shape(self.current_shape_start, pos)
            self.current_shape_start = None
            
        self.is_drawing = False
        self.update()
        self.stroke_updated.emit()
        
    def erase_at(self, pos: QPoint):
        """Erase strokes at the given position"""
        pos_tuple = (pos.x(), pos.y())
        strokes_to_remove = []
        
        for stroke in self.drawing_state.strokes:
            if stroke.tool_type == ToolType.TEXT:
                continue
                
            # Check if any point in the stroke is within eraser radius
            for point in stroke.points:
                dx = point[0] - pos.x()
                dy = point[1] - pos.y()
                dist = math.sqrt(dx * dx + dy * dy)
                
                if dist <= self.eraser_radius:
                    strokes_to_remove.append(stroke)
                    break
                    
        for stroke in strokes_to_remove:
            self.drawing_state.remove_connected_strokes(stroke)
            
        self.update()
        
    def pick_color(self, pos: QPoint):
        """Pick color from screen"""
        # For now, open color picker dialog
        from PyQt5.QtWidgets import QColorDialog
        color = QColorDialog.getColor(self.drawing_state.pen_color, self, "Pick Color")
        if color.isValid():
            self.drawing_state.pen_color = color
            
    def draw_shape(self, start_pos: QPoint, end_pos: QPoint):
        """Draw a shape"""
        stroke = Stroke(0, ToolType.SHAPES)
        stroke.color = self.drawing_state.pen_color
        stroke.pen_size = self.drawing_state.pen_size
        stroke.shape_type = self.shape_type
        stroke.points = [(start_pos.x(), start_pos.y()), (end_pos.x(), end_pos.y())]
        self.drawing_state.add_stroke(stroke)
        
    def on_update_timer(self):
        """Update timer callback"""
        if self.is_drawing:
            self.update()
            
    def paintEvent(self, event):
        """Paint the canvas"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # Draw background (transparent)
        painter.fillRect(self.rect(), Qt.transparent)
        
        # Draw all strokes
        for stroke in self.drawing_state.strokes:
            self.draw_stroke(painter, stroke)
            
        # Draw current stroke being drawn
        if self.current_stroke and self.current_stroke.points:
            self.draw_stroke(painter, self.current_stroke)
            
        # Draw eraser preview
        if self.is_drawing and self.drawing_state.current_tool == ToolType.ERASER:
            painter.setPen(QPen(QColor(200, 200, 200, 100), 1, Qt.DashLine))
            painter.drawEllipse(self.last_point, self.eraser_radius, self.eraser_radius)
            
    def draw_stroke(self, painter: QPainter, stroke: Stroke):
        """Draw a single stroke"""
        if not stroke.points:
            return
            
        if stroke.tool_type == ToolType.SHAPES:
            self.draw_shape_stroke(painter, stroke)
        elif stroke.tool_type == ToolType.TEXT:
            self.draw_text_stroke(painter, stroke)
        else:
            # Draw pen or highlighter stroke
            color = stroke.color
            pen = QPen(color, stroke.pen_size)
            pen.setCapStyle(Qt.RoundCap)
            pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen)
            
            if len(stroke.points) > 1:
                for i in range(len(stroke.points) - 1):
                    p1 = QPoint(stroke.points[i][0], stroke.points[i][1])
                    p2 = QPoint(stroke.points[i + 1][0], stroke.points[i + 1][1])
                    painter.drawLine(p1, p2)
            else:
                # Draw a point for single-point stroke
                painter.drawPoint(stroke.points[0][0], stroke.points[0][1])
                
    def draw_shape_stroke(self, painter: QPainter, stroke: Stroke):
        """Draw a shape stroke"""
        if len(stroke.points) < 2:
            return
            
        p1 = stroke.points[0]
        p2 = stroke.points[1]
        
        pen = QPen(stroke.color, stroke.pen_size)
        painter.setPen(pen)
        
        if stroke.shape_type == ShapeType.LINE:
            painter.drawLine(QPoint(p1[0], p1[1]), QPoint(p2[0], p2[1]))
        elif stroke.shape_type == ShapeType.RECTANGLE:
            rect = QRect(p1[0], p1[1], p2[0] - p1[0], p2[1] - p1[1])
            painter.drawRect(rect.normalized())
        elif stroke.shape_type == ShapeType.CIRCLE:
            radius = int(((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5)
            painter.drawEllipse(QPoint(p1[0], p1[1]), radius, radius)
        elif stroke.shape_type == ShapeType.ELLIPSE:
            rect = QRect(p1[0], p1[1], p2[0] - p1[0], p2[1] - p1[1])
            painter.drawEllipse(rect.normalized())
            
    def draw_text_stroke(self, painter: QPainter, stroke: Stroke):
        """Draw a text stroke"""
        if not stroke.text_content or not stroke.points:
            return
            
        painter.setFont(QFont("Arial", 12))
        painter.setPen(stroke.color)
        pos = stroke.points[0]
        painter.drawText(QPoint(pos[0], pos[1]), stroke.text_content)
