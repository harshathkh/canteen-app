// Menu page: "Add to cart" buttons and the cart counter in the header.

function bindAddButtons() {
  document.querySelectorAll(".add-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      fetch("/cart/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ item_id: btn.dataset.id }),
      })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          document.getElementById("cart-count").textContent = data.count;
        });
    });
  });
}

document.addEventListener("DOMContentLoaded", bindAddButtons);
window.addEventListener("load", bindAddButtons);
