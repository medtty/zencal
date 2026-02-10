# Main theme colors
THEME = {
    # Backgrounds
    "bg_dark": "#0a0a0f",  # Darkest background
    "bg_mid": "#1a1a24",  # Mid-tone background
    "bg_light": "#2a2a38",  # Lighter panels
    # Accent colors
    "accent": "#00d9ff",  # Primary cyan accent (EDIT THIS!)
    "accent_dim": "#0088aa",  # Dimmed accent
    # Text colors
    "text": "#e2e8f0",  # Primary text
    "text_dim": "#94a3b8",  # Secondary text
    "text_darker": "#64748b",  # Tertiary text
    # UI elements
    "border": "#334155",  # Borders and dividers
    "success": "#10b981",  # Success/positive
    "danger": "#ef4444",  # Danger/negative
}

# Fonts
FONTS = {
    "primary": "JetBrains Mono",  # Main font (change to "Consolas", "Courier New", etc.)
    "fallback": "Courier",  # Fallback if primary not available
}

# Button styles
BUTTON_STYLE = {
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

# Entry/Input styles
ENTRY_STYLE = {
    "font": (FONTS["primary"], 11),
    "bg": THEME["bg_mid"],
    "fg": THEME["text"],
    "relief": "flat",
    "insertbackground": THEME["accent"],
    "highlightbackground": THEME["border"],
    "highlightcolor": THEME["accent"],
    "highlightthickness": 1,
}

# Label styles
LABEL_STYLE = {
    "font": (FONTS["primary"], 9),
    "fg": THEME["text_dim"],
    "bg": THEME["bg_dark"],
    "anchor": "w",
}
