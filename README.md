# LuminaReader 📖

A modern, lightweight Markdown & PDF viewer for Windows with a focus on scientific document rendering.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

<img src="LuminaReader.png" width="128" height="128" alt="LuminaReader Icon">

## Features ✨

### Document Support
- 📄 **Markdown** - Full GitHub-flavored Markdown support with live preview
- 📑 **PDF** - High-quality PDF rendering with text selection and bookmarks
- 🔢 **LaTeX Math** - Perfect rendering of inline and block equations via MathJax
- 💻 **Syntax Highlighting** - Code blocks with language-specific colors

### Modern UI
- 🎨 **Frameless Design** - Clean, modern window without system borders
- 🌓 **Dual Themes** - Dark mode (default) and Light mode (Ctrl+T)
- 🔆 **Brightness Control** - Independent app brightness adjustment
- 📐 **High DPI Support** - Crisp rendering on 4K displays

### Navigation & Tools
- 🔍 **Search** - Find text within documents (Ctrl+F)
- 📑 **Table of Contents** - Auto-generated from document headers (Markdown) and PDF bookmarks
- 🔎 **Zoom Controls** - Mouse wheel + Ctrl zooming
- 🖱️ **Drag & Drop** - Open files by dropping them into the window
- 📑 **Multi-File Tabs** - Open multiple files with tab switching
- 📝 **PDF Annotations** - Highlight (yellow) and draw (cyan pen) on PDFs
- 📤 **Export to PDF** - Convert Markdown files to PDF

---

## 🚀 Quick Start (For Users)

### Option 1: Download Pre-built Binary
Download the latest release from the [Releases](../../releases) page and run `LuminaReader_V1.0.exe`.

### Option 2: Run from Source
```bash
# 1. Clone or download this repository
git clone https://github.com/yourusername/luminareader.git
cd luminareader

# 2. Run the quick start script
run.bat
```

---

## 🛠️ Building from Source (For Developers)

### Prerequisites
| Requirement | Version | Download |
|-------------|---------|----------|
| Python | 3.9 or higher | [python.org](https://www.python.org/downloads/) |
| Windows | 10 or 11 | - |
| Git | Any | [git-scm.com](https://git-scm.com/download/win) |

### Step-by-Step Build Instructions

#### Step 1: Get the Source Code
```bash
# Clone the repository
git clone https://github.com/yourusername/luminareader.git
cd luminareader
```

Or download and extract the ZIP file from GitHub.

#### Step 2: Create Virtual Environment
```bash
# Create a virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# You should see (venv) in your command prompt
```

#### Step 3: Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt
```

This installs:
- **PySide6** - Qt6 GUI framework
- **markdown** - Markdown processing
- **PyMuPDF** - PDF handling for bookmarks
- **pyinstaller** - For building executable

#### Step 4: Run the Application
```bash
# Run directly from source
python main.py

# Or open a specific file
python main.py examples\sample_document.md
```

#### Step 5: Build Executable (Optional)
```bash
# Build the executable using the provided script
build.bat
```

The executable will be created at:
```
dist\LuminaReader_V1.0.exe
```

**Note:** First build may take 5-10 minutes. Subsequent builds are faster.

---

## 📋 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + O` | Open file dialog |
| `Ctrl + F` | Find in document |
| `Ctrl + T` | Toggle dark/light theme |
| `Ctrl + +` | Zoom in |
| `Ctrl + -` | Zoom out |
| `Ctrl + 0` | Reset zoom to 100% |
| `Ctrl + Mouse Wheel` | Zoom in/out |
| `Esc` | Close search bar |

---

## 📁 Project Structure

```
LuminaReader/
│
├── 📄 main.py                 # Main application (single file ~1000 lines)
├── 📄 requirements.txt        # Python dependencies
├── 📄 LuminaReader.spec       # PyInstaller build configuration
├── 📄 build.bat              # One-click build script
├── 📄 run.bat                # Quick development launch
├── 📄 README.md              # This file
├── 📄 BUILD.md               # Detailed build instructions
├── 📄 QUICKSTART.md          # Quick reference
├── 📄 LICENSE                # MIT License
├── 📄 version_info.txt       # Windows version metadata
├── 📄 LuminaReader.iss       # Inno Setup installer script
│
├── 🎨 LuminaReader.png       # Application icon (source)
├── 🎨 LuminaReader.ico       # Application icon (Windows)
│
├── 📁 assets/                # Application assets
└── 📁 examples/              # Sample documents
    └── sample_document.md    # Test document with all features
```

---

## 🎯 Usage Guide

### Opening Files

1. **File Dialog**: Press `Ctrl+O` or click the "📂 Open" button
2. **Drag & Drop**: Drag a `.md` or `.pdf` file into the window
3. **Command Line**: `python main.py "path\to\file.md"`

### PDF Features

**Text Selection**: Simply click and drag to select text in PDFs

**Bookmarks**: PDF bookmarks/outlines are automatically extracted and shown in the left sidebar

**Annotations**:
- Click "🖍️ Highlight" button, then drag to highlight areas in yellow
- Click "✏️ Pen" button, then draw freehand in cyan
- Click "🗑️ Clear" to remove all annotations

### Markdown Features

**Math Rendering**:
- Inline math: `$E = mc^2$` → $E = mc^2$
- Block math:
```latex
$$
\sum_{i=1}^{n} x_i = \frac{1}{n} \sum_{i=1}^{n} x_i
$$
```

**Export to PDF**:
1. Open a Markdown file
2. Click "📤 Export PDF" button
3. Choose save location
4. PDF will be generated

---

## 🔧 Troubleshooting

### Build Issues

**"Python is not recognized"**
- Make sure Python is installed and added to PATH
- Try `py` instead of `python` on Windows

**"pip is not recognized"**
- Reinstall Python and check "Add Python to PATH" during installation

**Virtual environment activation fails**
- On Windows PowerShell, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Then try activating again

**PyInstaller build fails**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Try clean build: `build.bat clean`

### Runtime Issues

**PDF not loading**
- Check internet connection (PDF.js loads from CDN on first use)
- Try refreshing the file

**Math not rendering**
- MathJax requires internet connection
- Check if CDN is accessible

**Fonts look wrong**
- The app uses Google Fonts (Inter, Merriweather)
- Internet connection needed for first load

---

## 🏗️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3.9+ |
| **GUI Framework** | PySide6 (Qt6 bindings) |
| **Rendering Engine** | QWebEngineView (Chromium-based) |
| **Markdown Parser** | Marked.js |
| **Math Renderer** | MathJax 3 |
| **Code Highlighting** | Highlight.js |
| **PDF Viewer** | PDF.js (Mozilla) |

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [PySide6](https://doc.qt.io/qtforpython/) - Qt bindings for Python
- [MathJax](https://www.mathjax.org/) - Beautiful math rendering
- [PDF.js](https://mozilla.github.io/pdf.js/) - Mozilla's PDF renderer
- [Marked](https://marked.js.org/) - Markdown parser
- [Highlight.js](https://highlightjs.org/) - Syntax highlighting

---

<p align="center">
  Made with ❤️ for the scientific community
</p>
