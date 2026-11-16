/* Small dropdowns (a <details> that shows a note or a short list) close when you click anywhere
   else on the page, click the open text itself, or press Escape, as well as on their own arrow.
   MW 2026-11-15 design rule. Page sections (.px-roll, .panel and similar) and dropdowns that hold
   form fields stay open until their own title is clicked, so no answer is hidden mid-entry.
   Add data-keep-open to any <details> that should not close this way. */
(function () {
  if (window.__dropClose) return; window.__dropClose = 1;
  var SKIP = '.px-roll,.panel,.dashsec,.cntsec,.r90-partroll,.lgroup,.em-roll,[data-keep-open]';
  function small(d) { return !d.matches(SKIP) && !d.querySelector('input,select,textarea'); }
  document.addEventListener('click', function (e) {
    var t = e.target;
    if (!(t instanceof Element)) return;
    document.querySelectorAll('details[open]').forEach(function (d) {
      if (!small(d)) return;
      var s = d.querySelector(':scope > summary');
      if (s && s.contains(t)) return;                          // its own arrow toggles as usual
      if (d.contains(t)) {
        if (t.closest('details') !== d) return;                // a click inside a dropdown nested in this one
        if (t.closest('a,button,label,input,select,textarea,[tabindex]')) return;
        if (String(window.getSelection ? window.getSelection() : '').trim()) return;  // keep it open while text is being selected
      }
      d.open = false;
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape' || document.querySelector('dialog[open]')) return;
    var open = [].filter.call(document.querySelectorAll('details[open]'), small);
    if (!open.length) return;
    var last = open[open.length - 1], s = last.querySelector(':scope > summary');
    var hadFocus = last.contains(document.activeElement);
    open.forEach(function (d) { d.open = false; });
    if (hadFocus && s) s.focus();
  });
})();
