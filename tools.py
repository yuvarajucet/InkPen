"""
InkPen - Tool definitions and constants
"""
from enum import Enum, auto


class Tool(Enum):
    CURSOR = auto()
    PEN = auto()
    HIGHLIGHTER = auto()
    SHAPE = auto()
    TEXT = auto()
    ERASER = auto()


class Shape(Enum):
    LINE = auto()
    ARROW = auto()
    RECTANGLE = auto()
    ELLIPSE = auto()
    TRIANGLE = auto()


# Default settings
DEFAULT_PEN_COLOR = "#E74C3C"
DEFAULT_PEN_SIZE = 3
DEFAULT_HIGHLIGHTER_COLOR = "#F1C40F"
DEFAULT_HIGHLIGHTER_SIZE = 20
DEFAULT_HIGHLIGHTER_OPACITY = 120  # 0-255

PEN_SIZES = [1, 2, 3, 5, 8, 12, 16, 24]

PRESET_COLORS = [
    "#E74C3C",  # Red
    "#E67E22",  # Orange
    "#F1C40F",  # Yellow
    "#2ECC71",  # Green
    "#1ABC9C",  # Teal
    "#3498DB",  # Blue
    "#9B59B6",  # Purple
    "#EC407A",  # Pink
    "#FFFFFF",  # White
    "#BDC3C7",  # Light Gray
    "#7F8C8D",  # Gray
    "#2C3E50",  # Dark
]

HIGHLIGHTER_COLORS = [
    "#FFF176",  # Yellow
    "#A5D6A7",  # Green
    "#90CAF9",  # Blue
    "#F48FB1",  # Pink
    "#FFCC80",  # Orange
    "#CE93D8",  # Purple
]
