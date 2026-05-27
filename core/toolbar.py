from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QHBoxLayout,
    QColorDialog,
    QLabel,
    QSlider
)

from PyQt6.QtCore import Qt, QPoint
import qtawesome as qta
from core.constants import Tool


class Toolbar(QWidget):

    def __init__(self, overlay):
        super().__init__()

        self.overlay = overlay

        self.drag_pos = QPoint()

        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )

        self.setStyleSheet('''
            QWidget {
                background: rgba(20,20,20,230);
                border-radius: 14px;
                color: white;
            }

            QPushButton {
                background: #2c2c2c;
                border-radius: 8px;
                padding: 8px;
                min-width: 42px;
                min-height: 42px;
            }

            QPushButton:hover {
                background: #4d4d4d;
            }
        ''')

        layout = QHBoxLayout()

        cursor_btn = QPushButton()
        cursor_btn.setIcon(qta.icon('fa5s.mouse-pointer', color='white'))

        pen_btn = QPushButton()
        pen_btn.setIcon(qta.icon('fa5s.pen', color='white'))

        highlighter_btn = QPushButton()
        highlighter_btn.setIcon(qta.icon('fa5s.highlighter', color='yellow'))

        eraser_btn = QPushButton()
        eraser_btn.setIcon(qta.icon('fa5s.eraser', color='white'))

        text_btn = QPushButton()
        text_btn.setIcon(qta.icon('fa5s.font', color='white'))

        color_btn = QPushButton()
        color_btn.setIcon(qta.icon('fa5s.palette', color='white'))

        clear_btn = QPushButton()
        clear_btn.setIcon(qta.icon('fa5s.trash', color='red'))

        size_slider = QSlider(Qt.Orientation.Horizontal)
        size_slider.setMinimum(1)
        size_slider.setMaximum(25)
        size_slider.setValue(4)

        cursor_btn.clicked.connect(lambda: overlay.set_tool(Tool.CURSOR))
        pen_btn.clicked.connect(lambda: overlay.set_tool(Tool.PEN))
        highlighter_btn.clicked.connect(lambda: overlay.set_tool(Tool.HIGHLIGHTER))
        eraser_btn.clicked.connect(lambda: overlay.set_tool(Tool.ERASER))
        text_btn.clicked.connect(lambda: overlay.set_tool(Tool.TEXT))

        color_btn.clicked.connect(self.pick_color)

        clear_btn.clicked.connect(overlay.clear_all)

        size_slider.valueChanged.connect(overlay.set_pen_size)

        layout.addWidget(cursor_btn)
        layout.addWidget(pen_btn)
        layout.addWidget(highlighter_btn)
        layout.addWidget(eraser_btn)
        layout.addWidget(text_btn)
        layout.addWidget(QLabel("Size"))
        layout.addWidget(size_slider)
        layout.addWidget(color_btn)
        layout.addWidget(clear_btn)

        self.setLayout(layout)

        self.adjustSize()

        self.move(100, 100)

    def pick_color(self):

        color = QColorDialog.getColor()

        if color.isValid():
            self.overlay.set_color(color)

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):

        if event.buttons() == Qt.MouseButton.LeftButton:

            delta = event.globalPosition().toPoint() - self.drag_pos

            self.move(self.x() + delta.x(), self.y() + delta.y())

            self.drag_pos = event.globalPosition().toPoint()