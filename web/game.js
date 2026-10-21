/* The Defiant Jazz Incident, web version.
 *
 * The same flow as the terminal game (game/engine.py): title, cold open, the
 * suspects' statements, then a hub where the player investigates, reviews and
 * accuses. The AI lives beside the game: the hub offers example questions to
 * copy into Grafana Assistant or the player's own agent.
 *
 * The story is told in full-image panels: each story card is a few panels, each one
 * picture with a short headline, a line or two of caption and the spoken lines, stepped
 * through with Next panel. The panels come from game/SPOILERS-content/scene-art.md and
 * the rest of the story text from SPOILERS-content.js, both bundled by web/build.py. The
 * reveal stays encoded until the player accuses and confirms.
 *
 * The same script runs as a static page and as a Grafana Page (web/build.py --page).
 * A Page runs in a sandboxed frame with no forms, modals or localStorage, so the game
 * uses click handlers rather than form submits, and a host set up before this script
 * (window.DJ_HOST) can supply, each optionally:
 *   storage.getItem(key) / storage.setItem(key, value)  saved progress, may return promises
 *   onTheme(callback)          calls callback("dark" | "light") whenever the host's theme changes
 *   askAssistant(prompt)       opens Grafana Assistant with the prompt; returns a promise
 *   scenes                     the pictures as { name: URL }, for a frame that can't load files
 */
(function () {
  "use strict";

  var C = window.DJ_CONTENT;
  var HOST = window.DJ_HOST || {};
  var STORE_KEY = "defiantjazz.web.v1";
  var THEME_KEY = "defiantjazz.theme";
  var LEADS = C.decisions.length;

  // Examples only: the player asks whatever they like, in whichever AI they like.
  // The loader can move the data to just before the load, so these avoid clock times.
  var QUESTIONS = [
    "The Kipsake Sleep Floor telemetry is in this stack, under service_namespace " +
      "\"kipsake-sleep-floor\" in Loki, Prometheus and Tempo. During a five-minute power " +
      "outage on the night shift, Night Supervisor Mr. Hale was killed in the elevator. Who killed Mr. Hale?",
    "When did the Sleep Floor lose power, and what happened in the minutes before?",
    "What happened near the elevator while the power was out?",
  ];

  var LINKS = [
    ["Grafana Assistant", "https://grafana.com/docs/grafana-cloud/machine-learning/assistant/"],
    ["Grafana MCP server", "https://github.com/grafana/mcp-grafana"],
  ];

  // Pixel-art pictures in assets/, made by web/build.py --art. C.pictures gives every picture's
  // size as name: [width, height]; a panel whose picture is still to come (C.toCome) shows a
  // placeholder the same shape. Alt text is empty: the story stays in the HTML, and words drawn
  // in a picture are in its panel's transcript.
  var TITLE_ART = "title-splash";
  var REVEAL_ART = "scene-reveal";
  var PORTRAITS = { agnes: "portrait-agnes", bertram: "portrait-bertram", clement: "portrait-clement" };
  var LEAD_ICONS = ["search", "home", "chat"];

  var main = document.getElementById("main");
  var leadsEl = document.getElementById("leads");
  var restartBtn = document.getElementById("restart");
  var themeBtn = document.getElementById("theme-toggle");
  var statusEl = document.getElementById("status");
  var dialog = document.getElementById("restart-dialog");

  // ---- state ----------------------------------------------------------------

  function fresh() {
    return {
      view: "title",   // title, advert, cold, statement, hub, outside, lead, result, card, accuse, confirm, verdict
      step: 0,         // statement number or verdict page
      frame: 0,        // panel of the card on screen
      chosen: [],      // option index picked for each lead, in order
      outsideShown: false,
      reviewing: 0,    // index into reviewItems() for the card view
      picking: null,   // option highlighted on the lead view
      draft: { suspect: "", other: "", reasoning: "" },
      accused: null,   // { key, label } once the player has confirmed
      reasoning: "",
    };
  }

  // ---- storage ----------------------------------------------------------------
  // localStorage on a static page, or the host's store. Either may be missing or fail:
  // the game then plays on without saving.

  var storage = HOST.storage || {
    getItem: function (key) { return localStorage.getItem(key); },
    setItem: function (key, value) { localStorage.setItem(key, value); },
  };

  function noop() {}

  // Resolves to the stored text, or null when there's none, storage fails, or a host
  // store takes more than a few seconds to answer.
  function readStored(key) {
    var read = new Promise(function (resolve) { resolve(storage.getItem(key)); }).catch(function () { return null; });
    var late = new Promise(function (resolve) { setTimeout(function () { resolve(null); }, 5000); });
    return Promise.race([read, late]);
  }

  // One write at a time, and only the newest pending one: a host store is a round trip.
  var writing = false, pending = null;
  function writeStored(key, value) {
    pending = [key, value];
    if (writing) return;
    writing = true;
    (function next() {
      if (!pending) { writing = false; return; }
      var w = pending;
      pending = null;
      new Promise(function (resolve) { resolve(storage.setItem(w[0], w[1])); }).catch(noop).then(next);
    })();
  }

  function load(text) {
    var s = fresh();
    try {
      var saved = JSON.parse(text || "null");
      if (saved && typeof saved === "object") Object.assign(s, saved);
    } catch (e) { /* nothing usable: start fresh */ }
    // Drop anything that doesn't fit the content (for example after the cards change).
    var ok = Array.isArray(s.chosen) && s.chosen.length <= LEADS && s.chosen.every(function (v, i) {
      return Number.isInteger(v) && v >= 0 && v < C.decisions[i].options.length;
    });
    if (!ok) return fresh();
    if (!s.draft || typeof s.draft !== "object") s.draft = fresh().draft;
    if (!s.accused && (s.view === "verdict")) s.view = "hub";
    if (s.accused && s.view !== "verdict") s.view = "verdict";
    return s;
  }

  var state = fresh();

  function save() {
    writeStored(STORE_KEY, JSON.stringify(state));
  }

  // Every move starts on the first panel of what it shows, unless it says otherwise.
  function go(view, extra, opts) {
    state.view = view;
    state.frame = 0;
    if (extra) Object.assign(state, extra);
    save();
    render(opts && opts.keepFocus ? false : true);
  }

  // ---- small DOM helpers ------------------------------------------------------

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        var v = attrs[k];
        if (v === null || v === undefined || v === false) return;
        if (k === "text") node.textContent = v;
        else if (k === "onclick") node.addEventListener("click", v);
        else if (k === "class") node.className = v;
        else node.setAttribute(k, v === true ? "" : v);
      });
    }
    [].concat(children || []).forEach(function (c) {
      if (c === null || c === undefined || c === false) return;
      node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return node;
  }

  function button(label, onclick, cls, attrs) {
    return el("button", Object.assign({ type: "button", class: "btn " + (cls || ""), onclick: onclick }, attrs), label);
  }

  // A button with a small icon before its label.
  function iconButton(name, label, onclick, cls, attrs) {
    return button([icon(name), el("span", null, label)], onclick, cls, attrs);
  }

  function rule(label) {
    return el("div", { class: "rule", "aria-hidden": "true" }, label || "");
  }

  function heading(text, level) {
    return el("h" + (level || 2), { tabindex: "-1" }, text);
  }

  // Line icons, drawn inline: the page loads nothing from the network.
  var ICONS = {
    search: "M10.5 3a7.5 7.5 0 1 0 4.6 13.4l4.7 4.7 1.4-1.4-4.7-4.7A7.5 7.5 0 0 0 10.5 3zm0 2a5.5 5.5 0 1 1 0 11 5.5 5.5 0 0 1 0-11z",
    home: "M12 3 2 11.5l1.3 1.5L5 11.6V20a1 1 0 0 0 1 1h4v-6h4v6h4a1 1 0 0 0 1-1v-8.4l1.7 1.4 1.3-1.5zm5 16h-1v-6H8v6H7v-9.1l5-4.3 5 4.3z",
    chat: "M4 4h16a1 1 0 0 1 1 1v11a1 1 0 0 1-1 1H9l-5 4v-4H4a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1zm1 2v9h1v2.1L8.4 15H19V6z",
    spark: "M12 2l2 6 6 2-6 2-2 6-2-6-6-2 6-2zm7 12 1 3 3 1-3 1-1 3-1-3-3-1 3-1z",
    copy: "M8 3h11a1 1 0 0 1 1 1v13h-2V5H8zM5 7h10a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V8a1 1 0 0 1 1-1zm1 2v10h8V9z",
    eye: "M12 5c5 0 9 4.5 10 7-1 2.5-5 7-10 7S3 14.5 2 12c1-2.5 5-7 10-7zm0 2c-3.6 0-6.6 3-7.8 5 1.2 2 4.2 5 7.8 5s6.6-3 7.8-5c-1.2-2-4.2-5-7.8-5zm0 2a3 3 0 1 1 0 6 3 3 0 0 1 0-6z",
    accuse: "M12 2a5 5 0 0 1 5 5c0 2.8-2.2 5-5 5S7 9.8 7 7a5 5 0 0 1 5-5zm0 2a3 3 0 1 0 0 6 3 3 0 0 0 0-6zM4 21c0-4.4 3.6-7 8-7s8 2.6 8 7h-2c0-3.2-2.7-5-6-5s-6 1.8-6 5z",
    next: "M13.2 5.3 19.9 12l-6.7 6.7-1.4-1.4 4.3-4.3H4v-2h12.1l-4.3-4.3z",
    prev: "M10.8 5.3 4.1 12l6.7 6.7 1.4-1.4L7.9 13H20v-2H7.9l4.3-4.3z",
    check: "M9.5 16.2 5.3 12l-1.4 1.4 5.6 5.6L20.1 8.4 18.7 7z",
    lock: "M12 2a5 5 0 0 1 5 5v3h1a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V11a1 1 0 0 1 1-1h1V7a5 5 0 0 1 5-5zm0 2a3 3 0 0 0-3 3v3h6V7a3 3 0 0 0-3-3zm-5 8v8h10v-8z",
  };

  function icon(name) {
    var ns = "http://www.w3.org/2000/svg";
    var svg = document.createElementNS(ns, "svg");
    svg.setAttribute("viewBox", "0 0 24 24");
    svg.setAttribute("class", "icon");
    svg.setAttribute("aria-hidden", "true");
    var path = document.createElementNS(ns, "path");
    path.setAttribute("d", ICONS[name]);
    svg.appendChild(path);
    return svg;
  }

  var toastTimer = null;
  function announce(text) {
    statusEl.textContent = text;
    statusEl.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { statusEl.classList.remove("show"); }, 4500);
  }

  // ---- card text ----------------------------------------------------------------
  // The card format is described in game/content.py: "[...]" lines describe what's on
  // screen, "> ..." lines are text shown on screen, "Name: ..." lines are spoken.

  var SPEAKER = /^([A-Z][A-Za-z.' ]{0,24}): /;
  var BULLET = /^([-*•]|\d+[.)])\s+/;
  var TAGS = { "**": "strong", "*": "em", "~~": "s" };

  function inline(text, parent) {
    var stack = [[null, parent]];
    text.split(/(\*\*|~~|\*)/).forEach(function (piece) {
      if (!piece) return;
      var top = stack[stack.length - 1];
      if (TAGS[piece]) {
        var open = stack.findIndex(function (s) { return s[0] === piece; });
        if (open > 0) { stack.length = open; return; }
        var node = el(TAGS[piece]);
        if (piece === "~~") node.appendChild(el("span", { class: "sr-only" }, "crossed out: "));
        top[1].appendChild(node);
        stack.push([piece, node]);
        return;
      }
      top[1].appendChild(document.createTextNode(piece));
    });
    return parent;
  }

  // The investigator's lines on one side of a panel, everyone else's on the other.
  function cardBody(text) {
    var root = el("div", { class: "card-body" });
    var group = null; // the open <ul>, <ol> or screen block
    function into(kind, make) {
      if (!group || group.kind !== kind) { group = { kind: kind, node: make() }; root.appendChild(group.node); }
      return group.node;
    }
    text.split("\n").forEach(function (raw) {
      var line = raw.replace(/\s+$/, "");
      var stripped = line.replace(/^\s+/, "");
      if (!stripped) { group = null; return; }
      var bullet = stripped.match(BULLET);
      if (line.charAt(0) === "[" && line.slice(-1) === "]") {
        group = null;
        root.appendChild(inline(line.slice(1, -1), el("p", { class: "stage" })));
      } else if (line.charAt(0) === ">") {
        into("screen", function () { return el("div", { class: "screen" }); })
          .appendChild(inline(line.slice(1).trim(), el("div")));
      } else if (bullet) {
        var kind = /\d/.test(bullet[1]) ? "ol" : "ul";
        into(kind, function () { return el(kind); })
          .appendChild(inline(stripped.slice(bullet[0].length), el("li")));
      } else if (SPEAKER.test(line)) {
        group = null;
        var name = line.match(SPEAKER)[1];
        var p = el("p", { class: "speech" + (name === "You" ? " speech-you" : "") },
          el("span", { class: "speaker" }, name + ":"));
        p.appendChild(document.createTextNode(" "));
        root.appendChild(inline(line.slice(name.length + 2), p));
      } else {
        group = null;
        root.appendChild(inline(stripped, el("p")));
      }
    });
    return root;
  }

  // ---- hotspots --------------------------------------------------------------------
  // Numbered markers on the picture. Hovering, focusing or tapping one shows its note; a click
  // or tap keeps it open until the next click, a click elsewhere or Escape. One note at a time.

  var openSpot = null; // { button, note, pinned, hovered }
  var spotIds = 0;

  function showSpot(spot, pin) {
    if (openSpot && openSpot !== spot) hideSpot();
    if (pin) spot.pinned = true;
    if (openSpot === spot) return;
    openSpot = spot;
    spot.note.hidden = false;
    spot.button.setAttribute("aria-expanded", "true");
    placeSpot(spot);
  }

  function hideSpot() {
    if (!openSpot) return;
    openSpot.note.hidden = true;
    openSpot.button.setAttribute("aria-expanded", "false");
    openSpot.pinned = false;
    openSpot = null;
  }

  // Beside the marker, inside the picture's width, below it or above it, wherever it fits.
  function placeSpot(spot) {
    var b = spot.button, note = spot.note;
    note.style.left = "0px";
    note.style.top = "0px";
    var width = b.parentNode.clientWidth, w = note.offsetWidth, h = note.offsetHeight;
    var centre = b.offsetLeft + b.offsetWidth / 2;
    note.style.left = Math.max(0, Math.min(width - w, centre - w / 2)) + "px";
    var box = b.getBoundingClientRect();
    var below = window.innerHeight - box.bottom, above = box.top;
    var down = below >= h + 8 || below >= above;
    note.style.top = (down ? b.offsetTop + b.offsetHeight + 6 : b.offsetTop - h - 6) + "px";
  }

  function hotspot(h, i) {
    var id = "spot" + (++spotIds);
    var text = cardBody(h.body);
    text.id = id;
    var note = el("div", { class: "hotspot-note", hidden: true }, [
      el("p", { class: "hotspot-label", "aria-hidden": "true" }, (i + 1) + ". " + h.label),
      text,
    ]);
    var button = el("button", {
      type: "button", class: "hotspot", "aria-label": (i + 1) + ". " + h.label,
      "aria-expanded": "false", "aria-describedby": id,
    }, String(i + 1));
    // Set through the style object, not a style attribute: the page's CSP allows only that.
    button.style.left = h.x + "%";
    button.style.top = h.y + "%";
    var spot = { button: button, note: note, pinned: false, hovered: false };
    button.addEventListener("pointerenter", function (e) {
      if (e.pointerType !== "mouse") return;
      spot.hovered = true;
      if (!openSpot || !openSpot.pinned) showSpot(spot);
    });
    button.addEventListener("pointerleave", function (e) {
      if (e.pointerType !== "mouse") return;
      spot.hovered = false;
      if (openSpot === spot && !spot.pinned && document.activeElement !== button) hideSpot();
    });
    button.addEventListener("focus", function () { showSpot(spot); });
    // A kept note stays open while its text is clicked (focus goes nowhere), not when focus moves on.
    button.addEventListener("blur", function (e) {
      if (openSpot === spot && !spot.hovered && (!spot.pinned || e.relatedTarget)) hideSpot();
    });
    button.addEventListener("click", function () {
      if (openSpot === spot && spot.pinned) hideSpot(); else showSpot(spot, true);
    });
    return [button, note];
  }

  document.addEventListener("click", function (e) {
    if (openSpot && !openSpot.button.contains(e.target) && !openSpot.note.contains(e.target)) hideSpot();
  });
  window.addEventListener("resize", function () { if (openSpot) placeSpot(openSpot); });

  // ---- pictures and panels ------------------------------------------------------------

  function hasPicture(name) { return !!name && name in C.pictures && C.toCome.indexOf(name) < 0; }

  function picture(name) {
    var size = C.pictures[name];
    var src = (HOST.scenes && HOST.scenes[name]) || "assets/" + name + ".webp";
    return el("img", { src: src, alt: "", width: size[0], height: size[1], decoding: "async" });
  }

  // A small crop of a picture for a button, or a plain tile when there's no picture yet.
  function thumb(name) {
    return el("span", { class: "thumb" + (hasPicture(name) ? "" : " thumb-empty"), "aria-hidden": "true" },
      hasPicture(name) ? picture(name) : null);
  }

  function framesOf(c) { return C.art[c.title]; }

  // A panel's text, less the lines marked "(drawn)": words the picture shows legibly. They
  // aren't repeated under it, but stay a click away, for a small screen or a screen reader;
  // under a picture with nothing else to say (the flyer), only screen readers get them.
  // Without the picture yet, they show like the rest.
  var DRAWN = /^\(drawn\) /;
  function panelText(frame, pictured) {
    var lines = frame.body.split("\n");
    var drawn = lines.filter(function (l) { return DRAWN.test(l); });
    if (!pictured || !drawn.length) return cardBody(lines.map(function (l) { return l.replace(DRAWN, ""); }).join("\n"));
    var rest = lines.filter(function (l) { return !DRAWN.test(l); }).join("\n");
    var copy = cardBody(drawn.map(function (l) { return l.replace(DRAWN, ""); }).join("\n"));
    if (!rest.trim()) return el("div", { class: "sr-only" }, copy);
    var body = cardBody(rest);
    body.appendChild(el("details", { class: "drawn" }, [el("summary", null, "Text in the picture"), copy]));
    return body;
  }

  // The panel's list as tiles, each led by an icon for its first word (ask, investigate, accuse).
  var ROLE_ICONS = { ask: "spark", investigate: "search", accuse: "accuse" };
  function roleBody(text) {
    var body = cardBody(text);
    var list = body.querySelector("ul");
    if (list) {
      list.className = "role-tiles";
      [].forEach.call(list.children, function (li) {
        var word = (li.querySelector("strong") || li).textContent.toLowerCase();
        if (ROLE_ICONS[word]) li.insertBefore(icon(ROLE_ICONS[word]), li.firstChild);
      });
    }
    return body;
  }

  // One full-image panel: the picture (or a placeholder the same shape) with where we are,
  // the headline and what we hear over it, the hotspots on it, and its text under it.
  function panel(frame) {
    var name = frame.image;
    var size = name ? C.pictures[name] : [1200, 400];
    var pic = el("div", { class: "panel-pic" });
    pic.style.aspectRatio = size[0] + " / " + size[1];
    // The whole picture, never cropped: one taller than the 3:1 panels is narrower, to fit the screen.
    pic.style.maxWidth = "calc(" + (72 * size[0] / size[1]).toFixed(1) + "vh)";
    var pictured = hasPicture(name);
    if (!name) {
      pic.classList.add("panel-black");
    } else if (pictured) {
      pic.appendChild(picture(name));
      frame.hotspots.forEach(function (h, i) { hotspot(h, i).forEach(function (n) { pic.appendChild(n); }); });
    } else {
      // Art to come: the same frame, and a quiet label. The file to add is in data-picture.
      pic.classList.add("panel-placeholder");
      pic.setAttribute("data-picture", name);
      pic.appendChild(el("span", { class: "placeholder-label", "aria-hidden": "true" }, "Illustration to come"));
    }
    if (frame.dim) pic.classList.add("panel-dim");
    if (frame.sound) pic.appendChild(el("p", { class: "panel-sound" }, frame.sound));
    var head = frame.where || frame.headline ? el("div", { class: "panel-head" }, [
      frame.where ? el("p", { class: "panel-where" }, frame.where) : null,
      frame.headline ? heading(frame.headline) : null,
    ]) : null;
    var text = null;
    if (frame.body) text = frame.style === "role" ? roleBody(frame.body) : panelText(frame, pictured);
    var quiet = text && text.classList.contains("sr-only");
    return el("figure", { class: "panel" + (frame.style ? " panel-" + frame.style : "") }, [
      // "Your role" has no picture: its headline sits over its tiles.
      el("div", { class: "panel-art" + (head ? " has-head" : "") }, [head, frame.style === "role" ? null : pic]),
      text ? el("figcaption", { class: quiet ? null : "panel-text" }, text) : null,
    ]);
  }

  // Steps through a card's panels. opts: label (over the panel), intro (a line above it),
  // done (the buttons on the last panel), always (buttons on every panel).
  var keyNav = null;
  function player(c, opts) {
    var frames = framesOf(c);
    var i = Math.min(Math.max(state.frame | 0, 0), frames.length - 1);
    var last = i === frames.length - 1;
    function to(n) { state.frame = n; save(); render(true); }
    keyNav = function (step) {
      var n = i + step;
      if (n >= 0 && n < frames.length) to(n);
    };
    var nav = i > 0 ? [iconButton("prev", "Previous panel", function () { to(i - 1); }, "btn-quiet-console")] : [];
    var next = last ? opts.done || [] : [button([el("span", null, "Next panel"), icon("next")], function () { to(i + 1); }, "btn-primary btn-next")];
    return el("section", { class: "player" }, [
      el("div", { class: "chapterbar" }, [
        el("span", null, opts.label),
        frames.length > 1 ? el("span", { class: "chapter-count" }, "Panel " + (i + 1) + " of " + frames.length) : null,
      ]),
      opts.intro && i === 0 ? el("p", { class: "lede player-intro" }, opts.intro) : null,
      panel(frames[i]),
      el("div", { class: "framebar" }, [
        el("div", { class: "framebar-nav" }, nav),
        el("div", { class: "framebar-actions" }, (opts.always || []).concat(next)),
      ]),
    ]);
  }

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && openSpot) { hideSpot(); e.preventDefault(); return; }
    if (!keyNav || e.altKey || e.ctrlKey || e.metaKey || (dialog && dialog.open)) return;
    if (/^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName)) return;
    if (e.key === "ArrowRight") { keyNav(1); e.preventDefault(); }
    else if (e.key === "ArrowLeft") { keyNav(-1); e.preventDefault(); }
  });

  // A text card (the verdict): a heading and the card's text, as written.
  function card(c, title, ruleLabel) {
    return el("article", { class: "story text-card" }, [
      ruleLabel ? rule(ruleLabel) : null,
      heading(title || c.title),
      cardBody(c.body),
    ]);
  }

  // ---- game helpers -------------------------------------------------------------

  function leadTitle(n) { return C.decisions[n].title.split(" · ").slice(1).join(" · ") || C.decisions[n].title; }
  function chosenCard(n) { return C.decisions[n].options[state.chosen[n]]; }
  function leadsLeft() { return LEADS - state.chosen.length; }

  function leadsLine() {
    var n = state.chosen.length;
    if (n < LEADS) return "Leads left: " + (LEADS - n) + " of " + LEADS + " · next: " + C.leadKinds[n];
    return "Leads left: 0 of " + LEADS + " · all three leads used";
  }

  function reviewItems() {
    var items = [["The Kipsake advert", C.advert], ["Cold open", C.coldOpen]];
    C.testimonies.forEach(function (t) { items.push([t.title, t]); });
    if (state.outsideShown) items.push(["Outside World handout", C.outsideWorld]);
    state.chosen.forEach(function (_, n) {
      var c = chosenCard(n);
      items.push(["Lead " + (n + 1) + " · " + c.title, c]);
    });
    return items;
  }

  function firstPicture(c) {
    var withArt = framesOf(c).filter(function (f) { return f.image; });
    return withArt.length ? withArt[0].image : null;
  }

  function normalizeName(text) { return text.toLowerCase().replace(/[^a-z ]/g, "").trim(); }

  function investigate() {
    var n = state.chosen.length;
    if (n >= LEADS) return go("hub");
    if (n === 1 && !state.outsideShown) return go("outside", { outsideShown: true });
    go("lead", { picking: null });
  }

  function decodeReveal() {
    var bytes = Uint8Array.from(atob(C.reveal), function (ch) { return ch.charCodeAt(0); });
    return JSON.parse(new TextDecoder().decode(bytes));
  }

  // ---- clipboard --------------------------------------------------------------------
  // Inside a dashboard iframe the async clipboard API is often blocked, so fall back to
  // execCommand. copyText resolves to whether either worked.

  function execCopy(text) {
    var ok = false, active = document.activeElement;
    try {
      var ta = el("textarea", { readonly: true, "aria-hidden": "true" });
      ta.value = text;
      ta.style.position = "fixed";
      ta.style.top = "0";
      ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      ok = document.execCommand("copy");
      ta.remove();
    } catch (e) { ok = false; }
    if (active && active.focus) active.focus();
    return ok;
  }

  function copyText(text) {
    // execCommand first, while the click still counts as the player's: the async API can
    // take its time to refuse, and by then the fallback may no longer be allowed.
    if (execCopy(text)) return Promise.resolve(true);
    if (!navigator.clipboard || !window.isSecureContext) return Promise.resolve(false);
    return navigator.clipboard.writeText(text).then(function () { return true; }, function () { return false; });
  }

  function copy(text, sourceNode) {
    copyText(text).then(function (ok) {
      if (ok) return announce("Copied. Paste it into Grafana Assistant or your own AI.");
      selectText(sourceNode);
      announce("Couldn't copy from here. The question is selected: press Ctrl+C (⌘C on a Mac).");
    });
  }

  function selectText(node) {
    try {
      var range = document.createRange();
      range.selectNodeContents(node);
      var sel = window.getSelection();
      sel.removeAllRanges();
      sel.addRange(range);
    } catch (e) { /* nothing more to try */ }
  }

  // Inside a Grafana Page: one click copies the question where the frame allows it, and opens
  // Grafana Assistant with it filled in. A page can't send it for the player: Assistant opens
  // it as a draft, so the player presses Enter. Only the question goes, never story text.
  function ask(text, sourceNode) {
    var copied = copyText(text);
    Promise.resolve().then(function () { return HOST.askAssistant(text); }).then(function () {
      return copied.then(function (ok) {
        announce("The question is in Grafana Assistant: press Enter to send it." + (ok ? " It's copied too." : ""));
      });
    }, function () {
      return copied.then(function (ok) {
        if (!ok) selectText(sourceNode);
        announce("Couldn't open Grafana Assistant. " + (ok
          ? "The question is copied: paste it into Assistant."
          : "The question is selected: press Ctrl+C (⌘C on a Mac) to copy it."));
      });
    });
  }

  // ---- views ----------------------------------------------------------------------------

  var views = {};

  views.title = function () {
    var resume = state.chosen.length > 0;
    // The title sits on the key art's quiet left half, or under it on a narrow screen.
    return el("section", { class: "title-view" }, el("div", { class: "title-art" }, [
      picture(TITLE_ART),
      el("div", { class: "title-text" }, [
        el("h1", { class: "sr-only" }, "The Defiant Jazz Incident"),
        el("pre", { class: "banner", "aria-hidden": "true" }, C.banner),
        el("p", { class: "lede" }, "An observability murder mystery on the Sleep Floor at Kipsake."),
        el("div", { class: "actions" }, [
          button([el("span", null, resume ? "Continue" : "Start"), icon("next")],
            function () { go(resume ? "hub" : "advert"); }, "btn-primary btn-next"),
        ]),
      ]),
    ]));
  };

  views.advert = function () {
    return player(C.advert, {
      label: "Cold open",
      done: [button([el("span", null, "Continue"), icon("next")], function () { go("cold"); }, "btn-primary btn-next")],
    });
  };

  views.cold = function () {
    return player(C.coldOpen, {
      label: "Cold open",
      done: [button([el("span", null, "Start the interviews"), icon("next")],
        function () { go("statement", { step: 0 }); }, "btn-primary btn-next")],
    });
  };

  views.statement = function () {
    var i = Math.min(Math.max(state.step | 0, 0), C.testimonies.length - 1);
    var last = i === C.testimonies.length - 1;
    return player(C.testimonies[i], {
      label: "Interviews · " + (i + 1) + " of " + C.testimonies.length,
      intro: i === 0 ? C.testimonyIntro : null,
      done: [
        button([el("span", null, last ? "On to the case" : "Next interview"), icon("next")], function () {
          if (last) go("hub"); else go("statement", { step: i + 1 });
        }, "btn-primary btn-next"),
        i > 0 ? button("Previous interview", function () { go("statement", { step: i - 1 }); }, "btn-quiet-console") : null,
      ],
    });
  };

  // The three leads as a track: used (with what you picked), next, or still to come.
  function leadTrack() {
    var n = state.chosen.length;
    return el("ol", { class: "lead-track", "aria-label": leadsLine() }, C.leadKinds.map(function (kind, i) {
      var status = i < n ? chosenCard(i).title : i === n ? "Next" : "Later";
      var cls = i < n ? "used" : i === n ? "next" : "later";
      return el("li", { class: "lead-step lead-" + cls }, [
        el("span", { class: "lead-icon" }, icon(i < n ? "check" : LEAD_ICONS[i])),
        el("span", { class: "lead-words" }, [
          el("small", null, "Lead " + (i + 1)),
          el("span", { class: "lead-kind" }, kind),
          el("span", { class: "lead-status" }, status),
        ]),
      ]);
    }));
  }

  views.hub = function () {
    var n = state.chosen.length;

    var inv = el("section", { class: "console area-inv", "aria-labelledby": "h-inv" }, [
      el("div", { class: "console-bar" }, [el("span", { class: "dot" }), "Investigate"]),
      el("div", { class: "console-body" }, [
        el("h3", { id: "h-inv" }, n < LEADS ? leadsLeft() + " of " + LEADS + " leads left" : "All three leads followed"),
        leadTrack(),
        el("p", { class: "note" }, n < LEADS
          ? "Follow up your leads in order, whenever you like. Each time, you pick one of three options and see only that one."
          : "You've followed up all three leads. When you're ready, accuse the killer."),
        n < LEADS ? el("div", { class: "actions" }, [
          iconButton(LEAD_ICONS[n], "Investigate lead " + (n + 1) + ": " + C.leadKinds[n], investigate, "btn-primary"),
        ]) : null,
      ]),
    ]);

    var list = el("ol", { class: "questions" });
    QUESTIONS.forEach(function (q, i) {
      var text = el("span", { class: "q", id: "q" + i }, q);
      var btn = HOST.askAssistant
        ? iconButton("spark", "Ask Assistant", function () { ask(q, text); }, "btn-console", { "aria-describedby": "q" + i })
        : iconButton("copy", "Copy", function () { copy(q, text); }, "btn-console", { "aria-describedby": "q" + i });
      list.appendChild(el("li", null, [el("span", { class: "q-mark", "aria-hidden": "true" }, "❯"), text, btn]));
    });
    var ai = el("section", { class: "console area-ai", "aria-labelledby": "h-ai" }, [
      el("div", { class: "console-bar" }, [el("span", { class: "dot" }), "Ask your AI"]),
      el("div", { class: "console-body" }, [
        el("h3", { id: "h-ai" }, "It has read Kipsake's records, and nothing else"),
        el("p", null, "Ask Grafana Assistant in this Grafana, or your own AI agent through the Grafana MCP " +
          "server or gcx. It hasn't seen the interviews, the leads you follow, or anything you find. " +
          "If you want it to know something, tell it."),
        el("p", { class: "note" }, "Ask it anything. If you're not sure where to start:"),
        list,
        HOST.askAssistant ? el("p", { class: "note" }, "Ask Assistant opens Grafana Assistant with the question " +
          "filled in, ready to send with Enter, and copies it where the page is allowed to. " +
          "Using your own AI? Select a question and copy it.") : null,
        el("p", { class: "note" }, "The data's times are UTC. If it was loaded on an incident date, the " +
          "story's 03:02 is 03:02 in Grafana set to UTC. If it was loaded to end just before the load, " +
          "03:02 is a different clock time there. Either way, your AI can find the outage in the data."),
        el("p", { class: "note" }, ["Learn more: "].concat(LINKS.map(function (l, i) {
          return [i ? " · " : "", el("a", { href: l[1], target: "_blank", rel: "noopener noreferrer" }, l[0])];
        }).flat(), [" (opens in a new tab)"])),
      ]),
    ]);

    var items = reviewItems();
    var review = el("section", { class: "console area-review", "aria-labelledby": "h-review" }, [
      el("div", { class: "console-bar" }, [el("span", { class: "dot" }), "Review"]),
      el("div", { class: "console-body" }, [
        el("h3", { id: "h-review" }, "Everything you've seen"),
        el("ul", { class: "review-tiles" }, items.map(function (item, i) {
          return el("li", null, el("button", {
            type: "button", class: "review-tile", onclick: function () { go("card", { reviewing: i }); },
          }, [
            thumb(firstPicture(item[1])),
            el("small", { "aria-hidden": "true" }, (i < 9 ? "0" : "") + (i + 1)),
            el("span", null, item[0]),
          ]));
        })),
      ]),
    ]);

    var accuse = el("section", { class: "console area-accuse", "aria-labelledby": "h-accuse" }, [
      el("div", { class: "console-bar" }, [el("span", { class: "dot dot-alert" }), "Accuse"]),
      el("div", { class: "console-body" }, [
        el("h3", { id: "h-accuse" }, "Who killed Mr. Hale?"),
        el("div", { class: "suspect-strip", "aria-hidden": "true" }, Object.keys(C.suspects).map(function (key) {
          return el("span", { class: "suspect-mini" }, [thumb(PORTRAITS[key]), el("span", null, C.suspects[key])]);
        })),
        el("p", { class: "note" }, "When you're ready, name the killer and say why. You can do this any " +
          "time, even before all three leads. It ends the game."),
        el("div", { class: "actions" }, [iconButton("accuse", "Accuse…", function () { go("accuse"); }, "btn-alert")]),
      ]),
    ]);

    return el("section", { class: "hub" }, [
      el("div", { class: "chapterbar" }, [el("span", null, "Your turn"), el("span", null, "Incident File SF-1008")]),
      heading("The case"),
      el("p", { class: "lede" }, "Ask your AI anything. You have three leads to follow up, " +
        "one at a time, whenever you like. When you're ready, accuse the killer and say why."),
      el("div", { class: "hub-grid" }, [inv, ai, accuse, review]),
    ]);
  };

  views.outside = function () {
    return player(C.outsideWorld, {
      label: "Outside World handout",
      intro: "Before the next lead, a handout from outside Kipsake.",
      done: [button([el("span", null, "Continue to lead 2"), icon("next")],
        function () { go("lead", { picking: null }); }, "btn-primary btn-next")],
    });
  };

  // The lead's three options as big buttons: pick one, then follow it.
  views.lead = function () {
    var n = state.chosen.length;
    if (n >= LEADS) return views.hub();
    var d = C.decisions[n];
    var error = el("p", { class: "error", role: "alert" });
    var follow = button([el("span", null, "Follow this lead"), icon("next")], function () {
      if (state.picking === null || state.picking === undefined) { error.textContent = "Pick one of the three."; return; }
      go("result", { chosen: state.chosen.concat([state.picking]), picking: null });
    }, "btn-primary btn-next");
    var options = d.options.map(function (opt, i) {
      var picked = state.picking === i;
      return el("button", {
        type: "button", class: "option", "aria-pressed": picked ? "true" : "false",
        onclick: function () {
          state.picking = i;
          error.textContent = "";
          save();
          [].forEach.call(group.children, function (b, j) { b.setAttribute("aria-pressed", j === i ? "true" : "false"); });
        },
      }, [
        el("span", { class: "option-number", "aria-hidden": "true" }, String(i + 1)),
        el("span", { class: "option-words" }, [
          el("strong", null, opt.meta.option),
          opt.meta.note ? el("span", { class: "hint" }, opt.meta.note) : null,
        ]),
      ]);
    });
    var group = el("div", { class: "options", role: "group", "aria-labelledby": "lead-legend" }, options);
    return el("section", { class: "player" }, [
      el("div", { class: "chapterbar" }, [el("span", null, "Lead " + (n + 1) + " of " + LEADS), el("span", null, C.leadKinds[n])]),
      el("div", { class: "console decision" }, [
        el("div", { class: "console-bar" }, [el("span", { class: "dot" }), icon(LEAD_ICONS[n]), leadTitle(n)]),
        el("div", { class: "console-body" }, [
          heading(leadTitle(n)),
          cardBody(d.prompt),
          el("p", { class: "legend", id: "lead-legend" }, "Choose one. You'll see only the one you pick."),
          group,
          error,
          el("div", { class: "actions" }, [
            follow,
            button("Decide later", function () { go("hub"); announce("No rush. Investigate when you're ready."); }, "btn-quiet-console"),
          ]),
        ]),
      ]),
    ]);
  };

  views.result = function () {
    var n = state.chosen.length - 1;
    if (n < 0) return views.hub();
    var c = chosenCard(n);
    var more = n < LEADS - 1;
    return player(c, {
      label: "Lead " + (n + 1) + " of " + LEADS + " · " + c.title,
      done: [
        el("p", { class: "lede framebar-note" }, more
          ? "Ask your AI about anything here, or investigate again (lead " + (n + 2) + ": " + C.leadShort[n + 1] + ")."
          : "That was the last lead. Ask your AI anything else, then accuse."),
        button([el("span", null, "Back to the case"), icon("next")], function () { go("hub"); }, "btn-primary btn-next"),
        more ? button("Investigate lead " + (n + 2), investigate, "btn-quiet-console")
          : button("Accuse…", function () { go("accuse"); }, "btn-quiet-console"),
      ],
    });
  };

  views.card = function () {
    var items = reviewItems();
    var i = Math.min(Math.max(state.reviewing | 0, 0), items.length - 1);
    return player(items[i][1], {
      label: "Review · " + (i + 1) + " of " + items.length + " · " + items[i][0],
      done: [
        i < items.length - 1 ? button([el("span", null, "Next: " + items[i + 1][0]), icon("next")],
          function () { go("card", { reviewing: i + 1 }); }, "btn-primary btn-next") : null,
        i > 0 ? button("Previous card", function () { go("card", { reviewing: i - 1 }); }, "btn-quiet-console") : null,
      ],
      always: [button("Back to the case", function () { go("hub"); }, i < items.length - 1 ? "btn-quiet-console" : "btn-primary")],
    });
  };

  function accusation() {
    var d = state.draft;
    if (d.suspect && d.suspect !== "other") return { key: d.suspect, label: C.suspects[d.suspect] };
    if (d.suspect !== "other") return null;
    var name = (d.other || "").trim();
    if (!name) return null;
    var key = C.aliases[normalizeName(name)];
    return key ? { key: key, label: C.suspects[key] } : { key: "other", label: name };
  }

  function leadsNote() {
    var left = leadsLeft();
    if (!left) return null;
    return el("p", { class: "note" }, "You still have " + left + " lead" + (left > 1 ? "s" : "") +
      " to follow up. You can accuse now or keep investigating.");
  }

  views.accuse = function () {
    var d = state.draft;
    var error = el("p", { class: "error", role: "alert" });
    var choices = el("div", { class: "suspects" });
    var other = el("input", { type: "text", id: "other-name", autocomplete: "off", "aria-label": "Their name", placeholder: "Their name" });
    other.value = d.other || "";
    Object.keys(C.suspects).concat(["other"]).forEach(function (key) {
      var id = "s-" + key;
      var input = el("input", { type: "radio", name: "suspect", id: id, value: key, checked: d.suspect === key });
      input.addEventListener("change", function () {
        d.suspect = key;
        error.textContent = "";
        save();
        if (key === "other") other.focus();
      });
      choices.appendChild(el("label", { class: "suspect" + (key === "other" ? " suspect-other" : ""), for: id }, [
        input,
        key === "other" ? el("span", { class: "thumb thumb-empty", "aria-hidden": "true" }, "?") : thumb(PORTRAITS[key]),
        key === "other" ? el("span", { class: "suspect-name" }, ["Someone else", other])
          : el("strong", { class: "suspect-name" }, C.suspects[key]),
      ]));
    });
    other.addEventListener("input", function () {
      d.other = other.value;
      if (other.value.trim()) {
        d.suspect = "other";
        error.textContent = "";
        document.getElementById("s-other").checked = true;
      }
      save();
    });
    var reasoning = el("textarea", { id: "reasoning", rows: "6" });
    reasoning.value = d.reasoning || "";
    reasoning.addEventListener("input", function () { d.reasoning = reasoning.value; save(); });
    function submit() {
      if (!accusation()) {
        error.textContent = d.suspect === "other" ? "Type the name of the person you're accusing." : "Choose who you're accusing.";
        return;
      }
      go("confirm");
    }
    other.addEventListener("keydown", function (e) {
      if (e.key === "Enter") { e.preventDefault(); submit(); }
    });
    var form = el("div", { class: "accuse-form" }, [
      el("fieldset", null, [el("legend", null, "Who killed Mr. Hale?"), choices]),
      el("label", { class: "block", for: "reasoning" }, "Why? Explain your reasoning."),
      reasoning,
      error,
      el("div", { class: "actions" }, [
        iconButton("accuse", "Accuse", submit, "btn-alert"),
        button("Back to the case", function () { go("hub"); }, "btn-quiet-console"),
      ]),
    ]);
    return el("section", { class: "player" }, [
      el("div", { class: "chapterbar" }, [el("span", null, "Accuse"), el("span", null, "Incident File SF-1008")]),
      el("div", { class: "console" }, [
        el("div", { class: "console-bar" }, [el("span", { class: "dot dot-alert" }), "Name the killer"]),
        el("div", { class: "console-body" }, [heading("Name the killer"), leadsNote(), form]),
      ]),
    ]);
  };

  views.confirm = function () {
    var a = accusation();
    if (!a) return views.accuse();
    var notSuspect = a.key === "other";
    return el("section", { class: "player" }, [
      el("div", { class: "chapterbar" }, [el("span", null, "Accuse"), el("span", null, "Incident File SF-1008")]),
      el("div", { class: "console" }, [
        el("div", { class: "console-bar" }, [el("span", { class: "dot dot-alert" }), "Are you sure?"]),
        el("div", { class: "console-body" }, [
          heading("Accuse " + a.label + "?"),
          notSuspect ? el("p", null, a.label + " isn't one of the three suspects. You can accuse them anyway.") : null,
          leadsNote(),
          el("div", { class: "spoiler" }, [
            el("p", null, el("strong", null, "Spoiler warning: this ends the game.")),
            el("p", null, "The next screen names the killer and explains the whole solution. " +
              "If anyone else is playing along, make sure they're ready too."),
          ]),
          el("div", { class: "actions" }, [
            iconButton("accuse", "Accuse " + a.label + " and see the verdict", function () {
              go("verdict", { accused: a, reasoning: (state.draft.reasoning || "").trim(), step: 0 });
            }, "btn-alert"),
            button("Not yet, go back", function () { go("accuse"); }, "btn-quiet-console"),
          ]),
        ]),
      ]),
    ]);
  };

  views.verdict = function () {
    var a = state.accused;
    var cards = decodeReveal();
    var verdict = cards.find(function (c) { return c.meta.for === a.key; });
    var pages = [verdict].concat(cards.filter(function (c) { return c.meta.for === "all"; }));
    var i = Math.min(Math.max(state.step | 0, 0), pages.length - 1);
    var last = i === pages.length - 1;
    var parts = [el("div", { class: "chapterbar" }, [
      el("span", null, "The verdict"), el("span", { class: "chapter-count" }, (i + 1) + " of " + pages.length),
    ])];
    if (i === 0) {
      var stop = /\.$/.test(a.label) ? "" : ".";
      // The reveal's picture names the killer, so it's only ever made here, after the accusation.
      parts.push(panel({ image: REVEAL_ART, hotspots: [], body: "" }));
      parts.push(el("p", { class: "accused" }, el("strong", null, "You accused " + a.label + stop)));
      if (state.reasoning) parts.push(el("blockquote", { class: "reasoning" }, state.reasoning));
      parts.push(card(verdict, a.key === "other" ? "You named " + a.label : verdict.title));
    } else {
      parts.push(card(pages[i]));
    }
    if (last) parts.push(el("p", { class: "lede" }, "Thanks for playing."));
    parts.push(el("div", { class: "framebar" }, [
      el("div", { class: "framebar-nav" }, i > 0
        ? [iconButton("prev", "Previous", function () { go("verdict", { step: i - 1 }); }, "btn-quiet-console")] : []),
      el("div", { class: "framebar-actions" }, [last
        ? button("Play again", askRestart, "btn-primary")
        : button([el("span", null, "Continue"), icon("next")], function () { go("verdict", { step: i + 1 }); }, "btn-primary btn-next")]),
    ]));
    return el("section", { class: "player verdict" }, parts);
  };

  // ---- chrome ------------------------------------------------------------------------------

  function render(moveFocus) {
    hideSpot();
    keyNav = null;
    var view = views[state.view] ? state.view : "title";
    main.replaceChildren(views[view]());
    var started = view !== "title" || state.chosen.length > 0;
    restartBtn.hidden = !started;
    var showLeads = ["hub", "lead", "result", "card", "outside", "accuse", "confirm"].indexOf(view) >= 0;
    leadsEl.hidden = !showLeads;
    leadsEl.textContent = state.accused ? "Case closed" : leadsLine();
    if (state.accused) leadsEl.hidden = false;
    if (moveFocus) {
      window.scrollTo(0, 0);
      var h = main.querySelector("h2[tabindex], h1") || main;
      (h.tabIndex >= 0 || h.hasAttribute("tabindex") ? h : main).focus({ preventScroll: true });
    }
  }

  function currentTheme() {
    var set = document.documentElement.dataset.theme;
    if (set) return set;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function paintThemeButton() {
    var next = currentTheme() === "dark" ? "light" : "dark";
    themeBtn.textContent = next === "light" ? "Light theme" : "Dark theme";
    themeBtn.setAttribute("aria-label", "Switch to the " + next + " theme");
  }

  // In a Grafana Page the game follows Grafana's theme, so it has no toggle of its own.
  if (HOST.onTheme) {
    themeBtn.hidden = true;
    HOST.onTheme(function (mode) {
      if (mode === "dark" || mode === "light") document.documentElement.dataset.theme = mode;
    });
  }

  themeBtn.addEventListener("click", function () {
    var next = currentTheme() === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem(THEME_KEY, next); } catch (e) { /* not saved */ }
    paintThemeButton();
  });
  if (window.matchMedia) {
    var mq = window.matchMedia("(prefers-color-scheme: dark)");
    if (mq.addEventListener) mq.addEventListener("change", paintThemeButton);
  }

  function restart() {
    state = fresh();
    save();
    render(true);
    announce("Progress cleared. Starting over.");
  }

  function askRestart() {
    if (dialog && typeof dialog.showModal === "function") {
      dialog.returnValue = "";
      dialog.showModal();
    } else if (window.confirm("Start over? This clears your saved progress.")) {
      restart();
    }
  }

  restartBtn.addEventListener("click", askRestart);
  if (dialog) {
    // The buttons close the dialog themselves: a Grafana Page's sandbox blocks <form method="dialog">.
    [].forEach.call(dialog.querySelectorAll("button[value]"), function (btn) {
      btn.addEventListener("click", function () { dialog.close(btn.value); });
    });
    dialog.addEventListener("close", function () { if (dialog.returnValue === "restart") restart(); });
  }

  paintThemeButton();
  // Saved progress may come from an async store, so the first render waits for it.
  readStored(STORE_KEY).then(function (text) {
    state = load(text);
    render(false);
  });
})();
