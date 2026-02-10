from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).parent.parent / "zencal.log"


def log_message(msg):
    """Log message to file and console."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_line = f"[{timestamp}] {msg}"

    # Write to file
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line + "\n")
    except:
        pass

    # Print to console
    print(log_line)

    return log_line


def clear_log():
    """Clear the log file."""
    try:
        LOG_FILE.unlink()
    except:
        pass


def get_log_path():
    """Return the log file path."""
    return LOG_FILE
