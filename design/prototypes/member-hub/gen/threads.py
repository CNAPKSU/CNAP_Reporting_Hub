# Threads (all conversation threads) and one sample thread page. Prototype only, fictional members.
# MW 2026-11-15: "should the CNAP threads have its own page?" -> yes.
import sys, re, io, contextlib
sys.path.insert(0, '/tmp/claude-0/hubproto/gen')
with contextlib.redirect_stdout(io.StringIO()):
    import community as C
V = C.V
BY, av, intro = C.BY, C.av, C.intro

src = open(V + 'community.html').read()
head = src[:src.index('<main id="main">')]
compose = src[src.index('<dialog class="cm-compose"'):src.index('</dialog>') + 9]
foot = src[src.index('<footer class="foot">'):src.index('</footer>', src.index('<footer class="foot">')) + 9]
foot = foot.replace('The members, threads, and achievements are fictional.', 'The members and threads are fictional.')

ONE = 'Only one thread page is built in the prototype: Looking for an EEG collaborator.'
# key, title, topic, replies, activity, matched, why, unanswered
T = [
 ('jl', 'Looking for an EEG collaborator', 'Finding a collaborator', '4 replies', 'Active today', True, 'You record sleep EEG in your pilot project.', False),
 ('kb', 'Calibrating the eye tracker for participants who wear glasses', 'Methods and equipment', 'No replies yet', 'Started today', False, '', True),
 ('lp', 'Recruiting older adults: what has worked?', 'Recruiting', '3 replies', 'Active yesterday', True, 'Your study recruits adults over 65.', False),
 ('rg', 'Who has used the Beocat cluster for imaging?', 'Methods and equipment', 'No replies yet', 'Started Wednesday', True, 'Your team moved the team’s analysis pipeline onto Beocat. Be the first to answer.', True),
 ('hc', 'Office hours for mixed-effects models in R', 'Statistics', '6 replies', 'Active Monday', False, '', False),
 ('pr', 'Has anyone applied for the Brain & Behavior Research Foundation Young Investigator Grant?', 'Funding', '2 replies', 'Active Monday', True, 'You are weighing the same grant for next spring.', False),
 ('sr', 'A journal club on fear extinction, starting in December', 'Events and groups', '5 replies', 'Active last week', False, '', False),
 ('om', 'Housing rats on a reversed light cycle: tips for a new lab', 'Methods and equipment', '3 replies', 'Active last week', False, '', False),
 ('ms', 'Sharing EEG caps between studies: cleaning and scheduling', 'Methods and equipment', '4 replies', 'Active last week', True, 'You book EEG time in the Cognitive Neuroscience Core.', False),
 ('do', 'What I wish I had known before my first R01 submission', 'Funding', '9 replies', 'Active November 2', True, 'Your R21 is due in 123 days.', False),
 ('na', 'Graduate student position: motor learning and EEG, spring 2027', 'Hiring', '1 reply', 'Active October 30', False, '', False),
 ('wz', 'A template for data management plans that reviewers liked', 'Funding', '7 replies', 'Active October 28', False, '', False),
 ('tb', 'Tips for the new electrophysiology rig', 'Methods and equipment', '2 replies', 'Active October 26', False, '', False),
 ('ev', 'How often do you meet with your mentee in the first year?', 'Mentoring', '8 replies', 'Active October 21', False, '', False),
]
TOPICS = sorted(set(t[2] for t in T))

def row(k, t, tp, r, a, mt_, w, un):
    link = f'<a class="cm-tt" href="thread.html">{t}</a>' if k == 'jl' else f'<a class="cm-tt" href="#" data-proto title="{ONE}">{t}</a>'
    q = (t + ' ' + BY[k][2] + ' ' + tp).lower().replace('"', '')
    return (f'<li class="cm-th" data-m="{"1" if mt_ else "0"}" data-u="{"1" if un else "0"}" data-tp="{tp}" data-q="{q}">{av(k)}'
            f'<div class="cm-tm">{link}<p class="cm-tx">{BY[k][2]} · {tp} · {r} · {a}</p>{f"<p class=cm-why>{w}</p>" if w else ""}</div>'
            f'{"<span class=\"st st-on\">Unanswered</span>" if un else ""}</li>')

rows = ''.join(row(*t) for t in T)
topics = ''.join(f'<option value="{x}">{x}</option>' for x in TOPICS)

def hdr(title):
    return head.replace('<title>Community · CNAP Member Hub</title>', f'<title>{title} · CNAP Member Hub</title>')

listpage = hdr('Threads') + f'''<main id="main">
  <section class="co-open tp-open" aria-labelledby="t">
    <div class="wrap">
      <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><a href="community.html">Community</a><span aria-hidden="true">/</span><span aria-current="page">Threads</span></nav>
      <div class="tp-hd">
        <div>
          <h1 id="t">Threads</h1>
          <p class="lead">Questions about methods, equipment, recruiting, and funding, answered by the members who have the experience. Threads are visible only to CNAP members.</p>
        </div>
        <button type="button" class="btn pri" data-compose>Start a conversation thread</button>
      </div>
    </div>
  </section>
  <div class="wrap tp-body">
    <div class="tp-bar">
      <div class="pf-filt cm-tf" role="group" aria-label="Show"><button type="button" aria-pressed="false" data-t="m">Matched to you</button><button type="button" aria-pressed="false" data-t="u">Unanswered</button><button type="button" aria-pressed="true" data-t="a">All threads</button></div>
      <div class="tp-find">
        <label class="tp-l" for="tp-topic">Topic<select id="tp-topic"><option value="">All topics</option>{topics}</select></label>
        <label class="tp-l" for="tp-q">Search<input id="tp-q" type="search" placeholder="A method, a person, or a word"></label>
      </div>
    </div>
    <p class="tp-n" role="status"><b data-n>{len(T)}</b> threads</p>
    <ul class="cm-ths tp-list">{rows}</ul>
    <p class="tp-none" hidden>No threads match. Please try another word, or <button type="button" class="t3" data-compose>start a conversation thread</button>.</p>
  </div>
</main>

{compose}
{foot}
<script>
(function(){{
  var rows=[].slice.call(document.querySelectorAll('.tp-list .cm-th')),tb=document.querySelectorAll('.cm-tf button'),k='a',
      q=document.getElementById('tp-q'),tp=document.getElementById('tp-topic'),n=document.querySelector('[data-n]'),none=document.querySelector('.tp-none');
  function apply(){{var t=(q.value||'').trim().toLowerCase(),c=0;rows.forEach(function(r){{var ok=(k==='m'?r.dataset.m==='1':k==='u'?r.dataset.u==='1':true)&&(!tp.value||r.dataset.tp===tp.value)&&(!t||r.dataset.q.indexOf(t)>-1);r.hidden=!ok;if(ok)c++;}});n.textContent=c;n.nextSibling.textContent=c===1?' thread':' threads';none.hidden=c>0;}}
  tb.forEach(function(b){{b.addEventListener('click',function(){{k=b.dataset.t;tb.forEach(function(o){{o.setAttribute('aria-pressed',o===b)}});apply();}});}});
  q.addEventListener('input',apply);tp.addEventListener('change',apply);
  var dlg=document.querySelector('.cm-compose');document.querySelectorAll('[data-compose]').forEach(function(b){{b.addEventListener('click',function(){{try{{dlg.showModal();}}catch(e){{dlg.setAttribute('open','')}}dlg.querySelector('.cm-note').hidden=true;}});}});
  dlg.querySelector('[data-post]').addEventListener('click',function(){{dlg.querySelector('.cm-note').hidden=false;}});
}})();
</script>
<script src="hubchrome.js" defer></script>
</body>
</html>
'''
open(V + 'threads.html', 'w').write(listpage)

# The sample thread
R = [
 ('pr', 'Monday', 'I record sleep EEG in older adults, and our protocols are close to yours. I would be glad to compare montages and scoring rules. Our lab scores slow oscillations and spindles separately, which might help with your coupling question.'),
 ('ms', 'Monday', 'The Cognitive Neuroscience Core has two 64-channel systems that can run overnight. If you and a collaborator want to share a protocol, I can set up a joint booking so both studies use the same caps and settings.'),
 ('wz', 'Yesterday', 'If you end up pooling data across two labs, the Neuroinformatics Core can build one preprocessing pipeline for both, so the spindle detection is identical. Please send me the file formats when you know them.'),
 ('ev', 'Today', 'Jordan, Priya’s work on memory and sleep in aging would fit your aims well. I am happy to join a first meeting if that helps.'),
]
def reply(k, when, txt):
    m = BY[k]
    return (f'<li class="tp-r">{av(k)}<div class="tp-rb"><p class="tp-rh"><b>{m[2]}</b><span>{m[3]}</span><span>{when}</span></p>'
            f'<p class="tp-rt">{txt}</p>'+('' if k=='ev' else f'<p class="tp-ra"><a class="t3" href="{intro(m[2])}">Ask for an introduction</a></p>')+'</div></li>')
replies = ''.join(reply(*r) for r in R)
people = ''.join(f'<li>{av(k," sm")}<span>{BY[k][2]}</span></li>' for k in ['jl'] + [r[0] for r in R])
rel = ''.join(f'<li><a href="#" data-proto title="{ONE}">{t}</a><span>{r}</span></li>' for k, t, tp, r, *_ in T if k in ('ms', 'pr', 'lp'))

thread = hdr('Looking for an EEG collaborator') + f'''<main id="main">
  <section class="co-open tp-open" aria-labelledby="t">
    <div class="wrap">
      <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><a href="community.html">Community</a><span aria-hidden="true">/</span><a href="threads.html">Threads</a><span aria-hidden="true">/</span><span aria-current="page">Looking for an EEG collaborator</span></nav>
      <p class="for">Finding a collaborator</p>
      <h1 id="t">Looking for an EEG collaborator</h1>
      <div class="tp-by">{av('jl')}<p><b>Dr. Jordan Lee</b><span>Pilot project leader · Started November 9 · 4 replies</span></p></div>
    </div>
  </section>
  <div class="wrap tp-cols">
    <div class="tp-main">
      <div class="tp-q">
        <p>My pilot project records overnight EEG to see how sleep spindles relate to memory the next morning. For the R01, I would like to extend the study to adults over 65, and I am looking for a collaborator who already works with older participants.</p>
        <p>Ideally, someone who records sleep EEG or studies memory in aging, and who would consider a shared protocol. Please reply here, or ask the CNAP team for an introduction.</p>
      </div>
      <p class="cm-why tp-why">You record sleep EEG in your pilot project, so this thread was matched to you.</p>
      <h2 class="tp-h">4 replies</h2>
      <ol class="tp-rs">{replies}</ol>
      <form class="tp-reply" aria-labelledby="tp-rh">
        <h2 class="tp-h" id="tp-rh">Your reply</h2>
        <label class="sr" for="tp-rt">Your reply</label>
        <textarea id="tp-rt" rows="4" placeholder="Please share what you know, or who to ask."></textarea>
        <p class="tp-note" role="status" hidden>Prototype only. In the Member Hub, your reply posts here, and Dr. Jordan Lee is told about the reply.</p>
        <div class="tp-fb"><button type="submit" class="btn pri">Post your reply</button><span class="meta">Visible to CNAP members only.</span></div>
      </form>
    </div>
    <aside class="tp-side" aria-label="About this thread">
      <div class="tp-card"><h2 class="tp-sh">In this thread</h2><ul class="tp-ppl">{people}</ul></div>
      <div class="tp-card"><h2 class="tp-sh">Related threads</h2><ul class="tp-rel">{rel}</ul><a class="t3" href="threads.html">All threads</a></div>
    </aside>
  </div>
</main>

{foot}
<script>
(function(){{var f=document.querySelector('.tp-reply');f.addEventListener('submit',function(e){{e.preventDefault();f.querySelector('.tp-note').hidden=false;}});}})();
</script>
<script src="hubchrome.js" defer></script>
</body>
</html>
'''
open(V + 'thread.html', 'w').write(thread)
print('ok')
