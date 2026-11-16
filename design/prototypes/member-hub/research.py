import sys
sys.path.insert(0,'/tmp/claude-0/hubproto/gen')
from mail import mt
V='/tmp/claude-0/hubproto/v4/'
core=open(V+'core-ni.html').read()
hdr=core[core.index('<a class="skip"'):core.index('<main id="main">')]
hdr=hdr.replace('<a href="index.html#cores-h" aria-current="page">Resources</a>','<a href="index.html#cores-h">Resources</a>')
hdr=hdr.replace('<a href="research.html">Research</a>','<a href="research.html" aria-current="page">Research</a>')
SUG=mt('cnap@ksu.edu','Story idea for Research at CNAP','\n'.join(['Name:','Department:','','The story (a project milestone, a new paper or grant, a core capability, or a person to profile):','','Why members would want to read it:','','Photos or figures I can share:','']),cc=None)
S=[
 dict(id='sleep',kind='pilot',k='Pilot project',t='What a night of sleep does to a new memory',d='A CNAP pilot project is recording brain activity during sleep to learn which memories are kept by morning. The team describes its design and what it plans to test next.',date='November 10, 2026',m='November',read='4-minute read',img='img/neurons.jpg',alt='Generated illustration of branching neurons in magenta and teal on a dark ground',tag='Illustration',href='story.html'),
 dict(id='tms',kind='core',k='Core capability',t='Transcranial magnetic stimulation in the Cognitive Neuroscience Core',d='Combined with EEG, stimulation will let investigators test which brain regions a task depends on, not just which ones are active.',date='November 8, 2026',m='November',read='3-minute read',img='img/reel-3.jpg',alt='Placeholder for a photograph of the Cognitive Neuroscience Core',tag='Photo placeholder',href='#'),
 dict(id='pilot-team',kind='pilot',k='Pilot project',t='How a new pilot team is planning its first year',d='Milestones, a standing monthly meeting, and an early conversation with the cores: how one team set up its pilot award.',date='November 6, 2026',m='November',read='5-minute read',img='img/oscillations.jpg',alt='Generated illustration of brain oscillations',tag='Illustration',href='#'),
 dict(id='papers',kind='pubs',k='Publications',t='Three new papers that cite CNAP this fall',d='Work from two pilot projects and the Neuroinformatics Core, published between September and November.',date='November 3, 2026',m='November',read='2-minute read',img='img/reel-1.jpg',alt='Placeholder for a photograph of journal articles',tag='Photo placeholder',href='#'),
 dict(id='newest',kind='people',k='Investigator profile',t='Meet the Center’s newest pilot project leader',d='Why a sleep researcher joined CNAP, and what she hopes the Center’s cores will make possible.',date='October 29, 2026',m='October',read='4-minute read',img='img/reel-4.jpg',alt='Placeholder for a portrait photograph',tag='Photo placeholder',href='#'),
 dict(id='ni',kind='core',k='Core capability',t='What the Neuroinformatics Core can process for your lab',d='From EEG pipelines to machine learning on behavior videos, with run times measured in hours instead of weeks.',date='October 22, 2026',m='October',read='3-minute read',img='img/reel-5.jpg',alt='Placeholder for a photograph of the Neuroinformatics Core',tag='Photo placeholder',href='#'),
 dict(id='gw',kind='training',k='Training',t='Inside the fall grant-writing workshop series',d='Four sessions, from specific aims to the response to reviewers, and what participants took away.',date='October 15, 2026',m='October',read='4-minute read',img='img/reel-2.jpg',alt='Placeholder for a photograph of a workshop',tag='Photo placeholder',href='#'),
]
F=[('all','All stories'),('pilot','Pilot projects'),('core','Core capabilities'),('pubs','Publications'),('people','Investigator profiles'),('training','Training')]
def card(s,lead=False):
    img=f'<figure class="sc-im"><img src="{s["img"]}" alt="{s["alt"]}" loading="lazy"><span class="tag">{s["tag"]}</span></figure>'
    return f'''<li class="sc{' sc-lead' if lead else ''}" data-k="{s['kind']}"><a href="{s['href']}">{img}<div class="sc-t"><p class="eyebrow">{s['k']}</p><h3>{s['t']}</h3><p class="sc-d">{s['d']}</p><p class="meta">The CNAP team · {s['date']} · {s['read']}</p></div></a></li>'''
lead=S[0]
months={}
for s in S[1:]: months.setdefault(s['m']+' 2026',[]).append(s)
mon=''.join(f'<section class="rs-m" aria-label="{m}"><h2>{m}</h2><ul class="rs-grid">{"".join(card(s) for s in ss)}</ul></section>' for m,ss in months.items())
filt=''.join(f'<button type="button" aria-pressed="{"true" if k=="all" else "false"}" data-f="{k}">{l}</button>' for k,l in F)
index=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Research at CNAP · CNAP Member Hub</title>
<link rel="stylesheet" href="guide.css">
</head>
<body data-guide="research" class="rs-page">
{hdr}<main id="main">
  <section class="rs-open" aria-labelledby="t">
    <div class="wrap">
      <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">Research at CNAP</span></nav>
      <div class="rs-mast">
        <div><h1 id="t">Research at CNAP</h1><p class="lead">Work from the Center’s pilot projects, cores, and investigators.</p></div>
        <a class="btn" href="{SUG}">Suggest a story</a>
      </div>
      <div class="pf-filt rs-filt" role="group" aria-label="Show">{filt}</div>
    </div>
  </section>
  <div class="wrap rs-body">
    <ul class="rs-leadlist">{card(lead,True)}</ul>
    {mon}
    <p class="rs-none" hidden>No stories of this kind yet. <a href="{SUG}">Suggest one</a>.</p>
  </div>
</main>
<footer class="foot"><div class="wrap"><span>Cognitive and Neurobiological Approaches to Plasticity Center, Kansas State University</span><span>Prototype. The stories are sample content and the images are illustrations or placeholders. Publishing stories needs a story record and an editor screen, not yet built.</span></div></footer>
<script src="guide.js"></script>
<script>
(function(){{var bs=document.querySelectorAll('.rs-filt button'),cards=document.querySelectorAll('.sc'),ms=document.querySelectorAll('.rs-m'),none=document.querySelector('.rs-none');
bs.forEach(function(b){{b.addEventListener('click',function(){{var f=b.dataset.f,n=0;bs.forEach(function(o){{o.setAttribute('aria-pressed',o===b)}});
cards.forEach(function(c){{var on=f==='all'||c.dataset.k===f;c.hidden=!on;if(on)n++;}});
ms.forEach(function(m){{m.hidden=!m.querySelector('.sc:not([hidden])')}});none.hidden=n>0;}});}});}})();
</script>
</body>
</html>
'''
open(V+'research.html','w').write(index)

rel=''.join(card(s) for s in [S[2],S[1],S[4]])
story=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>What a Night of Sleep Does · CNAP Member Hub</title>
<link rel="stylesheet" href="guide.css">
</head>
<body data-guide="story" class="rs-page st-page">
{hdr}<div class="st-prog" aria-hidden="true"><i></i></div>
<main id="main">
  <article class="story-a" aria-labelledby="t">
    <header class="st-h wrap">
      <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><a href="research.html">Research at CNAP</a><span aria-hidden="true">/</span><span aria-current="page">Pilot project</span></nav>
      <p class="eyebrow">Pilot project</p>
      <h1 id="t">What a night of sleep does to a new memory</h1>
      <p class="st-deck">A CNAP pilot project is recording brain activity during sleep to learn which memories are kept by morning. The team describes its design and what it plans to test next.</p>
      <div class="st-by"><p class="meta">The CNAP team · November 10, 2026 · 4-minute read</p><button type="button" class="btn sm st-copy">Copy link</button></div>
    </header>
    <figure class="st-fig wrap"><img src="img/neurons.jpg" alt="Generated illustration of branching neurons in magenta and teal on a dark ground" width="1600" height="888"><figcaption>Illustration made for this prototype. It is not research data, and a project image will replace it.</figcaption></figure>
    <div class="st-body wrap">
      <div class="st-text">
        <p class="st-lede">Most of what we learn in a day is gone within a week. Some memories last, and a growing body of research points to sleep as one of the reasons. A pilot project funded by CNAP this year is asking a precise version of that question in adults over 65: which features of a night’s sleep predict what a person still remembers in the morning?</p>
        <h2>The design</h2>
        <p>Participants learn a list of word pairs in the evening and are tested twice: once before bed and again after waking. In between, the team records their brain activity across the full night with 64-channel electroencephalography (EEG) in the Cognitive Neuroscience Core’s recording rooms.</p>
        <p>The recordings let the team measure the slow oscillations and sleep spindles of deep sleep, two rhythms linked in earlier studies to memory. The question is whether the amount and timing of those rhythms predict how many pairs each person keeps overnight.</p>
        <blockquote class="st-q"><p>Older adults often sleep less deeply. If deep sleep is part of how memories are kept, that change could explain some of what we see in memory with age.</p><cite>Dr. Amara Okafor, pilot project leader</cite></blockquote>
        <h2>From recordings to results</h2>
        <p>A single night of high-density EEG produces gigabytes of data per person. The Neuroinformatics Core helped the team move its analysis pipeline onto Beocat, the university’s high-performance computing cluster, where steps that once took days now run in hours.</p>
        <p>The first participants were recorded this fall. The team expects to finish data collection in the spring and to present early results at a national sleep research meeting in April 2027.</p>
        <h2>What comes next</h2>
        <p>The second aim tests a practical idea: whether a short afternoon nap can restore overnight retention in participants whose night sleep is fragmented. If it does, the next step would be a larger study, and an application for external funding, which is the milestone every CNAP pilot works toward.</p>
        <p class="st-ack">This project was supported by a grant from the National Institute of General Medical Sciences, P20GM113109, of the National Institutes of Health.</p>
      </div>
      <aside class="st-side" aria-label="About the project">
        <div class="rp-card">
          <h2>About the project</h2>
          <dl class="st-dl">
            <div><dt>Project</dt><dd>Sleep-dependent memory consolidation in older adults</dd></div>
            <div><dt>Award</dt><dd>Pilot project, Grant Year 10</dd></div>
            <div><dt>Project leader</dt><dd>Dr. Amara Okafor</dd></div>
            <div><dt>Mentor</dt><dd>Dr. Elena Voss</dd></div>
            <div><dt>Cores used</dt><dd><a href="core-cn.html">Cognitive Neuroscience Core</a> and <a href="core-ni.html">Neuroinformatics Core</a></dd></div>
          </dl>
        </div>
        <div class="rp-card st-sug"><h2>Have a story?</h2><p>A project milestone, a new paper or grant, or a core capability members should know about.</p><a class="btn" href="{SUG}">Suggest a story</a></div>
      </aside>
    </div>
  </article>
  <section class="wrap st-rel" aria-labelledby="rel-h">
    <div class="st-relh"><h2 id="rel-h">More from Research at CNAP</h2><a class="t3" href="research.html">All stories</a></div>
    <ul class="rs-grid">{rel}</ul>
  </section>
</main>
<footer class="foot"><div class="wrap"><span>Cognitive and Neurobiological Approaches to Plasticity Center, Kansas State University</span><span>Prototype. This story is sample content. The project, people, and quote are fictional.</span></div></footer>
<script src="guide.js"></script>
<script>
(function(){{var b=document.querySelector('.st-copy');if(b)b.addEventListener('click',function(){{var u=location.href;var done=function(){{b.textContent='Link copied';setTimeout(function(){{b.textContent='Copy link'}},2000)}};try{{navigator.clipboard.writeText(u).then(done,function(){{}});}}catch(e){{}}}});
var bar=document.querySelector('.st-prog i'),art=document.querySelector('.st-text');function p(){{if(!bar||!art)return;var r=art.getBoundingClientRect(),h=r.height-innerHeight*.6;var v=Math.min(1,Math.max(0,(-r.top+innerHeight*.3)/Math.max(1,h)));bar.style.transform='scaleX('+v+')';}}addEventListener('scroll',p,{{passive:true}});p();}})();
</script>
</body>
</html>
'''
open(V+'story.html','w').write(story)
print('ok')
