document.addEventListener("DOMContentLoaded", function () {
    var navbar = document.getElementById('navbar');
    var logo = document.getElementById('logo-image');
    var lastScrollTop = 0; // Last scroll position
    var scrollThreshold = 50; // Amount of scroll to trigger fixed positioning
    var minScreenWidth = 768; // Minimum screen width to apply the effect

    window.addEventListener('scroll', function () {
        var currentScrollTop = window.scrollY;
        var screenWidth = window.innerWidth;

        if (screenWidth > minScreenWidth) {
            // Apply effects only if screen width is larger than minScreenWidth
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
        } else {
            // If screen width is less than or equal to minScreenWidth, remove effects
            navbar.classList.remove('fixed');
            navbar.classList.remove('scrolled');
            logo.style.opacity = 1; // Ensure the logo remains visible
        }

        lastScrollTop = currentScrollTop; // Update last scroll position
    });
});



document.addEventListener("DOMContentLoaded", function () {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const collapseElement = document.querySelector('.collapse');

    navbarToggler.addEventListener('click', function () {
        const isExpanded = navbarToggler.getAttribute('aria-expanded') === 'true';
        navbarToggler.classList.toggle('is-open', !isExpanded);
    });

    // Close menu if clicked outside
    document.addEventListener('click', function (event) {
        const isClickInside = collapseElement.contains(event.target) || navbarToggler.contains(event.target);

        if (!isClickInside && collapseElement.classList.contains('show')) {
            navbarToggler.click(); // This will toggle the menu off
        }
    });
});



