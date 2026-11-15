import sys
from urllib.parse import quote
sys.path.insert(0,'/tmp/claude-0/hubproto/gen')
from mail import mt
V='/tmp/claude-0/hubproto/v4/'
core=open(V+'core-ni.html').read()
hdr=core[core.index('<a class="skip"'):core.index('<main id="main">')]
hdr=hdr.replace('<a href="index.html#cores-h" aria-current="page">Resources</a>','<a href="index.html#cores-h">Resources</a>')
hdr=hdr.replace('<a href="events.html">Events</a>','<a href="events.html" aria-current="page">Events</a>')

# Real logistics from the Center's 2026 planning documents; people other than the three staff MW approved are fictional.
VEN={
 'hotel':('Bluemont Hotel','1212 Bluemont Avenue','Where out-of-town guests stay','https://maps.app.goo.gl/s2MBJzQAtdUMhSoK8'),
 'biz':('Business Building, Room 1092','1301 Lovers Lane','First floor, along the north wall','https://maps.app.goo.gl/s2MBJzQAtdUMhSoK8'),
 'bh':('Bluemont Hall','1114 Mid-Campus Drive','Tours start in the fourth-floor lobby','https://maps.app.goo.gl/8H25eBBk9Gpv9ssH8'),
 'mus':('Marianna Kistler Beach Museum of Art','701 Beach Lane','Use the main south entrance','https://maps.app.goo.gl/8LnGCWdU5b6CYWgz5'),
}
ROLES=[('all','A member or guest'),('talk','A speaker'),('poster','A poster presenter'),('mentor','A visiting mentor'),('core','A core director'),('eac','An advisory committee member')]

D1=[('8:40','9:00 a.m.','Coffee and a light breakfast','Optional','biz','meal',''),
 ('9:00','9:20 a.m.','Center overview','Heather Bailey, Center Director','biz','talk','core'),
 ('9:20','9:40 a.m.','Behavioral Neuroscience Core update','The Core Director','biz','talk','core'),
 ('9:40','9:50 a.m.','Break','','biz','break',''),
 ('9:50','10:10 a.m.','Neuroinformatics Core update','The Core Director','biz','talk','core'),
 ('10:10','10:30 a.m.','Cognitive Neuroscience Core update','The Core Director','biz','talk','core'),
 ('10:30','10:45 a.m.','Break','','biz','break',''),
 ('10:45','11:05 a.m.','Discussion of the cores','Everyone is invited to contribute','biz','disc','core mentor eac'),
 ('11:05','11:40 a.m.','The Center’s future, a guided discussion','Everyone is invited to contribute','biz','disc','mentor eac'),
 ('11:40','12:10 p.m.','Group photographs','In the Business Building atrium','biz','photo','all'),
 ('12:10','1:15 p.m.','Lunch','Boxed lunches for everyone who RSVPs, and usually a few extras','biz','meal',''),
 ('1:15','1:30 p.m.','Walk to Bluemont Hall','About 5 minutes','walk','walk',''),
 ('1:30','2:30 p.m.','Guided tours of the cores and the CONNECT Lab','Starting in the Bluemont Hall fourth-floor lobby','bh','tour','core'),
 ('2:30','2:45 p.m.','Break','','bh','break',''),
 ('2:45','4:00 p.m.','Advisory committee meeting','Closed meeting, Bluemont Hall, Room 106. Everyone else can hang posters or take a longer break.','bh','closed','eac core'),
 ('4:00','6:00 p.m.','Free time','Poster presenters can hang posters on the fourth floor of Bluemont Hall until 6:00 p.m.','bh','free','poster'),
 ('6:00','9:00 p.m.','Evening banquet and keynote address','Marianna Kistler Beach Museum of Art','mus','evening','all')]
D2=[('8:40','9:00 a.m.','Coffee and a light breakfast','Optional','biz','meal',''),
 ('9:00','9:05 a.m.','Opening remarks','Heather Bailey, Center Director','biz','talk',''),
 ('9:05','9:25 a.m.','Sleep spindles and memory in the aging brain','Research project, Dr. Priya Raman','biz','talk','talk'),
 ('9:25','9:45 a.m.','Mapping large-scale brain networks at scale','Research project, Dr. Rosa García','biz','talk','talk'),
 ('9:45','9:55 a.m.','Break','','biz','break',''),
 ('9:55','10:15 a.m.','Discussion of the research projects','Everyone is invited to contribute','biz','disc','mentor eac'),
 ('10:15','10:35 a.m.','What a night of sleep does to a new memory','Pilot project, Dr. Amara Okafor','biz','talk','talk'),
 ('10:35','10:45 a.m.','Break','','biz','break',''),
 ('10:45','11:05 a.m.','Brain stimulation and the speed of motor learning','Pilot project, Dr. Lena Park','biz','talk','talk'),
 ('11:05','11:20 a.m.','Discussion of the pilot projects','Everyone is invited to contribute','biz','disc','mentor eac'),
 ('11:20','11:30 a.m.','Walk to Bluemont Hall','About 5 minutes','walk','walk',''),
 ('11:30','12:25 p.m.','Poster session','Posters line the fourth-floor hallways of Bluemont Hall. Everyone is encouraged to attend.','bh','poster','poster all'),
 ('12:25','12:30 p.m.','Closing remarks','Heather Bailey, in the fourth-floor lobby','bh','talk','all')]
KIND={'meal':'Meal','talk':'Talk','break':'Break','disc':'Discussion','photo':'Photographs','walk':'Walk','tour':'Tours','closed':'Closed meeting','free':'Free time','evening':'Evening','poster':'Posters'}
def row(t):
    a,b,ti,de,pl,k,fr=t
    plc='' if pl=='walk' else f'<span class="sv-pl sv-pl-{pl}">{VEN[pl][0].split(",")[0]}</span>'
    return f'''<li class="sv-it sv-k-{k}" data-for="{fr}"><p class="sv-tm"><b>{a}</b><span>to {b}</span></p><div class="sv-ib"><p class="sv-kl"><span class="sv-kn">{KIND[k]}</span>{plc}</p><p class="sv-ti">{ti}</p>{f'<p class="sv-de">{de}</p>' if de else ''}</div></li>'''
d1=''.join(row(t) for t in D1); d2=''.join(row(t) for t in D2)

CK={
 'all':['<a href="#sv-rsvp">RSVP</a> for lunch and the banquet, and note any dietary needs','Please indicate whether you’re comfortable being photographed','Please add the Site Visit dates to your calendar. Use this link if you like: <a href="__OCAL__" target="_blank" rel="noopener">Outlook</a> or <a href="__GCAL__" target="_blank" rel="noopener">Google Calendar</a>.','Please read the program, the map, and the questions below','Pack comfortable walking shoes, layers, and an umbrella'],
 'talk':['Please plan for 15 minutes. The 20-minute slot leaves 3 minutes for questions and 2 for the next presenter to set up.','Please email your slides to Morgan Wills anytime before the visit, or bring the slides the morning of your talk','Please arrive a few minutes early to load your slides and check the projector','Stay for the discussion that follows your talk'],
 'poster':['Please confirm your entry in the poster booklet when Morgan Wills sends the booklet','Print your poster no larger than 60 by 40 inches','Please look for your poster number and hallway map, sent in advance','Hang your poster on Tuesday between 2:45 and 6:00 p.m. on the fourth floor of Bluemont Hall','Stand by your poster from 11:30 a.m. on Wednesday'],
 'mentor':['You aren’t asked to present, but your questions during each discussion are valuable','Your room at the Bluemont Hotel is booked for Monday and Tuesday nights','Arrange a ride with your mentee if you’d rather not use a rideshare','Please keep your travel receipts, sign the front of each receipt, and email the receipts to Roxana Ortiz'],
 'core':['Prepare a 15-minute core update. The 20-minute slot leaves 3 minutes for questions and 2 for the next presenter to set up.','Please plan your stops for the guided tours','Attend the closed advisory committee meeting at 2:45 p.m. on Tuesday','Participate in the group photo'],
 'eac':['Please read the meeting agenda below before Tuesday','Attend the closed meeting at 2:45 p.m. on Tuesday in Bluemont Hall, Room 106','Your room at the Bluemont Hotel is booked for Monday and Tuesday nights','Please keep your travel receipts, sign the front of each receipt, and email the receipts to Roxana Ortiz']}

import math as _m,random as _r
def _glowbrain(seed=21):
    R=_r.Random(seed);W=1440
    def trace(y,amp,k0,k1,spikes,ci):
        comps=[(k,R.uniform(0,6.283),R.uniform(.3,1)) for k in range(k0,k1)]
        sp=[(R.uniform(0,W),R.uniform(.6,1.0)*R.choice([-1,1])) for _ in range(spikes)]
        pts=[]
        for x in range(0,W+1,3):
            t=x/W*2*_m.pi
            v=sum(w*_m.sin(k*t+ph) for k,ph,w in comps)/len(comps)*3.0
            env=.9-.6*_m.exp(-((x-1130)/300)**2)
            v*=env
            for sx,h in sp:
                d=abs(x-sx)
                if d<10: v+=h*(1-d/10)*3.2*env
            pts.append(f'{x} {y+v*amp:.1f}')
        return f'<path class="tr tr{ci}" d="M'+' L'.join(pts)+'"/>'
    ys=[(250,9,40,70,6),(330,12,30,60,9),(410,15,26,56,12),(490,13,34,66,9),(570,10,22,48,7),(650,8,40,72,5)]
    traces=''.join(trace(y,a,k0,k1,sp,i) for i,(y,a,k0,k1,sp) in enumerate(ys))
    brain=('<g class="br" transform="translate(725 147) scale(1.35)">'
      '<path class="bo" d="M110 240 C 90 160 150 80 250 62 C 330 42 420 48 478 96 C 530 138 548 210 515 262 C 498 290 470 300 440 296 C 420 330 380 340 350 322 C 320 340 270 336 250 312 C 210 322 160 310 140 286 C 118 276 112 260 110 240 Z"/>'
      '<path class="bo" d="M440 296 C 470 300 500 290 505 315 C 505 345 470 355 440 345 C 425 338 425 310 440 296"/>'
      '<path class="bo" d="M405 322 C 410 348 412 372 420 398"/>'
      '<g class="su"><path d="M330 58 C 318 110 345 150 330 200"/><path d="M190 252 C 250 226 320 230 382 252"/><path d="M200 108 C 240 128 230 170 272 190"/><path d="M420 88 C 398 130 430 160 410 210"/><path d="M262 282 C 300 270 340 286 372 280"/><path d="M158 180 C 190 168 212 200 242 194"/><path d="M462 158 C 482 190 470 220 492 242"/><path d="M372 120 C 360 150 384 170 372 200"/><path d="M262 104 C 282 130 270 150 292 170"/></g></g>')
    return ('<svg class="sv-glow" viewBox="0 0 1440 860" preserveAspectRatio="xMaxYMid slice" aria-hidden="true" focusable="false">'
      '<defs><radialGradient id="sv-rg" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#c04fd8" stop-opacity=".55"/><stop offset=".45" stop-color="#7a3bb8" stop-opacity=".22"/><stop offset="1" stop-color="#2a1740" stop-opacity="0"/></radialGradient>'
      '<filter id="sv-gl" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
      '<ellipse cx="1130" cy="420" rx="420" ry="320" fill="url(#sv-rg)"/>'
      f'<g filter="url(#sv-gl)"><g class="trs">{traces}</g></g></svg>')
NEURO=_glowbrain()

CKH={'all':'For everyone','talk':'For speakers','poster':'For poster presenters','mentor':'For visiting mentors','core':'For core directors','eac':'For advisory committee members'}
ck=''.join(f'''<ul class="sv-ck" data-role="{k}"{'' if k=='all' else ' hidden'}><li class="sv-cklh" aria-hidden="true">{CKH[k]}</li>{''.join(f'<li><label><input type="checkbox" data-ck="{k}{i}"><span>{x}</span></label></li>' for i,x in enumerate(v))}</ul>''' for k,v in CK.items())
HINT={'all':'The essentials for everyone','talk':'Your talk slot and slides','poster':'Hanging and presenting your poster','mentor':'Your hotel and the discussions','core':'Your update, tours, and the closed meeting','eac':'The closed meeting and the meeting agenda'}
roles=''.join(f'<button type="button" aria-pressed="{"true" if k=="all" else "false"}" data-role="{k}"><span class="sv-rt">{l}</span><span class="sv-rh">{HINT[k]}</span></button>' for k,l in ROLES)

FAQ=[('I’m presenting. When do I send my slides?','There is no deadline. Please email your slides to Morgan Wills at mkwills@ksu.edu anytime before the visit, or bring them on a USB drive the morning of your talk. Please arrive a few minutes early to load them and check the projector.'),('I’m not presenting. Do I need to prepare?','No. Reading the program, the map, and these questions is enough. The Center looks forward to the perspectives you bring to each discussion.'),
 ('Where do I park?','Out-of-town guests park free at the Bluemont Hotel, and every venue is within walking distance. In-town guests can buy a $6 daily permit for the Union Parking Garage through the parking app, since street parking isn’t allowed before 9:00 a.m. Parking on campus is free after 5:00 p.m., so the banquet is easy.'),
 ('Can I get a ride?','Uber and other rideshares run in Manhattan, but cars can be scarce. Book ahead and allow extra time, or arrange a ride with your CNAP mentee.'),
 ('What will the weather be like?','Late May is usually mild: highs in the mid-70s to low 80s, evenings in the upper 50s to low 60s, and a chance of an afternoon thunderstorm. Rooms can be cool, so bring layers, a light jacket, and an umbrella.'),
 ('Is there Wi-Fi?','Yes. Guests from outside K-State can join the “KSU Guest” network.'),
 ('Can I join online?','Yes. Every session, including the keynote, has a Zoom option. The link comes in your confirmation email.'),
 ('What about meals?','Breakfast is at the hotel and at the Business Building each morning. Tuesday lunch is a boxed lunch for everyone who RSVPs, labeled for dietary needs. Wednesday lunch is informal: plenty of colleagues head out together after the poster session.'),
 ('How are photographs used?','Group photographs may appear on the CNAP website, in presentations, and in Center materials. You chose your photography preference when you RSVPed, and Morgan Wills can change it for you.'),
 ('How do I get reimbursed for travel?','Keep your receipts, sign the front of each receipt, and email the receipts to Roxana Ortiz after the visit. Lodging, hotel parking, and breakfast are already covered, so you won’t be charged for those.')]
faq=''.join(f'<details class="sv-fq"><summary>{q}</summary><p>{a}</p></details>' for q,a in FAQ)

PHOTOS=['Everyone','The Behavioral Neuroscience Core','The Cognitive Neuroscience Core','The Neuroinformatics Core','The Administrative Core','Primary project award recipients','Pilot project award recipients','The External Advisory Committee','All graduate students']
photos=''.join(f'<li><span class="num">{i}</span>{p}</li>' for i,p in enumerate(PHOTOS,1))
DINE=[('The Chef Café','Breakfast and lunch from a local kitchen','https://www.toasttab.com/local/order/thechefcafe'),('Bluestem Bistro','Coffee, sandwiches, and light lunches','https://order.online/store/-28139002/'),('So Long Saloon','Burgers and regional cooking','https://www.allmenus.com/ks/manhattan/256968-so-long-saloon/menu/'),('Tallgrass Taphouse','Pub-style dining','https://www.toasttab.com/tallgrasstaphouse'),('Liquid Art Winery and Estate','A winery with a restaurant. Call ahead.','https://www.liquidartwinery.com/tasting-room')]
dine=''.join(f'<li><b>{a}</b><span>{b}</span><a class="t3" href="{u}" target="_blank" rel="noopener">See the menu</a></li>' for a,b,u in DINE)

ven=''.join(f'''<li class="sv-v sv-v-{k}"><span class="sv-vn num" aria-hidden="true">{i}</span><img class="sv-vph" src="img/venue-{k}.jpg" alt="{v[0]}" loading="lazy"><div><p class="sv-vt">{v[0]}</p><p class="sv-va">{v[1]}, Manhattan, Kansas</p><p class="sv-vd">{v[2]}</p><a class="t3" href="{v[3]}" target="_blank" rel="noopener">Walking directions</a></div></li>''' for i,(k,v) in enumerate(VEN.items(),1))

GCAL='https://calendar.google.com/calendar/render?action=TEMPLATE&amp;text='+quote('CNAP Site Visit')+'&amp;dates=20270525/20270527&amp;details='+quote('The 2027 CNAP Site Visit, Kansas State University. Program: the Site Visit page in the Member Hub.')+'&amp;location='+quote('Kansas State University, Manhattan, Kansas')
OCAL='https://outlook.office.com/calendar/0/deeplink/compose?subject='+quote('CNAP Site Visit')+'&amp;startdt=2027-05-25&amp;enddt=2027-05-27&amp;allday=true&amp;location='+quote('Kansas State University, Manhattan, Kansas')
ck=ck.replace('__OCAL__',OCAL).replace('__GCAL__',GCAL)
ASK=mt('mkwills@ksu.edu','Site Visit question','\n'.join(['Name:','','My question:','']))
RCPT=mt('roxana@ksu.edu','Site Visit travel receipts','\n'.join(['Name:','','Receipts attached for:','']))

SECS=[('sv-dates','Preparation dates'),('sv-why','Why Site Visit'),('sv-prog','The program'),('sv-eve','The evening'),('sv-rsvp','RSVP'),('sv-map','Getting around'),('sv-you','Your checklist'),('sv-stay','Travel and stay'),('sv-food','Food'),('sv-pho','Photographs'),('sv-heard','Last year’s feedback'),('sv-faq','Questions')]
spine=''.join(f'<li><a href="#{i}"><span class="n"><b>{n}</b></span><span>{t}</span></a></li>' for n,(i,t) in enumerate(SECS,1))

page=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>The 2027 Site Visit · CNAP Member Hub</title>
<link rel="stylesheet" href="guide.css">
</head>
<body class="sv-page">
{hdr}<main id="main">
  <aside class="card ask sv-ask sv-askf" aria-label="Who to ask"><h2>Who to ask</h2><div class="pp-row"><div class="pp-it"><button type="button" class="pp-b" aria-expanded="false" aria-controls="sv-pp-mw" title="Morgan Wills, Assistant Director for Grants and Contracts"><span class="pp-i">MW</span><span class="sr">Morgan Wills, Assistant Director for Grants and Contracts</span></button><div class="pp-p" id="sv-pp-mw" hidden><p class="pp-r">Assistant Director for Grants and Contracts</p><p class="pp-n">Morgan Wills</p><a class="pp-e" href="{ASK}">mkwills@ksu.edu</a><p class="pp-d">The Site Visit, RSVPs, and the program.</p></div></div><div class="pp-it"><button type="button" class="pp-b" aria-expanded="false" aria-controls="sv-pp-ro" title="Roxana Ortiz, Grant Specialist and Accountant"><span class="pp-i">RO</span><span class="sr">Roxana Ortiz, Grant Specialist and Accountant</span></button><div class="pp-p" id="sv-pp-ro" hidden><p class="pp-r">Grant Specialist and Accountant</p><p class="pp-n">Roxana Ortiz</p><a class="pp-e" href="{RCPT}">roxana@ksu.edu</a><p class="pp-d">Travel and reimbursement.</p></div></div><div class="pp-it"><button type="button" class="pp-b" aria-expanded="false" aria-controls="sv-pp-hb" title="Heather Bailey, Director"><span class="pp-i">HB</span><span class="sr">Heather Bailey, Director</span></button><div class="pp-p" id="sv-pp-hb" hidden><p class="pp-r">Director</p><p class="pp-n">Heather Bailey</p><a class="pp-e" href="mailto:hbailey@ksu.edu">hbailey@ksu.edu</a><p class="pp-d">The Center and the Site Visit program.</p></div></div><div class="pp-it"><button type="button" class="pp-b" aria-expanded="false" aria-controls="sv-pp-help" title="Help during the visit"><span class="pp-i"><svg viewBox="0 0 16 16" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><rect x="2" y="3.5" width="12" height="9" rx="1.5"/><path d="M2.5 4.5 8 9l5.5-4.5"/></svg></span><span class="sr">Help during the visit</span></button><div class="pp-p" id="sv-pp-help" hidden><p class="pp-n">Help during the visit</p><p class="pp-d">A phone number for help is in your confirmation email. General questions go to <a href="mailto:cnap@ksu.edu">cnap@ksu.edu</a>.</p></div></div></div></aside>
  <nav class="spine sv-rail" aria-label="Sections on this page"><p class="spine-h">On this page</p><div class="spine-track" aria-hidden="true"><span class="spine-fill"></span></div><ol>{spine}</ol></nav>

  <section class="sv-hero" aria-labelledby="t">
    {NEURO}
    <div class="wrap">
      <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><a href="events.html">Events</a><span aria-hidden="true">/</span><span aria-current="page">The 2027 Site Visit</span></nav>
      <div class="sv-hg">
        <div class="sv-hd">
          <p class="for">Kansas State University · Manhattan, Kansas</p>
          <h1 id="t">The 2027 CNAP Site Visit</h1>
          <p class="sv-lead">Two days with the people behind the Center’s science: core tours, project talks, an evening at the Beach Museum, and a poster session that fills the halls of Bluemont Hall.</p>
          <div class="sv-act"><a class="btn pri" href="#sv-rsvp">RSVP</a><a class="btn" href="#sv-prog">See the program</a><span class="sv-cal">Add to <a href="{GCAL}" target="_blank" rel="noopener">Google Calendar</a> or <a href="{OCAL}" target="_blank" rel="noopener">Outlook</a></span></div>
        </div>
        <div class="sv-when" aria-label="Tuesday, May 25, and Wednesday, May 26, 2027">
          <p class="sv-im"><span>May 2027</span></p>
          <div class="sv-dpair">
            <div><p class="sv-dw">Tuesday</p><p class="sv-dn">25</p><p class="sv-dt">8:40 a.m. to 9:00 p.m.</p></div>
            <div><p class="sv-dw">Wednesday</p><p class="sv-dn">26</p><p class="sv-dt">8:40 a.m. to 12:30 p.m.</p></div>
          </div>
          <p class="sv-cd"><b class="num" data-days>192</b> days to go</p>
        </div>
      </div>
    </div>
  </section>

  <section class="sv-dk" id="sv-dates" aria-labelledby="sv-dk-h">
    <div class="wrap">
      <div class="sv-dkh"><h2 id="sv-dk-h">Your 2027 Site Visit preparation dates</h2><button class="btn" type="button" id="sv-dk-all">Add all dates to my calendar</button></div>
      <ol class="sv-dkg"><li class="sv-dkc"><p class="sv-dkd">Thursday, March 25</p><p class="sv-dkt">RSVP closes</p><p class="sv-dkx">Please use the RSVP form on this page.</p><p class="sv-dkl">Add to <a href="https://outlook.office.com/calendar/0/deeplink/compose?subject=CNAP%20Site%20Visit%3A%20RSVP%20closes&amp;startdt=2027-03-25&amp;enddt=2027-03-26&amp;allday=true" target="_blank" rel="noopener">Outlook</a> or <a href="https://calendar.google.com/calendar/render?action=TEMPLATE&amp;text=CNAP%20Site%20Visit%3A%20RSVP%20closes&amp;dates=20270325/20270326&amp;details=Use%20the%20RSVP%20form%20on%20the%20Site%20Visit%20page.&amp;ctz=America/Chicago" target="_blank" rel="noopener">Google</a></p></li><li class="sv-dkc"><p class="sv-dkd">Friday, April 23</p><p class="sv-dkt">Poster registration closes</p><p class="sv-dkx">Please register in the RSVP form on this page.</p><p class="sv-dkl">Add to <a href="https://outlook.office.com/calendar/0/deeplink/compose?subject=CNAP%20Site%20Visit%3A%20poster%20registration%20closes&amp;startdt=2027-04-23&amp;enddt=2027-04-24&amp;allday=true" target="_blank" rel="noopener">Outlook</a> or <a href="https://calendar.google.com/calendar/render?action=TEMPLATE&amp;text=CNAP%20Site%20Visit%3A%20poster%20registration%20closes&amp;dates=20270423/20270424&amp;details=Register%20in%20the%20RSVP%20form%20on%20this%20page.&amp;ctz=America/Chicago" target="_blank" rel="noopener">Google</a></p></li><li class="sv-dkc sv-dkc-open"><p class="sv-dkd">Anytime before your talk</p><p class="sv-dkt">Speakers’ slides</p><p class="sv-dkx">Please email your slides to Morgan Wills, or bring the slides the morning of your talk. There is no deadline.</p><p class="sv-dkl"><a href="#sv-faq">More in Questions</a></p></li><li class="sv-dkc"><p class="sv-dkd">Tuesday, May 25</p><p class="sv-dkt">Day 1</p><p class="sv-dkx">Breakfast by 8:40 a.m. in the Business Building. The program begins at 9:00 a.m.</p><p class="sv-dkl">Add to <a href="https://outlook.office.com/calendar/0/deeplink/compose?subject=CNAP%20Site%20Visit%2C%20day%201&amp;startdt=2027-05-25T08:40:00&amp;enddt=2027-05-25T21:00:00" target="_blank" rel="noopener">Outlook</a> or <a href="https://calendar.google.com/calendar/render?action=TEMPLATE&amp;text=CNAP%20Site%20Visit%2C%20day%201&amp;dates=20270525T084000/20270525T210000&amp;details=Breakfast%20by%208%3A40%20a.m.%20in%20the%20Business%20Building.%20The%20program%20begins%20at%209%3A00%20a.m.&amp;ctz=America/Chicago" target="_blank" rel="noopener">Google</a></p></li><li class="sv-dkc"><p class="sv-dkd">Wednesday, May 26</p><p class="sv-dkt">Day 2</p><p class="sv-dkx">Breakfast by 8:40 a.m. The visit ends by 12:30 p.m. in Bluemont Hall.</p><p class="sv-dkl">Add to <a href="https://outlook.office.com/calendar/0/deeplink/compose?subject=CNAP%20Site%20Visit%2C%20day%202&amp;startdt=2027-05-26T08:40:00&amp;enddt=2027-05-26T12:30:00" target="_blank" rel="noopener">Outlook</a> or <a href="https://calendar.google.com/calendar/render?action=TEMPLATE&amp;text=CNAP%20Site%20Visit%2C%20day%202&amp;dates=20270526T084000/20270526T123000&amp;details=Breakfast%20by%208%3A40%20a.m.%20The%20visit%20ends%20by%2012%3A30%20p.m.%20in%20Bluemont%20Hall.&amp;ctz=America/Chicago" target="_blank" rel="noopener">Google</a></p></li></ol>
    </div>
  </section>

  <section class="sv-sec sv-why" id="sv-why" aria-labelledby="sv-why-h">
    <div class="wrap">
      <header class="sv-sh"><h2 id="sv-why-h">Why Site Visit</h2><p>The Site Visit gives Center members an important opportunity to reflect on the past year and look ahead to the next. The Site Visit also gives the Center’s External Advisory Committee a firsthand view of the Center’s progress and where the Center stands today. We hope everyone leaves motivated and encouraged in each member’s work and role within the CNAP scientific community.</p></header>
      <div class="sv-three">
        <article><p class="sv-n num">01</p><h3>Stronger together</h3><p>Mentors, project leaders, core staff, and students meet in person, and the conversations started here often become collaborations.</p></article>
        <article><p class="sv-n num">02</p><h3>Science up close</h3><p>Hear where each project and core stands, walk through the labs, and see the work of two dozen students and trainees on the poster walls.</p></article>
        <article><p class="sv-n num">03</p><h3>The next generation</h3><p>Graduate students present alongside faculty, and the feedback from visiting experts shapes the projects that follow.</p></article>
      </div>
      <ul class="sv-nums" aria-label="The 2026 Site Visit in numbers"><li><a href="#sv-heard"><b class="num">56</b><span>Attendees in 2026</span><em>What attendees said</em></a></li><li><a href="#sv-prog" data-day="2"><b class="num">24</b><span>Posters</span><em>The poster session</em></a></li><li><a href="#sv-prog"><b class="num">9</b><span>Speakers, including the keynote</span><em>The program</em></a></li><li><a href="index.html#cores-h"><b class="num">3</b><span>Research cores on tour</span><em>The cores</em></a></li><li><a href="research.html"><b class="num">4</b><span>Research and pilot projects</span><em>The projects</em></a></li></ul>
    </div>
  </section>

  <div class="sv-tband"><div class="wrap">
      <div class="sv-tailor" id="sv-tailor" role="group" aria-labelledby="sv-tlx"><div class="sv-tlx"><p id="sv-tlx">See the visit as</p><p>Your choice highlights your sessions in the program and adds your tasks to the checklist. This choice is not your RSVP.</p></div><div class="sv-rb">{roles}</div></div>
  </div></div>

  <section class="sv-sec sv-prog" id="sv-prog" aria-labelledby="sv-prog-h">
    <div class="wrap">
      <header class="sv-sh"><h2 id="sv-prog-h">The program</h2><p>All times are Central. <span class="sv-hl-note" hidden>Sessions marked with a dot are the ones for you.</span></p></header>
      <div class="sv-days" role="tablist" aria-label="Day"><button type="button" role="tab" aria-selected="true" aria-controls="sv-d1" id="sv-t1"><b>Day 1</b><span>Tuesday, May 25</span></button><button type="button" role="tab" aria-selected="false" aria-controls="sv-d2" id="sv-t2"><b>Day 2</b><span>Wednesday, May 26</span></button></div>
      <ol class="sv-tl" id="sv-d1" role="tabpanel" aria-labelledby="sv-t1">{d1}</ol>
      <ol class="sv-tl" id="sv-d2" role="tabpanel" aria-labelledby="sv-t2" hidden>{d2}</ol>
    </div>
  </section>

  <section class="sv-eve" id="sv-eve" aria-labelledby="sv-eve-h">
    <div class="wrap sv-eg">
      <div class="sv-et">
        <p class="sv-ek">Tuesday, May 25 · 6:00 to 9:00 p.m.</p>
        <h2 id="sv-eve-h">An evening at the Beach Museum</h2>
        <p class="sv-el">Dinner among the galleries of the Marianna Kistler Beach Museum of Art, followed by the keynote address. Parking beside the museum is free after 5:00 p.m., and the hotel is a 5-minute walk away.</p>
        <ol class="sv-run"><li><b>6:00</b>Arrival and open bar, with two drink tickets each</li><li><b>6:30</b>Buffet dinner</li><li><b>7:00</b>Dinner and conversation</li><li><b>7:30</b>Keynote address</li><li><b>8:25</b>Closing remarks from the Director</li></ol>
        <div class="sv-key"><p class="sv-kk">Keynote address</p><p class="sv-kt">The 2027 keynote speaker will be announced on this page.</p><p class="sv-kdesc">Each year a nationally known neuroscientist closes the first day with a talk written for the whole Center.</p></div>
      </div>
      <figure class="sv-menu" aria-labelledby="menu-h">
        <p class="sv-mk" id="menu-h">The 2026 menu</p>
        <div class="sv-mg"><p class="sv-mh">Entrées</p><p>Chicken breast almondine with a wild rice blend</p><p>Steak Portofino with mushrooms, roasted peppers, and onions</p></div>
        <div class="sv-mg"><p class="sv-mh">Salads and sides</p><p>Sonoma salad with cranberries, feta, and candied pecans</p><p>Rotini and tortellini pasta salad · Wild rice salad</p><p>Green beans · Garlic-herb mashed potatoes</p></div>
        <div class="sv-mg"><p class="sv-mh">Dessert</p><p>Apple cobbler with vanilla ice cream</p></div>
        <figcaption>Wine, beer, cocktails, and soft drinks. Dietary needs from your RSVP are noted at the door.</figcaption>
      </figure>
    </div>
  </section>

  <section class="sv-sec sv-rsvp" id="sv-rsvp" aria-labelledby="sv-rsvp-h">
    <div class="wrap sv-fg">
      <header class="sv-sh"><h2 id="sv-rsvp-h">RSVP</h2><p>Attendance is expected of core directors, primary project leaders, pilot project leaders, the External Advisory Committee, the Center Director, and the Associate Director. Everyone else interested is welcome, and students involved in the Center are especially encouraged to come.</p><p>One form covers attendance, meals, and photographs. When you finish, a confirmation email arrives with the details, your answers, and a calendar file for Outlook.</p><p class="sv-fine">Please RSVP by Thursday, March 25. Questions go to Morgan Wills.</p><p class="proto-note">Prototype. This form does not send anything yet.</p></header>
      <div class="sv-rs">
        <form id="sv-form" novalidate>
          <fieldset><legend>How will you attend?</legend><div class="sv-ops"><label class="sv-op"><input type="radio" name="att" value="person" checked><span>I will attend in person</span></label><label class="sv-op"><input type="radio" name="att" value="zoom"><span>I will attend on Zoom</span></label><label class="sv-op"><input type="radio" name="att" value="no"><span>I am unable to attend</span></label></div></fieldset>
          <fieldset data-show="person"><legend>Which parts of the Site Visit do you plan to attend?</legend><div class="sv-ops"><label class="sv-op sv-op2"><input type="checkbox" name="part" value="0" checked><span><b>Tuesday, 8:40 a.m. to 1:15 p.m.</b><em>Breakfast, the Center overview, core updates and discussion, group photographs, and lunch</em></span></label><label class="sv-op sv-op2"><input type="checkbox" name="part" value="1" checked><span><b>Tuesday, 1:30 to 2:30 p.m.</b><em>Guided tours of the cores and the CONNECT Lab</em></span></label><label class="sv-op sv-op2"><input type="checkbox" name="part" value="2" checked><span><b>Tuesday, 2:45 to 4:00 p.m.</b><em>Advisory committee meeting, closed session</em></span></label><label class="sv-op sv-op2"><input type="checkbox" name="part" value="3" checked><span><b>Tuesday, 6:00 to 9:00 p.m.</b><em>Keynote address and banquet</em></span></label><label class="sv-op sv-op2"><input type="checkbox" name="part" value="4" checked><span><b>Wednesday, 8:40 to 11:20 a.m.</b><em>Breakfast, then the research project and pilot project presentations</em></span></label><label class="sv-op sv-op2"><input type="checkbox" name="part" value="5" checked><span><b>Wednesday, 11:30 a.m. to 12:30 p.m.</b><em>Poster session</em></span></label></div></fieldset>
          <fieldset data-show="person"><legend>Which meals do you plan to attend?</legend><div class="sv-ops"><label class="sv-op"><input type="checkbox" name="meal" value="lunch" checked><span>Tuesday lunch, about halfway through the morning program</span></label><label class="sv-op"><input type="checkbox" name="meal" value="dinner" checked><span>Tuesday dinner, the keynote address and banquet</span></label><label class="sv-op"><input type="checkbox" name="meal" value="neither"><span>Neither</span></label></div><p class="sv-hint">This gives the caterers a headcount. Breakfast needs no RSVP.</p></fieldset>
          <label class="sv-tx sv-q" data-show="person"><b>It is our pleasure to accommodate your dietary restrictions. Please describe your dietary restrictions, or leave this blank.</b><textarea name="diet" rows="2"></textarea></label>
          <fieldset data-show="person"><legend>CNAP will have a photographer and videographer at the event. May we use photographs or videos that include your image in public materials, such as our website, presentation slides, social media, or promotional content?</legend><div class="sv-ops sv-ops-row"><label class="sv-op"><input type="radio" name="photo" value="yes"><span>Yes</span></label><label class="sv-op"><input type="radio" name="photo" value="no"><span>No</span></label></div><p class="sv-hint">Your participation is not affected if you prefer to opt out.</p></fieldset>
          <fieldset data-show="person"><legend>Will you need parking?</legend><div class="sv-ops"><label class="sv-op"><input type="radio" name="park" value="drive"><span>I’ll drive and need parking</span></label><label class="sv-op"><input type="radio" name="park" value="nodrive"><span>I won’t need parking</span></label></div><p class="sv-hint">New for 2027, after last year’s feedback about the parking garage.</p></fieldset>
          <fieldset data-show="person"><legend>Traveling from out of town? Which nights do you need a hotel room?</legend><div class="sv-ops"><label class="sv-op"><input type="checkbox" name="stay" value="mon"><span>Monday night, May 24</span></label><label class="sv-op"><input type="checkbox" name="stay" value="tue"><span>Tuesday night, May 25</span></label></div><p class="sv-hint">Please leave both unchecked if you don’t need a room. Roxana Ortiz confirms each room by email.</p></fieldset>
          <fieldset data-show="person zoom"><legend>Would you like to register for the poster session on Wednesday?</legend><div class="sv-ops"><label class="sv-op"><input type="radio" name="poster" value="yes"><span>Yes</span></label><label class="sv-op"><input type="radio" name="poster" value="no"><span>No</span></label><label class="sv-op"><input type="radio" name="poster" value="done"><span>I’ve already registered</span></label><label class="sv-op"><input type="radio" name="poster" value="later"><span>I plan to register later</span></label><label class="sv-op"><input type="radio" name="poster" value="maybe"><span>Maybe. Please send more information first.</span></label></div></fieldset>
          <div class="sv-pp" id="sv-pp" hidden>
            <p class="sv-ck2">The poster session</p>
            <p class="sv-pp-host">Hosted by the Kansas State University Department of Psychological Sciences.</p>
            <dl class="sv-pp-facts">
              <div><dt>Where</dt><dd>The fourth-floor hallways of Bluemont Hall</dd></div>
              <div><dt>When</dt><dd>Wednesday, May 26, 11:30 a.m. to 12:25 p.m.</dd></div>
              <div><dt>Hang your poster</dt><dd>Tuesday, May 25, between 2:45 and 6:00 p.m., during the free time. The building stays open until 6:00 p.m. Hanging the day before lets you attend the project talks that come right before the session.</dd></div>
              <div><dt>Largest size</dt><dd>60 by 40 inches</dd></div>
              <div><dt>Poster number and map</dt><dd>Sent to you before the visit</dd></div>
              <div><dt>Please register by</dt><dd>Friday, April 23, 2027</dd></div>
            </dl>
            <fieldset><legend>Would you like to enter your poster information now?</legend><div class="sv-ops sv-ops-row"><label class="sv-op"><input type="radio" name="pnow" value="now" checked><span>Yes, now</span></label><label class="sv-op"><input type="radio" name="pnow" value="later"><span>I’ll add the poster information later</span></label></div><p class="sv-hint" id="sv-pl-hint" hidden>Please return to this page any time before Friday, April 23. Your confirmation email will include a reminder.</p></fieldset>
            <div class="sv-pfields" id="sv-pfields">
              <label class="sv-tx"><span>Poster title</span><textarea name="ptitle" rows="2"></textarea></label>
              <label class="sv-tx"><span>Authors, first name followed by last name</span><input type="text" name="pauth" autocomplete="off"></label>
              <label class="sv-tx"><span>Affiliation, the university followed by the department</span><input type="text" name="paff" placeholder="Kansas State University, Department of Psychological Sciences" autocomplete="off"></label>
              <label class="sv-tx"><span>Abstract, up to 150 words</span><textarea name="pabs" rows="6"></textarea><small class="sv-wc" id="sv-wc">0 of 150 words</small></label>
            </div>
          </div>
          <fieldset class="sv-me"><legend>About you</legend>
            <p class="sv-who-am">Amara Okafor <span>(fictional member, from your Hub profile)</span></p>
            <label class="sv-tx" data-show="person zoom"><span>A different first name for your name tag, if you’d like one</span><input type="text" name="tag" placeholder="For example, Mike instead of Michael" autocomplete="off"></label>
            <label class="sv-tx"><span>Your connection to CNAP</span><select name="role"><option>University or departmental leadership</option><option>New or interested</option><option>General member</option><option>Mentor</option><option selected>Pilot project leader</option><option>Primary research project leader</option><option>Core director</option><option>External Advisory Committee member</option><option>Graduate student</option><option>Postdoctoral fellow</option><option>Other</option></select></label>
          </fieldset>
          <label class="sv-tx sv-q" data-show="person"><b>Accessibility needs, or anything else we should know</b><textarea name="note" rows="2"></textarea></label>
          <div class="sv-rs-act"><button class="btn pri" type="submit">Send my RSVP</button></div>
        </form>
        <div class="sv-done" id="sv-done" hidden tabindex="-1">
          <p class="sv-ck2">RSVP received</p>
          <h3 id="sv-thx">Thank you, Amara.</h3>
          <p>Your confirmation email is on the way. Here is what the email says.</p>
          <article class="sv-mail" aria-label="Confirmation email preview">
            <dl class="sv-mhd"><div><dt>From</dt><dd>CNAP, cnap@ksu.edu</dd></div><div><dt>To</dt><dd>Amara Okafor</dd></div><div><dt>Subject</dt><dd id="sv-subj">You’re registered for the 2027 CNAP Site Visit</dd></div></dl>
            <div class="sv-mb">
              <p id="sv-hello">Dear Amara,</p>
              <p id="sv-lead2">Thank you for registering for the 2027 CNAP Site Visit. We look forward to having you in Manhattan.</p>
              <div class="sv-cal2" id="sv-calbox"><p><b>Tuesday, May 25, and Wednesday, May 26, 2027</b><br>Kansas State University, Manhattan, Kansas</p><button class="btn pri" type="button" id="sv-ics">Add to my Outlook calendar</button><p class="sv-hint">The calendar file holds both days, with a reminder the day before each. In the email, the calendar file is attached.</p></div>
              <h4>The program at a glance</h4>
              <ul class="sv-glance"><li><b>Tuesday morning</b> Center overview, core updates, and discussion</li><li><b>Tuesday afternoon</b> Guided tours of the cores and the CONNECT Lab</li><li><b>Tuesday evening</b> Keynote address and banquet at the Beach Museum</li><li><b>Wednesday morning</b> Project presentations, then the poster session</li><li><b>Wednesday</b> The visit ends by 12:30 p.m.</li></ul>
              <p id="sv-sched">A detailed schedule, with rooms and the speaker lineup, follows in the weeks before the visit.</p>
              <h4>Your answers</h4>
              <dl class="sv-meals" id="sv-sum"></dl>
              <p id="sv-postr" hidden>Your poster details are still to come. Please add the poster details on the Site Visit page by Friday, April 23.</p>
              <p>To change an answer, return to the Site Visit page. Questions go to Morgan Wills at mkwills@ksu.edu.</p>
              <p>With thanks,<br>The CNAP office</p>
            </div>
          </article>
          <button class="btn" type="button" id="sv-edit">Change my answers</button>
          <p class="proto-note">Prototype. Nothing was sent, and no email goes out.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="sv-sec sv-map" id="sv-map" aria-labelledby="sv-map-h">
    <div class="wrap">
      <header class="sv-sh"><h2 id="sv-map-h">Getting around</h2><p>Four places, all within a 15-minute walk of the hotel. The diagram shows the walk between each one.</p></header>
      <div class="sv-mapg">
        <figure class="sv-route" aria-label="Walking times: hotel to Business Building 10 minutes, Business Building to Bluemont Hall 5 minutes, hotel to Bluemont Hall 15 minutes, hotel to the Beach Museum 5 minutes">
          <svg viewBox="0 0 560 480" aria-hidden="true">
            <g class="sv-north"><path d="M520 62 L520 30 M513 40 L520 28 L527 40"/><text x="520" y="80">N</text></g>
            <path class="sv-r2" d="M160 74 C 250 70, 300 110, 322 172"/>
            <path class="sv-r0" d="M450 352 C 400 352, 360 336, 346 300 L 336 212"/>
            <path class="sv-r3" d="M452 376 C 380 414, 260 414, 172 404"/>
            <path class="sv-r1" d="M452 370 C 380 380, 260 368, 210 326 C 160 280, 140 180, 140 94"/>
            <g class="sv-tag"><rect x="214" y="58" width="64" height="24" rx="12"/><text x="246" y="75">5 min</text></g>
            <g class="sv-tag"><rect x="352" y="244" width="74" height="24" rx="12"/><text x="389" y="261">10 min</text></g>
            <g class="sv-tag"><rect x="270" y="398" width="64" height="24" rx="12"/><text x="302" y="415">5 min</text></g>
            <g class="sv-tag"><rect x="120" y="226" width="74" height="24" rx="12"/><text x="157" y="243">15 min</text></g>
            <g class="sv-st sv-st-bh"><circle cx="140" cy="74" r="20"/><text x="140" y="80">3</text><text class="sv-lb" x="140" y="38" style="text-anchor:middle">Bluemont Hall</text></g>
            <g class="sv-st sv-st-biz"><circle cx="330" cy="192" r="20"/><text x="330" y="198">2</text><text class="sv-lb" x="360" y="198">Business Building</text></g>
            <g class="sv-st sv-st-mus"><circle cx="150" cy="402" r="20"/><text x="150" y="408">4</text><text class="sv-lb" x="150" y="448" style="text-anchor:middle">Beach Museum</text></g>
            <g class="sv-st sv-st-hotel"><circle cx="470" cy="362" r="20"/><text x="470" y="368">1</text><text class="sv-lb" x="470" y="408" style="text-anchor:middle">Bluemont Hotel</text></g>
          </svg>
          <figcaption>A diagram of walking times with north at the top, not drawn to scale. Directional signs are posted at every venue.</figcaption>
        </figure>
        <ol class="sv-vs">{ven}</ol>
      </div>
    </div>
  </section>

  <section class="sv-sec sv-you" id="sv-you" aria-labelledby="sv-you-h">
    <div class="wrap sv-yg">
      <header class="sv-sh"><h2 id="sv-you-h">Your checklist</h2><p>The list follows the role you chose at the top of the page.</p><p>Your ticks are saved in this browser only.</p><div class="sv-ckp" aria-live="polite"><p class="sv-ckpn"><b data-ckdone>0</b> of <span data-cktotal>0</span> done</p><span class="sv-ckpb" aria-hidden="true"><i></i></span></div><p class="sv-yr">Showing the list for <b data-rolename>a member or guest</b>.</p><p class="sv-yr"><a href="#sv-tailor">Change your role</a></p><figure class="sv-ckph"><span class="im"><img src="img/reel-2.jpg" alt="Placeholder for a photo of a core tour at the 2026 Site Visit" loading="lazy"><span class="tag">Photo placeholder</span></span></figure></header>
      <div class="sv-ckw">{ck}
        <details class="sv-ag" data-role="eac" hidden><summary>The closed meeting agenda</summary><ol><li>Feedback on the year’s progress, and suggestions</li><li>Grant program updates and the administrative supplement opportunity</li><li>Core updates, staffing, and challenges</li><li>Plans for the Center’s next phase: sustainability and a stronger campus-wide presence</li></ol></details>
      </div>
    </div>
  </section>

  <section class="sv-sec sv-stay" id="sv-stay" aria-labelledby="sv-stay-h">
    <div class="wrap">
      <header class="sv-sh"><h2 id="sv-stay-h">Travel and stay</h2></header>
      <div class="sv-cards">
        <article class="sv-c sv-c-lead"><p class="sv-ck2">For out-of-town guests</p><h3>Your room is booked</h3><p>The Center reserves a room for each out-of-town guest at the Bluemont Hotel from Monday, May 24, to Wednesday, May 26. Please give your first and last name at the front desk for your key.</p><dl class="sv-dl"><div><dt>Check-in</dt><dd>4:00 p.m.</dd></div><div><dt>Checkout</dt><dd>11:00 a.m.</dd></div><div><dt>Covered by the Center</dt><dd>Lodging, hotel parking, and breakfast</dd></div><div><dt>Early or late</dt><dd>Luggage storage is available. Please ask the front desk about early check-in or late checkout.</dd></div></dl><p class="sv-fine">The hotel is smoke-free, and smoking in a room carries a $250 cleaning fee.</p></article>
        <article class="sv-c"><p class="sv-ck2">For K-State guests</p><h3>Parking</h3><p>Street parking isn’t allowed before 9:00 a.m. Please park in the Union Parking Garage with a $6 daily permit from the parking app. Campus parking is free after 5:00 p.m.</p><a class="t3" href="https://www.k-state.edu/parking/parking/visitor.html" target="_blank" rel="noopener">Visitor parking at K-State</a></article>
        <article class="sv-c"><p class="sv-ck2">After the visit</p><h3>Travel reimbursement</h3><p>Please sign the front of each receipt, then email your receipts to Roxana Ortiz, Grant Specialist and Accountant. Lodging, hotel parking, and breakfast are already paid.</p><a class="t3" href="{RCPT}">Email Roxana</a><span class="sv-em">roxana@ksu.edu</span></article>
        <article class="sv-c"><p class="sv-ck2">What to bring</p><h3>Shoes, layers, and an umbrella</h3><p>The program moves between buildings, the rooms run cool, and late-May afternoons can bring a thunderstorm. Highs are usually in the 70s.</p></article>
      </div>
    </div>
  </section>

  <section class="sv-sec sv-food" id="sv-food" aria-labelledby="sv-food-h">
    <div class="wrap sv-fg">
      <header class="sv-sh"><h2 id="sv-food-h">Food</h2><p>Note any dietary needs in your RSVP. Dietary needs are accommodated at every meal the Center provides.</p><dl class="sv-meals"><div><dt>Each morning</dt><dd>Coffee and a light breakfast in the Business Building. Out-of-town guests also have breakfast at the hotel.</dd></div><div><dt>Tuesday lunch</dt><dd>A boxed lunch for everyone who RSVPs, labeled with your name and dietary needs.</dd></div><div><dt>Tuesday dinner</dt><dd>A buffet at the banquet. Staff will guide you to your options.</dd></div><div><dt>Wednesday lunch</dt><dd>With colleagues at a restaurant nearby, after the poster session.</dd></div></dl></header>
      <div class="sv-food2"><p class="sv-ck2">Wednesday lunch with colleagues</p><p>After the poster session, groups head out together. Most places open around 12:30 p.m.</p><ul class="sv-dine">{dine}</ul></div>
    </div>
  </section>

  <section class="sv-sec sv-pho" id="sv-pho" aria-labelledby="sv-pho-h">
    <div class="wrap sv-pg">
      <header class="sv-sh"><h2 id="sv-pho-h">Photographs</h2><p>Tuesday from 11:40 a.m. to 12:10 p.m. in the Business Building atrium. The photographs may appear on the CNAP website, in presentations, and in Center materials. Core directors and project leaders are also invited to take an individual photograph, or to send a current headshot.</p><a class="t3" href="index.html#ph-h">See the 2026 photographs</a><figure class="sv-phfig"><span class="im"><img src="img/reel-1.jpg" alt="Placeholder for the 2026 group photograph" loading="lazy"><span class="tag">Photo placeholder</span></span><figcaption>Everyone, at the 2026 Site Visit</figcaption></figure></header>
      <div class="sv-phw"><p class="sv-ck2 sv-phh">Group photographs, in the order the photographs will be taken</p><ol class="sv-photos">{photos}</ol></div>
    </div>
  </section>

  <section class="sv-sec sv-heard" id="sv-heard" aria-labelledby="sv-heard-h">
    <div class="wrap">
      <header class="sv-sh"><h2 id="sv-heard-h">Last year’s feedback</h2><p>Twenty-three attendees, about half of those present, answered the survey after the 2026 Site Visit.</p></header>
      <div class="sv-fb"><div class="sv-fbb"><p class="sv-ck2">By the numbers</p><ul class="sv-nums sv-hstats2" aria-label="Survey results"><li><b class="num">100%</b><span>rated the overall experience excellent or good</span></li><li><b class="num">100%</b><span>rated the timing and pacing excellent</span></li><li><b class="num">21 of 21</b><span>said there was plenty or mostly enough time for discussion</span></li><li><b class="num">9 of 9</b><span>who commented on the new two-day schedule favored the new schedule</span></li></ul></div><div class="sv-fbb"><p class="sv-ck2">In attendees’ words</p><div class="sv-fbq"><figure class="sv-fquo"><span class="sv-fqm" aria-hidden="true">“</span><blockquote><p>It gave breathing room… It gave more opportunities for networking and interacting with folks I didn’t know.</p></blockquote><figcaption>On the new two-day schedule</figcaption></figure><figure class="sv-fquo"><span class="sv-fqm" aria-hidden="true">“</span><blockquote><p>I loved the dinner at the art museum… It was nice to have time to walk around the museum and chat.</p></blockquote><figcaption>On the banquet</figcaption></figure></div></div><div class="sv-fbb"><p class="sv-ck2">What we heard, and what changes for 2027</p><ol class="sv-fbt"><li><p class="sv-fh"><span>We heard</span>Outside the survey, two attendees asked for more science and shorter administrative updates.</p><svg class="sv-fa" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M14 7l5 5-5 5"/></svg><p class="sv-fc"><span>For 2027</span>More time for research, including methods and results, and shorter administrative updates</p></li><li><p class="sv-fh"><span>We heard</span>Several said the poster session felt short for the number of posters.</p><svg class="sv-fa" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M14 7l5 5-5 5"/></svg><p class="sv-fc"><span>For 2027</span>A longer poster session, with a break after the final talk</p></li><li><p class="sv-fh"><span>We heard</span>Reminder emails came unevenly, and the calendar RSVP repeated the registration.</p><svg class="sv-fa" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M14 7l5 5-5 5"/></svg><p class="sv-fc"><span>For 2027</span>Reminders spaced evenly through the spring, and one RSVP on this page</p></li><li><p class="sv-fh"><span>We heard</span>Two attendees had trouble paying at the campus parking garage.</p><svg class="sv-fa" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M14 7l5 5-5 5"/></svg><p class="sv-fc"><span>For 2027</span>Free visitor parking in a nearby lot, which the office is looking into</p></li></ol></div></div>
    </div>
  </section>

  <section class="sv-sec sv-faq" id="sv-faq" aria-labelledby="sv-faq-h">
    <div class="wrap sv-qg">
      <div><header class="sv-sh"><h2 id="sv-faq-h">Questions</h2></header><div class="sv-fqs">{faq}</div></div>
      
    </div>
  </section>
</main>
<footer class="foot"><div class="wrap"><span>Cognitive and Neurobiological Approaches to Plasticity Center, Kansas State University</span><span>Prototype. Venues, logistics, and the 2026 figures come from the Center’s 2026 planning documents. The 2027 project speakers and talk titles are fictional.</span></div></footer>
<script>
(function(){{
  var KEY='cnap-sv-role',CKK='cnap-sv-ck',role='all',done={{}};
  try{{role=localStorage.getItem(KEY)||'all';done=JSON.parse(localStorage.getItem(CKK)||'{{}}')||{{}};}}catch(e){{}}
  var NAMES={{all:'a member or guest',talk:'a speaker',poster:'a poster presenter',mentor:'a visiting mentor',core:'a core director',eac:'an advisory committee member'}};
  function setRole(r){{role=r;try{{localStorage.setItem(KEY,r);}}catch(e){{}}
    document.querySelectorAll('.sv-rb button').forEach(function(b){{b.setAttribute('aria-pressed',b.dataset.role===r);}});
    document.querySelectorAll('.sv-it').forEach(function(li){{var f=(li.dataset.for||'').split(' ');li.classList.toggle('is-you',r!=='all'&&f.indexOf(r)>-1);}});
    document.querySelector('.sv-hl-note').hidden=r==='all';
    document.querySelectorAll('[data-role]').forEach(function(el){{if(el.tagName==='BUTTON')return;el.hidden=!(el.dataset.role==='all'&&el.classList.contains('sv-ck')||el.dataset.role===r);}});
    document.querySelector('[data-rolename]').textContent=r==='all'?NAMES.all:NAMES[r]+', with the list for everyone';}}
  document.querySelectorAll('.sv-rb button').forEach(function(b){{b.addEventListener('click',function(){{setRole(b.dataset.role);}});}});
  document.querySelectorAll('[data-ck]').forEach(function(c){{c.checked=!!done[c.dataset.ck];c.addEventListener('change',function(){{done[c.dataset.ck]=c.checked;try{{localStorage.setItem(CKK,JSON.stringify(done));}}catch(e){{}}}});}});
  setRole(NAMES[role]?role:'all');
  var tabs=[].slice.call(document.querySelectorAll('.sv-days [role=tab]'));
  tabs.forEach(function(t,i){{t.addEventListener('click',function(){{tabs.forEach(function(o){{var on=o===t;o.setAttribute('aria-selected',on);document.getElementById(o.getAttribute('aria-controls')).hidden=!on;}});}});
    t.addEventListener('keydown',function(e){{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){{var n=tabs[(i+(e.key==='ArrowRight'?1:tabs.length-1))%tabs.length];n.click();n.focus();}}}});}});
  try{{var d=Math.ceil((new Date(2027,4,25)-new Date())/864e5);var el=document.querySelector('[data-days]');if(d>0)el.textContent=d;else el.parentNode.textContent=d>-2?'Happening now':'Thank you for coming';}}catch(e){{}}
  var pb=document.querySelectorAll('.sv-ask .pp-b');function closeAll(){{pb.forEach(function(o){{o.setAttribute('aria-expanded','false');document.getElementById(o.getAttribute('aria-controls')).hidden=true;}});}}
  pb.forEach(function(b){{b.addEventListener('click',function(e){{e.stopPropagation();var open=b.getAttribute('aria-expanded')==='true';closeAll();if(!open){{b.setAttribute('aria-expanded','true');document.getElementById(b.getAttribute('aria-controls')).hidden=false;}}}});}});
  document.addEventListener('click',function(e){{if(!e.target.closest('.sv-ask'))closeAll();}});document.addEventListener('keydown',function(e){{if(e.key==='Escape')closeAll();}});
  var f=document.getElementById('sv-form'),done=document.getElementById('sv-done'),sum=document.getElementById('sv-sum');
  function lab(n){{return Array.prototype.map.call(f.querySelectorAll('[name="'+n+'"]:checked'),function(i){{var b=i.nextElementSibling.querySelector('em');return b?b.textContent:i.nextElementSibling.textContent;}});}}
  function att(){{return (f.querySelector('[name=att]:checked')||{{}}).value;}}
  function syncAtt(){{var v=att();f.querySelectorAll('[data-show]').forEach(function(el){{el.hidden=el.getAttribute('data-show').split(' ').indexOf(v)<0;}});}}
  f.addEventListener('change',function(e){{if(e.target.name==='att')syncAtt();if(e.target.name==='meal'){{var n=f.querySelector('[name=meal][value=neither]');if(e.target===n&&n.checked)f.querySelectorAll('[name=meal]:not([value=neither])').forEach(function(x){{x.checked=false;}});else if(e.target!==n&&e.target.checked)n.checked=false;}}}});syncAtt();
  var pp=document.getElementById('sv-pp'),pf=document.getElementById('sv-pfields'),plh=document.getElementById('sv-pl-hint'),wc=document.getElementById('sv-wc'),pabs=f.querySelector('[name=pabs]');
  function syncPoster(){{var v=(f.querySelector('[name=poster]:checked')||{{}}).value,a=att();pp.hidden=!(v==='yes'&&a!=='no');var n=(f.querySelector('[name=pnow]:checked')||{{}}).value;pf.hidden=n!=='now';plh.hidden=n!=='later';}}
  f.addEventListener('change',function(e){{if(e.target.name==='poster'||e.target.name==='pnow'||e.target.name==='att')syncPoster();}});syncPoster();
  pabs.addEventListener('input',function(){{var n=(pabs.value.trim().match(/\\S+/g)||[]).length;wc.textContent=n+' of 150 words';wc.classList.toggle('over',n>150);}});
  function ics(){{var Z=function(d,a,b,t){{return 'BEGIN:VEVENT\\r\\nUID:cnap-sv-2027-'+d+'@ksu.edu\\r\\nDTSTAMP:20261115T000000Z\\r\\nDTSTART:'+a+'\\r\\nDTEND:'+b+'\\r\\nSUMMARY:'+t+'\\r\\nLOCATION:Kansas State University\\\\, Manhattan\\\\, Kansas\\r\\nDESCRIPTION:The detailed schedule follows in the weeks before the visit. Questions: mkwills@ksu.edu\\r\\nBEGIN:VALARM\\r\\nTRIGGER:-P1D\\r\\nACTION:DISPLAY\\r\\nDESCRIPTION:CNAP Site Visit tomorrow\\r\\nEND:VALARM\\r\\nEND:VEVENT\\r\\n';}};
    return 'BEGIN:VCALENDAR\\r\\nVERSION:2.0\\r\\nPRODID:-//CNAP//Site Visit//EN\\r\\n'+Z(1,'20270525T134000Z','20270526T020000Z','CNAP Site Visit, day 1')+Z(2,'20270526T134000Z','20270526T173000Z','CNAP Site Visit, day 2')+'END:VCALENDAR\\r\\n';}}
  document.getElementById('sv-ics').addEventListener('click',function(){{var b=this,data=ics();
    function fallback(){{window.open('https://outlook.office.com/calendar/0/deeplink/compose?subject=CNAP%20Site%20Visit&startdt=2027-05-25&enddt=2027-05-27&allday=true','_blank','noopener');}}
    if(window.claude&&claude.use){{claude.use('downloads').then(function(d){{if(!d)return fallback();d.save({{filename:'CNAP-Site-Visit-2027.ics',data:data}}).catch(function(){{}});}});}}
    else{{try{{var u=URL.createObjectURL(new Blob([data],{{type:'text/calendar'}}));var a=document.createElement('a');a.href=u;a.download='CNAP-Site-Visit-2027.ics';document.body.appendChild(a);a.click();a.remove();}}catch(e){{fallback();}}}}}});
  f.addEventListener('submit',function(e){{e.preventDefault();var v=att();var rows=[['Attending',lab('att').join('')]];
    if(v==='person'){{var d=f.querySelector('[name=diet]').value.trim();rows.push(['Parts you plan to attend',lab('part').join(String.fromCharCode(10))||'None selected'],['Meals',lab('meal').join(String.fromCharCode(10))||'None selected'],['Dietary restrictions',d||'None'],['Photographs and video',lab('photo').join('')||'No answer'],['Parking',lab('park').join('')||'No answer'],['Hotel room',lab('stay').join(', ')||'Not needed']);}}
    if(v!=='no'){{var t=f.querySelector('[name=tag]').value.trim();rows.push(['Poster session',lab('poster').join('')||'No answer']);if(!pp.hidden&&!pf.hidden){{var g=function(n){{return f.querySelector('[name='+n+']').value.trim()||'Not entered';}};var wn=(pabs.value.trim().match(/\\S+/g)||[]).length;rows.push(['Poster title',g('ptitle')],['Authors',g('pauth')],['Affiliation',g('paff')],['Abstract',wn?wn+' words':'Not entered']);}}rows.push(['Name tag',t||'Amara']);}}
    rows.push(['Connection to CNAP',f.querySelector('[name=role]').value]);
    sum.innerHTML='';rows.forEach(function(r){{var w=document.createElement('div'),t=document.createElement('dt'),dd=document.createElement('dd');t.textContent=r[0];dd.textContent=r[1];w.appendChild(t);w.appendChild(dd);sum.appendChild(w);}});
    var no=v==='no';document.getElementById('sv-calbox').hidden=no;document.getElementById('sv-sched').hidden=no;
    document.getElementById('sv-subj').textContent=no?'We’ll miss you at the 2027 CNAP Site Visit':'You’re registered for the 2027 CNAP Site Visit';
    document.getElementById('sv-lead2').textContent=no?'Thank you for letting us know. We’ll miss you this year, and we’ll share highlights after the visit.':(v==='zoom'?'Thank you for registering for the 2027 CNAP Site Visit. We look forward to having you with us on Zoom. The Zoom link comes with the detailed schedule.':'Thank you for registering for the 2027 CNAP Site Visit. We look forward to having you in Manhattan.');
    var pv=(f.querySelector('[name=poster]:checked')||{{}}).value,pn=(f.querySelector('[name=pnow]:checked')||{{}}).value;document.getElementById('sv-postr').hidden=!((pv==='yes'&&pn==='later')||pv==='later');
    f.hidden=true;done.hidden=false;done.focus();done.scrollIntoView({{block:'start'}});}});
  document.getElementById('sv-edit').addEventListener('click',function(){{done.hidden=true;f.hidden=false;f.querySelector('input').focus();}});
  document.querySelectorAll('[data-day]').forEach(function(a){{a.addEventListener('click',function(){{var t=document.getElementById('sv-t'+a.getAttribute('data-day'));if(t)t.click();}});}});
  (function(){{var els=[document.querySelector('.sv-rail'),document.querySelector('.sv-askf')],h=document.querySelector('.sv-hero');if(!h)return;function f(){{var t=Math.max(124,h.getBoundingClientRect().bottom+32);els.forEach(function(e){{if(!e)return;var lim=innerHeight-e.offsetHeight-84;e.style.top=Math.max(Math.min(t,lim),Math.min(124,lim))+'px';}});}}addEventListener('scroll',f,{{passive:true}});addEventListener('resize',f);f();}})();
  try{{if('scrollRestoration' in history)history.scrollRestoration='manual';}}catch(e){{}}
  function svTop(){{window.scrollTo(0,0);try{{document.documentElement.scrollIntoView({{block:'start'}});}}catch(e){{}}}}
  if(location.hash){{try{{history.replaceState(null,'',location.pathname+location.search);}}catch(e){{}}}}
  svTop();addEventListener('load',function(){{svTop();setTimeout(svTop,60);}});
  function ckProg(){{var b=[].slice.call(document.querySelectorAll('.sv-ck:not([hidden]) input[type=checkbox]'));var d=b.filter(function(x){{return x.checked;}}).length;var e=document.querySelector('[data-ckdone]');if(!e)return;e.textContent=d;document.querySelector('[data-cktotal]').textContent=b.length;document.querySelector('.sv-ckpb i').style.width=(b.length?d/b.length*100:0)+'%';}}
  document.addEventListener('change',function(e){{if(e.target.closest&&e.target.closest('.sv-ck'))ckProg();}});document.addEventListener('click',function(e){{if(e.target.closest&&e.target.closest('.sv-rb'))setTimeout(ckProg,0);}});setTimeout(ckProg,0);
  (function(){{var btn=document.getElementById('sv-dk-all');if(!btn)return;
    function ev(id,a,b,t,ad){{var d=ad?';VALUE=DATE':'';return 'BEGIN:VEVENT\\r\\nUID:cnap-sv-'+id+'@ksu.edu\\r\\nDTSTAMP:20261115T000000Z\\r\\nDTSTART'+d+':'+a+'\\r\\nDTEND'+d+':'+b+'\\r\\nSUMMARY:'+t+'\\r\\nBEGIN:VALARM\\r\\nTRIGGER:-P1D\\r\\nACTION:DISPLAY\\r\\nDESCRIPTION:'+t+'\\r\\nEND:VALARM\\r\\nEND:VEVENT\\r\\n';}}
    function cal(){{return 'BEGIN:VCALENDAR\\r\\nVERSION:2.0\\r\\nPRODID:-//CNAP//Site Visit key dates//EN\\r\\n'+ev('rsvp','20270325','20270326','CNAP Site Visit: RSVP closes',1)+ev('poster','20270423','20270424','CNAP Site Visit: poster registration closes',1)+ev('d1','20270525T134000Z','20270526T020000Z','CNAP Site Visit, day 1')+ev('d2','20270526T134000Z','20270526T173000Z','CNAP Site Visit, day 2')+'END:VCALENDAR\\r\\n';}}
    btn.addEventListener('click',function(){{var data=cal();
      if(window.claude&&claude.use){{claude.use('downloads').then(function(d){{if(d)d.save({{filename:'CNAP-Site-Visit-2027-key-dates.ics',data:data}}).catch(function(){{}});}});}}
      else{{try{{var u=URL.createObjectURL(new Blob([data],{{type:'text/calendar'}}));var a=document.createElement('a');a.href=u;a.download='CNAP-Site-Visit-2027-key-dates.ics';document.body.appendChild(a);a.click();a.remove();}}catch(e){{}}}}}});}})();
  var sp=document.querySelector('.sv-rail'),links=[].slice.call(sp.querySelectorAll('ol a')),secs=links.map(function(a){{return document.querySelector(a.getAttribute('href'));}}),tr=sp.querySelector('.spine-track'),fl=sp.querySelector('.spine-fill'),ol=sp.querySelector('ol');
  function spy(){{var y=innerHeight*.35,k=-1;secs.forEach(function(s,i){{if(s.getBoundingClientRect().top<y)k=i;}});links.forEach(function(a,i){{if(i===k)a.setAttribute('aria-current','step');else a.removeAttribute('aria-current');a.classList.toggle('done',i<k);}});sp.classList.toggle('on',k>-1);}}
  function track(){{if(!tr||getComputedStyle(tr).display==='none')return;var o=ol.getBoundingClientRect().top;function dot(a){{return a.getBoundingClientRect().top-o+parseFloat(getComputedStyle(a,'::before').top)+5;}}var t=dot(links[0]),b=dot(links[links.length-1]);tr.style.top=(ol.offsetTop+t)+'px';tr.style.height=(b-t)+'px';var c=sp.querySelector('a[aria-current]');fl.style.height=c?(dot(c)-t)+'px':'0px';}}
  addEventListener('scroll',function(){{spy();track();}},{{passive:true}});addEventListener('resize',track);['mouseenter','mouseleave','focusin','focusout','transitionend'].forEach(function(e){{sp.addEventListener(e,function(){{requestAnimationFrame(track);setTimeout(track,280);}});}});spy();track();
  if('IntersectionObserver' in window){{document.documentElement.classList.add('sv-js');var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{e.target.classList.add('in');io.unobserve(e.target);}}}});}},{{rootMargin:'0px 0px -20% 0px'}});document.querySelectorAll('.sv-route,.sv-sh').forEach(function(el){{io.observe(el);}});}}
}})();
</script>
<script src="hubchrome.js" defer></script>
</body>
</html>
'''
open(V+'sitevisit.html','w').write(page)
print('ok')
