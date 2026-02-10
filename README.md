# ZenCal : Minimal Fullscreen Calendar Reminders

```
⬡ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ⬡
     ____           ____      _
    |_  /___ _ _   / ___|__ _| |
     / // -_) ' \ | |   / _` | |
    /___\___|_||_| \___|\__,_|_|

    Distraction-Free Event Reminders
⬡ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ⬡
```

[![License: MIT](https://img.shields.io/badge/License-MIT-00d9ff.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)]()
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**A minimal, distraction-free full-screen event reminder that you can't ignore.**

[Download Latest Release](https://github.com/medtty/zencal/releases/latest) • [Report Bug](https://github.com/medtty/zencal/issues) • [Request Feature](https://github.com/medtty/zencal/discussions)

</div>

---

## 🎯 What is ZenCal?

ZenCal is a **minimal, distraction-free full-screen event reminder** that takes over your entire screen when it's time for important events. No more missing meetings because you ignored a tiny notification popup.

### The Problem
Traditional calendar apps show small notification popups that are easy to ignore or dismiss. You glance at them, think "I'll remember" then you forget.

### The Solution
ZenCal **takes over your entire screen** with large, impossible-to-ignore text when an event starts. It stays on screen for the exact duration you specify, then disappears. Simple. Effective. Impossible to miss.

---

## ✨ Key Features

- 🖥️ **Fullscreen Takeover** : Impossible to ignore when events start
- ⏱️ **Live Countdown** : Real-time timer showing remaining duration  
- 📅 **Visual Calendar** : Month grid with event indicators
- 🔄 **Repeating Events** : Daily, weekdays, weekly, monthly patterns
- 💾 **Export/Import** : Sync events between devices via JSON
- 🖼️ **System Tray** : Runs silently in background
- ⚡ **Lightweight** : No bloat, minimal resource usage
- 🔓 **Open Source** : MIT License, fully hackable

---

## 🚀 Installation

### Windows

**Installer (Recommended)**
1. Download `ZenCal-Setup-1.0.0.exe` from [Releases](https://github.com/medtty/zencal/releases/latest)
2. Run the installer
3. Find **ZenCal** and **ZenCal Manager** in Start Menu
4. Done! ✨

### Linux

**Option 1: Install Script**
```bash
# Download release
git clone https://github.com/medtty/zencal.git
cd zencal

# Install system-wide
sudo ./install_linux.sh

# Or user-only
./install_linux.sh

# Launch
zencal              # Overlay
zencal --manager    # Manager
```

**Option 2: Run from Source**
```bash
git clone https://github.com/medtty/zencal.git
cd zencal
python zencal.py
```

---

## 📖 Quick Start Guide

### 1. Launch ZenCal

**Windows:**
- Start Menu → ZenCal

**Linux:**
```bash
zencal
```

A small window appears showing "No events scheduled"

### 2. Add Your First Event

Click the **"⚙ MANAGER"** button in the overlay (or run `zencal --manager`)

In the manager:
1. Click **"+ ADD"**
2. Fill in:
   - **Title**: "Team Meeting"
   - **Date**: 2026-02-15
   - **Time**: 14:30 (2:30 PM)
   - **Duration**: 60 minutes
   - **Repeat**: none
   - **Note**: "Bring laptop"
3. Click **"SAVE"**

### 3. Test It

When the event time arrives:
- Your screen goes **fullscreen** automatically
- Large text shows: **TEAM MEETING**
- Live countdown: **60m 0s remaining**
- After 60 minutes, it exits fullscreen automatically

---

## 🎨 Usage Examples

### Daily Standup (Repeating)
```json
{
  "title": "Daily Standup",
  "date": "2026-02-10",
  "time": "09:00",
  "duration_minutes": 15,
  "repeat": "weekdays",
  "note": "Zoom link: zoom.us/j/123"
}
```

### Gym Session (Weekly)
```json
{
  "title": "Gym",
  "date": "2026-02-10",
  "time": "18:00",
  "duration_minutes": 90,
  "repeat": "weekly",
  "note": "Leg day"
}
```

### One-Time Event
```json
{
  "title": "Doctor Appointment",
  "date": "2026-02-20",
  "time": "14:30",
  "duration_minutes": 30,
  "repeat": "none",
  "note": "Room 302"
}
```

---

## 🎨 Customization

### Change Theme Colors

Edit `ui/theme.py`:
```python
THEME = {
    "accent": "#00d9ff",      # Cyan (default)
    "bg_dark": "#0a0a0f",     # Dark background
    "text": "#e2e8f0",        # Light text
}
```

**Popular Themes:**
```python
# Dracula
"accent": "#bd93f9", "bg_dark": "#282a36"

# Nord
"accent": "#88c0d0", "bg_dark": "#2e3440"

# Gruvbox
"accent": "#83a598", "bg_dark": "#282828"

# Tokyo Night
"accent": "#7aa2f7", "bg_dark": "#1a1b26"
```

### Change Fonts

Edit `ui/theme.py`:
```python
FONTS = {
    "primary": "Consolas",     # Or any monospace font
    "fallback": "Courier",
}
```

### Settings

Manager → **⚙ SETTINGS**

Or edit `calendar.json`:
```json
{
  "settings": {
    "check_interval_seconds": 5,
    "font_size": 72,
    "font_color": "#00d9ff",
    "bg_color": "#0a0a0f"
  }
}
```

---

## 🔄 Sync Between Devices

### Method 1: Export/Import

**Device A:**
1. Manager → **⬆ EXPORT**
2. Save as `zencal_backup.json`

**Device B:**
1. Manager → **⬇ IMPORT**
2. Choose file
3. Select "Merge" or "Replace"

### Method 2: Cloud Sync (Recommended)

**Using Dropbox/Google Drive:**
```bash
# Move calendar.json to synced folder
mv calendar.json ~/Dropbox/zencal/calendar.json

# Create symlink
ln -s ~/Dropbox/zencal/calendar.json ./calendar.json
```

Both devices now share the same events automatically!

---

## ⌨️ Command Line Reference
```bash
# Overlay mode (default)
zencal                      # Run overlay
zencal --verbose            # Show logs
zencal --clear-log          # Clear log file

# Manager mode
zencal --manager            # Open event manager

# Help
zencal --help               # Show all options
```

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `ESC` | Exit fullscreen / Minimize to tray |
| `F11` | Toggle fullscreen |
| `Q` | Quit (with confirmation) |

---

## 🐛 Troubleshooting

### Fullscreen Not Working?

1. **Check event format:**
   - Date: `YYYY-MM-DD` (e.g., `2026-02-15`)
   - Time: `HH:MM` in 24-hour format (e.g., `14:30` not `2:30 PM`)

2. **Run with logs:**
```bash
   zencal --verbose
```

3. **Verify event exists:**
```bash
   zencal --manager
```

### System Tray Missing?

Install dependencies:
```bash
pip install pystray pillow
```

### Manager Button Not Responding?

**Windows:** Ensure Python is in PATH:
```bash
python --version
```

**Linux:** Make script executable:
```bash
chmod +x zencal.py
```

### High CPU Usage?

Increase check interval:
```json
{"settings": {"check_interval_seconds": 30}}
```

---

## 📁 Project Structure
```
zencal/
├── zencal.py              # Main entry point
├── zencal.ico             # Application icon
├── zencal.png             # Icon (PNG format)
├── calendar.json          # Your events (auto-generated)
├── zencal.log             # Debug log (auto-generated)
│
├── core/                  # Core functionality
│   ├── config.py          # Config loading/saving
│   ├── events.py          # Event matching logic
│   └── logger.py          # Logging system
│
├── ui/                    # User interface
│   ├── theme.py           # Colors & fonts ← CUSTOMIZE HERE
│   ├── overlay.py         # Fullscreen overlay
│   ├── manager_window.py  # Event manager
│   ├── calendar_view.py   # Calendar grid
│   └── dialogs.py         # Dialogs
│
├── build_windows.py       # Windows build script
├── build_linux.sh         # Linux build script
├── installer_windows.iss  # Inno Setup script
└── README.md
```

---

## 🔨 Building from Source

### Requirements
```bash
pip install pyinstaller pystray pillow
```

### Build Executable

**Windows:**
```batch
python build_windows.py
# Output: dist/ZenCal.exe
```

**Linux:**
```bash
chmod +x build_linux.sh
./build_linux.sh
# Output: dist/ZenCal
```

### Create Installer

**Windows:**
1. Install [Inno Setup](https://jrsoftware.org/isdl.php)
2. Run: `build_installer.bat`
3. Output: `installer_output/ZenCal-Setup-1.0.0.exe`

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push: `git push origin feature/amazing-feature`
5. Open Pull Request

---

## 📄 License

MIT License : see [LICENSE](LICENSE) for details.

**TL;DR:** Use it however you want, commercially or personally. No restrictions. Attribution appreciated but not required.

---

## 🙏 Acknowledgments

- **Font:** [JetBrains Mono](https://www.jetbrains.com/lp/mono/)
- **Built with:** Python + Tkinter + ❤️

---

## 📧 Support

- 🐛 [Report Bugs](https://github.com/medtty/zencal/issues)
- 💡 [Request Features](https://github.com/medtty/zencal/discussions)
- ⭐ [Star on GitHub](https://github.com/medtty/zencal)

---


**⬡ Built for people who value their time and attention ⬡**

Made with ⬡ by [MEDY](https://github.com/medtty)
