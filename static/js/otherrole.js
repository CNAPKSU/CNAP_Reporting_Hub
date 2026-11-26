/* Role in the Center (MW 2026-11-25): the "Other" text box shows only when Other is chosen. */
(function () {
  function wire(select) {
    var form = select.form;
    if (!form) return;
    var box = form.querySelector('[name="' + select.name + '_other"]');
    if (!box) return;
    var wrap = box.closest(".field") || box.parentNode;
    function sync() {
      var on = select.value === "other";
      wrap.style.display = on ? "" : "none";
      box.required = on;
      if (on && document.activeElement === select) box.focus();
    }
    select.addEventListener("change", sync);
    sync();
  }
  function init() {
    document.querySelectorAll('select[name$="center_role"]').forEach(wire);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
