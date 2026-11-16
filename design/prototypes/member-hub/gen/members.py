# A profile page for every fictional member and alumnus (MW 2026-11-15: "should these link to their profiles?")
import sys, io, contextlib, re
sys.path.insert(0, '/tmp/claude-0/hubproto/gen')
with contextlib.redirect_stdout(io.StringIO()):
    import community as C
exec(open('/tmp/claude-0/hubproto/gen/thread_data.py').read())
V = C.V
src = open(V + 'community.html').read()
head = src[:src.index('<main id="main"')]
foot = src[src.index('<footer class="foot">'):src.index('</footer>', src.index('<footer class="foot">')) + 9]
foot = re.sub(r'<span>Prototype\..*?</span>', '<span>Prototype. Every member here is fictional, except the Director, the Assistant Director for Grants and Contracts, and the Grant Specialist.</span>', foot, flags=re.S)

# thread titles by key, from the Threads page data
TT = {}
for line in open('/tmp/claude-0/hubproto/gen/threads_list.py').read().split('\n'):
    m = re.match(r" \('(\w\w)', '([^']+)', '([^']+)',", line)
    if m: TT[m.group(1)] = (m.group(2), m.group(3))

P = {}
for m in C.M:
    k, ini, name, role, grp, ints, tone, new = m
    P[k] = dict(k=k, ini=ini, name=name, role=role, ints=ints, tone=tone, new=new, alum=None)
for (ini, tone, name, c, w, f, ok) in C.AL:
    k = ini.lower()
    d = P.get(k, dict(k=k, ini=ini, name=name, role='CNAP alumnus', ints=[], tone=tone, new=False))
    d['alum'] = (c, w, f, ok)
    P[k] = d

def url(k): return f'member-{k}.html'

def page(d):
    k, name = d['k'], d['name']
    first = name.replace('Dr. ', '').split()[0]
    av = f'<span class="cm-av av-{d["tone"]} lg" aria-hidden="true">{d["ini"]}</span>'
    where = d['alum'][1] if d['alum'] else d['role']
    chips = ''.join(f'<span>{x}</span>' for x in d['ints'])
    started = [(kk, TT[kk][0]) for kk in TT if kk == k]
    replied = [(kk, TT[kk][0]) for kk, rs in REPLIES.items() if any(r[0] == k for r in rs) and kk in TT]
    def tl(kk, t): return f'<li><a href="{"thread.html" if kk == "jl" else "thread-" + kk + ".html"}">{t}</a></li>'
    threads = ''
    if started: threads += '<h3 class="mb-h3">Started</h3><ul class="mb-th">' + ''.join(tl(*x) for x in started) + '</ul>'
    if replied: threads += '<h3 class="mb-h3">Replied to</h3><ul class="mb-th">' + ''.join(tl(*x) for x in replied) + '</ul>'
    if not threads: threads = '<p class="mb-none">No threads yet.</p>'
    alum = ''
    if d['alum']:
        c, w, f, ok = d['alum']
        r, yrs = C._split(c); aw, ag = C._split(f)
        alum = (f'<section class="mb-sec" aria-labelledby="mb-path"><h2 id="mb-path" data-rail="At CNAP and after">At CNAP and after</h2>'
                f'<ol class="al-path"><li class="al-from"><span class="al-k">At CNAP</span><b>{r}</b>{f"<span>{yrs}</span>" if yrs else ""}</li><li class="al-gap" aria-hidden="true"></li>'
                f'<li class="al-to"><span class="al-k">After CNAP</span><b>{aw}</b>{f"<span>{ag}</span>" if ag else ""}</li></ol>'
                + ('<p class="al-ok" style="margin-top:14px">Happy to talk with new project leaders</p>' if ok else '') + '</section>')
    ints = f'<section class="mb-sec" aria-labelledby="mb-int"><h2 id="mb-int" data-rail="Interests and methods">Interests and methods</h2><p class="cm-chips mb-chips">{chips}</p></section>' if chips else ''
    return head.replace('<title>Community · CNAP Member Hub</title>', f'<title>{name} · CNAP Member Hub</title>') + f'''<main id="main" class="mb-page">
  <section class="mb-hero" aria-labelledby="t">
    <div class="wrap">
      <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><a href="community.html">Community</a><span aria-hidden="true">/</span><a href="community.html#cm-dir">Member directory</a><span aria-hidden="true">/</span><span aria-current="page">{name}</span></nav>
      <div class="mb-top">{av}<div><h1 id="t">{name}</h1><p class="mb-role">{where}</p>{'<span class="cm-new">New this month</span>' if d['new'] else ''}</div>
        <div class="cm-acts mb-acts"><button type="button" class="btn pri" data-direct="{name}">Email {first}</button><a class="btn" href="{C.intro(name)}" title="Starts an email asking the CNAP team to introduce you.">Ask for an introduction</a></div></div>
    </div>
  </section>
  <div class="wrap mb-body">
    {ints}
    {alum}
    <section class="mb-sec" aria-labelledby="mb-thr"><h2 id="mb-thr" data-rail="Threads">Threads</h2>{threads}</section>
  </div>
</main>
{foot}
<script>document.querySelectorAll('[data-direct]').forEach(function(b){{b.addEventListener('click',function(){{if(window.hubToast)hubToast('<b>In the Member Hub, this starts an email to '+b.dataset.direct+'.</b> The members here are fictional, so nothing opens in the prototype.');}});}});</script>
<script src="hubchrome.js" defer></script>
</body>
</html>
'''
for d in P.values():
    open(V + url(d['k']), 'w').write(page(d))
print('ok', len(P), 'member pages')
