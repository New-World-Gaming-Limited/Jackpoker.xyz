// Mobile menu toggle
(function() {
  const toggle = document.getElementById('mobileToggle');
  const nav = document.getElementById('mobileNav');
  if (toggle && nav) {
    toggle.addEventListener('click', function() {
      const isOpen = nav.classList.contains('open');
      nav.classList.toggle('open');
      toggle.classList.toggle('open');
      toggle.setAttribute('aria-expanded', !isOpen);
    });
  }
})();

// Theme toggle
(function() {
  const html = document.documentElement;
  let theme = 'dark'; // default
  html.setAttribute('data-theme', theme);

  // Create theme toggle button
  const btn = document.createElement('button');
  btn.className = 'theme-toggle';
  btn.setAttribute('data-theme-toggle', '');
  btn.setAttribute('aria-label', 'Switch to light mode');
  btn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>';
  document.body.appendChild(btn);

  btn.addEventListener('click', function() {
    theme = theme === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', theme);
    btn.setAttribute('aria-label', 'Switch to ' + (theme === 'dark' ? 'light' : 'dark') + ' mode');
    btn.innerHTML = theme === 'dark'
      ? '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>'
      : '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  });
})();

// Copy promo code
function copyPromo() {
  const code = 'WELCOME';
  navigator.clipboard.writeText(code).then(function() {
    const btn = document.querySelector('.btn-copy');
    if (btn) {
      const original = btn.textContent;
      btn.textContent = 'Copied!';
      btn.style.background = '#22C55E';
      setTimeout(function() {
        btn.textContent = original;
        btn.style.background = '';
      }, 2000);
    }
  }).catch(function() {
    // Fallback for clipboard API
    const textarea = document.createElement('textarea');
    textarea.value = code;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
  });
}

// FAQ accordion
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.faq-question').forEach(function(btn) {
    btn.addEventListener('click', function() {
      const item = this.closest('.faq-item');
      const wasOpen = item.classList.contains('open');
      // Close all
      document.querySelectorAll('.faq-item').forEach(function(i) {
        i.classList.remove('open');
      });
      // Toggle clicked
      if (!wasOpen) {
        item.classList.add('open');
      }
    });
  });
});

// Scroll header shadow
(function() {
  const header = document.getElementById('header');
  if (header) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 10) {
        header.style.boxShadow = '0 4px 16px rgba(0,0,0,0.3)';
      } else {
        header.style.boxShadow = 'none';
      }
    });
  }
})();

// Promo code page copy
function copyPromoCode() {
  const code = 'WELCOME';
  const feedback = document.getElementById('copyFeedback');
  navigator.clipboard.writeText(code).then(function() {
    if (feedback) {
      feedback.textContent = 'Copied to clipboard!';
      setTimeout(function() { feedback.textContent = ''; }, 3000);
    }
  }).catch(function() {
    const textarea = document.createElement('textarea');
    textarea.value = code;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    if (feedback) {
      feedback.textContent = 'Copied to clipboard!';
      setTimeout(function() { feedback.textContent = ''; }, 3000);
    }
  });
}
