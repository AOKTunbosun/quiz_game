// Results Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
  
  // Filter functionality
  const filterBtns = document.querySelectorAll('.filter-btn');
  const resultRows = document.querySelectorAll('.result-row');
  
  filterBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      // Update active button
      filterBtns.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      
      const filter = this.getAttribute('data-filter');
      
      resultRows.forEach(row => {
        const score = parseFloat(row.getAttribute('data-score'));
        
        if (filter === 'all') {
          row.style.display = '';
        } else if (filter === 'pass') {
          row.style.display = score >= 50 ? '' : 'none';
        } else if (filter === 'fail') {
          row.style.display = score < 50 ? '' : 'none';
        }
      });
    });
  });
  
});

