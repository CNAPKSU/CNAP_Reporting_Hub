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
# Real NeuroSync calendar (dates, weeks with no talk, rooms) from the Center's sign-up sheet; speakers and titles are fictional.
import datetime as dt
TODAY=dt.date(2026,11,14)
POOL=[('EL','t','Dr. Evan Liu','Biology, Kansas State University','Zebrafish and the genetics of learning'),
 ('HC','p','Dr. Hannah Cole','Statistics, Kansas State University','Mixed-effects models for repeated measures'),
 ('AO','p','Dr. Amara Okafor','Pilot project leader, CNAP','Sleep, memory, and the aging brain'),
 ('NS','a','Dr. Nora Shah','Kinesiology, Kansas State University','Exercise and memory in midlife'),
 ('JW','t','Dr. Julian West','Psychological Sciences, University of Kansas','Fear, safety, and the amygdala'),
 ('LP','a','Dr. Lena Park','Pilot project leader, CNAP','Brain stimulation and the speed of motor learning'),
 ('KR','a','Dr. Kendra Ross','Psychology, Wichita State University','Habits, goals, and the striatum'),
 ('MS','p','Dr. Maya Singh','Cognitive Neuroscience Core, CNAP','Eye movements as a window on working memory'),
 ('CB','a','Dr. Claire Bennett','Psychology, University of Missouri','Dopamine and the speed of choice'),
 ('TM','t','Dr. Tomás Medina','Anatomy and Physiology, Kansas State University','Glia and the timing of plasticity'),
 ('PR','p','Dr. Priya Raman','Psychological Sciences, Kansas State University','Memory consolidation during sleep'),
 ('DK','a','Dr. Daniel Kim','Invited speaker, Iowa State University','Machine learning for spike sorting')]
EXTRA=[('Dr. Ben Moreau','Biomedical Engineering, University of Kansas','Wearable EEG outside the lab'),('Dr. Iris Novak','Psychological Sciences, Kansas State University','Language, prediction, and the N400'),('Dr. Omar Haddad','Electrical Engineering, Kansas State University','Closed-loop stimulation for sleep'),('Dr. Grace Lin','Biology, Kansas State University','Songbirds and vocal learning'),('Dr. Felix Brandt','Psychology, Creighton University','Reward, effort, and fatigue'),('Dr. Rosa García','Research project leader, CNAP','Mapping large-scale brain networks'),('Dr. Jordan Lee','Pilot project leader, CNAP','Sleep EEG in shift workers'),('Dr. Sara Holm','Kinesiology, Kansas State University','Balance, aging, and the cerebellum'),('Dr. Victor Osei','Veterinary Medicine, Kansas State University','Inflammation and the aging brain'),('Dr. Mei Tanaka','Psychology, University of Nebraska','Attention in children with ADHD'),('Dr. Luis Romero','Statistics, Kansas State University','Bayesian methods for small samples'),('Dr. Anna Kowal','Neurology, University of Kansas Medical Center','Recovery of movement after stroke'),('Dr. Peter Quinn','Psychological Sciences, Kansas State University','Visual scenes and event memory'),('Dr. Hana Yusuf','Food, Nutrition, Dietetics and Health, Kansas State University','Diet and cognition in older adults'),('Dr. Caleb Ward','Physics, Kansas State University','Modeling neural oscillations'),('Dr. Elena Voss','Mentor, CNAP','Memory, plasticity, and the hippocampus'),('Dr. Ruth Adler','Psychology, Oklahoma State University','Social stress in adolescent rats'),('Dr. Noah Fischer','Computer Science, Kansas State University','Language models of recall'),('Dr. Priscilla Ong','Biochemistry, Kansas State University','Proteins that tag a memory'),('Dr. Marco Silva','Mechanical Engineering, Kansas State University','Sensors for gait in daily life')]
def ini(n): w=n.replace('Dr. ','').split(); return w[0][0]+w[-1][0]
TINT='ptaatp'
def wed(y,m,d): return dt.date(y,m,d)
def mk(sem,room,weeks,off,talks):
    out=[];k=0
    for d in weeks:
        if d in off: out.append(('off',d,off[d]));continue
        if talks is None: out.append(('open',d,None));continue
        if k<len(talks): out.append(('talk',d,talks[k]));k+=1
        else: out.append(('none',d,'No talk this week'))
    return out
def wk(start,n): return [start+dt.timedelta(days=7*i) for i in range(n)]
F26=wk(wed(2026,8,26),17); S27=wk(wed(2027,1,20),17); S26=wk(wed(2026,1,21),17); S26[11]=dt.date(2026,4,7)
F25=wk(wed(2025,8,27),17); S25=wk(wed(2025,1,22),17)
def P(i): return POOL[i]
def X(i): n,r,t=EXTRA[i%len(EXTRA)]; return (ini(n),TINT[i%6],n,r,t)
fall26=[P(0),P(1),P(2),P(3),None,P(4),P(5),P(6),P(7),P(8),P(9),P(10),P(11)]
SEM=[
 ('s27','Spring 2027','Sign-up is open','Leadership Room 127',mk('s27','',S27,{S27[0]:'First week of classes',S27[8]:'Spring break',S27[15]:'Last week of classes',S27[16]:'Final exams'},None)),
 ('f26','Fall 2026','This semester','Leadership Room 127',None),
 ('s26','Spring 2026','Past','Business Building, Room 1078',mk('s26','',S26,{S26[0]:'First week of classes',S26[8]:'Spring break',S26[15]:'Last week of classes',S26[16]:'Final exams'},[X(i) for i in range(13)])),
 ('f25','Fall 2025','Past','Business Building',mk('f25','',F25,{F25[0]:'First week of classes',F25[13]:'Fall break',F25[15]:'Last week of classes',F25[16]:'Final exams'},[X(i+5) for i in range(13)])),
 ('s25','Spring 2025','Past','Bluemont Hall, Room 498',mk('s25','',S25,{S25[0]:'First week of classes',S25[3]:'On-campus events canceled for weather',S25[8]:'Spring break',S25[16]:'Final exams'},[X(i+9) for i in range(14)]))]
f=[];k=0
offf={F26[0]:'First week of classes',F26[13]:'Fall break',F26[15]:'Last week of classes',F26[16]:'Final exams'}
for d in F26:
    if d in offf: f.append(('off',d,offf[d]));continue
    t=fall26[k];k+=1
    f.append(('none',d,'No talk this week') if t is None else ('talk',d,t))
SEM[1]=('f26','Fall 2026','This semester','Leadership Room 127',f)
SIGN=mt('cnap@ksu.edu','Presenting at NeuroSync','\n'.join(['Name:','Department:','','Working title:','','Dates that work for me:','']),cc=None)
SUGG=mt('cnap@ksu.edu','NeuroSync speaker suggestion','\n'.join(['Speaker name and institution:','Research topic:','Why CNAP members would value the talk:','','Your name:','']),cc=None)
IDEA=mt('cnap@ksu.edu','An idea for NeuroSync','\n'.join(['Name:','','My idea (a topic, a format, or a change to the series):','']),cc=None)
def gcal(iso,t):
    d=iso.replace('-','')
    return 'https://calendar.google.com/calendar/render?action=TEMPLATE&amp;text='+quote('NeuroSync: '+t)+f'&amp;dates={d}T203000Z/{d}T213000Z&amp;location='+quote(LOC+', Kansas State University')
def ocal(iso,t):
    return 'https://outlook.office.com/calendar/0/deeplink/compose?subject='+quote('NeuroSync: '+t)+f'&amp;startdt={iso}T14:30:00&amp;enddt={iso}T15:30:00&amp;location='+quote(LOC)
def signd(d):
    return mt('cnap@ksu.edu','Presenting at NeuroSync on '+d.strftime('%B %-d'),'\n'.join(['Name:','Department:','','Working title:','']),cc=None)
def date_cell(d): return f'<span class="ns-rd"><b>{d.day}</b><small>{d.strftime("%b")}</small></span>'
def srow(kind,d,x):
    if kind=='off': return f'<li class="ns-r is-off">{date_cell(d)}<span class="ns-ra ns-ra-off" aria-hidden="true"></span><div class="ns-rb"><p class="ns-rt">No talk</p><p class="ns-rw">{x}</p></div></li>'
    if kind=='none': return f'<li class="ns-r is-off">{date_cell(d)}<span class="ns-ra ns-ra-off" aria-hidden="true"></span><div class="ns-rb"><p class="ns-rt">No talk</p><p class="ns-rw">{x}</p></div></li>'
    if kind=='open': return f'<li class="ns-r is-open">{date_cell(d)}<span class="ns-ra ns-ra-open" aria-hidden="true">+</span><div class="ns-rb"><p class="ns-rt">Open</p><p class="ns-rw">Present your own work, or invite a speaker.</p></div><a class="btn sm" href="{signd(d)}">Sign up for {d.strftime("%B %-d")}</a></li>'
    i,t,n,role,ti=x
    st='past' if d<TODAY else ('next' if (d-TODAY).days<7 else 'up')
    tag={'past':'<span class="ns-tag">Recording to come</span>','next':'<span class="ns-tag on">This week</span>','up':f'<a class="ns-add" href="{gcal(d.isoformat(),ti)}" target="_blank" rel="noopener">Add to calendar</a>'}[st]
    return f'<li class="ns-r is-{st}">{date_cell(d)}<span class="cm-av av-{t}" aria-hidden="true">{i}</span><div class="ns-rb"><p class="ns-rt">{ti}</p><p class="ns-rw">{n} · {role}</p></div>{tag}</li>'
tabs=''.join(f'<button type="button" role="tab" aria-selected="{"true" if k=="f26" else "false"}" aria-controls="ns-{k}" id="ns-t-{k}"><b>{n}</b><span>{sub}</span></button>' for k,n,sub,room,rows in SEM)
def panel(k,n,sub,room,rows):
    talks=sum(1 for r in rows if r[0]=='talk'); opens=sum(1 for r in rows if r[0]=='open')
    head=f'<p class="ns-ph"><b>{n}</b> · {room} · ' + (f'{opens} open dates. Please choose a date to sign up.' if opens else f'{talks} talks') + '</p>'
    return f'<div class="ns-pnl" id="ns-{k}" role="tabpanel" aria-labelledby="ns-t-{k}"{"" if k=="f26" else " hidden"}>{head}<ol class="ns-rows">{"".join(srow(*r) for r in rows)}</ol></div>'
panels=''.join(panel(*s) for s in SEM)
def card(d,x,sem):
    i,t,n,role,ti=x
    return f'''<li class="ns-v" data-yr="{sem}"><div class="ns-vm av-{t}" aria-hidden="true"><span class="ns-vi">{i}</span><span class="ns-play"><svg viewBox="0 0 20 20" width="18" height="18"><path d="M6 4l10 6-10 6z" fill="currentColor"/></svg></span></div><div class="ns-vb"><p class="ns-vd">{d.strftime("%B %-d, %Y")}</p><p class="ns-vt">{ti}</p><p class="ns-vw">{n}<br>{role}</p><p class="ns-vs">Recording to come</p></div></li>'''
pastrows=[(d,x,k) for k,n,sub,room,rows in SEM for kind,d,x in rows if kind=='talk' and d<TODAY]
pastrows.sort(key=lambda r:r[0],reverse=True)
past=''.join(card(*r) for r in pastrows)
yrbtn='<button type="button" aria-pressed="true" data-yr="f26">Fall 2026</button>'+''.join(f'<button type="button" aria-pressed="false" data-yr="{k}">{n}</button>' for k,n,sub,room,rows in SEM if k in ('s26','f25','s25'))
INV=f'''<article class="ns-fly" aria-labelledby="fly-h">
        <div class="ns-fly-top"><p class="ns-fk">Invited speaker · Wednesday, December 2</p><div class="ns-fh"><div class="ns-hs av-a" aria-hidden="true"><span>DK</span><small>Headshot to come</small></div><div><p class="ns-fl">The talk</p><h3 id="fly-h">Machine learning for spike sorting</h3><p class="ns-fn">Dr. Daniel Kim</p><p class="ns-fr">Associate Professor of Computer Science and director of the Neural Data Lab, Iowa State University</p></div></div></div>
        <div class="ns-fly-b">
          <div><p class="ns-fl">About the speaker</p><p>Dr. Kim builds machine-learning tools that sort the electrical signals of single neurons from large recordings, so that labs can study thousands of cells at once. His lab shares the lab’s methods as open-source software used by groups across the country.</p></div>
          <div><p class="ns-fl">Recognition</p><ul class="ns-rec"><li>Early Career Award, a national neuroscience society, 2024</li><li>Funded by the National Institutes of Health and the National Science Foundation</li></ul></div>
        </div>
        <dl class="ns-fly-w"><div><dt>When</dt><dd>Wednesday, December 2, 2026<br>2:30 to 3:30 p.m.</dd></div><div><dt>Where</dt><dd>{LOC}<br>Refreshments provided</dd></div><div><dt>Online</dt><dd>Zoom. The link is in the weekly email.</dd></div><div><dt>Hosted by</dt><dd>The CNAP Center. Invited by Dr. Priya Raman.</dd></div></dl>
        <p class="ns-fq">Questions? <a href="mailto:mkwills@ksu.edu">mkwills@ksu.edu</a> · <a href="{gcal('2026-12-02','Machine learning for spike sorting')}" target="_blank" rel="noopener">Add to Google Calendar</a> · <a href="{ocal('2026-12-02','Machine learning for spike sorting')}" target="_blank" rel="noopener">Outlook</a></p>
      </article>'''

import math as _m, random as _r
_r.seed(11)
def _trace():
    pts=[];x=0.0;base=60
    spikes={140,175,420,640,668,690,930,1110}
    burst=(760,860)
    while x<=1200:
        xi=int(x)
        if any(abs(xi-s)<1 for s in spikes):
            pts+= [(x,base),(x+2,base-46),(x+4,base+14),(x+9,base+6),(x+14,base)];x+=14;continue
        y=base+_r.uniform(-1.6,1.6)+1.8*_m.sin(x/9.0)
        if burst[0]<x<burst[1]:
            env=_m.sin(_m.pi*(x-burst[0])/(burst[1]-burst[0]))
            y+=env*11*_m.sin(x*0.9)
        pts.append((x,y));x+=2
    return 'M'+' L'.join(f'{a:.1f} {b:.1f}' for a,b in pts)
wave=_trace()

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
  <nav class="spine sv-rail" aria-label="Sections on this page"><p class="spine-h">On this page</p><div class="spine-track" aria-hidden="true"><span class="spine-fill"></span></div><ol><li><a href="#ns-week"><span class="n"><b>1</b></span><span>This week</span></a></li><li><a href="#ns-sched"><span class="n"><b>2</b></span><span>The schedule</span></a></li><li><a href="#ns-past"><span class="n"><b>3</b></span><span>Past talks</span></a></li><li><a href="#ns-join"><span class="n"><b>4</b></span><span>Be part of NeuroSync</span></a></li><li><a href="#ns-email"><span class="n"><b>5</b></span><span>The weekly email</span></a></li></ol></nav>
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
        <article class="ns-wk" id="ns-week" aria-labelledby="wk-t">
          <p class="ns-wkk"><span class="ns-dot" aria-hidden="true"></span>This week at NeuroSync</p>
          <div class="ns-wkh"><div class="ns-hs av-p" aria-hidden="true"><span>PR</span><small>Headshot to come</small></div><div><p class="ns-wkd">Wednesday, November 18<br>2:30 to 3:30 p.m., Leadership Room 127</p><p class="ns-wkn">Dr. Priya Raman</p><p class="ns-wkr">Associate Professor, Psychological Sciences, Kansas State University</p></div></div>
          <div class="ns-wkm"><h2 id="wk-t">Memory consolidation during sleep</h2>
          <p class="ns-abs">How slow waves and sleep spindles decide which memories last, in younger and older adults. Dr. Raman will share new recordings from her lab’s overnight studies, and what the recordings suggest about memory in aging.</p>
          <details class="ns-bio"><summary>About Dr. Raman</summary><p>Dr. Raman studies how sleep shapes memory across the lifespan, using overnight electroencephalography (EEG) and behavioral testing. She leads a CNAP research project and collaborates with the Cognitive Neuroscience Core.</p></details>
          <div class="ns-wka"><span class="ns-cal">Add to <a href="{gcal('2026-11-18','Memory consolidation during sleep')}" target="_blank" rel="noopener">Google Calendar</a> or <a href="{ocal('2026-11-18','Memory consolidation during sleep')}" target="_blank" rel="noopener">Outlook</a></span></div></div>
        </article>
      </div>
    </div>
  </section>

  <section class="ns-sec" id="ns-sched" aria-labelledby="ns-sched-h">
    <div class="wrap">
      <header class="sv-sh"><h2 id="ns-sched-h">The schedule</h2><p>Talks run every Wednesday of the fall and spring semesters, except the first week of classes, breaks, the last week of classes, and finals. Spring 2027 sign-up is open now.</p></header>
      {INV}
      <div class="sv-days ns-semtabs" role="tablist" aria-label="Semester">{tabs}</div>
      {panels}
    </div>
  </section>

  <section class="ns-sec ns-past" id="ns-past" aria-labelledby="ns-past-h">
    <div class="wrap">
      <header class="sv-sh"><h2 id="ns-past-h">Past talks</h2><p>Recordings are added after each talk, so you can catch up on a week you missed or share a talk with your lab.</p></header>
      <div class="pf-filt ns-yf" role="group" aria-label="Semester">{yrbtn}</div>
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

  <section class="ns-sec ns-email" id="ns-email" aria-labelledby="ns-email-h">
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
  yb.forEach(function(b){{b.addEventListener('click',function(){{yb.forEach(function(o){{o.setAttribute('aria-pressed',o===b);}});vs.forEach(function(v){{v.hidden=v.dataset.yr!==b.dataset.yr;}});}});}});
  vs.forEach(function(v){{v.hidden=v.dataset.yr!=='f26';}});
  var sp=document.querySelector('.sv-rail'),links=[].slice.call(sp.querySelectorAll('ol a')),secs=links.map(function(a){{return document.querySelector(a.getAttribute('href'));}}),tr=sp.querySelector('.spine-track'),fl=sp.querySelector('.spine-fill'),ol=sp.querySelector('ol');
  function spy(){{var y=innerHeight*.35,k=-1;secs.forEach(function(s,i){{if(s.getBoundingClientRect().top<y)k=i;}});links.forEach(function(a,i){{if(i===k)a.setAttribute('aria-current','step');else a.removeAttribute('aria-current');a.classList.toggle('done',i<k);}});sp.classList.toggle('on',scrollY>200);}}
  function track(){{if(!tr||getComputedStyle(tr).display==='none')return;var o=ol.getBoundingClientRect().top;function dot(a){{return a.getBoundingClientRect().top-o+parseFloat(getComputedStyle(a,'::before').top)+5;}}var t=dot(links[0]),b=dot(links[links.length-1]);tr.style.top=(ol.offsetTop+t)+'px';tr.style.height=(b-t)+'px';var c=sp.querySelector('a[aria-current]');fl.style.height=c?(dot(c)-t)+'px':'0px';}}
  addEventListener('scroll',function(){{spy();track();}},{{passive:true}});addEventListener('resize',track);['mouseenter','mouseleave','focusin','focusout','transitionend'].forEach(function(e){{sp.addEventListener(e,function(){{requestAnimationFrame(track);setTimeout(track,280);}});}});spy();track();
  if('IntersectionObserver' in window){{document.documentElement.classList.add('sv-js');var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{e.target.classList.add('in');io.unobserve(e.target);}}}});}},{{rootMargin:'0px 0px -20% 0px'}});document.querySelectorAll('.sv-sh').forEach(function(el){{io.observe(el);}});}}
}})();
</script>
<script src="hubchrome.js" defer></script>
</body>
</html>
'''
open(V+'neurosync.html','w').write(page)
print('ok')
