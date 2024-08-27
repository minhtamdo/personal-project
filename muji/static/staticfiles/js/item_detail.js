document.addEventListener('DOMContentLoaded', function() {
    let selectedColor = '';
    let selectedSize = '';

    function updatePrice() {
        let priceDisplay = document.getElementById('price-display');
        let price = 0;

        document.querySelectorAll('.product-option').forEach(function(option) {
            if (option.dataset.color === selectedColor && option.dataset.size === selectedSize) {
                price = parseFloat(option.dataset.price);
            }
        });

        priceDisplay.textContent = 'Price: $' + price.toFixed(2);
    }

    function setActiveButton(buttonGroup, selectedValue) {
        buttonGroup.querySelectorAll('button').forEach(function(button) {
            if (button.dataset.value === selectedValue) {
                button.classList.add('active');
            } else {
                button.classList.remove('active');
            }
        });
    }

    document.querySelectorAll('.color-button').forEach(function(button) {
        button.addEventListener('click', function() {
            selectedColor = this.dataset.value;
            setActiveButton(document.querySelector('.button-group.colors'), selectedColor);
            updatePrice();
            document.getElementById('color-input').value = selectedColor;
        });
    });

    document.querySelectorAll('.size-button').forEach(function(button) {
        button.addEventListener('click', function() {
            selectedSize = this.dataset.value;
            setActiveButton(document.querySelector('.button-group.sizes'), selectedSize);
            updatePrice();
            document.getElementById('size-input').value = selectedSize;
        });
    });
});