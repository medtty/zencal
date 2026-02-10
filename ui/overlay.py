import subprocess
import sys
import tkinter as tk
from datetime import datetime, timedelta
from pathlib import Path

from core.config import get_config_path, load_config
from core.events import get_active_events, get_next_event
from core.logger import get_log_path, log_message
from ui.theme import FONTS, THEME


class ZenCalOverlay:
    """Main fullscreen overlay window."""

    def __init__(self, verbose=False):
        self.root = tk.Tk()
        self.root.title("ZenCal")
        self.config = load_config()
        self.settings = self.config.get("settings", {})
        self.is_fullscreen = False
        self.verbose = verbose
        self.current_active_event = None
        self.manager_process = None
        self.tray_icon = None

        # Theme
        self.bg_color = self.settings.get("bg_color", THEME["bg_dark"])
        self.accent_color = self.settings.get("font_color", THEME["accent"])
        self.dim_color = THEME["text_darker"]

        # Window setup
        self.root.configure(bg=self.bg_color)
        self.root.attributes("-topmost", True)
        self.root.geometry("700x180+100+100")

        # Set icon if available
        ico_path = Path(__file__).parent.parent / "zencal.ico"
        png_path = Path(__file__).parent.parent / "zencal.png"

        if ico_path.exists():
            try:
                self.root.iconbitmap(str(ico_path))
            except Exception as e:
                print(f"Could not load .ico: {e}")
                if png_path.exists():
                    try:
                        self.root.iconphoto(True, tk.PhotoImage(file=str(png_path)))
                    except:
                        pass
        elif png_path.exists():
            try:
                self.root.iconphoto(True, tk.PhotoImage(file=str(png_path)))
            except:
                pass

        # Setup system tray
        self.setup_system_tray()

        # Handle window close -> minimize to tray
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)

        # UI
        self.setup_ui()

        # Log startup (minimal)
        self.log("🚀 ZenCal started")
        self.log(f"📅 Loaded {len(self.config.get('events', []))} events")
        if not self.verbose:
            print(f"💡 Tip: Run with --verbose flag to see detailed logs in terminal")

        # Start timers
        self.check_events()
        self.update_countdown()

    def setup_system_tray(self):
        """Setup system tray icon."""
        try:
            import pystray
            from PIL import Image

            # Try to load .ico first, then .png, then create default
            ico_path = Path(__file__).parent.parent / "zencal.ico"
            png_path = Path(__file__).parent.parent / "zencal.png"

            if ico_path.exists():
                try:
                    icon_image = Image.open(ico_path)
                    self.log(f"✓ Loaded tray icon: {ico_path.name}")
                except Exception as e:
                    self.log(f"⚠️  Could not load .ico: {e}, trying .png")
                    if png_path.exists():
                        icon_image = Image.open(png_path)
                    else:
                        icon_image = self.create_default_icon()
            elif png_path.exists():
                try:
                    icon_image = Image.open(png_path)
                    self.log(f"✓ Loaded tray icon: {png_path.name}")
                except:
                    icon_image = self.create_default_icon()
            else:
                icon_image = self.create_default_icon()
                self.log("⚠️  No icon file found, using default")

            def on_show(icon, item):
                self.root.deiconify()
                self.root.lift()

            def on_quit(icon, item):
                icon.stop()
                self.quit_app()

            menu = pystray.Menu(
                pystray.MenuItem("Show ZenCal", on_show, default=True),
                pystray.MenuItem("Open Manager", lambda: self.open_manager()),
                pystray.MenuItem("Quit", on_quit),
            )

            self.tray_icon = pystray.Icon("zencal", icon_image, "ZenCal", menu)

            # Run in background thread
            import threading

            threading.Thread(target=self.tray_icon.run, daemon=True).start()

            self.has_tray = True
            self.log("✓ System tray enabled")

        except ImportError:
            self.has_tray = False
            print(
                "ℹ️  System tray disabled (install 'pystray' and 'pillow' for tray support)"
            )

    def create_default_icon(self):
        """Create a simple default icon."""
        from PIL import Image, ImageDraw

        width = 64
        height = 64
        image = Image.new("RGB", (width, height), THEME["bg_dark"])
        dc = ImageDraw.Draw(image)

        # Draw a simple calendar icon
        dc.rectangle([10, 10, 54, 54], outline=THEME["accent"], width=3)
        dc.rectangle([10, 10, 54, 20], fill=THEME["accent"])
        dc.text((20, 28), "Z", fill=THEME["accent"])

        return image

    def minimize_to_tray(self):
        """Minimize to system tray."""
        if self.has_tray:
            self.root.withdraw()
            # Optional: show notification
            try:
                self.tray_icon.notify("ZenCal is running in the background")
            except:
                pass
        else:
            # No tray support - just minimize
            self.root.iconify()

    def setup_ui(self):
        """Setup the overlay UI."""
        container = tk.Frame(self.root, bg=self.bg_color)
        container.pack(expand=True, fill="both")

        # Title
        self.title_label = tk.Label(
            container,
            text="ZenCal Active",
            font=(FONTS["primary"], 24, "bold"),
            fg=self.accent_color,
            bg=self.bg_color,
        )
        self.title_label.pack(expand=True, pady=(20, 5))

        # Subtitle
        self.sub_label = tk.Label(
            container,
            text="Monitoring events...",
            font=(FONTS["primary"], 14),
            fg=self.dim_color,
            bg=self.bg_color,
        )
        self.sub_label.pack(pady=(0, 5))

        # Button bar
        button_bar = tk.Frame(container, bg=self.bg_color)
        button_bar.pack(side="bottom", pady=(10, 15))

        btn_style = {
            "font": (FONTS["primary"], 9),
            "bg": THEME["bg_light"],
            "fg": THEME["text"],
            "activebackground": THEME["accent_dim"],
            "activeforeground": THEME["text"],
            "relief": "flat",
            "padx": 12,
            "pady": 6,
            "cursor": "hand2",
            "bd": 0,
        }

        # Manager button (highlighted)
        tk.Button(
            button_bar,
            text="⚙ MANAGER",
            command=self.open_manager,
            font=(FONTS["primary"], 9, "bold"),
            bg=THEME["accent"],
            fg=THEME["bg_dark"],
            activebackground=THEME["accent_dim"],
            activeforeground=THEME["bg_dark"],
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
            bd=0,
        ).pack(side="left", padx=5)

        tk.Button(
            button_bar, text="FULLSCREEN", command=self.toggle_fullscreen, **btn_style
        ).pack(side="left", padx=5)
        tk.Button(button_bar, text="QUIT", command=self.quit, **btn_style).pack(
            side="left", padx=5
        )

        # Hint
        self.hint_label = tk.Label(
            container,
            text="ESC: minimize  •  F11: fullscreen  •  Q: quit",
            font=(FONTS["primary"], 9),
            fg=THEME["border"],
            bg=self.bg_color,
        )
        self.hint_label.pack(side="bottom", pady=(0, 5))

        # Keybinds
        self.root.bind("<Escape>", lambda e: self.minimize())
        self.root.bind("<F11>", lambda e: self.toggle_fullscreen())
        self.root.bind("q", lambda e: self.quit())
        self.root.bind("Q", lambda e: self.quit())

    def open_manager(self):
        """Open the manager GUI."""
        # Check if manager is already running
        if self.manager_process and self.manager_process.poll() is None:
            self.log("⚠️  Manager already open")
            return

        try:
            # Get path to main script
            if getattr(sys, "frozen", False):
                # Running as compiled executable
                executable = sys.executable
                args = [executable, "--manager"]
            else:
                # Running as Python script
                script_path = Path(__file__).parent.parent / "zencal.py"
                args = [sys.executable, str(script_path), "--manager"]

            # Launch manager as separate process
            if sys.platform == "win32":
                self.manager_process = subprocess.Popen(
                    args, creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                self.manager_process = subprocess.Popen(args)

            self.log("✓ Manager opened")
        except Exception as e:
            self.log(f"❌ Failed to open manager: {e}")

    def log(self, msg):
        """Log message to file and optionally terminal."""
        log_message(msg)
        # Only print to terminal if verbose mode
        if self.verbose:
            print(msg)

    def go_fullscreen(self):
        """Enter fullscreen mode."""
        if not self.is_fullscreen:
            if sys.platform == "win32":
                self.root.state("zoomed")
                self.root.attributes("-fullscreen", True)
            else:
                self.root.attributes("-fullscreen", True)

            self.is_fullscreen = True
            self.title_label.config(
                font=(FONTS["primary"], self.settings.get("font_size", 72), "bold")
            )

    def exit_fullscreen(self):
        """Exit fullscreen mode."""
        if self.is_fullscreen:
            if sys.platform == "win32":
                self.root.attributes("-fullscreen", False)
                self.root.state("normal")
            else:
                self.root.attributes("-fullscreen", False)

            self.root.geometry("700x180+100+100")
            self.is_fullscreen = False
            self.title_label.config(font=(FONTS["primary"], 24, "bold"))

    def minimize(self):
        """Minimize or exit fullscreen."""
        if self.is_fullscreen:
            self.exit_fullscreen()
        else:
            self.minimize_to_tray()

    def toggle_fullscreen(self):
        """Toggle fullscreen."""
        if self.is_fullscreen:
            self.exit_fullscreen()
        else:
            self.go_fullscreen()

    def quit(self):
        """Show quit confirmation."""
        from tkinter import messagebox

        if messagebox.askyesno("Quit ZenCal", "Are you sure you want to quit ZenCal?"):
            self.quit_app()

    def quit_app(self):
        """Actually quit the application."""
        self.log("👋 Shutting down")
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.destroy()
        sys.exit(0)

    def update_countdown(self):
        """Update countdown every second."""
        if self.current_active_event:
            try:
                now = datetime.now()
                today = now.date()
                event = self.current_active_event

                event_time = datetime.strptime(event["time"], "%H:%M").time()
                event_end = datetime.combine(today, event_time) + timedelta(
                    minutes=event.get("duration_minutes", 30)
                )
                remaining = event_end - now

                if remaining.total_seconds() <= 0:
                    self.log(f"⏱️  Event ended: {event['title']}")
                    self.current_active_event = None
                    self.exit_fullscreen()
                else:
                    mins_left = max(0, int(remaining.total_seconds() // 60))
                    secs_left = max(0, int(remaining.total_seconds() % 60))

                    note = event.get("note", "")
                    sub_parts = []
                    if note:
                        sub_parts.append(note)
                    sub_parts.append(f"{mins_left}m {secs_left}s remaining")

                    self.sub_label.config(text="  •  ".join(sub_parts))
            except Exception as e:
                self.log(f"❌ Countdown error: {e}")

        self.root.after(1000, self.update_countdown)

    def check_events(self):
        """Check for active events."""
        try:
            self.config = load_config()
            self.settings = self.config.get("settings", {})

            active = get_active_events(self.config)

            if active:
                event = active[0]

                # Only log when NEW event starts
                if not self.current_active_event or self.current_active_event.get(
                    "title"
                ) != event.get("title"):
                    self.log(f"🔔 Event active: {event['title']}")
                    self.current_active_event = event
                    self.go_fullscreen()

                    self.title_label.config(
                        text=event["title"],
                        fg=self.settings.get("font_color", THEME["accent"]),
                    )
                    self.hint_label.config(
                        text="ESC: minimize  •  Q: quit", fg=self.dim_color
                    )

            else:
                if self.current_active_event:
                    # Event just ended
                    self.current_active_event = None

                self.exit_fullscreen()

                next_ev, next_dt = get_next_event(self.config)
                if next_ev and next_dt:
                    self.title_label.config(
                        text=f"▶ Next: {next_ev['title']}",
                        font=(FONTS["primary"], 24, "bold"),
                        fg=self.accent_color,
                    )
                    self.sub_label.config(
                        text=f"at {next_dt.strftime('%H:%M')}",
                        font=(FONTS["primary"], 14),
                    )
                else:
                    self.title_label.config(
                        text="◯ No events scheduled",
                        font=(FONTS["primary"], 24, "bold"),
                        fg=self.dim_color,
                    )
                    self.sub_label.config(
                        text=datetime.now().strftime("%A, %B %d · %H:%M"),
                        font=(FONTS["primary"], 14),
                    )

                self.hint_label.config(
                    text="ESC: minimize  •  F11: fullscreen  •  Q: quit",
                    fg=THEME["border"],
                )

        except Exception as e:
            self.log(f"❌ ERROR: {e}")
            import traceback

            if self.verbose:
                traceback.print_exc()

        interval = self.settings.get("check_interval_seconds", 5) * 1000
        self.root.after(interval, self.check_events)

    def run(self):
        """Run the application."""
        self.root.mainloop()
