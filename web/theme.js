// Set the theme before the first paint: the player's saved choice, then ?theme=dark|light
// (for example from the dashboard's iframe URL). With neither, follow prefers-color-scheme.
(function () {
  var theme = null;
  try { theme = localStorage.getItem("defiantjazz.theme"); } catch (e) { theme = null; }
  if (theme !== "dark" && theme !== "light") {
    try { theme = new URLSearchParams(location.search).get("theme"); } catch (e) { theme = null; }
  }
  if (theme === "dark" || theme === "light") document.documentElement.dataset.theme = theme;
})();
