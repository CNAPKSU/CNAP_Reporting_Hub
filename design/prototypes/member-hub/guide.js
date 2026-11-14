/* Guide behaviour: the spine follows the reader, "Mark as read" is remembered in this browser only
   (the Hub doesn't store it yet), and the acknowledgement copies to the clipboard. */
(function(){
  var key='cnap-guide-'+document.body.dataset.guide,store={};
  try{store=JSON.parse(localStorage.getItem(key)||'{}')||{};}catch(e){}
  var steps=[].slice.call(document.querySelectorAll('.step')),links=[].slice.call(document.querySelectorAll('.spine a'));
  var ring=document.querySelector('.who .ring-p'),count=document.getElementById('read-n');
  function paint(){var n=0;steps.forEach(function(s,i){var on=!!store[s.id];if(on)n++;var b=s.querySelector('.read');if(b){b.setAttribute('aria-pressed',on);b.lastChild.textContent=on?'Read':'Mark as read';}links[i]&&links[i].classList.toggle('done',on);});
    if(ring)ring.style.strokeDasharray=n+' '+steps.length;if(count)count.textContent=n+' of '+steps.length;}
  steps.forEach(function(s){var b=s.querySelector('.read');if(!b)return;b.addEventListener('click',function(){store[s.id]=!store[s.id];try{localStorage.setItem(key,JSON.stringify(store));}catch(e){}paint();});});
  paint();
  function spy(){var y=innerHeight*.3,cur=steps[0];steps.forEach(function(s){if(s.getBoundingClientRect().top<y)cur=s;});links.forEach(function(a){a.toggleAttribute('aria-current',a.getAttribute('href')==='#'+cur.id);if(a.hasAttribute('aria-current'))a.setAttribute('aria-current','step');});}
  addEventListener('scroll',spy,{passive:true});spy();
  var cb=document.querySelector('.cite button');if(cb)cb.addEventListener('click',function(){var t=document.getElementById('cite-t').textContent.trim();
    function done(){cb.textContent='Copied';setTimeout(function(){cb.textContent='Copy the acknowledgement';},1800);}
    try{navigator.clipboard.writeText(t).then(done,function(){sel();});}catch(e){sel();}
    function sel(){var r=document.createRange();r.selectNodeContents(document.getElementById('cite-t'));var s=getSelection();s.removeAllRanges();s.addRange(r);cb.textContent='Selected. Press Ctrl+C to copy';}});
})();
