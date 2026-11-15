/* Shared prototype chrome for every Member Hub page (MW 2026-11-14):
   1. "Start a thread" in the top ribbon, next to My work.
   2. The Page feedback button and dialog, matching the Django app's _feedback.html.
   Prototype only: the feedback dialog sends nothing. */
(function () {
  var css = ''
    + '.hc-thread{display:inline-flex;align-items:center;gap:8px;min-height:40px;padding:0 14px;border-radius:999px;border:1px solid var(--line-2,#d5d3d9);background:transparent;color:var(--purple-ink,#3c1d66);font:500 14.5px/1 var(--sans,system-ui,sans-serif);text-decoration:none;white-space:nowrap}'
    + '@media (min-width:1300px){.tools:has(.hc-thread:not([hidden])) .search{width:190px}}'
    + '.hc-thread:hover{background:var(--purple-tint,#efe8f8)}'
    + '.hc-thread svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}'
    + '.hc-thread.hc-icon span{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}.hc-thread.hc-icon{padding:0 11px}.hc-thread[hidden]{display:none}'
    + '.fbk-open{position:fixed;right:22px;bottom:22px;z-index:50;padding:10px 20px;border-radius:999px;border:0;background:var(--purple,#512888);color:#fff;font:600 14px/20px var(--sans,system-ui,sans-serif);box-shadow:0 8px 24px -8px rgba(60,29,102,.5);cursor:pointer}'
    + '.fbk-open:hover{background:var(--purple-ink,#3c1d66)}'
    + '@media (max-width:980px){.fbk-open{bottom:calc(78px + env(safe-area-inset-bottom,0px));right:16px}}'
    + 'dialog.fbk{border:0;border-radius:12px;padding:26px 28px;width:min(520px,calc(100vw - 32px));box-shadow:0 18px 50px rgba(31,27,41,.25);font:400 15px/22px var(--sans,system-ui,sans-serif);color:var(--ink,#1d1b21);background:var(--paper,#fff)}'
    + 'dialog.fbk::backdrop{background:rgba(31,27,41,.35)}'
    + '.fbk h2{margin:0 0 6px;font:500 22px/28px var(--serif,Georgia,serif)}'
    + '.fbk p{margin:0}.fbk .fbk-sub{color:var(--muted,#6b6772);font-size:14px}'
    + '.fbk fieldset{border:0;padding:0;margin:14px 0}'
    + '.fbk-topics{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px}'
    + '.fbk-topics legend,.fbk-rate legend{font-weight:600;margin-bottom:6px;font-size:14px}'
    + '.fbk-topics label{display:flex;gap:8px;align-items:center;font-size:14px}'
    + '.fbk-topics input{accent-color:var(--purple,#512888)}'
    + '.fbk-rate{display:flex;gap:8px}.fbk-rate label{cursor:pointer}.fbk-rate input{position:absolute;opacity:0}'
    + '.fbk-rate span{display:inline-grid;place-items:center;width:38px;height:38px;border-radius:50%;border:1px solid var(--line,#e6e3ea);font-weight:600}'
    + '.fbk-rate input:checked+span{background:var(--purple,#512888);color:#fff;border-color:var(--purple,#512888)}'
    + '.fbk-rate input:focus-visible+span{outline:2px solid var(--purple,#512888);outline-offset:2px}'
    + '.fbk label.fbk-l{display:block;font-weight:600;font-size:14px}'
    + '.fbk textarea{width:100%;box-sizing:border-box;margin-top:6px;padding:10px 12px;border:1px solid var(--line-2,#d5d3d9);border-radius:8px;font:inherit;background:var(--paper,#fff);color:inherit}'
    + '.fbk-msg{min-height:1.2em;margin-top:8px!important;color:var(--purple,#512888);font-size:14px}'
    + '.fbk-row{display:flex;gap:10px;margin-top:12px}'
    + '.fbk-row button{min-height:42px;padding:0 18px;border-radius:8px;font:500 15px/1 var(--sans,system-ui,sans-serif);cursor:pointer;border:1px solid var(--line-2,#d5d3d9);background:var(--surface,#fff);color:var(--ink,#1d1b21)}'
    + '.fbk-row .fbk-send{background:var(--purple,#512888);border-color:var(--purple,#512888);color:#fff}'
    + '.fbk-proto{margin-top:10px!important;font-size:12.5px;color:var(--muted,#6b6772)}'
    + '@media (max-width:560px){.fbk-topics{grid-template-columns:1fr}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  /* 1. Start a thread, in the ribbon */
  var mw = document.querySelector('a.mywork:not([hidden])');
  if (mw && !document.querySelector('.hc-thread')) {
    var a = document.createElement('a');
    a.className = 'hc-thread';
    a.href = 'community.html?t=other#cm-ask';
    a.title = 'Ask the CNAP community a question, look for a collaborator, or post a position';
    a.innerHTML = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2.5 3.5h11v7h-6l-3 2.5v-2.5h-2z"/></svg><span>Start a thread</span>';
    mw.parentNode.insertBefore(a, mw);
  }

  /* 2. Page feedback */
  if (document.querySelector('.fbk-open')) return;
  var b = document.createElement('button');
  b.type = 'button'; b.className = 'fbk-open'; b.setAttribute('aria-haspopup', 'dialog');
  b.title = 'Tell us how this page could be better: its design, its wording, its logic, its speed, or a fun idea.';
  b.textContent = 'Page feedback';
  var topics = [['design', 'Design and look'], ['clarity', 'Clarity of wording or directions'], ['logic', 'Logic or flow'], ['speed', 'Speed and efficiency'], ['fun', 'Fun and motivating touches'], ['broken', 'Something is broken'], ['other', 'Something else']];
  var d = document.createElement('dialog');
  d.className = 'fbk'; d.setAttribute('aria-labelledby', 'fbk-h');
  d.innerHTML = '<form method="dialog" class="fbk-form"><h2 id="fbk-h">How could this page be better?</h2>'
    + '<p class="fbk-sub">Your note goes to the CNAP evaluation team, along with the page you are on.</p><p class="fbk-sub">Big ideas and small fixes are equally welcome.</p>'
    + '<fieldset class="fbk-topics"><legend>What is it about?</legend>' + topics.map(function (t) { return '<label><input type="radio" name="topic" value="' + t[0] + '"> ' + t[1] + '</label>'; }).join('') + '</fieldset>'
    + '<fieldset class="fbk-rate"><legend>How is this page overall? (optional)</legend>' + [1, 2, 3, 4, 5].map(function (n) { return '<label title="' + (n === 1 ? 'Poor' : n === 5 ? 'Excellent' : n + ' of 5') + '"><input type="radio" name="rating" value="' + n + '"><span>' + n + '</span></label>'; }).join('') + '</fieldset>'
    + '<label class="fbk-l" for="fbk-c">Your note</label><textarea id="fbk-c" name="comment" rows="4" placeholder="For example: the dates on this page are hard to find."></textarea>'
    + '<p class="fbk-msg" role="status"></p>'
    + '<div class="fbk-row"><button type="button" class="fbk-send">Send my note</button><button type="button" class="fbk-close">Cancel</button></div>'
    + '<p class="fbk-proto">Prototype. In the Hub, this note is saved for the evaluation team. Here, nothing is sent.</p></form>';
  document.body.appendChild(b); document.body.appendChild(d);
  var msg = d.querySelector('.fbk-msg');
  b.addEventListener('click', function () { msg.textContent = ''; if (d.showModal) d.showModal(); else d.setAttribute('open', ''); });
  d.querySelector('.fbk-close').addEventListener('click', function () { d.close ? d.close() : d.removeAttribute('open'); });
  d.querySelector('.fbk-send').addEventListener('click', function () {
    var f = d.querySelector('form'), topic = f.querySelector('input[name="topic"]:checked');
    if (!topic || !f.comment.value.trim()) { msg.textContent = 'Choose what it is about and write a few words.'; return; }
    msg.textContent = 'Thank you. In the prototype, nothing was sent.';
    f.reset(); setTimeout(function () { d.close ? d.close() : d.removeAttribute('open'); }, 1600);
  });
})();

/* Site navigation (MW 2026-11-15): every page has a home under one top-ribbon item, shown in a dropdown. */
(function () {
  var MAP = [
    ['Home', 'index.html', null],
    ['Reporting', 'reporting.html', [['My tasks', 'reporting.html'], ['My history', 'reporting-history.html']]],
    ['Research', 'research.html', [['Research at CNAP', 'research.html'], ['Research stories', 'story.html']]],
    ['Events', 'events.html', [['Events overview', 'events.html'], ['NeuroSync', 'neurosync.html'], ['The 2027 Site Visit', 'sitevisit.html']]],
    ['Funding', 'funding.html', [['Funding opportunities', 'funding.html'], ['Grant resources and toolkit', 'funding-resources.html'], ['Funding news', 'funding-news.html']]],
    ['Community', 'community.html', [['Community', 'community.html'], ['Member directory', 'community.html#cm-dir'], ['Alumni', 'community.html#cm-alum']]],
    ['Resources', 'core-bn.html', [['Behavioral Neuroscience Core', 'core-bn.html'], ['Cognitive Neuroscience Core', 'core-cn.html'], ['Neuroinformatics Core', 'core-ni.html'], ['Mentor guide', 'mentor.html'], ['Mentee guide', 'mentee.html']]]
  ];
  var here = (location.pathname.split('/').pop() || 'index.html');
  if (/^reporting-\d+/.test(here)) here = 'reporting.html';
  function inSec(sec) { return sec[1] === here || (sec[2] || []).some(function (x) { return x[1].split('#')[0] === here; }); }
  var css = ''
    + '.hn{display:flex;gap:4px;margin-left:12px;position:relative}'
    + '.hn-it{position:relative}'
    + '.hn-b,.hn a.hn-b{all:unset;box-sizing:border-box;display:inline-flex;align-items:center;gap:6px;padding:8px 12px;border-radius:8px;color:var(--ink-2,#45414c);font:500 15px/1.2 var(--sans,system-ui,sans-serif);cursor:pointer;white-space:nowrap}'
    + '.hn-b:hover{background:var(--band,#f2efe9);color:var(--ink,#1d1b21)}'
    + '.hn-b:focus-visible{outline:2px solid var(--purple,#512888);outline-offset:2px}'
    + '.hn-b[aria-current="page"],.hn-it.is-here>.hn-b{color:var(--purple,#512888);background:var(--purple-tint,#efe8f8)}'
    + '.hn-b svg{width:10px;height:10px;fill:none;stroke:currentColor;stroke-width:1.8;transition:transform .15s}'
    + '.hn-b[aria-expanded="true"] svg{transform:rotate(180deg)}'
    + '.hn-p{position:absolute;left:0;top:calc(100% + 8px);z-index:80;min-width:250px;padding:8px;border-radius:12px;background:var(--surface,#fff);border:1px solid var(--line,#e6e3ea);box-shadow:0 18px 40px -16px rgba(40,20,70,.3)}'
    + '.hn-p[hidden]{display:none}'
    + '.hn-p a{display:block;padding:9px 12px;border-radius:8px;color:var(--ink,#1d1b21);text-decoration:none;font:400 15px/1.3 var(--sans,system-ui,sans-serif)}'
    + '.hn-p a:hover,.hn-p a:focus-visible{background:var(--band,#f2efe9);outline:0}'
    + '.hn-p a[aria-current="page"]{color:var(--purple,#512888);font-weight:600;background:var(--purple-tint,#efe8f8)}'
    + '.hn-p a.hn-sep{margin-top:6px;border-top:1px solid var(--line,#e6e3ea);border-radius:0 0 8px 8px;padding-top:12px}'
    + '.hn-m{display:none}'
    + '@media (min-width:981px) and (max-width:1120px){.hn{gap:0;margin-left:4px}.hn-b,.hn a.hn-b{padding:8px 8px;font-size:14px}}'
    + '.hn-mp{position:fixed;left:0;right:0;top:64px;bottom:0;z-index:90;overflow:auto;padding:12px max(16px,env(safe-area-inset-left,0px)) 40px;background:var(--surface,#fff)}'
    + '.hn-mp h3{margin:16px 12px 4px;font:600 13px/18px var(--sans,system-ui,sans-serif);color:var(--muted,#6b6772)}'
    + '.hn-mp a{display:block;padding:12px;border-bottom:1px solid var(--line,#e6e3ea);color:var(--ink,#1d1b21);text-decoration:none;font-size:16px}'
    + '.hn-mp a[aria-current="page"]{color:var(--purple,#512888);font-weight:600}'
    + 'header .brand span,header .brand b{white-space:nowrap}@media (max-width:420px){header .brand small{display:none}}'
    + 'header.f-thread-icon .hc-thread span{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}header.f-thread-icon .hc-thread{padding:0 11px}'
    + 'header.f-tight .hn{gap:0;margin-left:4px}header.f-tight .hn-b{padding:8px 7px!important;font-size:14px!important}header.f-tight .wrap{gap:16px}'
    + 'header.f-search-icon .search{width:44px!important;padding:0!important;justify-content:center}header.f-search-icon .search>:not(svg){display:none}'
    + 'header.f-thread-off .hc-thread{display:none}'
    + 'header.f-menu .hn{display:none!important}header.f-menu .hn-m{all:unset;box-sizing:border-box;display:inline-flex;align-items:center;min-height:40px;padding:0 14px;border-radius:8px;border:1px solid var(--line-2,#d5d3d9);font:500 15px/1 var(--sans,system-ui,sans-serif);color:var(--ink,#1d1b21);cursor:pointer}'
    + 'header.f-mini .brand small,header.f-mini .mywork{display:none!important}header.f-mini .wrap{gap:10px}'
    + 'header.f-logo .brand>span{display:none}'
    + '.hn-acct{position:relative}'
    + '.hn-acct>.hn-av{all:unset;box-sizing:border-box;display:grid;place-items:center;width:40px;height:40px;border-radius:50%;background:var(--purple-tint,#efe8f8);color:var(--purple-ink,#3c1d66);font:600 14px/1 var(--sans,system-ui,sans-serif);cursor:pointer}'
    + '.hn-acct>.hn-av:focus-visible{outline:2px solid var(--purple,#512888);outline-offset:2px}'
    + '.hn-acct .hn-p{left:auto;right:0}'
    + '.hn-acct .hn-who{margin:4px 12px 8px;font:500 15px/1.3 var(--sans,system-ui,sans-serif);color:var(--ink,#1d1b21)}.hn-acct .hn-who span{display:block;font-size:13px;color:var(--muted,#6b6772);font-weight:400}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  var chev = '<svg viewBox="0 0 10 10" aria-hidden="true"><path d="M2 3.5l3 3 3-3"/></svg>';
  var nav = document.querySelector('header nav[aria-label="Main"]');
  if (!nav) return;
  var hn = document.createElement('nav'); hn.className = 'hn nav'; hn.setAttribute('aria-label', 'Main');
  var panels = [];
  function closeAll(except) { panels.forEach(function (x) { if (x !== except) { x.p.hidden = true; x.b.setAttribute('aria-expanded', 'false'); } }); }
  MAP.forEach(function (sec, i) {
    var it = document.createElement('div'); it.className = 'hn-it' + (inSec(sec) ? ' is-here' : '');
    if (!sec[2]) {
      var a = document.createElement('a'); a.className = 'hn-b'; a.href = sec[1]; a.textContent = sec[0];
      if (here === 'index.html') a.setAttribute('aria-current', 'page');
      it.appendChild(a);
    } else {
      var b = document.createElement('button'); b.type = 'button'; b.className = 'hn-b'; b.setAttribute('aria-expanded', 'false'); b.setAttribute('aria-controls', 'hn-p' + i);
      b.innerHTML = sec[0] + chev;
      var p = document.createElement('div'); p.className = 'hn-p'; p.id = 'hn-p' + i; p.hidden = true;
      sec[2].forEach(function (x) { var a = document.createElement('a'); a.href = x[1]; a.textContent = x[0]; if (x[1] === here) a.setAttribute('aria-current', 'page'); p.appendChild(a); });
      b.addEventListener('click', function (e) { e.stopPropagation(); var open = b.getAttribute('aria-expanded') === 'true'; closeAll(); if (!open) { p.hidden = false; b.setAttribute('aria-expanded', 'true'); } });
      panels.push({ b: b, p: p });
      it.appendChild(b); it.appendChild(p);
    }
    hn.appendChild(it);
  });
  nav.parentNode.replaceChild(hn, nav);
  /* phones: one menu with every group */
  var tools = document.querySelector('header .tools');
  if (tools) {
    var mb = document.createElement('button'); mb.type = 'button'; mb.className = 'hn-m'; mb.textContent = 'Menu'; mb.setAttribute('aria-expanded', 'false');
    var mp = document.createElement('div'); mp.className = 'hn-mp'; mp.hidden = true;
    MAP.forEach(function (sec) {
      var h = document.createElement('h3'); h.textContent = sec[0]; mp.appendChild(h);
      (sec[2] || [[sec[0], sec[1]]]).forEach(function (x) { var a = document.createElement('a'); a.href = x[1]; a.textContent = x[0]; if (x[1] === here) a.setAttribute('aria-current', 'page'); mp.appendChild(a); });
    });
    mb.addEventListener('click', function () { var o = mb.getAttribute('aria-expanded') === 'true'; mp.style.top = Math.max(0, mb.closest('header').getBoundingClientRect().bottom) + 'px'; mb.setAttribute('aria-expanded', String(!o)); mp.hidden = o; mb.textContent = o ? 'Menu' : 'Close'; });
    tools.insertBefore(mb, tools.firstChild); document.body.appendChild(mp);
    /* account menu on the initials */
    var av = tools.querySelector('.avatar');
    if (av && !av.getAttribute('aria-controls')) {
      var wrap = document.createElement('div'); wrap.className = 'hn-acct';
      var ab = document.createElement('button'); ab.type = 'button'; ab.className = 'hn-av'; ab.textContent = av.textContent.trim(); ab.setAttribute('aria-expanded', 'false'); ab.setAttribute('aria-controls', 'hn-acct'); ab.setAttribute('aria-label', (av.getAttribute('aria-label') || 'Your account') + ': profile and settings');
      var ap = document.createElement('div'); ap.className = 'hn-p'; ap.id = 'hn-acct'; ap.hidden = true;
      var nm = (av.getAttribute('aria-label') || '').split(':')[0];
      ap.innerHTML = (nm ? '<p class="hn-who">' + nm + '<span>Signed in</span></p>' : '') + '<a href="mentee-profile.html">Your profile</a><a href="#" data-proto>Change password</a><a href="#" data-proto class="hn-sep">Log out</a>';
      ap.querySelectorAll('[data-proto]').forEach(function (a) { a.addEventListener('click', function (e) { e.preventDefault(); }); a.title = 'Not part of the prototype'; });
      ab.addEventListener('click', function (e) { e.stopPropagation(); var open = ab.getAttribute('aria-expanded') === 'true'; closeAll(); if (!open) { ap.hidden = false; ab.setAttribute('aria-expanded', 'true'); } });
      panels.push({ b: ab, p: ap });
      wrap.appendChild(ab); wrap.appendChild(ap); av.parentNode.replaceChild(wrap, av);
    }
  }
  document.addEventListener('click', function (e) { if (!e.target.closest('.hn-p')) closeAll(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeAll(); } });
  /* one fit for the whole ribbon: step down until nothing runs past the edge */
  var hdr = hn.closest('header');
  var STEPS = ['f-thread-icon', 'f-tight', 'f-search-icon', 'f-thread-off', 'f-menu', 'f-mini', 'f-logo'];
  function over() {
    var w = document.documentElement.clientWidth, bad = false;
    hdr.querySelectorAll('.wrap > *, .tools > *').forEach(function (el) { if (el.offsetParent !== null && el.getBoundingClientRect().right > w - 8) bad = true; });
    return bad || hdr.scrollWidth > hdr.clientWidth + 1;
  }
  function fit() {
    STEPS.forEach(function (c) { hdr.classList.remove(c); });
    if (innerWidth <= 980) hdr.classList.add('f-menu');
    for (var i = 0; i < STEPS.length && over(); i++) hdr.classList.add(STEPS[i]);
  }
  fit(); addEventListener('resize', fit); addEventListener('load', fit); setTimeout(fit, 300);
})();
