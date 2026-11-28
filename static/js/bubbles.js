/* One information bubble for the whole site (MW 2026-11-28): the dark purple bubble of the "?" marks.
   Anything with a title shows its words in this bubble on hover or keyboard focus, instead of the
   browser's small gray tooltip. The words stay available to screen readers. */
(function () {
  if (window.__cnapBubbles) return;
  window.__cnapBubbles = true;
  var tip = null, owner = null, timer = null;

  function box() {
    if (tip) return tip;
    tip = document.createElement("div");
    tip.className = "cnap-bubble";
    tip.id = "cnap-bubble";
    tip.setAttribute("role", "tooltip");
    document.body.appendChild(tip);
    return tip;
  }

  function target(el) {
    while (el && el.nodeType === 1) {
      if (el.closest && el.closest(".whyq, .cnap-bubble")) return null;
      if (el.hasAttribute("data-bubble")) return el;
      if (el.hasAttribute("title") && el.getAttribute("title").trim() && el.tagName !== "IFRAME" && !(el instanceof SVGElement)) {
        var t = el.getAttribute("title");
        el.setAttribute("data-bubble", t);
        el.removeAttribute("title"); /* no second, gray tooltip */
        if (!el.getAttribute("aria-label") && !el.getAttribute("aria-labelledby") && !(el.textContent || "").trim()) {
          el.setAttribute("aria-label", t);
        }
        return el;
      }
      el = el.parentElement;
    }
    return null;
  }

  function place() {
    if (!owner || !tip) return;
    var r = owner.getBoundingClientRect(), vw = document.documentElement.clientWidth, vh = window.innerHeight, gap = 8;
    tip.style.left = "0px"; tip.style.top = "0px";
    var w = tip.offsetWidth, h = tip.offsetHeight;
    var left = Math.min(Math.max(8, r.left + r.width / 2 - w / 2), vw - w - 8);
    var top = r.bottom + gap;
    if (top + h > vh - 8 && r.top - gap - h > 8) top = r.top - gap - h;
    tip.style.left = Math.round(left) + "px";
    tip.style.top = Math.round(top) + "px";
  }

  function show(el) {
    clearTimeout(timer);
    owner = el;
    var t = box();
    t.textContent = el.getAttribute("data-bubble");
    t.classList.add("on");
    el.setAttribute("aria-describedby", ((el.getAttribute("aria-describedby") || "").replace("cnap-bubble", "") + " cnap-bubble").trim());
    place();
  }

  function hide() {
    clearTimeout(timer);
    if (owner) {
      var d = (owner.getAttribute("aria-describedby") || "").replace("cnap-bubble", "").trim();
      if (d) owner.setAttribute("aria-describedby", d); else owner.removeAttribute("aria-describedby");
    }
    owner = null;
    if (tip) tip.classList.remove("on");
  }

  document.addEventListener("mouseover", function (e) {
    var el = target(e.target);
    if (el === owner) return;
    if (!el) { if (owner && !owner.contains(e.target)) hide(); return; }
    clearTimeout(timer);
    timer = setTimeout(function () { show(el); }, owner ? 0 : 250);
  });
  document.addEventListener("mouseout", function (e) {
    var el = target(e.target);
    if (el && (!e.relatedTarget || !el.contains(e.relatedTarget))) { clearTimeout(timer); if (el === owner) hide(); }
  });
  document.addEventListener("focusin", function (e) { var el = target(e.target); if (el && e.target.matches(":focus-visible")) show(el); });
  document.addEventListener("focusout", hide);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") hide(); });
  /* capture: also when an inner panel scrolls, not just the window */
  document.addEventListener("scroll", function () { if (owner) place(); }, { passive: true, capture: true });
  window.addEventListener("resize", hide);
  document.addEventListener("mousedown", hide);
})();
