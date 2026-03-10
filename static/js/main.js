/* ============================================================
   RailBook — Main JavaScript
   ============================================================ */

// ── Flash Message Auto-Dismiss ────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
  const alerts = document.querySelectorAll('.alert.fade');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 5000); // 5 seconds
  });
});

// ── Show / Hide Password Toggle ───────────────────────────────
function togglePwd(inputId, btn) {
  const input = document.getElementById(inputId);
  if (!input) return;
  const icon = btn.querySelector('i');
  if (input.type === 'password') {
    input.type = 'text';
    icon.className = 'bi bi-eye-slash';
  } else {
    input.type = 'password';
    icon.className = 'bi bi-eye';
  }
}

// ── Confirm Action ────────────────────────────────────────────
function confirmAction(message) {
  return window.confirm(message);
}

// ── Active Nav Link Highlighting ──────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
  const links = document.querySelectorAll('#mainNav .nav-link');
  const current = window.location.pathname;
  links.forEach(function (link) {
    if (link.getAttribute('href') === current) {
      link.classList.add('active');
    }
  });
});
