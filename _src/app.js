/* Maison Valeria — scripts du site */
(function () {
  'use strict';

  /* ------------------------------------------------------------------
     Réglages de l'institut : à compléter dès réception des coordonnées.
     whatsapp : numéro au format international sans « + » (ex. 2135XXXXXXXX)
     ------------------------------------------------------------------ */
  var CONFIG = window.MV_CONFIG || { whatsapp: '' };

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };

  /* Prestations (même ordre que les pages) */
  var P = [
    ['Beauté du sourire', ['Blanchiment dentaire esthétique', 'Accompagnement & conseils personnalisés']],
    ['Coiffure & beauté capillaire', ['Coiffure féminine', 'Brushing et mise en beauté', 'Lissage brésilien', 'Lissage indien', 'Lissage japonais', 'Lissage coréen', 'Soins capillaires profonds', 'Protocole personnalisé']],
    ['Soins du visage & skincare', ['Soin du visage personnalisé', 'Masques', 'Soin éclat & hydratation', 'Routine skincare adaptée', 'Conseils produits & habitudes de soins']],
    ['Diagnostics beauté', ['Diagnostic capillaire (offert)', 'Diagnostic esthétique du visage (offert)']],
    ['Beauté des mains & ongles', ['Manucure & mise en beauté des mains', 'Pose d’ongles', 'Nail art & finitions personnalisées', 'Soins esthétiques des mains']]
  ];
  var ADDONS = ['Diagnostic capillaire offert', 'Diagnostic du visage offert'];

  /* Année */
  $$('#yr').forEach(function (e) { e.textContent = new Date().getFullYear(); });

  /* En-tête */
  var hdr = $('.hdr');
  function onScroll() {
    var y = window.scrollY;
    if (hdr) hdr.classList.toggle('solid', y > 40);
    if (fab) fab.classList.toggle('show', y > 600 && !bookingVisible);
  }
  var fab = $('.fab'), bookingVisible = false;
  window.addEventListener('scroll', onScroll, { passive: true });

  /* Menu mobile */
  var mnav = $('.mnav');
  $$('[data-menu]').forEach(function (b) {
    b.addEventListener('click', function () {
      mnav.classList.toggle('open');
      document.documentElement.style.overflow = mnav.classList.contains('open') ? 'hidden' : '';
    });
  });
  $$('.mnav a').forEach(function (a) {
    a.addEventListener('click', function () { mnav.classList.remove('open'); document.documentElement.style.overflow = ''; });
  });

  /* Apparition au défilement */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    $$('.rv').forEach(function (e) { io.observe(e); });
  } else { $$('.rv').forEach(function (e) { e.classList.add('in'); }); }

  /* Diaporama d'accueil */
  (function () {
    var hx = $('.hx'); if (!hx) return;
    var slides = $$('.s', hx), thumbs = $$('.thumbs button', hx), cnt = $('.cnt b', hx), bar = $('.bar i', hx);
    var i = 0, t = null, DUR = 6500;
    function go(n) {
      slides[i].classList.remove('on'); if (thumbs[i]) thumbs[i].classList.remove('on');
      i = (n + slides.length) % slides.length;
      slides[i].classList.add('on'); if (thumbs[i]) thumbs[i].classList.add('on');
      if (cnt) cnt.textContent = ('0' + (i + 1)).slice(-2);
      if (bar) { bar.classList.remove('run'); void bar.offsetWidth; bar.classList.add('run'); }
      clearTimeout(t); t = setTimeout(function () { go(i + 1); }, DUR);
    }
    thumbs.forEach(function (b, k) { b.addEventListener('click', function () { go(k); }); });
    var p = $('.prv', hx), n = $('.nxt', hx);
    if (p) p.addEventListener('click', function () { go(i - 1); });
    if (n) n.addEventListener('click', function () { go(i + 1); });
    var sx = null;
    hx.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    hx.addEventListener('touchend', function (e) {
      if (sx === null) return; var dx = e.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 50) go(i + (dx < 0 ? 1 : -1)); sx = null;
    });
    document.addEventListener('visibilitychange', function () { if (document.hidden) clearTimeout(t); else go(i); });
    go(0);
  })();

  /* Diagnostic : scanner animé */
  (function () {
    var sc = $('#scanner'); if (!sc) return;
    var D = {
      cap: { t: 'Cuir chevelu', steps: ['Analyse du cuir chevelu par caméra haute définition', 'Observation de l’état des cheveux et du cuir chevelu', 'Évaluation de vos besoins capillaires', 'Recommandation de soins et de produits adaptés'], lbl: ['Cuir chevelu', 'État des cheveux', 'Besoins capillaires', 'Soins adaptés'] },
      vis: { t: 'Peau du visage', steps: ['Analyse de la peau par un appareil spécialisé', 'Évaluation de l’hydratation et des imperfections', 'Identification des besoins de votre peau', 'Recommandations de soins personnalisées'], lbl: ['Texture', 'Hydratation', 'Imperfections', 'Soins sur mesure'] }
    };
    var POS = [[18, 16], [72, 26], [76, 70], [10, 74]];
    var ol = $('#dsteps'), lbls = $$('.lbl', sc), pts = $$('.pt', sc), img = $('#diagImg'), coreT = $('#coreT');
    var timer = null, mode = 'cap';
    function set(m) {
      mode = m; var d = D[m];
      $$('.dtabs button').forEach(function (b) { b.classList.toggle('on', b.getAttribute('data-m') === m); });
      ol.innerHTML = d.steps.map(function (s) { return '<li>' + s + '</li>'; }).join('');
      lbls.forEach(function (l, k) { l.textContent = d.lbl[k]; l.style.left = POS[k][0] + '%'; l.style.top = POS[k][1] + '%'; l.classList.remove('on'); });
      pts.forEach(function (p) { p.classList.remove('on'); });
      if (coreT) coreT.textContent = d.t;
      if (img) { img.classList.remove('show'); setTimeout(function () { img.src = img.getAttribute('data-' + m); img.onload = function () { img.classList.add('show'); }; if (img.complete) img.classList.add('show'); }, 250); }
      var k = 0, lis = $$('li', ol); clearInterval(timer);
      timer = setInterval(function () {
        if (k < 4) { lis[k].classList.add('on'); if (lbls[k]) lbls[k].classList.add('on'); if (pts[k]) pts[k].classList.add('on'); k++; }
        else { clearInterval(timer); setTimeout(function () { set(mode === 'cap' ? 'vis' : 'cap'); }, 2600); }
      }, 900);
    }
    $$('.dtabs button').forEach(function (b) { b.addEventListener('click', function () { set(b.getAttribute('data-m')); }); });
    var started = false;
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting && !started) { started = true; set('cap'); } }); }, { threshold: 0.3 }).observe(sc);
    } else set('cap');
  })();

  /* Vidéo de présentation */
  (function () {
    var sec = $('.mvv'); if (!sec) return;
    var v = $('video', sec), pp = $('.mvv-pp', sec), bar = $('.mvv-bar i', sec), user = false;
    if (window.matchMedia('(max-width:900px)').matches) { var so = $('source', v); so.src = so.src.replace('.mp4', '-720.mp4'); v.load(); }
    var PLAY = '<svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>', PAUSE = '<svg viewBox="0 0 24 24"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>';
    function ui() { pp.innerHTML = v.paused ? PLAY : PAUSE; pp.setAttribute('aria-label', v.paused ? 'Lecture' : 'Pause'); }
    ui(); v.addEventListener('play', ui); v.addEventListener('pause', ui);
    v.addEventListener('timeupdate', function () { if (v.duration) bar.style.width = (v.currentTime / v.duration * 100) + '%'; });
    pp.addEventListener('click', function () { user = true; if (v.paused) v.play(); else v.pause(); });
    $('.mvv-rs', sec).addEventListener('click', function () { v.currentTime = 0; v.play(); user = false; });
    v.addEventListener('click', function () { pp.click(); });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (e.isIntersecting) { sec.classList.add('on'); if (!user) { var r = v.play(); if (r && r.catch) r.catch(function () {}); } }
          else if (!v.paused && !user) v.pause();
        });
      }, { threshold: 0.35 }).observe(sec);
    } else sec.classList.add('on');
  })();

  /* Module de prise de rendez-vous */
  var booking = $('#booking');
  function bookUrl(code) { return '/rendez-vous' + (code ? '?s=' + encodeURIComponent(code) : '') + '#booking'; }

  $$('[data-book]').forEach(function (b) {
    b.addEventListener('click', function (e) {
      var code = b.getAttribute('data-book');
      if (!booking) { e.preventDefault(); location.href = bookUrl(code); return; }
      e.preventDefault(); if (window.MV_BOOK) window.MV_BOOK.pick(code);
    });
  });

  if (booking) (function () {
    var st = { step: 0, p: 0, s: -1, add: [], d: null, h: null };
    var MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'];
    var JOURS = ['dim.', 'lun.', 'mar.', 'mer.', 'jeu.', 'ven.', 'sam.'];
    var JOURSL = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'];
    var poles = $('#bkPoles'), opts = $('#bkOpts'), add = $('#bkAdd'), days = $('#bkDays'), slots = $('#bkSlots'), month = $('#bkMonth');
    var next = $('#bkNext'), back = $('#bkBack'), nav = $('#bkNav'), recap = $('#bkRecap');

    function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
    function fmtDate(d) { return JOURSL[d.getDay()] + ' ' + d.getDate() + ' ' + MOIS[d.getMonth()]; }

    function renderPoles() {
      poles.innerHTML = P.map(function (p, k) { return '<button type="button" class="chip' + (k === st.p ? ' on' : '') + '" data-i="' + k + '">' + esc(p[0]) + '</button>'; }).join('');
      opts.innerHTML = P[st.p][1].map(function (s, k) { return '<button type="button" class="opt' + (k === st.s ? ' on' : '') + '" data-k="' + k + '"><span class="dot"></span><span>' + esc(s) + '</span></button>'; }).join('');
      add.style.display = st.p === 3 ? 'none' : '';
      $$('input', add).forEach(function (c) { c.checked = st.add.indexOf(+c.getAttribute('data-a')) > -1; });
    }
    poles.addEventListener('click', function (e) { var b = e.target.closest('.chip'); if (!b) return; st.p = +b.getAttribute('data-i'); st.s = -1; renderPoles(); upd(); });
    opts.addEventListener('click', function (e) { var b = e.target.closest('.opt'); if (!b) return; st.s = +b.getAttribute('data-k'); renderPoles(); upd(); });
    add.addEventListener('change', function () { st.add = $$('input', add).filter(function (c) { return c.checked; }).map(function (c) { return +c.getAttribute('data-a'); }); upd(); });

    /* Jours : 21 jours à partir de demain */
    var DAYS = [];
    for (var k = 1; k <= 21; k++) { var d = new Date(); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() + k); DAYS.push(d); }
    function renderDays() {
      days.innerHTML = DAYS.map(function (d, k) {
        var on = st.d && st.d.getTime() === d.getTime();
        return '<button type="button" class="day' + (on ? ' on' : '') + '" data-k="' + k + '"' + '><small>' + JOURS[d.getDay()] + '</small><b>' + d.getDate() + '</b><small>' + MOIS[d.getMonth()].slice(0, 4) + '</small></button>';
      }).join('');
      var ref = st.d || DAYS[0]; month.textContent = MOIS[ref.getMonth()] + ' ' + ref.getFullYear();
    }
    function seed(n) { var x = Math.sin(n) * 10000; return x - Math.floor(x); }
    function renderSlots() {
      if (!st.d) { slots.innerHTML = '<p class="sub" style="grid-column:1/-1">Choisissez d’abord un jour.</p>'; return; }
      var out = [];
      for (var h = 10; h < 19; h++) for (var m = 0; m < 60; m += 30) {
        var lab = h + ':' + (m ? '30' : '00'), busy = seed(st.d.getTime() / 864e5 + h * 7 + m) < 0.28;
        out.push('<button type="button" class="slot' + (st.h === lab ? ' on' : '') + '" data-h="' + lab + '"' + (busy ? ' disabled' : '') + '>' + lab + '</button>');
      }
      slots.innerHTML = out.join('');
    }
    days.addEventListener('click', function (e) { var b = e.target.closest('.day'); if (!b || b.disabled) return; st.d = DAYS[+b.getAttribute('data-k')]; st.h = null; renderDays(); renderSlots(); upd(); });
    slots.addEventListener('click', function (e) { var b = e.target.closest('.slot'); if (!b || b.disabled) return; st.h = b.getAttribute('data-h'); renderSlots(); upd(); });

    var RE_TEL = /^(0[567]\d{8}|0[2-4]\d{7}|(\+|00)213[567]\d{8}|(\+|00)213[2-4]\d{7})$/;
    function telOk() { return RE_TEL.test(($('#iT').value || '').replace(/[\s.\-()]/g, '')); }
    function nameOk() { return ($('#iN').value || '').trim().length > 1; }
    ['#iN', '#iT'].forEach(function (s) { $(s).addEventListener('input', function () { $(s === '#iN' ? '#fN' : '#fT').classList.remove('bad'); upd(); }); });

    function valid() {
      if (st.step === 0) return st.s > -1;
      if (st.step === 1) return !!(st.d && st.h);
      if (st.step === 2) return nameOk() && ($('#iT').value || '').trim().length > 0;
      return true;
    }
    function svcLabel() { return st.s > -1 ? P[st.p][1][st.s] : '—'; }
    function upd() {
      $$('.bk-step').forEach(function (s, k) { s.classList.toggle('on', k === st.step); s.classList.toggle('done', k < st.step); });
      $$('.bk-pane').forEach(function (p, k) { p.classList.toggle('on', k === st.step); });
      back.style.visibility = st.step > 0 && st.step < 3 ? 'visible' : 'hidden';
      nav.style.display = st.step === 3 ? 'none' : 'flex';
      next.disabled = !valid();
      next.firstChild.nodeValue = st.step === 2 ? 'Envoyer ma demande ' : 'Continuer ';
      var extra = st.add.map(function (a) { return ADDONS[a]; });
      recap.innerHTML =
        '<li><span>Univers</span><span>' + esc(P[st.p][0]) + '</span></li>' +
        '<li><span>Prestation</span><span>' + esc(svcLabel()) + '</span></li>' +
        (extra.length ? '<li><span>En plus</span><span>' + esc(extra.join(', ')) + '</span></li>' : '') +
        '<li><span>Date</span><span>' + (st.d ? fmtDate(st.d) : '—') + '</span></li>' +
        '<li><span>Heure</span><span>' + (st.h || '—') + '</span></li>';
    }
    next.addEventListener('click', function () {
      if (st.step === 2) {
        var ok = true;
        if (!nameOk()) { $('#fN').classList.add('bad'); ok = false; }
        if (!telOk()) { $('#fT').classList.add('bad'); ok = false; }
        if (!ok) return;
        finish();
      }
      if (!valid()) return;
      st.step = Math.min(3, st.step + 1); upd();
      booking.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    back.addEventListener('click', function () { st.step = Math.max(0, st.step - 1); upd(); });

    function finish() {
      var n = new Date(), pad = function (x) { return ('0' + x).slice(-2); };
      var ref = 'MV-' + pad(st.d.getMonth() + 1) + pad(st.d.getDate()) + '-' + st.h.replace(':', '');
      var name = $('#iN').value.trim(), tel = $('#iT').value.trim(), mail = $('#iE').value.trim(), msg = $('#iM').value.trim();
      var extra = st.add.map(function (a) { return ADDONS[a]; });
      $('#bkRef').textContent = ref;
      var txt = 'Bonjour Maison Valeria, je souhaite réserver :\n• ' + svcLabel() + (extra.length ? '\n• ' + extra.join('\n• ') : '') +
        '\n• Le ' + fmtDate(st.d) + ' à ' + st.h + '\nNom : ' + name + '\nTéléphone : ' + tel + (mail ? '\nE-mail : ' + mail : '') + (msg ? '\nMessage : ' + msg : '') + '\nRéférence : ' + ref;
      var done = $('#bkDone'), act = $('#bkAct');
      if (CONFIG.whatsapp) {
        done.innerHTML = 'Merci ' + esc(name) + '. Envoyez votre demande sur WhatsApp : l’institut vous confirme le rendez-vous du <b>' + fmtDate(st.d) + ' à ' + st.h + '</b>.';
        act.innerHTML = '<a class="bk-wa" target="_blank" rel="noopener" href="https://wa.me/' + CONFIG.whatsapp + '?text=' + encodeURIComponent(txt) + '"><svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.4 14.2c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-3.3-.8-2.8-1.1-4.5-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.3.5-.4.4c-.1.2-.3.3-.1.6.2.3.7 1.2 1.6 1.9 1.1.9 2 1.2 2.3 1.4.3.1.5.1.6-.1l.9-1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.4z"/></svg>Envoyer sur WhatsApp</a>';
      } else {
        done.innerHTML = 'Merci ' + esc(name) + '. Votre demande pour <b>' + esc(svcLabel()) + '</b>, le <b>' + fmtDate(st.d) + ' à ' + st.h + '</b>, est prête. La réservation en ligne sera pleinement active à l’ouverture de l’institut : conservez votre référence.';
        act.innerHTML = '';
      }
    }
    $('#bkAgain').addEventListener('click', function () {
      st = { step: 0, p: 0, s: -1, add: [], d: null, h: null };
      ['#iN', '#iT', '#iE', '#iM'].forEach(function (s) { $(s).value = ''; });
      renderPoles(); renderDays(); renderSlots(); upd();
    });

    window.MV_BOOK = {
      pick: function (code) {
        var a = String(code || '').split(':'), p = +a[0], s = a.length > 1 ? +a[1] : -1;
        if (P[p]) { st.p = p; st.s = (s > -1 && s < P[p][1].length) ? s : -1; st.step = 0; }
        renderPoles(); upd();
        booking.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    };

    renderPoles(); renderDays(); renderSlots(); upd();
    var q = (location.search.match(/[?&]s=([^&]+)/) || [])[1];
    if (q) setTimeout(function () { window.MV_BOOK.pick(decodeURIComponent(q)); }, 300);

    if ('IntersectionObserver' in window && fab) {
      new IntersectionObserver(function (es) { es.forEach(function (e) { bookingVisible = e.isIntersecting; onScroll(); }); }, { threshold: 0.05 }).observe(booking);
    }
  })();

  onScroll();
})();
