# Copies the Django app's reporting pages (My tasks, My history, every form and its preview) into the
# prototype, unchanged in design (MW 2026-11-15: "keep all of the app's reporting pages the same").
# Source: snap/rep_*.html, fetched as the fictional demo member Amara Okafor. Nothing posts anywhere.
import re, os, shutil, glob
V = '/tmp/claude-0/hubproto/v4/'
ST = '/home/claude/cnap-platform/static/'
A = V + 'app/'
for d in ['css', 'js', 'img', 'fonts']:
    os.makedirs(A + d, exist_ok=True)

def name(path):
    if path == '/tasks/': return 'reporting.html'
    if path == '/history/': return 'reporting-history.html'
    m = re.fullmatch(r'/tasks/(\d+)/(preview/)?', path)
    if m: return 'reporting-%s%s.html' % (m.group(1), '-preview' if m.group(2) else '')
    return None

files = {}
for f in glob.glob('/tmp/claude-0/hubproto/snap/rep_*.html'):
    path = os.path.basename(f)[4:-5].replace('_', '/')
    files[path] = f

PROTO = ('<script>document.querySelectorAll("form[data-proto-form]").forEach(function(f){f.addEventListener("submit",function(e){e.preventDefault();'
         'var n=f.querySelector(".proto-note-sub");if(!n){n=document.createElement("p");n.className="proto-note-sub";n.setAttribute("role","status");'
         'n.style.cssText="margin:12px 0 0;padding:10px 14px;border-radius:8px;background:#f1ecf8;color:#3c1d66;font-size:14px";f.appendChild(n);}'
         'n.textContent="Prototype copy of the app page. In the Member Hub app, this saves your answers. Here, nothing is sent.";});});'
         'document.querySelectorAll("a[data-proto]").forEach(function(a){a.addEventListener("click",function(e){e.preventDefault();});a.title="Not part of the prototype";});</script>\n')

used = set()
for path, f in files.items():
    out = name(path)
    if not out: continue
    s = open(f).read()
    s = re.sub(r'<link rel="(icon|apple-touch-icon)"[^>]*>\n?', '', s)
    s = re.sub(r'<input type="hidden" name="csrfmiddlewaretoken" value="[^"]*">', '', s)
    s = re.sub(r'href="/static/forms/[^"]*"', 'href="#" data-proto', s)
    for m in re.findall(r'/static/((?:css|js|img)/[^"?\s]+)', s):
        used.add(m)
    s = re.sub(r'/static/((?:css|js|img)/[^"?\s]+)(?:\?v=\d+)?', r'app/\1', s)
    # page links
    def link(m):
        p = m.group(1)
        n = name(p)
        if n: return 'href="%s"' % n
        if p == '/': return 'href="index.html"'
        if p == '/profile/': return 'href="mentee-profile.html"'
        if p == '/funding/': return 'href="funding.html"'
        return 'href="#" data-proto'
    s = re.sub(r'href="(/[^"]*)"', link, s)
    s = s.replace('data-autosave="', 'data-was-autosave="')
    s = re.sub(r'<form method="post"( action="[^"]*")?', '<form method="post" action="#" data-proto-form', s)
    # the app's own feedback widget posts to the server; the shared prototype one replaces it
    if '<button type="button" class="fbk-open"' in s:
        i = s.index('<button type="button" class="fbk-open"'); j = s.index('</script>', s.index('</dialog>', i)) + 9
        s = s[:i] + s[j:]
    s = s.replace('</body>', PROTO + '<script src="hubchrome.js" defer></script>\n</body>')
    assert '/static/' not in s and 'csrfmiddlewaretoken' not in s and 'href="/' not in s and 'action="/' not in s, (out, re.findall(r'(?:href|action)="/[^"]*"', s)[:3])
    open(V + out, 'w').write(s)

for m in used:
    if m.startswith('forms/'): continue
    os.makedirs(os.path.dirname(A + m), exist_ok=True)
    shutil.copy(ST + m, A + m)
shutil.copy(ST + 'fonts/Lora-Variable.ttf', A + 'fonts/Lora-Variable.ttf')
print('ok', sorted(name(p) for p in files if name(p)))
print('assets', sorted(used))
