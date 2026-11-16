# The 2026 Site Visit photographs (MW 2026-11-15). Placeholders only: no real photographs of people.
import sys, io, contextlib
sys.path.insert(0, '/tmp/claude-0/hubproto/gen')
from mail import mt
V = '/tmp/claude-0/hubproto/v4/'
src = open(V + 'threads.html').read()
head = src[:src.index('<main id="main"')].replace('<title>Threads · CNAP Member Hub</title>', '<title>2026 Site Visit Photographs · CNAP Member Hub</title>').replace(' aria-current="page"', '')
foot = src[src.index('<footer class="foot">'):src.index('</footer>', src.index('<footer class="foot">')) + 9]
foot = foot[:foot.index('<span>Prototype')] + '<span>Prototype. Every photograph here is a placeholder. The real gallery comes from the CNAP team’s 2026 photographs.</span></div></footer>'
SHARE = mt('cnap@ksu.edu', 'Photographs from the 2026 Site Visit', '\n'.join(['Name:', '', 'What the photographs show:', '', 'A link to the photographs, or attach them:', '']), cc=None)
DAYS = [
 ('Day 1', 'Wednesday, May 27', [
   ('Core tours', 8, 'reel-2.jpg', 'The research cores open the labs to visitors.'),
   ('Project presentations', 14, 'reel-5.jpg', 'Every project leader presents progress.'),
   ('Keynote address', 4, 'reel-3.jpg', 'Before the banquet.'),
   ('Banquet', 8, 'reel-4.jpg', 'At the Beach Museum of Art.')]),
 ('Day 2', 'Thursday, May 28', [
   ('Poster session', 10, 'reel-1.jpg', 'Students and investigators present research.'),
   ('Group photographs', 4, None, 'Everyone, then each core.')]),
]
total = sum(n for _, _, gs in DAYS for _, n, _, _ in gs)
def group(t, n, img, d):
    tiles = ''
    for i in range(n):
        if i == 0 and img:
            tiles += f'<li class="pg-t pg-lead"><img src="img/{img}" alt="Placeholder for a photograph: {t.lower()}" loading="lazy"><span class="pg-tag">Photo placeholder</span></li>'
        else:
            tiles += f'<li class="pg-t" aria-hidden="true"></li>'
    gid = 'pg-' + t.lower().replace(' ', '-')
    return (f'<section class="pg-g" aria-labelledby="{gid}"><header class="pg-gh"><h3 id="{gid}" data-rail="{t}">{t}</h3><p>{d} {n} photographs.</p></header>'
            f'<ul class="pg-grid" aria-label="{n} placeholder photographs of {t.lower()}">{tiles}</ul></section>')
body = ''
for day, date, gs in DAYS:
    did = 'pg-' + day.lower().replace(' ', '')
    body += f'<section class="pg-day" aria-labelledby="{did}"><h2 class="pg-dh" id="{did}">{day}<span>{date}</span></h2>{"".join(group(*g) for g in gs)}</section>'
jump = ''.join(f'<li><a href="#pg-{t.lower().replace(" ", "-")}">{t}</a></li>' for _, _, gs in DAYS for t, _, _, _ in gs)
page = head + f'''<main id="main">
  <section class="pg-hero" aria-labelledby="t">
    <div class="wrap pg-hgrid">
      <div class="pg-hl">
        <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><a href="sitevisit.html">Site Visit</a><span aria-hidden="true">/</span><span aria-current="page">2026 photographs</span></nav>
        <p class="pg-kick">May 27 and 28, 2026 · Manhattan, Kansas</p>
        <h1 id="t">The 2026 Site Visit, in photographs</h1>
        <p class="pg-lead">{total} photographs from two days of core tours, project presentations, the keynote and banquet, and the poster session, in the order of the program.</p>
        <div class="pg-act"><a class="btn pg-pri" href="sitevisit.html">Plan for the 2027 Site Visit</a><a class="btn pg-sec" href="{SHARE}">Share your photographs</a></div>
      </div>
      <div class="pg-collage" aria-hidden="true">
        <figure class="pg-c1"><img src="img/reel-1.jpg" alt=""><figcaption>Poster session</figcaption></figure>
        <figure class="pg-c2"><img src="img/reel-2.jpg" alt=""><figcaption>Core tours</figcaption></figure>
        <figure class="pg-c3"><img src="img/reel-3.jpg" alt=""><figcaption>Keynote address</figcaption></figure>
        <span class="pg-ph">Photo placeholders</span>
      </div>
    </div>
  </section>
  <nav class="pg-jumpbar" aria-label="Jump to a part of the program"><div class="wrap"><ul class="pg-jump">{jump}</ul></div></nav>
  <div class="wrap pg-body">{body}</div>
</main>

{foot}
<script src="hubchrome.js" defer></script>
</body>
</html>
'''
open(V + 'sitevisit-2026.html', 'w').write(page)
print('ok', total)
