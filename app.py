"""Campus Canteen web app."""
from flask import Flask, jsonify, redirect, render_template, request, session

import auth
import cart as cart_lib
import orders
import pricing
from db import get_conn, init_db
from timefmt import format_order_time

app = Flask(__name__)
app.secret_key = "dev-only-change-me"


@app.route("/")
def menu():
    conn = get_conn()
    items = conn.execute("SELECT * FROM menu_items WHERE available = 1").fetchall()
    conn.close()
    return render_template("menu.html", items=items)


@app.route("/login", methods=["POST"])
def login():
    user = auth.login(request.form["email"], request.form["password"])
    if user is None:
        return "Invalid email or password", 401
    session["user_id"] = user["id"]
    return redirect("/")


@app.route("/cart/add", methods=["POST"])
def add_to_cart():
    item_id = int(request.json["item_id"])
    conn = get_conn()
    item = conn.execute("SELECT * FROM menu_items WHERE id = ?", (item_id,)).fetchone()
    conn.close()
    cart = session.get("cart", {})
    cart_lib.add_item(cart, dict(item))
    session["cart"] = cart
    return jsonify({"count": cart_lib.item_count(cart)})


@app.route("/checkout", methods=["POST"])
def checkout():
    cart = session.get("cart", {})
    subtotal = cart_lib.cart_total(cart)
    code = request.form.get("coupon")
    total = pricing.final_total(subtotal, code)
    order_id = orders.place_order(session["user_id"], cart, total, code)
    session["cart"] = {}
    return redirect(f"/orders?placed={order_id}")


@app.route("/orders")
def order_list():
    page = int(request.args.get("page", 1))
    rows = orders.order_history(session["user_id"], page)
    for r in rows:
        r["display_time"] = format_order_time(r["created_at"])
    return jsonify(rows)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
