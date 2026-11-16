(function(){if(location.hash)return;try{if('scrollRestoration' in history)history.scrollRestoration='manual';}catch(e){}
function top(){window.scrollTo(0,0);try{document.scrollingElement.scrollTop=0;}catch(e){}}
top();document.addEventListener('DOMContentLoaded',top);addEventListener('load',function(){top();setTimeout(top,150);});
addEventListener('pageshow',function(e){if(e.persisted)top();});})();
/* Guide behaviour: the spine follows the reader, "Mark as read" is remembered in this browser only
   (the Hub doesn't store it yet), and the acknowledgement copies to the clipboard. */
(function(){
  var key='cnap-guide-'+document.body.dataset.guide,store={};
  try{store=JSON.parse(localStorage.getItem(key)||'{}')||{};}catch(e){}
  var steps=[].slice.call(document.querySelectorAll('.step')),links=[].slice.call(document.querySelectorAll('.spine a'));
  var ring=document.querySelector('.who .ring-p'),count=document.getElementById('read-n');
  function paint(){var n=0;steps.forEach(function(s,i){var on=!!store[s.id];if(on)n++;var b=s.querySelector('.read');if(b){b.setAttribute('aria-pressed',on);b.lastChild.textContent=on?'Read':'Mark as read';}links[i]&&links[i].classList.toggle('done',on);document.querySelectorAll('.hs a[href="#'+s.id+'"]').forEach(function(a){a.classList.toggle('done',on);});});
    if(ring)ring.style.strokeDasharray=n+' '+steps.length;if(count)count.textContent=n+' of '+steps.length;}
  steps.forEach(function(s){var b=s.querySelector('.read');if(!b)return;b.addEventListener('click',function(){store[s.id]=!store[s.id];try{localStorage.setItem(key,JSON.stringify(store));}catch(e){}paint();});});
  paint();
  function spy(){var y=innerHeight*.3,cur=steps[0];steps.forEach(function(s){if(s.getBoundingClientRect().top<y)cur=s;});links.forEach(function(a){a.toggleAttribute('aria-current',a.getAttribute('href')==='#'+cur.id);if(a.hasAttribute('aria-current'))a.setAttribute('aria-current','step');});}
  var tr=document.querySelector('.spine-track'),fl=document.querySelector('.spine-fill'),ol=document.querySelector('.spine ol');
  function track(){if(!tr||!links.length)return;var o=ol.getBoundingClientRect().top,dot=function(a){var r=a.getBoundingClientRect();var s=getComputedStyle(a,'::before');return r.top-o+parseFloat(s.top)+5;};
    var t=dot(links[0]),b=dot(links[links.length-1]);tr.style.top=(ol.offsetTop+t)+'px';tr.style.height=(b-t)+'px';
    var cur=document.querySelector('.spine a[aria-current]');fl.style.height=cur?(dot(cur)-t)+'px':'0px';}
  addEventListener('scroll',function(){spy();track();},{passive:true});addEventListener('resize',track);var sp=document.querySelector('.spine');if(sp){['mouseenter','mouseleave','focusin','focusout','transitionend'].forEach(function(e){sp.addEventListener(e,function(){requestAnimationFrame(track);setTimeout(track,280);});});}spy();track();
  var cb=document.querySelector('.cite button');if(cb)cb.addEventListener('click',function(){var t=document.getElementById('cite-t').textContent.trim();
    function done(){cb.textContent='Copied';setTimeout(function(){cb.textContent='Copy the acknowledgement';},1800);}
    try{navigator.clipboard.writeText(t).then(done,function(){sel();});}catch(e){sel();}
    function sel(){var r=document.createRange();r.selectNodeContents(document.getElementById('cite-t'));var s=getSelection();s.removeAllRanges();s.addRange(r);cb.textContent='Selected. Press Ctrl+C to copy';}});
})();

(function(){var bs=document.querySelectorAll('.pp-b');if(!bs.length)return;var hint=document.querySelector('.pp-hint');
bs.forEach(function(b){b.addEventListener('click',function(){var open=b.getAttribute('aria-expanded')==='true';
bs.forEach(function(o){o.setAttribute('aria-expanded','false');document.getElementById(o.getAttribute('aria-controls')).hidden=true});
if(!open){b.setAttribute('aria-expanded','true');document.getElementById(b.getAttribute('aria-controls')).hidden=false}
});});})();

(function(){function closeAll(){document.querySelectorAll('.pp-b[aria-expanded="true"]').forEach(function(b){b.setAttribute('aria-expanded','false');document.getElementById(b.getAttribute('aria-controls')).hidden=true;});}
document.addEventListener('click',function(e){if(!e.target.closest('.pp-it'))closeAll();});
document.addEventListener('keydown',function(e){if(e.key==='Escape'){var o=document.querySelector('.pp-b[aria-expanded="true"]');closeAll();if(o)o.focus();}});})();

(function(){var a=document.querySelector('[data-dl]');if(!a||!window.claude||!window.claude.use)return;var dl=null;
window.claude.use('downloads').then(function(d){dl=d;}).catch(function(){});
a.addEventListener('click',function(e){if(!dl)return;e.preventDefault();var name=a.getAttribute('data-dl');
var b64=window.CNAP_MEETING_LOG;var p=b64?Promise.resolve(Uint8Array.from(atob(b64),function(c){return c.charCodeAt(0);})):fetch(name).then(function(r){if(!r.ok)throw 0;return r.blob();});p.then(function(d){return dl.save({filename:name,data:d});}).catch(function(){});});})();

(function(){document.addEventListener('click',function(e){var a=e.target.closest('a[href^="index.html#"]');if(!a)return;try{sessionStorage.setItem('cnap-goto',a.getAttribute('href').split('#')[1]);}catch(x){}});})();

/* Stevens Amendment statements (MW 2026-11-14): each Copy button copies the statement beside it */
(function(){document.querySelectorAll('.stv-copy').forEach(function(b){b.addEventListener('click',function(){var p=b.parentNode.querySelector('p'),t=p.textContent.trim();
  function done(){b.textContent='Copied';setTimeout(function(){b.textContent='Copy'},1800);}
  function sel(){var r=document.createRange();r.selectNodeContents(p);var s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent='Selected. Press Ctrl+C';}
  try{navigator.clipboard.writeText(t).then(done,sel);}catch(e){sel();}});});})();

/* Guide heroes (MW 2026-11-15: "pull the paragraph and the box over the line of CNAP"): the intro and
   the step list end where the title's longest line ends. */
(function(){var h=document.querySelector('.open-g h1');if(!h)return;var els=[].slice.call(document.querySelectorAll('.open-g .lead,.open-g .hs'));
function fit(){var r=document.createRange();r.selectNodeContents(h);var w=0,tops={};[].forEach.call(r.getClientRects(),function(x){w=Math.max(w,x.width);tops[Math.round(x.top)]=1;});if(Object.keys(tops).length>1)w=h.parentNode.clientWidth;
  var narrow=innerWidth<760,inset=Math.round(parseFloat(getComputedStyle(h).fontSize)*.045);/* the serif M starts a few pixels in from its box, so the intro and list step in to line up with its stem */
  els.forEach(function(e){e.style.marginLeft=inset+'px';e.style.maxWidth=narrow?'':Math.round(Math.max(w,360)-inset)+'px';e.style.width=narrow?'':'100%';});}
fit();addEventListener('resize',fit);if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fit);addEventListener('load',fit);})();
