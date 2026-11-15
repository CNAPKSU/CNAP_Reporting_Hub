import sys
from urllib.parse import quote
sys.path.insert(0,'/tmp/claude-0/hubproto/gen')
from mail import mt
V='/tmp/claude-0/hubproto/v4/'
core=open(V+'core-ni.html').read()
hdr=core[core.index('<a class="skip"'):core.index('<main id="main">')]
hdr=hdr.replace('<a href="index.html#cores-h" aria-current="page">Resources</a>','<a href="index.html#cores-h">Resources</a>')
hdr=hdr.replace('<a href="events.html">Events</a>','<a href="events.html" aria-current="page">Events</a>')
LOC='Leadership Room 127'
# Fictional speakers, matching the Events page and the homepage.
# date iso, weekday-date text, initials, tint, name, role, title, state
FALL=[('2026-09-02','September 2','EL','t','Dr. Evan Liu','Biology, Kansas State University','Zebrafish and the genetics of learning','past'),
 ('2026-09-16','September 16','AO','p','Dr. Amara Okafor','Pilot project leader, CNAP','Sleep, memory, and the aging brain','past'),
 ('2026-09-30','September 30','NS','a','Dr. Nora Shah','Kinesiology, Kansas State University','Exercise and memory in midlife','past'),
 ('2026-10-14','October 14','JW','t','Dr. Julian West','Psychological Sciences, University of Kansas','Fear, safety, and the amygdala','past'),
 ('2026-10-28','October 28','MS','p','Dr. Maya Singh','Cognitive Neuroscience Core, CNAP','Eye movements as a window on working memory','past'),
 ('2026-11-04','November 4','CB','a','Dr. Claire Bennett','Psychology, University of Missouri','Dopamine and the speed of choice','past'),
 ('2026-11-11','November 11','TM','t','Dr. Tomás Medina','Anatomy and Physiology, Kansas State University','Glia and the timing of plasticity','past'),
 ('2026-11-18','November 18','PR','p','Dr. Priya Raman','Psychological Sciences, Kansas State University','Memory consolidation during sleep','next'),
 ('2026-12-02','December 2','DK','a','Dr. Daniel Kim','Computer Science, Kansas State University','Machine learning for spike sorting','up'),
 ('2026-12-09','December 9','AH','t','Dr. Ana Herrera','Kinesiology, Kansas State University','Stress, the heart, and the aging brain','up')]
SPRING=[('2027-01-27','January 27','SN','p','Dr. Sam Novak','Psychological Sciences, Kansas State University','Rodent models of memory decline','up'),
 ('2027-02-03','February 3','LT','a','Dr. Lea Torres','Psychology, University of Nebraska','Learning across the lifespan','up'),
 ('2027-02-10','February 10','MO','t','Dr. Maya Okafor','Psychological Sciences, Kansas State University','Attention and the sleeping brain','up'),
 ('2027-02-17','February 17','RB','p','Dr. Ravi Bhat','Neuroscience, Washington University in St. Louis','Imaging small circuits in behaving animals','up'),
 ('2027-02-24','February 24','','','Open date','','Sign up to present','open'),
 ('2027-03-03','March 3','','','Open date','','Sign up to present','open')]
SIGN=mt('cnap@ksu.edu','Presenting at NeuroSync','\n'.join(['Name:','Department:','','Working title:','','Dates that work for me:','']),cc=None)
SUGG=mt('cnap@ksu.edu','NeuroSync speaker suggestion','\n'.join(['Speaker name and institution:','Research topic:','Why CNAP members would value the talk:','','Your name:','']),cc=None)
IDEA=mt('cnap@ksu.edu','An idea for NeuroSync','\n'.join(['Name:','','My idea (a topic, a format, or a change to the series):','']),cc=None)
def gcal(iso,t):
    d=iso.replace('-','')
    return 'https://calendar.google.com/calendar/render?action=TEMPLATE&amp;text='+quote('NeuroSync: '+t)+f'&amp;dates={d}T203000Z/{d}T213000Z&amp;location='+quote(LOC+', Kansas State University')
def ocal(iso,t):
    return 'https://outlook.office.com/calendar/0/deeplink/compose?subject='+quote('NeuroSync: '+t)+f'&amp;startdt={iso}T14:30:00&amp;enddt={iso}T15:30:00&amp;location='+quote(LOC)
def srow(r):
    iso,dt,i,t,n,role,ti,st=r
    if st=='open':
        return f'<li class="ns-r is-open"><span class="ns-rd"><b>{dt.split()[1]}</b><small>{dt.split()[0][:3]}</small></span><span class="ns-ra ns-ra-open" aria-hidden="true">+</span><div class="ns-rb"><p class="ns-rt">This date is open</p><p class="ns-rw">Present your own work, or bring a speaker.</p></div><a class="btn sm" href="{SIGN}">Sign up to present</a></li>'
    tag={'past':'<span class="ns-tag">Recording to come</span>','next':'<span class="ns-tag on">This week</span>','up':f'<a class="ns-add" href="{gcal(iso,ti)}" target="_blank" rel="noopener">Add to calendar</a>'}[st]
    return f'<li class="ns-r is-{st}"><span class="ns-rd"><b>{dt.split()[1]}</b><small>{dt.split()[0][:3]}</small></span><span class="cm-av av-{t}" aria-hidden="true">{i}</span><div class="ns-rb"><p class="ns-rt">{ti}</p><p class="ns-rw">{n} · {role}</p></div>{tag}</li>'
fall=''.join(srow(r) for r in FALL); spring=''.join(srow(r) for r in SPRING)
PAST=[r for r in FALL if r[7]=='past'][::-1]
LAST=[('2026-04-22','April 22','KR','a','Dr. Kendra Ross','Psychology, Wichita State University','Habits, goals, and the striatum'),
      ('2026-04-08','April 8','BM','t','Dr. Ben Moreau','Biomedical Engineering, University of Kansas','Wearable EEG outside the lab'),
      ('2026-03-11','March 11','HC','p','Dr. Hannah Cole','Statistics, Kansas State University','Mixed-effects models for repeated measures'),
      ('2026-02-18','February 18','LP','a','Dr. Lena Park','Pilot project leader, CNAP','Brain stimulation and motor learning')]
def card(r,yr):
    iso,dt,i,t,n,role,ti=r[:7]
    return f'''<li class="ns-v" data-yr="{yr}"><div class="ns-vm av-{t}" aria-hidden="true"><span class="ns-vi">{i}</span><span class="ns-play"><svg viewBox="0 0 20 20" width="18" height="18"><path d="M6 4l10 6-10 6z" fill="currentColor"/></svg></span></div><div class="ns-vb"><p class="ns-vd">{dt}, {iso[:4]}</p><p class="ns-vt">{ti}</p><p class="ns-vw">{n}<br>{role}</p><p class="ns-vs">Recording to come</p></div></li>'''
past=''.join(card(r,'2026-27') for r in PAST)+''.join(card(r,'2025-26') for r in LAST)

wave='M0 60 '+' '.join(f'Q {x+15} {60-(38 if k%3==1 else 18 if k%3==0 else 28)*(1 if k%2==0 else -1)} {x+30} 60' for k,x in enumerate(range(0,1200,30)))

page=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>NeuroSync · CNAP Member Hub</title>
<link rel="stylesheet" href="guide.css">
</head>
<body class="ns-page">
{hdr}<main id="main">
  <section class="ns-hero" aria-labelledby="t">
    <svg class="ns-wave" viewBox="0 0 1200 120" preserveAspectRatio="none" aria-hidden="true"><path d="{wave}"/></svg>
    <div class="wrap">
      <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><a href="events.html">Events</a><span aria-hidden="true">/</span><span aria-current="page">NeuroSync</span></nav>
      <div class="ns-hg">
        <div>
          <p class="for">The CNAP weekly speaker series</p>
          <h1 id="t">NeuroSync</h1>
          <p class="ns-lead">Every Wednesday, a researcher from K-State or beyond brings new work to the whole Center, followed by questions and conversation over refreshments.</p>
          <dl class="ns-facts"><div><dt>When</dt><dd>Wednesdays, 2:30 to 3:30 p.m.</dd></div><div><dt>Where</dt><dd>{LOC}</dd></div><div><dt>Who comes</dt><dd>CNAP members are expected to attend. Guests are welcome.</dd></div></dl>
        </div>
        <article class="ns-wk" aria-labelledby="wk-t">
          <p class="ns-wkk"><span class="ns-dot" aria-hidden="true"></span>This week at NeuroSync</p>
          <div class="ns-wkh"><div class="ns-hs av-p" aria-hidden="true"><span>PR</span><small>Headshot to come</small></div><div><p class="ns-wkd">Wednesday, November 18</p><p class="ns-wkn">Dr. Priya Raman</p><p class="ns-wkr">Associate Professor, Psychological Sciences, Kansas State University</p></div></div>
          <h2 id="wk-t">Memory consolidation during sleep</h2>
          <p class="ns-abs">How slow waves and sleep spindles decide which memories last, in younger and older adults. Dr. Raman will share new recordings from her lab’s overnight studies, and what they suggest about memory in aging.</p>
          <details class="ns-bio"><summary>About Dr. Raman</summary><p>Dr. Raman studies how sleep shapes memory across the lifespan, using overnight electroencephalography (EEG) and behavioral testing. She leads a CNAP research project and collaborates with the Cognitive Neuroscience Core.</p></details>
          <div class="ns-wka"><span class="ns-cal">Add to <a href="{gcal('2026-11-18','Memory consolidation during sleep')}" target="_blank" rel="noopener">Google Calendar</a> or <a href="{ocal('2026-11-18','Memory consolidation during sleep')}" target="_blank" rel="noopener">Outlook</a></span></div>
        </article>
      </div>
    </div>
  </section>

  <section class="ns-sec" id="ns-sched" aria-labelledby="ns-sched-h">
    <div class="wrap">
      <header class="sv-sh"><h2 id="ns-sched-h">The schedule</h2><p>Talks run through the fall and spring semesters. Open dates are waiting for a speaker.</p></header>
      <div class="sv-days" role="tablist" aria-label="Semester"><button type="button" role="tab" aria-selected="true" aria-controls="ns-fall" id="ns-t1"><b>Fall 2026</b><span>September to December</span></button><button type="button" role="tab" aria-selected="false" aria-controls="ns-spring" id="ns-t2"><b>Spring 2027</b><span>January to May</span></button></div>
      <ol class="ns-rows" id="ns-fall" role="tabpanel" aria-labelledby="ns-t1">{fall}</ol>
      <ol class="ns-rows" id="ns-spring" role="tabpanel" aria-labelledby="ns-t2" hidden>{spring}</ol>
    </div>
  </section>

  <section class="ns-sec ns-past" id="ns-past" aria-labelledby="ns-past-h">
    <div class="wrap">
      <header class="sv-sh"><h2 id="ns-past-h">Past talks</h2><p>Recordings are added after each talk, so you can catch up on a week you missed or share a talk with your lab.</p></header>
      <div class="pf-filt ns-yf" role="group" aria-label="Year"><button type="button" aria-pressed="true" data-yr="all">All years</button><button type="button" aria-pressed="false" data-yr="2026-27">2026 to 2027</button><button type="button" aria-pressed="false" data-yr="2025-26">2025 to 2026</button></div>
      <ul class="ns-vs">{past}</ul>
    </div>
  </section>

  <section class="ns-sec ns-join" id="ns-join" aria-labelledby="ns-join-h">
    <div class="wrap">
      <header class="sv-sh"><h2 id="ns-join-h">Be part of NeuroSync</h2></header>
      <div class="ns-three">
        <article><p class="sv-n num">01</p><h3>Present your work</h3><p>Project leaders, core staff, and trainees are welcome to present. A NeuroSync talk is a good place to try out a conference talk or a job talk.</p><a class="btn pri" href="{SIGN}">Sign up to present</a></article>
        <article><p class="sv-n num">02</p><h3>Suggest a speaker</h3><p>Know a researcher whose work CNAP members should hear? The CNAP team handles the invitation and the visit.</p><a class="btn" href="{SUGG}">Suggest a speaker</a></article>
        <article><p class="sv-n num">03</p><h3>Share an idea</h3><p>A topic, a format, or a change to the series. Ideas from members shape each semester’s schedule.</p><a class="btn" href="{IDEA}">Send an idea</a></article>
      </div>
    </div>
  </section>

  <section class="ns-sec ns-email" aria-labelledby="ns-email-h">
    <div class="wrap ns-eg">
      <div><header class="sv-sh"><h2 id="ns-email-h">This Week at NeuroSync</h2><p>Every Monday the CNAP team emails the week’s talk to all members: the speaker’s headshot and biography, the talk title and summary, and the room and time. Everything in the email is also on this page.</p></header></div>
      <figure class="ns-mail" aria-label="A sketch of the weekly email">
        <p class="ns-mf">From CNAP · Monday</p>
        <p class="ns-ms">This Week at NeuroSync</p>
        <div class="ns-mb"><span class="ns-mh av-p" aria-hidden="true">PR</span><div><p class="ns-mt">Memory consolidation during sleep</p><p class="ns-mw">Dr. Priya Raman · Wednesday, 2:30 p.m. · {LOC}</p></div></div>
        <p class="ns-ml"><span></span><span></span><span class="s"></span></p>
        <p class="ns-mbtns"><span>Full schedule</span><span>Sign up to present</span><span>Past talks</span><span>Send an idea</span></p>
      </figure>
    </div>
  </section>
</main>
<footer class="foot"><div class="wrap"><span>Cognitive and Neurobiological Approaches to Plasticity Center, Kansas State University</span><span>Prototype. The speakers, talks, and biographies are fictional, and recordings aren’t connected yet.</span></div></footer>
<script>
(function(){{
  var tabs=[].slice.call(document.querySelectorAll('.sv-days [role=tab]'));
  tabs.forEach(function(t,i){{t.addEventListener('click',function(){{tabs.forEach(function(o){{var on=o===t;o.setAttribute('aria-selected',on);document.getElementById(o.getAttribute('aria-controls')).hidden=!on;}});}});
    t.addEventListener('keydown',function(e){{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){{var n=tabs[(i+1)%tabs.length];n.click();n.focus();}}}});}});
  var yb=document.querySelectorAll('.ns-yf button'),vs=document.querySelectorAll('.ns-v');
  yb.forEach(function(b){{b.addEventListener('click',function(){{yb.forEach(function(o){{o.setAttribute('aria-pressed',o===b);}});vs.forEach(function(v){{v.hidden=b.dataset.yr!=='all'&&v.dataset.yr!==b.dataset.yr;}});}});}});
  if('IntersectionObserver' in window){{document.documentElement.classList.add('sv-js');var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{e.target.classList.add('in');io.unobserve(e.target);}}}});}},{{rootMargin:'0px 0px -20% 0px'}});document.querySelectorAll('.sv-sh').forEach(function(el){{io.observe(el);}});}}
}})();
</script>
</body>
</html>
'''
open(V+'neurosync.html','w').write(page)
print('ok')
