/* The Defiant Jazz Incident, local mode.
 *
 * The same game, played from your own machine with the open-source stack in local/ (Loki, Prometheus, Tempo,
 * Grafana and the Grafana MCP server). It isn't in a Grafana Page, so there's no Grafana Assistant and no Chat
 * button: you ask your own AI agent, through the MCP server or gcx, and the example questions point at the local
 * data sources. This file holds everything that's different, so game.js keeps one set of wording for the Page.
 *
 * It does nothing, and defines nothing, unless the page is local: local-config.js (which the game's server in
 * local/ writes) set window.DJ_LOCAL_CONFIG, or the address has ?local. Inside a Grafana Page (window.DJ_HOST)
 * it never runs, and the Page build doesn't include it. game.js reads window.DJ_LOCAL if there is one.
 *
 * The one thing here that can reach the network is the optional leaderboard button, and only when the player
 * clicks it, and only when local-config.js names a collector (leaderboardUrl, off by default). It sends the same
 * accusation_scored event the Grafana Page records (the points for each question, the total and the name the player
 * chose), marked source=local, and never what the player typed in their answers.
 */
(function () {
  "use strict";

  if (window.DJ_HOST) return;
  var cfg = window.DJ_LOCAL_CONFIG;
  if (!cfg && /[?&]local(=|&|#|$)/.test(location.search)) cfg = {};
  if (!cfg) return;

  var GRAFANA = String(cfg.grafanaUrl || "http://localhost:3000").replace(/\/+$/, "");
  var MCP = String(cfg.mcpUrl || "http://localhost:8000/mcp");
  var DASHBOARD = String(cfg.dashboardUrl || "");
  var LEADERBOARD = /^(https:\/\/|http:\/\/(localhost|127\.0\.0\.1)(:\d+)?\/)[^\s]+$/.test(String(cfg.leaderboardUrl || "")) ? String(cfg.leaderboardUrl) : "";

  var MCP_REPO = "https://gra.fan/mcprepo";
  var GCX_REPO = "https://gra.fan/gcxrepo";
  var PLAYER_KEY = "dj_local_player_id";
  var SENT_KEY = "defiantjazz.local.sent";
  var DOMAIN = "defiant-jazz";
  var QUESTION_IDS = ["killer", "why", "jazz", "blackout", "waffles", "seat", "elevator"];

  // What the three example questions open with: the same wording as the Grafana Page, naming the local data sources.
  var DATA = "Using the Kipsake data in this local Grafana stack from the last 30 days, in all three signals " +
    "(logs in Loki, metrics in Prometheus, traces in Tempo; the data source UIDs are loki, prometheus and tempo), " +
    "all tagged service_namespace=\"kipsake-sleep-floor\" (service.namespace in Tempo; search Tempo without a time range, " +
    "or open a trace by the trace_id on a door log line), ";

  function code(el, text) { return el("code", null, text); }

  // ---- the hub's "Ask your AI" box --------------------------------------------------------------
  function hubIntro(h) {
    var el = h.el, fragment = document.createDocumentFragment();
    [
      el("p", null, ["Ask your own AI agent. It investigates through the open-source ", h.link("Grafana MCP server", MCP_REPO),
        " that runs on this machine at ", code(el, MCP), ", or through ", h.link("gcx", GCX_REPO),
        ". It hasn't seen the interviews, the leads you follow, or anything you find. If you want it to know something, tell it."]),
      el("p", { class: "note" }, ["In Claude Code, connect it with ", code(el, "claude mcp add --transport http grafana-local " + MCP),
        ". Any other agent with MCP support: add an HTTP (streamable-http) server at the same address. " +
        "Start your agent outside this repository's folder, so it can't read the spoilers."]),
      el("p", { class: "note" }, "No MCP? Paste game/ai-evidence/case-bundle.md into any chatbot instead."),
    ].forEach(function (node) { fragment.appendChild(node); });
    return fragment;
  }

  function timesNote() {
    return "The data's times are UTC. It was loaded with the incident on the most recent Thursday, so the story's " +
      "03:02 is 03:02 in Grafana set to UTC. Your AI can find the outage in the data either way.";
  }

  // ---- the leaderboard ------------------------------------------------------------------------------
  // The payload is what the Grafana Page records as accusation_scored: points per question, the total, which marker
  // it was and the name the player chose. Everything is a short string. Never the answers.
  function payload(score, name) {
    var pts = {};
    (score.rows || []).forEach(function (r) { pts[r.id] = r.points; });
    var out = { score: score.total, max: score.max,
      judge: (score.rows || []).some(function (r) { return r.by === "ai"; }) ? "ai" : "matcher", name: name || "" };
    QUESTION_IDS.forEach(function (id) { out[id] = pts[id] || 0; });
    var attrs = {};
    Object.keys(out).forEach(function (k) { attrs[k] = String(out[k]).slice(0, 80); });
    attrs.source = "local";
    return attrs;
  }

  function random(bytes) {
    var a = new Uint8Array(bytes);
    try { crypto.getRandomValues(a); } catch (e) { for (var i = 0; i < a.length; i++) a[i] = Math.floor(Math.random() * 256); }
    return Array.prototype.map.call(a, function (b) { return ("0" + b.toString(16)).slice(-2); }).join("");
  }

  // The same random id on each visit from this browser, so a player is one row on the board. Never a login, name or email.
  function playerId() {
    try {
      var saved = localStorage.getItem(PLAYER_KEY);
      if (saved && /^p_[A-Za-z0-9]{6,32}$/.test(saved)) return saved;
      var fresh = "p_" + random(8);
      localStorage.setItem(PLAYER_KEY, fresh);
      return fresh;
    } catch (e) {
      return "p_" + random(8);
    }
  }

  // The body a Grafana Frontend Observability collector (Faro) takes: the same event the Page's Faro records, with the
  // app, environment and domain the play statistics dashboard filters on. The player is marked player_id_source=local_storage.
  function faroBody(attrs, finishedAt) {
    var when = new Date(finishedAt && isFinite(finishedAt) ? finishedAt : Date.now());
    var data = Object.assign({ app_version: "local-web", environment: "prod" }, attrs);
    return {
      meta: {
        sdk: { name: "@grafana/faro-core", version: "2.11.0", integrations: [] },
        app: { name: DOMAIN, version: "local-web", environment: "prod" },
        session: { id: random(8) },
        user: { id: playerId(), attributes: { player_id_source: "local_storage" } },
        page: { url: location.origin + location.pathname },
        view: { name: "default" },
      },
      events: [{ name: "accusation_scored", domain: DOMAIN, attributes: data, timestamp: when.toISOString() }],
    };
  }

  function submit(attrs, finishedAt) {
    return fetch(LEADERBOARD, {
      method: "POST", mode: "cors", credentials: "omit", referrerPolicy: "no-referrer",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(faroBody(attrs, finishedAt)),
    }).then(function (res) { if (!res.ok) throw new Error("HTTP " + res.status); });
  }

  function wasSent(finishedAt) {
    try { return localStorage.getItem(SENT_KEY) === String(finishedAt); } catch (e) { return sentInMemory === finishedAt; }
  }
  var sentInMemory = 0;
  function markSent(finishedAt) {
    sentInMemory = finishedAt;
    try { localStorage.setItem(SENT_KEY, String(finishedAt)); } catch (e) { /* kept in memory */ }
  }

  // The last page of the verdict: the player's own score, a way back to their own Grafana, and, if a collector is set
  // up, the opt-in. Nothing is sent until the player clicks the button.
  function boardView(h) {
    var el = h.el, score = h.score, name = h.name || "";
    var box = el("div", { class: "board", "aria-live": "polite" });
    box.appendChild(el("p", null, "Your score: " + score.total + " / " + score.max + (name ? " as " + name : "") + "."));
    box.appendChild(el("p", { class: "note" }, "This game runs on your machine, so there's no leaderboard here and nobody else " +
      "sees your score" + (LEADERBOARD ? ", unless you add it below." : ".")));
    if (DASHBOARD) {
      box.appendChild(el("div", { class: "actions" }, [h.button("Open the Kipsake dashboard in your Grafana", function () {
        window.open(DASHBOARD, "_blank", "noopener,noreferrer");
      }, "btn-quiet-console")]));
    }
    if (!LEADERBOARD) return box;

    var attrs = payload(score, name);
    var status = el("p", { class: "note", role: "status" });
    var send = null;
    function done() {
      send.disabled = true;
      status.textContent = "Sent. It can take a few minutes to show up on the leaderboard, with a \"played locally\" badge. Thanks!";
    }
    send = h.button("Add my score to the public leaderboard", function () {
      send.disabled = true;
      status.textContent = "Sending…";
      submit(attrs, h.finishedAt).then(function () {
        markSent(h.finishedAt);
        done();
      }, function () {
        send.disabled = false;
        status.textContent = "Couldn't send it. Check your connection and try again, or skip it: nothing was added.";
      });
    }, "btn-primary");
    var rows = [["Your score", attrs.score + " / " + attrs.max], ["Your name", name || "(none: Anonymous detective)"],
      ["Points for each question", QUESTION_IDS.map(function (id) { return attrs[id]; }).join(", ")]];
    box.appendChild(el("section", { class: "opt-in", "aria-labelledby": "h-opt-in" }, [
      el("h3", { id: "h-opt-in" }, "Add my score to the public leaderboard (optional)"),
      el("p", null, "Nothing leaves your machine unless you click the button below. If you do, the game sends Grafana's public " +
        "leaderboard only this: your score, the points for each question, the name you chose, the time you finished and a random " +
        "player id kept in this browser. It never sends your answers."),
      el("ul", { class: "opt-in-list" }, rows.map(function (r) { return el("li", null, [el("strong", null, r[0] + ": "), r[1]]); })),
      el("p", { class: "note" }, "Scores from your own machine can't be checked, so the leaderboard marks them \"played locally\". " +
        "This is the only thing in the local game that contacts Grafana Cloud."),
      el("div", { class: "actions" }, [send]),
      status,
    ]));
    if (wasSent(h.finishedAt)) done();
    return box;
  }

  window.DJ_LOCAL = {
    grafanaUrl: GRAFANA,
    mcpUrl: MCP,
    dashboardUrl: DASHBOARD,
    leaderboardUrl: LEADERBOARD,
    data: DATA,
    hubIntro: hubIntro,
    timesNote: timesNote,
    links: [["Grafana (Explore)", GRAFANA + "/explore"], ["Grafana MCP server", MCP_REPO], ["gcx", GCX_REPO]],
    copied: "Copied. Paste it into your AI agent.",
    judgeNote: "There's no Grafana Assistant here, so the matcher is the judge: it marked your answers on its own. " +
      "On the Grafana Page, an AI judge also reads the answers the matcher marked down.",
    nameNote: function (max) {
      return "Only used if you add your score to the public leaderboard at the end. Up to " + max +
        " characters. Leave it empty to show as Anonymous detective.";
    },
    boardView: boardView,
    // For tests.
    _payload: payload,
    _faroBody: faroBody,
  };
})();
