// Password strength checker
const passwordInput = document.getElementById('password');
const confirmPasswordInput = document.getElementById('confirmPassword');
const passwordStrengthDiv = document.getElementById('passwordStrength');
const passwordMatchDiv = document.getElementById('passwordMatch');

if (passwordInput) {
  passwordInput.addEventListener('input', function() {
    const password = this.value;
    let strength = 0;
    let message = '';
    let strengthClass = '';
    
    if (password.length > 0) {
      // Length check
      if (password.length >= 8) strength++;
      if (password.length >= 12) strength++;
      
      // Character variety checks
      if (/[a-z]/.test(password)) strength++;
      if (/[A-Z]/.test(password)) strength++;
      if (/[0-9]/.test(password)) strength++;
      if (/[^a-zA-Z0-9]/.test(password)) strength++;
      
      // Determine strength
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
    
    // Check password match if confirm has value
    if (confirmPasswordInput && confirmPasswordInput.value) {
      checkPasswordMatch();
    }
  });
}

// Password match checker
function checkPasswordMatch() {
  if (passwordInput && confirmPasswordInput) {
    const password = passwordInput.value;
    const confirm = confirmPasswordInput.value;
    
    if (confirm.length > 0) {
      if (password === confirm) {
        passwordMatchDiv.textContent = '✓ Passwords match';
        passwordMatchDiv.className = 'password-match match';
      } else {
        passwordMatchDiv.textContent = '✗ Passwords do not match';
        passwordMatchDiv.className = 'password-match mismatch';
      }
    } else {
      passwordMatchDiv.textContent = '';
    }
  }
}

if (confirmPasswordInput) {
  confirmPasswordInput.addEventListener('input', checkPasswordMatch);
}

// Form validation before submit
const signupForm = document.getElementById('signupForm');
if (signupForm) {
  signupForm.addEventListener('submit', function(e) {
    // Check if passwords match
    if (passwordInput && confirmPasswordInput) {
      if (passwordInput.value !== confirmPasswordInput.value) {
        e.preventDefault();
        alert('Passwords do not match. Please check and try again.');
        confirmPasswordInput.focus();
        return false;
      }
    }
    
    // Check password strength (optional - warn but allow)
    if (passwordInput && passwordInput.value.length < 6) {
      e.preventDefault();
      alert('Password should be at least 6 characters long for security.');
      passwordInput.focus();
      return false;
    }
    
    // Validate phone numbers (basic Nigerian format)
    const studentPhone = document.getElementById('studentPhone');
    const parentPhone = document.getElementById('parentPhone');
    const phoneRegex = /^0[789][01]\d{8}$/;
    
    if (studentPhone && studentPhone.value) {
      if (!phoneRegex.test(studentPhone.value)) {
        e.preventDefault();
        alert('Please enter a valid Nigerian phone number for the student (e.g., 08012345678)');
        studentPhone.focus();
        return false;
      }
    }
    
    if (parentPhone && parentPhone.value) {
      if (!phoneRegex.test(parentPhone.value)) {
        e.preventDefault();
        alert('Please enter a valid Nigerian phone number for the parent (e.g., 08012345678)');
        parentPhone.focus();
        return false;
      }
    }
    
    return true;
  });
}

// Phone number formatting (optional)
const phoneInputs = document.querySelectorAll('input[type="tel"]');
phoneInputs.forEach(input => {
  input.addEventListener('input', function(e) {
    // Remove any non-digit characters
    this.value = this.value.replace(/[^0-9]/g, '');
    
    // Limit to 11 digits
    if (this.value.length > 11) {
      this.value = this.value.slice(0, 11);
    }
  });
});

// Smooth select dropdown styling enhancement
const selectElements = document.querySelectorAll('select');
selectElements.forEach(select => {
  select.addEventListener('change', function() {
    if (this.value) {
      this.style.color = '#ffffff';
    }
  });
});