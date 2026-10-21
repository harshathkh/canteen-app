"""Coupons and final price calculation at checkout."""

COUPONS = {
    "WELCOME10": {"type": "percent", "value": 10},
    "FLAT50": {"type": "flat", "value": 50, "min_total": 200},
    "STUDENT15": {"type": "percent", "value": 15},
}

GST_RATE = 0.05


def apply_coupon(subtotal, code):
    """Return the subtotal after the coupon, or the subtotal unchanged."""
    if not code:
        return subtotal
    coupon = COUPONS.get(code.strip().upper())
    if coupon is None:
        return subtotal
    if coupon["type"] == "percent":
        return round(subtotal * coupon["value"] / 100, 2)
    if coupon["type"] == "flat":
        if subtotal < coupon.get("min_total", 0):
            return subtotal
        return max(subtotal - coupon["value"], 0)
    return subtotal


def final_total(subtotal, code=None):
    discounted = apply_coupon(subtotal, code)
    return round(discounted * (1 + GST_RATE), 2)
