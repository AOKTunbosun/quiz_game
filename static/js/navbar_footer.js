// Wait for DOM to fully load
document.addEventListener('DOMContentLoaded', function () {

    // Mobile menu toggle functionality
    const mobileMenuBtn = document.getElementById('mobileMenu');
    const navLinks = document.querySelector('.nav-links');
    const navButtons = document.querySelector('.nav-buttons');

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function () {
            if (navLinks.style.display === 'flex') {
                navLinks.style.display = 'none';
                navButtons.style.display = 'none';
            } else {
                navLinks.style.display = 'flex';
                navButtons.style.display = 'flex';
                navLinks.style.flexDirection = 'column';
                navButtons.style.flexDirection = 'column';
                navLinks.style.position = 'absolute';
                navLinks.style.top = '70px';
                navLinks.style.left = '0';
                navLinks.style.width = '100%';
                navLinks.style.backgroundColor = '#0a0a0a';
                navLinks.style.padding = '1rem';
                navLinks.style.borderBottom = '1px solid rgba(243, 156, 18, 0.2)';

                navButtons.style.position = 'absolute';
                navButtons.style.top = '250px';
                navButtons.style.left = '0';
                navButtons.style.width = '100%';
                navButtons.style.backgroundColor = '#0a0a0a';
                navButtons.style.padding = '1rem';
                navButtons.style.gap = '0.5rem';
            }
        });
    }

    // Handle window resize - reset mobile menu styles
    window.addEventListener('resize', function () {
        if (window.innerWidth > 768) {
            if (navLinks) {
                navLinks.style.display = '';
                navLinks.style.position = '';
                navLinks.style.backgroundColor = '';
                navLinks.style.padding = '';
                navLinks.style.borderBottom = '';
            }
            if (navButtons) {
                navButtons.style.display = '';
                navButtons.style.position = '';
                navButtons.style.backgroundColor = '';
                navButtons.style.padding = '';
                navButtons.style.gap = '';
            }
        }
    });


    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add animation on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe feature cards and topic cards
    document.querySelectorAll('.feature-card, .topic-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });

    // Newsletter subscription (placeholder for backend integration)
    const newsletterBtn = document.querySelector('.newsletter-form button');
    if (newsletterBtn) {
        newsletterBtn.addEventListener('click', function () {
            const emailInput = document.querySelector('.newsletter-form input');
            if (emailInput && emailInput.value) {
                alert('Thank you for subscribing! You will receive updates soon.');
                emailInput.value = '';
            } else {
                alert('Please enter a valid email address.');
            }
        });
    }

    // Prevent form submission if newsletter form is inside a form (just in case)
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const emailInput = this.querySelector('input');
            if (emailInput && emailInput.value) {
                alert('Thank you for subscribing!');
                emailInput.value = '';
            }
        });
    }
});