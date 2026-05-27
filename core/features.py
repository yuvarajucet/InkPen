"""Enhanced drawing features for InkPen"""

from typing import List, Tuple
from collections import deque


class UndoRedoStack:
    """Manages undo/redo operations"""
    
    def __init__(self, max_size: int = 100):
        self.undo_stack: deque = deque(maxlen=max_size)
        self.redo_stack: deque = deque(maxlen=max_size)
        
    def push_undo(self, state):
        """Push state to undo stack"""
        self.undo_stack.append(state)
        self.redo_stack.clear()
        
    def undo(self):
        """Get previous state"""
        if self.undo_stack:
            state = self.undo_stack.pop()
            self.redo_stack.append(state)
            return state
        return None
        
    def redo(self):
        """Get next state"""
        if self.redo_stack:
            state = self.redo_stack.pop()
            self.undo_stack.append(state)
            return state
        return None
        
    def can_undo(self) -> bool:
        """Check if undo is available"""
        return len(self.undo_stack) > 0
        
    def can_redo(self) -> bool:
        """Check if redo is available"""
        return len(self.redo_stack) > 0
        
    def clear(self):
        """Clear all history"""
        self.undo_stack.clear()
        self.redo_stack.clear()


class StrokeSmoothing:
    """Smooth strokes for better drawing quality"""
    
    @staticmethod
    def catmull_rom(p0: Tuple[int, int], p1: Tuple[int, int], 
                     p2: Tuple[int, int], p3: Tuple[int, int], 
                     t: float) -> Tuple[float, float]:
        """Catmull-Rom spline interpolation"""
        t2 = t * t
        t3 = t2 * t
        
        x = 0.5 * (2 * p1[0] + (-p0[0] + p2[0]) * t + 
                   (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + 
                   (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
        
        y = 0.5 * (2 * p1[1] + (-p0[1] + p2[1]) * t + 
                   (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + 
                   (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
        
        return (int(x), int(y))
    
    @staticmethod
    def smooth_stroke(points: List[Tuple[int, int]], smoothness: int = 3) -> List[Tuple[int, int]]:
        """Smooth a stroke using Catmull-Rom splines"""
        if len(points) < 4:
            return points
        
        smoothed = []
        for i in range(len(points) - 1):
            p0 = points[max(0, i - 1)]
            p1 = points[i]
            p2 = points[min(len(points) - 1, i + 1)]
            p3 = points[min(len(points) - 1, i + 2)]
            
            for t in [j / smoothness for j in range(smoothness)]:
                point = StrokeSmoothing.catmull_rom(p0, p1, p2, p3, t)
                smoothed.append(point)
        
        smoothed.append(points[-1])
        return smoothed


class PressureSensitivity:
    """Simulate pressure sensitivity for more natural drawing"""
    
    @staticmethod
    def calculate_stroke_width(distance: float, base_width: int, max_width: int = 50) -> int:
        """Calculate stroke width based on distance between points"""
        # Shorter distance = thicker stroke (pressure effect)
        if distance < 5:
            return max_width
        elif distance > 50:
            return base_width
        else:
            ratio = (50 - distance) / 45
            return int(base_width + (max_width - base_width) * ratio)


class ColorPaletteManager:
    """Manage color palettes"""
    
    PRESET_PALETTES = {
        "Basic": [
            "#000000",  # Black
            "#FF0000",  # Red
            "#00FF00",  # Green
            "#0000FF",  # Blue
            "#FFFF00",  # Yellow
            "#FF00FF",  # Magenta
            "#00FFFF",  # Cyan
            "#FFFFFF",  # White
        ],
        "Pastel": [
            "#FFB3BA",  # Light Red
            "#FFDFBA",  # Light Orange
            "#FFFFBA",  # Light Yellow
            "#BAFFC9",  # Light Green
            "#BAE1FF",  # Light Blue
            "#E0BBE4",  # Light Purple
        ],
        "Dark": [
            "#1a1a2e",
            "#16213e",
            "#0f3460",
            "#e94560",
            "#533483",
            "#2d3a3a",
        ],
        "Vibrant": [
            "#FF006E",
            "#FB5607",
            "#FFBE0B",
            "#8338EC",
            "#3A86FF",
            "#06FFA5",
        ],
    }
    
    @staticmethod
    def get_palette(name: str) -> List[str]:
        """Get a preset palette"""
        return ColorPaletteManager.PRESET_PALETTES.get(name, ColorPaletteManager.PRESET_PALETTES["Basic"])
    
    @staticmethod
    def get_all_palettes() -> dict:
        """Get all available palettes"""
        return ColorPaletteManager.PRESET_PALETTES


class DrawingPresets:
    """Drawing presets for quick setup"""
    
    PRESETS = {
        "Sketch": {"pen_size": 2, "opacity": 255, "color": "#000000"},
        "Highlighter": {"pen_size": 8, "opacity": 128, "color": "#FFFF00"},
        "Bold": {"pen_size": 8, "opacity": 255, "color": "#000000"},
        "Subtle": {"pen_size": 1, "opacity": 200, "color": "#CCCCCC"},
        "Presentation": {"pen_size": 5, "opacity": 255, "color": "#0078D4"},
    }
    
    @staticmethod
    def get_preset(name: str) -> dict:
        """Get a preset configuration"""
        return DrawingPresets.PRESETS.get(name, DrawingPresets.PRESETS["Sketch"])
    
    @staticmethod
    def get_all_presets() -> dict:
        """Get all available presets"""
        return DrawingPresets.PRESETS
