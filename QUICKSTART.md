# LuminaReader - Quick Start Guide
===================================

## 🚀 Getting Started (5 Minutes)

### Option 1: Run from Source (Recommended for Development)

```bash
# 1. Navigate to project folder
cd LuminaReader

# 2. Run the quick start script
run.bat
```

Or manually:

```bash
# 1. Create virtual environment (first time only)
python -m venv venv

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Install dependencies (first time only)
pip install -r requirements.txt

# 4. Run the application
python main.py
```

### Option 2: Build Executable

```bash
# Build the executable
build.bat

# Run the built executable
dist\LuminaReader.exe
```

## 📖 Opening Files

### Method 1: File Dialog
- Press `Ctrl + O`
- Or click the "📂 Open" button in the toolbar

### Method 2: Drag & Drop
- Drag any `.md` or `.pdf` file into the window

### Method 3: Command Line
```bash
python main.py "path\to\your\file.md"
```

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + O` | Open file |
| `Ctrl + F` | Find in document |
| `Ctrl + T` | Toggle dark/light theme |
| `Ctrl + +` | Zoom in |
| `Ctrl + -` | Zoom out |
| `Ctrl + 0` | Reset zoom |
| `Ctrl + Mouse Wheel` | Zoom in/out |
| `Esc` | Close search bar |

## 🎨 Features Overview

### Document Rendering
- ✅ **Markdown** - Full GFM support with syntax highlighting
- ✅ **PDF** - High-quality rendering with smooth scrolling
- ✅ **Math** - LaTeX equations via MathJax
- ✅ **Code** - Syntax highlighting for 100+ languages

### User Interface
- 🌙 **Dark Mode** - Default eye-friendly theme
- ☀️ **Light Mode** - Toggle with Ctrl+T
- 🔆 **Brightness** - Independent app brightness control
- 📐 **High DPI** - 4K display support

### Navigation
- 🔍 **Search** - Find text in documents
- 📑 **TOC** - Auto-generated table of contents
- 🔎 **Zoom** - Smooth zoom with mouse wheel
- 🖱️ **Drag & Drop** - Quick file opening

## 🧪 Testing

Try opening the sample document:

```bash
python main.py examples\sample_document.md
```

This document demonstrates:
- Typography and formatting
- Code blocks with syntax highlighting
- Mathematical equations
- Tables and lists
- Blockquotes

## 🛠️ Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "QtWebEngine not found" error
```bash
pip uninstall PySide6 -y
pip install PySide6>=6.5.0
```

### Application won't start
1. Check Python version: `python --version` (need 3.9+)
2. Check Windows version (Windows 10/11 required)
3. Try running from command line to see error messages

## 📦 Project Structure

```
LuminaReader/
├── main.py              # Main application
├── requirements.txt     # Dependencies
├── run.bat             # Quick launch script
├── build.bat           # Build executable
├── examples/           # Sample files
│   └── sample_document.md
├── BUILD.md            # Detailed build guide
├── README.md           # Full documentation
└── QUICKSTART.md       # This file
```

## 🎯 Next Steps

1. **Try it out** - Open the sample document
2. **Open your files** - Test with your own Markdown/PDF files
3. **Customize** - Edit themes in `main.py`
4. **Build** - Create standalone executable
5. **Distribute** - Share with others!

## 💡 Tips

- **Math Rendering**: Use `$...$` for inline math and `$$...$$` for block equations
- **Code Blocks**: Specify language for syntax highlighting (e.g., ```python)
- **Images**: Relative paths work for images in the same folder as the Markdown file
- **Zoom**: Hold Ctrl and scroll mouse wheel for quick zoom

## 🆘 Getting Help

- Check [BUILD.md](BUILD.md) for detailed build instructions
- Check [README.md](README.md) for full documentation
- Report issues on GitHub

---

**Enjoy reading with LuminaReader!** 📖✨
