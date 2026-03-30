/* ============================================
   JACKPOKER.POKER — Main JavaScript
   ============================================ */

// ── Storage helpers (cookie-based, iframe-safe) ──
function jpGetTheme() {
  try {
    var m = document.cookie.match(/jp-theme=([^;]+)/);
    if (m) return m[1];
  } catch(e) {}
  return null;
}

function jpSetTheme(val) {
  try { document.cookie = 'jp-theme=' + val + ';path=/;max-age=31536000;SameSite=Lax'; } catch(e) {}
}

// ── Theme Toggle (runs immediately to prevent FOUC) ──
(function() {
  var theme = jpGetTheme() || 'dark';
  document.documentElement.setAttribute('data-theme', theme);
})();

document.addEventListener('DOMContentLoaded', function() {

  // ── Expired Events Auto-Hide ──
  // Elements with data-expires="YYYY-MM-DD" are hidden after that date passes (UTC end-of-day)
  (function() {
    var now = new Date();
    document.querySelectorAll('[data-expires]').forEach(function(el) {
      var expiryStr = el.getAttribute('data-expires');
      if (!expiryStr) return;
      // Parse as end-of-day UTC on the expiry date
      var parts = expiryStr.split('-');
      var expiryDate = new Date(Date.UTC(
        parseInt(parts[0], 10),
        parseInt(parts[1], 10) - 1,
        parseInt(parts[2], 10),
        23, 59, 59, 999
      ));
      if (now > expiryDate) {
        el.style.display = 'none';
        el.setAttribute('aria-hidden', 'true');
      }
    });
  })();

  // ── Theme Toggle Button ──
  var themeBtn = document.getElementById('themeToggle');
  if (themeBtn) {
    themeBtn.addEventListener('click', function() {
      var html = document.documentElement;
      var current = html.getAttribute('data-theme') || 'dark';
      var next = current === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      jpSetTheme(next);
      themeBtn.setAttribute('aria-label', 'Switch to ' + (next === 'dark' ? 'light' : 'dark') + ' mode');
    });
  }

  // ── Mobile Menu Toggle ──
  var menuToggle = document.getElementById('menuToggle');
  var mainNav = document.getElementById('mainNav');
  if (menuToggle && mainNav) {
    menuToggle.addEventListener('click', function() {
      var isOpen = mainNav.classList.toggle('open');
      menuToggle.textContent = isOpen ? '\u2715' : '\u2630';
      menuToggle.setAttribute('aria-expanded', isOpen);
    });
  }

  // ── Scroll Header Shadow ──
  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function() {
      if (window.scrollY > 10) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // ── Copy Promo Code (supports multiple buttons) ──
  document.querySelectorAll('[data-copy-code]').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var code = btn.getAttribute('data-copy-code') || 'WELCOME';
      var originalText = btn.textContent;

      navigator.clipboard.writeText(code).then(function() {
        btn.textContent = 'Copied!';
        setTimeout(function() { btn.textContent = originalText; }, 2000);
      }).catch(function() {
        var ta = document.createElement('textarea');
        ta.value = code;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        btn.textContent = 'Copied!';
        setTimeout(function() { btn.textContent = originalText; }, 2000);
      });
    });
  });

  // ── FAQ Accordion ──
  document.querySelectorAll('.faq-question').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var item = this.closest('.faq-item');
      var wasActive = item.classList.contains('active');

      // Close siblings only within same .faq-list
      var list = item.closest('.faq-list');
      if (list) {
        list.querySelectorAll('.faq-item').forEach(function(i) {
          i.classList.remove('active');
        });
      }

      if (!wasActive) {
        item.classList.add('active');
      }
    });
  });

  // ── Smooth Scroll for Anchor Links ──
  document.querySelectorAll('a[href^="#"]').forEach(function(link) {
    link.addEventListener('click', function(e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ── Scroll-triggered Reveal Animations ──
  var revealObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.fade-in-up, .feature-card, .card, .tournament-card, .news-card, .bonus-tier, .faq-item, .vip-tier-card, section > .container > .section-header').forEach(function(el) {
    el.classList.add('reveal-target');
    revealObserver.observe(el);
  });

  // ── Animated Stat Counters ──
  var statObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        animateStats(entry.target);
        statObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.3 });

  document.querySelectorAll('.hero-stats, .stats-bar').forEach(function(el) {
    statObserver.observe(el);
  });

  function animateStats(container) {
    container.querySelectorAll('.stat-value, .stat-number').forEach(function(el) {
      var text = el.textContent.trim();
      var match = text.match(/^([^0-9]*)([0-9,.]+)(.*)$/);
      if (!match) return;

      var prefix = match[1];
      var numStr = match[2].replace(/,/g, '');
      var suffix = match[3];
      var target = parseFloat(numStr);
      var hasDecimal = numStr.includes('.');
      var duration = 1800;
      var start = performance.now();

      function step(now) {
        var elapsed = now - start;
        var progress = Math.min(elapsed / duration, 1);
        // Ease out cubic
        var eased = 1 - Math.pow(1 - progress, 3);
        var current = target * eased;

        if (hasDecimal) {
          el.textContent = prefix + current.toFixed(1).replace(/\B(?=(\d{3})+(?!\d))/g, ',') + suffix;
        } else {
          el.textContent = prefix + Math.round(current).toLocaleString('en-US') + suffix;
        }

        if (progress < 1) {
          requestAnimationFrame(step);
        } else {
          el.textContent = text; // Restore exact original
        }
      }
      requestAnimationFrame(step);
    });
  }

  // ── Tilt effect on feature cards (subtle parallax) ──
  if (window.matchMedia('(pointer: fine)').matches) {
    document.querySelectorAll('.feature-card, .tournament-card, .mockup-main').forEach(function(card) {
      card.addEventListener('mousemove', function(e) {
        var rect = card.getBoundingClientRect();
        var x = (e.clientX - rect.left) / rect.width - 0.5;
        var y = (e.clientY - rect.top) / rect.height - 0.5;
        card.style.setProperty('--mouse-x', (x * 8).toFixed(1) + 'deg');
        card.style.setProperty('--mouse-y', (-y * 8).toFixed(1) + 'deg');
      });
      card.addEventListener('mouseleave', function() {
        card.style.removeProperty('--mouse-x');
        card.style.removeProperty('--mouse-y');
      });
    });
  }

  // ── Live "players online" pulse indicator ──
  var playerCountEl = document.querySelector('.live-players-count');
  if (playerCountEl) {
    var base = 847;
    function updatePlayerCount() {
      var variance = Math.floor(Math.random() * 120) - 60;
      var count = base + variance;
      playerCountEl.textContent = count.toLocaleString('en-US');
    }
    updatePlayerCount();
    setInterval(updatePlayerCount, 8000);
  }

});

// ── Legacy copy function (backward compat for inline onclick) ──
function copyPromo() {
  var code = 'WELCOME';
  navigator.clipboard.writeText(code).then(function() {
    var btn = document.querySelector('.promo-code-copy');
    if (btn) {
      var orig = btn.textContent;
      btn.textContent = 'Copied!';
      setTimeout(function() { btn.textContent = orig; }, 2000);
    }
  }).catch(function() {
    var ta = document.createElement('textarea');
    ta.value = code;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
  });
}

function copyPromoCode() {
  copyPromo();
}

// ── Language Switcher ──
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.lang-switcher').forEach(function(switcher) {
    var btn = switcher.querySelector('.lang-btn');
    if (!btn) return;

    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      switcher.classList.toggle('open');
      btn.setAttribute('aria-expanded', switcher.classList.contains('open'));
    });
  });

  // Close on outside click
  document.addEventListener('click', function() {
    document.querySelectorAll('.lang-switcher.open').forEach(function(s) {
      s.classList.remove('open');
      var b = s.querySelector('.lang-btn');
      if (b) b.setAttribute('aria-expanded', 'false');
    });
  });

  // Close on Escape
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      document.querySelectorAll('.lang-switcher.open').forEach(function(s) {
        s.classList.remove('open');
        var b = s.querySelector('.lang-btn');
        if (b) b.setAttribute('aria-expanded', 'false');
      });
    }
  });
});
