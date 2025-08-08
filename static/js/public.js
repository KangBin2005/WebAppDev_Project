// Retrieve existing cart or create an empty one
let cart = JSON.parse(localStorage.getItem("cart")) || [];

// Select cart amount badge from navbar (if present)
let cartAmountEl = document.querySelector(".cart-amount");

/**
 * Update the cart count badge in the navbar
 */
function updateCartCount() {
    if (!cartAmountEl) return; // Do nothing if no badge exists
    let totalItems = cart.reduce((acc, item) => acc + item.quantity, 0);
    cartAmountEl.textContent = totalItems;
}

// Initial update when page loads
updateCartCount();

/**
 * Add a product to the cart
 * @param {string} id - Product ID
 * @param {string} name - Product name
 * @param {number} price - Product price
 */
function addToCart(id, name, price) {
    let existingItem = cart.find(item => item.id === id);

    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: id,
            name: name,
            price: price,
            quantity: 1
        });
    }

    localStorage.setItem("cart", JSON.stringify(cart));
    updateCartCount();
}

// Attach click events to all Add-to-Cart buttons
document.querySelectorAll(".add-to-cart-btn").forEach(button => {
    button.addEventListener("click", function () {
        let id = this.dataset.id;
        let name = this.dataset.name;
        let price = parseFloat(this.dataset.price);
        addToCart(id, name, price);
    });
});