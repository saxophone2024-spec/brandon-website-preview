/* Brandon Jinwoo Choi — v3 interactions */
(function () {
  'use strict';
  var doc = document.documentElement;
  var nav = document.getElementById('nav');

  /* 1. language */
  var langButtons = document.querySelectorAll('[data-lang-btn]');
  function setLang(lang) {
    lang = lang === 'en' ? 'en' : 'ko';
    doc.dataset.lang = lang;
    doc.lang = lang;
    try { localStorage.setItem('bjc-lang', lang); } catch (e) {}
    langButtons.forEach(function (b) {
      var on = b.dataset.langBtn === lang;
      b.classList.toggle('is-on', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
  }
  langButtons.forEach(function (b) { b.addEventListener('click', function () { setLang(b.dataset.langBtn); }); });
  setLang(doc.dataset.lang || 'ko');

  /* 2. nav + active section + floating cta */
  var links = document.querySelectorAll('.nav__link');
  var sections = ['about', 'booking', 'schedule', 'epk', 'media', 'contact']
    .map(function (id) { return document.getElementById(id); }).filter(Boolean);
  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (nav) nav.classList.toggle('is-solid', y > 12);
    var current = '';
    var mid = y + window.innerHeight * 0.35;
    sections.forEach(function (s) { if (s.offsetTop <= mid) current = s.id; });
    links.forEach(function (l) { l.classList.toggle('is-active', l.dataset.sec === current); });
    var cta = document.getElementById('mobile-cta');
    var contact = document.getElementById('contact');
    if (cta) {
      var show = y > window.innerHeight * 0.55;
      if (contact) { var r = contact.getBoundingClientRect(); if (r.top < window.innerHeight * 0.98) show = false; }
      cta.classList.toggle('is-on', show);
    }
  }
  var ticking = false;
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; requestAnimationFrame(function () { onScroll(); ticking = false; }); }
  }, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();

  // hide floating CTA while typing in the form
  var formEl = document.getElementById('book-form');
  if (formEl && window.matchMedia('(max-width: 900px)').matches) {
    formEl.addEventListener('focusin', function () {
      var c = document.getElementById('mobile-cta');
      if (c) c.classList.remove('is-on');
    });
  }

  /* 3. mobile menu */
  var burger = document.querySelector('.nav__burger');
  function closeMenu() {
    document.body.classList.remove('menu-open');
    if (burger) { burger.setAttribute('aria-expanded', 'false'); burger.setAttribute('aria-label', 'Menu'); }
  }
  if (burger) {
    burger.addEventListener('click', function () {
      var open = document.body.classList.toggle('menu-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Menu');
    });
  }
  document.querySelectorAll('.menu a').forEach(function (a) { a.addEventListener('click', closeMenu); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMenu(); });
  window.addEventListener('resize', function () { if (window.innerWidth > 900) closeMenu(); });

  /* 4. reveal */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.06 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* 5. EPK tabs */
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.tab'));
  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        var p = document.getElementById(t.getAttribute('aria-controls'));
        if (p) p.hidden = !on;
      });
    });
    tab.addEventListener('keydown', function (e) {
      var i = tabs.indexOf(tab), next = null;
      if (e.key === 'ArrowRight') next = tabs[(i + 1) % tabs.length];
      if (e.key === 'ArrowLeft') next = tabs[(i - 1 + tabs.length) % tabs.length];
      if (next) { e.preventDefault(); next.focus(); next.click(); }
    });
  });

  /* 6. copy */
  document.querySelectorAll('.copy-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var src = document.getElementById(btn.dataset.copy);
      if (!src) return;
      var text = src.innerText.replace(/\s+\n/g, '\n').trim();
      var done = function () {
        var old = btn.textContent;
        btn.textContent = 'Copied ✓';
        btn.classList.add('is-done');
        setTimeout(function () { btn.textContent = old; btn.classList.remove('is-done'); }, 1800);
      };
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(done, function () { fallback(text, done); });
      } else { fallback(text, done); }
    });
  });
  function fallback(text, done) {
    var ta = document.createElement('textarea');
    ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); done(); } catch (e) {}
    document.body.removeChild(ta);
  }

  /* 7. programme card → select */
  var programSelect = document.getElementById('f-program');
  document.querySelectorAll('[data-program]').forEach(function (a) {
    a.addEventListener('click', function () {
      if (!programSelect) return;
      var v = a.dataset.program;
      var exists = Array.prototype.some.call(programSelect.options, function (o) { return o.value === v; });
      if (exists) programSelect.value = v;
    });
  });

  /* 8. form → mailto */
  var form = document.getElementById('book-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var data = new FormData(form);
      var name = (data.get('name') || '').toString().trim();
      var email = (data.get('email') || '').toString().trim();
      if (!name || !email) {
        var f = !name ? document.getElementById('f-name') : document.getElementById('f-email');
        if (f) f.focus();
        return;
      }
      var opt = programSelect && programSelect.selectedOptions[0];
      var ko = doc.dataset.lang === 'ko';
      var label = opt ? (ko ? opt.dataset.ko : opt.dataset.en) || opt.textContent.trim() : '';
      var subject = (ko ? '[섭외 문의] ' : '[Booking enquiry] ') + (label || '') + ' — ' + name;
      var lines = [
        (ko ? '이름: ' : 'Name: ') + name,
        (ko ? '소속: ' : 'Organisation: ') + ((data.get('org') || '').toString().trim() || '-'),
        (ko ? '이메일: ' : 'Email: ') + email,
        (ko ? '프로그램: ' : 'Programme: ') + (label || '-'),
        (ko ? '희망 일자: ' : 'Preferred date: ') + ((data.get('date') || '').toString().trim() || '-'),
        '',
        (data.get('message') || '').toString().trim(),
        '',
        '— brandonjinwoochoi.com'
      ];
      window.location.href = 'mailto:admin@mosphere.org?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'));
      form.classList.add('is-sent');
    });
  }

  /* 9. year */
  var y = document.getElementById('year');
  if (y) y.textContent = String(new Date().getFullYear());

  /* 10. schedule — drop dates that have already passed from "Upcoming" */
  var upcoming = document.getElementById('sched-upcoming');
  if (upcoming) {
    var today = new Date();
    today.setHours(0, 0, 0, 0);
    var kept = [];
    Array.prototype.slice.call(upcoming.querySelectorAll('.sched-row')).forEach(function (li) {
      var iso = li.getAttribute('data-date');
      if (!iso) { kept.push(li); return; }
      var p = iso.split('-');
      var dt = new Date(+p[0], +p[1] - 1, +p[2]);
      if (dt < today) {
        if (li.parentNode) li.parentNode.removeChild(li);
      } else {
        kept.push(li);
      }
    });
    var flag = upcoming.querySelector('.sched-row__flag');
    if (flag && flag.parentNode) flag.parentNode.removeChild(flag);
    if (kept.length) {
      var next = document.createElement('span');
      next.className = 'sched-row__flag';
      next.textContent = 'Next';
      kept[0].appendChild(next);
    }
    var count = document.getElementById('sched-count');
    if (count) {
      var koLabel = count.querySelector('.ko');
      var enLabel = count.querySelector('.en');
      count.textContent = kept.length + ' ';
      if (koLabel) count.appendChild(koLabel);
      if (enLabel) count.appendChild(enLabel);
    }
    var emptyNote = document.getElementById('sched-empty');
    if (!kept.length) {
      upcoming.hidden = true;
      if (emptyNote) emptyNote.hidden = false;
    }
  }
})();
