from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QHBoxLayout,
    QColorDialog,
    QComboBox,
    QLabel,
    QSlider
)

from PyQt6.QtCore import Qt
import qtawesome as qta

from core.constants import Tool


class Toolbar(QWidget):

    def __init__(self, overlay):
        super().__init__()

        self.overlay = overlay

        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )

        self.setStyleSheet('''
            QWidget {
                background: rgba(30, 30, 30, 230);
                border-radius: 12px;
                color: white;
            }

            QPushButton {
                background: #2d2d2d;
                border: none;
                padding: 8px;
                border-radius: 8px;
                color: white;
                min-width: 42px;
                min-height: 42px;
            }

            QPushButton:hover {
                background: #4a4a4a;
            }
        ''')

        layout = QHBoxLayout()

        cursor_btn = QPushButton()
        cursor_btn.setIcon(qta.icon('fa5s.mouse-pointer'))

        pen_btn = QPushButton()
        pen_btn.setIcon(qta.icon('fa5s.pen'))

        highlighter_btn = QPushButton()
        highlighter_btn.setIcon(qta.icon('fa5s.highlighter'))

        eraser_btn = QPushButton()
        eraser_btn.setIcon(qta.icon('fa5s.eraser'))

        text_btn = QPushButton()
        text_btn.setIcon(qta.icon('fa5s.font'))

        color_btn = QPushButton()
        color_btn.setIcon(qta.icon('fa5s.palette'))

        clear_btn = QPushButton()
        clear_btn.setIcon(qta.icon('fa5s.trash'))

        shape_combo = QComboBox()
        shape_combo.addItems(["Rectangle", "Ellipse", "Line"])

        size_slider = QSlider(Qt.Orientation.Horizontal)
        size_slider.setMinimum(1)
        size_slider.setMaximum(20)
        size_slider.setValue(4)

        cursor_btn.clicked.connect(lambda: overlay.set_tool(Tool.CURSOR))
        pen_btn.clicked.connect(lambda: overlay.set_tool(Tool.PEN))
        highlighter_btn.clicked.connect(lambda: overlay.set_tool(Tool.HIGHLIGHTER))
        eraser_btn.clicked.connect(lambda: overlay.set_tool(Tool.ERASER))
        text_btn.clicked.connect(lambda: overlay.set_tool(Tool.TEXT))

        clear_btn.clicked.connect(overlay.clear_all)

        color_btn.clicked.connect(self.pick_color)

        shape_combo.currentTextChanged.connect(self.select_shape)

        size_slider.valueChanged.connect(overlay.set_pen_size)

        layout.addWidget(cursor_btn)
        layout.addWidget(pen_btn)
        layout.addWidget(highlighter_btn)
        layout.addWidget(eraser_btn)
        layout.addWidget(text_btn)
        layout.addWidget(shape_combo)
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

    def select_shape(self, text):

        if text == "Rectangle":
            self.overlay.set_tool(Tool.RECTANGLE)

        elif text == "Ellipse":
            self.overlay.set_tool(Tool.ELLIPSE)

        elif text == "Line":
            self.overlay.set_tool(Tool.LINE)