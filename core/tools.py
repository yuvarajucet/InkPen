"""Tool definitions and implementations for InkPen"""

from enum import Enum
from PyQt5.QtGui import QColor
from typing import List, Tuple


class ToolType(Enum):
    """Available tools"""
    CURSOR = "cursor"
    PEN = "pen"
    ERASER = "eraser"
    HIGHLIGHTER = "highlighter"
    COLOR_PICKER = "color_picker"
    SHAPES = "shapes"
    TEXT = "text"
    DELETE = "delete"


class ShapeType(Enum):
    """Available shapes"""
    LINE = "line"
    RECTANGLE = "rectangle"
    CIRCLE = "circle"
    ELLIPSE = "ellipse"


class Stroke:
    """Represents a single drawn stroke"""
    
    def __init__(self, stroke_id: int, tool_type: ToolType, points: List[Tuple[int, int]] = None):
        self.id = stroke_id
        self.tool_type = tool_type
        self.points = points or []
        self.color = QColor(0, 0, 0)
        self.pen_size = 2
        self.shape_type = None
        self.text_content = ""
        
    def add_point(self, point: Tuple[int, int]):
        """Add a point to the stroke"""
        self.points.append(point)
        
    def is_connected_to(self, other: 'Stroke', threshold: int = 10) -> bool:
        """Check if this stroke is connected to another stroke"""
        if not self.points or not other.points:
            return False
            
        for p1 in self.points:
            for p2 in other.points:
                dx = p1[0] - p2[0]
                dy = p1[1] - p2[1]
                dist = (dx * dx + dy * dy) ** 0.5
                if dist <= threshold:
                    return True
        return False


class DrawingState:
    """Manages the state of all drawn content"""
    
    def __init__(self):
        self.strokes: List[Stroke] = []
        self.stroke_counter = 0
        self.current_tool = ToolType.PEN
        self.pen_size = 2
        self.pen_color = QColor(0, 0, 0)
        self.highlighter_color = QColor(255, 255, 0, 128)
        
    def add_stroke(self, stroke: Stroke) -> int:
        """Add a stroke and return its ID"""
        stroke.id = self.stroke_counter
        self.strokes.append(stroke)
        self.stroke_counter += 1
        return stroke.id
        
    def remove_stroke(self, stroke_id: int):
        """Remove a stroke by ID"""
        self.strokes = [s for s in self.strokes if s.id != stroke_id]
        
    def get_connected_strokes(self, stroke: Stroke) -> List[Stroke]:
        """Get all strokes connected to the given stroke"""
        connected = {stroke}
        to_check = [stroke]
        
        while to_check:
            current = to_check.pop(0)
            for other in self.strokes:
                if other not in connected and current.is_connected_to(other):
                    connected.add(other)
                    to_check.append(other)
                    
        return list(connected)
        
    def remove_connected_strokes(self, stroke: Stroke):
        """Remove a stroke and all connected strokes"""
        connected = self.get_connected_strokes(stroke)
        for s in connected:
            self.remove_stroke(s.id)
            
    def clear_all(self):
        """Clear all strokes"""
        self.strokes.clear()
        self.stroke_counter = 0