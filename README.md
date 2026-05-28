# InkPen - Screen Annotation Overlay Tool

A lightweight, always-on-top screen annotation tool for Windows that lets you draw, highlight, and annotate over any application in real-time.

![InkPen](https://img.shields.io/badge/Windows-10%2F11-0078D4?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-41CD52?style=flat-square)

## Features

✨ **Core Capabilities:**
- 📝 **Pen Tool** - Draw freehand with customizable colors and sizes
- 🎨 **Highlighter** - Transparent highlighting with opacity control
- ✂️ **Shape Tools** - Line, arrow, rectangle, ellipse, triangle
- 📄 **Text Tool** - Add text annotations to your drawings
- 🧹 **Eraser Tool** - Remove entire connected strokes with one swipe
- 🎯 **Cursor Mode** - Switch to normal clicking without drawing interference
- 🚀 **Always-On-Top** - Toolbar and canvas stay above all windows
- 💾 **Persistent Settings** - Remembers your tool preferences and colors
- ⌨️ **Undo Support** - Revert your last action
- 🗑️ **Clear All** - Remove all drawings with one click

## Installation

### Option 1: Download Pre-built Executable (Easiest)

1. Go to [Releases](../../releases)
2. Download the latest `InkPen.exe`
3. Run it directly (no installation required!)
4. The floating toolbar will appear on your screen

### Option 2: Build from Source

**Requirements:**
- Python 3.11 or higher
- Windows 10/11 (64-bit)

**Setup:**
```bash
# Clone the repository
git clone https://github.com/yourusername/inkpen.git
cd inkpen

# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

**Build as EXE:**
```bash
# Install PyInstaller if not already installed
pip install pyinstaller

# Build the executable
pyinstaller inkpen.spec --onefile

# The executable will be in ./dist/InkPen.exe
```

## Usage Guide

### Toolbar Overview

The floating toolbar contains the following tools (left to right):

| Tool | Icon | Function |
|------|------|----------|
| **Cursor** | 🖱️ | Click-through mode - normal interaction with apps below |
| **Pen** | ✏️ | Freehand drawing with selected color |
| **Highlighter** | 🖍️ | Semi-transparent highlighting |
| **Pen Size** | 📊 | Adjust pen/highlighter thickness |
| **Text** | 📝 | Add text annotations (opens text input dialog) |
| **Shape** | 📐 | Line, arrow, rectangle, ellipse, or triangle |
| **Eraser** | 🗑️ | Remove entire connected strokes |
| **Color Picker** | 🎨 | Choose pen and highlighter colors |
| **Clear All** | 🗑️ | Remove all drawings from screen |

### Keyboard Shortcuts

- **Ctrl+Z** - Undo last action
- **X** - Switch to eraser (when toolbar is focused)
- **ESC** - Activate cursor mode for click-through

### Quick Workflow

1. **Start Drawing:**
   - Click the pen tool
   - Select a color if desired
   - Adjust pen size if needed
   - Draw on your screen over any application

2. **Highlight Text:**
   - Click the highlighter tool
   - Choose a highlight color
   - Draw over text to highlight it

3. **Add Shapes:**
   - Click the shape tool
   - Select desired shape from popup
   - Click and drag on screen to draw shape

4. **Add Text:**
   - Click the text tool
   - Click where you want text to appear
   - Type your text in the dialog
   - Text appears on screen

5. **Fix Mistakes:**
   - Use eraser to remove individual strokes
   - Use Ctrl+Z to undo last action
   - Click "Clear All" to start fresh

6. **Normal Interaction:**
   - Click cursor tool to disable drawing mode
   - Click normally on windows below
   - Click pen tool to resume drawing

## Settings

Settings are automatically saved and restored:
- Last selected tool
- Last used colors (pen and highlighter)
- Pen size preference
- Toolbar position on screen

Settings are stored in Windows Registry under:
```
HKEY_CURRENT_USER\Software\InkPen\InkPen
```

## Architecture

### Project Structure

```
inkpen/
├── main.py              # Entry point
├── app.py               # Main application controller
├── toolbar.py           # Floating toolbar UI
├── canvas.py            # Drawing canvas overlay
├── tools.py             # Tool definitions and constants
├── icons.py             # SVG icon definitions
├── requirements.txt     # Python dependencies
├── inkpen.spec          # PyInstaller configuration
└── .github/
    └── workflows/
        └── build.yml    # GitHub Actions CI/CD workflow
```

### Key Components

**Canvas (`canvas.py`):**
- Full-screen transparent overlay
- Handles all drawing input
- Stroke management and hit detection
- Supports click-through when in cursor mode

**Toolbar (`toolbar.py`):**
- Floating always-on-top widget
- Tool selection buttons
- Color picker and size selector popups
- Draggable window

**Tools (`tools.py`):**
- Tool enums and shape definitions
- Color presets
- Default configuration constants

## Development

### Adding New Tools

1. Add tool to `Tool` enum in `tools.py`
2. Create button in `InkPenToolbar._setup_ui()` with corresponding icon
3. Implement drawing logic in `DrawingCanvas._draw_stroke()`
4. Connect tool change signal to canvas

### Adding New Shapes

1. Add shape to `Shape` enum in `tools.py`
2. Add shape button to shape popup in `toolbar.py`
3. Implement drawing logic in `DrawingCanvas._draw_stroke()`

### Custom Icons

Icons are defined as SVG strings in `icons.py`. To add new icons:

1. Create SVG string with `currentColor` placeholders
2. Add to `icons.py` as `ICON_NAME = """..."""`
3. Use `svg_to_icon()` or `svg_to_pixmap()` to convert

## Performance

- **Minimal CPU Usage**: Only draws when actively annotating
- **Low Memory Footprint**: ~100MB when running
- **Responsive UI**: 60+ FPS drawing performance
- **No Dependencies**: Single EXE, no runtime installation needed

## Troubleshooting

### Application won't start
- Ensure Windows 10 or 11 (64-bit)
- Run as Administrator if permission issues occur
- Check that no other instance is running

### Drawing not showing up
- Ensure pen tool (not cursor) is selected
- Check that color is visible on background
- Try using highlighter tool instead

### Toolbar disappeared
- Move your mouse to where toolbar was last visible
- Restart the application (toolbar position is saved)

### Performance issues
- Close other resource-intensive applications
- Reduce number of strokes on canvas (use Clear All)
- Check Windows display driver is updated

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

Found a bug or have a feature request?

1. Check [existing issues](../../issues)
2. Create a [new issue](../../issues/new) with:
   - Clear description of problem/request
   - Steps to reproduce (if bug)
   - Windows version and build number
   - Screenshot if applicable

## Roadmap

- [ ] Multi-monitor full support
- [ ] Preset color palettes
- [ ] Stroke width variations (pressure sensitivity)
- [ ] Image annotation (paste and annotate)
- [ ] Recording drawings as GIF/video
- [ ] Custom brushes and effects
- [ ] Touch screen support

## Credits

Built with:
- [PyQt5](https://pypi.org/project/PyQt5/) - GUI framework
- [PyInstaller](https://pyinstaller.org/) - Executable packaging

## Version History

### v2024.12.01 (Latest)
- Initial public release
- Core tools: Pen, Highlighter, Shapes, Text, Eraser
- Color picker with presets
- Undo and Clear All functionality
- Persistent settings
- GitHub Actions CI/CD

---

**Made with ❤️ for Windows users who love annotating**

*InkPen - Because sometimes a screenshot just needs a circle around it.*
