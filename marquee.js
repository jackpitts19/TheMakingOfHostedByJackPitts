/* Past-guests marquee for /be-a-guest.
   Paints the scrolling band of guest names from window.EPISODES (episodes.js,
   the same source of truth the homepage renders from). Without JavaScript the
   band stays empty and site.css hides it; the static "Past guests include"
   list on the page covers that case. */
(function () {
  var track = document.getElementById("marquee-track");
  var episodes = window.EPISODES || [];
  if (!track || !episodes.length) return;

  function escHtml(s) {
    return String(s || "").replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;", "'": "&#39;" }[c];
    });
  }
  function slugify(name) {
    return String(name || "")
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "") || "episode";
  }
  // Mirrors seo_urls.extract_guest_name() and the homepage renderer.
  function extractGuestName(title) {
    if (!title) return "";
    function stripQuotes(v) { return v.replace(/^["“”'\s]+|["“”'\s]+$/g, ""); }
    var t = title.trim();
    if (t.indexOf("|") > -1) return stripQuotes(t.split("|").pop()) || title;
    if (/^From\s/i.test(t)) {
      var parts = t.split(/:|\s+with\s+/i);
      return parts.length > 1 ? stripQuotes(parts[parts.length - 1]) : title;
    }
    t = t.replace(/^In\s+The\s+Making\s+Of:\s*/i, "");
    t = t.replace(/^The\s+Making\s+(Of|of)\s+/i, "");
    t = t.split(/:|\s+with\s+|\s+from\s+/i)[0];
    t = t.split(/\s+of\s+/)[0];
    t = stripQuotes(t);
    return t || title;
  }
  // A pinned slug always wins, so URLs never move. Mirrors seo_urls.episode_slug().
  function episodePageHref(ep) {
    if (ep.slug) return "/episodes/" + String(ep.slug);
    return "/episodes/" + slugify(ep.guest || extractGuestName(ep.title || "") || ep.title || "");
  }
  function displayGuest(ep) {
    var name = String(ep.guest || extractGuestName(ep.title || "") || "");
    if (name.indexOf("|") > -1) name = name.split("|").pop();
    return name.trim() || String(ep.title || "");
  }

  var seen = {};
  var guests = [];
  episodes.forEach(function (ep) {
    var name = displayGuest(ep);
    if (!name || seen[name]) return;
    seen[name] = true;
    guests.push({ name: name, href: episodePageHref(ep) });
  });

  // The second run only exists for the seamless loop, so it is hidden from
  // assistive tech and removed from the tab order.
  function buildRun(isDuplicate) {
    var hide = isDuplicate ? ' aria-hidden="true"' : "";
    var html = ['<span class="marquee-label"' + hide + ">Past Guests</span>"];
    guests.forEach(function (g) {
      html.push(
        '<a class="marquee-name" href="' + escHtml(g.href) + '"' +
        (isDuplicate
          ? ' aria-hidden="true" tabindex="-1"'
          : ' aria-label="' + escHtml("Listen to the episode with " + g.name) + '"') +
        ">" + escHtml(g.name) + "</a>"
      );
    });
    return html.join("");
  }
  track.innerHTML = buildRun(false) + buildRun(true);
})();
