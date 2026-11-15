from urllib.parse import quote
def mt(to,subj,body,cc='cnap@ksu.edu'):
    u=f'mailto:{to}?subject={quote(subj)}&body={quote(body)}'
    if cc and cc!=to:u+=f'&cc={cc}'
    return u.replace('&','&amp;')
L='\n'
NI_REQ=mt('cnap@ksu.edu','Neuroinformatics Core: analysis request',L.join(['Name:','Department:','CNAP project or grant:','','Data (type, size, and format):','','Research question:','','Help needed (consultation, analysis pipeline, Beocat access, or training):','','Timeline or deadline:','']))
NI_CON=mt('cnap@ksu.edu','Neuroinformatics Core: consultation request',L.join(['Name:','Department:','','What I would like to discuss:','','Times that work for me:','']))
CN_REQ=mt('cnap@ksu.edu','Cognitive Neuroscience Core: instrument time request',L.join(['Name:','Department:','Study title:','IRB protocol number and approval status:','','Equipment needed (EGI EEG, OpenBCI mobile EEG, or CONNECT Lab):','','Number of sessions and preferred dates:','','Questions:','']),cc=None)
CN_CON=mt('cnap@ksu.edu','Cognitive Neuroscience Core: consultation request',L.join(['Name:','Department:','','What I would like to discuss:','','Times that work for me:','']),cc=None)
BN_REQ=mt('cnap@ksu.edu','Behavioral Neuroscience Core: space and equipment request',L.join(['Name:','Department:','Study title:','IACUC protocol number and approval status:','','Species and number of animals:','','Rooms or equipment needed:','','Preferred dates:','','Questions:','']),cc=None)
BN_CON=mt('cnap@ksu.edu','Behavioral Neuroscience Core: consultation or tour request',L.join(['Name:','Department:','','Consultation, tour, or both:','','What I would like to discuss:','','Times that work for me:','']),cc=None)
