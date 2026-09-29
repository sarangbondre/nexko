(() => {
  const nav = document.getElementById('nav');
  const toggle = nav.querySelector('.nav__toggle');

  // Solid nav once past the top of the hero
  const onScroll = () => nav.classList.toggle('is-solid', window.scrollY > 40);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // Mobile menu
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', open);
  });
  nav.querySelectorAll('.nav__links a').forEach(a =>
    a.addEventListener('click', () => {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    })
  );

  // Reveal on scroll
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));

  // Subtle parallax on the full-bleed band
  const band = document.querySelector('.band__media');
  if (band && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const parent = band.parentElement;
    const move = () => {
      const r = parent.getBoundingClientRect();
      if (r.bottom < 0 || r.top > innerHeight) return;
      const p = (r.top + r.height / 2 - innerHeight / 2) / innerHeight;
      band.style.transform = `translate3d(0, ${p * -8}%, 0)`;
    };
    move();
    window.addEventListener('scroll', () => requestAnimationFrame(move), { passive: true });
  }

  // Service "enquire" links preselect the service in the form
  const select = document.getElementById('service');
  document.querySelectorAll('[data-service]').forEach(a =>
    a.addEventListener('click', () => { select.value = a.dataset.service; })
  );

  // Enquiry form: compose an email or WhatsApp message (no backend needed)
  const form = document.getElementById('enquiry');
  const err = document.getElementById('formError');

  const collect = () => {
    const d = Object.fromEntries(new FormData(form));
    if (!d.name.trim() || !d.phone.trim()) {
      err.textContent = 'Please add your name and phone number.';
      return null;
    }
    err.textContent = '';
    return d;
  };
  const body = d => [
    `Name: ${d.name}`,
    d.company && `Company: ${d.company}`,
    `Phone: ${d.phone}`,
    d.email && `Email: ${d.email}`,
    `Service: ${d.service}`
  ].filter(Boolean).join('\n') + (d.message.trim() ? `\n\n${d.message.trim()}` : '');

  form.addEventListener('submit', e => {
    e.preventDefault();
    const d = collect();
    if (!d) return;
    const subject = `Enquiry: ${d.service}${d.company ? ' – ' + d.company : ''}`;
    location.href = `mailto:info@nexkorenewable.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body(d))}`;
  });

  document.getElementById('waSend').addEventListener('click', () => {
    const d = collect();
    if (!d) return;
    const text = `Hi NEXKO, I'd like to discuss a project.\n\n${body(d)}`;
    window.open(`https://wa.me/919822218891?text=${encodeURIComponent(text)}`, '_blank', 'noopener');
  });

  document.getElementById('year').textContent = new Date().getFullYear();
})();
