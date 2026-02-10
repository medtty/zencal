#!/usr/bin/env python3
import argparse
import sys


def main():
    """Launch ZenCal in overlay or manager mode."""
    parser = argparse.ArgumentParser(
        description="ZenCal - Distraction-Free Event Reminders",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  zencal                    Launch overlay (default)
  zencal --manager          Launch manager GUI
  zencal --verbose          Launch overlay with verbose logging
  zencal --clear-log        Clear log file on startup
        """,
    )

    parser.add_argument(
        "--manager",
        "-m",
        action="store_true",
        help="Launch manager GUI instead of overlay",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed logs in terminal (overlay only)",
    )
    parser.add_argument(
        "--clear-log", action="store_true", help="Clear log file on startup"
    )

    args = parser.parse_args()

    if args.manager:
        # Launch manager
        print("=" * 60)
        print("⬡ ZenCal Manager Starting...")
        print("=" * 60)

        from ui.manager_window import EventManagerApp

        app = EventManagerApp()
        app.run()
    else:
        # Launch overlay (default)
        from core.logger import clear_log

        if args.clear_log:
            clear_log()
            print("✓ Log file cleared")

        print("=" * 60)
        print("⬡ ZenCal Starting...")
        if args.verbose:
            print("📋 Verbose mode enabled - logs will show in terminal")
        else:
            print("💡 Use --verbose flag to see logs in terminal")
            print("📁 Or check zencal.log file for detailed logs")
        print("=" * 60)

        from ui.overlay import ZenCalOverlay

        app = ZenCalOverlay(verbose=args.verbose)
        app.run()


if __name__ == "__main__":
    main()
