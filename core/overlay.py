"""Overlay window management for InkPen"""

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QApplication
from .drawing import DrawingCanvas


class OverlayWindow(QMainWindow):
    """The main transparent overlay window for drawing"""
    
    def __init__(self):
        super().__init__()
        self.canvas = DrawingCanvas()
        
        # Set up window properties for overlay
        self.setWindowTitle("InkPen Overlay")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.Tool
        )
        
        # Set up the canvas as central widget
        self.setCentralWidget(self.canvas)
        
        # Make window frameless and transparent
        self.setStyleSheet("background-color: transparent;")
        
        # Cover entire screen
        screen = QApplication.primaryScreen()
        geom = screen.geometry()
        self.setGeometry(geom)
        
    def get_canvas(self) -> DrawingCanvas:
        """Get the canvas widget"""
        return self.canvas