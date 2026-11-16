/* Shared prototype chrome for every Member Hub page (MW 2026-11-14):
   1. "Start a thread" in the top ribbon, next to My work.
   2. The Page feedback button and dialog, matching the Django app's _feedback.html.
   Prototype only: the feedback dialog sends nothing. */
(function () {
  var css = ''
    + '.hc-thread{display:inline-flex;align-items:center;gap:8px;min-height:40px;padding:0 14px;border-radius:999px;border:1px solid var(--line-2,#d5d3d9);background:transparent;color:var(--purple-ink,#3c1d66);font:500 14.5px/1 var(--sans,system-ui,sans-serif);text-decoration:none;white-space:nowrap}'
    + '@media (min-width:1300px){.tools:has(.hc-thread:not([hidden])) .search{width:190px}}'
    + '.hc-thread:hover{background:var(--purple-tint,#efe8f8)}'
    + 'header:has(.hn)>.wrap{max-width:none;padding-left:max(20px,env(safe-area-inset-left,0px));padding-right:max(20px,env(safe-area-inset-right,0px))}'
    + '.mywork{white-space:nowrap}'
    + '.hc-thread{background:var(--purple,#512888);border-color:var(--purple,#512888);color:#fff;font-weight:600}.hc-thread:hover{background:var(--purple-ink,#3c1d66)}header .hc-thread,header .hc-thread:hover,header .hc-thread:focus-visible,header .hc-thread:visited{color:#fff!important}'
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
    a.href = 'threads.html';
    a.title = 'Opens Threads: ask the CNAP community a question, look for a collaborator, or answer a colleague';
    if (/threads\.html$/.test(location.pathname)) a.addEventListener('click', function (e) { var d = document.querySelector('.cm-compose'); if (!d) return; e.preventDefault(); try { d.showModal(); } catch (x) { d.setAttribute('open', ''); } });
    a.innerHTML = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2.5 3.5h11v7h-6l-3 2.5v-2.5h-2z"/></svg><span>Start a thread</span>';
    a.setAttribute('aria-label', 'Start a thread');
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
    + '<fieldset class="fbk-topics"><legend>What is the note about?</legend>' + topics.map(function (t) { return '<label><input type="radio" name="topic" value="' + t[0] + '"> ' + t[1] + '</label>'; }).join('') + '</fieldset>'
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
    ['Reporting', 'reporting.html', [['My tasks', 'reporting.html', 'Surveys and reports due this session'], ['My history', 'reporting-history.html', 'Everything you have submitted']]],
    ['Research', 'research.html', [['Research stories', 'research.html', 'Work from the Center’s pilot projects, cores, and investigators'], ['Suggest a story', 'mailto:cnap@ksu.edu?subject=Story%20idea%20for%20Research%20at%20CNAP', 'Tell the CNAP team about a milestone, paper, or person to profile']]],
    ['Events', 'events.html', [['Events calendar', 'events.html', 'Every Center event, deadline, and campus date'], ['NeuroSync', 'neurosync.html', 'The Wednesday speaker series'], ['The 2027 Site Visit', 'sitevisit.html', 'May 25 and 26, 2027']]],
    ['Funding', 'funding.html', [['Funding opportunities', 'funding.html', 'Picked for you, and relevant to most members'], ['Grant resources and toolkit', 'funding-resources.html', 'Weigh an opportunity and get help with a draft'], ['Funding news', 'funding-news.html', 'News from sponsors, and events and talks']]],
    ['Community', 'community.html', [['Community', 'community.html', 'Achievements, people, and ways to connect'], ['Threads', 'threads.html', 'Questions answered by members who have the experience'], ['Member directory', 'community.html#cm-dir', 'Find a colleague or a type of expertise'], ['Alumni', 'community.html#cm-alum', 'Where former members are now']]],
    ['Resources', 'core-bn.html', [['Behavioral Neuroscience Core', 'core-bn.html', 'Services, equipment, and how to book'], ['Cognitive Neuroscience Core', 'core-cn.html', 'Services, equipment, and how to book'], ['Neuroinformatics Core', 'core-ni.html', 'Data, analysis, and consultation'], ['Mentor guide', 'mentor.html', 'For mentors of CNAP investigators'], ['Mentee guide', 'mentee.html', 'For pilot and project investigators']]]
  ];
  var here = (location.pathname.split('/').pop() || 'index.html');
  if (/^reporting-\d+/.test(here)) here = 'reporting.html';
  if (here === 'thread.html') here = 'threads.html';
  if (here === 'sitevisit-2026.html') here = 'sitevisit.html';
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
    + 'header .hn .hn-p{min-width:320px;padding:6px;display:grid;gap:2px}'
    + 'header .hn .hn-p[hidden],.hn-acct .hn-p[hidden]{display:none!important}'
    + 'header .hn .hn-p a,header .hn .hn-p a:hover{display:grid;gap:1px;padding:10px 14px 10px 16px;border-radius:8px;border:0;box-shadow:none;text-decoration:none;background:transparent;position:relative}'
    + 'header .hn .hn-p a b{font:500 15px/21px var(--sans,system-ui,sans-serif);color:var(--ink,#1d1b21)}'
    + 'header .hn .hn-p a small{font:400 13px/18px var(--sans,system-ui,sans-serif);color:var(--muted,#6b6772)}'
    + 'header .hn .hn-p a:hover,header .hn .hn-p a:focus-visible{background:var(--band,#f2efe9)}'
    + 'header .hn .hn-p a+a{margin-top:0}header .hn .hn-p a+a::before{content:"";position:absolute;left:16px;right:14px;top:-1px;height:1px;background:var(--line,#e6e3ea)}'
    + 'header .hn .hn-p a:hover::before,header .hn .hn-p a:hover+a::before,header .hn .hn-p a[aria-current="page"]::before,header .hn .hn-p a[aria-current="page"]+a::before{opacity:0}'
    + 'header .hn .hn-p a[aria-current="page"]{background:var(--purple-tint,#efe8f8);box-shadow:inset 3px 0 0 var(--purple,#512888)}'
    + 'header .hn .hn-p a[aria-current="page"] b{color:var(--purple-ink,#3c1d66);font-weight:600}'
    + 'header .hn .hn-p a.hn-gap{margin-top:8px}header .hn .hn-p a.hn-gap::before{top:-5px;left:6px;right:6px;background:var(--line-2,#d5d3d9)}'
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
      if (here === sec[1]) a.setAttribute('aria-current', 'page');
      it.appendChild(a);
    } else {
      var b = document.createElement('button'); b.type = 'button'; b.className = 'hn-b'; b.setAttribute('aria-expanded', 'false'); b.setAttribute('aria-controls', 'hn-p' + i);
      b.innerHTML = sec[0] + chev;
      var p = document.createElement('div'); p.className = 'hn-p'; p.id = 'hn-p' + i; p.hidden = true;
      sec[2].forEach(function (x, k) { var a = document.createElement('a'); a.href = x[1]; a.innerHTML = '<b></b><small></small>'; a.firstChild.textContent = x[0]; a.lastChild.textContent = x[2] || ''; if (x[1] === here) a.setAttribute('aria-current', 'page'); if (sec[0] === 'Resources' && k === 3) a.className = 'hn-gap'; p.appendChild(a); });
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
      ap.innerHTML = (nm ? '<p class="hn-who">' + nm + '<span>Signed in</span></p>' : '') + '<a href="mentee-profile.html">Your profile</a><a href="#" data-proto title="Not part of the prototype.">Change password</a><a href="#" data-proto class="hn-sep" title="Not part of the prototype.">Log out</a>';
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
  var STEPS = ['f-tight', 'f-search-icon', 'f-thread-icon', 'f-thread-off', 'f-menu', 'f-mini', 'f-logo'];
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

/* Every link has a hover description (CNAP Hub Design Rules, Buttons and links). Links without one get a plain description of where they go. */
(function () {
  var NAMES = {'index.html':'Home','reporting.html':'My tasks in Reporting','reporting-history.html':'My history in Reporting','research.html':'Research at CNAP','story.html':'the research story','events.html':'Events','neurosync.html':'NeuroSync','sitevisit.html':'the 2027 Site Visit page','funding.html':'Funding opportunities','funding-resources.html':'Grant resources','funding-news.html':'Funding news','community.html':'Community','threads.html':'Threads','thread.html':'the thread','core-bn.html':'the Behavioral Neuroscience Core page','core-cn.html':'the Cognitive Neuroscience Core page','core-ni.html':'the Neuroinformatics Core page','mentor.html':'the mentor guide','mentee.html':'the mentee guide','mentee-profile.html':'the profile page'};
  function run() {
    document.querySelectorAll('a[href]').forEach(function (a) {
      if (a.title || a.getAttribute('aria-describedby')) return;
      var h = a.getAttribute('href') || '', t = '';
      if (/^mailto:/.test(h)) t = 'Starts an email to ' + h.slice(7).split('?')[0] + '.';
      else if (/^https?:/.test(h)) { try { t = 'Opens ' + new URL(h).hostname.replace(/^www\./, '') + ' in a new tab.'; } catch (e) {} }
      else if (h.charAt(0) === '#' && h.length > 1) { var el = document.getElementById(h.slice(1)); var hd = el && (el.querySelector('h2,h3') || el); if (hd && hd.textContent.trim()) t = 'Goes to ' + hd.textContent.trim().replace(/\s+/g, ' ').slice(0, 60) + ' on this page.'; }
      else { var f = h.split('#')[0].split('?')[0]; if (NAMES[f]) t = 'Opens ' + NAMES[f] + '.'; }
      if (t) a.title = t;
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
  setTimeout(run, 500);
})();
document.querySelectorAll("a[data-proto]").forEach(function(a){a.addEventListener("click",function(e){e.preventDefault();});});

/* Hover and focus descriptions in the Hub's own style, in place of the browser's plain white boxes (MW 2026-11-15) */
(function () {
  if (window.__hubTips) return; window.__hubTips = 1;
  var st = document.createElement('style');
  st.textContent = '.hub-tip{position:fixed;z-index:1000;max-width:min(300px,calc(100vw - 24px));padding:9px 12px;border-radius:10px;background:#22132f;color:#f6f2fa;'
    + 'font:500 13.5px/19px "Inter Hub","Inter",system-ui,-apple-system,"Segoe UI",sans-serif;letter-spacing:.005em;box-shadow:0 10px 28px -10px rgba(20,11,26,.55),0 0 0 1px rgba(255,255,255,.22);'
    + 'pointer-events:none;opacity:0;transform:translateY(3px);transition:opacity .14s ease,transform .14s ease;text-wrap:pretty}'
    + '.hub-tip.on{opacity:1;transform:none}'
    + '.hub-tip::after{content:"";position:absolute;left:var(--ax,50%);width:10px;height:10px;background:inherit;transform:translateX(-50%) rotate(45deg);border-radius:2px}'
    + '.hub-tip[data-side="top"]::after{bottom:-4px}.hub-tip[data-side="bottom"]::after{top:-4px}'
    + '@media (prefers-reduced-motion:reduce){.hub-tip{transition:none}}';
  document.head.appendChild(st);
  var tip = document.createElement('div'); tip.className = 'hub-tip'; tip.setAttribute('role', 'tooltip'); tip.id = 'hub-tip';
  var cur = null, timer = 0;
  function host(el) { if (el && el.closest && el.closest('.hr-rail, .otp, .spine')) return null; while (el && el.nodeType === 1) { if (el.hasAttribute && (el.hasAttribute('title') || el.hasAttribute('data-tip'))) return el; el = el.parentElement; } return null; }
  function claim(el) { var t = el.getAttribute('title'); if (t) { el.setAttribute('data-tip', t); el.removeAttribute('title'); } return el.getAttribute('data-tip'); }
  function show(el) {
    var text = claim(el); if (!text) return;
    if (!tip.parentNode) document.body.appendChild(tip);
    cur = el; tip.textContent = text; tip.classList.remove('on'); tip.style.left = '0px'; tip.style.top = '0px';
    el.setAttribute('aria-describedby', 'hub-tip');
    var r = el.getBoundingClientRect(), w = tip.offsetWidth, h = tip.offsetHeight, gap = 10;
    var side = r.top - h - gap > 8 ? 'top' : 'bottom';
    var cx = r.left + r.width / 2, left = Math.max(12, Math.min(innerWidth - w - 12, cx - w / 2));
    var top = side === 'top' ? r.top - h - gap : r.bottom + gap;
    tip.dataset.side = side; tip.style.left = left + 'px'; tip.style.top = top + 'px';
    tip.style.setProperty('--ax', Math.max(14, Math.min(w - 14, cx - left)) + 'px');
    requestAnimationFrame(function () { tip.classList.add('on'); });
  }
  function hide() { clearTimeout(timer); if (cur) cur.removeAttribute('aria-describedby'); cur = null; tip.classList.remove('on'); }
  document.addEventListener('mouseover', function (e) {
    var el = host(e.target); if (el === cur) return;
    if (el) claim(el);
    hide(); if (!el) return;
    timer = setTimeout(function () { show(el); }, 350);
  });
  document.addEventListener('mouseout', function (e) { var el = host(e.target); if (el && el === cur && !el.contains(e.relatedTarget)) hide(); else if (el && !el.contains(e.relatedTarget)) clearTimeout(timer); });
  document.addEventListener('focusin', function (e) { var el = host(e.target); if (el && e.target.matches && e.target.matches(':focus-visible')) show(el); });
  document.addEventListener('focusout', hide);
  addEventListener('scroll', hide, { passive: true });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') hide(); });
})();

/* A small confirmation that says what just happened (MW 2026-11-15) */
(function () {
  if (window.hubToast) return;
  var st = document.createElement('style');
  st.textContent = '.hub-toast{position:fixed;left:50%;bottom:calc(24px + env(safe-area-inset-bottom,0px));z-index:1001;max-width:min(460px,calc(100vw - 32px));padding:12px 16px 12px 14px;border-radius:12px;background:#22132f;color:#fff;'
    + 'font:500 14.5px/21px "Inter Hub","Inter",system-ui,-apple-system,"Segoe UI",sans-serif;box-shadow:0 16px 36px -14px rgba(20,11,26,.6),0 0 0 1px rgba(255,255,255,.12);'
    + 'display:flex;gap:10px;align-items:flex-start;transform:translate(-50%,12px);opacity:0;transition:opacity .18s ease,transform .18s ease}'
    + '.hub-toast.on{opacity:1;transform:translate(-50%,0)}.hub-toast b{font-weight:700}'
    + '.hub-toast svg{flex:none;width:18px;height:18px;margin-top:1px;fill:none;stroke:#d4bdf6;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}'
    + '@media (prefers-reduced-motion:reduce){.hub-toast{transition:none}}';
  document.head.appendChild(st);
  var el = document.createElement('div'); el.className = 'hub-toast'; el.setAttribute('role', 'status'); el.setAttribute('aria-live', 'polite');
  var t = 0;
  window.hubToast = function (html) {
    if (!el.parentNode) document.body.appendChild(el);
    el.innerHTML = '<svg viewBox="0 0 18 18" aria-hidden="true"><path d="M4 9.5l3.2 3L14 5.5"/></svg><span>' + html + '</span>';
    el.classList.remove('on'); void el.offsetWidth; el.classList.add('on');
    clearTimeout(t); t = setTimeout(function () { el.classList.remove('on'); }, 4200);
  };
})();

/* Thread email preferences (prototype: kept in this browser only). MW 2026-11-15: let people choose how often, and unfollow from the email. */
(function () {
  var LAB = { daily: 'one email a day', weekly: 'one email a week', mine: 'emails only about your own questions', none: 'no emails' };
  window.hubThreadPref = function (v) {
    try { if (v) localStorage.setItem('hub-thread-mail', v); return localStorage.getItem('hub-thread-mail') || 'weekly'; } catch (e) { return v || 'weekly'; }
  };
  var CH = ' <a href="threads.html#th-mail" style="color:#d4bdf6;text-decoration:underline;text-underline-offset:3px">Change</a>';
  window.hubThreadMsg = function (kind) {
    var p = hubThreadPref(), l = LAB[p];
    var tail = p === 'none' ? ' You chose no emails, so please check Threads for replies.' : p === 'mine' ? ' You chose emails only about your own questions, so this thread won’t email you.' : ' You’ll hear about new replies in ' + l + ', and they show on your Home page.';
    if (kind === 'follow') return '<b>Following.</b>' + tail + CH;
    if (kind === 'unfollow') return '<b>Unfollowed.</b> You won’t hear about new replies to this thread.';
    if (kind === 'reply') return '<b>Your reply is posted.</b> You now follow this thread.' + tail + CH;
    if (kind === 'post') return '<b>Your thread is posted.</b> ' + (p === 'none' ? 'You chose no emails, so please check Threads for replies.' : 'We’ll email you when someone first replies' + (p === 'daily' || p === 'weekly' ? ', then ' + l + ' after that.' : '.')) + CH;
    if (kind === 'saved') return '<b>Saved.</b> ' + (p === 'none' ? 'No thread emails. New replies still show on your Home page.' : 'You’ll get ' + l + '. The first reply to your own question still comes right away.' ) + ' In the prototype, nothing is sent.';
    return '';
  };
})();

/* "On this page" dot rail for pages that do not have one yet, matching Home (MW 2026-11-15) */
(function () {
  function build() {
    if (document.querySelector('.otp, .spine, .hr-rail')) return;
    var main = document.querySelector('main'); if (!main) return;
    var marked = [].slice.call(main.querySelectorAll('[data-rail]'));
    var hs = marked.length ? marked : [].slice.call(main.querySelectorAll('h2')).filter(function (h) {
      if (h.closest('dialog, aside, .th-side, .tp-side, [hidden], .cm-day, .ev-cal, .sr')) return false;
      var t = h.textContent.trim(); return t && t.length < 60 && h.getClientRects().length;
    });
    if (hs.length < 3) return;
    var st = document.createElement('style');
    st.textContent = '.hr-rail{position:fixed;z-index:30;left:max(10px,env(safe-area-inset-left,0px));top:124px;width:28px;padding:10px 0;box-sizing:border-box;border-radius:12px;border:1px solid transparent;background:transparent;transition:width .2s ease,background-color .2s,box-shadow .2s,border-color .2s;font-family:"Inter Hub","Inter",system-ui,sans-serif}'
      + '.hr-rail ol{position:relative;list-style:none;margin:0;padding:0}'
      + '.hr-rail ol::before{content:"";position:absolute;left:13px;top:12px;bottom:12px;width:1px;background:var(--line-2,#d3cdc3)}'
      + '.hr-rail a{position:relative;display:block;height:26px;padding:3px 12px 3px 30px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;color:transparent;font-size:14px;line-height:20px;text-decoration:none}'
      + '.hr-rail a::before{content:"";position:absolute;left:9px;top:9px;width:7px;height:7px;border-radius:50%;background:var(--surface,#fff);border:1.5px solid var(--line-2,#d3cdc3);transition:all .25s}'
      + '.hr-rail a.seen::before{border-color:var(--purple,#512888)}'
      + '.hr-rail a[aria-current="true"]::before{background:var(--purple,#512888);border-color:var(--purple,#512888);box-shadow:0 0 0 4px rgba(81,40,136,.14)}'
      + '.hr-rail .hr-h{display:none;margin:0 0 6px;padding:0 16px 10px 14px;border-bottom:1px solid var(--line,#e4e0d8);font:500 19px/24px "Lora Hub","Lora",Georgia,serif;color:var(--ink,#1d1b21)}'
      + '.hr-rail:hover,.hr-rail:focus-within{width:250px;padding:16px 0 10px;background:var(--surface,#fff);border-color:var(--line,#e4e0d8);box-shadow:0 18px 40px -18px rgba(29,27,33,.3)}'
      + '.hr-rail:hover .hr-h,.hr-rail:focus-within .hr-h{display:block}'
      + '.hr-rail:hover a,.hr-rail:focus-within a{color:var(--ink-2,#423e48);height:auto;white-space:normal;padding-top:6px;padding-bottom:6px}'
      + '.hr-rail:hover a:hover,.hr-rail:focus-within a:hover{color:var(--purple,#512888)}'
      + '.hr-rail:hover a[aria-current="true"],.hr-rail:focus-within a[aria-current="true"]{color:var(--purple-ink,#3c1d66);font-weight:600}'
      + '.hr-rail:hover a::before,.hr-rail:focus-within a::before{top:12px}'
      + '@media (max-width:1180px){.hr-rail{display:none}}@media (prefers-reduced-motion:reduce){.hr-rail,.hr-rail a::before{transition:none}}';
    document.head.appendChild(st);
    var nav = document.createElement('nav'); nav.className = 'hr-rail'; nav.setAttribute('aria-label', 'Sections on this page');
    var ol = document.createElement('ol'), links = [];
    hs.forEach(function (h, i) {
      if (!h.id) h.id = 'sec-' + (i + 1);
      var li = document.createElement('li'), a = document.createElement('a');
      a.href = '#' + h.id; a.textContent = h.getAttribute('data-rail') || h.textContent.replace(/\s+/g, ' ').trim();
      a.addEventListener('click', function (e) { e.preventDefault(); var y = h.getBoundingClientRect().top + scrollY - 110; scrollTo({ top: y, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' }); h.classList.remove('th-bounce'); setTimeout(function () { void h.offsetWidth; h.classList.add('th-bounce'); }, 450); });
      li.appendChild(a); ol.appendChild(li); links.push(a);
    });
    var hh = document.createElement('p'); hh.className = 'hr-h'; hh.textContent = 'On this page';
    nav.appendChild(hh); nav.appendChild(ol); document.body.appendChild(nav);
    function spy() {
      var cur = 0; hs.forEach(function (h, i) { if (h.getBoundingClientRect().top < 200) cur = i; });
      links.forEach(function (a, i) { a.toggleAttribute('aria-current', i === cur); if (i === cur) a.setAttribute('aria-current', 'true'); a.classList.toggle('seen', i < cur); });
    }
    addEventListener('scroll', spy, { passive: true }); spy();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { setTimeout(build, 50); }); else setTimeout(build, 50);
})();
