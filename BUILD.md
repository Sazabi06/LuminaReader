# Build Instructions for LuminaReader

Complete guide for building LuminaReader from source code.

---

## 📋 Prerequisites

Before you start, make sure you have:

| Software | Minimum Version | Download Link |
|----------|----------------|---------------|
| Python | 3.9 | [Download Python](https://www.python.org/downloads/) |
| Windows | 10 or 11 | - |
| Git | (Optional) | [Download Git](https://git-scm.com/download/win) |

> **Important:** During Python installation, check **"Add Python to PATH"** option!

---

## 🚀 Quick Build (3 Steps)

The easiest way to build:

```bash
# Step 1: Clone or download this repo
git clone https://github.com/yourusername/luminareader.git
cd luminareader

# Step 2: Run the build script
build.bat

# Step 3: Find your executable
dist\LuminaReader_V1.0.exe
```

That's it! The script will:
- Create a virtual environment
- Install all dependencies
- Build the executable

---

## 🔧 Manual Build (Step-by-Step)

If the quick build doesn't work, follow these detailed steps:

### Step 1: Open Command Prompt or PowerShell

Press `Win + R`, type `cmd`, and press Enter.

Navigate to the project folder:
```bash
cd path\to\luminareader
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
```

This creates a folder named `venv` with isolated Python packages.

### Step 3: Activate Virtual Environment

**Command Prompt:**
```bash
venv\Scripts\activate
```

**PowerShell:**
```powershell
venv\Scripts\Activate.ps1
```

You should see `(venv)` at the start of your prompt.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

Expected packages installed:
- PySide6 (Qt6 framework)
- markdown (Markdown processing)
- PyMuPDF (PDF bookmark extraction)
- pyinstaller (Build tool)

### Step 5: Test the Application

```bash
python main.py
```

If the app opens, you're ready to build!

### Step 6: Build the Executable

```bash
pyinstaller LuminaReader.spec --noconfirm
```

Wait 5-10 minutes for the build to complete.

### Step 7: Find Your Executable

The executable will be at:
```
dist\LuminaReader_V1.0.exe
```

---

## 🔨 Build Options

### Method 1: One-File Build (Default)

Creates a single `.exe` file (~220 MB).

```bash
pyinstaller LuminaReader.spec
```

**Pros:**
- Single file to share
- Easy to distribute

**Cons:**
- Slower startup
- May trigger antivirus warnings

### Method 2: One-Folder Build

Creates a folder with the executable and dependencies (~150 MB total).

Edit `LuminaReader.spec` and change:
```python
exe = EXE(
    ...
    # Add this parameter:
    onefile=False,  # Change to False for folder build
    ...
)
```

Then build:
```bash
pyinstaller LuminaReader.spec
```

**Pros:**
- Faster startup
- Less antivirus issues

**Cons:**
- Multiple files to distribute

---

## 📦 Creating an Installer

To create a professional Windows installer:

### Using Inno Setup

1. Download and install [Inno Setup](https://jrsoftware.org/isinfo.php)

2. Open `LuminaReader.iss` in Inno Setup

3. Click **Build** → **Compile**

4. Find the installer at:
   ```
   installer\LuminaReader_Setup_v1.0.0.exe
   ```

---

## 🐛 Troubleshooting

### "Python is not recognized"

**Solution:**
1. Reinstall Python
2. Check "Add Python to PATH" during installation
3. Restart Command Prompt

### "Cannot activate virtual environment"

**PowerShell Error:**
```powershell
# Run as Administrator first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again
venv\Scripts\Activate.ps1
```

### "pip install fails"

**Solution:**
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Then install requirements
pip install -r requirements.txt
```

### "Build fails with QtWebEngine error"

**Solution:**
```bash
# Reinstall PySide6
pip uninstall PySide6 PySide6-Addons PySide6-Essentials shiboken6 -y
pip install PySide6>=6.5.0
```

### "Antivirus deletes the .exe"

This is a common false positive with PyInstaller builds.

**Solutions:**
1. Use the one-folder build instead of one-file
2. Add the dist folder to antivirus exclusions
3. Sign the executable with a certificate (advanced)

### "Executable won't start"

**Check:**
1. Build completed without errors
2. You're running on Windows 10/11
3. Try building with `--console` to see error messages:
   ```bash
   pyinstaller --console LuminaReader.spec
   ```

---

## 📊 Build Comparison

| Build Type | File Size | Startup Time | Best For |
|------------|-----------|--------------|----------|
| One-File | ~220 MB | 5-10 seconds | Easy sharing |
| One-Folder | ~150 MB | 1-2 seconds | Regular use |
| With Installer | ~70 MB (compressed) | Varies | Distribution |

---

## 🎯 Development Mode

For development and testing, run directly from source:

```bash
# Activate virtual environment
venv\Scripts\activate

# Run the application
python main.py

# Or with a file
python main.py examples\sample_document.md
```

---

## 📝 Customization

### Changing the Icon

Replace `LuminaReader.png` with your own image (recommended: 1024x1024px PNG), then:

```bash
# Requires Pillow
python -c "from PIL import Image; img = Image.open('LuminaReader.png'); img.save('LuminaReader.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])"
```

### Changing App Name

Edit these files:
- `LuminaReader.spec` - Change `name='LuminaReader_V1.0'`
- `version_info.txt` - Update version strings
- `LuminaReader.iss` - Update `#define MyAppName`

---

## 📄 File Association (Advanced)

To make LuminaReader the default app for `.md` and `.pdf` files:

Run as Administrator in Command Prompt:

```cmd
reg add "HKCR\.md" /ve /d "LuminaReader.md" /f
reg add "HKCR\LuminaReader.md" /ve /d "Markdown Document" /f
reg add "HKCR\LuminaReader.md\shell\open\command" /ve /d "\"C:\Path\To\LuminaReader_V1.0.exe\" \"%1\"" /f

reg add "HKCR\.pdf" /ve /d "LuminaReader.pdf" /f
reg add "HKCR\LuminaReader.pdf" /ve /d "PDF Document" /f
reg add "HKCR\LuminaReader.pdf\shell\open\command" /ve /d "\"C:\Path\To\LuminaReader_V1.0.exe\" \"%1\"" /f
```

---

## ✅ Build Checklist

Before distributing your build:

- [ ] Executable launches without errors
- [ ] Can open Markdown files
- [ ] Can open PDF files
- [ ] Theme toggle works (Ctrl+T)
- [ ] Zoom controls work (Ctrl++, Ctrl+-)
- [ ] Search works (Ctrl+F)
- [ ] Math renders correctly
- [ ] Code highlighting works
- [ ] Text is selectable in PDFs
- [ ] PDF bookmarks display in sidebar

---

## 📚 Additional Resources

- [PyInstaller Documentation](https://pyinstaller.org/)
- [PySide6 Documentation](https://doc.qt.io/qtforpython/)
- [Inno Setup Documentation](https://jrsoftware.org/ishelp/)

---

**Need Help?** Open an issue on GitHub with your error message.
