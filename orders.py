"""Placing orders and listing a user's order history."""
from datetime import datetime, timezone

from db import get_conn

PAGE_SIZE = 10


def place_order(user_id, cart, total, coupon=None):
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO orders (user_id, total, coupon, created_at) VALUES (?, ?, ?, ?)",
        (user_id, total, coupon, datetime.now(timezone.utc).isoformat()),
    )
    order_id = cur.lastrowid
    for item_id, line in cart.items():
        conn.execute(
            "INSERT INTO order_items (order_id, item_id, quantity, price) VALUES (?, ?, ?, ?)",
            (order_id, int(item_id), line["quantity"], line["price"]),
        )
    conn.commit()
    conn.close()
    return order_id


def order_history(user_id, page=1):
    """Orders for a user, newest first. Pages start at 1."""
    offset = page * PAGE_SIZE
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (user_id, PAGE_SIZE, offset),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def order_count(user_id):
    conn = get_conn()
    n = conn.execute("SELECT COUNT(*) FROM orders WHERE user_id = ?", (user_id,)).fetchone()[0]
    conn.close()
    return n
