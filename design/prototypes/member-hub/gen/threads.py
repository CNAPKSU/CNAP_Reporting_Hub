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
rel = ''.join(f'<li><a href="#" data-proto title="{ONE}">{t}</a><span>{rep(r)}</span></li>' for k, t, tp, r, *_ in T if k in ('ms', 'pr', 'lp'))

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
