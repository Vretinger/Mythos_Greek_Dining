document.addEventListener("DOMContentLoaded", function () {
    var navbar = document.getElementById('navbar');
    var logo = document.getElementById('logo-image');
    var navbarPlaceholder = document.getElementById('navbar-placeholder');
    var lastScrollTop = 0; // Last scroll position
    var scrollThreshold = 50; // Amount of scroll to trigger fixed positioning

    window.addEventListener('scroll', function () {
        var currentScrollTop = window.scrollY;

        if (currentScrollTop > scrollThreshold) {
            // Scrolling past threshold
            navbar.classList.add('fixed');
            navbar.classList.add('scrolled');
        } else {
            // Less than threshold
            navbar.classList.remove('fixed');
            navbar.classList.remove('scrolled');
        }

        // Hide the logo before the navbar becomes fixed
        if (currentScrollTop > scrollThreshold - 50) {
            logo.style.opacity = 0; // Start hiding the logo
        } else {
            logo.style.opacity = 1; // Make sure the logo is visible at the top
        }

        lastScrollTop = currentScrollTop; // Update last scroll position
    });
});


