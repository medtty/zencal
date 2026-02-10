# **ZenCal** — Minimal Fullscreen Calendar

```
⬡ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ⬡
     ____           ____      _
    |_  /___ _ _   / ___|__ _| |
     / // -_) ' \ | |   / _` | |
    /___\___|_||_| \___|\__,_|_|

    Distraction-Free Event Reminders
⬡ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ⬡
```

A minimal, distraction-free full-screen event reminder system with ORION-OS inspired theming. Takes over your screen when it's time for important events, then gets out of your way.

[![License: MIT](https://img.shields.io/badge/License-MIT-cyan.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)]()

---

## ✨ **Features**

### 🖥️ **Fullscreen Event Display**
- Automatically takes over your entire screen when an event starts
- Large, centered text with countdown timer
- Clean, minimal interface with no distractions
- Auto-exits when event duration expires

### 📅 **Smart Event Management**
- Visual calendar grid showing all events
- Repeating events (daily, weekdays, weekly, monthly)
- Duration-based reminders (stays on screen for exact time)
- Quick-add today button for last-minute events

### 🎨 **ORION-OS Theme**
- Cyberpunk-inspired dark UI with cyan accents
- Fully customizable colors and fonts
- Monospace typography for clean aesthetics
- Easy theme editing via single config file

### 🔄 **Cross-Platform Sync**
- Export/import events as JSON files
- Sync via cloud storage (Dropbox, Syncthing, etc.)
- Portable config file works on any device
- No account or internet connection required

### 🖼️ **System Tray Integration**
- Runs silently in background
- Close window → minimizes to tray (doesn't quit)
- Right-click tray icon for quick access
- Custom icon support

### ⚡ **Performance**
- Lightweight (no external databases)
- Minimal resource usage
- Fast startup and event checking
- Zero dependencies for basic usage

---

## 📸 **Screenshots**

### Main Overlay (Idle)
```
┌─────────────────────────────────────────┐
│                                         │
│        ▶ Next: Team Meeting            │
│              at 14:30                   │
│                                         │
│  [⚙ MANAGER] [FULLSCREEN] [QUIT]      │
└─────────────────────────────────────────┘
```

### Fullscreen Event
```
╔═══════════════════════════════════════════╗
║                                           ║
║                                           ║
║              TEAM MEETING                 ║
║                                           ║
║        Discuss Q1 roadmap                 ║
║          45m 23s remaining                ║
║                                           ║
║                                           ║
╚═══════════════════════════════════════════╝
```

### Event Manager
```
┌─────────────────────────────────────────────────────────┐
│  ⬡ ZENCAL  •  EVENT MANAGER                            │
├──────────────┬──────────────────────────────────────────┤
│  CALENDAR    │  ▶ EVENTS                               │
│              │                                          │
│    FEB 2026  │  [+ADD] [✎EDIT] [🗑DELETE] [⚙SETTINGS] │
│  Mo Tu We Th │  [⬇IMPORT] [⬆EXPORT]                    │
│              │                                          │
│   1  2  3  4 │  Title       Date        Time  Duration │
│   5  6  7  8 │  ───────────────────────────────────────│
│  ●1 10 11 12 │  Meeting     2026-02-10  14:30  60m    │
│  13 14 15 16 │  Gym         2026-02-11  07:00  90m    │
│              │  Dinner      2026-02-12  19:00  60m    │
└──────────────┴──────────────────────────────────────────┘
```

---

## 🚀 **Quick Start**

### **Installation**

**Option 1: Run from source (recommended for development)**
```bash
# Clone the repository
git clone https://github.com/yourusername/zencal.git
cd zencal

# No dependencies needed! Python 3.8+ with Tkinter is enough

# Optional: For system tray support
pip install pystray pillow
```

**Option 2: Download pre-built executables**
- Download from [Releases](https://github.com/yourusername/zencal/releases)
- No Python installation required
- Includes system tray support

### **Usage**

```bash
# Launch overlay (default)
python zencal.py

# Launch manager
python zencal.py --manager

# Overlay with verbose logging
python zencal.py --verbose

# Clear logs and start
python zencal.py --clear-log
```

---

## 📖 **Detailed Usage**

### **Adding Events**

1. **Via Manager GUI:**
   ```bash
   python manager.py
   ```
   - Click **"+ ADD"** button
   - Fill in event details
   - Click **"SAVE"**

2. **Quick Add Today:**
   - Open overlay → Click **"⚙ MANAGER"**
   - Click **"+ QUICK ADD TODAY"**
   - Date is pre-filled with today

3. **Manually edit JSON:**
   ```json
   {
     "title": "Meeting",
     "date": "2026-02-10",
     "time": "14:30",
     "duration_minutes": 60,
     "repeat": "none",
     "note": "Bring laptop"
   }
   ```

### **Event Properties**

| Field | Format | Example | Description |
|-------|--------|---------|-------------|
| `title` | String | `"Team Standup"` | Event name (shown in fullscreen) |
| `date` | YYYY-MM-DD | `"2026-02-10"` | Event date |
| `time` | HH:MM | `"09:30"` | Start time (24-hour format) |
| `duration_minutes` | Integer | `30` | How long to show fullscreen |
| `repeat` | String | `"daily"` | Recurrence pattern |
| `note` | String | `"Room 302"` | Optional note (shown below title) |

**Repeat Options:**
- `none` — One-time event
- `daily` — Every day from start date
- `weekdays` — Monday-Friday only
- `weekly` — Same day each week
- `monthly` — Same date each month

### **Keyboard Shortcuts (Overlay)**

| Key | Action |
|-----|--------|
| `ESC` | Minimize to tray / Exit fullscreen |
| `F11` | Toggle fullscreen |
| `Q` | Quit (with confirmation) |

### **System Tray**

**Right-click tray icon:**
- **Show ZenCal** — Restore overlay window
- **Open Manager** — Launch event manager
- **Quit** — Exit application

---

## 🎨 **Customization**

### **Change Colors**

Edit `ui/theme.py`:

```python
THEME = {
    "accent": "#00d9ff",      # Cyan accent (change to any hex color)
    "bg_dark": "#0a0a0f",     # Main background
    "bg_mid": "#1a1a24",      # Panel background
    "text": "#e2e8f0",        # Text color
    # ... more options
}
```

**Popular themes:**
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

### **Change Fonts**

Edit `ui/theme.py`:

```python
FONTS = {
    "primary": "JetBrains Mono",  # Change to "Consolas", "Fira Code", etc.
    "fallback": "Courier",
}
```

### **Adjust Settings**

Manager → **⚙ SETTINGS** button:
- **Check Interval** — How often to check for events (seconds)
- **Title Font Size** — Fullscreen text size
- **Text Color** — Fullscreen text color (hex)
- **Background Color** — Fullscreen background (hex)

Or edit `calendar.json` directly:
```json
{
  "settings": {
    "check_interval_seconds": 5,
    "font_size": 72,
    "font_color": "#00d9ff",
    "bg_color": "#0a0a0f",
    "subtitle_font_size": 28
  }
}
```

---

## 🔄 **Syncing Between Devices**

### **Method 1: Export/Import**

**Device A:**
```bash
python manager.py
# Click "⬆ EXPORT"
# Save as: zencal_export_20260210.json
```

**Device B:**
```bash
python manager.py
# Click "⬇ IMPORT"
# Select: zencal_export_20260210.json
# Choose "Merge" or "Replace"
```

### **Method 2: Cloud Sync**

**Option A: Direct file sync**
```bash
# Put calendar.json in synced folder
ln -s ~/Dropbox/zencal/calendar.json ~/zencal/calendar.json
```

**Option B: Syncthing (recommended)**
1. Install [Syncthing](https://syncthing.net/)
2. Share `zencal/` folder between devices
3. Both overlays read from same `calendar.json`

**Option C: Git**
```bash
git init
git add calendar.json
git commit -m "Update events"
git push
```

---

## 🔨 **Building Executables**

### **Windows**

```bash
# Install dependencies
pip install pyinstaller pystray pillow

# Build
python build_windows.py

# Output: dist/ZenCal.exe
```

### **Linux**

```bash
# Install dependencies
pip install pyinstaller pystray pillow

# Build
chmod +x build_linux.sh
./build_linux.sh

# Output: dist/ZenCal
```

### **Custom Icon**

Place `zencal.png` in project root before building. The script will automatically:
- Convert PNG to ICO (Windows)
- Embed icon in executable
- Use for system tray

**Icon requirements:**
- Format: PNG
- Size: 256x256 or larger
- Transparent background recommended

---

## 📁 **Project Structure**

```
zencal/
├── zencal.py              # Overlay launcher
├── manager.py             # Manager launcher
├── zencal.png             # App icon (place yours here)
├── calendar.json          # Your events (auto-generated)
├── zencal.log             # Debug log (auto-generated)
│
├── core/                  # Core logic
│   ├── __init__.py
│   ├── config.py          # Config loading/saving
│   ├── events.py          # Event matching logic
│   └── logger.py          # Logging system
│
├── ui/                    # User interface
│   ├── __init__.py
│   ├── theme.py           # Colors & fonts (CUSTOMIZE HERE!)
│   ├── overlay.py         # Fullscreen overlay
│   ├── manager_window.py  # Manager main window
│   ├── calendar_view.py   # Calendar grid component
│   └── dialogs.py         # Event/Settings dialogs
│
├── build_windows.py       # Windows build script
├── build_linux.sh         # Linux build script
└── README.md              # This file
```

---

## 🐛 **Troubleshooting**

### **Fullscreen not triggering?**

1. **Check event is configured correctly:**
   ```bash
   python zencal.py --verbose
   ```
   You'll see logs showing when events are checked.

2. **Verify time format:**
   - Date: `YYYY-MM-DD` (e.g., `2026-02-10`)
   - Time: `HH:MM` in 24-hour format (e.g., `14:30` not `2:30 PM`)

3. **Check duration hasn't expired:**
   - Event shows from `time` to `time + duration_minutes`

### **Manager button not working?**

- **Windows:** Ensure `python` is in your PATH
- **Linux:** Make sure `manager.py` is executable: `chmod +x manager.py`

### **System tray not showing?**

Install dependencies:
```bash
pip install pystray pillow
```

If still not working, app will minimize normally instead.

### **Events not syncing?**

- Both devices must have same `calendar.json` file
- Check file permissions (must be readable/writable)
- Manager auto-reloads config, but overlay checks every 5 seconds

### **Fonts look wrong?**

Install JetBrains Mono:
```bash
# Ubuntu/Debian
sudo apt install fonts-jetbrains-mono

# Arch
sudo pacman -S ttf-jetbrains-mono

# Windows
# Download from: https://www.jetbrains.com/lp/mono/
```

Or change font in `ui/theme.py`:
```python
FONTS = {
    "primary": "Consolas",  # Use system font
}
```

### **High CPU usage?**

Increase check interval in settings (default: 5 seconds):
```json
{
  "settings": {
    "check_interval_seconds": 30
  }
}
```

---

## 🔧 **Advanced Usage**

### **Run on Startup**

**Windows:**
1. Press `Win + R`
2. Type `shell:startup` and press Enter
3. Create shortcut to `ZenCal.exe` or `zencal.py`

**Linux (systemd):**
```bash
# Create service file
nano ~/.config/systemd/user/zencal.service
```

```ini
[Unit]
Description=ZenCal Event Reminder

[Service]
ExecStart=/usr/bin/python3 /path/to/zencal/zencal.py
Restart=always

[Install]
WantedBy=default.target
```

```bash
# Enable and start
systemctl --user enable zencal.service
systemctl --user start zencal.service
```

### **Verbose Logging**

```bash
# See detailed logs in terminal
python zencal.py --verbose

# Or check log file
tail -f zencal.log
```

### **Multiple Profiles**

```bash
# Use different config files
export ZENCAL_CONFIG=~/work-events.json
python zencal.py

export ZENCAL_CONFIG=~/personal-events.json
python zencal.py
```

*(Note: Requires modifying `core/config.py` to check environment variable)*

---

## 🤝 **Contributing**

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Development setup:**
```bash
git clone https://github.com/yourusername/zencal.git
cd zencal
# No build step needed - edit and run directly
python zencal.py --verbose
```

---

## 📝 **Changelog**

### **v1.0.0** (2026-02-10)
- ✨ Initial release
- 🖥️ Fullscreen event overlay
- 📅 Calendar view with event indicators
- 🔄 Import/export functionality
- 🎨 ORION-OS theme
- 🖼️ System tray integration
- 🔨 Windows/Linux executable builds

---

## 📄 **License**

MIT License - see [LICENSE](LICENSE) file for details.

**TL;DR:** Use it however you want, commercially or personally, with no restrictions. Attribution appreciated but not required.

---

## 🙏 **Credits**

- **Design Inspiration:** ORION-OS aesthetic
- **Font:** [JetBrains Mono](https://www.jetbrains.com/lp/mono/)
- **Icons:** Custom designed
- **Built with:** Python, Tkinter, ❤️

---

## 💬 **Support**

- 🐛 **Bug reports:** [Open an issue](https://github.com/yourusername/zencal/issues)
- 💡 **Feature requests:** [Start a discussion](https://github.com/yourusername/zencal/discussions)
- 📧 **Email:** your.email@example.com

---

## 🌟 **Star History**

If you find ZenCal useful, consider giving it a star! ⭐

---

<div align="center">

**Made with ⬡ by [Your Name]**

[Website](https://yourwebsite.com) • [Twitter](https://twitter.com/yourusername) • [GitHub](https://github.com/yourusername)

</div>

---

## 🎯 **Philosophy**

ZenCal is built on these principles:

1. **Minimal by default** — No bloat, no unnecessary features
2. **Distraction-free** — Takes over your screen when needed, then disappears
3. **Local-first** — Your data stays on your device
4. **Cross-platform** — Works the same on Windows and Linux
5. **Hackable** — Easy to customize and extend

---

**⬡ Built for people who value their time and attention ⬡**
