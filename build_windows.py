import sys
from pathlib import Path

import PyInstaller.__main__

# ---------------------------------------------------------------------
# Project root (absolute, no guessing)
# ---------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent

# ---------------------------------------------------------------------
# Icon handling
# ---------------------------------------------------------------------
PNG_ICON = ROOT / "zencal.png"
ICO_ICON = ROOT / "zencal.ico"

icon_args = []

if not PNG_ICON.exists():
    print("⚠ zencal.png not found — building without icon")
else:
    try:
        from PIL import Image

        img = Image.open(PNG_ICON).convert("RGBA")

        # Windows expects multiple icon sizes
        img.save(
            ICO_ICON,
            format="ICO",
            sizes=[
                (16, 16),
                (32, 32),
                (48, 48),
                (64, 64),
                (128, 128),
                (256, 256),
            ],
        )

        icon_args = [f"--icon={ICO_ICON.as_posix()}"]
        print(f"✓ Windows icon created: {ICO_ICON}")

    except Exception as e:
        print(f"⚠ Failed to generate ICO: {e}")

# ---------------------------------------------------------------------
# PyInstaller build
# ---------------------------------------------------------------------
print("\nBuilding ZenCal for Windows...\n")

PyInstaller.__main__.run(
    [
        str(ROOT / "zencal.py"),
        "--name=ZenCal",
        "--onefile",
        "--windowed",  # No console window
        "--clean",  # Avoid stale build artifacts
        "--noconfirm",
        "--add-data=core;core",
        "--add-data=ui;ui",
        "--hidden-import=pystray",
        "--hidden-import=PIL",
        *icon_args,
    ]
)

print("\n" + "=" * 60)
print("✓ Build complete")
print("=" * 60)
print("Executable: dist/ZenCal.exe")
print("\nIf the icon still looks wrong:")
print("• Rename the exe (Windows icon cache)")
print("• Restart Explorer")
print("• Inspect with Resource Hacker")
print("=" * 60)
