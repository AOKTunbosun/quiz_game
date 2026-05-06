// Topics Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
  
  // Add click event to topic cards
  const topicCards = document.querySelectorAll('.topic-card');
  
  topicCards.forEach(card => {
    card.addEventListener('click', function(e) {
      // Don't trigger if clicking on the actual link
      if (e.target.tagName !== 'A' && !e.target.closest('.btn-view')) {
        const link = this.querySelector('.btn-view');
        if (link && link.href) {
          window.location.href = link.href;
        }
      }
    });
  });
  
});