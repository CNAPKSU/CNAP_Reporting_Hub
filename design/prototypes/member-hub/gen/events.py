import sys,datetime as dtm
from urllib.parse import quote
sys.path.insert(0,'/tmp/claude-0/hubproto/gen')
from mail import mt
V='/tmp/claude-0/hubproto/v4/'
core=open(V+'core-ni.html').read()
import importlib.util as _u;_sp=_u.spec_from_file_location('evcal','/tmp/claude-0/hubproto/gen/evcal.py');evcal=_u.module_from_spec(_sp);_sp.loader.exec_module(evcal)
CALMK=evcal.SNIP['markup'];CALJS=evcal.SNIP['script']
hdr=core[core.index('<a class="skip"'):core.index('<main id="main">')]
hdr=hdr.replace('<a href="index.html#cores-h" aria-current="page">Resources</a>','<a href="index.html#cores-h">Resources</a>')
hdr=hdr.replace('<a href="events.html">Events</a>','<a href="events.html" aria-current="page">Events</a>')
TODAY=dtm.date(2026,11,13)
KIND={'ns':'NeuroSync','ctr':'Center event','due':'Deadline','you':'My meeting','cam':'K-State date'}
SHAPE={'ns':'<circle cx="5" cy="5" r="4"/>','ctr':'<path d="M5 .8 9.2 5 5 9.2.8 5z"/>','due':'<rect x="1.2" y="1.2" width="7.6" height="7.6" rx="1"/>','you':'<circle cx="5" cy="5" r="3.2" fill="none" stroke="currentColor" stroke-width="1.8"/>','cam':'<path d="M5 1 9.3 9H.7z"/>'}
def mk(k): return f'<svg viewBox="0 0 10 10" class="emk k-{k}" aria-hidden="true">{SHAPE[k]}</svg>'
NSLOC='Leadership Room 127'
E=[# date,time,end,kind,title,detail,(enddate)
 ('2026-11-04','2:30 p.m.','3:30 p.m.','ns','Dopamine and the speed of choice','NeuroSync talk · '+NSLOC,None),
 ('2026-11-06','All day',None,'due','Pre-submission review requests','Send drafts to the Assistant Director for Grants and Contracts',None),
 ('2026-11-11','2:30 p.m.','3:30 p.m.','ns','Glia and the timing of plasticity','NeuroSync talk · '+NSLOC,None),
 ('2026-11-13','2:00 p.m.','3:00 p.m.','ctr','Behavioral Neuroscience Core office hours','Questions about space, equipment, and procedures',None),
 ('2026-11-17','3:00 p.m.','4:00 p.m.','you','Mentor meeting with Dr. Elena Voss','Shown only to you',None),
 ('2026-11-18','2:30 p.m.','3:30 p.m.','ns','Memory consolidation during sleep','Dr. Priya Raman · '+NSLOC,None),
 ('2026-11-18','4:00 p.m.','5:00 p.m.','cam','Campus seminar: Neural circuits of fear learning','From the K-State calendar',None),
 ('2026-11-19','12:00 p.m.','1:00 p.m.','ctr','Workshop: Writing a strong Specific Aims page','Grant writing workshop series',None),
 ('2026-11-20','All day',None,'due','Year 11 pilot letters of intent','One page, to the Administrative Core by 5:00 p.m.',None),
 ('2026-11-22','All week',None,'cam','Fall break, no classes','November 22 to 29','2026-11-29'),
 ('2026-11-26','All day',None,'cam','Thanksgiving, campus closed','November 26 and 27','2026-11-27'),
 ('2026-11-30','All day',None,'due','Fall reporting closes','Surveys and reports are due in the Member Hub',None),
 ('2026-12-02','2:30 p.m.','3:30 p.m.','ns','Machine learning for spike sorting','Dr. Daniel Kim · '+NSLOC,None),
 ('2026-12-03','10:00 a.m.','10:30 a.m.','you','Check-in with Dr. Elena Voss','Shown only to you',None),
 ('2026-12-10','3:30 p.m.','5:00 p.m.','ctr','Fall social for members and students','Every member, student, and core user is welcome',None),
 ('2026-12-11','All day',None,'cam','Last day of fall classes','From the K-State calendar',None),
 ('2026-12-14','All week',None,'cam','Final examinations','December 14 to 18','2026-12-18'),
 ('2026-12-24','All day',None,'cam','Winter break, campus closed','December 24 to 31','2026-12-31'),
]
def d(s): return dtm.date.fromisoformat(s)
def t24(t):
    h,m=t.replace(' a.m.','').replace(' p.m.','').split(':');h=int(h)
    if 'p.m.' in t and h!=12: h+=12
    return f'{h:02d}{m}00'
def cal_links(e):
    ds,t,te,k,ti,de,end=e
    if k not in('ns','ctr','due'):return ''
    body=de
    if t in('All day','All week'):
        s=ds.replace('-','');en=(d(end or ds)+dtm.timedelta(days=1)).isoformat()
        g=f'https://calendar.google.com/calendar/render?action=TEMPLATE&text={quote(ti)}&dates={s}/{en.replace("-","")}&details={quote(body)}'
        o=f'https://outlook.office.com/calendar/0/deeplink/compose?path=%2Fcalendar%2Faction%2Fcompose&rru=addevent&subject={quote(ti)}&startdt={ds}&enddt={en}&allday=true&body={quote(body)}'
    else:
        a=t24(t);b=t24(te);s=ds.replace('-','')
        g=f'https://calendar.google.com/calendar/render?action=TEMPLATE&text={quote(ti)}&dates={s}T{a}/{s}T{b}&ctz=America/Chicago&details={quote(body)}'
        o=f'https://outlook.office.com/calendar/0/deeplink/compose?path=%2Fcalendar%2Faction%2Fcompose&rru=addevent&subject={quote(ti)}&startdt={ds}T{a[:2]}:{a[2:4]}:00&enddt={ds}T{b[:2]}:{b[2:4]}:00&body={quote(body)}'
    g=g.replace('&','&amp;');o=o.replace('&','&amp;')
    return f'<span class="ev-add"><a href="{o}" target="_blank" rel="noopener">Add to Outlook</a><a href="{g}" target="_blank" rel="noopener">Google</a></span>'
WD=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
MON=['January','February','March','April','May','June','July','August','September','October','November','December']
def row(e):
    ds,t,te,k,ti,de,end=e
    tm=t if t in('All day','All week') else f'{t.replace(" p.m.","").replace(" a.m.","")} to {te}' if te else t
    return f'''<li class="ev k-{k}{' past' if d(ds)<TODAY else ''}" data-k="{k}"><span class="ev-t">{tm}</span><div class="ev-b"><span class="ev-k">{mk(k)}{KIND[k]}</span><b>{ti}</b><span class="ev-d">{de}</span></div>{cal_links(e)}</li>'''
days={}
for e in E: days.setdefault(e[0],[]).append(e)
months={}
for ds in sorted(days): months.setdefault(ds[:7],[]).append(ds)
def dayblock(ds):
    D=d(ds);cls=' is-today' if D==TODAY else (' is-past' if D<TODAY else '')
    lab='Today' if D==TODAY else WD[D.weekday()]
    return f'''<div class="ag-day{cls}" data-day="{ds}"><div class="ag-date"><span class="ag-wd">{lab}</span><span class="ag-n">{D.day}</span><span class="ag-mo">{MON[D.month-1]}</span></div><ul class="ag-evs">{''.join(row(e) for e in days[ds])}</ul></div>'''
past=[ds for ds in sorted(days) if d(ds)<TODAY]
up=[ds for ds in sorted(days) if d(ds)>=TODAY]
upm={}
for ds in up: upm.setdefault(ds[:7],[]).append(ds)
agenda=''.join(f'<section class="ag-m" aria-label="{MON[int(m[5:])-1]} {m[:4]}"><h2>{MON[int(m[5:])-1]} {m[:4]}</h2>{"".join(dayblock(x) for x in dl)}</section>' for m,dl in upm.items())
earlier=f'<details class="ag-past"><summary>Earlier in November <span>{sum(len(days[x]) for x in past)} events</span></summary>{"".join(dayblock(x) for x in past)}</details>'
F=''.join(f'<button type="button" class="ev-f" aria-pressed="true" data-k="{k}">{mk(k)}{l}</button>' for k,l in [('ns','NeuroSync'),('ctr','Center events'),('due','Deadlines'),('you','My meetings'),('cam','K-State dates')])
SUB=mt('cnap@ksu.edu','Event for the CNAP calendar','\n'.join(['Event title:','Date and time:','Location or Zoom link:','Who it is for:','','Description:','','Contact person:','']),cc=None)
SPK=mt('cnap@ksu.edu','NeuroSync speaker suggestion','\n'.join(['Speaker name and institution:','Research topic:','Why CNAP members would value the talk:','','Your name:','']),cc=None)
ns_next=[e for e in E if e[3]=='ns' and d(e[0])>=TODAY][0]
lineup=[('PR','Wednesday, November 18','Memory consolidation during sleep','Dr. Priya Raman'),('DK','Wednesday, December 2','Machine learning for spike sorting','Dr. Daniel Kim, invited speaker'),('+','Spring 2027','13 Wednesdays are open for sign-up','Sign up to present')]
lu=''.join(f'<li><span class="lu-dt">{dt}</span><span class="lu-i" aria-hidden="true">{i}</span><b>{ti}</b><span class="lu-w">{w}</span></li>' for i,dt,ti,w in lineup)
sv=('2027-05-25','All day',None,'ctr','CNAP Site Visit','Core tours, project presentations, keynote address and banquet, and a poster session','2027-05-26')
html=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Events · CNAP Member Hub</title>
<link rel="stylesheet" href="guide.css">
<link rel="stylesheet" href="evcal.css">
</head>
<body data-guide="events" class="ev-page">
{hdr}<main id="main">
  <section class="rs-open ev-open" aria-labelledby="t">
    <div class="wrap">
      <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">Events</span></nav>
      <div class="rs-mast">
        <div><h1 id="t">Events</h1><p class="lead">NeuroSync talks, Center events, deadlines, and campus dates in one place. Your own meetings show only to you.</p></div>
        <div class="ev-acts"><a class="btn" href="{SUB}">Submit an event</a></div>
      </div>
      <div class="ev-feat">
        <div class="ev-poster" aria-hidden="true"><span class="p-day">Wednesday</span><span class="p-num">18</span><span class="p-mon">November</span></div>
        <div class="ev-ft">
          <p class="eyebrow">This week at NeuroSync</p>
          <h2>Memory consolidation during sleep</h2>
          <p class="ev-who"><b>Dr. Priya Raman</b>, Department of Psychological Sciences</p>
          <p class="ev-desc">How slow waves and sleep spindles decide which memories last, in younger and older adults.</p>
          <p class="meta">Wednesday, November 18, 2:30 to 3:30 p.m. · Leadership Room 127 · Refreshments provided</p>
          <div class="ev-fa">{cal_links(ns_next).replace('class="ev-add"','class="ev-add ev-lg"').replace('>Google</a>','>Google Calendar</a>')}</div>
        </div>
      </div>
    </div>
  </section>

  <div class="ev-body">
    <div class="wrap">
      <div class="ev-main">
        <div class="ev-mode" role="group" aria-label="Show the calendar as"><button type="button" data-mode="month" aria-pressed="true">Calendar</button><button type="button" data-mode="list" aria-pressed="false">List</button></div>
        <div class="ev-cal" id="ev-month">{CALMK}</div>
        <div id="ev-list" hidden>
        <div class="ev-bar"><div class="ev-filt" role="group" aria-label="Show">{F}</div><p class="ev-tz">Central Time</p></div>
        {earlier}
        {agenda}
        <p class="ev-none" hidden>Nothing to show. Turn on more types above.</p>
        </div>
      </div>
      <aside class="ev-side" aria-label="Key dates and NeuroSync">
        <div class="rp-card">
          <h2>Key dates</h2>
          <ul class="kd">
            <li class="k-due"><span class="kd-n">20</span><div><b>Year 11 pilot letters of intent</b><span>Friday, November 20</span></div></li>
            <li class="k-due"><span class="kd-n">30</span><div><b>Fall reporting closes</b><span>Monday, November 30</span></div></li>
            <li class="k-ctr"><span class="kd-n">25</span><div><b>2027 CNAP Site Visit</b><span>Tuesday and Wednesday, May 25 and 26</span></div></li>
          </ul>
        </div>
        <div class="rp-card">
          <h2>Subscribe</h2>
          <p class="ev-sub">Please add the Center calendar to Outlook or Google, so new events appear automatically. Your private meetings are never included.</p>
          <button type="button" class="btn ev-copyfeed">Copy calendar link</button>
          <p class="meta ev-feed-note">The subscription link is created when the Hub goes live.</p>
        </div>
      </aside>
    </div>
  </div>

  <section class="ev-ns" aria-labelledby="ns-h">
    <div class="wrap">
      <div class="ev-nsh"><div><p class="eyebrow">Every Wednesday, 2:30 to 3:30 p.m.</p><h2 id="ns-h"><a class="sh-link" href="neurosync.html">NeuroSync Weekly Speaker Series</a></h2><p>Talks are in Leadership Room 127. Refreshments are provided. CNAP members are expected to attend, and guests are welcome.</p></div><a class="btn" href="neurosync.html">The full schedule and past talks</a></div>
      <ol class="lu">{lu}</ol>
    </div>
  </section>

  <section class="ev-sv" aria-labelledby="sv-h">
    <div class="wrap ev-svg">
      <div class="ev-svd" aria-hidden="true"><span>May</span><b>25</b><i>and</i><b>26</b><span>2027</span></div>
      <div>
        <p class="eyebrow">The Center’s main event of the year</p>
        <h2 id="sv-h"><a class="sh-link" href="sitevisit.html">The 2027 CNAP Site Visit</a></h2>
        <ol class="agenda ev-agenda">
          <li><span class="ag-d">Tuesday, May 25<small>Daytime</small></span><span>Core tours, then primary project and pilot project presentations and updates.</span></li>
          <li><span class="ag-d">Tuesday, May 25<small>Evening</small></span><span>Keynote address and banquet.</span></li>
          <li><span class="ag-d">Wednesday, May 26<small>Morning, ending by noon</small></span><span>Poster session, open to everyone.</span></li>
        </ol>
        <div class="ev-fa">{cal_links(sv).replace('class="ev-add"','class="ev-add ev-lg"').replace('>Google</a>','>Google Calendar</a>')}<a class="btn pri" href="sitevisit.html">The program, travel, and FAQ</a><a class="t3" href="sitevisit-2026.html">See the 2026 photographs</a></div>
      </div>
    </div>
  </section>
</main>
<footer class="foot"><div class="wrap"><span>Cognitive and Neurobiological Approaches to Plasticity Center, Kansas State University</span><span>Prototype. The NeuroSync schedule, speakers, and Center events are sample content, shown as of Friday, November 13. K-State dates come from the academic calendar.</span></div></footer>
<script src="guide.js"></script>
<script>
(function(){{
  {CALJS}
}})();
(function(){{var bs=document.querySelectorAll('.ev-mode button'),m=document.getElementById('ev-month'),l=document.getElementById('ev-list');
  function set(k){{bs.forEach(function(b){{b.setAttribute('aria-pressed',b.dataset.mode===k)}});m.hidden=k!=='month';l.hidden=k!=='list';try{{localStorage.setItem('ev-mode',k)}}catch(e){{}}}}
  bs.forEach(function(b){{b.addEventListener('click',function(){{set(b.dataset.mode)}})}});
  var k='month';try{{k=localStorage.getItem('ev-mode')||'month'}}catch(e){{}}set(k);
}})();
</script>
<script>
(function(){{var on={{ns:1,ctr:1,due:1,you:1,cam:1}},bs=document.querySelectorAll('.ev-f'),none=document.querySelector('.ev-none');
function apply(){{var n=0;document.querySelectorAll('.ev').forEach(function(e){{var v=!!on[e.dataset.k];e.hidden=!v;if(v&&!e.classList.contains('past'))n++;}});
document.querySelectorAll('.ag-day').forEach(function(x){{x.hidden=!x.querySelector('.ev:not([hidden])');}});
document.querySelectorAll('.ag-m').forEach(function(x){{x.hidden=!x.querySelector('.ag-day:not([hidden])');}});none.hidden=n>0;}}
bs.forEach(function(b){{b.addEventListener('click',function(){{var k=b.dataset.k;on[k]=on[k]?0:1;b.setAttribute('aria-pressed',!!on[k]);apply();}});}});
var c=document.querySelector('.ev-copyfeed');if(c)c.addEventListener('click',function(){{c.textContent='Available when the Hub goes live';setTimeout(function(){{c.textContent='Copy calendar link'}},2400);}});}})();
</script>
<script src="hubchrome.js" defer></script>
</body>
</html>
'''
open(V+'events.html','w').write(html)
print('ok')
