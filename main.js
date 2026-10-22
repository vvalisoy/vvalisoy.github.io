// vvalisoy — window manager, terminal, notes, photos, mail and clock for the desktop / home screen.
(() => {
  const phone = matchMedia('(max-width: 700px)');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const wins = new Map([...document.querySelectorAll('.win')].map((w) => [w.id, w]));
  let z = 100;
  let cascade = 0;

  // ---------- windows ----------

  const front = (win) => {
    for (const w of wins.values()) w.classList.toggle('is-front', w === win);
    win.style.zIndex = ++z;
  };

  const place = (win) => {
    if (win.dataset.placed || phone.matches) return;
    const r = win.getBoundingClientRect();
    const top = 28;
    const w = r.width, h = r.height;
    const step = (cascade++ % 6) * 26;
    const x = Math.max(8, Math.min(innerWidth - w - 8, (innerWidth - w) / 2 - 80 + step));
    const y = Math.max(top + 8, Math.min(innerHeight - h - 90, (innerHeight - h) / 2 - 40 + step));
    win.style.left = `${x}px`;
    win.style.top = `${y}px`;
    win.dataset.placed = '1';
  };

  const running = () => {
    document.querySelectorAll('.app[data-open]').forEach((a) => {
      a.classList.toggle('is-running', wins.get(a.dataset.open)?.classList.contains('is-open'));
    });
  };

  const open = (id) => {
    const win = wins.get(id);
    if (!win) return;
    win.classList.remove('is-closing');
    win.classList.add('is-open');
    place(win);
    front(win);
    running();
    const focusable = win.querySelector('input, textarea, .win__done, a, button');
    if (id === 'w-terminal') win.querySelector('input')?.focus({ preventScroll: true });
    else if (phone.matches) focusable?.focus({ preventScroll: true });
    if (phone.matches) history.replaceState(null, '', `#${id}`);
  };

  const close = (win) => {
    if (!win.classList.contains('is-open')) return;
    const done = () => { win.classList.remove('is-open', 'is-closing'); running(); };
    if (reduced.matches) return done();
    win.classList.add('is-closing');
    win.classList.remove('is-open');
    win.addEventListener('animationend', done, { once: true });
    setTimeout(done, 400);
    if (location.hash === `#${win.id}`) history.replaceState(null, '', location.pathname);
  };

  document.addEventListener('click', (e) => {
    const opener = e.target.closest('[data-open]');
    if (opener) {
      e.preventDefault();
      document.querySelectorAll('.icon.is-selected').forEach((i) => i.classList.remove('is-selected'));
      if (opener.classList.contains('icon')) opener.classList.add('is-selected');
      open(opener.dataset.open);
      return;
    }
    const closer = e.target.closest('.light--close, .win__done, .win--alert .mac-button');
    if (closer) {
      e.preventDefault();
      close(closer.closest('.win'));
      return;
    }
    const max = e.target.closest('.light--max');
    if (max) {
      const win = max.closest('.win');
      const big = win.classList.toggle('is-max');
      Object.assign(win.style, big
        ? { left: '8px', top: '36px', width: 'calc(100vw - 16px)', maxHeight: 'calc(100vh - 120px)' }
        : { width: '', maxHeight: '' });
      return;
    }
    const min = e.target.closest('.light--min');
    if (min) { close(min.closest('.win')); return; }
    if (!e.target.closest('.icon')) document.querySelectorAll('.icon.is-selected').forEach((i) => i.classList.remove('is-selected'));
  });

  document.addEventListener('pointerdown', (e) => {
    const win = e.target.closest('.win');
    if (win) front(win);
  });

  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape') return;
    const top = [...wins.values()].filter((w) => w.classList.contains('is-open')).sort((a, b) => b.style.zIndex - a.style.zIndex)[0];
    if (top) close(top);
  });

  // drag by the title bar (desktop only)
  document.querySelectorAll('.win__bar').forEach((bar) => {
    bar.addEventListener('pointerdown', (e) => {
      if (phone.matches || e.button !== 0 || e.target.closest('a, button')) return;
      const win = bar.closest('.win');
      const r = win.getBoundingClientRect();
      const dx = e.clientX - r.left, dy = e.clientY - r.top;
      bar.setPointerCapture(e.pointerId);
      const move = (ev) => {
        win.style.left = `${Math.min(innerWidth - 60, Math.max(60 - r.width, ev.clientX - dx))}px`;
        win.style.top = `${Math.min(innerHeight - 40, Math.max(28, ev.clientY - dy))}px`;
      };
      const up = () => { bar.removeEventListener('pointermove', move); bar.removeEventListener('pointerup', up); };
      bar.addEventListener('pointermove', move);
      bar.addEventListener('pointerup', up);
    });
  });

  // a link like vvalisoy.github.io/#w-valuto opens that window
  const fromHash = () => { const id = location.hash.slice(1); if (wins.has(id)) open(id); };
  fromHash();
  addEventListener('hashchange', fromHash);

  // ---------- notes ----------

  const notes = [...document.querySelectorAll('.note')];
  const showNote = (id) => {
    notes.forEach((n) => n.classList.toggle('is-active', n.id === id));
    document.querySelectorAll('[data-note]').forEach((a) => a.setAttribute('aria-current', String(a.dataset.note === id)));
  };
  if (notes.length) showNote(notes[0].id);
  document.querySelectorAll('[data-note]').forEach((a) => a.addEventListener('click', (e) => { e.preventDefault(); showNote(a.dataset.note); }));

  // ---------- photos ----------

  const photos = [...document.querySelectorAll('[data-photo]')];
  const viewer = document.querySelector('.viewer');
  const gallery = document.querySelector('.gallery');
  let current = 0;
  const show = (i) => {
    current = (i + photos.length) % photos.length;
    const img = photos[current].querySelector('img');
    const vImg = viewer.querySelector('img');
    vImg.src = img.currentSrc || img.src;
    vImg.alt = img.alt;
    viewer.querySelector('a').href = photos[current].href;
    viewer.hidden = false;
    gallery.hidden = true;
  };
  photos.forEach((p, i) => p.addEventListener('click', (e) => { e.preventDefault(); show(i); }));
  viewer?.querySelectorAll('[data-step]').forEach((b) => b.addEventListener('click', () => show(current + Number(b.dataset.step))));
  viewer?.querySelector('img').addEventListener('click', () => { viewer.hidden = true; gallery.hidden = false; });

  // ---------- mail ----------

  document.querySelector('[data-mail]')?.addEventListener('submit', (e) => {
    e.preventDefault();
    const f = e.currentTarget;
    const q = `subject=${encodeURIComponent(f.subject.value)}&body=${encodeURIComponent(f.body.value)}`;
    location.href = `mailto:vali@gevelopers.com?${q}`;
  });

  // ---------- clock ----------

  const tz = document.querySelector('[data-clock]')?.dataset.tz || 'Asia/Baku';
  const fmt = new Intl.DateTimeFormat('en-GB', { hour: '2-digit', minute: '2-digit', timeZone: tz });
  const day = new Intl.DateTimeFormat('en-GB', { weekday: 'short', day: 'numeric', month: 'short', timeZone: tz });
  const tick = () => {
    const now = new Date();
    const t = fmt.format(now);
    document.querySelectorAll('[data-clock-time]').forEach((el) => { el.textContent = phone.matches ? t : `${day.format(now)}  ${t}`; });
    document.querySelectorAll('[data-clock-big]').forEach((el) => { el.textContent = t; });
  };
  tick();
  setInterval(tick, 10000);
  phone.addEventListener('change', tick);

  // ---------- terminal ----------

  const term = document.querySelector('[data-term]');
  if (!term) return;
  const out = term.querySelector('.term__out');
  const input = term.querySelector('input');
  const history_ = [];
  let hi = 0;
  term.querySelector('[data-login]').textContent = new Date().toDateString().slice(0, 10);
  term.addEventListener('click', () => input.focus());

  const esc = (s) => s.replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' })[c]);
  const print = (htmlText) => { out.insertAdjacentHTML('beforeend', `${htmlText}\n`); term.scrollTop = term.scrollHeight; };
  const projects = {
    tiketvisa: 'w-tiketvisa', unlisim: 'w-unlisim', valuto: 'w-valuto', anonympass: 'w-anonympass',
    digitalrocket: 'w-digitalrocket', undrgoods: 'w-undrgoods', missingstone: 'w-missingstone',
    asiainsight: 'w-asiainsight', harborfalcon: 'w-harborfalcon', gevelopers: 'w-gevelopers', course: 'w-course',
    about: 'w-about', photos: 'w-photos', gallery: 'w-photos', mail: 'w-mail', code: 'w-code', trash: 'w-trash',
  };
  const commands = {
    help: () => print([
      '<b>whoami</b>      who is this',
      '<b>projects</b>    what I have shipped',
      '<b>open</b> <span class="dim">&lt;name&gt;</span> open a project, e.g. open valuto',
      '<b>skills</b>      the stack',
      '<b>contact</b>     how to reach me',
      '<b>social</b>      where else I am',
      '<b>date</b>        the time in Baku',
      '<b>clear</b>       clear the screen',
      '<b>exit</b>        close the terminal',
    ].join('\n')),
    whoami: () => print('Vali Valiyev (<b>@vvalisoy</b>). Software engineer and digital nomad from Sumgait, Azerbaijan.\nFounder of Gevelopers LLC. Builds travel products from wherever the Wi-Fi holds.'),
    ls: () => commands.projects(),
    projects: () => print([
      '<span class="dim">startups/</span>',
      '  tiketvisa      onward tickets and hotel bookings with a real PNR',
      '  unlisim        travel eSIM, 200+ destinations',
      '  valuto         pay like a local with QR codes abroad',
      '  anonympass     crypto payment gateway, Tron and Solana',
      '<span class="dim">clients/</span>',
      '  digitalrocket  undrgoods  missingstone  asiainsight  harborfalcon',
      '<span class="dim">teaching/</span>',
      '  course         Elementor A\'dan Z\'ye, 2,600+ students on Udemy',
      '',
      'Type <b>open valuto</b> (or any name above).',
    ].join('\n')),
    open: (arg) => {
      const id = projects[(arg || '').toLowerCase().replace(/[^a-z]/g, '')];
      if (!id) return print(`open: no such project: ${esc(arg || '')}. Try <b>projects</b>.`);
      print(`<span class="ok">opening ${esc(arg)}…</span>`);
      open(id);
    },
    skills: () => print('TypeScript  React  Next.js  Expo  PHP  MySQL  WordPress  WooCommerce\nCloudflare Workers  Supabase  Solana  Stripe  Shopify  SEO  n8n'),
    contact: () => print('mail      <a href="mailto:vali@gevelopers.com">vali@gevelopers.com</a>\ntelegram  <a href="https://t.me/vvalisoy" target="_blank" rel="noopener">@vvalisoy</a>\nor type <b>open mail</b>'),
    social: () => print([
      '<a href="https://github.com/vvalisoy" target="_blank" rel="noopener">github.com/vvalisoy</a>',
      '<a href="https://instagram.com/vvalisoy" target="_blank" rel="noopener">instagram.com/vvalisoy</a>',
      '<a href="https://substack.com/@vvalisoy" target="_blank" rel="noopener">substack.com/@vvalisoy</a>',
      '<a href="https://linktr.ee/vvalisoy" target="_blank" rel="noopener">linktr.ee/vvalisoy</a>',
    ].join('\n')),
    date: () => print(`${new Intl.DateTimeFormat('en-GB', { dateStyle: 'full', timeStyle: 'short', timeZone: tz }).format(new Date())} (Baku)`),
    clear: () => { out.innerHTML = ''; },
    exit: () => close(term.closest('.win')),
    sudo: () => print('Nice try. This incident will be reported to vali@gevelopers.com.'),
    hire: () => { print('<span class="ok">Great choice.</span> Opening a new message…'); open('w-mail'); },
    cat: (arg) => (/readme/i.test(arg || '') ? commands.whoami() : print(`cat: ${esc(arg || '')}: No such file or directory`)),
    pwd: () => print('/Users/vali'),
    echo: (arg) => print(esc(arg || '')),
  };

  term.querySelector('form').addEventListener('submit', (e) => {
    e.preventDefault();
    const line = input.value.trim();
    input.value = '';
    print(`<span class="ok">vali@macbook ~ %</span> ${esc(line)}`);
    if (!line) return;
    history_.push(line);
    hi = history_.length;
    const [cmd, ...rest] = line.split(/\s+/);
    const fn = commands[cmd.toLowerCase()];
    if (fn) fn(rest.join(' '));
    else print(`zsh: command not found: ${esc(cmd)}. Type <b>help</b>.`);
  });
  input.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowUp' && hi > 0) { input.value = history_[--hi]; e.preventDefault(); }
    if (e.key === 'ArrowDown') { hi = Math.min(history_.length, hi + 1); input.value = history_[hi] || ''; e.preventDefault(); }
  });
})();
