/* Shared prototype chrome for every Member Hub page (MW 2026-11-14):
   1. "Start a thread" in the top ribbon, next to My work.
   2. The Page feedback button and dialog, matching the Django app's _feedback.html.
   Prototype only: the feedback dialog sends nothing. */
(function () {
  var css = ''
    + '.hc-thread{display:inline-flex;align-items:center;gap:8px;min-height:40px;padding:0 14px;border-radius:999px;border:1px solid var(--line-2,#d5d3d9);background:transparent;color:var(--purple-ink,#3c1d66);font:500 14.5px/1 var(--sans,system-ui,sans-serif);text-decoration:none;white-space:nowrap}'
    + '.hc-thread:hover{background:var(--purple-tint,#efe8f8)}'
    + '.hc-thread svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}'
    + '@media (max-width:760px){.hc-thread span{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}.hc-thread{padding:0 11px}}'
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
