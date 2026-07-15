<div align="center">

# 🌸 Bloom Sub

### Smart, Thread-Safe & Multi-Encoding Subtitle Converter

Repair, convert, and batch-process subtitle encodings with a modern, high-performance desktop application.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-green?style=for-the-badge&logo=qt)
![Platform](https://img.shields.io/badge/Platform-Windows-blue?style=for-the-badge&logo=windows)
![Executable](https://img.shields.io/badge/Executable-.EXE-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

</div>

---

# 📖 Overview

**Bloom Sub** is a sleek, reliable desktop utility designed to permanently fix unreadable or corrupted Persian, Arabic, and international subtitle files.

Subtitles often display strange characters such as:

```text
Ø§Ù„Ø¹Ø±Ø¨ÙŠØ©
ÈÇÑÇä
Ø³Ù„Ø§Ù…
```

These issues are caused by encoding mismatches between legacy subtitle files and modern media players.

Bloom Sub combines a **hybrid automatic encoding detection engine** with **asynchronous multi-threaded processing** to quickly convert individual subtitle files or entire media libraries into clean, universal encodings such as **UTF-8**.

Unlike many online converters, **Bloom Sub works completely offline**, never uploads your files, and **never overwrites your original subtitles**, ensuring maximum privacy and safety.

---

# ✨ Key Features

| Feature | Technical Implementation | Benefits |
| :--- | :--- | :--- |
| **🔍 Intelligent Auto Detection** | Dual-Layer Detection (Heuristic + Chardet Fallback) | Detects legacy subtitle encodings with high accuracy. |
| **⚡ Multi-Threaded Processing** | QThread Background Worker | Smooth UI with no freezing during large conversions. |
| **📂 Batch & Recursive Conversion** | Recursive scanning using `os.walk()` | Convert thousands of subtitle files in one operation. |
| **🛡 Safe Conversion** | Automatic timestamped output folders | Original subtitle files always remain untouched. |
| **📁 Smart Folder Structure** | Preserves original directory hierarchy | Converted subtitles stay organized exactly like the source. |
| **✨ Path Cleansing** | Removes hidden Unicode direction characters (`\u202A`, `\u202B`, etc.) | Fixes drag-and-drop path issues on Windows. |
| **♻️ Encoding Fallback System** | Multiple decoding attempts on failure | Successfully opens problematic subtitle files without corruption. |
| **📝 Automatic File Naming** | Prevents duplicate filenames (`_1`, `_2`, ...) | Eliminates accidental overwrites automatically. |

---

# ⚙️ How It Works

Bloom Sub follows a secure processing pipeline to maximize compatibility while preventing data loss.

```text
        Input Subtitle(s)
               │
               ▼
     Path Cleansing (RTL/LTR Fix)
               │
               ▼
      🔍 Hybrid Encoding Detection
      ├── Fast Heuristic Matching
      └── Chardet Statistical Analysis
               │
               ▼
      Background QThread Processing
               │
      ┌────────┴────────┐
      ▼                 ▼
Read Subtitle      Create Timestamped
   Content          Output Directory
      │                 │
      └────────┬────────┘
               ▼
     Encoding Conversion Engine
               │
               ▼
     Smart File Name Generator
      (Avoid Duplicate Files)
               │
               ▼
     ✅ Verified Converted Subtitle
```

---

# 📊 Supported Encodings

## 📥 Input Encodings

| Display Name | Python Codec | Description |
| --- | --- | --- |
| Automatic Detection | Hybrid Detection Engine | Automatically detects subtitle encoding |
| UTF-8 with BOM | `utf-8-sig` | Windows-compatible UTF-8 |
| UTF-8 | `utf-8` | Universal modern encoding |
| UTF-16 LE | `utf-16-le` | Windows Unicode format |
| UTF-16 BE | `utf-16-be` | Big Endian Unicode |
| Windows-1256 | `windows-1256` | Persian & Arabic legacy subtitles |

---

## 📤 Output Encodings

- UTF-8
- UTF-8 with BOM
- UTF-16 LE
- UTF-16 BE
- Windows-1256

---

# 📄 Supported Subtitle Formats

Bloom Sub supports:

- SRT
- ASS
- SSA
- SUB
- TXT
- VTT

---

# 🎨 Modern Desktop Interface

Bloom Sub features a modern desktop experience built with **PyQt5**.

### Interface Highlights

- Clean and minimal layout
- Responsive desktop UI
- Compact design
- Live progress bar
- Real-time conversion status
- Smart ComboBoxes
- Automatic output folder generation
- Drag-and-drop support
- Localized RTL dialogs for Persian users

---

# 🚀 Installation

## Requirements

- Python 3.8 or newer

---

## Run From Source

### Clone Repository

```bash
git clone https://github.com/Data-Blooom/Bloom-Sub.git
cd Bloom-Sub
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Launch

```bash
python main.py
```

---

## Windows Executable

> 💡 **No Python installed? No problem!**

Bloom Sub is also available as a standalone **Windows (.exe)** application.

Simply download the latest release and run it instantly—no installation or configuration required.

---

# 🌟 Highlights

- ⚡ Fully asynchronous processing
- 🧠 Intelligent dual-layer encoding detection
- 🔒 100% offline operation
- 📁 Original files remain untouched
- 📂 Automatic timestamped output folders
- 🚀 Fast batch conversion
- 🛡 Reliable subtitle preservation
- 🎬 Designed for large subtitle collections

---

# 📸 Screenshots

<div align="center">

| Bloom Sub Main Interface |
| :---: |
| <img src="https://github.com/Data-Blooom/Bloom-Sub/raw/main/Screenshot/bloom%20sub.png" width="700" alt="Bloom Sub Main Interface"> |

</div>

---

# ❤️ About

Bloom Sub was created by **Data Bloom** to make subtitle encoding conversion simple, safe, and reliable.

No more unreadable subtitles or broken characters—just drag, convert, and enjoy your movies.

---

<div align="center">

### 🌸 Made with ❤️ by Data Bloom

</div>