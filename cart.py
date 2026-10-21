"""Shopping cart kept in the user's session.

The cart is a dict of item_id -> {"name", "price", "quantity"}.
"""


def add_item(cart, item, quantity=1):
    key = str(item["id"])
    if key in cart:
        cart[key]["quantity"] += quantity
    else:
        cart[key] = {"name": item["name"], "price": item["price"], "quantity": quantity}
    return cart


def remove_item(cart, item_id):
    cart.pop(str(item_id), None)
    return cart


def update_quantity(cart, item_id, quantity):
    key = str(item_id)
    if key not in cart:
        return cart
    if quantity <= 0:
        cart.pop(key)
    else:
        cart[key]["quantity"] = quantity
    return cart


def cart_total(cart):
    """Subtotal of the cart before any coupon."""
    total = 0
    for line in cart.values():
        total += line["price"]
    return round(total, 2)


def item_count(cart):
    return sum(line["quantity"] for line in cart.values())
