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
 'all':['RSVP for lunch and the banquet, and note any dietary needs','Say whether you’re comfortable being photographed','Add both days to your calendar','Read the program, the map, and the questions below','Pack comfortable walking shoes, layers, and an umbrella'],
 'talk':['Plan for 17 minutes. The other 3 minutes of your 20-minute slot are for changing speakers.','Email your slides to Morgan Wills the day before the visit','Arrive a few minutes early to load your slides and check the projector','Stay for the discussion that follows your talk'],
 'poster':['Confirm your entry in the poster booklet when Morgan Wills sends it','Print your poster no larger than 60 by 40 inches','Look for your poster number and hallway map, sent in advance','Hang your poster on Tuesday between 2:30 and 6:00 p.m. on the fourth floor of Bluemont Hall','Stand by your poster from 11:30 a.m. on Wednesday'],
 'mentor':['You aren’t asked to present, but your questions during each discussion are valuable','Your room at the Bluemont Hotel is booked for Monday and Tuesday nights','Arrange a ride with your mentee if you’d rather not use a rideshare','Keep your travel receipts and email them to Roxana Ortiz'],
 'core':['Prepare a 17-minute core update','Plan your stops for the guided tours','Attend the closed advisory committee meeting at 2:45 p.m. on Tuesday','Take an individual photograph, or send a current headshot'],
 'eac':['Read the meeting agenda below before Tuesday','Attend the closed meeting at 2:45 p.m. on Tuesday in Bluemont Hall, Room 106','Your room at the Bluemont Hotel is booked for Monday and Tuesday nights','Keep your travel receipts and email them to Roxana Ortiz']}
ck=''.join(f'''<ul class="sv-ck" data-role="{k}"{'' if k=='all' else ' hidden'}>{''.join(f'<li><label><input type="checkbox" data-ck="{k}{i}"><span>{x}</span></label></li>' for i,x in enumerate(v))}</ul>''' for k,v in CK.items())
roles=''.join(f'<button type="button" aria-pressed="{"true" if k=="all" else "false"}" data-role="{k}">{l}</button>' for k,l in ROLES)

FAQ=[('I’m not presenting. Do I need to prepare?','No. Reading the program, the map, and these questions is enough. The Center looks forward to the perspectives you bring to each discussion.'),
 ('Where do I park?','Out-of-town guests park free at the Bluemont Hotel, and every venue is within walking distance. In-town guests can buy a $6 daily permit for the Union Parking Garage through the parking app, since street parking isn’t allowed before 9:00 a.m. Parking on campus is free after 5:00 p.m., so the banquet is easy.'),
 ('Can I get a ride?','Uber and other rideshares run in Manhattan, but cars can be scarce. Book ahead and allow extra time, or arrange a ride with your CNAP mentee.'),
 ('What will the weather be like?','Late May is usually mild: highs in the mid-70s to low 80s, evenings in the upper 50s to low 60s, and a chance of an afternoon thunderstorm. Rooms can be cool, so bring layers, a light jacket, and an umbrella.'),
 ('Is there Wi-Fi?','Yes. Guests from outside K-State can join the “KSU Guest” network.'),
 ('Can I join online?','Yes. Every session, including the keynote, has a Zoom option. The link comes in your confirmation email.'),
 ('What about meals?','Breakfast is at the hotel and at the Business Building each morning. Tuesday lunch is a boxed lunch for everyone who RSVPs, labeled for dietary needs. Wednesday lunch is informal: plenty of colleagues head out together after the poster session.'),
 ('How are photographs used?','Group photographs may appear on the CNAP website, in presentations, and in Center materials. You chose your photography preference when you RSVPed, and Morgan Wills can change it for you.'),
 ('How do I get reimbursed for travel?','Keep your receipts and email them to Roxana Ortiz after the visit. Lodging, hotel parking, and breakfast are already covered, so you won’t be charged for those.')]
faq=''.join(f'<details class="sv-fq"><summary>{q}</summary><p>{a}</p></details>' for q,a in FAQ)

PHOTOS=['Everyone','The Behavioral Neuroscience Core','The Cognitive Neuroscience Core','The Neuroinformatics Core','The Administrative Core','Primary project award recipients','Pilot project award recipients','The External Advisory Committee','All graduate students']
photos=''.join(f'<li><span class="num">{i}</span>{p}</li>' for i,p in enumerate(PHOTOS,1))
DINE=[('The Chef Café','Breakfast and lunch from a local kitchen'),('Bluestem Bistro','Coffee, sandwiches, and light lunches'),('So Long Saloon','Burgers and regional cooking'),('Tallgrass Taphouse','Pub-style dining'),('Liquid Art Winery and Estate','A winery with a restaurant. Call ahead.')]
dine=''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a,b in DINE)

ven=''.join(f'''<li class="sv-v sv-v-{k}"><span class="sv-vn num" aria-hidden="true">{i}</span><div><p class="sv-vt">{v[0]}</p><p class="sv-va">{v[1]}, Manhattan, Kansas</p><p class="sv-vd">{v[2]}</p><a class="t3" href="{v[3]}" target="_blank" rel="noopener">Walking directions</a></div></li>''' for i,(k,v) in enumerate(VEN.items(),1))

GCAL='https://calendar.google.com/calendar/render?action=TEMPLATE&amp;text='+quote('CNAP Site Visit')+'&amp;dates=20270525/20270527&amp;details='+quote('The 2027 CNAP Site Visit, Kansas State University. Program: the Site Visit page in the Member Hub.')+'&amp;location='+quote('Kansas State University, Manhattan, Kansas')
OCAL='https://outlook.office.com/calendar/0/deeplink/compose?subject='+quote('CNAP Site Visit')+'&amp;startdt=2027-05-25&amp;enddt=2027-05-27&amp;allday=true&amp;location='+quote('Kansas State University, Manhattan, Kansas')
ASK=mt('mkwills@ksu.edu','Site Visit question','\n'.join(['Name:','','My question:','']))
RCPT=mt('roxana@ksu.edu','Site Visit travel receipts','\n'.join(['Name:','','Receipts attached for:','']))

SECS=[('sv-why','Why it matters'),('sv-prog','The program'),('sv-eve','The evening'),('sv-map','Getting around'),('sv-you','Your checklist'),('sv-stay','Travel and stay'),('sv-food','Food'),('sv-pho','Photographs'),('sv-faq','Questions')]
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
  <nav class="spine sv-rail" aria-label="Sections on this page"><p class="spine-h">On this page</p><div class="spine-track" aria-hidden="true"><span class="spine-fill"></span></div><ol>{spine}</ol></nav>

  <section class="sv-hero" aria-labelledby="t">
    <div class="wrap">
      <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><a href="events.html">Events</a><span aria-hidden="true">/</span><span aria-current="page">The 2027 Site Visit</span></nav>
      <div class="sv-hg">
        <div class="sv-hd">
          <p class="for">Kansas State University · Manhattan, Kansas</p>
          <h1 id="t">The 2027 CNAP Site Visit</h1>
          <p class="sv-lead">Two days with the people behind the Center’s science: core tours, project talks, an evening at the Beach Museum, and a poster session that fills the halls of Bluemont Hall.</p>
          <div class="sv-act"><a class="btn pri" href="#sv-prog">See the program</a><span class="sv-cal">Add to <a href="{GCAL}" target="_blank" rel="noopener">Google Calendar</a> or <a href="{OCAL}" target="_blank" rel="noopener">Outlook</a></span></div>
        </div>
        <div class="sv-date" aria-label="Tuesday, May 25, and Wednesday, May 26, 2027">
          <p class="sv-mo">May 2027</p>
          <p class="sv-dd"><span><b>25</b><small>Tuesday</small></span><i aria-hidden="true"></i><span><b>26</b><small>Wednesday</small></span></p>
          <p class="sv-cd"><b class="num" data-days>192</b> days to go</p>
        </div>
      </div>
      <div class="sv-role" role="group" aria-labelledby="role-l"><p id="role-l">I’m coming as</p><div class="sv-rb">{roles}</div></div>
    </div>
  </section>

  <section class="sv-sec sv-why" id="sv-why" aria-labelledby="sv-why-h">
    <div class="wrap">
      <header class="sv-sh"><h2 id="sv-why-h">Why it matters</h2><p>The Site Visit is where the External Advisory Committee sees the Center’s year firsthand. For everyone else, it’s the one time each year the whole Center is in one place.</p></header>
      <div class="sv-three">
        <article><p class="sv-n num">01</p><h3>Stronger together</h3><p>Mentors, project leaders, core staff, and students meet in person, and the conversations started here often become collaborations.</p></article>
        <article><p class="sv-n num">02</p><h3>Science up close</h3><p>Hear where each project and core stands, walk through the labs, and see the work of two dozen students and trainees on the poster walls.</p></article>
        <article><p class="sv-n num">03</p><h3>The next generation</h3><p>Graduate students present alongside faculty, and the feedback from visiting experts shapes the projects that follow.</p></article>
      </div>
      <ul class="sv-nums" aria-label="The 2026 Site Visit in numbers"><li><b class="num">56</b><span>Attendees in 2026</span></li><li><b class="num">24</b><span>Posters</span></li><li><b class="num">9</b><span>Speakers, including the keynote</span></li><li><b class="num">3</b><span>Research cores on tour</span></li><li><b class="num">4</b><span>Research and pilot projects</span></li></ul>
    </div>
  </section>

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

  <section class="sv-sec sv-map" id="sv-map" aria-labelledby="sv-map-h">
    <div class="wrap">
      <header class="sv-sh"><h2 id="sv-map-h">Getting around</h2><p>Four places, all within a 15-minute walk of the hotel. The diagram shows the walk between each one.</p></header>
      <div class="sv-mapg">
        <figure class="sv-route" aria-label="Walking times: hotel to Business Building 10 minutes, Business Building to Bluemont Hall 5 minutes, hotel to Bluemont Hall 15 minutes, hotel to the Beach Museum 5 minutes">
          <svg viewBox="0 0 560 360" aria-hidden="true">
            <path class="sv-r0" d="M110 70 C 220 70, 260 70, 300 110"/>
            <path class="sv-r1" d="M110 70 L110 180 C110 230 150 260 200 260 L440 260"/>
            <path class="sv-r2" d="M300 110 C 360 170, 420 200, 440 260"/>
            <path class="sv-r3" d="M110 70 C 60 120, 50 300, 120 320"/>
            <g class="sv-tag"><rect x="176" y="48" width="74" height="24" rx="12"/><text x="213" y="65">10 min</text></g>
            <g class="sv-tag"><rect x="354" y="160" width="64" height="24" rx="12"/><text x="386" y="177">5 min</text></g>
            <g class="sv-tag"><rect x="236" y="248" width="74" height="24" rx="12"/><text x="273" y="265">15 min</text></g>
            <g class="sv-tag"><rect x="22" y="196" width="64" height="24" rx="12"/><text x="54" y="213">5 min</text></g>
            <g class="sv-st sv-st-hotel"><circle cx="110" cy="70" r="20"/><text x="110" y="76">1</text><text class="sv-lb" x="140" y="42">Bluemont Hotel</text></g>
            <g class="sv-st sv-st-biz"><circle cx="300" cy="110" r="20"/><text x="300" y="116">2</text><text class="sv-lb" x="330" y="104">Business Building</text></g>
            <g class="sv-st sv-st-bh"><circle cx="440" cy="260" r="20"/><text x="440" y="266">3</text><text class="sv-lb" x="440" y="306" style="text-anchor:middle">Bluemont Hall</text></g>
            <g class="sv-st sv-st-mus"><circle cx="120" cy="320" r="20"/><text x="120" y="326">4</text><text class="sv-lb" x="152" y="326">Beach Museum</text></g>
          </svg>
          <figcaption>A diagram of walking times, not drawn to scale. Directional signs are posted at every venue.</figcaption>
        </figure>
        <ol class="sv-vs">{ven}</ol>
      </div>
    </div>
  </section>

  <section class="sv-sec sv-you" id="sv-you" aria-labelledby="sv-you-h">
    <div class="wrap sv-yg">
      <header class="sv-sh"><h2 id="sv-you-h">Your checklist</h2><p>Choose how you’re coming at the top of the page, and the list changes to match. Your ticks are saved in this browser.</p><p class="sv-yr">Showing the list for <b data-rolename>a member or guest</b>.</p></header>
      <div class="sv-ckw">{ck}
        <details class="sv-ag" data-role="eac" hidden><summary>The closed meeting agenda</summary><ol><li>Feedback on the year’s progress, and suggestions</li><li>Grant program updates and the administrative supplement opportunity</li><li>Core updates, staffing, and challenges</li><li>Plans for the Center’s next phase: sustainability and a stronger campus-wide presence</li></ol></details>
      </div>
    </div>
  </section>

  <section class="sv-sec sv-stay" id="sv-stay" aria-labelledby="sv-stay-h">
    <div class="wrap">
      <header class="sv-sh"><h2 id="sv-stay-h">Travel and stay</h2></header>
      <div class="sv-cards">
        <article class="sv-c sv-c-lead"><p class="sv-ck2">For out-of-town guests</p><h3>Your room is booked</h3><p>The Center reserves a room for each out-of-town guest at the Bluemont Hotel from Monday, May 24, to Wednesday, May 26. Give your first and last name at the front desk for your key.</p><dl class="sv-dl"><div><dt>Check-in</dt><dd>4:00 p.m.</dd></div><div><dt>Checkout</dt><dd>11:00 a.m.</dd></div><div><dt>Covered by the Center</dt><dd>Lodging, hotel parking, and breakfast</dd></div><div><dt>Early or late</dt><dd>Luggage storage is available. Ask the front desk about early check-in or late checkout.</dd></div></dl><p class="sv-fine">The hotel is smoke-free, and smoking in a room carries a $250 cleaning fee.</p></article>
        <article class="sv-c"><p class="sv-ck2">For K-State guests</p><h3>Parking</h3><p>Street parking isn’t allowed before 9:00 a.m. Park in the Union Parking Garage with a $6 daily permit from the parking app. Campus parking is free after 5:00 p.m.</p><a class="t3" href="https://www.k-state.edu/parking/parking/visitor.html" target="_blank" rel="noopener">Visitor parking at K-State</a></article>
        <article class="sv-c"><p class="sv-ck2">After the visit</p><h3>Travel reimbursement</h3><p>Email your receipts to Roxana Ortiz, Grant Specialist and Accountant. Lodging, hotel parking, and breakfast are already paid.</p><a class="t3" href="{RCPT}">Email Roxana</a><span class="sv-em">roxana@ksu.edu</span></article>
        <article class="sv-c"><p class="sv-ck2">What to bring</p><h3>Shoes, layers, and an umbrella</h3><p>The program moves between buildings, the rooms run cool, and late-May afternoons can bring a thunderstorm. Highs are usually in the 70s.</p></article>
      </div>
    </div>
  </section>

  <section class="sv-sec sv-food" id="sv-food" aria-labelledby="sv-food-h">
    <div class="wrap sv-fg">
      <header class="sv-sh"><h2 id="sv-food-h">Food</h2><p>Breakfast both mornings, a boxed lunch on Tuesday, and the banquet Tuesday evening. Dietary needs from your RSVP are labeled on each lunch.</p></header>
      <div class="sv-food2"><p class="sv-ck2">Wednesday lunch with colleagues</p><p>After the poster session, groups head out together. Most places open around 12:30 p.m.</p><ul class="sv-dine">{dine}</ul></div>
    </div>
  </section>

  <section class="sv-sec sv-pho" id="sv-pho" aria-labelledby="sv-pho-h">
    <div class="wrap sv-pg">
      <header class="sv-sh"><h2 id="sv-pho-h">Photographs</h2><p>Tuesday from 11:40 a.m. to 12:10 p.m. in the Business Building atrium. The photographs may appear on the CNAP website, in presentations, and in Center materials. Core directors and project leaders are also invited to take an individual photograph, or to send a current headshot.</p><a class="t3" href="index.html#ph-h">See the 2026 photographs</a></header>
      <ol class="sv-photos">{photos}</ol>
    </div>
  </section>

  <section class="sv-sec sv-faq" id="sv-faq" aria-labelledby="sv-faq-h">
    <div class="wrap sv-qg">
      <div><header class="sv-sh"><h2 id="sv-faq-h">Questions</h2></header><div class="sv-fqs">{faq}</div></div>
      <aside class="sv-who" aria-label="Who to ask">
        <p class="sv-ck2">Who to ask</p>
        <div class="sv-p"><span class="cm-av av-p" aria-hidden="true">MW</span><div><p class="sv-pn">Morgan Wills</p><p class="sv-pr">The Site Visit, RSVPs, and the program</p><a href="{ASK}">mkwills@ksu.edu</a></div></div>
        <div class="sv-p"><span class="cm-av av-t" aria-hidden="true">RO</span><div><p class="sv-pn">Roxana Ortiz</p><p class="sv-pr">Travel and reimbursement</p><a href="{RCPT}">roxana@ksu.edu</a></div></div>
        <div class="sv-p"><span class="cm-av av-a" aria-hidden="true">HB</span><div><p class="sv-pn">Heather Bailey</p><p class="sv-pr">Center Director</p><a href="mailto:hbailey@ksu.edu">hbailey@ksu.edu</a></div></div>
        <p class="sv-fine">During the visit, a phone number for help is in your confirmation email.</p>
      </aside>
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
  var sp=document.querySelector('.sv-rail'),links=[].slice.call(sp.querySelectorAll('ol a')),secs=links.map(function(a){{return document.querySelector(a.getAttribute('href'));}}),tr=sp.querySelector('.spine-track'),fl=sp.querySelector('.spine-fill'),ol=sp.querySelector('ol');
  function spy(){{var y=innerHeight*.35,k=-1;secs.forEach(function(s,i){{if(s.getBoundingClientRect().top<y)k=i;}});links.forEach(function(a,i){{if(i===k)a.setAttribute('aria-current','step');else a.removeAttribute('aria-current');a.classList.toggle('done',i<k);}});sp.classList.toggle('on',k>-1);}}
  function track(){{if(!tr||getComputedStyle(tr).display==='none')return;var o=ol.getBoundingClientRect().top;function dot(a){{return a.getBoundingClientRect().top-o+parseFloat(getComputedStyle(a,'::before').top)+5;}}var t=dot(links[0]),b=dot(links[links.length-1]);tr.style.top=(ol.offsetTop+t)+'px';tr.style.height=(b-t)+'px';var c=sp.querySelector('a[aria-current]');fl.style.height=c?(dot(c)-t)+'px':'0px';}}
  addEventListener('scroll',function(){{spy();track();}},{{passive:true}});addEventListener('resize',track);['mouseenter','mouseleave','focusin','focusout','transitionend'].forEach(function(e){{sp.addEventListener(e,function(){{requestAnimationFrame(track);setTimeout(track,280);}});}});spy();track();
  if('IntersectionObserver' in window){{document.documentElement.classList.add('sv-js');var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{e.target.classList.add('in');io.unobserve(e.target);}}}});}},{{rootMargin:'0px 0px -20% 0px'}});document.querySelectorAll('.sv-route,.sv-sh').forEach(function(el){{io.observe(el);}});}}
}})();
</script>
</body>
</html>
'''
open(V+'sitevisit.html','w').write(page)
print('ok')
