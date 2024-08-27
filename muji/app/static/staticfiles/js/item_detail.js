document.addEventListener('DOMContentLoaded', function() {
    let selectedColor = '';
    let selectedSize = '';

    function updatePrice() {
        let priceDisplay = document.getElementById('price-display');
        let price = 0;
        let imageUrl = '';

        document.querySelectorAll('.product-option').forEach(function(option) {
            if (option.dataset.color === selectedColor && option.dataset.size === selectedSize) {
                price = parseFloat(option.dataset.price);
                imageUrl = option.dataset.image;
                updateImage(imageUrl);
                jumpToImage(imageUrl);
            }
        });

        priceDisplay.textContent = 'Price: ¥' + price.toFixed(2);
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

    function updateImage(imageUrl) {
        const imageElement = document.getElementById('item-image');
        if (imageUrl) {
            imageElement.src = imageUrl;
        } else {
            imageElement.src = imageElement.dataset.defaultImage;
        }
    }

    function jumpToImage(imageUrl) {
        const galleryImages = document.querySelectorAll('.gallery-image');
        galleryImages.forEach(img => {
            if (img.src === imageUrl) {
                img.scrollIntoView({ behavior: 'smooth', inline: 'center' });
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

    // Handle clicking on gallery images
    document.querySelectorAll('.gallery-image').forEach(image => {
        image.addEventListener('click', function() {
            updateImage(this.src); // Update the main image to the clicked gallery image
        });
    });

    // Initialize default image URL from the element's data attribute
    const itemImage = document.getElementById('item-image');
    if (itemImage) {
        itemImage.dataset.defaultImage = itemImage.src;
    }
});
document.addEventListener('DOMContentLoaded', () => {
    const slideWrap = document.getElementById('item-slide-wrap');
    const slides = document.querySelectorAll('.slide-item');
    const prevButton = document.getElementById('prev');
    const nextButton = document.getElementById('next');
    
    const itemsToShow = 3;
    const totalSlides = slides.length;
    const totalPages = Math.ceil(totalSlides / itemsToShow);
    let currentPage = 0;

    function updateSlidePosition() {
        const slideWidth = slides[0].offsetWidth * itemsToShow;
        slideWrap.style.transform = `translateX(-${currentPage * slideWidth}px)`;
    }

    function goToPrevSlide() {
        if (currentPage > 0) {
            currentPage--;
            updateSlidePosition();
        }
    }

    function goToNextSlide() {
        if (currentPage < totalPages - 1) {
            currentPage++;
            updateSlidePosition();
        }
    }

    prevButton.addEventListener('click', goToPrevSlide);
    nextButton.addEventListener('click', goToNextSlide);

    // Initialize slide position
    updateSlidePosition();
});


document.addEventListener('DOMContentLoaded', () => {
    const quantityInput = document.getElementById('quantity');
    const decreaseButton = document.getElementById('decrease');
    const increaseButton = document.getElementById('increase');

    let quantity = parseInt(quantityInput.value, 10);

    function updateQuantity() {
        quantityInput.value = quantity;
        decreaseButton.disabled = quantity <= 1;
    }

    decreaseButton.addEventListener('click', () => {
        if (quantity > 1) {
            quantity--;
            updateQuantity();
        }
    });

    increaseButton.addEventListener('click', () => {
        quantity++;
        updateQuantity();
    });

    // Initialize button state
    updateQuantity();
});

document.addEventListener('DOMContentLoaded', () => {
    const wishlistBtn = document.querySelector('.wishlist-btn');

    if (wishlistBtn) {
        wishlistBtn.addEventListener('click', async (event) => {
            event.preventDefault();
            const form = wishlistBtn.closest('form');
            const formData = new FormData(form);

            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                    }
                });

                if (response.ok) {
                    // Toggle button text based on the response or update UI accordingly
                    if (wishlistBtn.textContent === 'Add to Wishlist') {
                        wishlistBtn.textContent = 'Remove from Wishlist';
                    } else {
                        wishlistBtn.textContent = 'Add to Wishlist';
                    }
                } else {
                    console.error('Failed to update wishlist');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    }
});
