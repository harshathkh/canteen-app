"""Formatting timestamps for display on the order pages."""
from datetime import datetime


def format_order_time(iso_string):
    """Show an order's time like '21 Oct 2026, 1:05 PM'."""
    dt = datetime.fromisoformat(iso_string)
    return dt.strftime("%d %b %Y, %I:%M %p").lstrip("0")


def is_today(iso_string):
    dt = datetime.fromisoformat(iso_string)
    return dt.date() == datetime.now().date()
