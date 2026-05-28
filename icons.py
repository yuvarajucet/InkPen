"""
InkPen - High quality SVG icons
All icons rendered as QPixmap from inline SVG
"""
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QColor
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import QByteArray


def svg_to_pixmap(svg_str: str, size: int = 24, color: str = None) -> QPixmap:
    """Convert SVG string to QPixmap, optionally recoloring it."""
    if color:
        svg_str = svg_str.replace('currentColor', color)
        svg_str = svg_str.replace('#ICONCOLOR', color)
    else:
        svg_str = svg_str.replace('currentColor', '#FFFFFF')
        svg_str = svg_str.replace('#ICONCOLOR', '#FFFFFF')

    renderer = QSvgRenderer(QByteArray(svg_str.encode('utf-8')))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    renderer.render(painter)
    painter.end()
    return pixmap


def svg_to_icon(svg_str: str, size: int = 24, color: str = None) -> QIcon:
    return QIcon(svg_to_pixmap(svg_str, size, color))


# ── SVG Icon Definitions ────────────────────────────────────────────────────

ICON_CURSOR = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <path d="M5.5 3.5L5.5 17.5L9 14L11.5 20.5L13.5 19.5L11 13L15.5 13L5.5 3.5Z"
        fill="currentColor" stroke="currentColor" stroke-width="0.5"
        stroke-linejoin="round"/>
</svg>
"""

ICON_PEN = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <path d="M17.5 2.5C18.3 1.7 19.7 1.7 20.5 2.5L21.5 3.5C22.3 4.3 22.3 5.7 21.5 6.5L9 19L4 20L5 15L17.5 2.5Z"
        fill="currentColor" opacity="0.9"/>
  <path d="M15 5L19 9" stroke="#00000044" stroke-width="1.5" stroke-linecap="round"/>
  <path d="M4 20L5 15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
</svg>
"""

ICON_HIGHLIGHTER = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <rect x="7" y="3" width="10" height="13" rx="2" fill="currentColor" opacity="0.85"/>
  <path d="M9 16L7.5 21H16.5L15 16H9Z" fill="currentColor" opacity="0.6"/>
  <rect x="9" y="5" width="6" height="2" rx="1" fill="white" opacity="0.4"/>
  <line x1="12" y1="21" x2="12" y2="23" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
</svg>
"""

ICON_SHAPE = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <rect x="2.5" y="2.5" width="8" height="8" rx="1"
        stroke="currentColor" stroke-width="2" fill="none"/>
  <circle cx="17" cy="7" r="4.5" stroke="currentColor" stroke-width="2" fill="none"/>
  <path d="M3 22L8 14L13 22H3Z" stroke="currentColor" stroke-width="2"
        fill="none" stroke-linejoin="round"/>
  <line x1="15" y1="16" x2="22" y2="22" stroke="currentColor" stroke-width="2"
        stroke-linecap="round"/>
</svg>
"""

ICON_ERASER = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <path d="M20.5 7.5L16.5 3.5C15.7 2.7 14.3 2.7 13.5 3.5L3 14L7.5 20.5H13L20.5 13C21.3 12.2 21.3 8.3 20.5 7.5Z"
        fill="currentColor" opacity="0.85"/>
  <path d="M13.5 3.5L20.5 10.5" stroke="white" stroke-width="1.5" opacity="0.4"/>
  <line x1="3" y1="20.5" x2="13" y2="20.5" stroke="currentColor" stroke-width="2.5"
        stroke-linecap="round"/>
  <path d="M7.5 20.5L3 15" stroke="currentColor" stroke-width="1.5" opacity="0.6"/>
</svg>
"""

ICON_TEXT = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <path d="M4 6V4H20V6" stroke="currentColor" stroke-width="2.5"
        stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="12" y1="4" x2="12" y2="20" stroke="currentColor" stroke-width="2.5"
        stroke-linecap="round"/>
  <line x1="8" y1="20" x2="16" y2="20" stroke="currentColor" stroke-width="2.5"
        stroke-linecap="round"/>
</svg>
"""

ICON_COLOR_PICKER = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <circle cx="12" cy="10" r="7" fill="currentColor" opacity="0.15"
          stroke="currentColor" stroke-width="1.5"/>
  <path d="M8 8 Q12 4 16 8 Q18 12 12 15 Q6 12 8 8Z" fill="currentColor" opacity="0.7"/>
  <path d="M9 9 Q12 6.5 15 9" stroke="white" stroke-width="1" opacity="0.5"
        fill="none" stroke-linecap="round"/>
  <rect x="10" y="17" width="4" height="5" rx="1" fill="currentColor"/>
</svg>
"""

ICON_TRASH = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <path d="M3 6H21" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M8 6V4H16V6" stroke="currentColor" stroke-width="2" stroke-linecap="round"
        stroke-linejoin="round"/>
  <path d="M5 6L6 20H18L19 6" stroke="currentColor" stroke-width="2"
        stroke-linecap="round" stroke-linejoin="round" fill="none"/>
  <line x1="10" y1="10" x2="10" y2="17" stroke="currentColor" stroke-width="1.8"
        stroke-linecap="round"/>
  <line x1="14" y1="10" x2="14" y2="17" stroke="currentColor" stroke-width="1.8"
        stroke-linecap="round"/>
</svg>
"""

ICON_PEN_SIZE = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <circle cx="12" cy="18" r="2.5" fill="currentColor"/>
  <circle cx="12" cy="11" r="1.8" fill="currentColor"/>
  <circle cx="12" cy="5.5" r="1.1" fill="currentColor"/>
  <line x1="3" y1="21" x2="21" y2="21" stroke="currentColor" stroke-width="1.5"
        stroke-linecap="round" opacity="0.5"/>
</svg>
"""

ICON_MINIMIZE = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <line x1="5" y1="12" x2="19" y2="12" stroke="currentColor" stroke-width="2.5"
        stroke-linecap="round"/>
</svg>
"""

ICON_CLOSE = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="2.5"
        stroke-linecap="round"/>
  <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="2.5"
        stroke-linecap="round"/>
</svg>
"""

ICON_UNDO = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <path d="M4 8H15C18.3 8 21 10.7 21 14C21 17.3 18.3 20 15 20H8"
        stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/>
  <path d="M4 8L8 4M4 8L8 12" stroke="currentColor" stroke-width="2.5"
        stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

ICON_LINE = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <line x1="4" y1="20" x2="20" y2="4" stroke="currentColor" stroke-width="2.5"
        stroke-linecap="round"/>
</svg>
"""

ICON_ARROW = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <line x1="5" y1="19" x2="19" y2="5" stroke="currentColor" stroke-width="2.5"
        stroke-linecap="round"/>
  <path d="M10 5H19V14" stroke="currentColor" stroke-width="2.5"
        stroke-linecap="round" stroke-linejoin="round" fill="none"/>
</svg>
"""

ICON_RECT = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <rect x="3" y="5" width="18" height="14" rx="2"
        stroke="currentColor" stroke-width="2.5" fill="none"/>
</svg>
"""

ICON_ELLIPSE = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <ellipse cx="12" cy="12" rx="9" ry="6.5"
           stroke="currentColor" stroke-width="2.5" fill="none"/>
</svg>
"""

ICON_TRIANGLE = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <path d="M12 4L21 20H3L12 4Z" stroke="currentColor" stroke-width="2.5"
        fill="none" stroke-linejoin="round"/>
</svg>
"""

ICON_DRAG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <circle cx="9" cy="6" r="1.5" fill="currentColor"/>
  <circle cx="15" cy="6" r="1.5" fill="currentColor"/>
  <circle cx="9" cy="12" r="1.5" fill="currentColor"/>
  <circle cx="15" cy="12" r="1.5" fill="currentColor"/>
  <circle cx="9" cy="18" r="1.5" fill="currentColor"/>
  <circle cx="15" cy="18" r="1.5" fill="currentColor"/>
</svg>
"""
