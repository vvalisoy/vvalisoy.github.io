// vvalisoy — window manager, draggable icons, terminal, notes, photos, mail and clock.
(() => {
  const phone = matchMedia('(max-width: 700px)');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const wins = new Map([...document.querySelectorAll('.win')].map((w) => [w.id, w]));
  const store = {
    get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch { return null; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* private mode */ } },
    del(k) { try { localStorage.removeItem(k); } catch { /* private mode */ } },
  };
  let z = 100;
  let cascade = 0;
  let suppressClick = false;

  // ---------- windows ----------

  const front = (win) => {
    for (const w of wins.values()) w.classList.toggle('is-front', w === win);
    win.style.zIndex = ++z;
  };

  const place = (win) => {
    if (win.dataset.placed || phone.matches) return;
    const r = win.getBoundingClientRect();
    const step = (cascade++ % 6) * 26;
    const x = Math.max(8, Math.min(innerWidth - r.width - 8, (innerWidth - r.width) / 2 - 80 + step));
    const y = Math.max(40, Math.min(innerHeight - r.height - 90, (innerHeight - r.height) / 2 - 40 + step));
    win.style.left = `${x}px`;
    win.style.top = `${y}px`;
    win.dataset.placed = '1';
  };

  const running = () => {
    document.querySelectorAll('.app[data-open]').forEach((a) => {
      a.classList.toggle('is-running', !!wins.get(a.dataset.open)?.classList.contains('is-open'));
    });
  };

  const onOpen = {};

  const open = (id) => {
    const win = wins.get(id);
    if (!win) return;
    win.classList.remove('is-closing');
    win.classList.add('is-open');
    place(win);
    front(win);
    running();
    onOpen[id]?.(win);
    if (phone.matches) history.replaceState(null, '', `#${id}`);
  };

  const close = (win) => {
    if (!win || !win.classList.contains('is-open')) return;
    const done = () => { win.classList.remove('is-open', 'is-closing'); running(); };
    if (location.hash === `#${win.id}`) history.replaceState(null, '', location.pathname);
    if (reduced.matches) return done();
    win.classList.add('is-closing');
    win.classList.remove('is-open');
    win.addEventListener('animationend', done, { once: true });
    setTimeout(done, 400);
  };

  const deselect = () => document.querySelectorAll('.icon.is-selected').forEach((i) => i.classList.remove('is-selected'));

  document.addEventListener('click', (e) => {
    if (suppressClick) { suppressClick = false; e.preventDefault(); return; }
    const opener = e.target.closest('[data-open]');
    if (opener) {
      e.preventDefault();
      deselect();
      if (opener.classList.contains('icon')) opener.classList.add('is-selected');
      open(opener.dataset.open);
      return;
    }
    if (e.target.closest('[data-cleanup]')) { e.preventDefault(); cleanUp(); return; }
    const closer = e.target.closest('.light--close, .win__done, .win--alert .mac-button');
    if (closer) { e.preventDefault(); close(closer.closest('.win')); return; }
    const max = e.target.closest('.light--max');
    if (max) {
      const win = max.closest('.win');
      const big = win.classList.toggle('is-max');
      Object.assign(win.style, big
        ? { left: '8px', top: '36px', width: 'calc(100vw - 16px)', maxHeight: 'calc(100vh - 124px)' }
        : { width: '', maxHeight: '' });
      return;
    }
    const min = e.target.closest('.light--min');
    if (min) { close(min.closest('.win')); return; }
    if (!e.target.closest('.icon')) deselect();
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

  // drag windows by the title bar (desktop only)
  document.querySelectorAll('.win__bar').forEach((bar) => {
    bar.addEventListener('pointerdown', (e) => {
      if (phone.matches || e.button !== 0 || e.target.closest('a, button')) return;
      const win = bar.closest('.win');
      const r = win.getBoundingClientRect();
      const dx = e.clientX - r.left, dy = e.clientY - r.top;
      bar.setPointerCapture(e.pointerId);
      const move = (ev) => {
        win.style.left = `${Math.min(innerWidth - 60, Math.max(60 - r.width, ev.clientX - dx))}px`;
        win.style.top = `${Math.min(innerHeight - 44, Math.max(30, ev.clientY - dy))}px`;
      };
      const up = () => { bar.removeEventListener('pointermove', move); bar.removeEventListener('pointerup', up); };
      bar.addEventListener('pointermove', move);
      bar.addEventListener('pointerup', up);
    });
  });

  // ---------- desktop icons: drag them anywhere, positions are remembered ----------

  const area = document.querySelector('.icons');
  const icons = [...document.querySelectorAll('.icon')];
  const KEY = 'vvalisoy:icons';
  const saved = store.get(KEY) || {};
  const setPos = (icon, x, y) => { icon.style.setProperty('--x', `${x}%`); icon.style.setProperty('--y', `${y}%`); };
  icons.forEach((icon) => {
    icon.dataset.home = `${icon.style.getPropertyValue('--x')}|${icon.style.getPropertyValue('--y')}`;
    const p = saved[icon.dataset.open];
    if (p) setPos(icon, p.x, p.y);
  });

  function cleanUp() {
    store.del(KEY);
    icons.forEach((icon) => {
      const [x, y] = icon.dataset.home.split('|');
      icon.style.setProperty('--x', x);
      icon.style.setProperty('--y', y);
    });
  }

  icons.forEach((icon) => {
    icon.addEventListener('dragstart', (e) => e.preventDefault());
    icon.addEventListener('pointerdown', (e) => {
      if (phone.matches || e.button !== 0) return;
      const box = area.getBoundingClientRect();
      const r = icon.getBoundingClientRect();
      const offX = e.clientX - (r.left + r.width / 2);
      const offY = e.clientY - r.top;
      const startX = e.clientX, startY = e.clientY;
      let dragging = false;
      const move = (ev) => {
        if (!dragging && Math.hypot(ev.clientX - startX, ev.clientY - startY) < 5) return;
        if (!dragging) {
          dragging = true;
          icon.setPointerCapture(e.pointerId);
          icon.classList.add('is-dragging');
          deselect();
          icon.classList.add('is-selected');
        }
        const cx = Math.min(box.right - 30, Math.max(box.left + 30, ev.clientX - offX));
        const cy = Math.min(box.bottom - 40, Math.max(box.top, ev.clientY - offY));
        setPos(icon, ((cx - box.left) / box.width * 100).toFixed(2), ((cy - box.top) / box.height * 100).toFixed(2));
      };
      const up = () => {
        removeEventListener('pointermove', move);
        removeEventListener('pointerup', up);
        if (!dragging) return;
        icon.classList.remove('is-dragging');
        suppressClick = true;
        setTimeout(() => { suppressClick = false; }, 0);
        const all = store.get(KEY) || {};
        all[icon.dataset.open] = { x: parseFloat(icon.style.getPropertyValue('--x')), y: parseFloat(icon.style.getPropertyValue('--y')) };
        store.set(KEY, all);
      };
      addEventListener('pointermove', move);
      addEventListener('pointerup', up);
    });
  });

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

  // ---------- mail: sent through FormSubmit, since GitHub Pages cannot run server code ----------

  const form = document.querySelector('[data-mail]');
  if (form) {
    const status = form.querySelector('.mail__status');
    const sendBtns = document.querySelectorAll('.mail__send, .mail__foot .mac-button');
    const say = (text, cls) => { status.className = `mail__status ${cls || ''}`; status.innerHTML = text; };
    onOpen['w-mail'] = (win) => {
      if (!phone.matches) win.querySelector('input[name="email"]').focus({ preventScroll: true });
    };
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      if (form._honey.value) return;
      const data = {
        email: form.email.value.trim(),
        _replyto: form.email.value.trim(),
        _subject: `${form._subject.value.trim()} (via vvalisoy.github.io)`,
        message: form.message.value,
        _template: 'box',
        _captcha: 'false',
      };
      sendBtns.forEach((b) => { b.disabled = true; });
      say('Sending…');
      try {
        const res = await fetch('https://formsubmit.co/ajax/vali@gevelopers.com', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify(data),
        });
        const json = await res.json().catch(() => ({}));
        if (!res.ok || String(json.success) === 'false') throw new Error(json.message || res.statusText);
        const win = form.closest('.win');
        win.classList.remove('is-sent'); void win.offsetWidth; win.classList.add('is-sent');
        form.message.value = '';
        say('Sent. Vali will reply to your address, usually within a day.', 'is-ok');
      } catch {
        const q = `subject=${encodeURIComponent(form._subject.value)}&body=${encodeURIComponent(form.message.value)}`;
        say(`Could not send right now. <a href="mailto:vali@gevelopers.com?${q}">Open it in your mail app</a> instead.`, 'is-err');
      } finally {
        sendBtns.forEach((b) => { b.disabled = false; });
      }
    });
  }

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
  if (term) {
    const out = term.querySelector('.term__out');
    const input = term.querySelector('input');
    const past = [];
    let hi = 0;
    const PS = '<span class="ok">vali@macbook ~ %</span>';
    const esc = (s) => s.replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' })[c]);
    const print = (htmlText) => { out.insertAdjacentHTML('beforeend', `${htmlText}\n`); term.scrollTop = term.scrollHeight; };
    const s = (t) => `<span class="s">"${t}"</span>`;
    const VALI_TS = [
      '<span class="c">// Hi. This is me, typed.</span>',
      `<span class="k">export const</span> <span class="v">vali</span> = {`,
      `  name: ${s('Vali Valiyev')},`,
      `  handle: ${s('@vvalisoy')},`,
      `  from: ${s('Sumgait, Azerbaijan')},`,
      `  basedIn: ${s('Baku, mostly')},`,
      `  role: ${s('Software engineer')},`,
      `  company: ${s('Gevelopers LLC')},`,
      `  shipping: [${s('TiketVisa')}, ${s('UnliSIM')}, ${s('Valuto')}, ${s('AnonymPass')}],`,
      `  stack: [${s('TypeScript')}, ${s('React')}, ${s('Next.js')}, ${s('Expo')},`,
      `          ${s('Cloudflare Workers')}, ${s('Supabase')}, ${s('PHP')}, ${s('WordPress')}],`,
      '  wordpressSitesBuilt: <span class="n">200</span>,',
      '  udemyStudents: <span class="n">2600</span>,',
      `  speaks: [${s('az')}, ${s('tr')}, ${s('en')}],`,
      '  availableForWork: <span class="k">true</span>,',
      '};',
      '',
      '<span class="k">export function</span> <span class="f">hire</span>(project: <span class="t">string</span>) {',
      `  <span class="k">return</span> <span class="f">fetch</span>(${s('mailto:vali@gevelopers.com')}, { body: project });`,
      '}',
    ].join('\n');

    // every time the terminal opens it starts fresh with vali.ts on screen
    onOpen['w-terminal'] = () => {
      const login = new Date().toString().slice(0, 24);
      out.innerHTML = '';
      print(`<span class="dim">Last login: ${login} on ttys001</span>`);
      print(`${PS} cat vali.ts`);
      print(VALI_TS);
      print('');
      print('<span class="dim">Type <b>help</b> to see what else this terminal can do.</span>');
      input.value = '';
      if (!phone.matches) input.focus({ preventScroll: true });
      term.scrollTop = 0;
    };
    term.addEventListener('click', () => input.focus());

    const projects = {
      tiketvisa: 'w-tiketvisa', unlisim: 'w-unlisim', valuto: 'w-valuto', anonympass: 'w-anonympass',
      digitalrocket: 'w-digitalrocket', undrgoods: 'w-undrgoods', missingstone: 'w-missingstone',
      asiainsight: 'w-asiainsight', harborfalcon: 'w-harborfalcon', travelsolotiket: 'w-travelsolotiket',
      gevelopers: 'w-gevelopers', course: 'w-course',
      about: 'w-about', photos: 'w-photos', gallery: 'w-photos', mail: 'w-mail', trash: 'w-trash',
    };
    const commands = {
      help: () => print([
        '<b>cat vali.ts</b>  print me again',
        '<b>whoami</b>       who is this',
        '<b>projects</b>     what I have shipped',
        '<b>open</b> <span class="dim">&lt;name&gt;</span>  open a project, e.g. open valuto',
        '<b>skills</b>       the stack',
        '<b>contact</b>      how to reach me',
        '<b>hire</b>         start a message',
        '<b>social</b>       where else I am',
        '<b>date</b>         the time in Baku',
        '<b>clear</b>        clear the screen',
        '<b>exit</b>         close the terminal',
      ].join('\n')),
      whoami: () => print('Vali Valiyev (<b>@vvalisoy</b>). Software engineer and digital nomad from Sumgait, Azerbaijan.\nFounder of Gevelopers LLC. Builds travel products from wherever the Wi-Fi holds.'),
      ls: () => print('vali.ts  projects/  photos/  README.md'),
      projects: () => print([
        '<span class="dim">startups/</span>',
        '  tiketvisa        onward tickets and hotel bookings with a real PNR',
        '  unlisim          travel eSIM, 200+ destinations',
        '  valuto           pay like a local with QR codes abroad',
        '  anonympass       crypto payment gateway, Tron and Solana',
        '<span class="dim">clients/</span>',
        '  digitalrocket  undrgoods  missingstone  asiainsight  harborfalcon  travelsolotiket',
        '<span class="dim">teaching/</span>',
        "  course           Elementor A'dan Z'ye, 2,600+ students on Udemy",
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
      contact: () => print('mail      <a href="mailto:vali@gevelopers.com">vali@gevelopers.com</a>\ntelegram  <a href="https://t.me/vvalisoy" target="_blank" rel="noopener">@vvalisoy</a>\nor type <b>hire</b>'),
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
      cat: (arg) => {
        if (/vali\.ts/i.test(arg || '')) return print(VALI_TS);
        if (/readme/i.test(arg || '')) return commands.whoami();
        print(`cat: ${esc(arg || '')}: No such file or directory`);
      },
      pwd: () => print('/Users/vali'),
      echo: (arg) => print(esc(arg || '')),
    };

    term.querySelector('form').addEventListener('submit', (e) => {
      e.preventDefault();
      const line = input.value.trim();
      input.value = '';
      print(`${PS} ${esc(line)}`);
      if (!line) return;
      past.push(line);
      hi = past.length;
      const [cmd, ...rest] = line.split(/\s+/);
      const fn = commands[cmd.toLowerCase()];
      if (fn) fn(rest.join(' '));
      else print(`zsh: command not found: ${esc(cmd)}. Type <b>help</b>.`);
    });
    input.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowUp' && hi > 0) { input.value = past[--hi]; e.preventDefault(); }
      if (e.key === 'ArrowDown') { hi = Math.min(past.length, hi + 1); input.value = past[hi] || ''; e.preventDefault(); }
    });
  }

  // a link like vvalisoy.github.io/#w-valuto opens that window
  const fromHash = () => { const id = location.hash.slice(1); if (wins.has(id)) open(id); };
  fromHash();
  addEventListener('hashchange', fromHash);
})();
