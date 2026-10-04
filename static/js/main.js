// DK Fashions — small interactions
(function () {
  // Mobile nav toggle
  var toggle = document.getElementById('navToggle');
  var header = document.getElementById('siteHeader');
  if (toggle && header) {
    toggle.addEventListener('click', function () {
      header.classList.toggle('open');
    });
  }

  // Hero video: some browsers defer autoplay — nudge it, and retry on any interaction
  var heroVid = document.querySelector('.hero-media');
  if (heroVid) {
    var tryPlay = function () {
      var pr = heroVid.play();
      if (pr && pr.catch) pr.catch(function () { /* blocked until interaction */ });
    };
    tryPlay();
    heroVid.addEventListener('loadeddata', tryPlay);
    document.addEventListener('visibilitychange', function () { if (!document.hidden) tryPlay(); });
    ['pointerdown', 'touchstart', 'keydown', 'scroll'].forEach(function (evt) {
      window.addEventListener(evt, tryPlay, { once: true, passive: true });
    });
  }

  // Header lifts on scroll
  if (header) {
    var onScroll = function () {
      header.classList.toggle('scrolled', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // Scroll-reveal animations
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }
  // Safety net: never leave content hidden if the observer misses something.
  setTimeout(function () {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }, 2500);

  // Newsletter (front-end only)
  document.querySelectorAll('.news-form').forEach(function (form) {
    form.addEventListener('submit', function () {
      var thanks = form.parentElement.querySelector('.news-thanks');
      form.style.display = 'none';
      if (thanks) thanks.hidden = false;
    });
  });

  // Auto-dismiss toasts
  var box = document.getElementById('messages');
  if (box) {
    setTimeout(function () {
      Array.prototype.forEach.call(box.children, function (t) {
        t.style.transition = 'opacity .4s, transform .4s';
        t.style.opacity = '0';
        t.style.transform = 'translateX(30px)';
      });
      setTimeout(function () { box.remove(); }, 500);
    }, 4200);
  }

  // Quantity steppers
  document.querySelectorAll('[data-qty]').forEach(function (box) {
    var input = box.querySelector('input');
    box.querySelectorAll('button').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var step = btn.dataset.step === 'up' ? 1 : -1;
        var v = Math.max(1, (parseInt(input.value, 10) || 1) + step);
        input.value = v;
        if (box.dataset.autosubmit) box.closest('form').submit();
      });
    });
  });

  // Size selection (visual only) + fill hidden field
  document.querySelectorAll('.size-row').forEach(function (row) {
    var hidden = document.querySelector('#selectedSize');
    row.querySelectorAll('.size-pill').forEach(function (pill) {
      pill.addEventListener('click', function () {
        row.querySelectorAll('.size-pill').forEach(function (p) { p.classList.remove('sel'); });
        pill.classList.add('sel');
        if (hidden) hidden.value = pill.textContent.trim();
      });
    });
  });
})();
