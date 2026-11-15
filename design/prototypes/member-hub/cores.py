import re,sys
sys.path.insert(0,'/tmp/claude-0/hubproto/gen')
from mail import *
V='/tmp/claude-0/hubproto/v4/'
mentor=open(V+'mentor.html').read()
hdr=mentor[mentor.index('<a class="skip"'):mentor.index('<main id="main">')]
hdr=hdr.replace('<a class="mywork" href="index.html#wk">My work <span class="count">2</span></a><span class="avatar" aria-label="Dr. Elena Voss">EV</span>','<a class="mywork" href="index.html#wk">My work <span class="count">4</span></a><span class="avatar" aria-label="Dr. Amara Okafor">AO</span>')
hdr=hdr.replace('<a href="index.html#cores-h">Resources</a>','<a href="index.html#cores-h" aria-current="page">Resources</a>')

def page(code,cls,title,name,mission,facts,actions,sections,contact_note,rail=''):
    nav=''.join(f'<li><a href="#{sid}"><span class="n"><b>{i+1}</b></span><span>{lab}</span></a></li>' for i,(sid,lab,_) in enumerate(sections))
    secs=''.join(f'''
        <section class="step cs" id="{sid}" aria-labelledby="{sid}-h">
          <h2 id="{sid}-h">{lab}</h2>
          <div class="cs-b">{body}</div>
        </section>''' for sid,lab,body in sections)
    fx=''.join(f'<li><b class="num">{a}</b><span>{b}</span></li>' for a,b in facts)
    others=[('ni','NI','Neuroinformatics Core'),('cn','CN','Cognitive Neuroscience Core'),('bn','BN','Behavioral Neuroscience Core')]
    oth=''.join(f'<a class="co-o co-{c}" href="core-{c}.html"><span class="co-ol">{k}</span><span>{n}</span></a>' for c,k,n in others if c!=cls)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title} · CNAP Member Hub</title>
<link rel="stylesheet" href="guide.css">
</head>
<body data-guide="core-{cls}" class="core-page co-{cls}">
{hdr}<main id="main">
  <section class="co-open" aria-labelledby="t">
    <div class="wrap">
      <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><a href="index.html#cores-h">Research cores</a><span aria-hidden="true">/</span><span aria-current="page">{name}</span></nav>
      <div class="co-hero">
        <span class="co-mono" aria-hidden="true">{code}</span>
        <div class="co-hd">
          <p class="for">Research core</p>
          <h1 id="t">{name}</h1>
          <p class="lead">{mission}</p>
          <div class="co-act">{actions}</div>
        </div>
      </div>
      <ul class="co-facts" aria-label="At a glance">{fx}</ul>
    </div>
  </section>

  <div class="guide">
    <div class="wrap">
      <nav class="spine" aria-label="Sections on this page">
        <p class="spine-h">On this page</p><div class="spine-track" aria-hidden="true"><span class="spine-fill"></span></div>
        <ol>{nav}</ol>
      </nav>
      <div class="steps">{secs}
        <aside class="co-more" aria-label="The other cores"><p>The other research cores</p><div>{oth}</div></aside>
      </div>
      <aside class="co-rail" aria-label="Contact the core">{rail}</aside>
    </div>
  </div>
</main>

<footer class="foot"><div class="wrap"><span>Cognitive and Neurobiological Approaches to Plasticity Center, Kansas State University</span><span>{contact_note}</span></div></footer>
<script src="guide.js"></script>
</body>
</html>
'''

def ul(items,cls='dots'): return f'<ul class="{cls}">'+''.join(f'<li>{x}</li>' for x in items)+'</ul>'
def tiles(items): return '<ul class="co-tiles">'+''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a,b in items)+'</ul>'
def chips(items): return '<p class="co-chips">'+''.join(f'<span>{x}</span>' for x in items)+'</p>'
def spec(items): return '<dl class="co-spec">'+''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a,b in items)+'</dl>'
def person(ini,role,nm,desc,mail=None):
    m=f'<a href="mailto:{mail}">{mail}</a>' if mail else ''
    return f'<li><span class="who-ini" aria-hidden="true">{ini}</span><div><p class="pp-r">{role}</p><p class="co-pn">{nm}</p>{m}<p class="co-pd">{desc}</p></div></li>'
def how(steps): return '<ol class="co-how">'+''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a,b in steps)+'</ol>'

def rail(role,nm,mail,loc,primary,web=''):
    return f'''<div class="co-rc"><p class="co-rk">Contact</p><p class="pp-r">{role}</p><p class="co-pn">{nm}</p><a class="co-re" href="mailto:{mail}">{mail}</a>
<dl class="co-rd"><div><dt>Location</dt><dd>{loc}</dd></div><div><dt>On the CNAP website</dt><dd><a href="{web}" target="_blank" rel="noopener">Core page</a></dd></div></dl></div>'''

fee='<p class="co-fee"><span><b>Schedule of charges</b> Rates for core services will be posted here.</span><span class="core-soon">Coming soon</span></p>'
connect='''<div class="co-cx"><div><p class="for">A separate facility, with support from two cores</p><p class="co-cx-n">Cog + Neuro Network for Experimentation and Computing Technologies. A staffed drop-in room, BH 444, with four workstations for R, MATLAB, Python, JMP, PsychoPy, Unity, and more.</p></div>
<div class="co-cx-g"><div><b>Experiment assistance</b><span>Through the Cognitive Neuroscience Core: experiment programming and design consultation, hardware integration with EEG, TMS, eye tracking, and response devices, help adapting existing scripts, and shared experiment code and templates.</span></div><div><b>Data assistance</b><span>Through the Neuroinformatics Core: data pipelines and analysis consultation, workflows for large-scale and parallel analysis on Beocat, machine learning help, and workshops on analysis tools and methods.</span></div></div>
<a class="btn" href="https://connect-lab.carrd.co" target="_blank" rel="noopener">Visit the CONNECT Lab</a></div>'''
def actions(primary,req,con,conlab='Book a consultation'):
    return f'<a class="btn pri" href="{req}">{primary}</a><a class="btn" href="{con}">{conlab}</a><a class="t3" href="#work">How to work with the core</a>'

# ---------- NI ----------
bars='''<div class="co-bars" role="list">
<div class="co-bar" role="listitem"><p><b>Electroencephalography (EEG) analysis</b><span>1,280 hours before, about 20 hours on Beocat</span></p><div class="co-tr"><i class="was" style="--w:100%"></i></div><div class="co-tr"><i class="now" style="--w:1.6%"></i></div></div>
<div class="co-bar" role="listitem"><p><b>Bayesian simulations</b><span>More than 1,000 hours before, about 8 hours on Beocat</span></p><div class="co-tr"><i class="was" style="--w:78%"></i></div><div class="co-tr"><i class="now" style="--w:.7%"></i></div></div>
<div class="co-bar" role="listitem"><p><b>Image processing</b><span>Days of processing reduced to hours</span></p></div>
</div><p class="co-key"><span class="k-was"></span>Before <span class="k-now"></span>On Beocat with the Neuroinformatics Core</p>'''
ni=page('NI','ni','Neuroinformatics Core','Neuroinformatics Core',
 'Advanced computing, data science, and artificial intelligence (AI) support for CNAP, enabling data-driven neuroscience through high-performance computing and machine learning.',
 [('496','Processor cores for CNAP on Beocat'),('10','Graphics processing units (GPUs)'),('3.4 TB','Memory (RAM)'),('882,000+','Core hours run for CNAP in Grant Year 9')],
 actions('Request analysis',NI_REQ,NI_CON),
 [('ni-svc','Services',ul(['Research computing and high-performance computing (HPC) support','Machine learning and data science assistance','Data analysis and statistics, including data processing and analysis support','Custom scripting for data import, cleaning, and analysis','Research software, workflow development, and automation','Secure data transfer and collaboration','Hands-on training and one-on-one consultation'])+fee),
  ('ni-inf','Computing infrastructure','<p>The core is integrated with Beocat, the Kansas State University high-performance computing cluster in the Carl R. Ice College of Engineering.</p>'+spec([('Beocat cluster','More than 10,000 shared compute cores'),('Dedicated to CNAP','496 cores, 10 GPUs, and 3.4 terabytes (TB) of memory'),('Storage','3 petabytes (PB) of primary storage and 290 TB of high-speed storage'),('Access','Open OnDemand and Jupyter, with secure data transfer')])),
  ('ni-imp','Time saved on Beocat',bars+'<p class="meta">In Grant Year 9, CNAP members ran more than 208,000 jobs and 882,000 core hours on Beocat.</p>'),
  ('ni-ai','Sample AI and machine learning projects',tiles([('AI for behavior analysis','Automated scoring of novel object recognition and social interaction tests'),('Large language models for cognitive health','Language models applied to mild cognitive impairment and recall'),('Prompt optimization','Optimizing prompts for stance detection'),('Multimodal analysis','EEG combined with behavioral data')])),
  ('ni-trn','Training and outreach',ul(['Workshops in R, Python, and machine learning','Training on Beocat, Open OnDemand, and Jupyter','Online tutorials and documentation','About 80 participants trained through outreach','Graduate courses in deep learning and databases'])),
  ('ni-out','Research outcomes in Grant Year 9','<ul class="co-facts co-facts-in">'+''.join(f'<li><b class="num">{a}</b><span>{b}</span></li>' for a,b in [('1','Funded grant'),('8','Pending grants, more than $14 million'),('14','Publications, including journal and conference papers'),('12','Conference presentations and posters')])+'</ul>'),
  ('ni-cx','CONNECT Lab',connect),
  ('ni-ppl','People','<ul class="co-ppl">'+person('DC','Core Director','Dr. Doina Caragea','Leads the core’s computing, data science, and machine learning support for CNAP investigators.','dcaragea@ksu.edu')+'</ul>'),
  ('work','Working with the core',how([('Book a consultation','Describe your data and your question. The core helps you choose an approach and estimate the computing you need.'),('Get access','The core sets up your Beocat account and secure data transfer, and points you to training if you need it.'),('Run your analysis','Work on your own with core support, or ask the core to build the pipeline with you.'),('Cite the core','Acknowledge CNAP and the Neuroinformatics Core in publications and presentations that used its resources.')])+'<p class="meta">Questions about the Neuroinformatics Core go to <a href="mailto:dcaragea@ksu.edu">dcaragea@ksu.edu</a>.<br>General questions go to <a href="mailto:cnap@ksu.edu">cnap@ksu.edu</a>.<br><a href="https://www.k-state.edu/cnap/research-cores/ni-core.html" target="_blank" rel="noopener">The Neuroinformatics Core on the CNAP website</a></p>')],
 'Prototype. Request and booking forms are not connected yet.',rail('Core Director','Dr. Doina Caragea','dcaragea@ksu.edu','Beocat, Carl R. Ice College of Engineering','Request analysis','https://www.k-state.edu/cnap/research-cores/ni-core.html'))

# ---------- CN ----------
cn=page('CN','cn','Cognitive Neuroscience Core','Cognitive Neuroscience Core',
 'Human neuroscience, electroencephalography (EEG), and brain stimulation support for CNAP. The only COBRE-funded cognitive neuroscience and EEG core in Kansas.',
 [('6','Geodesic Sensor Nets, 64 channels each'),('16','Channels on each mobile OpenBCI system'),('About 15 min','To set up a Hydrocel net'),('TMS and rTMS','Combined with EEG in Phase 2')],
 actions('Request instrument time',CN_REQ,CN_CON),
 [('cn-fac','Facilities','<p>Fully equipped, research-ready spaces for human neuroscience studies.</p>'+tiles([('EEG recording rooms','Dedicated rooms for EEG recording and experimental testing'),('Controlled environments','Spaces for cognitive and behavioral experimentation'),('Participant spaces','Preparation and data collection areas'),('Technical support areas','Data processing and equipment setup'),('Coordination space','Offices for study design and analysis support'),('CONNECT Lab','Experiment programming and technical development, integrating experiments with EEG, transcranial magnetic stimulation (TMS), eye tracking, and response devices')])),
  ('cn-cap','Research capabilities',chips(['EEG during cognitive tasks','Event-related potentials (ERP)','Visual cognition','Attention','Eye-movement paradigms','Sensorimotor processing','Electromyography (EMG)','Manipulation of cognitive and perceptual processes','TMS and repetitive TMS (rTMS) with EEG, Phase 2'])),
  ('cn-eq','Equipment and technology','''<div class="co-eq">
<article><p class="pr-t">Primary EEG system</p><h3>Electrical Geodesics, Inc. (EGI) EEG systems</h3><p>Six 64-channel Geodesic Sensor Nets (GSN) with full-head coverage across the scalp, face, and neck. Hydrocel nets allow rapid setup, about 15 minutes, supporting efficient experimental throughput.</p>'''+spec([('Amplifiers','One Net Amps 400, the main amplifier, and one Net Amps 300'),('Software','Net Station 5 for acquisition and analysis'),('Data','MFF format, exported to EDF+, MATLAB, EEGLAB, FieldTrip, or custom pipelines')])+'''</article>
<article><p class="pr-t">Mobile and wireless EEG</p><h3>OpenBCI systems</h3><p>Portable systems with small, medium, and large EEG caps and Cyton and Daisy biosensing boards in a 16-channel configuration. They record EEG and EMG and transmit wirelessly.</p>'''+spec([('Transmission','Radio frequency or Bluetooth Low Energy'),('Sampling','125 hertz (Hz) per channel'),('Software','MATLAB, EEGLAB, FieldTrip, ERPLAB, OpenViBE, Lab Streaming Layer (LSL), BrainBay, and BioEra')])+'''</article>
<article><p class="pr-t">Phase 2</p><h3>Transcranial magnetic stimulation (TMS) and repetitive TMS (rTMS)</h3><p>Integrated with EEG, these systems will enable causal manipulation of neural activity, so researchers can directly test the role of specific brain regions in cognitive processes and strengthen translational neuroscience applications.</p></article>
</div>'''),
  ('cn-svc','Services',ul(['Study design consultation and methodological guidance','Experimental programming, setup, and troubleshooting','EEG data collection assistance and session support','Pre-collection validation: IRB approval verification, timing tests, and system checks','Coordination of equipment readiness and technical troubleshooting','Future support for TMS and rTMS experimental design and safety workflows'])+'<p class="meta">Custom scripting and data analysis support are offered through the <a href="core-ni.html">Neuroinformatics Core</a>.</p>'+fee),
  ('cn-cx','CONNECT Lab',connect),
  ('cn-imp','Impact',ul(['Enables advanced human cognitive neuroscience research at scale','Provides centralized EEG and neuroimaging infrastructure for CNAP investigators','Strengthens methodological rigor and reproducibility in cognitive neuroscience studies','Expands experimental capabilities by integrating EEG with brain stimulation','Strengthens competitiveness for extramural funding in cognitive and translational neuroscience'])),
  ('cn-ppl','People','<ul class="co-ppl">'+person('LL','Senior Advisor','Dr. Lester Loschky','Professor of Cognitive Psychology. Expert in visual cognition, attention, and eye-movement research. He has played a central role in the core’s development since its inception and guides its operations and research direction.')+person('JH','Scientific Advisor','Dr. Julio C. Hernandez-Pavon','Assistant Professor of Human Neuroscience, Department of Psychological Sciences. Expert in brain stimulation, EEG, neuroimaging, and signal processing. His research focuses on brain connectivity, neuroplasticity, and stimulation-based approaches for motor, language, and neurological disorders, including stroke and Parkinson’s disease.')+'</ul>'),
  ('work','Working with the core',how([('Book a consultation','Talk through your study design and which system fits your question.'),('Confirm approvals','The core verifies your Institutional Review Board (IRB) approval before any data collection.'),('Validate your setup','Timing tests and system checks are run with you before your first participant.'),('Collect your data','Schedule sessions, with core support for setup and troubleshooting.')])+'<p class="meta">Questions about the Cognitive Neuroscience Core go to <a href="mailto:cnap@ksu.edu">cnap@ksu.edu</a>.<br><a href="https://www.k-state.edu/cnap/research-cores/cn-core.html" target="_blank" rel="noopener">The Cognitive Neuroscience Core on the CNAP website</a></p>')],
 'Prototype. Request and booking forms are not connected yet.',rail('Cognitive Neuroscience Core','CNAP team','cnap@ksu.edu','Department of Psychological Sciences','Request instrument time','https://www.k-state.edu/cnap/research-cores/cn-core.html'))

# ---------- BN ----------
bn=page('BN','bn','Behavioral Neuroscience Core','Behavioral Neuroscience Core',
 'Behavioral research, animal models, and experimental neuroscience support for CNAP. Built in 1981, the only dedicated multi-user behavioral neuroscience facility in psychology in Kansas.',
 [('51','Rooms'),('7,300+','Net assignable square feet'),('1981','Year the facility was built'),('Phase 2','Electrophysiology and optogenetics planned')],
 actions('Request instrument time',BN_REQ,BN_CON,'Book a consultation or tour'),
 [('bn-fac','Facilities',tiles([('Colony rooms','Purpose-built rooms for small animals such as rodents and birds, with special housing for altered light and dark cycles, special populations, and breeding'),('Procedure rooms','Behavioral testing'),('Surgery and wet laboratory','Space for surgical and laboratory procedures'),('Cage wash and storage','In-house cage washer and laundry facility'),('Offices and meeting room','In a separate block from the animal areas')])),
  ('bn-as','Assays and techniques',chips(['Pavlovian paradigms','Instrumental paradigms','Drug self-administration','Locomotor behavior','Open field search and navigation','Ultrasonic vocalization recordings','Forced swim tests'])),
  ('bn-eq','Equipment','<p>Added since Phase 1 of the CNAP grant, with upgrades continuing under Phase 2.</p>'+spec([('Surgery','Two dual-arm stereotaxic instruments with microinfusion pumps, two isoflurane rigs, two procedure hoods, downdraft surgical tables, and four heat pumps for recovery'),('Imaging','Fluorescence microscope, co-funded by the Kansas IDeA Network of Biomedical Research Excellence (K-INBRE)'),('Storage and preparation','Research-grade refrigerator, −20°C freezer, two −80°C freezers, large autoclave, ice machine, and reverse osmosis and deionized water'),('Analysis','Blood alcohol analyzer'),('Husbandry','In-house cage washer and laundry facility')])+'<p class="meta">Planned for Phase 2: shared equipment for electrophysiological recording and optogenetic manipulation.</p>'),
  ('bn-svc','Services',ul(['Design and running of behavioral assays','Surgical and laboratory procedure support, including stereotaxic surgery','Animal care and husbandry, including cage changes and cage washing','Scheduling of all facility spaces and equipment, and equipment maintenance','Facility records for compliance reporting','Coordination with the Comparative Medicine Group, the Institutional Animal Care and Use Committee (IACUC), and the Division of Facilities','Training and onboarding for new students and staff'])+fee),
  ('bn-ppl','People','<ul class="co-ppl">'+person('CP','Core Director','Dr. Charles Pickens','Associate Professor, Department of Psychological Sciences, and IACUC member. About 20 years of research with rats and mice, including reinforcer devaluation, fear conditioning and punishment learning, alcohol consumption and exposure, intracranial lesion and infusion surgery, and immunohistochemistry. He oversees operations and supervises staff.')+person('CC','Animal Care Technician','Cameron Carr-Thompson','Handles husbandry, daily room checks, and IACUC and AAALAC records, trains new students and staff, and arranges equipment maintenance.')+person('AD','Assistant Director','Assistant Director','Orders supplies, maintains inventory, and arranges maintenance of equipment and shared spaces.')+'</ul>'),
  ('work','Working with the core',how([('Schedule a tour','See the colony, procedure, and surgery rooms, and talk through your study with the Core Director.'),('Confirm approvals','Your IACUC protocol must be approved before animals arrive or procedures begin.'),('Complete training','The Animal Care Technician trains new students and staff on facility procedures.'),('Book space and equipment','The core schedules rooms and equipment for your study.')])+'<p class="meta">For facilities, services, or a tour, contact the Core Director through <a href="mailto:cnap@ksu.edu">cnap@ksu.edu</a>.<br><a href="https://www.k-state.edu/cnap/research-cores/bn-core.html" target="_blank" rel="noopener">The Behavioral Neuroscience Core on the CNAP website</a></p>')],
 'Prototype. Request and booking forms are not connected yet.',rail('Core Director','Dr. Charles Pickens','cnap@ksu.edu','Department of Psychological Sciences','Request instrument time','https://www.k-state.edu/cnap/research-cores/bn-core.html'))

for c,h in [('ni',ni),('cn',cn),('bn',bn)]: open(V+f'core-{c}.html','w').write(h)
print('ok')
