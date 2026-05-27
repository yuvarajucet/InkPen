import sys
from PyQt6.QtWidgets import QApplication
from core.overlay import OverlayWindow
from core.toolbar import Toolbar

def main():
    app = QApplication(sys.argv)

    overlay = OverlayWindow()
    toolbar = Toolbar(overlay)

    overlay.set_toolbar(toolbar)

    toolbar.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()