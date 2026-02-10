import calendar as cal
import tkinter as tk
from datetime import datetime, timedelta

from core.events import is_repeat_active
from ui.theme import FONTS, THEME


class CalendarView:
    """Calendar grid component."""

    def __init__(self, parent, config, on_day_click=None):
        self.parent = parent
        self.config = config
        self.current_date = datetime.now()
        self.on_day_click = on_day_click

        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        """Setup calendar UI."""
        # Header
        header = tk.Frame(self.parent, bg=THEME["bg_dark"])
        header.pack(fill="x", pady=(0, 15))

        tk.Label(
            header,
            text="▶ CALENDAR",
            font=(FONTS["primary"], 14, "bold"),
            fg=THEME["text"],
            bg=THEME["bg_dark"],
        ).pack(anchor="w")

        # Navigation
        nav_frame = tk.Frame(self.parent, bg=THEME["bg_mid"], height=45)
        nav_frame.pack(fill="x", pady=(0, 15))

        btn_style = {
            "font": (FONTS["primary"], 10),
            "bg": THEME["bg_light"],
            "fg": THEME["text"],
            "activebackground": THEME["accent_dim"],
            "activeforeground": THEME["text"],
            "relief": "flat",
            "padx": 15,
            "pady": 8,
            "cursor": "hand2",
            "bd": 0,
        }

        tk.Button(nav_frame, text="◀", command=self.prev_month, **btn_style).pack(
            side="left", padx=10, pady=8
        )

        self.month_label = tk.Label(
            nav_frame,
            text="",
            font=(FONTS["primary"], 12, "bold"),
            fg=THEME["accent"],
            bg=THEME["bg_mid"],
        )
        self.month_label.pack(side="left", expand=True, pady=8)

        tk.Button(nav_frame, text="▶", command=self.next_month, **btn_style).pack(
            side="left", padx=10, pady=8
        )
        tk.Button(nav_frame, text="TODAY", command=self.goto_today, **btn_style).pack(
            side="left", padx=(5, 10), pady=8
        )

        # Calendar grid
        self.calendar_frame = tk.Frame(self.parent, bg=THEME["bg_dark"])
        self.calendar_frame.pack(fill="both", expand=True)

    def prev_month(self):
        """Previous month."""
        self.current_date = self.current_date - timedelta(days=28)
        self.current_date = self.current_date.replace(day=1)
        self.refresh()

    def next_month(self):
        """Next month."""
        self.current_date = self.current_date.replace(day=28) + timedelta(days=4)
        self.current_date = self.current_date.replace(day=1)
        self.refresh()

    def goto_today(self):
        """Go to current month."""
        self.current_date = datetime.now()
        self.refresh()

    def refresh(self):
        """Refresh calendar display."""
        # Clear
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # Update label
        self.month_label.config(text=self.current_date.strftime("%B %Y").upper())

        year = self.current_date.year
        month = self.current_date.month
        month_calendar = cal.monthcalendar(year, month)

        # Get events
        events_by_date = {}
        for event in self.config.get("events", []):
            try:
                event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
                if event_date.year == year and event_date.month == month:
                    day = event_date.day
                    if day not in events_by_date:
                        events_by_date[day] = []
                    events_by_date[day].append(event)

                # Repeating
                repeat = event.get("repeat", "none")
                if repeat in ["daily", "weekdays", "weekly", "monthly"]:
                    for week in month_calendar:
                        for day in week:
                            if day == 0:
                                continue
                            check_date = datetime(year, month, day).date()
                            if is_repeat_active(event, check_date):
                                if day not in events_by_date:
                                    events_by_date[day] = []
                                if event not in events_by_date[day]:
                                    events_by_date[day].append(event)
            except (ValueError, KeyError):
                continue

        # Day headers
        days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
        for i, day in enumerate(days):
            label = tk.Label(
                self.calendar_frame,
                text=day,
                font=(FONTS["primary"], 8, "bold"),
                fg=THEME["text_dim"],
                bg=THEME["bg_dark"],
                width=6,
            )
            label.grid(row=0, column=i, padx=2, pady=2)

        # Days
        today = datetime.now().date()
        for week_num, week in enumerate(month_calendar, start=1):
            for day_num, day in enumerate(week):
                if day == 0:
                    frame = tk.Frame(
                        self.calendar_frame, bg=THEME["bg_dark"], width=45, height=45
                    )
                    frame.grid(
                        row=week_num, column=day_num, padx=2, pady=2, sticky="nsew"
                    )
                else:
                    date = datetime(year, month, day).date()
                    is_today = date == today
                    has_events = day in events_by_date

                    if is_today:
                        bg = THEME["accent"]
                        fg = THEME["bg_dark"]
                    elif has_events:
                        bg = THEME["bg_light"]
                        fg = THEME["text"]
                    else:
                        bg = THEME["bg_mid"]
                        fg = THEME["text_dim"]

                    frame = tk.Frame(
                        self.calendar_frame,
                        bg=bg,
                        width=45,
                        height=45,
                        highlightbackground=THEME["border"],
                        highlightthickness=1,
                    )
                    frame.grid(
                        row=week_num, column=day_num, padx=2, pady=2, sticky="nsew"
                    )

                    label = tk.Label(
                        frame,
                        text=str(day),
                        font=(FONTS["primary"], 11, "bold" if is_today else "normal"),
                        fg=fg,
                        bg=bg,
                        cursor="hand2" if has_events else "arrow",
                    )
                    label.pack(expand=True, pady=(5, 0))

                    if has_events:
                        indicator = tk.Label(
                            frame,
                            text=f"●{len(events_by_date[day])}",
                            font=(FONTS["primary"], 7),
                            fg=THEME["accent"] if not is_today else THEME["bg_dark"],
                            bg=bg,
                        )
                        indicator.pack(pady=(0, 2))

                        if self.on_day_click:
                            label.bind(
                                "<Button-1>", lambda e, d=day: self.on_day_click(d)
                            )

        # Grid weights
        for i in range(7):
            self.calendar_frame.columnconfigure(i, weight=1)
        for i in range(len(month_calendar) + 1):
            self.calendar_frame.rowconfigure(i, weight=1)

    def update_config(self, config):
        """Update config and refresh."""
        self.config = config
        self.refresh()
