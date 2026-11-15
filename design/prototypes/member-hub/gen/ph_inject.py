import re
def inject(s):
    imgs=['reel-1','reel-3','reel-4','reel-2','reel-5']
    k=[0]
    def ph(cls,alt):
        i=imgs[k[0]%len(imgs)];k[0]+=1
        return '<figure class="%s"><img src="img/%s.jpg" alt="Placeholder for a photo of %s" loading="lazy"><span class="pp-tag">Photo placeholder</span></figure>'%(cls,i,alt)
    s=s.replace('<li class="fp-pin">','<li class="fp-pin">'+'@@PH@@')
    while '@@PH@@' in s: s=s.replace('@@PH@@',ph('fp-pin-ph','this news'),1)
    s=s.replace('<div class="fp-ev-t">','@@EV@@<div class="fp-ev-t">')
    while '@@EV@@' in s: s=s.replace('@@EV@@',ph('fp-ev-ph','this event'),1)
    if 'fp-photos.css' not in s: s=s.replace('</head>','<link rel="stylesheet" href="fp-photos.css">\n</head>',1)
    return s
