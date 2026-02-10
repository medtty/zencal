import json
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk

from core.config import load_config, save_config
from ui.calendar_view import CalendarView
from ui.dialogs import EventDialog, SettingsDialog
from ui.theme import BUTTON_STYLE, FONTS, THEME


class EventManagerApp:
    """Main event manager application."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ZenCal Manager")
        self.root.geometry("1200x750")
        self.root.configure(bg=THEME["bg_dark"])

        # ADD THIS SECTION:
        # Set window icon
        from pathlib import Path

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
        # END OF NEW SECTION

        self.config = load_config()
        self.selected_index = None

        self.setup_ui()
        self.refresh_event_list()

    def setup_ui(self):
        """Setup the main UI."""
        # Header bar
        header_bar = tk.Frame(self.root, bg=THEME["bg_mid"], height=60)
        header_bar.pack(fill="x")
        header_bar.pack_propagate(False)

        tk.Label(
            header_bar,
            text="⬡ ZENCAL",
            font=(FONTS["primary"], 20, "bold"),
            fg=THEME["accent"],
            bg=THEME["bg_mid"],
        ).pack(side="left", padx=30, pady=15)

        tk.Label(
            header_bar,
            text="EVENT MANAGER",
            font=(FONTS["primary"], 10),
            fg=THEME["text_dim"],
            bg=THEME["bg_mid"],
        ).pack(side="left", pady=15)

        # Main container
        main_container = tk.Frame(self.root, bg=THEME["bg_dark"])
        main_container.pack(fill="both", expand=True)

        # Left pane: Calendar
        left_pane = tk.Frame(main_container, bg=THEME["bg_dark"], width=380)
        left_pane.pack(side="left", fill="both", padx=(20, 10), pady=20)
        left_pane.pack_propagate(False)

        # Right pane: Event list
        right_pane = tk.Frame(main_container, bg=THEME["bg_dark"])
        right_pane.pack(side="left", fill="both", expand=True, padx=(10, 20), pady=20)

        # ─── LEFT PANE: Calendar ──────────────────────────────────────────────

        self.calendar_view = CalendarView(
            left_pane, self.config, on_day_click=self.on_calendar_day_click
        )

        # Quick add button
        tk.Button(
            left_pane,
            text="+ QUICK ADD TODAY",
            command=self.quick_add_today,
            font=(FONTS["primary"], 11, "bold"),
            bg=THEME["accent"],
            fg=THEME["bg_dark"],
            activebackground=THEME["accent_dim"],
            activeforeground=THEME["bg_dark"],
            relief="flat",
            padx=20,
            pady=12,
            cursor="hand2",
            bd=0,
        ).pack(fill="x", pady=(15, 0))

        # ─── RIGHT PANE: Event List ──────────────────────────────────────────

        # Header
        header = tk.Frame(right_pane, bg=THEME["bg_dark"])
        header.pack(fill="x", pady=(0, 15))

        tk.Label(
            header,
            text="▶ EVENTS",
            font=(FONTS["primary"], 14, "bold"),
            fg=THEME["text"],
            bg=THEME["bg_dark"],
        ).pack(side="left")

        # Button frame
        btn_frame = tk.Frame(right_pane, bg=THEME["bg_dark"])
        btn_frame.pack(fill="x", pady=(0, 15))

        tk.Button(
            btn_frame, text="+ ADD", command=self.add_event, width=10, **BUTTON_STYLE
        ).pack(side="left", padx=(0, 8))
        tk.Button(
            btn_frame, text="✎ EDIT", command=self.edit_event, width=10, **BUTTON_STYLE
        ).pack(side="left", padx=(0, 8))
        tk.Button(
            btn_frame,
            text="🗑 DELETE",
            command=self.delete_event,
            width=10,
            **BUTTON_STYLE,
        ).pack(side="left", padx=(0, 8))
        tk.Button(
            btn_frame,
            text="⚙ SETTINGS",
            command=self.open_settings,
            width=12,
            **BUTTON_STYLE,
        ).pack(side="left", padx=(0, 8))

        # Import/Export
        tk.Button(
            btn_frame,
            text="⬇ IMPORT",
            command=self.import_events,
            width=10,
            **BUTTON_STYLE,
        ).pack(side="right")
        tk.Button(
            btn_frame,
            text="⬆ EXPORT",
            command=self.export_events,
            width=10,
            **BUTTON_STYLE,
        ).pack(side="right", padx=(0, 8))

        # Event list
        list_frame = tk.Frame(right_pane, bg=THEME["bg_mid"])
        list_frame.pack(fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        # Treeview
        columns = ("title", "date", "time", "duration", "repeat", "note")
        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
            selectmode="browse",
        )

        self.tree.heading("title", text="TITLE")
        self.tree.heading("date", text="DATE")
        self.tree.heading("time", text="TIME")
        self.tree.heading("duration", text="DURATION")
        self.tree.heading("repeat", text="REPEAT")
        self.tree.heading("note", text="NOTE")

        self.tree.column("title", width=180)
        self.tree.column("date", width=100)
        self.tree.column("time", width=80)
        self.tree.column("duration", width=90)
        self.tree.column("repeat", width=100)
        self.tree.column("note", width=150)

        self.tree.pack(fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)

        # Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background=THEME["bg_mid"],
            foreground=THEME["text"],
            fieldbackground=THEME["bg_mid"],
            borderwidth=0,
            font=(FONTS["primary"], 10),
        )
        style.configure(
            "Treeview.Heading",
            background=THEME["bg_light"],
            foreground=THEME["accent"],
            relief="flat",
            font=(FONTS["primary"], 9, "bold"),
        )
        style.map("Treeview", background=[("selected", THEME["bg_light"])])

        # Double-click to edit
        self.tree.bind("<Double-1>", lambda e: self.edit_event())

        # Event count
        self.count_label = tk.Label(
            right_pane,
            text="",
            font=(FONTS["primary"], 9),
            fg=THEME["text_darker"],
            bg=THEME["bg_dark"],
        )
        self.count_label.pack(anchor="e", pady=(10, 0))

    def on_calendar_day_click(self, day):
        """Handle calendar day click."""
        # Could implement filtering by day here
        messagebox.showinfo(
            "Day Clicked", f"Clicked day {day}\n(Filter feature coming soon)"
        )

    def quick_add_today(self):
        """Quick add event for today."""
        today = datetime.now().strftime("%Y-%m-%d")
        dialog = EventDialog(self.root, "Quick Add Today", {"date": today})
        if dialog.result:
            self.config["events"].append(dialog.result)
            save_config(self.config)
            self.refresh_event_list()
            self.calendar_view.update_config(self.config)

    def refresh_event_list(self):
        """Reload events and update list."""
        self.config = load_config()
        self.tree.delete(*self.tree.get_children())

        events = self.config.get("events", [])

        # Sort by date/time
        try:
            events_sorted = sorted(
                events, key=lambda e: (e.get("date", "9999"), e.get("time", "99:99"))
            )
        except:
            events_sorted = events

        for event in events_sorted:
            self.tree.insert(
                "",
                "end",
                values=(
                    event.get("title", ""),
                    event.get("date", ""),
                    event.get("time", ""),
                    f"{event.get('duration_minutes', 30)}m",
                    event.get("repeat", "none"),
                    event.get("note", ""),
                ),
            )

        self.count_label.config(
            text=f"◯ {len(events)} event{'s' if len(events) != 1 else ''}"
        )

    def add_event(self):
        """Add new event."""
        dialog = EventDialog(self.root, "Add Event")
        if dialog.result:
            self.config["events"].append(dialog.result)
            save_config(self.config)
            self.refresh_event_list()
            self.calendar_view.update_config(self.config)

    def edit_event(self):
        """Edit selected event."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an event to edit.")
            return

        item_values = self.tree.item(selected[0])["values"]
        if not item_values:
            return

        # Find event
        title = item_values[0]
        date = item_values[1]
        time = item_values[2]

        event_index = None
        for i, event in enumerate(self.config["events"]):
            if (
                event.get("title") == title
                and event.get("date") == date
                and event.get("time") == time
            ):
                event_index = i
                break

        if event_index is None:
            messagebox.showerror("Error", "Could not find event")
            return

        event = self.config["events"][event_index]

        dialog = EventDialog(self.root, "Edit Event", event)
        if dialog.result:
            self.config["events"][event_index] = dialog.result
            save_config(self.config)
            self.refresh_event_list()
            self.calendar_view.update_config(self.config)

    def delete_event(self):
        """Delete selected event."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an event to delete.")
            return

        item_values = self.tree.item(selected[0])["values"]
        if not item_values:
            return

        title = item_values[0]
        date = item_values[1]
        time = item_values[2]

        # Find and remove
        event_index = None
        for i, event in enumerate(self.config["events"]):
            if (
                event.get("title") == title
                and event.get("date") == date
                and event.get("time") == time
            ):
                event_index = i
                break

        if event_index is None:
            messagebox.showerror("Error", "Could not find event")
            return

        event = self.config["events"][event_index]

        if messagebox.askyesno("Confirm Delete", f"Delete '{event['title']}'?"):
            self.config["events"].pop(event_index)
            save_config(self.config)
            self.refresh_event_list()
            self.calendar_view.update_config(self.config)

    def import_events(self):
        """Import events from JSON."""
        filepath = filedialog.askopenfilename(
            title="Import Events",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )

        if not filepath:
            return

        try:
            with open(filepath, "r") as f:
                data = json.load(f)

            if "events" not in data:
                messagebox.showerror("Error", "Invalid format: 'events' key not found")
                return

            imported = data["events"]

            if self.config.get("events"):
                choice = messagebox.askyesnocancel(
                    "Import Mode",
                    f"Found {len(imported)} events.\n\n"
                    "Yes = Merge\nNo = Replace\nCancel = Abort",
                )

                if choice is None:
                    return
                elif choice:
                    self.config["events"].extend(imported)
                else:
                    self.config["events"] = imported
            else:
                self.config["events"] = imported

            save_config(self.config)
            self.refresh_event_list()
            self.calendar_view.update_config(self.config)
            messagebox.showinfo("Success", f"Imported {len(imported)} events")

        except Exception as e:
            messagebox.showerror("Import Error", f"Failed:\n{str(e)}")

    def export_events(self):
        """Export events to JSON."""
        filepath = filedialog.asksaveasfilename(
            title="Export Events",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"zencal_export_{datetime.now().strftime('%Y%m%d')}.json",
        )

        if not filepath:
            return

        try:
            export_data = {
                "events": self.config.get("events", []),
                "exported_at": datetime.now().isoformat(),
                "event_count": len(self.config.get("events", [])),
            }

            with open(filepath, "w") as f:
                json.dump(export_data, f, indent=2)

            messagebox.showinfo(
                "Success", f"Exported {len(export_data['events'])} events"
            )

        except Exception as e:
            messagebox.showerror("Export Error", f"Failed:\n{str(e)}")

    def open_settings(self):
        """Open settings dialog."""
        SettingsDialog(self.root, self.config)
        self.config = load_config()

    def run(self):
        """Run the application."""
        self.root.mainloop()
