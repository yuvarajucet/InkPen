# InkPen Installation & Quick Start Guide

## Quick Installation

### Option 1: Download Pre-built Executable (Easiest)
1. Visit the [Releases](https://github.com/yourusername/InkPen/releases) page
2. Download the latest `InkPen.zip`
3. Extract the ZIP file
4. Run `InkPen.exe`

### Option 2: Build from Source

#### Prerequisites
- Windows 7 or later
- Python 3.8 or higher ([Download Python](https://www.python.org/downloads/))
- Git (optional, for cloning)

#### Installation Steps

1. **Clone or download the repository**:
```bash
git clone https://github.com/yourusername/InkPen.git
cd InkPen
```

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python app.py
```

### Option 3: Build Your Own Executable

1. **Complete the source installation first** (steps 1-2 above)

2. **Install PyInstaller**:
```bash
pip install pyinstaller
```

3. **Build the executable**:
```bash
REM Using the build script (Windows)
build.bat

REM Or use PyInstaller directly
pyinstaller build.spec
```

4. **Run the built executable**:
```bash
dist\InkPen\InkPen.exe
```

## First Run

1. **Launch InkPen**
   - Run `InkPen.exe` or `python app.py`

2. **The toolbar will appear** at the top-right of your screen

3. **Select a drawing tool** from the toolbar

4. **Start drawing** on any application

## Basic Usage

### Drawing Tools

| Tool | Description | Shortcut |
|------|-------------|----------|
| **Cursor** | Selection/pointer mode | `C` |
| **Pen** | Freehand drawing | `P` |
| **Eraser** | Remove strokes (line-based) | `E` |
| **Highlighter** | Semi-transparent highlighting | `H` |
| **Color Picker** | Select any color | (Click button) |
| **Shapes** | Draw geometric shapes | `S` |
| **Text** | Add text annotations | `T` |
| **Clear** | Delete all drawings | `Ctrl+D` |

### Customization

1. **Adjust Pen Size**:
   - Use the slider or spinner in the toolbar
   - Range: 1-50 pixels

2. **Change Color**:
   - Click the color preview button
   - Select any color from the color picker

3. **Select Shapes**:
   - Click "Shapes" tool
   - Choose shape type from dropdown (Line, Rectangle, Circle, Ellipse)

## Troubleshooting

### "No such file or directory" error
- Ensure you're in the correct directory
- Run from Command Prompt/PowerShell in the InkPen folder

### "Python is not recognized"
- Python is not in your system PATH
- Solution: Reinstall Python and check "Add Python to PATH" during installation
- Or use: `py app.py` instead of `python app.py`

### Executable won't start
- Try running as Administrator
- Check Windows Defender/Antivirus isn't blocking it
- Ensure Windows is up to date

### Can't draw on certain applications
- Some full-screen games block overlays
- Try drawing on regular applications first

### Application crashes
1. Check the console for error messages
2. Ensure all dependencies are installed: `pip install -r requirements.txt`
3. Try running with Python directly: `python app.py`

## File Structure

```
InkPen/
├── app.py                    Main application
├── build.bat                 Windows build script
├── build.spec                PyInstaller configuration
├── requirements.txt          Python dependencies
├── setup.py                  Package setup
├── README.md                 Documentation
├── INSTALL.md               This file
├── core/
│   ├── __init__.py
│   ├── overlay.py            Overlay window
│   ├── toolbar.py            Tool toolbar
│   ├── drawing.py            Drawing canvas
│   ├── tools.py              Tool definitions
│   ├── utils.py              Utility functions
│   └── features.py           Advanced features
├── dist/                     Built executable (after build)
│   ├── InkPen/
│   │   ├── InkPen.exe
│   │   ├── ...libraries...
│   │   └── ...resources...
│   └── InkPen.zip           Packaged executable
└── .github/
    └── workflows/
        └── build-release.yml CI/CD pipeline
```

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| OS | Windows 7 | Windows 10/11 |
| RAM | 256 MB | 512 MB |
| Disk Space | 50 MB | 100 MB |
| Display | 1024x768 | 1920x1080 or higher |
| Python | 3.8 | 3.10+ |

## Performance Tips

1. **Close unnecessary applications** to free up system memory
2. **Disable Windows animations** for smoother drawing
3. **Use appropriate pen size** - smaller sizes are faster
4. **Clear drawings regularly** to maintain performance

## Advanced Usage

### Command-Line Options

```bash
# Run with verbose output
python app.py --verbose

# Run in debug mode
python app.py --debug

# Specify window size
python app.py --width 1920 --height 1080
```

### Configuration

Create a `config.ini` file in the InkPen directory:

```ini
[UI]
theme=dark
toolbar_position=top_right
auto_hide=false

[Drawing]
default_pen_size=2
default_color=#000000
smooth_strokes=true
stroke_smoothness=3

[Performance]
max_strokes=1000
enable_gpu=true
```

## Getting Help

- **Documentation**: See `README.md`
- **Issues**: Open an issue on GitHub
- **Discussions**: Check existing issues first
- **Email**: Contact support@example.com

## Uninstallation

### If using executable:
- Simply delete the `InkPen` folder and `InkPen.zip`

### If using Python source:
1. Delete the `InkPen` folder
2. Remove Python if you installed it only for InkPen

## Updates

### Checking for updates:
1. Visit the [Releases](https://github.com/yourusername/InkPen/releases) page
2. Download the latest version
3. Back up your current version (optional)
4. Extract/run the new version

---

**Need help?** Open an issue or check the FAQ section on GitHub!
