# InkPen - Quick Start Guide

## Installation (Choose One)

### 🚀 Easiest: Download EXE

1. Go to [Releases](../../releases)
2. Download `InkPen.exe`
3. Double-click to run (no installation needed)
4. Floating toolbar appears - start annotating!

### 🛠️ From Source (For Developers)

```bash
# 1. Clone repo
git clone https://github.com/yourusername/inkpen.git
cd inkpen

# 2. Create Python environment (optional)
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python main.py
```

### 📦 Build Your Own EXE

```bash
# After installing dependencies:
pip install pyinstaller

# Build executable
pyinstaller inkpen.spec --onefile

# Find it at: dist/InkPen.exe
```

## First Time Using InkPen

1. **Launch the app** - EXE or `python main.py`
2. **Toolbar appears** - Small window with tool buttons
3. **Select a tool** - Click pen, highlighter, etc.
4. **Start drawing** - Click and drag on screen
5. **Switch apps** - Toolbar stays on top! Keep drawing
6. **Done** - Click X button to close or clear drawings with trash icon

## Tool Quick Reference

| Tool | Use For | How To Use |
|------|---------|-----------|
| 🖱️ Cursor | Normal clicking | Click to pass clicks through to windows |
| ✏️ Pen | Free drawing | Select color, then click-drag to draw |
| 🎨 Highlighter | Transparent highlight | Click-drag to highlight with opacity |
| 📊 Pen Size | Change thickness | Click button to select size |
| 📝 Text | Add text | Click location, type text in dialog |
| 📐 Shapes | Draw shapes | Select shape, click-drag to draw |
| 🗑️ Eraser | Remove strokes | Click-drag to erase entire connected strokes |
| 🎨 Colors | Choose colors | Click to open color picker popup |

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Z` | Undo last action |
| `X` | Switch to eraser |
| `C` | Switch to cursor mode |

## Common Tasks

### Draw on any screen
```
1. Click Pen tool ✏️
2. Choose color (click 🎨)
3. Click-drag on screen to draw
4. Annotations appear instantly over any app
```

### Highlight important text
```
1. Click Highlighter tool 🎨
2. Select highlight color
3. Click-drag over text
4. Semi-transparent highlight appears
```

### Add shapes and arrows
```
1. Click Shape tool 📐
2. Pick shape from popup (line, arrow, rect, etc.)
3. Click-drag on screen
4. Shape appears with current color and size
```

### Add text labels
```
1. Click Text tool 📝
2. Click where you want text
3. Type in dialog box
4. Text appears on screen in chosen color
```

### Fix mistakes
```
Option 1: Use eraser 🗑️ - removes entire stroke
Option 2: Press Ctrl+Z - undo last action
Option 3: Click Clear All 🗑️ - removes everything
```

### Return to normal use
```
Click Cursor tool 🖱️ to enable click-through
- Toolbar stays on top
- Clicks pass through to windows below
- Click Pen tool to resume drawing
```

## Settings & Customization

Settings are automatically saved:
- **Last tool used** - Toolbar remembers your choice
- **Colors** - Pen and highlighter colors persist
- **Pen size** - Your size preference is saved
- **Toolbar position** - Stays where you drag it

All settings stored in Windows Registry (auto-managed).

## Tips & Tricks

### 💡 Pro Tips

1. **Drag the toolbar** - Click the drag handle at top to move it anywhere
2. **Pen size variety** - 8 preset sizes, find your favorite
3. **Precision drawing** - Use pen tool for freehand, shapes for geometric
4. **Color combos** - 12 preset pen colors + 6 highlight colors + custom picker
5. **Undo is your friend** - Ctrl+Z always available
6. **Multiple strokes** - Each press-drag-release is one stroke (erase removes whole stroke)

### ⚡ Speed Tricks

1. Click color indicator (circle) to quickly open color picker
2. Right-click toolbar title bar to get system menu
3. Drag toolbar by title to reposition
4. Use keyboard shortcuts for quick tool switching

### 🎨 Color Tips

- **Pen colors**: 12 presets + unlimited custom colors
- **Highlighter**: 6 presets, all have transparency
- **Custom color**: Click "Custom" in color picker to use any color

## Troubleshooting

### "Can't find Python"
- Download the EXE version instead
- Or: `pip install python` (in case Python not in PATH)

### "Toolbar disappeared"
- Restart the app
- Position is saved, toolbar will return to last location

### "Can't draw on certain apps"
- Some apps (games) may block overlays
- Try cursor mode to interact with those apps
- Consider annotating screenshots instead

### "Drawing is slow"
- Close unnecessary background apps
- Reduce number of strokes (use Clear All)
- Update graphics drivers

### "Drawings look pixelated"
- Your monitor's DPI scaling
- InkPen auto-detects but restart if issues persist

## Performance

- **CPU**: Very low (only processes when drawing)
- **RAM**: ~100MB typical
- **Startup**: < 2 seconds
- **Drawing**: 60+ FPS smooth
- **File Size**: ~150MB (standalone EXE)

## System Requirements

✅ **Requirements:**
- Windows 10 (Build 14393+) or Windows 11
- 64-bit architecture
- 200MB free disk space
- Any modern processor

❌ **Not supported:**
- Windows 7/8
- 32-bit Windows
- Linux/macOS

## Next Steps

- 📖 Read full [README.md](README.md)
- 🤝 Contribute on [GitHub](../../)
- 🐛 Report bugs on [Issues](../../issues)
- ⭐ Star the repo if you like it!

---

**Need help?** Open an issue on GitHub or check the README for more details.

**Happy annotating!** ✨
