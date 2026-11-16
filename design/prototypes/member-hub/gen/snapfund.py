import sys;sys.path.insert(0,"/tmp/claude-0/hubproto")
import re,shutil
V='/tmp/claude-0/hubproto/v4/'
for f in ['funding.html','funding-resources.html','funding-news.html']:
    s=open('snap/'+f).read()
    s=re.sub(r'<link rel="(icon|apple-touch-icon)"[^>]*>\n?','',s)
    s=re.sub(r'href="/static/hub/hub\.css\?v=\d+"','href="hub.css"',s)
    s=re.sub(r'href="/static/hub/page\.css\?v=\d+"','href="hub-page.css"',s)
    s=re.sub(r'src="/static/hub/page\.js\?v=\d+"','src="hub-page.js"',s)
    s=re.sub(r'<input type="hidden" name="csrfmiddlewaretoken" value="[^"]*">','',s)
    for a,b in [('href="/funding/resources/','href="funding-resources.html'),('href="/funding/news/','href="funding-news.html'),('href="/funding/','href="funding.html'),('href="/tasks/"','href="reporting.html"'),('href="/#','href="index.html#'),('href="/"','href="index.html"'),('href="/profile/"','href="mentee-profile.html"'),('href="/history/"','href="reporting.html"'),('href="/accounts/password/"','href="#"'),('action="/accounts/logout/"','action="#"'),('action="/funding/suggest/"','action="#" data-proto-form')]:
        s=s.replace(a,b)
    s=re.sub(r'href="index.html#com-h" data-thread="(\w+)"',r'href="community.html?t=\1#cm-ask" data-thread="\1"',s)
    s=s.replace('href="index.html#com-h"','href="community.html"')
    s=s.replace('aria-label="Priya Natarajan: profile and settings">PN</button>','aria-label="Dr. Amara Okafor: profile and settings">AO</button>')
    s=s.replace('<p class="acct-who">Priya Natarajan<span>Neuroinformatics Core director</span></p>','<p class="acct-who">Dr. Amara Okafor<span>Pilot project leader</span></p>')
    i=s.index('<button type="button" class="fbk-open"'); j=s.index('</script>',s.index('</dialog>',i))+9
    s=s[:i]+s[j:]
    s=s.replace('</body>','<script src="hubchrome.js" defer></script>\n</body>') if 'hubchrome' not in s else s
    s=s.replace('<a href="mailto:cnap@ksu.edu" title="Opens an email to the CNAP team.">cnap@ksu.edu</a></div></footer>','<span>Prototype copy of the Member Hub app’s Funding page. The opportunities, news, and events are the app’s sample records. The suggestion form doesn’t send from the prototype.</span></div></footer>')
    s=s.replace('<script src="hub-page.js" defer></script>','''<script src="hub-page.js" defer></script>
<script>document.querySelectorAll('[data-proto-form]').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault();var n=f.querySelector('.fp-proto');if(!n){n=document.createElement('p');n.className='fp-proto fp-help';n.setAttribute('role','status');f.appendChild(n);}n.textContent='Prototype only: in the Member Hub app, the suggestion goes to the CNAP team for review.';});});</script>''')
    s=__import__('ph_inject').inject(s)
    assert 'Natarajan' not in s and '/static/' not in s and 'csrf' not in s, f
    open(V+f,'w').write(s)
shutil.copy('/home/claude/cnap-platform/static/hub/hub.css',V+'hub.css')
shutil.copy('/home/claude/cnap-platform/static/hub/page.css',V+'hub-page.css')
shutil.copy('/home/claude/cnap-platform/static/hub/page.js',V+'hub-page.js')
print('ok')
