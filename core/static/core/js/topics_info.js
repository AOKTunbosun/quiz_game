// Topic Info Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
  
  // Optional: Add smooth scroll to quiz button
  const quizBtn = document.querySelector('.btn-start-quiz');
  
  if (quizBtn) {
    quizBtn.addEventListener('click', function(e) {
      // Just letting the link work normally
      // You can add analytics tracking here if needed
      console.log('Starting quiz for topic');
    });
  }
  
});