// Quiz Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
  
  const quizForm = document.getElementById('quizForm');
  const clearAllBtn = document.getElementById('clearAllBtn');
  
  // Clear all answers button
  if (clearAllBtn) {
    clearAllBtn.addEventListener('click', function() {
      if (confirm('Are you sure you want to clear all your answers?')) {
        const radioButtons = document.querySelectorAll('.option input[type="radio"]');
        radioButtons.forEach(radio => {
          radio.checked = false;
        });
      }
    });
  }
  
  // Form submission confirmation
  if (quizForm) {
    quizForm.addEventListener('submit', function(e) {
      // Check if all questions are answered
      const questions = document.querySelectorAll('.question-card');
      let allAnswered = true;
      let unansweredCount = 0;
      
      questions.forEach(question => {
        const selected = question.querySelector('input[type="radio"]:checked');
        if (!selected) {
          allAnswered = false;
          unansweredCount++;
          question.style.borderColor = 'rgba(231, 76, 60, 0.5)';
        } else {
          question.style.borderColor = '';
        }
      });
      
      if (!allAnswered) {
        e.preventDefault();
        const confirmSubmit = confirm(`You have ${unansweredCount} unanswered question(s). Are you sure you want to submit?`);
        if (!confirmSubmit) {
          return false;
        }
      }
      
      // Final confirmation
      const totalQuestions = questions.length;
      const finalConfirm = confirm(`You are about to submit your quiz. Total questions: ${totalQuestions}. Continue?`);
      
      if (!finalConfirm) {
        e.preventDefault();
        return false;
      }
      
      return true;
    });
  }
  
  // Auto-save indicator (optional - visual feedback when answer is selected)
  const radioButtons = document.querySelectorAll('.option input[type="radio"]');
  radioButtons.forEach(radio => {
    radio.addEventListener('change', function() {
      const questionCard = this.closest('.question-card');
      if (questionCard) {
        questionCard.style.borderColor = 'rgba(46, 204, 113, 0.5)';
        setTimeout(() => {
          questionCard.style.borderColor = '';
        }, 500);
      }
    });
  });
  
  // Show progress (answered count)
  function updateProgress() {
    const total = document.querySelectorAll('.question-card').length;
    const answered = document.querySelectorAll('.option input[type="radio"]:checked').length;
    
    // You can display this somewhere if needed
    console.log(`Progress: ${answered}/${total} answered`);
  }
  
  radioButtons.forEach(radio => {
    radio.addEventListener('change', updateProgress);
  });
  
});