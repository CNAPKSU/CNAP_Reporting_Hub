# Threads list page (MW 2026-11-15: "level this up"). Run from threads.py, which supplies BY, av, head, compose, foot, V.
ONE = 'Only one thread page is built in the prototype: Looking for an EEG collaborator.'
# key, title, topic, replies, activity, matched, why, unanswered, excerpt, repliers, group
T = [
 ('jl', 'Looking for an EEG collaborator', 'Finding a collaborator', 4, 'Active today', True, 'You record sleep EEG in your pilot project.', False,
  'For the R01, I would like to extend my overnight EEG study to adults over 65, and I am looking for someone who already works with older participants.', ['pr', 'ms', 'wz', 'ev'], 'week'),
 ('kb', 'Calibrating the eye tracker for participants who wear glasses', 'Methods and equipment', 0, 'Started today', False, '', True,
  'Reflections from lenses throw off calibration for about a third of my participants. Has anyone found settings or a routine that works?', [], 'week'),
 ('lp', 'Recruiting older adults: what has worked?', 'Recruiting', 3, 'Active yesterday', True, 'Your study recruits adults over 65.', False,
  'Flyers at the library brought in two people in a month. I would love to hear what has worked for other labs in Manhattan.', ['ms', 'pr', 'do'], 'week'),
 ('rg', 'Who has used the Beocat cluster for imaging?', 'Methods and equipment', 0, 'Started Wednesday', True, 'Your team moved your analysis pipeline onto Beocat.', True,
  'I am moving fMRI preprocessing onto Beocat and would like to hear how others set up storage and job arrays.', [], 'week'),
 ('hc', 'Office hours for mixed-effects models in R', 'Statistics', 6, 'Active Monday', False, '', False,
  'I am holding open office hours on Tuesdays this month for anyone fitting mixed-effects models. Bring your data and your questions.', ['jl', 'lp', 'na', 'om'], 'week'),
 ('pr', 'Has anyone applied for the Brain & Behavior Research Foundation Young Investigator Grant?', 'Funding', 2, 'Active Monday', True, 'You are weighing the same grant for next spring.', False,
  'I am deciding whether to apply in the spring round and would value a word from anyone who has been through it.', ['do', 'ev'], 'week'),
 ('sr', 'A journal club on fear extinction, starting in December', 'Events and groups', 5, 'Active last week', False, '', False,
  'Every other Thursday at noon, starting December 3. Students are especially welcome. Reply if you would like the reading list.', ['tb', 'om', 'kb', 'na'], 'earlier'),
 ('om', 'Housing rats on a reversed light cycle: tips for a new lab', 'Methods and equipment', 3, 'Active last week', False, '', False,
  'Our room switches to a reversed cycle in January. What should I know about lighting, checks, and handling?', ['tb', 'sr'], 'earlier'),
 ('ms', 'Sharing EEG caps between studies: cleaning and scheduling', 'Methods and equipment', 4, 'Active last week', True, 'You book EEG time in the Cognitive Neuroscience Core.', False,
  'A proposal for a shared cleaning log and booking buffer, so caps are dry and ready between sessions.', ['jl', 'na', 'pr'], 'earlier'),
 ('do', 'What I wish I had known before my first R01 submission', 'Funding', 9, 'Active November 2', True, 'Your R21 is due in 123 days.', False,
  'Five things I would do differently, from the aims page to the timing of letters. Please add your own.', ['ev', 'pr', 'rg', 'hc'], 'earlier'),
 ('na', 'Graduate student position: motor learning and EEG, spring 2027', 'Hiring', 1, 'Active October 30', False, '', False,
  'Posting for my advisor: a funded position running EEG sessions on motor learning, starting in January.', ['lp'], 'earlier'),
 ('wz', 'A template for data management plans that reviewers liked', 'Funding', 7, 'Active October 28', False, '', False,
  'A template from the Neuroinformatics Core, with notes on what reviewers asked about in the last cycle.', ['rg', 'hc', 'do', 'jl'], 'earlier'),
 ('tb', 'Tips for the new electrophysiology rig', 'Methods and equipment', 2, 'Active October 26', False, '', False,
  'The new rig is set up in the Behavioral Neuroscience Core. A few notes on grounding and booking.', ['sr', 'om'], 'earlier'),
 ('ev', 'How often do you meet with your mentee in the first year?', 'Mentoring', 8, 'Active October 21', False, '', False,
  'I meet my mentee every two weeks. Curious how other mentors pace the first year of a pilot.', ['sr', 'do', 'pr', 'hc'], 'earlier'),
]
exec(open('/tmp/claude-0/hubproto/gen/thread_data.py').read())
def _uniq(xs):
    o = []
    for x in xs:
        if x not in o and x != 'ao': o.append(x)
    return o
T = [(k, t, tp, len(REPLIES[k]), a, mt_, w, len(REPLIES[k]) == 0, ex, _uniq([r[0] for r in REPLIES[k]]), g) for (k, t, tp, r, a, mt_, w, un, ex, rs, g) in T]
# days since the thread started; threads Amara (the viewer) started or replied to; threads she follows
STARTED = {'jl': 6, 'kb': 0, 'lp': 9, 'rg': 3, 'hc': 12, 'pr': 5, 'sr': 14, 'om': 10, 'ms': 16, 'do': 21, 'na': 17, 'wz': 30, 'tb': 22, 'ev': 40}
MINE = {'lp', 'hc', 'do'}
FOLLOW = {'jl', 'ms', 'pr'}
TONE = {'Finding a collaborator': 'p', 'Methods and equipment': 't', 'Recruiting': 'a', 'Statistics': 'g', 'Funding': 'b', 'Events and groups': 'l', 'Hiring': 'a', 'Mentoring': 'p'}
TOPICS = sorted(set(t[2] for t in T))
def rep(n): return 'No replies yet' if n == 0 else ('1 reply' if n == 1 else f'{n} replies')

def row(k, t, tp, r, a, mt_, w, un, ex, rs, grp):
    href = url(k)
    pa = ''
    q = (t + ' ' + BY[k][2] + ' ' + tp + ' ' + ex).lower().replace('"', '')
    stack = ''.join(av(x, ' sm') for x in rs[:3])
    if un:
        right = '<div class="th-n th-n0"><span class="th-nn">0</span><span class="th-nl">Be the first</span></div>'
    else:
        right = f'<div class="th-n"><span class="th-nn">{r}</span><span class="th-nl">{"reply" if r == 1 else "replies"}</span><span class="th-stack" aria-hidden="true">{stack}</span></div>'
    why = f'<p class="th-why"><b>Matched to you.</b> {w}</p>' if w else ''
    mine = f'<p class="th-mine">You replied to this thread.</p>' if k in MINE else ''
    fol = k in FOLLOW
    fb = (f'<button type="button" class="th-fol" aria-pressed="{"true" if fol else "false"}" title="Follow this thread to get one email a day when it has new replies.">'
          f'<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 2.5h8v11l-4-3-4 3z"/></svg><span>{"Following" if fol else "Follow"}</span></button>')
    return (f'<li class="th-row{" th-un" if un else ""}" data-m="{"1" if mt_ else "0"}" data-u="{"1" if un else "0"}" data-tp="{tp}" data-g="{grp}" data-r="{r}" data-s="{STARTED[k]}" data-me="{"1" if k in MINE else "0"}" data-f="{"1" if fol else "0"}" data-q="{q}">'
            f'{av(k)}<div class="th-body"><p class="th-tp th-{TONE[tp]}">{tp}</p><h3 class="th-t"><a href="{href}"{pa}>{t}</a></h3><p class="th-ex">{ex}</p>'
            f'<div class="th-foot"><p class="th-meta">{BY[k][2]} · {rep(r)} · {a}</p>{fb}</div>{why}{mine}</div>{right}</li>')

week = [x for x in T if x[10] == 'week']
earlier = [x for x in T if x[10] == 'earlier']
rows = (f'<li class="th-grp" data-gh="week"><h2>This week</h2><span>{len(week)} threads</span></li>' + ''.join(row(*x) for x in week)
        + f'<li class="th-grp" data-gh="earlier"><h2>Earlier this fall</h2><span>{len(earlier)} threads</span></li>' + ''.join(row(*x) for x in earlier))
unans = [x for x in T if x[7]]
def spotcard(x):
    return (f'<li class="th-spot">{av(x[0])}<div class="th-spb"><p class="th-tp th-{TONE[x[2]]}">{x[2]}</p><h3><a href="{url(x[0])}">{x[1]}</a></h3><p class="th-ex">{x[8]}</p>'
            f'<p class="th-meta">Asked by {BY[x[0]][2]} · {x[4]}</p></div>'
            f'<a class="btn" href="{url(x[0])}#reply">Answer this thread</a></li>')
spot = ''.join(spotcard(x) for x in unans)
topics = ''.join(f'<li><button type="button" class="th-topic" data-topic="{x}" aria-pressed="false"><span class="th-dot th-{TONE[x]}" aria-hidden="true"></span><span class="th-tn">{x}</span><span class="th-c">{sum(1 for t in T if t[2] == x)}</span></button></li>' for x in TOPICS)
HELP = [('pr', 11), ('ev', 9), ('ms', 8), ('do', 7)]
helpful = ''.join(f'<li>{av(k, " sm")}<span class="th-hp"><b>{BY[k][2]}</b><small>{BY[k][3]}</small></span><span class="th-hc"><b>{n}</b> replies</span></li>' for k, n in HELP)
n_m = sum(1 for t in T if t[5])
n_u = len(unans)

ART = '''<svg class="th-art" viewBox="0 0 600 320" aria-hidden="true" preserveAspectRatio="xMaxYMid slice"><g fill="none" stroke="currentColor" stroke-width="1.2">
<path d="M380 60h150a24 24 0 0 1 24 24v58a24 24 0 0 1-24 24h-92l-30 26v-26h-28a24 24 0 0 1-24-24V84a24 24 0 0 1 24-24z"/>
<path d="M290 150h120a20 20 0 0 1 20 20v44a20 20 0 0 1-20 20h-20v22l-26-22h-74a20 20 0 0 1-20-20v-44a20 20 0 0 1 20-20z" opacity=".7"/>
<path d="M470 196h86a18 18 0 0 1 18 18v36a18 18 0 0 1-18 18h-58l-22 20v-20h-6a18 18 0 0 1-18-18v-36a18 18 0 0 1 18-18z" opacity=".5"/></g>
<g fill="currentColor"><circle cx="425" cy="113" r="3.2"/><circle cx="445" cy="113" r="3.2"/><circle cx="465" cy="113" r="3.2"/></g></svg>'''

SCRIPT = '''<script>
(function(){
  var list=document.querySelector('.th-list'),rows=[].slice.call(list.querySelectorAll('.th-row')),grps=[].slice.call(list.querySelectorAll('.th-grp')),
      tb=document.querySelectorAll('.cm-tf button'),k='a',topic='',q=document.getElementById('th-q'),sortv='recent',
      n=document.querySelector('[data-n]'),nl=document.querySelector('[data-nl]'),clr=document.querySelector('.th-clear'),tpn=document.querySelector('[data-tpn]'),none=document.querySelector('.th-none'),
      tps=[].slice.call(document.querySelectorAll('.th-topic'));
  rows.forEach(function(r,i){r.dataset.i=i;});
  function apply(){
    var t=(q.value||'').trim().toLowerCase(),c=0;
    rows.forEach(function(r){var ok=(k==='m'?r.dataset.m==='1':k==='u'?r.dataset.u==='1':k==='me'?r.dataset.me==='1':k==='f'?r.dataset.f==='1':true)&&(!topic||r.dataset.tp===topic)&&(!t||r.dataset.q.indexOf(t)>-1);r.hidden=!ok;if(ok)c++;});
    var cmp={replies:function(a,b){return b.dataset.r-a.dataset.r;},fewest:function(a,b){return a.dataset.r-b.dataset.r||a.dataset.s-b.dataset.s;},'new':function(a,b){return a.dataset.s-b.dataset.s;}}[sortv];
    if(cmp){grps.forEach(function(g){g.hidden=true;});rows.slice().sort(cmp).forEach(function(r){list.appendChild(r);});}
    else{grps.forEach(function(g){list.appendChild(g);var mine=rows.filter(function(r){return r.dataset.g===g.dataset.gh;}).sort(function(a,b){return a.dataset.i-b.dataset.i;});mine.forEach(function(r){list.appendChild(r);});
      var v=mine.filter(function(r){return !r.hidden;}).length;g.hidden=!v;g.querySelector('span').textContent=v+(v===1?' thread':' threads');});}
    n.textContent=c;nl.textContent=c===1?'thread':'threads';clr.hidden=!topic;tpn.textContent=topic;none.hidden=c>0;
    tps.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.topic===topic);});
  }
  tb.forEach(function(b){b.addEventListener('click',function(){k=b.dataset.t;tb.forEach(function(o){o.setAttribute('aria-pressed',o===b)});apply();});});
  var still=matchMedia('(prefers-reduced-motion: reduce)').matches;
  function land(h){var y=h.getBoundingClientRect().top+scrollY-110;scrollTo({top:y,behavior:still?'auto':'smooth'});
    var go=function(){h.classList.remove('th-bounce');void h.offsetWidth;h.classList.add('th-bounce');};var t0=Date.now(),last=-1;
    (function wait(){if(Math.abs(scrollY-last)<1||Date.now()-t0>1200){go();return;}last=scrollY;setTimeout(wait,80);})();}
  document.querySelectorAll('[data-jump]').forEach(function(j){j.addEventListener('click',function(){
    if(j.dataset.jump==='u'){land(document.getElementById('wait-h'));return;}
    k=j.dataset.jump;topic='';q.value='';tb.forEach(function(o){o.setAttribute('aria-pressed',o.dataset.t===k)});apply();land(document.querySelector('#th-all h2'));});});
  tps.forEach(function(b){b.addEventListener('click',function(){topic=topic===b.dataset.topic?'':b.dataset.topic;apply();});});
  document.querySelector('[data-clear]').addEventListener('click',function(){topic='';apply();});
  q.addEventListener('input',apply);
  var pref=window.hubThreadPref?hubThreadPref():'weekly';document.querySelectorAll('input[name=tmail]').forEach(function(r){r.checked=r.value===pref;r.addEventListener('change',function(){hubThreadPref(r.value);hubToast(hubThreadMsg('saved'));});});
  var sd=document.querySelector('.th-sample');document.querySelector('[data-sample]').addEventListener('click',function(){try{sd.showModal();}catch(x){sd.setAttribute('open','')}sd.querySelector('.cm-note').hidden=true;var d=hubThreadPref()==='daily';sd.querySelector('[data-seh]').textContent=d?'New replies today':'New replies this week';sd.querySelector('[data-sef]').textContent=d?'once a day':'once a week';});
  sd.querySelectorAll('[data-unf]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();var n=sd.querySelector('.cm-note');n.textContent='In a real email, this link unfollows in one click, with no sign-in. Nothing changes in the prototype.';n.hidden=false;});});
  sd.querySelector('[data-closeme]').addEventListener('click',function(e){e.preventDefault();try{sd.close();}catch(x){sd.removeAttribute('open')}document.getElementById('th-mail').scrollIntoView({block:'center'});});
  if(location.hash==='#th-mail'){setTimeout(function(){var m=document.getElementById('th-mail');m.scrollIntoView({block:'center'});m.classList.add('th-flash');},300);}
  var fc=document.querySelector('[data-fc]');function fcount(){fc.textContent=rows.filter(function(r){return r.dataset.f==='1';}).length;}fcount();
  rows.forEach(function(r){var fb=r.querySelector('.th-fol');fb.addEventListener('click',function(){var on=fb.getAttribute('aria-pressed')!=='true';fb.setAttribute('aria-pressed',on);fb.querySelector('span').textContent=on?'Following':'Follow';r.dataset.f=on?'1':'0';fcount();if(k==='f')apply();if(window.hubToast)hubToast(hubThreadMsg(on?'follow':'unfollow'));});});
  var sb=document.getElementById('th-sortb'),sm=document.getElementById('th-sortm'),opts=[].slice.call(sm.querySelectorAll('[role=option]')),sl=document.querySelector('[data-sortl]');
  function openM(o){sm.hidden=!o;sb.setAttribute('aria-expanded',o);if(o){(sm.querySelector('[aria-selected=true]')||opts[0]).focus();}}
  function pick(li){sortv=li.dataset.v;opts.forEach(function(x){x.setAttribute('aria-selected',x===li)});sl.textContent=li.firstChild.textContent;openM(false);sb.focus();apply();}
  sb.addEventListener('click',function(e){e.stopPropagation();openM(sm.hidden);});
  opts.forEach(function(li,i){li.addEventListener('click',function(){pick(li);});li.addEventListener('keydown',function(e){if(e.key==='ArrowDown'){e.preventDefault();opts[Math.min(i+1,opts.length-1)].focus();}else if(e.key==='ArrowUp'){e.preventDefault();opts[Math.max(i-1,0)].focus();}else if(e.key==='Enter'||e.key===' '){e.preventDefault();pick(li);}else if(e.key==='Escape'){openM(false);sb.focus();}});});
  document.addEventListener('click',function(e){if(!sm.hidden&&!e.target.closest('.th-sort'))openM(false);});
  var dlg=document.querySelector('.cm-compose');document.querySelectorAll('[data-compose]').forEach(function(b){b.addEventListener('click',function(){try{dlg.showModal();}catch(e){dlg.setAttribute('open','')}dlg.querySelector('.cm-note').hidden=true;});});
  dlg.querySelector('[data-post]').addEventListener('click',function(){
    var ti=dlg.querySelector('#cmc-t'),de=dlg.querySelector('#cmc-d'),v=(ti.value||'').trim();
    if(!v){ti.focus();ti.setAttribute('aria-invalid','true');var nt=dlg.querySelector('.cm-note');nt.textContent='Please write your question first.';nt.hidden=false;return;}
    ti.removeAttribute('aria-invalid');
    var kind=(dlg.querySelector('input[name=kind]:checked')||{}).value||'other',TP={funding:'Funding',expertise:'Finding a collaborator',student:'Hiring',other:'Your question'}[kind];
    var li=document.createElement('li');li.className='th-row th-un th-newrow';li.dataset.m='0';li.dataset.u='1';li.dataset.me='1';li.dataset.f='1';li.dataset.tp=TP;li.dataset.g='week';li.dataset.r='0';li.dataset.s='0';li.dataset.i='-1';li.dataset.q=(v+' '+(de.value||'')).toLowerCase();
    li.innerHTML='<span class="cm-av av-p" aria-hidden="true">AO</span><div class="th-body"><p class="th-tp th-p"></p><h3 class="th-t"></h3><p class="th-ex"></p><div class="th-foot"><p class="th-meta">You · No replies yet · Just now</p><button type="button" class="th-fol th-done" aria-pressed="false" title="Mark your question as answered. The emails stop, and others see it is resolved."><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3.5 8.5l3 3 6-7"/></svg><span>Mark as answered</span></button></div><p class="th-mine">You started this thread, so you follow it. In the prototype, it disappears when you leave the page.</p></div><div class="th-n th-n0"><span class="th-nn">0</span><span class="th-nl">New</span></div>';
    var dn=li.querySelector('.th-done');dn.addEventListener('click',function(){var on=dn.getAttribute('aria-pressed')!=='true';dn.setAttribute('aria-pressed',on);dn.querySelector('span').textContent=on?'Answered':'Mark as answered';li.classList.toggle('th-answered',on);if(window.hubToast)hubToast(on?'<b>Marked as answered.</b> The emails about this thread stop, and others see it is resolved.':'<b>Reopened.</b> You’ll hear about new replies again.');});
    li.querySelector('.th-tp').textContent=TP;li.querySelector('.th-t').textContent=v;li.querySelector('.th-ex').textContent=de.value||'';
    var gw=list.querySelector('[data-gh=week]');gw.after(li);rows.unshift(li);
    ti.value='';de.value='';try{dlg.close();}catch(x){dlg.removeAttribute('open');}
    k='a';topic='';q.value='';tb.forEach(function(o){o.setAttribute('aria-pressed',o.dataset.t==='a')});apply();
    document.getElementById('th-all').scrollIntoView({behavior:'auto'});li.classList.add('th-flash');fcount();if(window.hubToast)hubToast(hubThreadMsg('post'));
  });
  var af=document.querySelector('.th-ask');af.addEventListener('submit',function(e){e.preventDefault();var v=document.getElementById('th-askq').value.trim();try{dlg.showModal();}catch(x){dlg.setAttribute('open','')}dlg.querySelector('.cm-note').hidden=true;var ti=dlg.querySelector('#cmc-t');if(ti){ti.value=v;(v?dlg.querySelector('#cmc-d'):ti).focus();}});
})();
</script>'''

listpage = hdr('Threads') + f'''<main id="main" class="th-page">
  <section class="th-hero" aria-labelledby="t">
    {ART}
    <div class="wrap">
      <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><a href="community.html">Community</a><span aria-hidden="true">/</span><span aria-current="page">Threads</span></nav>
      <div class="th-hgrid">
        <div class="th-hl">
          <h1 id="t">Threads</h1>
          <p class="th-lead">Ask the colleagues who have already faced the same question. Methods, equipment, recruiting, and funding, answered by CNAP members. Only members can see threads.</p>
          <form class="th-ask" role="search" aria-label="Start a thread"><span class="cm-av av-p" aria-hidden="true">AO</span><label class="sr" for="th-askq">Your question</label><input id="th-askq" class="th-askp" type="text" placeholder="What would you like to ask the Center?" autocomplete="off"><button type="submit" class="th-askb">Start a thread</button></form>
        </div>
        <div class="th-stats" role="group" aria-label="Jump to threads">
          <button type="button" data-jump="a" title="Shows every open thread in the list below."><span class="th-sl">Open threads</span><span class="th-sn num">{len(T)}</span></button>
          <button type="button" data-jump="m" title="Shows the threads matched to your research interests."><span class="th-sl">Matched to you</span><span class="th-sn num">{n_m}</span></button>
          <button type="button" class="th-st-u" data-jump="u" title="Jumps to the threads no one has answered yet."><span class="th-sl">Not answered yet</span><span class="th-sn num">{n_u}</span></button>
        </div>
      </div>
    </div>
  </section>

  <section class="th-wait" aria-labelledby="wait-h">
    <div class="wrap">
      <div class="th-panel">
        <div class="th-sech"><h2 id="wait-h">No one has answered these yet</h2><p>{["No","One","Two","Three","Four","Five"][n_u]} colleagues are still waiting for a reply. If you know something, please share what you know. One reply can save someone weeks.</p></div>
        <ul class="th-spots">{spot}</ul>
      </div>
    </div>
  </section>

  <div class="wrap th-cols">
    <div class="th-main" id="th-all">
      <div class="th-sech"><h2>All threads</h2><p>Every conversation, newest activity first. Please filter, search, or pick a topic on the right.</p></div>
      <div class="th-bar">
        <div class="pf-filt cm-tf th-tf" role="group" aria-label="Show"><button type="button" aria-pressed="true" data-t="a">All threads</button><button type="button" aria-pressed="false" data-t="m">Matched to you</button><button type="button" aria-pressed="false" data-t="u">Unanswered</button><button type="button" aria-pressed="false" data-t="me">My threads</button><button type="button" aria-pressed="false" data-t="f">Following <span class="th-fc" data-fc></span></button></div>
        <div class="th-find">
          <label class="th-search" for="th-q"><span class="sr">Search threads</span><svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="7" cy="7" r="5"/><path d="M11 11l3.5 3.5"/></svg><input id="th-q" type="search" placeholder="Search a method, a person, or a word"></label>
          <div class="th-sort"><button type="button" class="th-sortb" id="th-sortb" aria-haspopup="listbox" aria-expanded="false" aria-controls="th-sortm"><span class="th-sortk">Sort:</span> <span data-sortl>Most recent activity</span><svg viewBox="0 0 10 10" aria-hidden="true"><path d="M2 3.5l3 3 3-3"/></svg></button>
            <ul class="th-sortm" id="th-sortm" role="listbox" aria-labelledby="th-sortb" hidden>
              <li role="option" aria-selected="true" data-v="recent" tabindex="-1">Most recent activity<small>Threads with new replies first</small></li>
              <li role="option" aria-selected="false" data-v="new" tabindex="-1">Newest first<small>Questions asked most recently</small></li>
              <li role="option" aria-selected="false" data-v="replies" tabindex="-1">Most replies<small>The busiest conversations</small></li>
              <li role="option" aria-selected="false" data-v="fewest" tabindex="-1">Fewest replies<small>Questions that most need an answer</small></li>
            </ul></div>
        </div>
      </div>
      <p class="th-status" role="status"><span data-n>{len(T)}</span> <span data-nl>threads</span><span class="th-clear" hidden> in <b data-tpn></b>. <button type="button" class="t3" data-clear>Show every topic</button></span></p>
      <ul class="th-list">{rows}</ul>
      <p class="th-none" hidden>No threads match. Please try another word, or <button type="button" class="t3" data-compose>start a thread</button>.</p>
    </div>
    <aside class="th-side" aria-label="Topics and people">
      <section class="th-card" aria-labelledby="tp-h"><h2 id="tp-h">Topics</h2><ul class="th-topics">{topics}</ul></section>
      <section class="th-card" aria-labelledby="hp-h"><h2 id="hp-h">Most helpful this fall</h2><ul class="th-help">{helpful}</ul></section>
      <section class="th-card th-mail" id="th-mail" aria-labelledby="mail-h"><h2 id="mail-h">Your thread emails</h2>
        <fieldset class="th-mf"><legend class="sr">How often should we email you about threads?</legend>
          <label><input type="radio" name="tmail" value="weekly"><span>Once a week<small>A summary of new replies, if there are any.</small></span></label>
          <label><input type="radio" name="tmail" value="daily"><span>Once a day<small>Only on days with new replies.</small></span></label>
          <label><input type="radio" name="tmail" value="mine"><span>Only my own questions<small>Replies to threads you started.</small></span></label>
          <label><input type="radio" name="tmail" value="none"><span>No emails<small>New replies still show on your Home page.</small></span></label>
        </fieldset>
        <p class="th-mnote">Unless you choose no emails, the first reply to your own question comes right away. Every email has an Unfollow link for each thread.</p>
        <button type="button" class="t3" data-sample>See a sample email</button>
      </section>
      <section class="th-card th-how" aria-labelledby="how-h"><h2 id="how-h">How threads work</h2>
        <ol><li>Only CNAP members can see threads.</li><li>Members with matching interests get a note about your question.</li><li>The CNAP team aims to read every thread, and joins in when the team can help.</li></ol></section>
    </aside>
  </div>
</main>

{compose}
<dialog class="cm-compose th-sample" aria-labelledby="se-h">
  <form method="dialog" class="cm-form">
    <p class="th-se-meta">From: CNAP Member Hub<br>Subject: 3 new replies in threads you follow</p>
    <h2 id="se-h" data-seh>New replies this week</h2>
    <div class="th-se-item"><b>Looking for an EEG collaborator</b><span>2 new replies, from Dr. Wei Zhang and Dr. Elena Voss</span><p><a href="thread.html">Read the replies</a> <span class="th-se-sep">|</span> <a href="#" data-unf>Unfollow this thread</a></p></div>
    <div class="th-se-item"><b>Sharing EEG caps between studies</b><span>1 new reply, from Dr. Maya Singh</span><p><a href="thread-ms.html">Read the reply</a> <span class="th-se-sep">|</span> <a href="#" data-unf>Unfollow this thread</a></p></div>
    <p class="th-se-foot">You get this email <span data-sef>once a week</span> because you follow these threads. <a href="threads.html#th-mail" data-closeme>Change how often</a>, or <a href="#" data-unf>stop all thread emails</a>.</p>
    <p class="cm-note" role="status" hidden></p>
    <div class="cm-fb"><button type="submit" value="cancel" class="btn">Close</button></div>
  </form>
</dialog>
{foot}
{SCRIPT}
<script src="hubchrome.js" defer></script>
</body>
</html>
'''
open(V + 'threads.html', 'w').write(listpage)
