V='/tmp/claude-0/hubproto/v4/'
core=open(V+'core-ni.html').read()
hdr=core[core.index('<a class="skip"'):core.index('<main id="main">')]
hdr=hdr.replace('<a href="index.html#cores-h" aria-current="page">Resources</a>','<a href="index.html#cores-h">Resources</a>')
hdr=hdr.replace('<a href="reporting.html">Reporting</a>','<a href="reporting.html" aria-current="page">Reporting</a>')
hdr=hdr.replace('<a class="mywork" href="index.html#wk">','<a class="mywork" href="reporting.html">')

def pill(s):
    m={'progress':('In progress','st-on'),'todo':('Not started',''),'done':('Submitted','st-ok'),'opt':('Opted out','st-opt')}
    t,c=m[s];return f'<span class="st {c}">{t}</span>'
def row(name,ctx,state,time,acts,extra=''):
    return f'''<li class="rp-row"><div class="rp-m"><p class="rp-n">{name}</p><p class="rp-c">{ctx}</p>{extra}</div><div class="rp-s">{pill(state)}<span class="rp-t">{time}</span></div><div class="rp-a">{acts}</div></li>'''
def b(lab,pri=False,href='form-preview'): return f'<a class="btn{" pri" if pri else ""} sm" href="#{href}">{lab}</a>'
def q(lab,href='#'): return f'<a class="t3" href="{href}">{lab}</a>'
ring='''<svg viewBox="0 0 120 120" class="rp-ring" aria-hidden="true"><circle cx="60" cy="60" r="52" class="r-bg"/><circle cx="60" cy="60" r="52" class="r-ok" pathLength="6" style="stroke-dasharray:1 6"/><circle cx="60" cy="60" r="52" class="r-opt" pathLength="6" style="stroke-dasharray:1 6;stroke-dashoffset:-1"/></svg>'''
G=[
 ('Your CNAP grant','These surveys and reports ask about your project and your mentoring relationship.',[
   row('Pilot Project Semiannual Progress Report','Sleep-dependent memory consolidation in older adults','progress','1–2 page upload, plus 5 minutes',b('Continue',True)+q('Preview')),
   row('Mentee Survey','Your mentoring with Dr. Elena Voss','todo','About 10 minutes',b('Start')+q('Preview'),'<p class="rp-x">Your answers are confidential. Your mentor never sees them.</p>')]),
 ('NIH documents','Collected once a year for the Center’s Research Performance Progress Report (RPPR) to NIH.',[
   row('NIH Documents: Biosketch, Current and Pending (Other) Support, and Malign Foreign Talent Recruitment Program (MFTRP) Certification','Due Thursday, November 19','todo','1–3 PDF uploads',b('Start')+q('Preview'),'<p class="rp-x rp-due">6 days left, earlier than the rest of your reporting</p>')]),
 ('Other Center features and services','These surveys cover Center programs and events.',[
   row('Team Synergy Survey','How well CNAP members work together across disciplines','todo','About 10 minutes',b('Start')+q('Preview'))]),
]
groups=''.join(f'''<div class="rp-g"><div class="rp-gh"><h3>{t}</h3><p>{s}</p></div><ul class="rp-list">{''.join(rs)}</ul></div>''' for t,s,rs in G)
done=''.join([
 row('Behavioral Neuroscience (BN) Core Facility User Survey','Submitted Monday, November 9','done','About 10 minutes',q('View your answers')),
 row('Cognitive Neuroscience (CN) Core User Survey','You told us you didn’t use this core this session','opt','Opted out November 9',q('Change your answer'))])
year=[
 ('Year 10 Fall','Open now','st-on','Opened November 2. Due Monday, November 30.','Six surveys and reports, about 1 hour 20 minutes in all.',True),
 ('Year 10 Spring','Not open yet','','Opens mid-April 2027. Due early May.','Expected for your roles: the Pilot Project Semiannual Progress Report, the Mentee Survey, and the core user surveys, about 1 hour.',False),
]
yl=''.join(f'''<li class="{'is-now' if now else ''}"><span class="yl-dot" aria-hidden="true"></span><div><h3>{n} <span class="st {c}">{s}</span></h3><p>{d}</p><p class="meta">{t}</p></div></li>''' for n,s,c,d,t,now in year)
html=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Reporting · CNAP Member Hub</title>
<link rel="stylesheet" href="guide.css">
</head>
<body data-guide="reporting" class="rp-page">
{hdr}<main id="main">
  <section class="rp-open" aria-labelledby="t">
    <div class="wrap">
      <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">Reporting</span></nav>
      <div class="rp-hero">
        <div class="rp-hd">
          <p class="for">Year 10 Fall reporting</p>
          <h1 id="t">Your reporting, Amara</h1>
          <p class="lead">What you report here goes into the Center’s annual Research Performance Progress Report (RPPR) to the National Institutes of Health (NIH). Other respondents never see your answers.</p>
          <dl class="rp-facts">
            <div><dt>Due</dt><dd>Monday, November 30<span>17 days left</span></dd></div>
            <div><dt>Your answers cover</dt><dd>June 1 to November 30, 2026</dd></div>
            <div><dt>Still to do</dt><dd>4 surveys and reports<span>About 1 hour in all</span></dd></div>
          </dl>
        </div>
        <div class="rp-prog">
          <div class="rp-ringwrap" role="img" aria-label="2 of 6 done: 1 submitted, 1 opted out, 4 still to do.">{ring}<p><b class="num">2</b><span>of 6 done</span></p></div>
          <ul class="rp-key"><li><i class="k-ok"></i>1 submitted</li><li><i class="k-opt"></i>1 opted out</li><li><i class="k-todo"></i>4 to do</li></ul>
        </div>
      </div>
      <a class="rp-next" href="#form-preview">
        <span class="rp-next-k">Pick up where you left off</span>
        <span class="rp-next-n">Pilot Project Semiannual Progress Report</span>
        <span class="rp-next-t">In progress. A 1–2 page upload, plus about 5 minutes.</span>
        <span class="btn pri">Continue<svg viewBox="0 0 20 20" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 10h11M11 5.5 15.5 10 11 14.5"/></svg></span>
      </a>
    </div>
  </section>

  <div class="rp-body">
    <div class="wrap">
      <div class="rp-main">
        <section class="rp-sec" aria-labelledby="todo-h">
          <div class="rp-sh"><h2 id="todo-h">To do</h2><p>4 surveys and reports and 1 product review, grouped by what they are about.</p></div>
          {groups}
          <div class="rp-g"><div class="rp-gh"><h3 id="prod-h">Publications, talks, and grants</h3><p>Keep your products up to date. These are the same records your mentor sees on your profile.</p></div>
          <ul class="rp-list">{row('Review your publications, talks, and grants','3 products to review and 1 question to answer','todo','About 10 minutes',b('Start')+q('See all products','mentee-profile.html'),'<p class="rp-x">Your journal article under review and your NIH R21 have new status questions.</p>')}</ul></div>
        </section>

        <section class="rp-sec" aria-labelledby="done-h">
          <div class="rp-sh"><h2 id="done-h">Finished</h2><p>2 this session.</p></div>
          <ul class="rp-list rp-done">{done}</ul>
        </section>

        <section class="rp-sec" aria-labelledby="yr-h">
          <div class="rp-sh"><h2 id="yr-h">Your year</h2><p>Every reporting session in Grant Year 10. A session that hasn’t opened shows what your current roles call for, so it can change if your roles change.</p></div>
          <ol class="rp-yl">{yl}</ol>
          <p class="rp-more"><a class="t3" href="#history">See everything you’ve submitted in past years</a></p>
        </section>
      </div>

      <aside class="rp-side" aria-label="Help with reporting">
        <div class="rp-card">
          <h2>Helpful documents</h2>
          <ul class="rp-docs"><li><a href="#">Progress report template</a><span>Word document</span></li><li><a href="#">How to write your progress summary</a><span>Two-page guide</span></li><li><a href="#">Acknowledging CNAP in your work</a><span>The grant citation, word for word</span></li></ul>
        </div>
        <div class="rp-card">
          <h2>How reporting works</h2>
          <ul class="rp-how"><li>Your answers save as you go. Leave and come back anytime before the due date.</li><li>Preview shows every question before you start.</li><li>If a survey doesn’t apply to you, opt out. That answer is useful too.</li></ul>
          <p class="rp-ask">Questions? <a href="mailto:cnap@ksu.edu">cnap@ksu.edu</a></p>
        </div>
      </aside>
    </div>
  </div>
</main>

<footer class="foot"><div class="wrap"><span>Cognitive and Neurobiological Approaches to Plasticity Center, Kansas State University</span><span>Prototype. The surveys and their names are real. The person, dates, and progress are fictional. In the Member Hub, this page lists your own assignments.</span></div></footer>
<script src="guide.js"></script>
<script src="hubchrome.js" defer></script>
</body>
</html>
'''
open(V+'reporting.html','w').write(html)
print('ok')
