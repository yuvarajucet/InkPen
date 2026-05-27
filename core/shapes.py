from dataclasses import dataclass
from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QColor
from core.constants import Tool

@dataclass
class ShapeItem:
    start: QPoint
    end: QPoint
    color: QColor
    width: int
    shape_type: Tool