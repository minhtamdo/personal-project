console.log('JS Loaded');
document.addEventListener('DOMContentLoaded', function() {
        // Get all elements with class 'material-symbols-outlined'
        var bookmarkHearts = document.querySelectorAll('.material-symbols-outlined');

        // Loop through each element
        bookmarkHearts.forEach(function(bookmarkHeart) {
            // Add role="button" accessibility
            bookmarkHeart.setAttribute('role', 'button');
            
            // Add click event listener to each element
            bookmarkHeart.addEventListener('click', function() {
                // Toggle color between current color and coral (#ff6347)
                var currentColor = bookmarkHeart.style.color || getComputedStyle(bookmarkHeart).color;
                var coralColor = '#ff6347';

                if (currentColor === '#3C3C43') {
                    bookmarkHeart.style.color = coralColor;
                } else {
                    bookmarkHeart.style.color = '#3C3C43';
                }
            });
        });
    });
