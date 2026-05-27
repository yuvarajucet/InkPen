"""InkPen - Windows Overlay Drawing Application"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from core.overlay import OverlayWindow
from core.toolbar import ToolBar


def main():
    """Main entry point for InkPen application"""
    app = QApplication(sys.argv)
    
    # Create overlay window
    overlay = OverlayWindow()
    overlay.show()
    
    # Create toolbar
    canvas = overlay.get_canvas()
    toolbar = ToolBar(canvas)
    toolbar.show()
    
    # Set window icon and title
    app.setApplicationName("InkPen")
    app.setApplicationVersion("1.0.0")
    
    # Keyboard shortcuts
    from PyQt5.QtWidgets import QShortcut
    from PyQt5.QtGui import QKeySequence
    
    # Ctrl+D to clear all
    QShortcut(QKeySequence("Ctrl+D"), overlay, lambda: canvas.clear_canvas())
    
    # ESC to exit
    QShortcut(QKeySequence("Escape"), overlay, app.quit)
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
