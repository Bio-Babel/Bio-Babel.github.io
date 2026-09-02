/* ═══════════════════════════════════════════════════════════════════════════
   Bio-Babel — site behaviour. No dependencies, no build step.
   ═══════════════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ───────────────────────────────────────────────── nav: stick + burger ─ */
  var nav = $('#nav');
  var onScroll = function () { nav.classList.toggle('is-stuck', window.scrollY > 12); };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  var burger = $('#navBurger');
  var navLinks = $('#navLinks');
  burger.addEventListener('click', function () {
    var open = navLinks.classList.toggle('is-open');
    burger.setAttribute('aria-expanded', String(open));
  });
  navLinks.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') {
      navLinks.classList.remove('is-open');
      burger.setAttribute('aria-expanded', 'false');
    }
  });

  /* ─────────────────────────────────────────── nav: active section link ─ */
  var linkFor = {};
  $$('#navLinks a').forEach(function (a) {
    var href = a.getAttribute('href') || '';   /* page links (paper/, ../#why) are not sections */
    if (href.charAt(0) === '#' && href.length > 1) linkFor[href.slice(1)] = a;
  });
  var sections = Object.keys(linkFor)
    .map(function (id) { return document.getElementById(id); })
    .filter(Boolean);

  if (sections.length && 'IntersectionObserver' in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        $$('#navLinks a').forEach(function (a) { a.classList.remove('is-active'); });
        var a = linkFor[en.target.id];
        if (a) a.classList.add('is-active');
      });
    }, { rootMargin: '-45% 0px -50% 0px', threshold: 0 });
    sections.forEach(function (s) { spy.observe(s); });
  }

  /* ──────────────────────────────────────────────── reveal on first view ─ */
  var revealTargets = $$([
    '.section .eyebrow', '.section .h2', '.section .lede',
    '.card', '.lib', '.sys', '.zig', '.flow', '.split',
    '.join', '.filters', '.libs__note', '.closer__inner',
    '.paper-card', '.beyond__text'
  ].join(','));

  if (!reduced && 'IntersectionObserver' in window) {
    revealTargets.forEach(function (el) { el.classList.add('reveal'); });
    var revealer = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        var sibs = Array.prototype.slice.call(el.parentNode.children).indexOf(el);
        el.style.transitionDelay = Math.min(sibs, 6) * 55 + 'ms';
        el.classList.add('is-in');
        obs.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealTargets.forEach(function (el) { revealer.observe(el); });
  }

  /* ──────────────────────────────────────────────── stat counters ────── */
  var stats = $$('.stat b[data-count]');
  if (stats.length && 'IntersectionObserver' in window) {
    var counter = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        obs.unobserve(en.target);
        var el = en.target;
        var end = parseFloat(el.dataset.count);
        var pre = el.dataset.prefix || '';
        var suf = el.dataset.suffix || '';
        if (reduced || !end) { return; }
        var t0 = null, dur = 1100;
        var tick = function (ts) {
          if (t0 === null) t0 = ts;
          var p = Math.min((ts - t0) / dur, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          el.textContent = pre + Math.round(end * eased).toLocaleString('en-US') + suf;
          if (p < 1) requestAnimationFrame(tick);
        };
        el.textContent = pre + '0' + suf;
        requestAnimationFrame(tick);
      });
    }, { threshold: 0.5 });
    stats.forEach(function (s) { counter.observe(s); });
  }

  /* ──────────────────────────────────────────────────── copy to clipboard ─ */
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-copy]');
    if (!btn) return;
    var text = btn.dataset.copy;
    var done = function () {
      btn.classList.add('is-copied');
      setTimeout(function () { btn.classList.remove('is-copied'); }, 1600);
    };
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(done, function () {});
    } else {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.cssText = 'position:fixed;opacity:0';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); done(); } catch (err) {}
      document.body.removeChild(ta);
    }
  });

  /* ─────────────────────────────────────────────────────── the ziggurat ─ */
  var tiers = $$('#zigTower .zig__tier');
  var details = $$('#zigPanel .zig__detail');
  var selectTier = function (name) {
    tiers.forEach(function (t) { t.classList.toggle('is-on', t.dataset.tier === name); });
    details.forEach(function (d) { d.classList.toggle('is-on', d.dataset.tier === name); });
  };
  tiers.forEach(function (t) {
    t.addEventListener('click', function () { selectTier(t.dataset.tier); });
    t.addEventListener('mouseenter', function () { selectTier(t.dataset.tier); });
  });
  if (tiers.length) selectTier('foundation');

  /* ───────────────────────────────────────────────────── library filter ─ */
  var libs = $$('#libGrid .lib');
  $$('.filters__btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var f = btn.dataset.filter;
      $$('.filters__btn').forEach(function (b) {
        var on = b === btn;
        b.classList.toggle('is-active', on);
        b.setAttribute('aria-selected', String(on));
      });
      libs.forEach(function (lib) {
        lib.classList.toggle('is-hidden', f !== 'all' && lib.dataset.group !== f);
      });
    });
  });

})();
