document.addEventListener('DOMContentLoaded', function() {
        function updateCartQuantity(cartId, quantity) {
            fetch("{% url 'update_cart_quantity' %}", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
                },
                body: JSON.stringify({ cart_id: cartId, quantity: quantity })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error('Error:', data.error);
                } else if (data.status === 'updated') {
                    let itemTotalPrice = parseFloat(data.item_total_price) || 0;
                    let totalPrice = parseFloat(data.total_price) || 0;
                    let itemTotalPriceElem = document.querySelector('#cart-item-' + cartId + ' .item-total-price');
                    if (itemTotalPriceElem) {
                        itemTotalPriceElem.textContent = '$' + itemTotalPrice.toFixed(2);
                    } else {
                        console.error('Item total price element not found');
                    }
                    let totalPriceElem = document.getElementById('total-price');
                    if (totalPriceElem) {
                        totalPriceElem.textContent = 'Total Price: $' + totalPrice.toFixed(2);
                    } else {
                        console.error('Total price element not found');
                    }
                } else if (data.status === 'removed') {
                    let itemElem = document.getElementById('cart-item-' + cartId);
                    if (itemElem) {
                        itemElem.remove();
                    } else {
                        console.error('Cart item element not found');
                    }
                    let totalPriceElem = document.getElementById('total-price');
                    if (totalPriceElem) {
                        let totalPrice = parseFloat(data.total_price) || 0;
                        totalPriceElem.textContent = 'Total Price: $' + totalPrice.toFixed(2);
                    } else {
                        console.error('Total price element not found');
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        }

        function checkout() {
            fetch("{% url 'checkout' %}", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Checkout successful!');
                    window.location.reload(); // Reload to update cart view
                } else {
                    alert('Checkout failed: ' + data.error);
                }
            })
            .catch(error => console.error('Error:', error));
        }

        document.querySelectorAll('.quantity-increase').forEach(button => {
            button.addEventListener('click', function() {
                let quantityInput = this.previousElementSibling;
                let quantity = parseInt(quantityInput.value);
                let cartId = this.dataset.cartId;
                quantity++;
                quantityInput.value = quantity;
                updateCartQuantity(cartId, quantity);
            });
        });

        document.querySelectorAll('.quantity-decrease').forEach(button => {
            button.addEventListener('click', function() {
                let quantityInput = this.nextElementSibling;
                let quantity = parseInt(quantityInput.value);
                let cartId = this.dataset.cartId;
                if (quantity > 1) {
                    quantity--;
                    quantityInput.value = quantity;
                    updateCartQuantity(cartId, quantity);
                }
            });
        });
        document.getElementById('checkout-button').addEventListener('click', checkout);
    });
