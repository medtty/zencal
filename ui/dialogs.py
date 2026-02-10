import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from core.config import save_config
from ui.theme import ENTRY_STYLE, FONTS, LABEL_STYLE, THEME


class EventDialog:
    """Dialog for adding/editing events."""

    def __init__(self, parent, title, event=None):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x450")
        self.dialog.configure(bg=THEME["bg_dark"])
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (450 // 2)
        self.dialog.geometry(f"+{x}+{y}")

        self.event = event or {}
        self.setup_form()

        self.dialog.wait_window()

    def setup_form(self):
        """Setup the form UI."""
        # Header
        header = tk.Frame(self.dialog, bg=THEME["bg_mid"], height=50)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="▶ EVENT DETAILS",
            font=(FONTS["primary"], 12, "bold"),
            fg=THEME["accent"],
            bg=THEME["bg_mid"],
        ).pack(side="left", padx=20, pady=15)

        # Form
        form_frame = tk.Frame(self.dialog, bg=THEME["bg_dark"])
        form_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Title
        tk.Label(form_frame, text="TITLE", **LABEL_STYLE).pack(fill="x", pady=(0, 5))
        self.title_var = tk.StringVar(value=self.event.get("title", ""))
        tk.Entry(form_frame, textvariable=self.title_var, **ENTRY_STYLE).pack(
            fill="x", ipady=10, pady=(0, 15)
        )

        # Date
        tk.Label(form_frame, text="DATE (YYYY-MM-DD)", **LABEL_STYLE).pack(
            fill="x", pady=(0, 5)
        )
        self.date_var = tk.StringVar(
            value=self.event.get("date", datetime.now().strftime("%Y-%m-%d"))
        )
        tk.Entry(form_frame, textvariable=self.date_var, **ENTRY_STYLE).pack(
            fill="x", ipady=10, pady=(0, 15)
        )

        # Time
        tk.Label(form_frame, text="TIME (HH:MM)", **LABEL_STYLE).pack(
            fill="x", pady=(0, 5)
        )
        self.time_var = tk.StringVar(value=self.event.get("time", "09:00"))
        tk.Entry(form_frame, textvariable=self.time_var, **ENTRY_STYLE).pack(
            fill="x", ipady=10, pady=(0, 15)
        )

        # Duration
        tk.Label(form_frame, text="DURATION (minutes)", **LABEL_STYLE).pack(
            fill="x", pady=(0, 5)
        )
        self.duration_var = tk.StringVar(
            value=str(self.event.get("duration_minutes", 30))
        )
        tk.Entry(form_frame, textvariable=self.duration_var, **ENTRY_STYLE).pack(
            fill="x", ipady=10, pady=(0, 15)
        )

        # Repeat
        tk.Label(form_frame, text="REPEAT", **LABEL_STYLE).pack(fill="x", pady=(0, 5))
        self.repeat_var = tk.StringVar(value=self.event.get("repeat", "none"))

        style = ttk.Style()
        style.configure(
            "TCombobox", fieldbackground=THEME["bg_mid"], background=THEME["bg_mid"]
        )

        repeat_combo = ttk.Combobox(
            form_frame,
            textvariable=self.repeat_var,
            values=["none", "daily", "weekdays", "weekly", "monthly"],
            state="readonly",
            font=(FONTS["primary"], 11),
        )
        repeat_combo.pack(fill="x", ipady=10, pady=(0, 15))

        # Note
        tk.Label(form_frame, text="NOTE (optional)", **LABEL_STYLE).pack(
            fill="x", pady=(0, 5)
        )
        self.note_var = tk.StringVar(value=self.event.get("note", ""))
        tk.Entry(form_frame, textvariable=self.note_var, **ENTRY_STYLE).pack(
            fill="x", ipady=10, pady=(0, 20)
        )

        # Buttons
        btn_frame = tk.Frame(form_frame, bg=THEME["bg_dark"])
        btn_frame.pack(fill="x")

        tk.Button(
            btn_frame,
            text="CANCEL",
            command=self.dialog.destroy,
            font=(FONTS["primary"], 10),
            bg=THEME["bg_light"],
            fg=THEME["text"],
            activebackground=THEME["bg_mid"],
            relief="flat",
            padx=30,
            pady=10,
            cursor="hand2",
            bd=0,
        ).pack(side="right", padx=(10, 0))

        tk.Button(
            btn_frame,
            text="SAVE",
            command=self.save,
            font=(FONTS["primary"], 10, "bold"),
            bg=THEME["accent"],
            fg=THEME["bg_dark"],
            activebackground=THEME["accent_dim"],
            relief="flat",
            padx=30,
            pady=10,
            cursor="hand2",
            bd=0,
        ).pack(side="right")

    def save(self):
        """Validate and save event."""
        try:
            title = self.title_var.get().strip()
            if not title:
                messagebox.showerror("Error", "Title cannot be empty")
                return

            date = self.date_var.get().strip()
            datetime.strptime(date, "%Y-%m-%d")

            time = self.time_var.get().strip()
            datetime.strptime(time, "%H:%M")

            duration = int(self.duration_var.get())
            if duration <= 0:
                raise ValueError("Duration must be positive")

            self.result = {
                "title": title,
                "date": date,
                "time": time,
                "duration_minutes": duration,
                "repeat": self.repeat_var.get(),
                "note": self.note_var.get().strip(),
            }

            self.dialog.destroy()

        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Check your inputs:\n{str(e)}")


class SettingsDialog:
    """Dialog for editing settings."""

    def __init__(self, parent, config):
        self.config = config
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Settings")
        self.dialog.geometry("500x400")
        self.dialog.configure(bg=THEME["bg_dark"])
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (400 // 2)
        self.dialog.geometry(f"+{x}+{y}")

        self.setup_form()
        self.dialog.wait_window()

    def setup_form(self):
        """Setup settings form."""
        # Header
        header = tk.Frame(self.dialog, bg=THEME["bg_mid"], height=50)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="⚙ SETTINGS",
            font=(FONTS["primary"], 12, "bold"),
            fg=THEME["accent"],
            bg=THEME["bg_mid"],
        ).pack(side="left", padx=20, pady=15)

        form_frame = tk.Frame(self.dialog, bg=THEME["bg_dark"])
        form_frame.pack(fill="both", expand=True, padx=30, pady=20)

        settings = self.config["settings"]

        tk.Label(form_frame, text="CHECK INTERVAL (seconds)", **LABEL_STYLE).pack(
            fill="x", pady=(0, 5)
        )
        self.interval_var = tk.StringVar(value=str(settings["check_interval_seconds"]))
        tk.Entry(form_frame, textvariable=self.interval_var, **ENTRY_STYLE).pack(
            fill="x", ipady=10, pady=(0, 15)
        )

        tk.Label(form_frame, text="TITLE FONT SIZE", **LABEL_STYLE).pack(
            fill="x", pady=(0, 5)
        )
        self.font_size_var = tk.StringVar(value=str(settings["font_size"]))
        tk.Entry(form_frame, textvariable=self.font_size_var, **ENTRY_STYLE).pack(
            fill="x", ipady=10, pady=(0, 15)
        )

        tk.Label(form_frame, text="TEXT COLOR (hex)", **LABEL_STYLE).pack(
            fill="x", pady=(0, 5)
        )
        self.font_color_var = tk.StringVar(value=settings["font_color"])
        tk.Entry(form_frame, textvariable=self.font_color_var, **ENTRY_STYLE).pack(
            fill="x", ipady=10, pady=(0, 15)
        )

        tk.Label(form_frame, text="BACKGROUND COLOR (hex)", **LABEL_STYLE).pack(
            fill="x", pady=(0, 5)
        )
        self.bg_color_var = tk.StringVar(value=settings["bg_color"])
        tk.Entry(form_frame, textvariable=self.bg_color_var, **ENTRY_STYLE).pack(
            fill="x", ipady=10, pady=(0, 20)
        )

        btn_frame = tk.Frame(form_frame, bg=THEME["bg_dark"])
        btn_frame.pack(fill="x")

        tk.Button(
            btn_frame,
            text="CANCEL",
            command=self.dialog.destroy,
            font=(FONTS["primary"], 10),
            bg=THEME["bg_light"],
            fg=THEME["text"],
            activebackground=THEME["bg_mid"],
            relief="flat",
            padx=30,
            pady=10,
            cursor="hand2",
            bd=0,
        ).pack(side="right", padx=(10, 0))

        tk.Button(
            btn_frame,
            text="SAVE",
            command=self.save,
            font=(FONTS["primary"], 10, "bold"),
            bg=THEME["accent"],
            fg=THEME["bg_dark"],
            activebackground=THEME["accent_dim"],
            relief="flat",
            padx=30,
            pady=10,
            cursor="hand2",
            bd=0,
        ).pack(side="right")

    def save(self):
        """Save settings."""
        try:
            self.config["settings"]["check_interval_seconds"] = int(
                self.interval_var.get()
            )
            self.config["settings"]["font_size"] = int(self.font_size_var.get())
            self.config["settings"]["font_color"] = self.font_color_var.get()
            self.config["settings"]["bg_color"] = self.bg_color_var.get()

            save_config(self.config)
            messagebox.showinfo("Success", "Settings saved! Restart overlay to apply.")
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")
