#!/usr/bin/env python3
"""
LuminaReader - A Modern, Lightweight Markdown & PDF Viewer
===========================================================
A frameless Windows desktop application for viewing Markdown and PDF files
with high-fidelity rendering, math support, and modern UI.

Author: LuminaReader Team
License: MIT
"""

import sys
import os
import json
import re
import math
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Callable

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QStackedWidget, QFileDialog, QMessageBox,
    QSlider, QLineEdit, QScrollArea, QFrame, QSizePolicy, QMenu,
    QSystemTrayIcon, QToolButton, QGraphicsOpacityEffect
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings, QWebEngineProfile
from PySide6.QtCore import (
    Qt, QTimer, QUrl, QSize, QPoint, QMimeData, QThread, Signal,
    QObject, QEvent, QPropertyAnimation, QEasingCurve
)
from PySide6.QtGui import (
    QFont, QIcon, QPixmap, QDragEnterEvent, QDropEvent, QMouseEvent,
    QKeyEvent, QCursor, QScreen, QFontDatabase, QAction, QPalette, QColor
)

# =============================================================================
# CONSTANTS & CONFIGURATION
# =============================================================================

APP_NAME = "LuminaReader"
APP_VERSION = "1.0.0"
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600
TITLE_BAR_HEIGHT = 40
STATUS_BAR_HEIGHT = 30
SIDEBAR_WIDTH = 280

# Theme Colors
THEMES = {
    "dark": {
        "name": "Dark",
        "bg_primary": "#1a1a1a",
        "bg_secondary": "#252525",
        "bg_tertiary": "#2d2d2d",
        "text_primary": "#e8e8e8",
        "text_secondary": "#a0a0a0",
        "accent": "#4a9eff",
        "accent_hover": "#3a8eef",
        "border": "#3a3a3a",
        "button_hover": "#3a3a3a",
        "button_pressed": "#454545",
        "success": "#4caf50",
        "warning": "#ff9800",
        "error": "#f44336"
    },
    "light": {
        "name": "Light",
        "bg_primary": "#f5f5f5",
        "bg_secondary": "#ffffff",
        "bg_tertiary": "#eeeeee",
        "text_primary": "#333333",
        "text_secondary": "#666666",
        "accent": "#2196f3",
        "accent_hover": "#1976d2",
        "border": "#dddddd",
        "button_hover": "#e0e0e0",
        "button_pressed": "#d0d0d0",
        "success": "#4caf50",
        "warning": "#ff9800",
        "error": "#f44336"
    }
}

# MathJax Configuration
MATHJAX_CONFIG = """
<script>
window.MathJax = {
    tex: {
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
        processEscapes: true,
        processEnvironments: true,
        packages: {'[+]': ['ams', 'noerrors', 'noundefined']}
    },
    options: {
        skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
    },
    loader: {
        load: ['[tex]/ams', '[tex]/noerrors', '[tex]/noundefined']
    },
    startup: {
        pageReady: () => {
            return MathJax.startup.defaultPageReady();
        }
    }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.min.js" async></script>
"""

# Highlight.js for code syntax highlighting
HIGHLIGHT_JS = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/cpp.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/javascript.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/bash.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/json.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/xml.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/css.min.js"></script>
<script>hljs.highlightAll();</script>
"""



# PDF.js for PDF rendering
PDF_JS_CDN = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"
PDF_JS_WORKER_CDN = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js"

# Marked.js for Markdown parsing
MARKED_JS = """
<script src="https://cdn.jsdelivr.net/npm/marked@9.1.6/marked.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked-gfm-heading-id@3.1.3/lib/index.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked-highlight@2.0.6/lib/index.umd.min.js"></script>
"""


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"


def count_words_in_markdown(text: str) -> int:
    """Count words in markdown text (excluding syntax)."""
    # Remove code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)
    # Remove inline code
    text = re.sub(r'`[^`]*`', '', text)
    # Remove markdown syntax
    text = re.sub(r'[#*_[\](){}|`~]', ' ', text)
    # Remove LaTeX
    text = re.sub(r'\$+[^$]+\$+', '', text)
    # Count words
    words = text.split()
    return len(words)


# =============================================================================
# HTML TEMPLATES
# =============================================================================

def get_base_html(theme: str = "dark", font_family: str = "sans-serif") -> str:
    """Generate base HTML template with theme and font configuration."""
    theme_colors = THEMES[theme]
    
    font_css = """
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Merriweather:wght@300;400;700&family=Fira+Code:wght@400;500&display=swap');
    """
    
    if font_family == "serif":
        content_font = "'Merriweather', Georgia, serif"
    else:
        content_font = "'Inter', -apple-system, BlinkMacSystemFont, sans-serif"
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LuminaReader</title>
    <style>
        {font_css}
        
        :root {{
            --bg-primary: {theme_colors['bg_primary']};
            --bg-secondary: {theme_colors['bg_secondary']};
            --bg-tertiary: {theme_colors['bg_tertiary']};
            --text-primary: {theme_colors['text_primary']};
            --text-secondary: {theme_colors['text_secondary']};
            --accent: {theme_colors['accent']};
            --accent-hover: {theme_colors['accent_hover']};
            --border: {theme_colors['border']};
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        html, body {{
            height: 100%;
            font-family: {content_font};
            background-color: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            overflow-x: hidden;
        }}
        
        body {{
            padding: 40px 60px;
            max-width: 900px;
            margin: 0 auto;
        }}
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            font-weight: 600;
            line-height: 1.3;
            color: var(--text-primary);
        }}
        
        h1 {{ font-size: 2.2em; border-bottom: 2px solid var(--border); padding-bottom: 0.3em; }}
        h2 {{ font-size: 1.8em; border-bottom: 1px solid var(--border); padding-bottom: 0.2em; }}
        h3 {{ font-size: 1.5em; }}
        h4 {{ font-size: 1.25em; }}
        h5 {{ font-size: 1.1em; }}
        h6 {{ font-size: 1em; color: var(--text-secondary); }}
        
        p {{
            margin-bottom: 1em;
            text-align: justify;
        }}
        
        /* Links */
        a {{
            color: var(--accent);
            text-decoration: none;
            transition: color 0.2s;
        }}
        
        a:hover {{
            color: var(--accent-hover);
            text-decoration: underline;
        }}
        
        /* Lists */
        ul, ol {{
            margin-bottom: 1em;
            padding-left: 2em;
        }}
        
        li {{
            margin-bottom: 0.3em;
        }}
        
        /* Code */
        code {{
            font-family: 'Fira Code', 'Consolas', monospace;
            background-color: var(--bg-tertiary);
            padding: 0.2em 0.4em;
            border-radius: 4px;
            font-size: 0.9em;
        }}
        
        pre {{
            background-color: var(--bg-tertiary);
            padding: 1em;
            border-radius: 8px;
            overflow-x: auto;
            margin-bottom: 1em;
        }}
        
        pre code {{
            background: none;
            padding: 0;
        }}
        
        /* Blockquotes */
        blockquote {{
            border-left: 4px solid var(--accent);
            padding-left: 1em;
            margin-left: 0;
            margin-bottom: 1em;
            color: var(--text-secondary);
            font-style: italic;
        }}
        
        /* Tables */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 1em;
        }}
        
        th, td {{
            padding: 0.75em;
            text-align: left;
            border: 1px solid var(--border);
        }}
        
        th {{
            background-color: var(--bg-tertiary);
            font-weight: 600;
        }}
        
        tr:nth-child(even) {{
            background-color: var(--bg-secondary);
        }}
        
        /* Images */
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 1em 0;
        }}
        
        /* Horizontal Rule */
        hr {{
            border: none;
            border-top: 2px solid var(--border);
            margin: 2em 0;
        }}
        
        /* Math */
        .math-inline {{
            display: inline-block;
            vertical-align: middle;
        }}
        
        .math-display {{
            display: block;
            text-align: center;
            margin: 1em 0;
            overflow-x: auto;
        }}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: var(--bg-primary);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: var(--bg-tertiary);
            border-radius: 5px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: var(--border);
        }}
        
        /* Selection */
        ::selection {{
            background-color: var(--accent);
            color: white;
        }}
        
        /* Search highlight */
        .search-highlight {{
            background-color: #ffeb3b;
            color: #000;
            padding: 0 2px;
            border-radius: 2px;
        }}
        
        /* Loading */
        .loading {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-size: 1.2em;
            color: var(--text-secondary);
        }}
        
        /* PDF Container */
        #pdf-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }}
        
        .pdf-page {{
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            background: white;
        }}
        
        .pdf-page canvas {{
            display: block;
        }}
        
        /* TOC */
        #toc {{
            position: fixed;
            left: 0;
            top: 0;
            width: 250px;
            height: 100%;
            background: var(--bg-secondary);
            border-right: 1px solid var(--border);
            padding: 20px;
            overflow-y: auto;
            transform: translateX(-100%);
            transition: transform 0.3s ease;
        }}
        
        #toc.visible {{
            transform: translateX(0);
        }}
        
        .toc-item {{
            padding: 8px 12px;
            cursor: pointer;
            border-radius: 4px;
            transition: background 0.2s;
        }}
        
        .toc-item:hover {{
            background: var(--bg-tertiary);
        }}
        
        .toc-h1 {{ font-weight: 600; }}
        .toc-h2 {{ padding-left: 20px; }}
        .toc-h3 {{ padding-left: 40px; font-size: 0.9em; }}
    </style>
    {MARKED_JS}
    {MATHJAX_CONFIG}
    {HIGHLIGHT_JS}
</head>
<body>
    <div id="content"></div>
    <script>
        // Initialize marked with plugins
        marked.use(markedGfmHeadingId.gfmHeadingId());
        marked.use(markedHighlight.markedHighlight({{
            langPrefix: 'hljs language-',
            highlight: function(code, lang) {{
                const language = hljs.getLanguage(lang) ? lang : 'plaintext';
                return hljs.highlight(code, {{ language }}).value;
            }}
        }}));
        
        // Configure marked options
        marked.setOptions({{
            gfm: true,
            breaks: true,
            headerIds: true,
            mangle: false
        }});
        
        // Global functions for Qt to call
        window.renderMarkdown = function(content) {{
            document.getElementById('content').innerHTML = marked.parse(content);
            // Re-highlight code blocks
            hljs.highlightAll();
            // Re-render MathJax
            if (window.MathJax) {{
                MathJax.typesetPromise();
            }}
        }};
        
        window.setTheme = function(themeName) {{
            document.documentElement.setAttribute('data-theme', themeName);
        }};
        
        window.setFont = function(fontName) {{
            document.body.style.fontFamily = fontName === 'serif' 
                ? "'Merriweather', Georgia, serif" 
                : "'Inter', -apple-system, BlinkMacSystemFont, sans-serif";
        }};
        
        window.zoom = function(factor) {{
            document.body.style.zoom = factor;
        }};
        
        window.findText = function(query) {{
            // Remove previous highlights
            document.querySelectorAll('.search-highlight').forEach(el => {{
                const parent = el.parentNode;
                parent.replaceChild(document.createTextNode(el.textContent), el);
                parent.normalize();
            }});
            
            if (!query) return 0;
            
            let count = 0;
            const walker = document.createTreeWalker(
                document.body,
                NodeFilter.SHOW_TEXT,
                null,
                false
            );
            
            const nodes = [];
            let node;
            while (node = walker.nextNode()) {{
                if (node.nodeValue.toLowerCase().includes(query.toLowerCase())) {{
                    nodes.push(node);
                }}
            }}
            
            nodes.forEach(node => {{
                const span = document.createElement('span');
                span.className = 'search-highlight';
                const regex = new RegExp(`(${{query}})`, 'gi');
                const parts = node.nodeValue.split(regex);
                
                parts.forEach((part, i) => {{
                    if (part.toLowerCase() === query.toLowerCase()) {{
                        const mark = document.createElement('span');
                        mark.className = 'search-highlight';
                        mark.textContent = part;
                        node.parentNode.insertBefore(mark, node);
                        count++;
                    }} else {{
                        node.parentNode.insertBefore(document.createTextNode(part), node);
                    }}
                }});
                
                node.parentNode.removeChild(node);
            }});
            
            return count;
        }};
        
        window.scrollToHeading = function(headingId) {{
            const element = document.getElementById(headingId);
            if (element) {{
                element.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }}
        }};
        
        window.getHeadings = function() {{
            const headings = [];
            document.querySelectorAll('h1, h2, h3, h4, h5, h6').forEach((el, i) => {{
                if (!el.id) el.id = 'heading-' + i;
                headings.push({{
                    level: parseInt(el.tagName[1]),
                    text: el.textContent,
                    id: el.id
                }});
            }});
            return JSON.stringify(headings);
        }};
    </script>
</body>
</html>"""


def get_pdf_viewer_html(theme: str = "dark") -> str:
    """Generate HTML template for PDF viewing using PDF.js with text selection and annotation support."""
    theme_colors = THEMES[theme]
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PDF Viewer - LuminaReader</title>
    <script src="{PDF_JS_CDN}"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            user-select: text;
            -webkit-user-select: text;
        }}
        
        html, body {{
            height: 100%;
            background-color: {theme_colors['bg_primary']};
            overflow-y: auto;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        
        #pdf-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
            min-height: 100%;
        }}
        
        .pdf-page-wrapper {{
            position: relative;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
            background: white;
        }}
        
        .pdf-page {{
            display: block;
        }}
        
        .pdf-text-layer {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            overflow: hidden;
            opacity: 1;
            line-height: 1.0;
        }}
        
        .pdf-text-layer > span {{
            position: absolute;
            white-space: pre;
            cursor: text;
            transform-origin: 0% 0%;
            color: transparent;
            opacity: 0;
        }}
        
        .pdf-text-layer > span:hover {{
            opacity: 0.1;
        }}
        
        .pdf-text-layer ::selection {{
            background: rgba(74, 158, 255, 0.5);
            color: transparent;
        }}
        
        .annotation-layer {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            pointer-events: auto;
            z-index: 10;
        }}
        
        .highlight-annotation {{
            position: absolute;
            background-color: rgba(255, 255, 0, 0.4);
            pointer-events: none;
            border-radius: 2px;
        }}
        
        .pen-annotation {{
            position: absolute;
            pointer-events: none;
        }}
        
        .pen-annotation svg {{
            width: 100%;
            height: 100%;
        }}
        
        .annotation-toolbar {{
            position: fixed;
            top: 10px;
            right: 10px;
            background: {theme_colors['bg_secondary']};
            border: 1px solid {theme_colors['border']};
            border-radius: 8px;
            padding: 8px;
            display: flex;
            gap: 8px;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }}
        
        .annotation-btn {{
            padding: 6px 12px;
            border: 1px solid {theme_colors['border']};
            background: {theme_colors['bg_tertiary']};
            color: {theme_colors['text_primary']};
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            display: flex;
            align-items: center;
            gap: 4px;
        }}
        
        .annotation-btn:hover {{
            background: {theme_colors['button_hover']};
        }}
        
        .annotation-btn.active {{
            background: {theme_colors['accent']};
            color: white;
            border-color: {theme_colors['accent']};
        }}
        
        .loading {{
            color: {theme_colors['text_secondary']};
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            padding: 40px;
            text-align: center;
        }}
        
        .error {{
            color: {theme_colors['error']};
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            padding: 40px;
            text-align: center;
        }}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {theme_colors['bg_primary']};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {theme_colors['bg_tertiary']};
            border-radius: 5px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {theme_colors['border']};
        }}
    </style>
</head>
<body>
    <div class="annotation-toolbar" id="annotationToolbar">
        <button class="annotation-btn" id="btnSelect" title="Select Text (Default)">
            🖱️ Select
        </button>
        <button class="annotation-btn" id="btnHighlight" title="Highlight (Yellow)">
            🖍️ Highlight
        </button>
        <button class="annotation-btn" id="btnPen" title="Pen (Cyan)">
            ✏️ Pen
        </button>
        <button class="annotation-btn" id="btnClear" title="Clear Annotations">
            🗑️ Clear
        </button>
    </div>
    
    <div id="pdf-container">
        <div class="loading">Loading PDF...</div>
    </div>
    
    <script>
        pdfjsLib.GlobalWorkerOptions.workerSrc = '{PDF_JS_WORKER_CDN}';
        
        let pdfDoc = null;
        let displayScale = 1.5;
        let currentPage = 1;
        let totalPages = 0;
        const MAX_DPI = 1600;
        const BASE_DPI = 72;
        
        // Annotation state
        let annotationMode = 'select'; // 'select', 'highlight', 'pen'
        let isDrawing = false;
        let currentPath = [];
        let annotations = {{}}; // pageNum -> [annotations]
        
        // Setup annotation toolbar
        document.getElementById('btnSelect').addEventListener('click', () => setAnnotationMode('select'));
        document.getElementById('btnHighlight').addEventListener('click', () => setAnnotationMode('highlight'));
        document.getElementById('btnPen').addEventListener('click', () => setAnnotationMode('pen'));
        document.getElementById('btnClear').addEventListener('click', clearAnnotations);
        
        function setAnnotationMode(mode) {{
            annotationMode = mode;
            document.querySelectorAll('.annotation-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById('btn' + mode.charAt(0).toUpperCase() + mode.slice(1)).classList.add('active');
            
            // Update cursor for all annotation layers
            document.querySelectorAll('.annotation-layer').forEach(layer => {{
                layer.style.cursor = mode === 'select' ? 'default' : 'crosshair';
            }});
        }}
        
        function clearAnnotations() {{
            annotations = {{}};
            document.querySelectorAll('.highlight-annotation, .pen-annotation').forEach(el => el.remove());
        }}
        
        window.loadPDF = async function(pdfData) {{
            try {{
                const container = document.getElementById('pdf-container');
                container.innerHTML = '<div class="loading">Loading PDF...</div>';
                
                // Convert base64 to Uint8Array
                const binaryString = window.atob(pdfData);
                const bytes = new Uint8Array(binaryString.length);
                for (let i = 0; i < binaryString.length; i++) {{
                    bytes[i] = binaryString.charCodeAt(i);
                }}
                
                pdfDoc = await pdfjsLib.getDocument({{ data: bytes }}).promise;
                totalPages = pdfDoc.numPages;
                
                container.innerHTML = '';
                
                for (let pageNum = 1; pageNum <= totalPages; pageNum++) {{
                    await renderPage(pageNum);
                }}
                
                // Set initial mode
                setAnnotationMode('select');
                
                // Notify Qt that PDF is loaded
                if (window.qt) {{
                    window.qt.pdfLoaded(totalPages);
                }}
                
            }} catch (error) {{
                document.getElementById('pdf-container').innerHTML = 
                    '<div class="error">Error loading PDF: ' + error.message + '</div>';
            }}
        }};
        
        async function renderPage(pageNum) {{
            const page = await pdfDoc.getPage(pageNum);
            
            // Display viewport
            const displayViewport = page.getViewport({{ scale: displayScale }});
            
            // Calculate render scale
            const dpr = window.devicePixelRatio || 1;
            const maxRenderMultiplier = MAX_DPI / (BASE_DPI * displayScale);
            const renderMultiplier = Math.min(Math.max(dpr, 2), maxRenderMultiplier);
            const renderScale = displayScale * renderMultiplier;
            const renderViewport = page.getViewport({{ scale: renderScale }});
            
            // Create wrapper
            const wrapper = document.createElement('div');
            wrapper.className = 'pdf-page-wrapper';
            wrapper.style.width = Math.floor(displayViewport.width) + 'px';
            wrapper.style.height = Math.floor(displayViewport.height) + 'px';
            wrapper.dataset.pageNum = pageNum;
            
            // Create canvas
            const canvas = document.createElement('canvas');
            canvas.className = 'pdf-page';
            const context = canvas.getContext('2d');
            
            canvas.width = Math.floor(renderViewport.width);
            canvas.height = Math.floor(renderViewport.height);
            canvas.style.width = Math.floor(displayViewport.width) + 'px';
            canvas.style.height = Math.floor(displayViewport.height) + 'px';
            
            wrapper.appendChild(canvas);
            
            // Create text layer for selection
            const textLayer = document.createElement('div');
            textLayer.className = 'pdf-text-layer';
            textLayer.style.width = Math.floor(displayViewport.width) + 'px';
            textLayer.style.height = Math.floor(displayViewport.height) + 'px';
            wrapper.appendChild(textLayer);
            
            // Create annotation layer
            const annotationLayer = document.createElement('div');
            annotationLayer.className = 'annotation-layer';
            annotationLayer.style.width = Math.floor(displayViewport.width) + 'px';
            annotationLayer.style.height = Math.floor(displayViewport.height) + 'px';
            setupAnnotationLayer(annotationLayer, pageNum, displayScale);
            wrapper.appendChild(annotationLayer);
            
            const container = document.getElementById('pdf-container');
            container.appendChild(wrapper);
            
            // Render page
            await page.render({{
                canvasContext: context,
                viewport: renderViewport
            }}).promise;
            
            // Render text layer
            const textContent = await page.getTextContent();
            await renderTextLayer(textLayer, textContent, displayViewport, renderViewport);
        }}
        
        async function renderTextLayer(textLayerDiv, textContent, viewport, renderViewport) {{
            const scale = viewport.scale / renderViewport.scale;
            const textItems = textContent.items;
            
            for (const item of textItems) {{
                const tx = pdfjsLib.Util.transform(viewport.transform, item.transform);
                const fontHeight = Math.hypot(tx[0], tx[1]);
                const fontWidth = Math.hypot(tx[2], tx[3]);
                
                const span = document.createElement('span');
                span.textContent = item.str;
                span.style.left = tx[4] + 'px';
                span.style.top = tx[5] - fontHeight + 'px';
                span.style.fontSize = fontHeight + 'px';
                span.style.fontFamily = item.fontName || 'sans-serif';
                
                if (item.width > 0) {{
                    const transform = `scaleX(${{item.width * renderViewport.scale / (item.str.length * fontHeight)}})`;
                    span.style.transform = transform;
                }}
                
                textLayerDiv.appendChild(span);
            }}
        }}
        
        function setupAnnotationLayer(layer, pageNum, scale) {{
            let isDrawing = false;
            let currentHighlight = null;
            let currentPenPath = null;
            let startX, startY;
            
            layer.addEventListener('mousedown', (e) => {{
                if (annotationMode === 'select') return;
                
                isDrawing = true;
                const rect = layer.getBoundingClientRect();
                startX = e.clientX - rect.left;
                startY = e.clientY - rect.top;
                
                if (annotationMode === 'highlight') {{
                    currentHighlight = document.createElement('div');
                    currentHighlight.className = 'highlight-annotation';
                    currentHighlight.style.left = startX + 'px';
                    currentHighlight.style.top = startY + 'px';
                    layer.appendChild(currentHighlight);
                }} else if (annotationMode === 'pen') {{
                    currentPenPath = [{{x: startX, y: startY}}];
                }}
            }});
            
            layer.addEventListener('mousemove', (e) => {{
                if (!isDrawing) return;
                
                const rect = layer.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                if (annotationMode === 'highlight' && currentHighlight) {{
                    const left = Math.min(startX, x);
                    const top = Math.min(startY, y);
                    const width = Math.abs(x - startX);
                    const height = Math.abs(y - startY);
                    
                    currentHighlight.style.left = left + 'px';
                    currentHighlight.style.top = top + 'px';
                    currentHighlight.style.width = width + 'px';
                    currentHighlight.style.height = height + 'px';
                }} else if (annotationMode === 'pen') {{
                    currentPenPath.push({{x, y}});
                }}
            }});
            
            layer.addEventListener('mouseup', () => {{
                if (!isDrawing) return;
                isDrawing = false;
                
                if (annotationMode === 'pen' && currentPenPath && currentPenPath.length > 1) {{
                    renderPenPath(layer, currentPenPath);
                }}
                
                currentHighlight = null;
                currentPenPath = null;
            }});
        }}
        
        function renderPenPath(layer, path) {{
            if (path.length < 2) return;
            
            const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
            svg.className = 'pen-annotation';
            svg.style.position = 'absolute';
            svg.style.top = '0';
            svg.style.left = '0';
            svg.style.width = '100%';
            svg.style.height = '100%';
            svg.style.pointerEvents = 'none';
            
            const polyline = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
            const points = path.map(p => `${{p.x}},${{p.y}}`).join(' ');
            polyline.setAttribute('points', points);
            polyline.setAttribute('fill', 'none');
            polyline.setAttribute('stroke', '#00ffff');
            polyline.setAttribute('stroke-width', '2');
            polyline.setAttribute('stroke-linecap', 'round');
            polyline.setAttribute('stroke-linejoin', 'round');
            
            svg.appendChild(polyline);
            layer.appendChild(svg);
        }}
        
        window.setZoom = function(newDisplayScale) {{
            displayScale = newDisplayScale;
            if (pdfDoc) {{
                const container = document.getElementById('pdf-container');
                container.innerHTML = '';
                for (let pageNum = 1; pageNum <= totalPages; pageNum++) {{
                    renderPage(pageNum);
                }}
            }}
        }};
        
        window.getCurrentPage = function() {{
            const pages = document.querySelectorAll('.pdf-page-wrapper');
            const scrollTop = window.scrollY;
            
            for (let i = 0; i < pages.length; i++) {{
                const rect = pages[i].getBoundingClientRect();
                if (rect.top >= 0 && rect.top < window.innerHeight / 2) {{
                    return i + 1;
                }}
            }}
            
            return 1;
        }};
        
        window.scrollToPage = function(pageNum) {{
            const pages = document.querySelectorAll('.pdf-page-wrapper');
            if (pages[pageNum - 1]) {{
                pages[pageNum - 1].scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }}
        }};
        
        window.getSelectedText = function() {{
            return window.getSelection().toString();
        }};
    </script>
</body>
</html>"""


# =============================================================================
# CUSTOM WIDGETS
# =============================================================================

class CustomTitleBar(QFrame):
    """Custom title bar with window controls and app info."""
    
    # Signals
    minimizeClicked = Signal()
    maximizeClicked = Signal()
    closeClicked = Signal()
    mousePressed = Signal(QMouseEvent)
    mouseMoved = Signal(QMouseEvent)
    mouseReleased = Signal(QMouseEvent)
    doubleClicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.drag_pos = None
        self.is_maximized = False
        self.setup_ui()
        
    def setup_ui(self):
        self.setFixedHeight(TITLE_BAR_HEIGHT)
        self.setObjectName("titleBar")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(10)
        
        # App icon
        self.icon_label = QLabel("📖")
        self.icon_label.setFixedSize(24, 24)
        self.icon_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.icon_label)
        
        # App title
        self.title_label = QLabel(APP_NAME)
        self.title_label.setObjectName("titleLabel")
        layout.addWidget(self.title_label)
        
        # Spacer
        layout.addStretch()
        
        # Filename label
        self.filename_label = QLabel("No file open")
        self.filename_label.setObjectName("filenameLabel")
        layout.addWidget(self.filename_label)
        
        # Spacer
        layout.addStretch()
        
        # Window controls
        self.btn_minimize = QPushButton("−")
        self.btn_minimize.setObjectName("windowControl")
        self.btn_minimize.setFixedSize(40, 30)
        self.btn_minimize.setToolTip("Minimize")
        self.btn_minimize.clicked.connect(self.minimizeClicked.emit)
        layout.addWidget(self.btn_minimize)
        
        self.btn_maximize = QPushButton("□")
        self.btn_maximize.setObjectName("windowControl")
        self.btn_maximize.setFixedSize(40, 30)
        self.btn_maximize.setToolTip("Maximize")
        self.btn_maximize.clicked.connect(self.maximizeClicked.emit)
        layout.addWidget(self.btn_maximize)
        
        self.btn_close = QPushButton("×")
        self.btn_close.setObjectName("windowControlClose")
        self.btn_close.setFixedSize(40, 30)
        self.btn_close.setToolTip("Close")
        self.btn_close.clicked.connect(self.closeClicked.emit)
        layout.addWidget(self.btn_close)
        
    def set_filename(self, filename: str):
        """Update the filename display."""
        self.filename_label.setText(filename)
        
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()
            self.mousePressed.emit(event)
            
    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and self.drag_pos:
            self.mouseMoved.emit(event)
            
    def mouseReleaseEvent(self, event: QMouseEvent):
        self.drag_pos = None
        self.mouseReleased.emit(event)
        
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        self.doubleClicked.emit()


class StatusBar(QFrame):
    """Custom status bar with time and document info."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.start_timer()
        
    def setup_ui(self):
        self.setFixedHeight(STATUS_BAR_HEIGHT)
        self.setObjectName("statusBar")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(20)
        
        # Left side - document info
        self.info_label = QLabel("Ready")
        self.info_label.setObjectName("statusInfo")
        layout.addWidget(self.info_label)
        
        layout.addStretch()
        
        # Right side - time
        self.time_label = QLabel("00:00")
        self.time_label.setObjectName("statusTime")
        layout.addWidget(self.time_label)
        
    def start_timer(self):
        """Start the clock timer."""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every second
        self.update_time()
        
    def update_time(self):
        """Update the time display."""
        current_time = datetime.now().strftime("%H:%M")
        self.time_label.setText(current_time)
        
    def set_info(self, text: str):
        """Update the info text."""
        self.info_label.setText(text)


class BrightnessOverlay(QWidget):
    """Semi-transparent overlay for brightness control."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setStyleSheet("background-color: black;")
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0.0)
        self.hide()
        
    def set_brightness(self, value: int):
        """Set brightness level (0-100, where 0 is darkest)."""
        # Invert: higher value = brighter = less opacity
        opacity = (100 - value) / 100.0 * 0.9  # Max 90% dark
        self.opacity_effect.setOpacity(opacity)
        if value < 100:
            self.show()
            self.raise_()
        else:
            self.hide()


class SearchBar(QFrame):
    """Search bar widget for find functionality."""
    
    searchRequested = Signal(str)
    closeRequested = Signal()
    nextRequested = Signal()
    prevRequested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.hide()
        
    def setup_ui(self):
        self.setObjectName("searchBar")
        self.setFixedHeight(50)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 5, 15, 5)
        layout.setSpacing(10)
        
        # Search icon
        search_icon = QLabel("🔍")
        layout.addWidget(search_icon)
        
        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Find in document...")
        self.search_input.setObjectName("searchInput")
        self.search_input.returnPressed.connect(self.on_search)
        self.search_input.textChanged.connect(self.on_search)
        layout.addWidget(self.search_input)
        
        # Navigation buttons
        self.btn_prev = QPushButton("▲")
        self.btn_prev.setFixedSize(30, 30)
        self.btn_prev.setToolTip("Previous")
        self.btn_prev.clicked.connect(self.prevRequested.emit)
        layout.addWidget(self.btn_prev)
        
        self.btn_next = QPushButton("▼")
        self.btn_next.setFixedSize(30, 30)
        self.btn_next.setToolTip("Next")
        self.btn_next.clicked.connect(self.nextRequested.emit)
        layout.addWidget(self.btn_next)
        
        # Close button
        self.btn_close = QPushButton("×")
        self.btn_close.setFixedSize(30, 30)
        self.btn_close.setToolTip("Close (Esc)")
        self.btn_close.clicked.connect(self.close_requested)
        layout.addWidget(self.btn_close)
        
    def on_search(self):
        """Emit search signal with current text."""
        self.searchRequested.emit(self.search_input.text())
        
    def close_requested(self):
        """Close the search bar."""
        self.search_input.clear()
        self.hide()
        self.closeRequested.emit()
        
    def show_search(self):
        """Show and focus the search bar."""
        self.show()
        self.search_input.setFocus()
        self.search_input.selectAll()


class TOCSidebar(QFrame):
    """Table of Contents sidebar."""
    
    headingClicked = Signal(str)  # Emits heading ID
    bookmarkClicked = Signal(int)  # Emits page number for PDF bookmarks
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.headings = []
        self.bookmarks = []
        self.is_pdf_mode = False
        self.current_file_path = None
        self.setup_ui()
        
    def setup_ui(self):
        self.setObjectName("tocSidebar")
        self.setFixedWidth(SIDEBAR_WIDTH)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setObjectName("tocHeader")
        header.setFixedHeight(50)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 0, 15, 0)
        
        self.title_label = QLabel("📑 Table of Contents")
        self.title_label.setObjectName("tocTitle")
        header_layout.addWidget(self.title_label)
        
        layout.addWidget(header)
        
        # Scroll area for headings - use QFrame with background color
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setObjectName("tocScroll")
        self.scroll.setFrameShape(QFrame.NoFrame)
        
        self.content_widget = QFrame()
        self.content_widget.setObjectName("tocContentWidget")
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(8, 10, 8, 10)
        self.content_layout.setSpacing(0)
        self.content_layout.addStretch()
        
        self.scroll.setWidget(self.content_widget)
        layout.addWidget(self.scroll)
        
    def set_headings(self, headings: List[Dict]):
        """Set the headings list (for Markdown)."""
        self.headings = headings
        self.bookmarks = []
        self.is_pdf_mode = False
        self.title_label.setText("📑 Table of Contents")
        self.refresh_headings()
        
    def set_bookmarks(self, bookmarks: List[Dict], file_path: str = None):
        """Set the bookmarks list (for PDF)."""
        self.bookmarks = bookmarks
        self.headings = []
        self.is_pdf_mode = True
        self.current_file_path = file_path
        self.title_label.setText("📑 Bookmarks")
        self.refresh_bookmarks()
        
    def refresh_headings(self):
        """Refresh the TOC display for Markdown headings."""
        # Clear existing items (except stretch)
        while self.content_layout.count() > 1:
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Add heading items as simple labels with indentation
        for heading in self.headings:
            item_widget = self._create_heading_item(heading)
            self.content_layout.insertWidget(self.content_layout.count() - 1, item_widget)
            
    def refresh_bookmarks(self):
        """Refresh the TOC display for PDF bookmarks."""
        # Clear existing items (except stretch)
        while self.content_layout.count() > 1:
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Add bookmark items recursively
        for bookmark in self.bookmarks:
            item_widget = self._create_bookmark_item(bookmark)
            self.content_layout.insertWidget(self.content_layout.count() - 1, item_widget)
            
    def _create_heading_item(self, heading: Dict) -> QWidget:
        """Create a simple heading item widget."""
        item = QLabel(heading['text'])
        item.setObjectName(f"tocItem")
        
        # Calculate indentation based on heading level
        indent = (heading['level'] - 1) * 12
        font_size = 13 - (heading['level'] - 1) * 1  # Smaller font for deeper levels
        opacity = 1.0 - (heading['level'] - 1) * 0.15  # Slightly more transparent for deeper levels
        
        item.setStyleSheet(f"""
            QLabel {{
                padding: 6px 8px 6px {8 + indent}px;
                font-size: {max(font_size, 11)}px;
                border: none;
                background: transparent;
                border-radius: 4px;
            }}
            QLabel:hover {{
                background-color: rgba(255, 255, 255, 0.1);
            }}
        """)
        item.setCursor(QCursor(Qt.PointingHandCursor))
        item.setToolTip(heading['text'])
        
        # Make clickable
        def on_click(event, hid=heading['id']):
            self.headingClicked.emit(hid)
        
        item.mousePressEvent = on_click
        return item
        
    def _create_bookmark_item(self, bookmark: Dict, level: int = 0) -> QWidget:
        """Create a bookmark item widget for PDF."""
        container = QFrame()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # Main bookmark label
        item = QLabel(bookmark['title'])
        item.setObjectName("tocItem")
        
        indent = level * 12
        font_size = max(13 - level, 11)
        
        item.setStyleSheet(f"""
            QLabel {{
                padding: 5px 8px 5px {8 + indent}px;
                font-size: {font_size}px;
                border: none;
                background: transparent;
                border-radius: 4px;
            }}
            QLabel:hover {{
                background-color: rgba(255, 255, 255, 0.1);
            }}
        """)
        item.setCursor(QCursor(Qt.PointingHandCursor))
        item.setToolTip(bookmark['title'])
        
        # Make clickable
        def on_click(event, page=bookmark.get('page', 1)):
            self.bookmarkClicked.emit(page)
        
        item.mousePressEvent = on_click
        container_layout.addWidget(item)
        
        # Add children recursively
        if 'children' in bookmark and bookmark['children']:
            for child in bookmark['children']:
                child_widget = self._create_bookmark_item(child, level + 1)
                container_layout.addWidget(child_widget)
        
        return container
            
    def clear(self):
        """Clear all headings and bookmarks."""
        self.headings = []
        self.bookmarks = []
        self.is_pdf_mode = False
        self.title_label.setText("📑 Table of Contents")
        self.refresh_headings()


# =============================================================================
# MAIN WINDOW
# =============================================================================

class LuminaReader(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        
        # Window state
        self.current_file: Optional[str] = None
        self.current_file_type: Optional[str] = None  # 'md' or 'pdf'
        self.current_theme = "dark"
        self.current_font = "sans-serif"
        self.zoom_level = 1.0
        self.brightness_value = 100
        self.is_maximized = False
        self.drag_position = None
        
        # Multi-file support
        self.open_files: List[Dict] = []  # List of {path, type, title}
        self.current_file_index: int = -1
        
        # Setup
        self.setup_window()
        self.setup_ui()
        self.setup_styles()
        self.setup_connections()
        self.setup_drag_drop()
        
        # Load initial content
        self.show_welcome_screen()
        
    def setup_window(self):
        """Configure window properties."""
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.resize(1200, 800)
        
        # Frameless window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Enable high DPI scaling
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
        
    def setup_ui(self):
        """Create and layout UI components."""
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Title bar
        self.title_bar = CustomTitleBar(self)
        self.main_layout.addWidget(self.title_bar)
        
        # Toolbar (integrated menu bar, like VS Code)
        self.setup_toolbar()
        self.main_layout.addWidget(self.toolbar)
        
        # Tab bar for multi-file support
        self.setup_tab_bar()
        self.main_layout.addWidget(self.tab_bar)
        
        # Content area (sidebar + viewer)
        self.content_area = QWidget()
        content_layout = QHBoxLayout(self.content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # TOC Sidebar
        self.toc_sidebar = TOCSidebar(self)
        self.toc_sidebar.headingClicked.connect(self.on_toc_heading_clicked)
        self.toc_sidebar.bookmarkClicked.connect(self.on_pdf_bookmark_clicked)
        content_layout.addWidget(self.toc_sidebar)
        
        # Viewer stack
        self.viewer_stack = QStackedWidget()
        
        # Web view for Markdown
        self.web_view = QWebEngineView()
        self.web_view.settings().setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True
        )
        self.web_view.settings().setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True
        )
        self.web_view.settings().setAttribute(
            QWebEngineSettings.WebAttribute.JavascriptEnabled, True
        )
        self.web_view.settings().setAttribute(
            QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True
        )
        self.viewer_stack.addWidget(self.web_view)
        
        # PDF view
        self.pdf_view = QWebEngineView()
        self.pdf_view.settings().setAttribute(
            QWebEngineSettings.WebAttribute.JavascriptEnabled, True
        )
        self.pdf_view.loadFinished.connect(self.on_pdf_load_finished)
        self.viewer_stack.addWidget(self.pdf_view)
        
        content_layout.addWidget(self.viewer_stack)
        
        self.main_layout.addWidget(self.content_area)
        
        # Search bar
        self.search_bar = SearchBar(self)
        self.search_bar.searchRequested.connect(self.on_search)
        self.search_bar.closeRequested.connect(self.on_search_close)
        self.main_layout.addWidget(self.search_bar)
        
        # Status bar
        self.status_bar = StatusBar(self)
        self.main_layout.addWidget(self.status_bar)
        
        # Brightness overlay (on top of everything)
        self.brightness_overlay = BrightnessOverlay(self.central_widget)
        
    def setup_tab_bar(self):
        """Setup tab bar for multi-file support."""
        self.tab_bar = QFrame()
        self.tab_bar.setObjectName("tabBar")
        self.tab_bar.setFixedHeight(32)
        self.tab_bar.hide()  # Hide when no files open
        
        self.tab_layout = QHBoxLayout(self.tab_bar)
        self.tab_layout.setContentsMargins(8, 4, 8, 4)
        self.tab_layout.setSpacing(6)
        self.tab_layout.addStretch()
        
    def setup_toolbar(self):
        """Setup integrated toolbar bar with controls (like VS Code menu bar)."""
        self.toolbar = QFrame()
        self.toolbar.setObjectName("appToolbar")
        self.toolbar.setFixedHeight(40)
        
        toolbar_layout = QHBoxLayout(self.toolbar)
        toolbar_layout.setContentsMargins(12, 4, 12, 4)
        toolbar_layout.setSpacing(6)
        
        # Open button
        btn_open = QPushButton("📂  Open")
        btn_open.setObjectName("toolbarBtn")
        btn_open.setToolTip("Open file (Ctrl+O)")
        btn_open.setMinimumWidth(80)
        btn_open.setMinimumHeight(30)
        btn_open.clicked.connect(self.open_file_dialog)
        toolbar_layout.addWidget(btn_open)
        
        # Export button (for Markdown to PDF)
        self.btn_export = QPushButton("📤  Export PDF")
        self.btn_export.setObjectName("toolbarBtn")
        self.btn_export.setToolTip("Export Markdown to PDF")
        self.btn_export.setMinimumWidth(100)
        self.btn_export.setMinimumHeight(30)
        self.btn_export.clicked.connect(self.export_markdown_to_pdf)
        self.btn_export.setEnabled(False)  # Disabled by default, enabled for Markdown
        toolbar_layout.addWidget(self.btn_export)
        
        # Separator
        sep1 = QFrame()
        sep1.setObjectName("toolbarSeparator")
        sep1.setFixedWidth(1)
        sep1.setFixedHeight(22)
        toolbar_layout.addWidget(sep1)
        
        # Theme toggle
        self.btn_theme = QPushButton("🌙  Theme")
        self.btn_theme.setObjectName("toolbarBtn")
        self.btn_theme.setToolTip("Toggle theme (Ctrl+T)")
        self.btn_theme.setMinimumWidth(90)
        self.btn_theme.setMinimumHeight(30)
        self.btn_theme.clicked.connect(self.toggle_theme)
        toolbar_layout.addWidget(self.btn_theme)
        
        # Font toggle
        self.btn_font = QPushButton("Aa  Font")
        self.btn_font.setObjectName("toolbarBtn")
        self.btn_font.setToolTip("Toggle font style")
        self.btn_font.setMinimumWidth(80)
        self.btn_font.setMinimumHeight(30)
        self.btn_font.clicked.connect(self.toggle_font)
        toolbar_layout.addWidget(self.btn_font)
        
        # Separator
        sep2 = QFrame()
        sep2.setObjectName("toolbarSeparator")
        sep2.setFixedWidth(1)
        sep2.setFixedHeight(22)
        toolbar_layout.addWidget(sep2)
        
        # Zoom controls
        btn_zoom_out = QPushButton("−")
        btn_zoom_out.setObjectName("toolbarBtn")
        btn_zoom_out.setToolTip("Zoom out (Ctrl+-)")
        btn_zoom_out.setFixedSize(32, 30)
        btn_zoom_out.clicked.connect(lambda: self.adjust_zoom(-0.1))
        toolbar_layout.addWidget(btn_zoom_out)
        
        self.zoom_label = QLabel("100%")
        self.zoom_label.setObjectName("zoomLabel")
        self.zoom_label.setFixedWidth(52)
        self.zoom_label.setAlignment(Qt.AlignCenter)
        toolbar_layout.addWidget(self.zoom_label)
        
        btn_zoom_in = QPushButton("+")
        btn_zoom_in.setObjectName("toolbarBtn")
        btn_zoom_in.setToolTip("Zoom in (Ctrl++)")
        btn_zoom_in.setFixedSize(32, 30)
        btn_zoom_in.clicked.connect(lambda: self.adjust_zoom(0.1))
        toolbar_layout.addWidget(btn_zoom_in)
        
        # Separator
        sep3 = QFrame()
        sep3.setObjectName("toolbarSeparator")
        sep3.setFixedWidth(1)
        sep3.setFixedHeight(22)
        toolbar_layout.addWidget(sep3)
        
        # Brightness control
        brightness_label = QLabel("🔆  Brightness")
        brightness_label.setObjectName("toolbarLabel")
        brightness_label.setMinimumWidth(95)
        toolbar_layout.addWidget(brightness_label)
        
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setObjectName("brightnessSlider")
        self.brightness_slider.setRange(20, 100)
        self.brightness_slider.setValue(100)
        self.brightness_slider.setFixedWidth(120)
        self.brightness_slider.valueChanged.connect(self.on_brightness_changed)
        toolbar_layout.addWidget(self.brightness_slider)
        
        toolbar_layout.addStretch()
        
    def setup_styles(self):
        """Apply styles based on current theme."""
        theme = THEMES[self.current_theme]
        
        self.setStyleSheet(f"""
            /* Main Window */
            QWidget {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            }}
            
            /* Central Widget */
            #centralWidget {{
                background-color: {theme['bg_primary']};
                border-radius: 8px;
            }}
            
            /* Title Bar */
            #titleBar {{
                background-color: {theme['bg_secondary']};
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border-bottom: 1px solid {theme['border']};
            }}
            
            #titleLabel {{
                color: {theme['text_primary']};
                font-size: 14px;
                font-weight: 600;
            }}
            
            #filenameLabel {{
                color: {theme['text_secondary']};
                font-size: 13px;
            }}
            
            #windowControl {{
                background: transparent;
                border: none;
                color: {theme['text_primary']};
                font-size: 16px;
                border-radius: 4px;
            }}
            
            #windowControl:hover {{
                background-color: {theme['button_hover']};
            }}
            
            #windowControlClose {{
                background: transparent;
                border: none;
                color: {theme['text_primary']};
                font-size: 18px;
                border-radius: 4px;
            }}
            
            #windowControlClose:hover {{
                background-color: {theme['error']};
                color: white;
            }}
            
            /* Status Bar */
            #statusBar {{
                background-color: {theme['bg_secondary']};
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
                border-top: 1px solid {theme['border']};
            }}
            
            #statusInfo, #statusTime {{
                color: {theme['text_secondary']};
                font-size: 12px;
            }}
            
            /* App Toolbar */
            #appToolbar {{
                background-color: {theme['bg_secondary']};
                border-bottom: 1px solid {theme['border']};
            }}
            
            #toolbarLabel {{
                color: {theme['text_secondary']};
                font-size: 13px;
            }}
            
            #toolbarBtn {{
                background-color: {theme['bg_tertiary']};
                border: 1px solid {theme['border']};
                color: {theme['text_primary']};
                padding: 5px 12px;
                border-radius: 6px;
                font-size: 13px;
            }}
            
            #toolbarBtn:hover {{
                background-color: {theme['button_hover']};
                border-color: {theme['accent']};
            }}
            
            #toolbarSeparator {{
                background-color: {theme['border']};
            }}
            
            #zoomLabel {{
                color: {theme['text_secondary']};
                font-size: 12px;
            }}
            
            #brightnessSlider::groove:horizontal {{
                height: 6px;
                background: {theme['bg_tertiary']};
                border-radius: 3px;
            }}
            
            #brightnessSlider::handle:horizontal {{
                width: 16px;
                height: 16px;
                margin: -5px 0;
                background: {theme['accent']};
                border-radius: 8px;
            }}
            
            #brightnessSlider::sub-page:horizontal {{
                background: {theme['accent']};
                border-radius: 3px;
            }}
            
            /* TOC Sidebar */
            #tocSidebar {{
                background-color: {theme['bg_secondary']};
                border-right: 1px solid {theme['border']};
            }}
            
            #tocHeader {{
                background-color: {theme['bg_tertiary']};
                border-bottom: 1px solid {theme['border']};
            }}
            
            #tocTitle {{
                color: {theme['text_primary']};
                font-size: 14px;
                font-weight: 600;
            }}
            
            #tocScroll {{
                background-color: {theme['bg_secondary']};
                border: none;
            }}
            
            #tocScroll > QWidget {{
                background-color: {theme['bg_secondary']};
            }}
            
            #tocContentWidget {{
                background-color: {theme['bg_secondary']};
            }}
            
            #tocItem {{
                color: {theme['text_secondary']};
                background: transparent;
            }}
            
            #tocItem:hover {{
                color: {theme['text_primary']};
            }}
            
            /* Tab bar styles */
            #tabBar {{
                background-color: {theme['bg_secondary']};
                border-bottom: 1px solid {theme['border']};
            }}
            
            #tabItem {{
                background-color: {theme['bg_tertiary']};
                border: 1px solid {theme['border']};
                border-radius: 4px;
                color: {theme['text_secondary']};
                padding: 4px 12px;
                font-size: 12px;
            }}
            
            #tabItem:hover {{
                background-color: {theme['button_hover']};
                color: {theme['text_primary']};
            }}
            
            #tabItemActive {{
                background-color: {theme['accent']};
                border: 1px solid {theme['accent']};
                border-radius: 4px;
                color: white;
                padding: 4px 12px;
                font-size: 12px;
            }}
            
            #tabCloseBtn {{
                background: transparent;
                border: none;
                color: {theme['text_secondary']};
                font-size: 14px;
                padding: 0;
                margin-left: 8px;
            }}
            
            #tabCloseBtn:hover {{
                color: {theme['error']};
            }}
            
            /* Disabled button style */
            QPushButton:disabled {{
                background-color: {theme['bg_tertiary']};
                color: {theme['text_secondary']};
                border-color: {theme['border']};
            }}
            
            /* Search Bar */
            #searchBar {{
                background-color: {theme['bg_secondary']};
                border-top: 1px solid {theme['border']};
            }}
            
            #searchInput {{
                background-color: {theme['bg_tertiary']};
                border: 1px solid {theme['border']};
                color: {theme['text_primary']};
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 13px;
            }}
            
            #searchInput:focus {{
                border-color: {theme['accent']};
            }}
            
            /* Scrollbars */
            QScrollArea {{
                border: none;
            }}
            
            QScrollBar:vertical {{
                background: {theme['bg_primary']};
                width: 10px;
            }}
            
            QScrollBar::handle:vertical {{
                background: {theme['bg_tertiary']};
                border-radius: 5px;
                min-height: 30px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background: {theme['border']};
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0;
            }}
        """)
        
    def setup_connections(self):
        """Connect signals and slots."""
        # Title bar
        self.title_bar.minimizeClicked.connect(self.showMinimized)
        self.title_bar.maximizeClicked.connect(self.toggle_maximize)
        self.title_bar.closeClicked.connect(self.close)
        self.title_bar.mousePressed.connect(self.on_title_bar_mouse_press)
        self.title_bar.mouseMoved.connect(self.on_title_bar_mouse_move)
        self.title_bar.doubleClicked.connect(self.toggle_maximize)
        
    def setup_drag_drop(self):
        """Enable drag and drop functionality."""
        self.setAcceptDrops(True)
        
    def resizeEvent(self, event):
        """Handle window resize."""
        super().resizeEvent(event)
        # Resize overlay
        self.brightness_overlay.setGeometry(self.central_widget.rect())
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            
    def dropEvent(self, event: QDropEvent):
        """Handle file drop."""
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.lower().endswith(('.md', '.markdown', '.pdf')):
                self.load_file(file_path)
            else:
                QMessageBox.warning(self, "Invalid File", 
                    "Please drop a Markdown (.md) or PDF (.pdf) file.")
                
    def keyPressEvent(self, event: QKeyEvent):
        """Handle keyboard shortcuts."""
        if event.modifiers() == Qt.ControlModifier:
            if event.key() == Qt.Key_O:
                self.open_file_dialog()
            elif event.key() == Qt.Key_F:
                self.search_bar.show_search()
            elif event.key() == Qt.Key_T:
                self.toggle_theme()
            elif event.key() == Qt.Key_Plus or event.key() == Qt.Key_Equal:
                self.adjust_zoom(0.1)
            elif event.key() == Qt.Key_Minus:
                self.adjust_zoom(-0.1)
            elif event.key() == Qt.Key_0:
                self.reset_zoom()
        elif event.key() == Qt.Key_Escape:
            self.search_bar.close_requested()
            
        super().keyPressEvent(event)
        
    def wheelEvent(self, event):
        """Handle mouse wheel for zoom."""
        if event.modifiers() == Qt.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.adjust_zoom(0.1)
            else:
                self.adjust_zoom(-0.1)
            event.accept()
        else:
            super().wheelEvent(event)
            
    # =====================================================================
    # WINDOW CONTROL
    # =====================================================================
    
    def on_title_bar_mouse_press(self, event: QMouseEvent):
        """Start window drag."""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            
    def on_title_bar_mouse_move(self, event: QMouseEvent):
        """Handle window drag."""
        if event.buttons() == Qt.LeftButton and self.drag_position:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            
    def toggle_maximize(self):
        """Toggle window maximize state."""
        if self.is_maximized:
            self.showNormal()
            self.is_maximized = False
            self.title_bar.btn_maximize.setText("□")
        else:
            self.showMaximized()
            self.is_maximized = True
            self.title_bar.btn_maximize.setText("❐")
            
    # =====================================================================
    # FILE OPERATIONS
    # =====================================================================
    
    def open_file_dialog(self):
        """Open file dialog to select a document."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Document",
            "",
            "Documents (*.md *.markdown *.pdf);;Markdown (*.md *.markdown);;PDF (*.pdf);;All Files (*.*)"
        )
        if file_path:
            self.load_file(file_path)
            
    def load_file(self, file_path: str, add_to_tabs: bool = True):
        """Load and display a file."""
        try:
            if not os.path.exists(file_path):
                QMessageBox.critical(self, "Error", f"File not found:\n{file_path}")
                return
            
            # Check if file is already open
            for i, file_info in enumerate(self.open_files):
                if file_info['path'] == file_path:
                    self.switch_to_tab(i)
                    return
            
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext in ['.md', '.markdown']:
                self.load_markdown(file_path, add_to_tabs)
            elif file_ext == '.pdf':
                self.load_pdf(file_path, add_to_tabs)
            else:
                QMessageBox.warning(self, "Unsupported File", 
                    f"File type '{file_ext}' is not supported.")
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file:\n{str(e)}")
            
    def load_markdown(self, file_path: str, add_to_tabs: bool = True):
        """Load and render a Markdown file."""
        self.current_file_type = 'md'
        self.current_file = file_path
        
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Update UI
        filename = os.path.basename(file_path)
        self.title_bar.set_filename(filename)
        
        # Enable font button for Markdown
        self.btn_font.setEnabled(True)
        
        # Enable export button for Markdown
        self.btn_export.setEnabled(True)
        
        # Generate HTML
        html = get_base_html(self.current_theme, self.current_font)
        self.web_view.setHtml(html, QUrl.fromLocalFile(file_path))
        
        # Wait for page to load then inject content
        self.web_view.loadFinished.connect(lambda: self.inject_markdown_content(content))
        
        # Show web view
        self.viewer_stack.setCurrentIndex(0)
        
        # Update status
        word_count = count_words_in_markdown(content)
        self.status_bar.set_info(f"{word_count} words")
        
        # Generate TOC after a short delay
        QTimer.singleShot(500, self.update_toc)
        
        # Add to tabs
        if add_to_tabs:
            self.add_file_to_tabs(file_path, 'md', filename)
        
    def inject_markdown_content(self, content: str):
        """Inject markdown content into the web view."""
        # Escape special characters for JavaScript
        escaped = content.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
        
        js_code = f"""
            if (window.renderMarkdown) {{
                window.renderMarkdown(`{escaped}`);
            }}
        """
        self.web_view.page().runJavaScript(js_code)
        
    def load_pdf(self, file_path: str, add_to_tabs: bool = True):
        """Load and render a PDF file."""
        self.current_file_type = 'pdf'
        self.current_file = file_path
        
        # Update UI
        filename = os.path.basename(file_path)
        self.title_bar.set_filename(filename)
        
        # Disable font button for PDF
        self.btn_font.setEnabled(False)
        
        # Disable export button for PDF
        self.btn_export.setEnabled(False)
        
        # Read PDF as base64
        import base64
        with open(file_path, 'rb') as f:
            pdf_data = base64.b64encode(f.read()).decode('utf-8')
        
        # Extract bookmarks/outline from PDF
        self.extract_pdf_bookmarks(file_path)
        
        # Generate HTML
        html = get_pdf_viewer_html(self.current_theme)
        self.pdf_view.setHtml(html)
        
        # Store PDF data for injection after load
        self._pending_pdf_data = pdf_data
        
        # Show PDF view
        self.viewer_stack.setCurrentIndex(1)
        
        # Update status (will be updated when PDF loads)
        self.status_bar.set_info("Loading PDF...")
        
        # Add to tabs
        if add_to_tabs:
            self.add_file_to_tabs(file_path, 'pdf', filename)
            
    def extract_pdf_bookmarks(self, file_path: str):
        """Extract bookmarks/outline from PDF using PyMuPDF."""
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(file_path)
            
            bookmarks = []
            toc = doc.get_toc()
            
            # Convert flat TOC to hierarchical structure
            bookmark_stack = []
            for item in toc:
                level, title, page = item
                bookmark = {'title': title, 'page': page, 'level': level}
                
                if level == 1:
                    bookmarks.append(bookmark)
                    bookmark_stack = [bookmark]
                else:
                    # Find parent
                    while len(bookmark_stack) >= level:
                        bookmark_stack.pop()
                    if bookmark_stack:
                        parent = bookmark_stack[-1]
                        if 'children' not in parent:
                            parent['children'] = []
                        parent['children'].append(bookmark)
                        bookmark_stack.append(bookmark)
                    else:
                        bookmarks.append(bookmark)
                        bookmark_stack = [bookmark]
            
            if bookmarks:
                self.toc_sidebar.set_bookmarks(bookmarks, file_path)
            else:
                # If no bookmarks, try to generate from page count
                page_count = doc.page_count
                if page_count > 0:
                    simple_bookmarks = [{'title': f'Page {i+1}', 'page': i+1} for i in range(min(page_count, 50))]
                    self.toc_sidebar.set_bookmarks(simple_bookmarks, file_path)
                else:
                    self.toc_sidebar.clear()
            
            doc.close()
        except Exception as e:
            print(f"Error extracting PDF bookmarks: {e}")
            self.toc_sidebar.clear()
        
    def inject_pdf_content(self, pdf_data: str):
        """Inject PDF content into the PDF viewer."""
        js_code = f"""
            if (window.loadPDF) {{
                window.loadPDF('{pdf_data}');
            }}
        """
        self.pdf_view.page().runJavaScript(js_code)
        
    def on_pdf_load_finished(self, ok):
        """Handle PDF viewer page load finished."""
        if ok and hasattr(self, '_pending_pdf_data'):
            self.inject_pdf_content(self._pending_pdf_data)
            delattr(self, '_pending_pdf_data')
            
            # Auto-fit to window width after a short delay
            QTimer.singleShot(800, self.fit_pdf_to_window)
            
    def fit_pdf_to_window(self):
        """Fit PDF to window width."""
        if self.current_file_type == 'pdf':
            # Calculate scale to fit window width
            # PDF standard is 72 DPI, typical page is 612 points (8.5 inches)
            viewer_width = self.pdf_view.width() - 60  # Account for padding/margins
            pdf_page_width = 612  # Standard letter size in points
            scale = viewer_width / pdf_page_width
            scale = max(0.5, min(2.0, scale))  # Clamp between 0.5 and 2.0
            
            self.zoom_level = scale / 2.0  # Adjust for our base scale of 2.0
            self.apply_zoom()
            
    def on_pdf_bookmark_clicked(self, page_num: int):
        """Handle PDF bookmark click - scroll to page."""
        if self.current_file_type == 'pdf':
            js_code = f"window.scrollToPage({page_num});"
            self.pdf_view.page().runJavaScript(js_code)
        
    def export_markdown_to_pdf(self):
        """Export current Markdown file to PDF."""
        if self.current_file_type != 'md' or not self.current_file:
            QMessageBox.warning(self, "Export Error", "Please open a Markdown file first.")
            return
        
        # Get output file path
        default_name = Path(self.current_file).stem + ".pdf"
        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export to PDF",
            default_name,
            "PDF files (*.pdf)"
        )
        
        if not output_path:
            return
        
        try:
            # Read markdown content
            with open(self.current_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Use markdown + weasyprint or reportlab for conversion
            try:
                import markdown
                from weasyprint import HTML, CSS
                
                # Convert markdown to HTML
                html_content = markdown.markdown(md_content, extensions=['extra', 'codehilite'])
                
                # Add styling
                full_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <style>
                        body {{ font-family: Georgia, serif; line-height: 1.6; margin: 40px; }}
                        h1, h2, h3, h4, h5, h6 {{ color: #333; }}
                        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
                        pre {{ background: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
                        blockquote {{ border-left: 3px solid #ccc; margin-left: 0; padding-left: 20px; color: #666; }}
                        table {{ border-collapse: collapse; width: 100%; }}
                        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                        th {{ background-color: #f2f2f2; }}
                    </style>
                </head>
                <body>
                    {html_content}
                </body>
                </html>
                """
                
                # Convert to PDF
                HTML(string=full_html).write_pdf(output_path)
                
                QMessageBox.information(self, "Export Complete", f"PDF exported successfully to:\n{output_path}")
                
            except ImportError:
                # Fallback using Qt's PDF generation
                self.export_using_qt(output_path, md_content)
                
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export PDF:\n{str(e)}")
            
    def export_using_qt(self, output_path: str, md_content: str):
        """Fallback PDF export using Qt."""
        try:
            import markdown
            
            # Convert markdown to HTML
            html_content = markdown.markdown(md_content, extensions=['extra'])
            
            full_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Georgia, serif; line-height: 1.6; margin: 40px; font-size: 12pt; }}
                    h1 {{ font-size: 18pt; }}
                    h2 {{ font-size: 16pt; }}
                    h3 {{ font-size: 14pt; }}
                </style>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """
            
            # Create a temporary web view for printing
            from PySide6.QtWebEngineWidgets import QWebEngineView
            from PySide6.QtCore import QUrl
            
            temp_view = QWebEngineView()
            temp_view.setHtml(full_html)
            
            # Wait for load and print to PDF
            def do_print():
                from PySide6.QtGui import QPageLayout, QPageSize
                
                page_layout = QPageLayout(
                    QPageSize(QPageSize.A4),
                    QPageLayout.Portrait,
                    QMarginsF(20, 20, 20, 20)
                )
                
                temp_view.page().printToPdf(output_path, page_layout)
                QMessageBox.information(self, "Export Complete", f"PDF exported successfully to:\n{output_path}")
            
            temp_view.loadFinished.connect(do_print)
            
        except ImportError:
            QMessageBox.warning(self, "Export Error", 
                "PDF export requires additional packages.\nPlease install: pip install markdown weasyprint")

    def show_welcome_screen(self):
        """Display welcome screen when no file is open."""
        welcome_md = """# Welcome to LuminaReader

A modern, lightweight Markdown & PDF viewer with scientific focus.

## Features

- 📖 **Markdown Support** - Render markdown with syntax highlighting
- 📄 **PDF Viewer** - View PDF documents with smooth scrolling
- 🔢 **Math Support** - LaTeX equations via MathJax
- 🎨 **Themes** - Dark and Light modes
- 🔆 **Brightness Control** - Adjust app brightness independently
- 🔍 **Search** - Find text in documents (Ctrl+F)
- 📑 **Table of Contents** - Auto-generated from headers

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + O` | Open file |
| `Ctrl + F` | Find in document |
| `Ctrl + T` | Toggle theme |
| `Ctrl + +` | Zoom in |
| `Ctrl + -` | Zoom out |
| `Ctrl + 0` | Reset zoom |
| `Ctrl + Wheel` | Zoom in/out |

## Math Example

Inline math: $E = mc^2$

Block math:
$$
\\\\sum_{i=1}^{n} x_i = x_1 + x_2 + \\cdots + x_n
$$

---

**Drag and drop** a file here or press **Ctrl+O** to open.
"""
        
        self.current_file = None
        self.current_file_type = None
        
        html = get_base_html(self.current_theme, self.current_font)
        self.web_view.setHtml(html)
        self.web_view.loadFinished.connect(lambda: self.inject_markdown_content(welcome_md))
        
        self.viewer_stack.setCurrentIndex(0)
        self.toc_sidebar.clear()
        self.title_bar.set_filename("Welcome")
        self.status_bar.set_info("Ready")
        
        # Reset button states
        self.btn_font.setEnabled(True)
        self.btn_export.setEnabled(False)
        
    # =====================================================================
    # UI CONTROLS
    # =====================================================================
    
    def toggle_theme(self):
        """Toggle between dark and light themes."""
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.btn_theme.setText("☀️  Theme" if self.current_theme == "light" else "🌙  Theme")
        self.setup_styles()
        
        # Reload current file with new theme
        if self.current_file:
            self.load_file(self.current_file)
        else:
            self.show_welcome_screen()
            
    def toggle_font(self):
        """Toggle between serif and sans-serif fonts."""
        # Only works for Markdown
        if self.current_file_type != 'md':
            return
            
        self.current_font = "serif" if self.current_font == "sans-serif" else "sans-serif"
        
        # Update font in web view
        js_code = f"window.setFont('{self.current_font}');"
        self.web_view.page().runJavaScript(js_code)
        
    def adjust_zoom(self, delta: float):
        """Adjust zoom level."""
        self.zoom_level = max(0.5, min(3.0, self.zoom_level + delta))
        self.apply_zoom()
        
    def reset_zoom(self):
        """Reset zoom to 100%."""
        self.zoom_level = 1.0
        self.apply_zoom()
        
    def apply_zoom(self):
        """Apply current zoom level."""
        zoom_percent = int(self.zoom_level * 100)
        self.zoom_label.setText(f"{zoom_percent}%")
        
        if self.current_file_type == 'md':
            js_code = f"window.zoom({self.zoom_level});"
            self.web_view.page().runJavaScript(js_code)
        elif self.current_file_type == 'pdf':
            js_code = f"window.setZoom({self.zoom_level * 2.0});"
            self.pdf_view.page().runJavaScript(js_code)
            
    def on_brightness_changed(self, value: int):
        """Handle brightness slider change."""
        self.brightness_value = value
        self.brightness_overlay.set_brightness(value)
        
    # =====================================================================
    # SEARCH
    # =====================================================================
    
    def on_search(self, query: str):
        """Handle search request."""
        if self.current_file_type == 'md':
            js_code = f"window.findText('{query}');"
            self.web_view.page().runJavaScript(js_code, self.on_search_result)
            
    def on_search_result(self, result):
        """Handle search result."""
        if isinstance(result, int) and result > 0:
            self.status_bar.set_info(f"Found {result} matches")
        else:
            self.status_bar.set_info("No matches found")
            
    def on_search_close(self):
        """Handle search bar close."""
        # Clear highlights
        if self.current_file_type == 'md':
            js_code = "window.findText('');"
            self.web_view.page().runJavaScript(js_code)
            
    # =====================================================================
    # TABLE OF CONTENTS
    # =====================================================================
    
    def update_toc(self):
        """Update table of contents from current document."""
        if self.current_file_type == 'md':
            js_code = "window.getHeadings();"
            self.web_view.page().runJavaScript(js_code, self.on_toc_received)
            
    def on_toc_received(self, result):
        """Handle TOC data from JavaScript."""
        try:
            if result:
                headings = json.loads(result)
                self.toc_sidebar.set_headings(headings)
        except json.JSONDecodeError:
            pass
            
    def on_toc_heading_clicked(self, heading_id: str):
        """Scroll to clicked heading."""
        js_code = f"window.scrollToHeading('{heading_id}');"
        self.web_view.page().runJavaScript(js_code)
        
    # =====================================================================
    # MULTI-FILE TAB MANAGEMENT
    # =====================================================================
    
    def add_file_to_tabs(self, file_path: str, file_type: str, title: str):
        """Add a file to the tab bar."""
        # Check if already in tabs
        for i, file_info in enumerate(self.open_files):
            if file_info['path'] == file_path:
                self.current_file_index = i
                self.update_tab_bar()
                return
        
        # Add new file
        self.open_files.append({
            'path': file_path,
            'type': file_type,
            'title': title
        })
        self.current_file_index = len(self.open_files) - 1
        self.update_tab_bar()
        
    def update_tab_bar(self):
        """Update the tab bar display."""
        # Clear existing tabs (except stretch)
        while self.tab_layout.count() > 1:
            item = self.tab_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if len(self.open_files) == 0:
            self.tab_bar.hide()
            return
        
        self.tab_bar.show()
        
        # Add tabs
        for i, file_info in enumerate(self.open_files):
            tab = self.create_tab_widget(file_info, i == self.current_file_index)
            self.tab_layout.insertWidget(i, tab)
            
    def create_tab_widget(self, file_info: Dict, is_active: bool) -> QFrame:
        """Create a tab widget for a file."""
        tab = QFrame()
        tab.setObjectName("tabItemActive" if is_active else "tabItem")
        tab.setCursor(QCursor(Qt.PointingHandCursor))
        
        layout = QHBoxLayout(tab)
        layout.setContentsMargins(8, 2, 4, 2)
        layout.setSpacing(4)
        
        # File type icon
        icon = "📝" if file_info['type'] == 'md' else "📄"
        icon_label = QLabel(icon)
        layout.addWidget(icon_label)
        
        # File name (truncated)
        name_label = QLabel(file_info['title'])
        name_label.setStyleSheet("background: transparent; border: none;")
        layout.addWidget(name_label)
        
        # Close button
        close_btn = QPushButton("×")
        close_btn.setObjectName("tabCloseBtn")
        close_btn.setFixedSize(16, 16)
        close_btn.setToolTip("Close tab")
        close_btn.clicked.connect(lambda checked, path=file_info['path']: self.close_tab(path))
        layout.addWidget(close_btn)
        
        # Click to switch
        def on_tab_click(event):
            self.switch_to_file(file_info['path'])
        
        tab.mousePressEvent = on_tab_click
        name_label.mousePressEvent = on_tab_click
        icon_label.mousePressEvent = on_tab_click
        
        return tab
        
    def switch_to_file(self, file_path: str):
        """Switch to a file by path."""
        for i, file_info in enumerate(self.open_files):
            if file_info['path'] == file_path:
                self.switch_to_tab(i)
                return
                
    def switch_to_tab(self, index: int):
        """Switch to a tab by index."""
        if 0 <= index < len(self.open_files):
            self.current_file_index = index
            file_info = self.open_files[index]
            
            # Load without adding to tabs (already there)
            self.current_file = file_info['path']
            self.current_file_type = file_info['type']
            
            if file_info['type'] == 'md':
                self.load_markdown(file_info['path'], add_to_tabs=False)
            else:
                self.load_pdf(file_info['path'], add_to_tabs=False)
                
            self.update_tab_bar()
            
    def close_tab(self, file_path: str):
        """Close a tab by file path."""
        for i, file_info in enumerate(self.open_files):
            if file_info['path'] == file_path:
                self.open_files.pop(i)
                
                # Adjust current index
                if self.current_file_index >= len(self.open_files):
                    self.current_file_index = len(self.open_files) - 1
                
                # Switch to another file or show welcome
                if self.current_file_index >= 0:
                    self.switch_to_tab(self.current_file_index)
                else:
                    self.current_file = None
                    self.current_file_type = None
                    self.show_welcome_screen()
                    self.tab_bar.hide()
                
                self.update_tab_bar()
                break


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """Application entry point."""
    # Enable high DPI support
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    
    # Set application font
    font = QFont("Inter", 10)
    app.setFont(font)
    
    # Create and show main window
    window = LuminaReader()
    window.show()
    
    # Handle file argument
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        window.load_file(sys.argv[1])
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
