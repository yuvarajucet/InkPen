"""
InkPen - Screen Annotation Overlay Tool
Entry point
"""
import sys
import os

# Fix for PyInstaller bundled app
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont, QFontDatabase

from app import InkPenApp


def main():
    # Enable High DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setApplicationName("InkPen")
    app.setApplicationDisplayName("InkPen")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("InkPen")

    ink_app = InkPenApp()
    ink_app.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
