/* The Defiant Jazz Incident, web version.
 *
 * The same flow as the terminal game (game/engine.py): title, cold open, the
 * suspects' statements, then a hub where the player investigates, reviews and
 * accuses. The AI lives beside the game: the hub offers example questions to
 * copy into Grafana Assistant or the player's own agent.
 *
 * Story text comes from SPOILERS-content.js, built from game/SPOILERS-content/
 * by web/build.py. The reveal stays encoded until the player accuses and confirms.
 *
 * The same script runs as a static page and as a Grafana Page (web/build.py --page).
 * A Page runs in a sandboxed frame with no forms, modals or localStorage, so the game
 * uses click handlers rather than form submits, and a host set up before this script
 * (window.DJ_HOST) can supply, each optionally:
 *   storage.getItem(key) / storage.setItem(key, value)  saved progress, may return promises
 *   onTheme(callback)          calls callback("dark" | "light") whenever the host's theme changes
 *   askAssistant(prompt)       opens Grafana Assistant with the prompt; returns a promise
 *   scenes                     the header art as { name: URL }, for a frame that can't load files
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

  // Header art: pixel-art scenes in assets/, cut from the comic sheet by web/build.py --art,
  // as name: [width, height]. They hold no clue text, so their alt text is empty and the
  // story stays in the HTML. Lead options with a scene are listed by option name.
  var SCENES = {
    "scene-1-broadcast": [1086, 361],
    "scene-2-break-room": [1086, 346],
    "scene-3-elevator": [1086, 364],
    "scene-4-clement-home": [1086, 377],
  };
  var LEAD_SCENES = { "Elevator car 1": "scene-3-elevator", "Clement at home": "scene-4-clement-home" };

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

  function go(view, extra, opts) {
    state.view = view;
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

  function rule(label) {
    return el("div", { class: "rule", "aria-hidden": "true" }, label || "");
  }

  function heading(text, level) {
    return el("h" + (level || 2), { tabindex: "-1" }, text);
  }

  var toastTimer = null;
  function announce(text) {
    statusEl.textContent = text;
    statusEl.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { statusEl.classList.remove("show"); }, 3500);
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
        var p = el("p", { class: "speech" }, el("span", { class: "speaker" }, name + ":"));
        p.appendChild(document.createTextNode(" "));
        root.appendChild(inline(line.slice(name.length + 2), p));
      } else {
        group = null;
        root.appendChild(inline(stripped, el("p")));
      }
    });
    return root;
  }

  function scene(name) {
    var size = SCENES[name];
    var src = (HOST.scenes && HOST.scenes[name]) || "assets/" + name + ".webp";
    return el("figure", { class: "scene" },
      el("img", { src: src, alt: "", width: size[0], height: size[1], decoding: "async" }));
  }

  function card(c, title, ruleLabel) {
    if (c.meta && c.meta.style === "advert") return advert(c, ruleLabel);
    var body = cardBody(c.body);
    var art = c.meta && LEAD_SCENES[c.meta.option] ? scene(LEAD_SCENES[c.meta.option]) : null;
    if (c === C.coldOpen) {
      // The break room goes above "What happened that night".
      var at = [].find.call(body.children, function (n) { return /^What happened/.test(n.textContent); });
      body.insertBefore(scene("scene-2-break-room"), at || body.firstChild);
    }
    return el("article", { class: "story" }, [
      ruleLabel ? rule(ruleLabel) : null,
      art,
      heading(title || c.title),
      body,
    ]);
  }

  // The Kipsake advert: every line is its own paragraph (none of them are speaker lines).
  function advert(c, ruleLabel) {
    var body = el("div", { class: "card-body" });
    c.body.split("\n").forEach(function (raw) {
      var line = raw.trim();
      if (!line) return;
      if (line.charAt(0) === "[" && line.slice(-1) === "]") {
        body.appendChild(inline(line.slice(1, -1), el("p", { class: "stage" })));
      } else {
        body.appendChild(inline(line, el("p")));
      }
    });
    return el("article", { class: "advert-card" }, [
      ruleLabel ? rule(ruleLabel) : null,
      scene("scene-1-broadcast"),
      el("div", { class: "advert" }, [
        el("p", { class: "ad-label" }, "Advert"),
        heading(c.title),
        body,
      ]),
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
  // execCommand, and if that fails too, select the text for the player to copy.

  function copy(text, sourceNode, btn) {
    function done() { announce("Copied. Paste it into Grafana Assistant or your own AI."); }
    function fallback() {
      var ok = false;
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
      if (btn) btn.focus();
      if (ok) return done();
      selectText(sourceNode);
      announce("Couldn't copy from here. The question is selected: press Ctrl+C (⌘C on a Mac).");
    }
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(done, fallback);
    } else {
      fallback();
    }
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

  // Inside a Grafana Page: open the question in Grafana Assistant for the player to send.
  // Only the question goes, never story text.
  function ask(text, sourceNode) {
    Promise.resolve().then(function () { return HOST.askAssistant(text); }).then(function () {
      announce("Opened in Grafana Assistant. Check the question, then send it.");
    }, function () {
      selectText(sourceNode);
      announce("Couldn't open Grafana Assistant. The question is selected: press Ctrl+C (⌘C on a Mac) to copy it.");
    });
  }

  // ---- views ----------------------------------------------------------------------------

  var views = {};

  views.title = function () {
    var resume = state.chosen.length > 0;
    return el("section", { class: "title-view" }, [
      el("h1", { class: "sr-only" }, "The Defiant Jazz Incident"),
      el("pre", { class: "banner", "aria-hidden": "true" }, C.banner),
      el("p", { class: "lede" }, "An observability murder mystery on the Sleep Floor at Kipsake."),
      el("div", { class: "actions" }, [
        button(resume ? "Continue" : "Start", function () { go(resume ? "hub" : "advert"); }, "btn-primary"),
      ]),
    ]);
  };

  views.advert = function () {
    return el("section", { class: "story" }, [
      card(C.advert, null, "Cold open"),
      el("div", { class: "actions" }, [
        button("Continue", function () { go("cold"); }, "btn-primary"),
      ]),
    ]);
  };

  views.cold = function () {
    return el("section", null, [
      card(C.coldOpen, null, "Cold open"),
      el("div", { class: "actions" }, [
        button("Continue", function () { go("statement", { step: 0 }); }, "btn-primary"),
      ]),
    ]);
  };

  views.statement = function () {
    var i = Math.min(Math.max(state.step | 0, 0), C.testimonies.length - 1);
    var last = i === C.testimonies.length - 1;
    return el("section", { class: "story" }, [
      rule("Interviews · " + (i + 1) + " of " + C.testimonies.length),
      i === 0 ? el("p", { class: "story lede" }, C.testimonyIntro) : null,
      card(C.testimonies[i]),
      el("div", { class: "actions" }, [
        button(last ? "Continue" : "Next statement", function () {
          if (last) go("hub"); else go("statement", { step: i + 1 });
        }, "btn-primary"),
        i > 0 ? button("Previous", function () { go("statement", { step: i - 1 }); }) : null,
      ]),
    ]);
  };

  views.hub = function () {
    var n = state.chosen.length;

    var inv = el("section", { class: "panel area-inv", "aria-labelledby": "h-inv" }, [
      el("h3", { id: "h-inv" }, "Investigate"),
      el("p", null, leadsLine()),
      el("p", { class: "note" }, n < LEADS
        ? "You follow up your leads in order: a crime scene, a home visit, one last interview. " +
          "Each time you pick one of three options and see only that one."
        : "You've followed up all three leads. When you're ready, accuse the killer."),
      n < LEADS ? el("div", { class: "actions" }, [
        button("Investigate lead " + (n + 1) + ": " + C.leadKinds[n], investigate, "btn-primary"),
      ]) : null,
    ]);

    var list = el("ol", { class: "questions" });
    QUESTIONS.forEach(function (q, i) {
      var text = el("span", { class: "q", id: "q" + i }, q);
      var btn = HOST.askAssistant
        ? button("Ask Assistant", function () { ask(q, text); }, "btn-small", { "aria-describedby": "q" + i })
        : button("Copy", function () { copy(q, text, btn); }, "btn-small", { "aria-describedby": "q" + i });
      list.appendChild(el("li", null, [text, btn]));
    });
    var ai = el("section", { class: "panel area-ai", "aria-labelledby": "h-ai" }, [
      el("h3", { id: "h-ai" }, "Ask your AI"),
      el("p", null, "Your AI works beside the game, not inside it. Ask Grafana Assistant in this " +
        "Grafana, or your own AI agent through the Grafana MCP server or gcx. It has read Kipsake's " +
        "records in this stack, and nothing else. It hasn't seen the interviews, the leads you follow, " +
        "or anything you find. If you want it to know something, tell it."),
      el("p", null, "Ask it anything. These are only examples, if you're not sure where to start:"),
      list,
      HOST.askAssistant ? el("p", { class: "note" }, "Ask Assistant opens the question in Grafana Assistant " +
        "for you to check and send. Using your own AI? Select a question and copy it.") : null,
      el("p", { class: "note" }, "The data's times are UTC. If it was loaded on an incident date, the " +
        "story's 03:02 is 03:02 in Grafana set to UTC. If it was loaded to end just before the load, " +
        "03:02 is a different clock time there. Either way, your AI can find the outage in the data."),
      el("p", { class: "note" }, ["Learn more: "].concat(LINKS.map(function (l, i) {
        return [i ? " · " : "", el("a", { href: l[1], target: "_blank", rel: "noopener noreferrer" }, l[0])];
      }).flat(), [" (opens in a new tab)"])),
    ]);

    var items = reviewItems();
    var review = el("section", { class: "panel area-review", "aria-labelledby": "h-review" }, [
      el("h3", { id: "h-review" }, "Review"),
      el("p", { class: "note" }, "Re-read the advert, the cold open, the interviews and anything you've unlocked."),
      el("ul", { class: "review-list" }, items.map(function (item, i) {
        return el("li", null, el("button", {
          type: "button", class: "linklike", onclick: function () { go("card", { reviewing: i }); },
        }, item[0]));
      })),
    ]);

    var accuse = el("section", { class: "panel area-accuse", "aria-labelledby": "h-accuse" }, [
      el("h3", { id: "h-accuse" }, "Accuse"),
      el("p", { class: "note" }, "When you're ready, name the killer and say why. You can do this any " +
        "time, even before all three leads. It ends the game."),
      el("div", { class: "actions" }, [button("Accuse…", function () { go("accuse"); })]),
    ]);

    return el("section", null, [
      rule("Your turn"),
      heading("The case"),
      el("p", { class: "story" }, "Ask your AI anything. You have three leads to follow up, " +
        "one at a time, whenever you like. When you're ready, accuse the killer and say why."),
      el("div", { class: "hub-grid" }, [inv, ai, accuse, review]),
    ]);
  };

  views.outside = function () {
    return el("section", { class: "story" }, [
      rule("Outside World handout"),
      el("p", { class: "lede" }, "Before the next lead, a handout from outside Kipsake."),
      card(C.outsideWorld),
      el("div", { class: "actions" }, [button("Continue to lead 2", function () { go("lead", { picking: null }); }, "btn-primary")]),
    ]);
  };

  views.lead = function () {
    var n = state.chosen.length;
    if (n >= LEADS) return views.hub();
    var d = C.decisions[n];
    var error = el("p", { class: "error", role: "alert" });
    var form = el("div", { class: "lead-form" });
    var choices = el("div", { class: "choices" });
    d.options.forEach(function (opt, i) {
      var id = "opt" + i;
      var input = el("input", { type: "radio", name: "lead", id: id, value: String(i), checked: state.picking === i });
      input.addEventListener("change", function () { state.picking = i; error.textContent = ""; save(); });
      choices.appendChild(el("label", { class: "choice", for: id }, [
        input,
        el("span", null, [
          el("strong", null, (i + 1) + ") " + opt.meta.option),
          opt.meta.note ? el("span", { class: "hint" }, opt.meta.note) : null,
        ]),
      ]));
    });
    form.appendChild(el("fieldset", null, [el("legend", null, "Choose one. You'll see only the one you pick."), choices]));
    form.appendChild(error);
    // A click handler, not a form submit: a Grafana Page's sandbox blocks form submission.
    function follow() {
      var picked = form.querySelector("input[name=lead]:checked");
      if (!picked) { error.textContent = "Pick 1, 2 or 3."; return; }
      var chosen = state.chosen.concat([Number(picked.value)]);
      go("result", { chosen: chosen, picking: null });
    }
    form.appendChild(el("div", { class: "actions" }, [
      button("Follow this lead", follow, "btn-primary"),
      button("Decide later", function () { go("hub"); announce("No rush. Investigate when you're ready."); }),
    ]));
    return el("section", { class: "story" }, [
      rule("Lead " + (n + 1) + " of " + LEADS),
      heading(leadTitle(n)),
      cardBody(d.prompt),
      form,
    ]);
  };

  views.result = function () {
    var n = state.chosen.length - 1;
    if (n < 0) return views.hub();
    var c = chosenCard(n);
    var more = n < LEADS - 1;
    return el("section", null, [
      card(c, "Lead " + (n + 1) + " · " + c.title, "Lead " + (n + 1) + " of " + LEADS),
      el("p", { class: "story lede" }, more
        ? "Ask your AI about anything here, or investigate again (lead " + (n + 2) + ": " + C.leadShort[n + 1] + ")."
        : "That was the last lead. Ask your AI anything else, then accuse."),
      el("div", { class: "actions" }, [
        button("Back to the case", function () { go("hub"); }, "btn-primary"),
        more ? button("Investigate lead " + (n + 2), investigate) : button("Accuse…", function () { go("accuse"); }),
      ]),
    ]);
  };

  views.card = function () {
    var items = reviewItems();
    var i = Math.min(Math.max(state.reviewing | 0, 0), items.length - 1);
    return el("section", null, [
      card(items[i][1], items[i][0], "Review · " + (i + 1) + " of " + items.length),
      el("div", { class: "actions" }, [
        button("Back to the case", function () { go("hub"); }, "btn-primary"),
        i > 0 ? button("Previous", function () { go("card", { reviewing: i - 1 }); }) : null,
        i < items.length - 1 ? button("Next", function () { go("card", { reviewing: i + 1 }); }) : null,
      ]),
    ]);
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
    var choices = el("div", { class: "choices" });
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
      choices.appendChild(el("label", { class: "choice", for: id }, [
        input,
        key === "other" ? el("span", null, ["Someone else", other]) : el("strong", null, C.suspects[key]),
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
        button("Accuse", submit, "btn-primary"),
        button("Back to the case", function () { go("hub"); }),
      ]),
    ]);
    return el("section", { class: "story" }, [rule("Accuse"), heading("Name the killer"), leadsNote(), form]);
  };

  views.confirm = function () {
    var a = accusation();
    if (!a) return views.accuse();
    var notSuspect = a.key === "other";
    return el("section", { class: "story" }, [
      rule("Accuse"),
      heading("Accuse " + a.label + "?"),
      notSuspect ? el("p", null, a.label + " isn't one of the three suspects. You can accuse them anyway.") : null,
      leadsNote(),
      el("div", { class: "spoiler" }, [
        el("p", null, el("strong", null, "Spoiler warning: this ends the game.")),
        el("p", null, "The next screen names the killer and explains the whole solution. " +
          "If anyone else is playing along, make sure they're ready too."),
      ]),
      el("div", { class: "actions" }, [
        button("Accuse " + a.label + " and see the verdict", function () {
          go("verdict", { accused: a, reasoning: (state.draft.reasoning || "").trim(), step: 0 });
        }, "btn-primary"),
        button("Not yet, go back", function () { go("accuse"); }),
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
    var parts = [];
    if (i === 0) {
      var stop = /\.$/.test(a.label) ? "" : ".";
      parts.push(rule("The verdict"));
      parts.push(el("p", null, el("strong", null, "You accused " + a.label + stop)));
      if (state.reasoning) parts.push(el("blockquote", { class: "reasoning" }, state.reasoning));
      parts.push(card(verdict, a.key === "other" ? "You named " + a.label : verdict.title));
    } else {
      parts.push(card(pages[i], null, "The verdict · " + (i + 1) + " of " + pages.length));
    }
    if (last) parts.push(el("p", { class: "story" }, "Thanks for playing."));
    parts.push(el("div", { class: "actions" }, [
      last ? button("Play again", askRestart, "btn-primary") : button("Continue", function () { go("verdict", { step: i + 1 }); }, "btn-primary"),
      i > 0 ? button("Previous", function () { go("verdict", { step: i - 1 }); }) : null,
    ]));
    return el("section", { class: "story" }, parts);
  };

  // ---- chrome ------------------------------------------------------------------------------

  function render(moveFocus) {
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
