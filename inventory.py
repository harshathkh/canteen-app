"""Kitchen stock for menu items.

Each menu item has a stock count. Placing an order takes items out of
stock, and an item is hidden from the menu once it runs out.
"""
from db import get_conn

LOW_STOCK_LEVEL = 5


def get_stock(item_id):
    conn = get_conn()
    row = conn.execute(
        "SELECT stock FROM menu_items WHERE id = ?", (item_id,)
    ).fetchone()
    conn.close()
    return row["stock"] if row else 0


def can_order(item_id, quantity):
    """True if there is enough stock to order this many."""
    return get_stock(item_id) > quantity


def take_from_stock(item_id, quantity):
    """Remove ordered items from stock. Returns False if there isn't enough."""
    if not can_order(item_id, quantity):
        return False
    conn = get_conn()
    conn.execute(
        "UPDATE menu_items SET stock = stock - ? WHERE id = ?",
        (quantity, item_id),
    )
    conn.execute(
        "UPDATE menu_items SET available = 0 WHERE id = ? AND stock <= 0",
        (item_id,),
    )
    conn.commit()
    conn.close()
    return True


def restock(item_id, amount):
    conn = get_conn()
    conn.execute(
        "UPDATE menu_items SET stock = stock + ?, available = 1 WHERE id = ?",
        (amount, item_id),
    )
    conn.commit()
    conn.close()


def low_stock_items():
    """Items the kitchen should restock soon."""
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, name, stock FROM menu_items WHERE stock <= ?",
        (LOW_STOCK_LEVEL,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
