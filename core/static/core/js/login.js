// Password visibility toggle
const togglePassword = document.getElementById('togglePassword');
const passwordInput = document.getElementById('password');

if (togglePassword && passwordInput) {
  togglePassword.addEventListener('click', function() {
    // Toggle password type
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
    
    // Toggle eye icon
    const icon = this.querySelector('i');
    icon.classList.toggle('fa-eye');
    icon.classList.toggle('fa-eye-slash');
  });
}

// Form validation
const loginForm = document.getElementById('loginForm');

if (loginForm) {
  loginForm.addEventListener('submit', function(e) {
    const email = document.getElementById('email');
    const password = document.getElementById('password');
    
    // Basic email validation
    if (email && email.value) {
      const emailRegex = /^[^\s@]+@([^\s@]+\.)+[^\s@]+$/;
      if (!emailRegex.test(email.value)) {
        e.preventDefault();
        alert('Please enter a valid email address');
        email.focus();
        return false;
      }
    }
    
    // Check if password is empty
    if (password && !password.value) {
      e.preventDefault();
      alert('Please enter your password');
      password.focus();
      return false;
    }
    
    return true;
  });
}

// Enter key submit handling
if (passwordInput) {
  passwordInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      if (loginForm) {
        loginForm.dispatchEvent(new Event('submit'));
      }
    }
  });
}