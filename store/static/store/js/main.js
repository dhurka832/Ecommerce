/* ==========================================================================
   LUXE STORE — MAIN JAVASCRIPT
   Pure Vanilla JS (No Bootstrap, No jQuery)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {
  // 1. Mobile Menu Drawer Toggle
  const mobileToggle = document.getElementById('mobileMenuToggle');
  const mobileMenu = document.getElementById('mobileMenu');

  if (mobileToggle && mobileMenu) {
    mobileToggle.addEventListener('click', function () {
      mobileMenu.classList.toggle('active');
      const icon = mobileToggle.querySelector('i');
      if (icon) {
        if (mobileMenu.classList.contains('active')) {
          icon.classList.remove('fa-bars');
          icon.classList.add('fa-times');
        } else {
          icon.classList.remove('fa-times');
          icon.classList.add('fa-bars');
        }
      }
    });
  }

  // 2. Toast Alert Auto-Dismiss & Manual Close
  const toastAlerts = document.querySelectorAll('.luxe-toast');
  toastAlerts.forEach(function (toast) {
    const closeBtn = toast.querySelector('.toast-close-btn');
    if (closeBtn) {
      closeBtn.addEventListener('click', function () {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(50px)';
        setTimeout(function () {
          toast.remove();
        }, 300);
      });
    }

    // Auto dismiss after 5 seconds
    setTimeout(function () {
      if (toast && toast.parentElement) {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(50px)';
        setTimeout(function () {
          toast.remove();
        }, 300);
      }
    }, 5000);
  });

  // 3. Interactive Checkout Virtual Credit Card Sync & Test Card Autofill
  const cardInput = document.getElementById('cardNumberInput');
  const monthInput = document.getElementById('expMonthInput');
  const yearInput = document.getElementById('expYearInput');
  const cvcInput = document.getElementById('cvcInput');

  const cardDisplayNum = document.getElementById('displayCardNumber');
  const cardDisplayExp = document.getElementById('displayCardExpiry');

  if (cardInput && cardDisplayNum) {
    cardInput.addEventListener('input', function (e) {
      let val = e.target.value.replace(/\D/g, '').substring(0, 16);
      let formatted = '';
      for (let i = 0; i < val.length; i++) {
        if (i > 0 && i % 4 === 0) formatted += ' ';
        formatted += val[i];
      }
      e.target.value = formatted;

      if (formatted.length > 0) {
        let display = formatted;
        while (display.length < 19) {
          if (display.length === 4 || display.length === 9 || display.length === 14) {
            display += ' ';
          } else {
            display += '•';
          }
        }
        cardDisplayNum.textContent = display;
      } else {
        cardDisplayNum.textContent = '•••• •••• •••• ••••';
      }
    });
  }

  function updateExpiryDisplay() {
    if (!cardDisplayExp) return;
    const mm = monthInput && monthInput.value ? String(monthInput.value).padStart(2, '0') : 'MM';
    const yy = yearInput && yearInput.value ? String(yearInput.value).slice(-2) : 'YY';
    cardDisplayExp.textContent = mm + '/' + yy;
  }

  if (monthInput) monthInput.addEventListener('input', updateExpiryDisplay);
  if (yearInput) yearInput.addEventListener('input', updateExpiryDisplay);

  // Test card autofill chips
  const testChips = document.querySelectorAll('.test-chip');
  testChips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      const num = this.getAttribute('data-card');
      if (cardInput && num) {
        cardInput.value = num.replace(/(\d{4})/g, '$1 ').trim();
        if (cardDisplayNum) cardDisplayNum.textContent = cardInput.value;
      }
      if (monthInput) {
        monthInput.value = '12';
      }
      if (yearInput) {
        yearInput.value = '2028';
      }
      if (cvcInput) {
        cvcInput.value = '123';
      }
      updateExpiryDisplay();
      if (cardInput) cardInput.focus();
    });
  });

  // 4. Password Visibility Toggle on Auth Forms
  const togglePassBtns = document.querySelectorAll('.toggle-password-btn');
  togglePassBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      const targetInput = document.getElementById(this.getAttribute('data-target'));
      if (targetInput) {
        if (targetInput.type === 'password') {
          targetInput.type = 'text';
          this.innerHTML = '<i class="fa fa-eye-slash"></i>';
        } else {
          targetInput.type = 'password';
          this.innerHTML = '<i class="fa fa-eye"></i>';
        }
      }
    });
  });
});
