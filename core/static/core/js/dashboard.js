
// Dashboard JavaScript (minimal - just for interactivity)

document.addEventListener('DOMContentLoaded', function () {

    // Add hover effects or any client-side interactivity
    const actionCards = document.querySelectorAll('.action-card');

    actionCards.forEach(card => {
        card.addEventListener('click', function (e) {
            // Don't trigger if clicking on the actual link
            if (e.target.tagName !== 'A') {
                const link = this.querySelector('.action-btn');
                if (link && link.href) {
                    window.location.href = link.href;
                }
            }
        });
    });

    // Optional: Add a simple greeting message based on time of day
    const welcomeText = document.querySelector('.welcome-text p');
    if (welcomeText) {
        const hour = new Date().getHours();
        let greeting = '';

        if (hour < 12) {
            greeting = 'Good morning! 🌅 Ready to learn?';
        } else if (hour < 17) {
            greeting = 'Good afternoon! ☀️ Let\'s study Computer Studies!';
        } else {
            greeting = 'Good evening! 🌙 Perfect time to take a quiz!';
        }

        welcomeText.textContent = greeting;
    }

    // Optional: Add click tracking for quiz items (can be removed if not needed)
    const quizItems = document.querySelectorAll('.quiz-item');
    quizItems.forEach(item => {
        item.addEventListener('click', function (e) {
            if (e.target.tagName !== 'A') {
                const link = this.querySelector('.btn-start');
                if (link && link.href) {
                    window.location.href = link.href;
                }
            }
        });
    });

    // Recommended items click tracking
    const recommendedItems = document.querySelectorAll('.recommended-item');
    recommendedItems.forEach(item => {
        item.addEventListener('click', function (e) {
            if (e.target.tagName !== 'A') {
                const link = this.querySelector('.btn-recommended');
                if (link && link.href) {
                    window.location.href = link.href;
                }
            }
        });
    });
})
