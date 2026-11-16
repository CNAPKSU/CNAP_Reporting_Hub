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
 ('rg', 'Who has used the Beocat cluster for imaging?', 'Methods and equipment', 0, 'Started Wednesday', True, 'Your team moved its analysis pipeline onto Beocat.', True,
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
TONE = {'Finding a collaborator': 'p', 'Methods and equipment': 't', 'Recruiting': 'a', 'Statistics': 'g', 'Funding': 'b', 'Events and groups': 'l', 'Hiring': 'a', 'Mentoring': 'p'}
TOPICS = sorted(set(t[2] for t in T))
def rep(n): return 'No replies yet' if n == 0 else ('1 reply' if n == 1 else f'{n} replies')

def row(k, t, tp, r, a, mt_, w, un, ex, rs, grp):
    href = 'thread.html' if k == 'jl' else '#'
    pa = '' if k == 'jl' else f' data-proto title="{ONE}"'
    q = (t + ' ' + BY[k][2] + ' ' + tp + ' ' + ex).lower().replace('"', '')
    stack = ''.join(av(x, ' sm') for x in rs[:3])
    if un:
        right = '<div class="th-n th-n0"><span class="th-nn">0</span><span class="th-nl">Be the first</span></div>'
    else:
        right = f'<div class="th-n"><span class="th-nn">{r}</span><span class="th-nl">{"reply" if r == 1 else "replies"}</span><span class="th-stack" aria-hidden="true">{stack}</span></div>'
    why = f'<p class="th-why"><b>Matched to you.</b> {w}</p>' if w else ''
    return (f'<li class="th-row{" th-un" if un else ""}" data-m="{"1" if mt_ else "0"}" data-u="{"1" if un else "0"}" data-tp="{tp}" data-g="{grp}" data-r="{r}" data-q="{q}">'
            f'{av(k)}<div class="th-body"><p class="th-tp th-{TONE[tp]}">{tp}</p><h3 class="th-t"><a href="{href}"{pa}>{t}</a></h3><p class="th-ex">{ex}</p>'
            f'<p class="th-meta">{BY[k][2]} · {rep(r)} · {a}</p>{why}</div>{right}</li>')

week = [x for x in T if x[10] == 'week']
earlier = [x for x in T if x[10] == 'earlier']
rows = (f'<li class="th-grp" data-gh="week"><h2>This week</h2><span>{len(week)} threads</span></li>' + ''.join(row(*x) for x in week)
        + f'<li class="th-grp" data-gh="earlier"><h2>Earlier this fall</h2><span>{len(earlier)} threads</span></li>' + ''.join(row(*x) for x in earlier))
unans = [x for x in T if x[7]]
def spotcard(x):
    return (f'<article class="th-spot"><p class="th-tp th-{TONE[x[2]]}">{x[2]}</p><h3><a href="#" data-proto title="{ONE}">{x[1]}</a></h3><p class="th-ex">{x[8]}</p>'
            f'<div class="th-spf"><span class="th-who">{av(x[0], " sm")}<span>{BY[x[0]][2]}<small>{x[4]}</small></span></span>'
            f'<a class="btn sm" href="#" data-proto title="{ONE}">Answer this thread</a></div></article>')
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
      tb=document.querySelectorAll('.cm-tf button'),k='a',topic='',q=document.getElementById('th-q'),srt=document.getElementById('th-sort'),
      n=document.querySelector('[data-n]'),nl=document.querySelector('[data-nl]'),clr=document.querySelector('.th-clear'),tpn=document.querySelector('[data-tpn]'),none=document.querySelector('.th-none'),
      tps=[].slice.call(document.querySelectorAll('.th-topic'));
  rows.forEach(function(r,i){r.dataset.i=i;});
  function apply(){
    var t=(q.value||'').trim().toLowerCase(),c=0;
    rows.forEach(function(r){var ok=(k==='m'?r.dataset.m==='1':k==='u'?r.dataset.u==='1':true)&&(!topic||r.dataset.tp===topic)&&(!t||r.dataset.q.indexOf(t)>-1);r.hidden=!ok;if(ok)c++;});
    if(srt.value==='replies'){grps.forEach(function(g){g.hidden=true;});rows.slice().sort(function(a,b){return b.dataset.r-a.dataset.r;}).forEach(function(r){list.appendChild(r);});}
    else{grps.forEach(function(g){list.appendChild(g);var mine=rows.filter(function(r){return r.dataset.g===g.dataset.gh;}).sort(function(a,b){return a.dataset.i-b.dataset.i;});mine.forEach(function(r){list.appendChild(r);});
      var v=mine.filter(function(r){return !r.hidden;}).length;g.hidden=!v;g.querySelector('span').textContent=v+(v===1?' thread':' threads');});}
    n.textContent=c;nl.textContent=c===1?'thread':'threads';clr.hidden=!topic;tpn.textContent=topic;none.hidden=c>0;
    tps.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.topic===topic);});
  }
  tb.forEach(function(b){b.addEventListener('click',function(){k=b.dataset.t;tb.forEach(function(o){o.setAttribute('aria-pressed',o===b)});apply();});});
  tps.forEach(function(b){b.addEventListener('click',function(){topic=topic===b.dataset.topic?'':b.dataset.topic;apply();});});
  document.querySelector('[data-clear]').addEventListener('click',function(){topic='';apply();});
  q.addEventListener('input',apply);srt.addEventListener('change',apply);
  var dlg=document.querySelector('.cm-compose');document.querySelectorAll('[data-compose]').forEach(function(b){b.addEventListener('click',function(){try{dlg.showModal();}catch(e){dlg.setAttribute('open','')}dlg.querySelector('.cm-note').hidden=true;});});
  dlg.querySelector('[data-post]').addEventListener('click',function(){dlg.querySelector('.cm-note').hidden=false;});
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
          <p class="th-lead">Ask the people who have done it before. Methods, equipment, recruiting, and funding, answered by CNAP members. Only members can see threads.</p>
          <button type="button" class="th-ask" data-compose><span class="cm-av av-p" aria-hidden="true">AO</span><span class="th-askp">What would you like to ask the Center?</span><span class="th-askb">Start a thread</span></button>
        </div>
        <dl class="th-stats">
          <div><dt>Open threads</dt><dd class="num">{len(T)}</dd></div>
          <div><dt>Matched to you</dt><dd class="num">{n_m}</dd></div>
          <div class="th-st-u"><dt>Waiting for a first answer</dt><dd class="num">{n_u}</dd></div>
        </dl>
      </div>
    </div>
  </section>

  <section class="th-wait" aria-labelledby="wait-h">
    <div class="wrap">
      <div class="th-waith"><h2 id="wait-h">Waiting for a first answer</h2><p>One reply can save a colleague weeks. If you know something, please share it.</p></div>
      <div class="th-spots">{spot}</div>
    </div>
  </section>

  <div class="wrap th-cols">
    <div class="th-main">
      <div class="th-bar">
        <div class="pf-filt cm-tf" role="group" aria-label="Show"><button type="button" aria-pressed="true" data-t="a">All threads</button><button type="button" aria-pressed="false" data-t="m">Matched to you</button><button type="button" aria-pressed="false" data-t="u">Unanswered</button></div>
        <div class="th-find">
          <label class="th-search" for="th-q"><span class="sr">Search threads</span><svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="7" cy="7" r="5"/><path d="M11 11l3.5 3.5"/></svg><input id="th-q" type="search" placeholder="Search a method, a person, or a word"></label>
          <label class="th-sortl" for="th-sort"><span class="sr">Sort threads</span><select id="th-sort"><option value="recent">Most recent activity</option><option value="replies">Most replies</option></select></label>
        </div>
      </div>
      <p class="th-status" role="status"><span data-n>{len(T)}</span> <span data-nl>threads</span><span class="th-clear" hidden> in <b data-tpn></b>. <button type="button" class="t3" data-clear>Show every topic</button></span></p>
      <ul class="th-list">{rows}</ul>
      <p class="th-none" hidden>No threads match. Please try another word, or <button type="button" class="t3" data-compose>start a thread</button>.</p>
    </div>
    <aside class="th-side" aria-label="Topics and people">
      <section class="th-card" aria-labelledby="tp-h"><h2 id="tp-h">Topics</h2><ul class="th-topics">{topics}</ul></section>
      <section class="th-card" aria-labelledby="hp-h"><h2 id="hp-h">Most helpful this fall</h2><ul class="th-help">{helpful}</ul></section>
      <section class="th-card th-how" aria-labelledby="how-h"><h2 id="how-h">How threads work</h2>
        <ol><li>Only CNAP members can see threads.</li><li>Members whose interests match your question are told about it.</li><li>The CNAP team reads every thread and steps in when a question needs the office.</li></ol></section>
    </aside>
  </div>
</main>

{compose}
{foot}
{SCRIPT}
<script src="hubchrome.js" defer></script>
</body>
</html>
'''
open(V + 'threads.html', 'w').write(listpage)
