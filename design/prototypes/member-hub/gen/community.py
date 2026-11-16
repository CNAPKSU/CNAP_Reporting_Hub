import re
import sys
sys.path.insert(0,'/tmp/claude-0/hubproto/gen')
from mail import mt
V='/tmp/claude-0/hubproto/v4/'
core=open(V+'core-ni.html').read()
hdr=core[core.index('<a class="skip"'):core.index('<main id="main">')]
hdr=hdr.replace('<a href="index.html#cores-h" aria-current="page">Resources</a>','<a href="index.html#cores-h">Resources</a>')
hdr=hdr.replace('<a href="community.html">Community</a>','<a href="community.html" aria-current="page">Community</a>')
hdr=hdr.replace('<a href="community.html">Community</a>','<a href="community.html" aria-current="page">Community</a>')

# Fictional members (prototype). Staff names are the three MW asked to include.
M=[
 # key, initials, name, role, group, interests, tint, new
 ('kb','KB','Kira Bauer','Graduate student, Psychological Sciences','students',['Attention','Eye tracking','EEG'],'t',True),
 ('na','NA','Nadia Ahmed','Graduate student, Kinesiology','students',['Motor learning','EEG'],'a',True),
 ('om','OM','Omar Mendes','Graduate student, Biology','students',['Sleep','Rodent behavior'],'p',True),
 ('jl','JL','Dr. Jordan Lee','Pilot project leader','investigators',['Sleep','EEG','Memory'],'t',False),
 ('pr','PR','Dr. Priya Raman','Research project leader','investigators',['Sleep','Memory','Aging'],'p',False),
 ('lp','LP','Dr. Lena Park','Pilot project leader','investigators',['Motor learning','TMS'],'a',False),
 ('rg','RG','Dr. Rosa García','Research project leader','investigators',['Imaging','High-performance computing'],'t',False),
 ('hc','HC','Dr. Hannah Cole','Investigator','investigators',['Statistics','Bayesian models'],'p',False),
 ('ev','EV','Dr. Elena Voss','Your mentor','mentors',['Memory','Plasticity','Sleep','Grant writing'],'p',False),
 ('sr','SR','Dr. Samuel Reyes','Mentor','mentors',['Fear learning','Rodent behavior','Electrophysiology'],'a',False),
 ('ms','MS','Dr. Maya Singh','Cognitive Neuroscience Core','core',['Working memory','Aging','EEG','Eye tracking'],'t',False),
 ('wz','WZ','Dr. Wei Zhang','Neuroinformatics Core','core',['Data pipelines','Imaging','High-performance computing','Statistics'],'p',False),
 ('tb','TB','Tom Brandt','Behavioral Neuroscience Core','core',['Electrophysiology','Rodent behavior'],'a',False),
 ('do','DO','Dr. David Osei','Pilot project alumnus','alumni',['Aging','Cognition','Grant writing'],'t',False),
]
BY={m[0]:m for m in M}
G=[('all','Everyone'),('investigators','Project leaders'),('mentors','Mentors'),('core','Core staff'),('students','Students'),('alumni','Alumni')]
def av(k,size=''):
    m=BY[k];return f'<span class="cm-av av-{m[6]}{size}" aria-hidden="true">{m[1]}</span>'
def intro(name):
    return mt('cnap@ksu.edu',f'Introduction to {name}','\n'.join(['Name:','','I would like to meet '+name+' because:','','Times that work for me:','']),cc=None)

# 1. Your first month: six conversations
FIRST=[
 ('Your onboarding meeting','The CNAP team schedules this meeting for you, your mentor, and the Center Director. Together you go over your project, your milestones, and how your award year runs.','mentee.html','Read the mentee guide to prepare',None),
 ('Your mentor, Dr. Elena Voss','Set your regular meetings and agree on how often you will meet. Please bring your aims page and your timeline.','mentee.html#s2','About your mentoring agreement',None),
 ('Heather Bailey, Director','After your onboarding meeting, reach out to the Director any time for introductions to people and resources across the Center.',mt('hbailey@ksu.edu','Introduction from a new project leader','\n'.join(['Name:','Department:','Project title:','','Times that work for me:',''])),'Email Heather','hbailey@ksu.edu'),
 ('Morgan Wills, Assistant Director for Grants and Contracts','Plan your path to the R01 milestone, from your first submission to resubmission.',mt('mkwills@ksu.edu','Proposal planning meeting','\n'.join(['Name:','Department:','Project title:','','Funding I am considering:','','Times that work for me:',''])),'Book a time','mkwills@ksu.edu'),
 ('Roxana Ortiz, Grant Specialist and Accountant','Set up your budget, purchasing, and travel reimbursements before your first expense.',mt('roxana@ksu.edu','Budget and purchasing setup','\n'.join(['Name:','Department:','Project title:','','Questions about my budget or purchasing:',''])),'Email Roxana','roxana@ksu.edu'),
 ('The research cores you will use','Meet with the staff of each core you will use before you book time: a tour of the Behavioral Neuroscience Core, or a consultation with the Cognitive Neuroscience or Neuroinformatics Core. The core directors walk you through the equipment, the training you need, and how to schedule.','index.html#cores-h','See the research cores',None),
]
# who/icon and when for each first-month conversation
FWHO=[('grp','Week 1'),('ev','Week 1'),('HB','Week 2'),('MW','Week 2'),('RO','Before your first expense'),('core','Before you book core time')]
ICON={'grp':'<svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="7" cy="7" r="2.6"/><circle cx="13.5" cy="7.5" r="2.2"/><path d="M2.5 16c.7-3 2.4-4.3 4.5-4.3s3.8 1.3 4.5 4.3M12.5 11.7c2 0 3.5 1.2 4 3.8"/></svg>',
      'core':'<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M7.5 2.5v5L3.5 15a1.6 1.6 0 001.4 2.5h10.2a1.6 1.6 0 001.4-2.5l-4-7.5v-5"/><path d="M6.5 2.5h7M5.5 12.5h9"/></svg>'}
TONE={'HB':'p','MW':'t','RO':'a'}
def _fwho(k):
    if k in ICON: return f'<span class="ff-ic" aria-hidden="true">{ICON[k]}</span>'
    if k in BY: return av(k,' lg')
    return f'<span class="cm-av av-{TONE[k]} lg" aria-hidden="true">{k}</span>'
_cards=[f'''<li class="ff" data-k="ff{i}"><div class="ff-hd"><span class="ff-who">{_fwho(FWHO[i-1][0])}<span class="ff-n" aria-label="Step {i}">{i}</span></span>
  <div class="ff-tt"><p class="cm-ft">{t}</p>{'' if FWHO[i-1][1].startswith('Week') else '<span class="ff-when">'+FWHO[i-1][1]+'</span>'}</div></div>
  <p class="cm-fd">{d}</p>
  <div class="ff-ft"><p class="cm-fa"><a href="{h}">{l}</a>{f'<a class="cm-em" href="mailto:{e}">{e}</a>' if e else ''}</p>
  <button type="button" class="ff-done" aria-pressed="false"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3.5 8.5l3 3 6-7"/></svg><span>Mark as done</span></button></div></li>''' for i,(t,d,h,l,e) in enumerate(FIRST,1)]
FGRP=[('Week 1','Meet the people closest to your project.',[0,1]),('Week 2','Meet the CNAP office.',[2,3]),('Before you start','Set up your budget and core time before your first expense or booking.',[4,5])]
first=''.join(f'<section class="ff-wk" aria-label="{g}"><div class="ff-wkh"><p class="ff-wkt">{g}</p><p class="ff-wks">{sub}</p></div><ol class="ff-grid">{"".join(_cards[j] for j in ix)}</ol></section>' for g,sub,ix in FGRP)

# 2. Members who share your interests
MATCH=[('jl','You both record sleep EEG, and Jordan is looking for a collaborator.'),('pr','Priya studies memory consolidation during sleep and speaks at NeuroSync on November 18.'),('ms','Maya studies working memory in older adults in the core you use.'),('om','Omar joined this month and studies sleep in rodent models.')]
match=''.join(f'''<li class="cm-mc">{av(k,' lg')}<p class="cm-mn"><a class="mb-link" href="member-{k}.html">{BY[k][2]}</a></p><p class="cm-mr">{BY[k][3]}</p><p class="cm-why">{w}</p><p class="cm-chips">{''.join(f'<span>{x}</span>' for x in BY[k][5])}</p><div class="cm-acts"><button type="button" class="btn sm pri" data-direct="{BY[k][2]}">Email {BY[k][2].replace('Dr. ','').split()[0]}</button><span class="cm-or">or</span><a class="btn sm" href="{intro(BY[k][2])}" title="Starts an email asking the CNAP team to introduce you.">Ask for an introduction</a></div></li>''' for k,w in MATCH)

# 3. Who knows what
SK=['EEG','Sleep','Memory','Eye tracking','Rodent behavior','Electrophysiology','TMS','Imaging','High-performance computing','Statistics','Grant writing','Aging']
def who(s): return [m[0] for m in M if s in m[5]]
skills=''.join(f'''<li><button type="button" class="cm-sk" data-skill="{s}"><span class="cm-skn">{s}</span><span class="cm-stack">{''.join(av(k,' sm') for k in who(s)[:4])}</span><span class="cm-skc">{len(who(s))} member{'s' if len(who(s))!=1 else ''}</span></button></li>''' for s in SK)

# 4. Directory
filt=''.join(f'<button type="button" aria-pressed="{"true" if k=="all" else "false"}" data-g="{k}">{l}</button>' for k,l in G)
dirl=''.join(f'''<li class="cm-dr" data-g="{m[4]}" data-new="{'1' if m[7] else '0'}" data-s="{'|'.join(m[5])}" data-q="{(m[2]+' '+m[3]+' '+' '.join(m[5])).lower()}">{av(m[0])}<div class="cm-dm"><p class="cm-dn"><a class="mb-link" href="member-{m[0]}.html">{m[2]}</a>{' <span class="cm-new">New</span>' if m[7] else ''}</p><p class="cm-drl">{m[3]}</p></div><p class="cm-chips">{''.join(f'<span>{x}</span>' for x in m[5])}</p><a class="t3" href="{intro(m[2])}">Ask for an introduction</a></li>''' for m in M)

# 5. Ask the community
T=[('jl','Looking for an EEG collaborator','4 replies','Active today',True,'You record sleep EEG in your pilot project.',False),
   ('rg','Who has used the Beocat cluster for imaging?','No replies yet','Started Wednesday',True,'Your team moved the team’s analysis pipeline onto Beocat. Be the first to answer.',True),
   ('lp','Recruiting older adults: what has worked?','3 replies','Active yesterday',True,'Your study recruits adults over 65.',False),
   ('hc','Office hours for mixed-effects models in R','6 replies','Active Monday',False,'',False),
   ('sr','A journal club on fear extinction, starting in December','5 replies','Active last week',False,'',False),
   ('kb','Calibrating the eye tracker for participants who wear glasses','No replies yet','Started today',False,'',True)]
thr=''.join(f'''<li class="cm-th" data-m="{'1' if mt_ else '0'}" data-u="{'1' if un else '0'}">{av(k)}<div class="cm-tm">{f'<a class="cm-tt" href="thread.html">{t}</a>' if k=='jl' else f'<a class="cm-tt" href="#" data-proto title="Only one thread page is built in the prototype: Looking for an EEG collaborator.">{t}</a>'}<p class="cm-tx">{BY[k][2]} · {r} · {a}</p>{f'<p class="cm-why">{w}</p>' if w else ''}</div>{'<span class="st st-on">Unanswered</span>' if un else ''}</li>''' for k,t,r,a,mt_,w,un in T)

# 6. Recent achievements
A=[('ms','Publication','Attention and working memory in older adults: a two-year follow-up','Dr. Maya Singh and colleagues, with the Cognitive Neuroscience Core. Cites CNAP.','November 10'),
   ('do','Grant award','A first R01 for a former CNAP pilot project leader','Dr. David Osei, National Institute on Aging.','November 6'),
   ('wz','Invited talk','Neuroinformatics Core pipeline presented at a national meeting','Dr. Wei Zhang, Neuroinformatics Core.','October 30'),
   ('lp','Poster award','Best poster in motor learning at a regional neuroscience meeting','Dr. Lena Park, pilot project leader.','October 21')]
ach=''.join(f'''<li class="cm-ac">{av(k)}<div><p class="cm-ak">{kind}<span>{d}</span></p><p class="cm-at">{t}</p><p class="cm-ad">{x}</p><a class="t3" href="{mt('cnap@ksu.edu','Congratulations to '+BY[k][2],'Please pass on my congratulations to '+BY[k][2]+'.\n\n',cc=None)}">Send congratulations</a></div></li>''' for k,kind,t,x,d in A)

# 7. Ways to connect
W=[('Every Wednesday, 2:30 to 3:30 p.m.','NeuroSync Weekly Speaker Series','Talks in Leadership Room 127, with questions and time to talk after. CNAP members are expected to attend.','events.html','See the speakers'),
   ('Weekdays, staffed drop-in','CONNECT Lab','Help with experiment programming and data pipelines from the Cognitive Neuroscience and Neuroinformatics Cores.','core-cn.html#cn-cx','About the CONNECT Lab'),
   ('Thursday, December 10, 3:30 to 5:00 p.m.','Fall social for members and students','Every member, student, and core user is welcome.','events.html','See all events'),
   ('Throughout the year','Scientific Exchange Network','Collaborations, more core access, and workshops with partner institutions.','mentee.html','How Community works for your project'),
   ('May 25 and 26, 2027','The Site Visit','Two days of presentations, posters, and conversation with the External Advisory Committee.','events.html','About the Site Visit')]
ways=''.join(f'''<li><p class="cm-wk">{k}</p><p class="cm-wt">{t}</p><p class="cm-wd">{d}</p><a class="t3" href="{h}">{l}</a></li>''' for k,t,d,h,l in W)

# 8. Announcements
# 8. Announcements: the listserv emails, as an inbox (MW 2026-11-15: "unimpressive design")
# date, sender key, subject, preview, body paragraphs, attachment (name, size) or None, action note or None
SND={'ac':('AC','CNAP Administrative Core','a'),'hb':('HB','Heather Bailey, Director','p'),'mw':('MW','Morgan Wills, Grants and Contracts','t')}
AN=[('November 12','ac','Reminder: Year 11 pilot full proposals are due November 20',
     'Please send all proposal materials as one PDF to cnap@ksu.edu by 5:00 p.m. Central.',
     ['Please send all proposal materials as one compiled PDF to cnap@ksu.edu by 5:00 p.m. Central on Friday, November 20.','Arrange the contents in the order listed on pages 3 and 4 of the RFA. If the file is too large to attach, please share it with a cloud link such as OneDrive.'],
     ('Year 11 pilot RFA.pdf','412 KB'),'Due Friday, November 20'),
    ('November 9','hb','Welcome to our three newest graduate students',
     'Please join us in welcoming the three students to the Cognitive Neuroscience Core this month.',
     ['Please join us in welcoming Kira Bauer, Nadia Ahmed, and Omar Mendes, who joined the Cognitive Neuroscience Core this month.','You can find their interests on the Community page. If your work overlaps, please say hello.'],None,None),
    ('November 4','ac','Updated travel and reimbursement guidelines',
     'The attached guide replaces last year’s version and takes effect December 1.',
     ['The attached guide replaces last year’s version and takes effect December 1.','The main change: please sign the front of each receipt before you send it to Roxana Ortiz.'],
     ('Travel and reimbursement guide 2026.pdf','236 KB'),None),
    ('October 28','mw','Pre-submission review: request by November 6',
     'If you would like a review of a draft before a spring deadline, please send it by November 6.',
     ['If you would like a review of a draft before a spring deadline, please send it to Morgan Wills by November 6.','Reviews take about two weeks. Please include the funding opportunity and your deadline.'],None,None),
    ('October 20','ac','NeuroSync schedule for the rest of the fall',
     'Talks continue each Wednesday at 2:30 p.m. in Leadership Room 127, with a break on November 25.',
     ['Talks continue each Wednesday at 2:30 p.m. in Leadership Room 127. There is no talk on November 25.','The full schedule is on the NeuroSync page.'],('NeuroSync fall schedule.pdf','118 KB'),None),
    ('October 14','hb','Year 10 progress report: thank you',
     'Thank you to every project leader and core director for your sections of the progress report.',
     ['Thank you to every project leader and core director for your sections of the Year 10 progress report. It went to NIGMS on schedule.'],None,None),
    ('October 6','ac','Fall reporting opens in the Member Hub',
     'Fall surveys and reports are open now and close Monday, November 30.',
     ['Fall surveys and reports are open in the Member Hub and close Monday, November 30.','Most people need about an hour and a half in all. You can save and come back.'],None,None),
    ('September 29','mw','Letters of intent: Year 11 pilot projects',
     'Letters of intent for Year 11 pilot projects are due October 16 at 5:00 p.m. Central.',
     ['Letters of intent for Year 11 pilot projects are due October 16 at 5:00 p.m. Central.','Please include the project title, an abstract of up to 500 words, your proposed mentors, and three to five recommended reviewers.'],('Year 11 pilot RFA.pdf','412 KB'),None)]
def _ann(i,x):
    d,k,t,pv,body,att,act=x
    ini,who,tone=SND[k]
    attc=(f'<div class="an-file"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 2.5h7l3.5 3.5v11.5H5z"/><path d="M12 2.5V6h3.5"/></svg><span><b>{att[0]}</b><small>PDF, {att[1]}</small></span>'
          f'<a class="t3" href="#" data-proto title="In the Member Hub, this opens the attachment. Not part of the prototype.">Open</a></div>') if att else ''
    clip='<svg class="an-clip" viewBox="0 0 16 16" aria-label="Has an attachment" role="img"><path d="M10.5 4.5l-5 5a1.8 1.8 0 002.5 2.5l5.5-5.5a3 3 0 00-4.2-4.2L3.8 7.8"/></svg>' if att else ''
    tag=f'<span class="an-act">{act}</span>' if act else ''
    reply=mt('cnap@ksu.edu','Re: '+t,'')
    return (f'<li class="an{" an-due" if act else ""}" data-from="{k}" data-att="{"1" if att else "0"}"{" hidden data-older" if i>=4 else ""}><details{" open" if i==0 else ""}><summary>'
            f'<span class="cm-av av-{tone}" aria-hidden="true">{ini}</span>'
            f'<span class="an-m"><span class="an-top"><span class="an-from">{who}</span><span class="an-date">{d}</span></span>'
            f'<span class="an-subj">{t}{clip}</span><span class="an-pv">{pv}</span>{tag}</span></summary>'
            f'<div class="an-body">{"".join(f"<p>{p}</p>" for p in body)}{attc}<p class="an-foot"><a class="t3" href="{reply}">Reply to the CNAP team</a></p></div></details></li>')
ann=''.join(_ann(i,x) for i,x in enumerate(AN))
N_OLD=len(AN)-4


import math,random
random.seed(7)
W,H,CX,CY=520,380,260,190
GROUPS=[('pl','Project leaders',14),('mn','Mentors',11),('co','Core staff',9),('st','Students',17),('al','Alumni',6)]
seq=[g for g,_,n in GROUPS for _ in range(n)];random.shuffle(seq);tot=len(seq)
outer=[]
for idx,g in enumerate(seq):
    a=2*math.pi*(idx/tot)+random.uniform(-.05,.05);r=random.uniform(150,178)
    outer.append((g,CX+r*math.cos(a),CY+r*math.sin(a)*0.92))
MATCHN=[('jl','Jordan Lee','Sleep EEG',-2.35),('pr','Priya Raman','Sleep and memory',-0.75),('ms','Maya Singh','Aging',0.45),('om','Omar Mendes','Sleep',2.2)]
mpos=[(k,nm,why,CX+120*math.cos(a),CY+120*math.sin(a)*0.86) for k,nm,why,a in MATCHN]
lines=[]
for n,(g,x,y) in enumerate(outer):
    m=outer[(n+1)%len(outer)]
    lines.append(f'<path class="cm-l0" d="M{x:.1f} {y:.1f}L{m[1]:.1f} {m[2]:.1f}"/>')
    if n%5==0:
        k,nm,why,mx,my=mpos[min(3,int(4*n/len(outer)))]
        lines.append(f'<path class="cm-l1" d="M{x:.1f} {y:.1f}L{mx:.1f} {my:.1f}"/>')
for k,nm,why,x,y in mpos:
    lines.append(f'<path class="cm-l2" d="M{CX} {CY}L{x:.1f} {y:.1f}"/>')
dots=''.join(f'<circle class="cm-g-{g}" cx="{x:.1f}" cy="{y:.1f}" r="{4.5 if g!="st" else 3.5}"/>' for g,x,y in outer)
mnodes=''.join(f'<g class="cm-mn2" style="--d:{.25*i+.6}s"><circle cx="{x:.1f}" cy="{y:.1f}" r="21"/><text class="cm-ini" x="{x:.1f}" y="{y+5:.1f}">{BY[k][1]}</text><text class="cm-nm" x="{x:.1f}" y="{y+37:.1f}">{nm}</text><text class="cm-wy" x="{x:.1f}" y="{y+51:.1f}">{why}</text></g>' for i,(k,nm,why,x,y) in enumerate(mpos))
legend=''.join(f'<li><i class="cm-k-{g}"></i>{lbl}</li>' for g,lbl,_ in GROUPS)
NET=f'''<figure class="cm-net"><svg viewBox="0 0 {W} {H}" role="img" aria-label="You at the center of the CNAP network of 61 members, with four members who share your interests nearest to you"><g class="cm-ls">{''.join(lines)}</g><g class="cm-outer">{dots}</g>{mnodes}<g class="cm-me2"><circle class="cm-halo" cx="{CX}" cy="{CY}" r="44"/><circle cx="{CX}" cy="{CY}" r="32"/><text x="{CX}" y="{CY+6}">AO</text></g></svg>
          <figcaption><span class="cm-cap">You, the four members who share your interests,<br>and 57 more across the Center.</span><ul class="cm-legend">{legend}</ul></figcaption></figure>'''

# CNAP alumni (fictional)
AL=[('DO','t','Dr. David Osei','Pilot project leader, Grant Years 7 and 8','Associate Professor, Psychological Sciences, Kansas State University','First R01, National Institute on Aging, 2026',True),
    ('ID','p','Dr. Inês Duarte','Research project leader, Grant Years 1 to 4','Professor, Psychological Sciences, Kansas State University','R01, National Institute of Neurological Disorders and Stroke, 2020',True),
    ('LM','a','Dr. Leah Morgan','Research project leader, Grant Years 3 to 5','Associate Professor, Neuroscience, University of Nebraska','R01, National Institute of Mental Health, 2022',True),
    ('MH','t','Dr. Marcus Hale','Pilot project leader, Grant Year 8','Assistant Professor, Kinesiology, Kansas State University','R21, National Institute on Drug Abuse, 2025',False),
    ('SC','p','Dr. Sun-Mi Cho','Pilot project leader, Grant Years 5 and 6','Assistant Professor, Psychology, University of Colorado','K01, National Institute on Aging, 2023',True),
    ('AW','a','Dr. Aaron Whitfield','Pilot project leader, Grant Year 6','Research Scientist, a neurotechnology company','Moved into industry research in 2024',False)]
def _split(x):
    a,_,b=x.partition(', ')
    return (a,b) if b else (x,'')
def _path(c,f):
    r,yrs=_split(c); aw,ag=_split(f)
    return (f'<ol class="cm-path" aria-label="Career path">'
            f'<li class="cm-st"><span class="al-k">At CNAP</span><b>{r}</b>{f"<span>{yrs}</span>" if yrs else ""}</li>'
            f'<li class="cm-st cm-st2"><span class="al-k">After CNAP</span><b>{aw}</b>{f"<span>{ag}</span>" if ag else ""}</li></ol>')
def _last_year(c):
    nums=[int(x) for x in re.findall(r'\d+',c)]
    return 2016+max(nums) if nums else None
def _gap(c,f):
    y=re.findall(r'(20\d\d)',f); ly=_last_year(c)
    if not y or not ly: return ''
    g=int(y[-1])-ly
    return 'The same year' if g<=0 else ('1 year later' if g==1 else f'{g} years later')
NOW={'DO':('At K-State','Psychological Sciences'),'ID':('At K-State','Psychological Sciences'),'LM':('University of Nebraska','Neuroscience'),
     'MH':('At K-State','Kinesiology'),'SC':('University of Colorado','Psychology'),'AW':('In industry','Neurotechnology')}
def _alum(i,t,n,c,w,f,ok):
    r,yrs=_split(c); aw,ag=_split(f)
    first=n.replace('Dr. ','').split()[0]
    foot=(f'<div class="al-foot"><p class="al-ok">Happy to talk with new project leaders</p><div class="cm-acts"><button type="button" class="btn sm al-mail" data-direct="{n}">Email {first}</button>'
          f'<span class="cm-or">or</span><a class="btn sm" href="{intro(n)}" title="Starts an email asking the CNAP team to introduce you.">Ask for an introduction</a></div></div>') if ok else ''
    return (f'<li class="al"><div class="al-head"><span class="cm-av av-{t} lg" aria-hidden="true">{i}</span><div><p class="al-n"><a class="mb-link" href="member-{i.lower()}.html">{n}</a></p></div></div>'
            f'<ol class="al-path" aria-label="Career path"><li class="al-from"><span class="al-k">At CNAP</span><b>{r}</b>{f"<span>{yrs}</span>" if yrs else ""}</li>'
            '<li class="al-gap" aria-hidden="true"></li>'
            f'<li class="al-to"><span class="al-k">Now</span><b>{NOW[i][0]}</b><span>{NOW[i][1]}</span></li></ol>{foot}</li>')
alumni=''.join(_alum(*x) for x in AL)

SECS=[('cm-ach','Recent achievements'),('cm-ask','Ask the community'),('cm-first','Your first month'),('cm-match','Members who share your interests'),('cm-know','Member interests and expertise'),('cm-dir','Member directory'),('cm-alum','CNAP alumni'),('cm-ways','Ways to connect'),('cm-ann','Announcements'),('cm-priv','Your profile and privacy')]
spine=''.join(f'<li><a href="#{i}"><span class="n"><b>{n}</b></span><span>{t}</span></a></li>' for n,(i,t) in enumerate(SECS,1))
SHARE=mt('cnap@ksu.edu','An achievement to share','\n'.join(['Name:','','The achievement (a paper, grant, talk, award, or milestone):','','A link, if there is one:','']),cc=None)

page=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Community · CNAP Member Hub</title>
<link rel="stylesheet" href="guide.css">
</head>
<body data-guide="community" class="core-page cm-page">
{hdr}<main id="main">
  <section class="co-open cm-open" aria-labelledby="t">
    <div class="wrap">
      <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">Community</span></nav>
      <div class="cm-hero">
        <div class="cm-hd">
          <p class="for">The people of CNAP</p>
          <h1 id="t">Community</h1>
          <p class="lead">Who works on what, who to ask, and where to meet. Start here to find a collaborator, a second opinion on your methods, or someone who has navigated a similar challenge.</p>
          <div class="co-act"><button type="button" class="btn pri" data-compose>Start a conversation thread</button><button type="button" class="btn" data-share>Share an achievement</button></div>
        </div>
        {NET}
      </div>
      <ul class="co-facts cm-facts" aria-label="At a glance"><li><a href="#cm-dir"><b class="num">61</b><span>Members</span></a></li><li><a href="#cm-dir" data-newonly><b class="num">3</b><span>Joined this month</span></a></li><li><a href="#cm-ask"><b class="num">14</b><span>Open conversation threads</span></a></li><li><a href="#cm-ach"><b class="num">2</b><span>Grants awarded this fall</span></a></li><li><a href="#cm-alum"><b class="num">6</b><span>CNAP alumni</span></a></li></ul>
    </div>
  </section>

  <div class="guide">
    <div class="wrap">
      <nav class="spine" aria-label="Sections on this page">
        <p class="spine-h">On this page</p><div class="spine-track" aria-hidden="true"><span class="spine-fill"></span></div>
        <ol>{spine}</ol>
      </nav>
      <div class="steps">
        <section class="step cs" id="cm-ach" aria-labelledby="cm-ach-h">
          <h2 id="cm-ach-h">Recent achievements</h2>
          <div class="cs-b"><ul class="cm-acs">{ach}</ul><p class="meta">Have news of your own? <button type="button" class="t3" data-share>Share an achievement</button> and the CNAP team will post the achievement here and in the Center’s reports.</p></div>
        </section>
        <section class="step cs" id="cm-ask" aria-labelledby="cm-ask-h">
          <h2 id="cm-ask-h">Ask the community</h2>
          <div class="cs-b"><p>Questions about methods, equipment, recruiting, and funding, answered by the members who have the experience. Threads are visible only to CNAP members.</p>
            <div class="cm-thbar"><div class="pf-filt cm-tf" role="group" aria-label="Show"><button type="button" aria-pressed="true" data-t="m">Matched to you</button><button type="button" aria-pressed="false" data-t="u">Unanswered</button><button type="button" aria-pressed="false" data-t="a">All threads</button></div><button type="button" class="btn sm" data-compose>Start a conversation thread</button></div>
            <ul class="cm-ths">{thr}</ul>
            <p class="meta"><a class="t3" href="threads.html">See all 14 threads</a></p>
          </div>
        </section>
        <section class="step cs" id="cm-first" aria-labelledby="cm-first-h">
          <h2 id="cm-first-h">Your first month</h2>
          <div class="cs-b"><div class="ff-head"><p>Six conversations that make the rest of your award easier, best held in your first month.</p>
            <div class="ff-prog" role="status"><span class="ff-bar" aria-hidden="true"><span></span></span><span><b data-ffn>0</b> of 6 done</span></div></div>
            <div class="ff-weeks">{first}</div></div>
        </section>
        <section class="step cs" id="cm-match" aria-labelledby="cm-match-h">
          <h2 id="cm-match-h">Members who share your interests</h2>
          <div class="cs-b"><p>Matched on the interests in your profile: sleep, memory, aging, and EEG. Email these members directly, or ask the CNAP team to introduce you if you would rather not write out of the blue.</p><ul class="cm-mcs">{match}</ul></div>
        </section>
        <section class="step cs" id="cm-know" aria-labelledby="cm-know-h">
          <h2 id="cm-know-h">Member interests and expertise</h2>
          <div class="cs-b"><p>Methods and topics members have listed on member profiles. Please select a topic to see who knows the topic in the directory.</p><ul class="cm-sks">{skills}</ul></div>
        </section>
        <section class="step cs" id="cm-dir" aria-labelledby="cm-dir-h">
          <h2 id="cm-dir-h">Member directory</h2>
          <div class="cs-b">
            <div class="cm-tools"><label class="cm-search"><span class="sr">Search members</span><svg viewBox="0 0 20 20" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="9" cy="9" r="6"/><path d="m14 14 4 4"/></svg><input type="search" placeholder="Search by name, role, or method" data-dirq></label><p class="cm-count" role="status"><span data-dirn>{len(M)}</span> members shown</p></div>
            <div class="pf-filt cm-filt" role="group" aria-label="Show">{filt}</div>
            <p class="cm-skill-on" hidden><span data-sm>Showing members who know <b data-skn></b>.</span> <button type="button" class="t3 cm-clear">Show everyone</button></p>
            <ul class="cm-dir">{dirl}</ul>
            <p class="cm-none" hidden>No members match. Try a different word, or <button type="button" class="t3 cm-clear">show everyone</button>.</p>
          </div>
        </section>
        <section class="step cs" id="cm-alum" aria-labelledby="cm-alum-h">
          <h2 id="cm-alum-h">CNAP alumni</h2>
          <div class="cs-b"><p>Former project leaders, and where each one’s research has led. Each alumnus chooses what appears here, and can change or remove the entry at any time.</p><ul class="al-list">{alumni}</ul></div>
        </section>
        <section class="step cs" id="cm-ways" aria-labelledby="cm-ways-h">
          <h2 id="cm-ways-h">Ways to connect</h2>
          <div class="cs-b"><ul class="cm-ways">{ways}</ul></div>
        </section>
        <section class="step cs" id="cm-ann" aria-labelledby="cm-ann-h">
          <h2 id="cm-ann-h">Announcements</h2>
          <div class="cs-b"><p>Every email from the CNAP listserv, kept here so you can find any email again. Select an email to read the full message.</p>
            <div class="an-bar"><div class="pf-filt an-f" role="group" aria-label="Show"><button type="button" aria-pressed="true" data-af="all">All</button><button type="button" aria-pressed="false" data-af="ac">Administrative Core</button><button type="button" aria-pressed="false" data-af="hb">Director</button><button type="button" aria-pressed="false" data-af="mw">Grants and Contracts</button><button type="button" aria-pressed="false" data-af="att">With attachments</button></div></div>
            <ul class="an-list">{ann}</ul>
            <p class="an-more"><button type="button" class="btn sm" data-older>Show {N_OLD} older emails</button></p></div>
        </section>
        <section class="step cs" id="cm-priv" aria-labelledby="cm-priv-h">
          <h2 id="cm-priv-h">Your profile and privacy</h2>
          <div class="cs-b"><div class="pz">
            <div class="pz-intro">
              <p class="pz-lead">Other members see your name, role, interests, and the work you choose to show. Your reporting, your survey answers, and the funding picked for you are never shown to other members.</p>
              <p class="pz-tl" id="pz-tl">See your profile as</p><div class="pz-tog" role="group" aria-labelledby="pz-tl"><button type="button" data-pz="member" aria-pressed="true"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M1.5 8s2.4-4.5 6.5-4.5S14.5 8 14.5 8s-2.4 4.5-6.5 4.5S1.5 8 1.5 8z"/><circle cx="8" cy="8" r="2"/></svg>A member</button><button type="button" data-pz="me" aria-pressed="false"><svg viewBox="0 0 16 16" aria-hidden="true"><rect x="3.5" y="7" width="9" height="6.5" rx="1.5"/><path d="M5.5 7V5a2.5 2.5 0 015 0v2"/></svg>You</button></div>
              <p class="pz-say" role="status">This is what other CNAP members see.</p>
              <p class="pz-cta"><a class="btn pri" href="mentee-profile.html">Review your profile</a><span>You choose what to show, and you can change your choices any time.</span></p>
            </div>
            <div class="pz-card" data-view="member">
              <div class="pz-head"><span class="cm-av av-p lg" aria-hidden="true">AO</span><div><p class="pz-n">Dr. Amara Okafor</p><p class="pz-r">Pilot project leader, Psychological Sciences</p></div><span class="pz-badge"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M1.5 8s2.4-4.5 6.5-4.5S14.5 8 14.5 8s-2.4 4.5-6.5 4.5S1.5 8 1.5 8z"/><circle cx="8" cy="8" r="2"/></svg>Visible to members</span></div>
              <p class="cm-chips"><span>Sleep</span><span>Memory</span><span>Aging</span><span>EEG</span></p>
              <div class="pz-row"><span class="pz-l">Work you show</span><span class="pz-v">3 publications and 1 talk</span></div>
              <div class="pz-row"><span class="pz-l">Mentor</span><span class="pz-v">Dr. Elena Voss</span></div>
              <div class="pz-hidden"><span><svg viewBox="0 0 16 16" aria-hidden="true"><rect x="3.5" y="7" width="9" height="6.5" rx="1.5"/><path d="M5.5 7V5a2.5 2.5 0 015 0v2"/></svg></span>4 more things are hidden from other members.</div>
              <div class="pz-privs">
                <div class="pz-row pz-priv"><span class="pz-l"><svg viewBox="0 0 16 16" aria-hidden="true"><rect x="3.5" y="7" width="9" height="6.5" rx="1.5"/><path d="M5.5 7V5a2.5 2.5 0 015 0v2"/></svg>Mentee Survey answers</span><span class="pz-v">Confidential</span><span class="pz-only">Never shown to other members</span></div>
                <div class="pz-row pz-priv"><span class="pz-l"><svg viewBox="0 0 16 16" aria-hidden="true"><rect x="3.5" y="7" width="9" height="6.5" rx="1.5"/><path d="M5.5 7V5a2.5 2.5 0 015 0v2"/></svg>Reporting</span><span class="pz-v">2 of 6 done this fall</span><span class="pz-only">Never shown to other members</span></div>
                <div class="pz-row pz-priv"><span class="pz-l"><svg viewBox="0 0 16 16" aria-hidden="true"><rect x="3.5" y="7" width="9" height="6.5" rx="1.5"/><path d="M5.5 7V5a2.5 2.5 0 015 0v2"/></svg>Funding picked for you</span><span class="pz-v">3 matches</span><span class="pz-only">Never shown to other members</span></div>
                <div class="pz-row pz-priv"><span class="pz-l"><svg viewBox="0 0 16 16" aria-hidden="true"><rect x="3.5" y="7" width="9" height="6.5" rx="1.5"/><path d="M5.5 7V5a2.5 2.5 0 015 0v2"/></svg>Work you keep private</span><span class="pz-v">1 grant</span><span class="pz-only">Never shown to other members</span></div>
              </div>
            </div>
          </div></div>
        </section>
      </div>
      <aside class="co-rail" aria-label="Your community profile"><div class="co-rc cm-me"><p class="co-rk">Your community profile</p><span class="cm-av av-p lg" aria-hidden="true">AO</span><p class="co-pn">Dr. Amara Okafor</p><p class="pp-r">Pilot project leader, Grant Year 10</p><p class="cm-chips"><span>Sleep</span><span>Memory</span><span>Aging</span><span>EEG</span></p><dl class="co-rd"><div><dt>Mentor</dt><dd>Dr. Elena Voss</dd></div><div><dt>Cores you use</dt><dd><a href="core-cn.html">Cognitive Neuroscience</a> and <a href="core-ni.html">Neuroinformatics</a></dd></div></dl><a class="t3" href="mentee-profile.html">Review your profile</a></div></aside>
    </div>
  </div>
</main>

<dialog class="cm-compose" aria-labelledby="cmc-h">
  <form method="dialog" class="cm-form">
    <h2 id="cmc-h">Start a conversation thread</h2>
    <fieldset class="cm-kinds"><legend>What is the thread about?</legend>
      <label><input type="radio" name="kind" value="funding"><span>Experience with a funding opportunity</span></label>
      <label><input type="radio" name="kind" value="expertise"><span>Finding a collaborator or a kind of expertise</span></label>
      <label><input type="radio" name="kind" value="student"><span>Hiring a graduate student</span></label>
      <label><input type="radio" name="kind" value="other" checked><span>Something else</span></label>
    </fieldset>
    <label for="cmc-t">Your question</label><input id="cmc-t" type="text" placeholder="For example: who has run sleep EEG with older adults?">
    <label for="cmc-d">Details <span class="cm-opt">(optional)</span></label><textarea id="cmc-d" rows="4"></textarea>
    <p class="cm-note" role="status" hidden>Prototype only. In the Member Hub, the thread posts for CNAP members, and the members whose interests match are told about the thread.</p>
    <div class="cm-fb"><button type="submit" value="cancel" class="btn">Cancel</button><button type="button" class="btn pri" data-post>Post the thread</button></div>
  </form>
</dialog>
<dialog class="cm-compose cm-share" aria-labelledby="cms-h">
  <form method="dialog" class="cm-form">
    <h2 id="cms-h">Share an achievement</h2>
    <p class="cm-sub">Please choose something you have already recorded in the Member Hub, or describe something new. The CNAP team posts the achievement here and adds the achievement to the Center’s reports.</p>
    <fieldset class="cm-prods"><legend>From your publications, presentations, proposals, and awards</legend><label class="cm-pi"><input type="radio" name="prod" value="0" checked><span><b>Publication</b>Slow oscillations and overnight retention in healthy aging<small>Neurobiology of Learning and Memory · Under review</small></span></label><label class="cm-pi"><input type="radio" name="prod" value="1"><span><b>Presentation</b>Sleep, memory, and the aging brain<small>NeuroSync Weekly Speaker Series · September 2026</small></span></label><label class="cm-pi"><input type="radio" name="prod" value="2"><span><b>Proposal</b>Slow-wave sleep enhancement and memory in older adults<small>NIH R21, National Institute on Aging · Submitted June 16, 2026</small></span></label><label class="cm-pi"><input type="radio" name="prod" value="3"><span><b>Presentation</b>Nap timing restores word-pair retention in older adults with fragmented sleep<small>National sleep research meeting · Abstract submitted</small></span></label><label class="cm-pi"><input type="radio" name="prod" value="4"><span><b>Publication</b>Sleep spindles and next-day recall: a pilot study<small>Journal of Sleep Research · Published March 2025</small></span></label>
      <label class="cm-pi"><input type="radio" name="prod" value="new"><span><b>Something else</b>A new paper, talk, proposal, award, or milestone</span></label>
    </fieldset>
    <div class="cm-newfields" hidden><label for="cms-t">What happened</label><input id="cms-t" type="text" placeholder="For example: my R21 was funded by the National Institute on Aging"><label for="cms-l">A link <span class="cm-opt">(optional)</span></label><input id="cms-l" type="text" inputmode="url"></div>
    <label for="cms-n">A sentence for members <span class="cm-opt">(optional)</span></label><textarea id="cms-n" rows="2" placeholder="What it means for your project, or who helped"></textarea>
    <p class="cm-note" role="status" hidden>Prototype only. In the Member Hub, the CNAP team reviews your achievement, posts the achievement in Community, and adds the achievement to the Center’s reports.</p>
    <div class="cm-fb"><button type="submit" value="cancel" class="btn">Cancel</button><button type="button" class="btn pri" data-sendach>Share the achievement</button></div>
  </form>
</dialog>
<footer class="foot"><div class="wrap"><span>Cognitive and Neurobiological Approaches to Plasticity Center, Kansas State University</span><span>Prototype. The members, threads, and achievements are fictional. The Director, the Assistant Director for Grants and Contracts, and the Grant Specialist are real staff. Posting threads isn’t connected yet.</span></div></footer>
<script src="guide.js"></script>
<script>
(function(){{
  var rows=[].slice.call(document.querySelectorAll('.cm-dr')),q=document.querySelector('[data-dirq]'),n=document.querySelector('[data-dirn]'),none=document.querySelector('.cm-none'),gb=document.querySelectorAll('.cm-filt button'),son=document.querySelector('.cm-skill-on'),skn=document.querySelector('[data-skn]'),g='all',skill='';
  function apply(){{var t=(q.value||'').trim().toLowerCase(),c=0;rows.forEach(function(r){{var ok=(g==='all'||r.dataset.g===g)&&(!t||r.dataset.q.indexOf(t)>-1)&&(!skill||r.dataset.s.split('|').indexOf(skill)>-1);r.hidden=!ok;if(ok)c++;}});n.textContent=c;none.hidden=c>0;son.hidden=!skill;skn.textContent=skill;}}
  q.addEventListener('input',apply);
  var onlyNew=false;var a0=apply;apply=function(){{a0();if(onlyNew){{var c=0;rows.forEach(function(r){{if(r.dataset.new!=='1')r.hidden=true;if(!r.hidden)c++;}});n.textContent=c;son.hidden=false;son.querySelector('[data-sm]').textContent='Showing the three members who joined this month.';}}}};
  document.querySelector('[data-newonly]').addEventListener('click',function(){{onlyNew=true;skill='';q.value='';g='all';apply();}});
  document.querySelectorAll('.cm-clear').forEach(function(b){{b.addEventListener('click',function(){{onlyNew=false;son.querySelector('[data-sm]').innerHTML='Showing members who know <b data-skn></b>.';skn=son.querySelector('[data-skn]');apply();}});}});
  gb.forEach(function(b){{b.addEventListener('click',function(){{g=b.dataset.g;gb.forEach(function(o){{o.setAttribute('aria-pressed',o===b)}});apply();}});}});
  document.querySelectorAll('.cm-sk').forEach(function(b){{b.addEventListener('click',function(){{skill=b.dataset.skill;g='all';gb.forEach(function(o){{o.setAttribute('aria-pressed',o.dataset.g==='all')}});q.value='';apply();document.getElementById('cm-dir').scrollIntoView({{behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'}});}});}});
  document.querySelectorAll('.cm-clear').forEach(function(b){{b.addEventListener('click',function(){{skill='';q.value='';g='all';gb.forEach(function(o){{o.setAttribute('aria-pressed',o.dataset.g==='all')}});apply();}});}});
  (function(){{var items=[].slice.call(document.querySelectorAll('.an')),fb=document.querySelectorAll('.an-f button'),more=document.querySelector('[data-older]'),showOld=false,f='all';
    function ap(){{items.forEach(function(li){{var ok=f==='all'||(f==='att'?li.dataset.att==='1':li.dataset.from===f);li.hidden=!ok||(!showOld&&f==='all'&&li.hasAttribute('data-older'));}});more.hidden=showOld||f!=='all';}}
    fb.forEach(function(b){{b.addEventListener('click',function(){{f=b.dataset.af;fb.forEach(function(o){{o.setAttribute('aria-pressed',o===b)}});ap();}});}});
    more.addEventListener('click',function(){{showOld=true;ap();var first=items.filter(function(l){{return l.hasAttribute('data-older')}})[0];if(first)first.querySelector('summary').focus();}});ap();}})();
  (function(){{var cards=[].slice.call(document.querySelectorAll('.ff')),n=document.querySelector('[data-ffn]'),bar=document.querySelector('.ff-bar span');
    function upd(){{var c=cards.filter(function(x){{return x.classList.contains('is-done')}}).length;n.textContent=c;bar.style.width=(c/cards.length*100)+'%';}}
    cards.forEach(function(card){{var b=card.querySelector('.ff-done'),k=card.dataset.k,on=false;try{{on=localStorage.getItem(k)==='1'}}catch(e){{}}
      function set(v){{card.classList.toggle('is-done',v);b.setAttribute('aria-pressed',v);b.querySelector('span').textContent=v?'Done':'Mark as done';try{{localStorage.setItem(k,v?'1':'0')}}catch(e){{}}upd();}}
      set(on);b.addEventListener('click',function(){{set(!card.classList.contains('is-done'));}});}});}})();
  (function(){{var card=document.querySelector('.pz-card'),bs=document.querySelectorAll('[data-pz]'),say=document.querySelector('.pz-say');
    bs.forEach(function(b){{b.addEventListener('click',function(){{var v=b.dataset.pz;card.dataset.view=v;bs.forEach(function(o){{o.setAttribute('aria-pressed',o===b)}});
      card.querySelector('.pz-badge').lastChild.textContent=v==='me'?'Your view':'Visible to members';say.textContent=v==='me'?'This is your own view. The locked rows never appear to other members.':'This is what other CNAP members see.';}});}});}})();
  document.querySelectorAll('[data-direct]').forEach(function(b){{b.addEventListener('click',function(){{var n=b.dataset.direct;if(window.hubToast)hubToast('<b>In the Member Hub, this starts an email to '+n+'.</b> The members here are fictional, so nothing opens in the prototype.');}});}});
  var th=[].slice.call(document.querySelectorAll('.cm-th')),tb=document.querySelectorAll('.cm-tf button');
  function tf(k){{th.forEach(function(r){{r.hidden=k==='m'?r.dataset.m!=='1':k==='u'?r.dataset.u!=='1':false;}});}}
  tb.forEach(function(b){{b.addEventListener('click',function(){{tb.forEach(function(o){{o.setAttribute('aria-pressed',o===b)}});tf(b.dataset.t);}});}});tf('m');
  var dlg=document.querySelector('.cm-compose');document.querySelectorAll('[data-compose]').forEach(function(b){{b.addEventListener('click',function(){{try{{dlg.showModal();}}catch(e){{dlg.setAttribute('open','')}}dlg.querySelector('.cm-note').hidden=true;}});}});
  dlg.querySelector('[data-post]').addEventListener('click',function(){{dlg.querySelector('.cm-note').hidden=false;}});
  var PH={{funding:'For example: has anyone applied for the Brain & Behavior Research Foundation Young Investigator Grant?',expertise:'For example: does anyone know someone who runs TMS with EEG?',student:'For example: I am hiring a graduate student to run sleep EEG sessions in the spring',other:'For example: who has run sleep EEG with older adults?'}},ti=dlg.querySelector('#cmc-t');
  dlg.querySelectorAll('input[name=kind]').forEach(function(r){{r.addEventListener('change',function(){{ti.placeholder=PH[r.value];}});}});
  var sd=document.querySelector('.cm-share');document.querySelectorAll('[data-share]').forEach(function(b){{b.addEventListener('click',function(){{try{{sd.showModal();}}catch(e){{sd.setAttribute('open','')}}sd.querySelector('.cm-note').hidden=true;}});}});
  sd.querySelectorAll('input[name=prod]').forEach(function(r){{r.addEventListener('change',function(){{sd.querySelector('.cm-newfields').hidden=r.value!=='new';}});}});
  sd.querySelector('[data-sendach]').addEventListener('click',function(){{sd.querySelector('.cm-note').hidden=false;}});
  try{{var k=new URLSearchParams(location.search).get('t');if(k&&PH[k]){{var r=dlg.querySelector('input[value='+k+']');r.checked=true;ti.placeholder=PH[k];setTimeout(function(){{try{{dlg.showModal();}}catch(e){{dlg.setAttribute('open','')}}}},400);}}}}catch(e){{}}
}})();
</script>
<script src="hubchrome.js" defer></script>
</body>
</html>
'''
open(V+'community.html','w').write(page)
print('ok')
