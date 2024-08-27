// wishlist.js

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.remove-form').forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const form = this;
            const listItem = form.closest('.wishlist-item');

            // Send AJAX request to remove item
            fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            }).then(response => {
                if (response.ok) {
                    // Apply the animation
                    listItem.classList.add('hidden');
                    // Wait for the animation to complete
                    setTimeout(() => {
                        listItem.remove();
                        // Optionally, if the list is empty, show the empty message
                        if (document.querySelectorAll('.wishlist-item').length === 1) {
                            document.querySelector('.wishlist-item.empty').style.display = 'block';
                        }
                    }, 300); // Match the duration of the CSS transition
                }
            }).catch(error => {
                console.error('Error:', error);
            });
        });
    });
});
