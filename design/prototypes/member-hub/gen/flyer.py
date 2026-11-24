# Printable flyer for the invited NeuroSync speaker (MW 2026-11-15: "you can also print a flyer from here").
# Builds neurosync-flyer.html (letter size) and renders it to neurosync-flyer.pdf with Playwright.
# The speaker is fictional; the flyer says so in small type.
import subprocess, json
V = '/tmp/claude-0/hubproto/v4/'
html = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>NeuroSync flyer · Machine learning for spike sorting</title>
<style>
@font-face{font-family:"Inter Hub";src:url("fonts/inter-400.woff") format("woff");font-weight:400}
@font-face{font-family:"Inter Hub";src:url("fonts/inter-500.woff") format("woff");font-weight:500}
@font-face{font-family:"Inter Hub";src:url("fonts/inter-600.woff") format("woff");font-weight:600}
@font-face{font-family:"Lora Hub";src:url("fonts/lora.woff") format("woff");font-weight:400 700}
@page{size:8.5in 11in;margin:0}
*{box-sizing:border-box}
html,body{margin:0;background:#fff}
body{font-family:"Inter Hub",system-ui,sans-serif;color:#1f1a24}
.pg{width:8.5in;height:11in;display:flex;flex-direction:column;overflow:hidden}
.top{background:#140b1a;background:radial-gradient(120% 90% at 85% 10%,#2a1838 0%,#1a0f22 58%,#140b1a 100%);color:#fff;padding:.6in .7in .55in}
.series{display:flex;justify-content:space-between;align-items:baseline;font-size:12pt;letter-spacing:.02em}
.series b{font:500 22pt/1 "Lora Hub",Georgia,serif;letter-spacing:0}
.series span{color:rgba(255,255,255,.75)}
.kick{margin:.55in 0 0;color:#e9c98f;font-weight:600;font-size:13pt}
h1{margin:.12in 0 0;font:500 44pt/1.05 "Lora Hub",Georgia,serif;letter-spacing:-.01em}
.wave{display:block;width:100%;height:.55in;margin-top:.35in;opacity:.55}
.mid{flex:1;padding:.5in .7in 0;display:grid;grid-template-columns:1.6in 1fr;gap:.35in;align-content:start}
.hs{width:1.6in;height:1.6in;border-radius:50%;background:#efe8f8;display:grid;place-items:center;color:#3c1d66;font:500 30pt "Lora Hub",Georgia,serif;text-align:center}
.hs>div{display:flex;flex-direction:column;align-items:center;line-height:1}.hs small{display:block;font:500 8pt "Inter Hub",sans-serif;color:#6b6475;margin-top:.08in}
.who b{display:block;font:500 22pt/1.2 "Lora Hub",Georgia,serif}
.who p{margin:.06in 0 0;font-size:11.5pt;line-height:1.45;color:#4a4352}
.who .about{margin-top:.18in;font-size:12pt;line-height:1.55;color:#2c2632}
.facts{margin:.45in .7in 0;display:grid;grid-template-columns:repeat(3,1fr);border-top:2px solid #512888}
.facts div{padding:.16in .2in .18in 0}
.facts div+div{padding-left:.2in;border-left:1px solid #ddd5e6}
.facts dt{font-size:9.5pt;font-weight:600;color:#512888;letter-spacing:.02em}
.facts dd{margin:.05in 0 0;font-size:12.5pt;line-height:1.4}
.foot{margin-top:auto;padding:.3in .7in .45in;display:flex;justify-content:space-between;align-items:flex-end;font-size:9.5pt;color:#6b6475;border-top:1px solid #eee8f3}
.foot b{display:block;color:#1f1a24;font-size:10.5pt;margin-bottom:.03in}
.proto{font-size:8pt;color:#8a8392;text-align:right}
</style></head><body><div class="pg">
<div class="top">
  <div class="series"><b>NeuroSync</b><span>The CNAP Center’s weekly speaker series</span></div>
  <p class="kick">Invited speaker · Wednesday, December 2, 2026</p>
  <h1>Machine learning for spike sorting</h1>
  <svg class="wave" viewBox="0 0 1200 80" preserveAspectRatio="none" aria-hidden="true"><path d="WAVE" fill="none" stroke="#fff" stroke-width="1.6"/></svg>
</div>
<div class="mid">
  <div class="hs"><div>DK<small>Headshot to come</small></div></div>
  <div class="who"><b>Dr. Daniel Kim</b><p>Associate Professor of Computer Science and director of the Neural Data Lab, Iowa State University</p>
  <p class="about">Dr. Kim builds machine-learning tools that sort the electrical signals of single neurons from large recordings, so that labs can study thousands of cells at once. His lab shares its methods as open-source software used by groups across the country.</p></div>
</div>
<dl class="facts"><div><dt>When</dt><dd>Wednesday, December 2<br>2:30 to 3:30 p.m.</dd></div><div><dt>Where</dt><dd>LOC<br>Refreshments provided</dd></div><div><dt>Online</dt><dd>Zoom. The link is in the weekly email.</dd></div></dl>
<div class="foot"><div><b>Cognitive and Neurobiological Approaches to Plasticity (CNAP) Center</b>Kansas State University · Questions: mkwills@ksu.edu</div><div class="proto">Prototype sample.<br>The speaker is fictional.</div></div>
</div><script>/* on a screen narrower than the page, the letter-size flyer shrinks to fit; printing is unchanged (MW 2026-11-24 review) */(function(){function fit(){var w=816,z=Math.min(1,(document.documentElement.clientWidth-16)/w);document.querySelectorAll('.pg').forEach(function(p){p.style.zoom=z<1?z:'';});}fit();addEventListener('resize',fit);addEventListener('beforeprint',function(){document.querySelectorAll('.pg').forEach(function(p){p.style.zoom='';});});addEventListener('afterprint',fit);})();</script></body></html>'''
if __name__ == '__main__':
    import sys, io, contextlib
    sys.path.insert(0, '/tmp/claude-0/hubproto/gen')
    with contextlib.redirect_stdout(io.StringIO()):
        import neurosync as N
    html = html.replace('WAVE', N.wave).replace('LOC', N.LOC)
    open(V + 'neurosync-flyer.html', 'w').write(html)
    js = "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://%sneurosync-flyer.html');await p.waitForTimeout(500);await p.pdf({path:'%sneurosync-flyer.pdf',width:'8.5in',height:'11in',printBackground:true});await p.screenshot({path:'/tmp/claude-0/flyer.png',fullPage:true});await b.close();})();" % (V, V)
    open('/tmp/claude-0/flyer.js', 'w').write(js)
    subprocess.run(['node', '/tmp/claude-0/flyer.js'], check=True)
    print('ok')
