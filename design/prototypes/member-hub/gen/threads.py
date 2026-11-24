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

def hdr(title):
    return head.replace('<title>Community · CNAP Member Hub</title>', f'<title>{title} · CNAP Member Hub</title>')
exec(open('/tmp/claude-0/hubproto/gen/threads_list.py').read())

# One page per thread (MW 2026-11-15: "click on any possible link ... and it does the thing it implies")
C.BY['ao'] = ('ao', 'AO', 'Dr. Amara Okafor', 'Pilot project leader, you', 'investigators', [], 'p', False)
BYT = {x[0]: x for x in T}
def reply(k, when, txt):
    m = BY[k]
    who = 'You' if k == 'ao' else ML(k)
    act = '' if k in ('ao', 'ev') else f'<p class="tp-ra"><a class="t3" href="{intro(m[2])}" title="Starts an email to the CNAP team asking for an introduction to {m[2]}.">Ask for an introduction</a></p>'
    return (f'<li class="tp-r">{av(k)}<div class="tp-rb"><p class="tp-rh"><b>{who}</b><span>{m[3]}</span><span>{when}</span></p>'
            f'<p class="tp-rt">{txt}</p>{act}</div></li>')

def page(k):
    x = BYT[k]; t, tp, n, w = x[1], x[2], x[3], x[6]
    asker = BY[k]
    rs = REPLIES[k]
    replies = ''.join(reply(*r) for r in rs)
    ppl = [k] + [r[0] for r in rs]
    seen = []
    for p_ in ppl:
        if p_ not in seen: seen.append(p_)
    people = ''.join(f'<li>{av(p_, " sm")}<span>{"You" if p_ == "ao" else ML(p_)}</span></li>' for p_ in seen)
    same = [y for y in T if y[2] == tp and y[0] != k]
    other = [y for y in T if y[2] != tp and y[0] != k]
    rel = ''.join(f'<li><a href="{url(y[0])}">{y[1]}</a><span>{rep(y[3])}</span></li>' for y in (same + other)[:3])
    body = ''.join(f'<p>{p_}</p>' for p_ in BODY[k])
    why = f'<p class="cm-why tp-why">{w[0].upper() + w[1:]} This thread was matched to you.</p>' if w else ''
    fol = k in FOLLOW
    empty = '<li class="tp-empty"><p>No one has answered yet. If you know something, or know who to ask, please reply below.</p></li>' if n == 0 else ''
    return hdr(t) + f"""<main id="main">
  <section class="co-open tp-open" aria-labelledby="t">
    <div class="wrap">
      <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><a href="community.html">Community</a><span aria-hidden="true">/</span><a href="threads.html">Threads</a><span aria-hidden="true">/</span><span aria-current="page">{t}</span></nav>
      <p class="th-tp th-{TONE[tp]}">{tp}</p>
      <h1 id="t">{t}</h1>
      <div class="tp-byrow"><div class="tp-by">{av(k)}<p><b>{ML(k)}</b><span>{asker[3]} · Started {STARTED_ON[k]} · <span data-rc>{rep(n)}</span></span></p></div></div>
    </div>
  </section>
  <div class="wrap tp-cols">
    <div class="tp-main">
      <div class="tp-q" id="tp-question" data-rail="The question">{body}<p class="tp-folrow"><button type="button" class="th-fol tp-fol" aria-pressed="{'true' if fol else 'false'}" title="Follow this thread to get one email a day when it has new replies."><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 2.5h8v11l-4-3-4 3z"/></svg><span>{'Following' if fol else 'Follow'}</span></button></p></div>
      {why}
      <h2 class="tp-h" data-rh id="tp-replies" data-rail="Replies">{rep(n) if n else 'Replies'}</h2>
      <ol class="tp-rs">{empty}{replies}</ol>
      <form class="tp-reply" id="reply" aria-labelledby="tp-rh">
        <h2 class="tp-h" id="tp-rh" data-rail="Your reply">Your reply</h2>
        <label class="sr" for="tp-rt">Your reply</label>
        <textarea id="tp-rt" rows="4" placeholder="Please share what you know, or who to ask."></textarea>
        <p class="tp-note" role="status" hidden></p>
        <div class="tp-fb"><button type="submit" class="btn pri">Post your reply</button><span class="meta">Visible to CNAP members only.</span></div>
      </form>
    </div>
    <aside class="tp-side" aria-label="About this thread">
      <div class="tp-card"><h2 class="tp-sh">In this thread</h2><ul class="tp-ppl">{people}</ul></div>
      <div class="tp-card"><h2 class="tp-sh" id="tp-related" data-rail="Related threads">Related threads</h2><ul class="tp-rel">{rel}</ul><a class="t3" href="threads.html">All threads</a></div>
    </aside>
  </div>
</main>

{foot}
<script>
(function(){{
  var f=document.querySelector('.tp-reply'),ta=document.getElementById('tp-rt'),note=f.querySelector('.tp-note'),list=document.querySelector('.tp-rs'),
      rh=document.querySelector('[data-rh]'),rc=document.querySelector('[data-rc]'),n={n};
  function label(c){{return c===0?'No replies yet':(c===1?'1 reply':c+' replies');}}
  f.addEventListener('submit',function(e){{
    e.preventDefault();var v=ta.value.trim();
    if(!v){{note.textContent='Please write your reply first.';note.hidden=false;ta.focus();return;}}
    var em=list.querySelector('.tp-empty');if(em)em.remove();
    var li=document.createElement('li');li.className='tp-r tp-new';
    li.innerHTML='<span class="cm-av av-p" aria-hidden="true">AO</span><div class="tp-rb"><p class="tp-rh"><b>You</b><span>Pilot project leader</span><span>Just now</span></p><p class="tp-rt"></p></div>';
    li.querySelector('.tp-rt').textContent=v;list.appendChild(li);n++;rh.textContent=label(n);rc.textContent=label(n);ta.value='';
    note.textContent='Your reply is posted below. In the prototype, it disappears when you leave the page.';note.hidden=false;if(fb.getAttribute('aria-pressed')!=='true'){{fb.setAttribute('aria-pressed','true');fb.querySelector('span').textContent='Following';}}if(window.hubToast)hubToast(hubThreadMsg('reply'));
    li.scrollIntoView({{block:'center',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'}});
  }});
  var fb=document.querySelector('.tp-fol');fb.addEventListener('click',function(){{var on=fb.getAttribute('aria-pressed')!=='true';fb.setAttribute('aria-pressed',on);fb.querySelector('span').textContent=on?'Following':'Follow';if(window.hubToast)hubToast(hubThreadMsg(on?'follow':'unfollow'));}});
  if(location.hash==='#reply'){{setTimeout(function(){{ta.focus();}},300);}}
}})();
</script>
<script src="hubchrome.js" defer></script>
</body>
</html>
"""
for x in T:
    open(V + url(x[0]), 'w').write(page(x[0]))
print('ok', len(T), 'thread pages')
