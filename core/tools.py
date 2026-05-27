from dataclasses import dataclass
from PyQt6.QtGui import QColor
from core.constants import Tool

@dataclass
class Stroke:
    points: list
    color: QColor
    width: int
    tool: Tool