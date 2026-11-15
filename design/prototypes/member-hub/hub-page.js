/* Member Hub inner pages (MW 2026-11-14): On this page, Hide and Show, roll-ups, Show all and Collapse all. */
(function(){
  var sheet=document.querySelector('.pg-sheet');if(!sheet)return;
  var KEY='cnap-onpage-hidden',hide=sheet.querySelector('[data-navtoggle]'),show=sheet.querySelector('[data-navshow]');
  function setHidden(v){sheet.classList.toggle('nav-hidden',v);if(show)show.hidden=!v;if(hide)hide.setAttribute('aria-expanded',!v);try{localStorage.setItem(KEY,v?'1':'0');}catch(e){}}
  try{if(localStorage.getItem(KEY)==='1')setHidden(true);}catch(e){}
  if(hide)hide.addEventListener('click',function(){setHidden(true);if(show)show.focus();});
  if(show)show.addEventListener('click',function(){setHidden(false);if(hide)hide.focus();});
  var rolls=[].slice.call(sheet.querySelectorAll('.pg-roll'));
  sheet.querySelectorAll('[data-roll]').forEach(function(b){b.addEventListener('click',function(){var open=b.dataset.roll==='open';rolls.forEach(function(r){r.open=open;});});});
  document.querySelectorAll('[data-onpage]').forEach(function(a){a.addEventListener('click',function(){var t=document.querySelector(a.getAttribute('href'));if(t&&t.tagName==='DETAILS')t.open=true;});});
  var links=[].slice.call(sheet.querySelectorAll('.pg-onpage a'));
  function spy(){var y=innerHeight*.3,cur=null;rolls.forEach(function(r){if(r.getBoundingClientRect().top<y)cur=r;});links.forEach(function(a){a.setAttribute('aria-current',!!cur&&a.getAttribute('href')==='#'+cur.id);});}
  addEventListener('scroll',spy,{passive:true});spy();
})();

/* the avatar menu, as on the homepage */
(function(){try{var am=document.querySelector('.acct'),ab=am.querySelector('.avatar');function amOpen(v){am.classList.toggle('open',v);ab.setAttribute('aria-expanded',v);}
  ab.addEventListener('click',function(e){e.stopPropagation();amOpen(!am.classList.contains('open'));});
  document.addEventListener('click',function(e){if(!am.contains(e.target))amOpen(false);});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&am.classList.contains('open')){amOpen(false);ab.focus();}});}catch(e){}})();

/* Funding and proposals (MW 2026-11-14): the dot rail follows the reader, as on the guides */
(function(){
  var sp=document.querySelector('.fp-page .spine');if(!sp)return;
  var links=[].slice.call(sp.querySelectorAll('ol a')),secs=links.map(function(a){return document.querySelector(a.getAttribute('href'));}).filter(Boolean);
  var tr=sp.querySelector('.spine-track'),fl=sp.querySelector('.spine-fill'),ol=sp.querySelector('ol');
  function spy(){var y=innerHeight*.3,i=0;secs.forEach(function(s,k){if(s.getBoundingClientRect().top<y)i=k;});
    links.forEach(function(a,k){if(k===i)a.setAttribute('aria-current','step');else a.removeAttribute('aria-current');a.classList.toggle('done',k<i);});}
  function track(){if(!tr||!links.length||getComputedStyle(tr).display==='none')return;var o=ol.getBoundingClientRect().top;
    function dot(a){return a.getBoundingClientRect().top-o+parseFloat(getComputedStyle(a,'::before').top)+5;}
    var t=dot(links[0]),b=dot(links[links.length-1]);tr.style.top=(ol.offsetTop+t)+'px';tr.style.height=(b-t)+'px';
    var cur=sp.querySelector('a[aria-current]');fl.style.height=cur?(dot(cur)-t)+'px':'0px';}
  addEventListener('scroll',function(){spy();track();},{passive:true});addEventListener('resize',track);
  ['mouseenter','mouseleave','focusin','focusout','transitionend'].forEach(function(e){sp.addEventListener(e,function(){requestAnimationFrame(track);setTimeout(track,280);});});
  spy();track();
})();

/* Before you apply: Show all questions and Hide all questions (MW 2026-11-14) */
(function(){
  var b=document.querySelector('[data-qall]');if(!b)return;
  var ds=[].slice.call(document.querySelectorAll('.fp-qs details'));
  function sync(){var all=ds.every(function(d){return d.open;});b.textContent=all?'Hide all questions':'Show all questions';b.setAttribute('aria-expanded',all);}
  b.addEventListener('click',function(){var open=!ds.every(function(d){return d.open;});ds.forEach(function(d){d.open=open;});sync();});
  ds.forEach(function(d){d.addEventListener('toggle',sync);});
})();

/* the section rule's accent slides once each heading comes into view, as on the homepage */
(function(){try{if(!('IntersectionObserver' in window))return;document.documentElement.classList.add('js-draw');
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('drawn');io.unobserve(e.target);}});},{rootMargin:'0px 0px -25% 0px'});
  document.querySelectorAll('.fp-sh').forEach(function(el){io.observe(el);});}catch(e){}})();
