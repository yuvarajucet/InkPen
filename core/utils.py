"""Utility functions for InkPen"""

from PyQt5.QtGui import QColor, QIcon, QPixmap, QPainter, QBrush, QPen, QPolygon
from PyQt5.QtCore import Qt, QSize, QPoint
import math


def create_color_icon(color: QColor, size: int = 24) -> QIcon:
    """Create an icon with a solid color"""
    pixmap = QPixmap(size, size)
    pixmap.fill(color)
    return QIcon(pixmap)


def create_tool_icon(color: QColor, tool_name: str, size: int = 24) -> QIcon:
    """Create a styled tool icon"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    if tool_name == "pen":
        # Draw pen icon
        painter.setPen(QPen(color, 2))
        painter.drawLine(2, 20, 15, 7)
        painter.drawPolyline(QPolygon([
            QPoint(15, 7), QPoint(18, 4), QPoint(20, 6), QPoint(17, 9)
        ]))
        
    elif tool_name == "eraser":
        # Draw eraser icon
        painter.setBrush(QBrush(color))
        painter.drawRect(8, 2, 12, 12)
        painter.setBrush(QBrush(Qt.white))
        painter.drawRect(10, 4, 8, 8)
        
    elif tool_name == "highlighter":
        # Draw highlighter icon
        painter.setPen(QPen(color, 3))
        painter.drawLine(5, 15, 18, 2)
        painter.drawRect(6, 16, 10, 4)
        
    elif tool_name == "cursor":
        # Draw cursor/pointer icon
        painter.setPen(QPen(color, 2))
        painter.drawPolyline(QPolygon([
            QPoint(2, 2), QPoint(2, 16), QPoint(6, 12), QPoint(10, 18),
            QPoint(13, 17), QPoint(7, 11), QPoint(13, 11)
        ]))
        
    elif tool_name == "text":
        # Draw text icon
        painter.setPen(QPen(color, 2))
        painter.drawText(2, 6, 20, 16, Qt.AlignCenter, "A")
        
    elif tool_name == "shapes":
        # Draw shapes icon
        painter.setPen(QPen(color, 2))
        painter.drawRect(2, 2, 8, 8)
        painter.drawEllipse(12, 2, 8, 8)
        painter.drawLine(2, 14, 10, 20)
        
    elif tool_name == "color":
        # Draw color picker icon
        painter.setBrush(QBrush(color))
        painter.drawEllipse(2, 2, 8, 8)
        painter.setPen(QPen(color, 2))
        painter.drawPolyline(QPolygon([
            QPoint(12, 8), QPoint(18, 2), QPoint(20, 4)
        ]))
        
    painter.end()
    return QIcon(pixmap)


def distance(p1: tuple, p2: tuple) -> float:
    """Calculate Euclidean distance between two points"""
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def point_to_line_distance(point: tuple, line_start: tuple, line_end: tuple) -> float:
    """Calculate minimum distance from point to line segment"""
    x, y = point
    x1, y1 = line_start
    x2, y2 = line_end
    
    dx = x2 - x1
    dy = y2 - y1
    
    if dx == 0 and dy == 0:
        return distance(point, line_start)
    
    t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)))
    closest_x = x1 + t * dx
    closest_y = y1 + t * dy
    
    return distance(point, (closest_x, closest_y))
