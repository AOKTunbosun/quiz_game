// Profile Settings JavaScript
document.addEventListener('DOMContentLoaded', function() {
  
  // Tab switching
  const sidebarLinks = document.querySelectorAll('.sidebar-link');
  const tabContents = document.querySelectorAll('.tab-content');
  
  sidebarLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      
      // Remove active class from all links
      sidebarLinks.forEach(l => l.classList.remove('active'));
      
      // Add active class to clicked link
      this.classList.add('active');
      
      // Get tab to show
      const tabId = this.getAttribute('data-tab');
      
      // Hide all tab contents
      tabContents.forEach(content => content.classList.remove('active'));
      
      // Show selected tab content
      const activeTab = document.getElementById(`${tabId}-tab`);
      if (activeTab) {
        activeTab.classList.add('active');
      }
    });
  });
  
  // Password strength checker
  const newPassword = document.getElementById('newPassword');
  const confirmPassword = document.getElementById('confirmPassword');
  const passwordStrengthDiv = document.getElementById('passwordStrength');
  const passwordMatchDiv = document.getElementById('passwordMatch');
  
  if (newPassword) {
    newPassword.addEventListener('input', function() {
      const password = this.value;
      let strength = 0;
      let message = '';
      let strengthClass = '';
      
      if (password.length > 0) {
        if (password.length >= 8) strength++;
        if (password.length >= 12) strength++;
        if (/[a-z]/.test(password)) strength++;
        if (/[A-Z]/.test(password)) strength++;
        if (/[0-9]/.test(password)) strength++;
        if (/[^a-zA-Z0-9]/.test(password)) strength++;
        
        if (strength <= 2) {
          message = 'Weak password';
          strengthClass = 'weak';
        } else if (strength <= 4) {
          message = 'Medium password';
          strengthClass = 'medium';
        } else {
          message = 'Strong password!';
          strengthClass = 'strong';
        }
        
        passwordStrengthDiv.textContent = message;
        passwordStrengthDiv.className = `password-strength ${strengthClass}`;
      } else {
        passwordStrengthDiv.textContent = '';
      }
      
      if (confirmPassword && confirmPassword.value) {
        checkPasswordMatch();
      }
    });
  }
  
  function checkPasswordMatch() {
    if (newPassword && confirmPassword) {
      if (newPassword.value === confirmPassword.value && newPassword.value !== '') {
        passwordMatchDiv.textContent = '✓ Passwords match';
        passwordMatchDiv.className = 'password-match match';
      } else if (confirmPassword.value !== '') {
        passwordMatchDiv.textContent = '✗ Passwords do not match';
        passwordMatchDiv.className = 'password-match mismatch';
      } else {
        passwordMatchDiv.textContent = '';
      }
    }
  }
  
  if (confirmPassword) {
    confirmPassword.addEventListener('input', checkPasswordMatch);
  }
  
  // Phone number formatting
  const phoneInputs = document.querySelectorAll('input[type="tel"]');
  phoneInputs.forEach(input => {
    input.addEventListener('input', function(e) {
      this.value = this.value.replace(/[^0-9]/g, '');
      if (this.value.length > 11) {
        this.value = this.value.slice(0, 11);
      }
    });
  });
  
});