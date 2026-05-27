# InkPen - Windows Overlay Drawing Application

An always-on-top overlay drawing application for Windows that allows you to annotate and draw on top of any application.

## Features

- **Always-On-Top Toolbar**: Accessible drawing toolbar that stays visible on top of all windows
- **Multiple Drawing Tools**:
  - 🎨 **Pen**: Freehand drawing with adjustable brush size
  - 🔍 **Cursor**: Pointer tool for deselecting drawing mode
  - 🗑️ **Eraser**: Intelligent line-based eraser that removes entire connected strokes
  - 🟡 **Highlighter**: Semi-transparent highlighting tool
  - 🎨 **Color Picker**: Choose any color for drawing
  - 📦 **Shapes**: Draw lines, rectangles, circles, and ellipses
  - 📝 **Text**: Add text annotations
  - 🗑️ **Delete All**: Clear all drawings with one click

- **Customizable Settings**:
  - Adjustable brush/pen size (1-50 pixels)
  - Full color palette support
  - Multiple shape options
  - Real-time preview

- **High-Quality UI**: 
  - Modern dark theme
  - Custom tool icons
  - Smooth rendering (60 FPS)
  - Transparent overlay window

## System Requirements

- **OS**: Windows 7 or later
- **RAM**: 256MB minimum
- **Disk Space**: 100MB for standalone executable

## Installation

### Using Pre-built Executable
1. Download the latest `InkPen.zip` from the [Releases](../../releases) page
2. Extract the ZIP file
3. Run `InkPen.exe`

### Building from Source

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/InkPen.git
cd InkPen
```

2. **Install Python 3.8+** from [python.org](https://www.python.org)

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the application**:
```bash
python app.py
```

## Building the Executable

### Prerequisites
- Python 3.8+
- All dependencies installed from `requirements.txt`

### Build Steps

1. **Install PyInstaller** (if not already installed):
```bash
pip install pyinstaller
```

2. **Generate the executable**:
```bash
pyinstaller build.spec
```

3. The executable will be created in the `dist\InkPen` folder

4. **Create a portable version**:
```bash
cd dist
tar.exe -a -c -f InkPen.zip InkPen/
```

## Usage

### Starting the Application
- Run `InkPen.exe` or `python app.py`
- The toolbar will appear at the top-right of your screen
- The overlay covers the entire screen

### Drawing

1. **Select a tool** from the toolbar
2. **Adjust settings** if needed:
   - Pen size: Use the slider or spinner
   - Color: Click the color preview button
   - Shape: Select from the dropdown (for shapes tool)
3. **Draw** on any application by clicking and dragging
4. **Erase** using the eraser tool - it removes entire connected lines
5. **Delete all** with the Clear button or press `Ctrl+D`

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `P` | Pen tool |
| `E` | Eraser tool |
| `H` | Highlighter tool |
| `S` | Shapes tool |
| `T` | Text tool |
| `C` | Cursor tool |
| `Ctrl+D` | Delete all drawings |
| `Escape` | Exit application |

### Tool Descriptions

- **Cursor**: Deactivates drawing mode, allows mouse interaction with other applications
- **Pen**: Classic drawing tool with adjustable brush size and color
- **Eraser**: Touch a stroke to erase it and all connected lines
- **Highlighter**: Semi-transparent drawing for highlighting text/content
- **Color Picker**: Opens a color dialog to select any color
- **Shapes**: Draw geometric shapes (line, rectangle, circle, ellipse)
- **Text**: Click to add text annotations at a specific location
- **Clear**: Removes all drawings from the screen

## Architecture

```
InkPen/
├── app.py                      # Main application entry point
├── core/
│   ├── __init__.py
│   ├── overlay.py              # Overlay window management
│   ├── toolbar.py              # Toolbar widget
│   ├── drawing.py              # Drawing canvas and operations
│   ├── tools.py                # Tool definitions and state
│   └── utils.py                # Utility functions
├── build.spec                  # PyInstaller configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Technical Details

### Drawing System
- Strokes are stored as lists of coordinate points
- Each stroke tracks its tool type, color, and size
- Connected strokes are detected for intelligent line-based eraser
- Double buffering ensures smooth rendering at 60 FPS

### Overlay Window
- Uses PyQt5 with transparency and always-on-top flags
- Covers entire screen without blocking input to toolbar
- Real-time rendering with optimized dirty rectangle updates

### Performance
- Efficient memory usage with stroke batching
- Smooth drawing at high DPI displays
- Minimal CPU overhead in idle state

## Troubleshooting

### Application doesn't appear
- Check if Windows Taskbar or other UI elements are blocking it
- Try moving the toolbar with mouse drag

### Can't draw on certain applications
- Some full-screen games may not allow overlay drawing
- Try running InkPen as administrator

### Executable won't run
- Ensure Windows Defender/Antivirus isn't blocking it
- Try running from Administrator Command Prompt
- Check that your Windows installation is up to date

## Development

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Building and Testing

```bash
# Install dev dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Build the executable
pyinstaller build.spec
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Contact the development team

## Roadmap

- [ ] Undo/Redo functionality
- [ ] Save/Load drawings
- [ ] Custom brush shapes
- [ ] Layer support
- [ ] Dark mode theme option
- [ ] Settings persistence
- [ ] Customizable hotkeys
- [ ] Pattern/texture fills
- [ ] Drawing templates

## Credits

Built with:
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - GUI Framework
- [PyInstaller](https://www.pyinstaller.org/) - Executable Generation
- [Pillow](https://python-pillow.org/) - Image Processing

---

**InkPen v1.0.0** - Created for seamless screen annotation on Windows