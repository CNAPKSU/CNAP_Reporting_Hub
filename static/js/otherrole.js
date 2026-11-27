/* Roles in the Center (MW 2026-11-26): the "Other" text box shows only while Other is ticked. */
(function () {
  function wire(tick) {
    var form = tick.form;
    if (!form) return;
    var box = form.querySelector('[name="center_role_other"]');
    if (!box) return;
    var wrap = box.closest(".field") || box.parentNode;
    function sync(focus) {
      var on = tick.checked;
      wrap.style.display = on ? "" : "none";
      box.required = on;
      if (on && focus) box.focus();
    }
    tick.addEventListener("change", function () { sync(true); });
    sync(false);
  }
  function init() {
    document.querySelectorAll('input[name="center_roles"][value="other"]').forEach(wire);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
