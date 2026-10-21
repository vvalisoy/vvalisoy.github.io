// Section entrances: each [data-reveal] rises once, staggered by its order within its section.
(() => {
  const targets = [...document.querySelectorAll('[data-reveal]')];
  const bySection = new Map();
  for (const el of targets) {
    const host = el.closest('section, footer') || document.body;
    const n = bySection.get(host) || 0;
    el.style.setProperty('--i', Math.min(n, 8));
    bySection.set(host, n + 1);
  }
  document.querySelectorAll('.work__names .frame').forEach((f, i) => f.style.setProperty('--f', i));

  if (!('IntersectionObserver' in window)) { targets.forEach((el) => el.classList.add('is-in')); return; }
  const io = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.add('is-in');
      io.unobserve(entry.target);
    }
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 });
  targets.forEach((el) => io.observe(el));
  window.addEventListener('load', () => setTimeout(() => {
    targets.forEach((el) => { const r = el.getBoundingClientRect(); if (r.top < innerHeight && r.bottom > 0) el.classList.add('is-in'); });
  }, 2500));
})();

// Products: without script all four stand stacked; with it the tabs swap one plate at a time.
(() => {
  const products = [...document.querySelectorAll('[data-product]')];
  if (!products.length) return;
  const show = (id, focus) => {
    for (const p of products) {
      const on = p.id === id;
      p.hidden = !on;
      p.classList.toggle('is-shown', on);
      if (on && focus) p.querySelector(`.tabs a[href="#${id}"]`)?.focus({ preventScroll: true });
    }
  };
  show(products[0].id, false);
  products.forEach((p) => p.classList.remove('is-shown'));

  document.querySelectorAll('.products .tabs a').forEach((tab) => {
    tab.addEventListener('click', (e) => {
      e.preventDefault();
      show(tab.getAttribute('href').slice(1), true);
    });
    tab.addEventListener('keydown', (e) => {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      e.preventDefault();
      const i = products.findIndex((p) => !p.hidden);
      const next = products[(i + (e.key === 'ArrowRight' ? 1 : products.length - 1)) % products.length];
      show(next.id, true);
    });
  });
})();

// The live line: Vali's local time, and how far it is from the visitor's.
(() => {
  const row = document.querySelector('[data-clock]');
  if (!row) return;
  const tz = row.dataset.tz;
  const timeEl = row.querySelector('[data-clock-time]');
  const noteEl = row.querySelector('[data-clock-note]');
  const fmt = (zone) => new Intl.DateTimeFormat('en-GB', { hour: '2-digit', minute: '2-digit', timeZone: zone }).format(new Date());
  const offset = (zone) => {
    const now = new Date();
    const local = new Date(now.toLocaleString('en-US', { timeZone: zone }));
    return Math.round((local - new Date(now.toLocaleString('en-US'))) / 36e5 * 2) / 2;
  };
  const hour = () => Number(new Intl.DateTimeFormat('en-GB', { hour: 'numeric', hourCycle: 'h23', timeZone: tz }).format(new Date()));

  const tick = () => {
    timeEl.textContent = `, ${fmt(tz)}`;
    const diff = offset(tz);
    const h = hour();
    const state = h >= 9 && h < 19 ? 'working hours there' : h >= 19 && h < 24 ? 'evening there' : 'night there';
    const rel = diff === 0 ? 'Same time as you'
      : `${Math.abs(diff)} hour${Math.abs(diff) === 1 ? '' : 's'} ${diff > 0 ? 'ahead of' : 'behind'} you`;
    noteEl.textContent = `${rel}, ${state}. Replies usually come within a day.`;
  };
  tick();
  setInterval(tick, 15000);
})();

// The Baku clip plays only for visitors who have not asked for less motion; otherwise the poster stays.
(() => {
  const video = document.querySelector('.places video');
  if (!video || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const io = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting) video.play().catch(() => {}); else video.pause();
  });
  io.observe(video);
})();
