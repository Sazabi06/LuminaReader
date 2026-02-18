# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for LuminaReader
======================================

This file configures PyInstaller to build LuminaReader as a standalone executable.

Usage:
    pyinstaller LuminaReader.spec

Output:
    dist/LuminaReader.exe - Single executable file
"""

block_cipher = None

# Analysis configuration
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Add any data files here (e.g., assets, templates)
        # ('assets', 'assets'),
    ],
    hiddenimports=[
        # PySide6 WebEngine components
        'PySide6.QtWebEngineWidgets',
        'PySide6.QtWebEngineCore',
        'PySide6.QtWebChannel',
        'PySide6.QtNetwork',
        'PySide6.QtPrintSupport',
        
        # Additional Qt modules
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        
        # Python standard library modules that might be missed
        'pathlib',
        'json',
        're',
        'math',
        'base64',
        'datetime',
        
        # PDF and Markdown processing
        'fitz',  # PyMuPDF
        'markdown',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'sklearn',
        'tensorflow',
        'torch',
        'PIL',
        'cv2',
        'pytest',
        'unittest',
        'pydoc',
        'email',
        'http',
        'xmlrpc',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Create PYZ archive
pyz = PYZ(
    a.pure, 
    a.zipped_data, 
    cipher=block_cipher
)

# Create executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='LuminaReader_V1.0',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Enable UPX compression
    upx_exclude=[
        # Files that may cause issues with UPX
        'vcruntime140.dll',
        'python*.dll',
    ],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='LuminaReader.ico',  # Application icon
    version='version_info.txt',  # Version info file (optional)
)

# Collect all files for directory build (alternative to single file)
# Uncomment below for directory build instead of single file
"""
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='LuminaReader'
)
"""
