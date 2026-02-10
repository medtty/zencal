from datetime import datetime, timedelta


def is_event_active(event):
    """Check if an event should be showing right now."""
    now = datetime.now()
    today = now.date()

    try:
        event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
        event_time = datetime.strptime(event["time"], "%H:%M").time()
    except (ValueError, KeyError):
        return False

    repeat = event.get("repeat", "none")
    duration = event.get("duration_minutes", 30)

    # Check if this event applies today
    applies_today = False

    if repeat == "none":
        applies_today = today == event_date
    elif repeat == "daily":
        applies_today = today >= event_date
    elif repeat == "weekdays":
        applies_today = today >= event_date and today.weekday() < 5
    elif repeat == "weekly":
        applies_today = today >= event_date and today.weekday() == event_date.weekday()
    elif repeat == "monthly":
        applies_today = today >= event_date and today.day == event_date.day

    if not applies_today:
        return False

    # Check if we're within the time window
    event_start = datetime.combine(today, event_time)
    event_end = event_start + timedelta(minutes=duration)

    return event_start <= now <= event_end


def get_active_events(config):
    """Return list of currently active events."""
    return [e for e in config.get("events", []) if is_event_active(e)]


def get_next_event(config):
    """Return the next upcoming event today."""
    now = datetime.now()
    today = now.date()
    closest = None
    closest_dt = None

    for event in config.get("events", []):
        try:
            event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
            event_time = datetime.strptime(event["time"], "%H:%M").time()
        except (ValueError, KeyError):
            continue

        repeat = event.get("repeat", "none")

        applies_today = False
        if repeat == "none":
            applies_today = today == event_date
        elif repeat == "daily":
            applies_today = today >= event_date
        elif repeat == "weekdays":
            applies_today = today >= event_date and today.weekday() < 5
        elif repeat == "weekly":
            applies_today = (
                today >= event_date and today.weekday() == event_date.weekday()
            )
        elif repeat == "monthly":
            applies_today = today >= event_date and today.day == event_date.day

        if not applies_today:
            continue

        event_dt = datetime.combine(today, event_time)
        if event_dt > now:
            if closest_dt is None or event_dt < closest_dt:
                closest = event
                closest_dt = event_dt

    return closest, closest_dt


def is_repeat_active(event, check_date):
    """Check if a repeating event applies to a given date."""
    try:
        event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
    except (ValueError, KeyError):
        return False

    if check_date < event_date:
        return False

    repeat = event.get("repeat", "none")

    if repeat == "daily":
        return True
    elif repeat == "weekdays":
        return check_date.weekday() < 5
    elif repeat == "weekly":
        return check_date.weekday() == event_date.weekday()
    elif repeat == "monthly":
        return check_date.day == event_date.day

    return False
