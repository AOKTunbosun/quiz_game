// Subjects Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
  
  // Optional: Add click animation for subject card
  const subjectCard = document.querySelector('.subject-card');
  
  if (subjectCard) {
    subjectCard.addEventListener('click', function(e) {
      // Don't trigger if clicking on the actual link
      if (e.target.tagName !== 'A' && !e.target.closest('.btn-explore')) {
        const link = this.querySelector('.btn-explore');
        if (link && link.href) {
          window.location.href = link.href;
        }
      }
    });
  }
  
});