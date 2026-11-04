"""Self-check for the web game. Spoiler-free: it compares files, never quotes the cards.

    python3 -m unittest discover -s web
"""

import base64
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build  # noqa: E402
import content  # noqa: E402  (game/content.py, put on the path by build)
import scoring  # noqa: E402  (game/scoring.py, the Python matcher)

CONTENT = content.load()


def read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return f.read()


def bundle_data():
    text = read("SPOILERS-content.js")
    body = text.split("window.DJ_CONTENT = ", 1)[1].rstrip().rstrip(";")
    return json.loads(body)


def all_cards():
    cards = [CONTENT.advert, CONTENT.cold_open, CONTENT.outside_world] + list(CONTENT.testimonies)
    for decision in CONTENT.decisions:
        cards += decision.options
    return cards


class BundleTest(unittest.TestCase):
    def test_bundle_is_up_to_date(self):
        self.assertEqual(read("SPOILERS-content.js"), build.render(),
                         "web/SPOILERS-content.js is out of date: run python3 web/build.py")

    def test_bundle_has_every_card(self):
        data = bundle_data()
        bundled = [data["advert"], data["coldOpen"], data["outsideWorld"]] + data["testimonies"]
        for decision in data["decisions"]:
            bundled += decision["options"]
        as_tuples = {(c["title"], c["body"]) for c in bundled}
        for card in all_cards():
            self.assertIn((card.title, card.body), as_tuples, card.title)
        self.assertEqual([d["prompt"] for d in data["decisions"]],
                         [d.prompt for d in CONTENT.decisions])
        self.assertEqual(data["testimonyIntro"], CONTENT.testimony_intro)
        self.assertEqual(data["aliases"], CONTENT.aliases)

    def test_reveal_is_bundled_but_encoded(self):
        data = bundle_data()
        reveal = json.loads(base64.b64decode(data["reveal"]).decode("utf-8"))
        self.assertEqual([(c["title"], c["body"], c["meta"]) for c in reveal],
                         [(c.title, c.body, c.meta) for c in CONTENT.reveal.cards])
        text = read("SPOILERS-content.js")
        for card in CONTENT.reveal.cards:
            for line in card.body.splitlines():
                if len(line.strip()) >= 25:
                    self.assertNotIn(line.strip(), text, "reveal text is readable in the bundle")

    def test_content_files_keep_spoilers_in_their_names(self):
        self.assertTrue(os.path.exists(os.path.join(HERE, "SPOILERS-content.js")))
        page = read("index.html")
        self.assertIn('src="SPOILERS-content.js"', page)


class PageTest(unittest.TestCase):
    def test_no_network_requests_at_runtime(self):
        page, css = read("index.html"), read("style.css")
        scripts = read("game.js") + read("theme.js")
        # Every script and stylesheet is local.
        for tag in re.findall(r"<(?:script|link)\b[^>]*>", page):
            self.assertNotRegex(tag, r"(?:src|href)=\"(?:https?:)?//", tag)
        self.assertNotRegex(css, r"@import|url\(\s*['\"]?(?:https?:)?//")
        self.assertNotRegex(scripts, r"\bfetch\(|XMLHttpRequest|WebSocket|EventSource|sendBeacon|import\(")
        self.assertIn("connect-src 'none'", page)

    def test_links_open_in_a_new_tab(self):
        game = read("game.js")
        # The SVG namespace names the icons' markup, it isn't a link.
        urls = [u for u in re.findall(r"\"(https?://[^\"]+)\"", game) if u != "http://www.w3.org/2000/svg"]
        self.assertTrue(urls)
        for url in urls:
            self.assertTrue(f'"{url}"]' in game or url in ("https://gra.fan/mcprepo", "https://gra.fan/gcxrepo"), f"{url} should be in LINKS")
        self.assertIn('target: "_blank", rel: "noopener noreferrer"', game)
        # The MCP server and gcx are linked by their short links, wherever the game names them.
        self.assertIn('["Grafana MCP server", MCP_URL]', game)
        self.assertIn('["gcx", GCX_URL]', game)
        self.assertIn('extLink("Grafana MCP server", MCP_URL)', game)
        self.assertIn('extLink("gcx", GCX_URL)', game)
        self.assertNotIn("github.com/grafana/mcp-grafana", game)

    def test_assistant_prompts_say_to_click_chat(self):
        game = read("game.js")
        self.assertIn('click ", el("strong", null, "Chat"), " at the top to start chatting', game)
        self.assertIn("click Chat to start chatting", game)
        self.assertIn("If you don't see it, click Chat.", game)

    def test_arrow_keys_step_panels_only(self):
        game = read("game.js")
        handler = game.split('document.addEventListener("keydown"', 1)[1].split("\n  });", 1)[0]
        # Ignored with a modifier held, in a text field or select, or while a dialog is open.
        for guard in ("e.altKey", "e.ctrlKey", "e.metaKey", "e.shiftKey", "INPUT|TEXTAREA|SELECT", "isContentEditable", "dialog.open"):
            self.assertIn(guard, handler)
        # Only the two arrows, and only through keyNav (Next and Back on panels): no choice, lead or accusation.
        # Enter starts the game from the title and Tab stays on an open note's Close button; nothing else.
        self.assertEqual(sorted(set(re.findall(r'e\.key === "(\w+)"', handler))),
                         ["ArrowLeft", "ArrowRight", "Enter", "Escape", "Tab"])
        self.assertEqual(re.findall(r"\b(\w+)\(", handler.split('"ArrowRight"', 1)[1]).count("keyNav"), 2)
        for name in ("investigate", "accuse", "choose", "follow", "go"):
            self.assertNotRegex(handler, r"\b%s\(" % name)
        # The player and the verdict set it, and a hint sits beside the Next button.
        self.assertGreaterEqual(game.count("keyNav = function (step"), 2)
        self.assertIn("keys step through", game)
        self.assertIn("position: sticky; bottom: 0", read("style.css").split(".framebar {", 1)[1].split("}", 1)[0])

    def test_the_ai_box_comes_before_investigate_in_the_hub(self):
        css = read("style.css")
        self.assertIn('grid-template-areas: "ai" "inv" "review" "accuse";', css)
        self.assertIn('grid-template-areas: "ai inv" "ai accuse" "review review";', css)
        self.assertIn('el("div", { class: "hub-grid" }, [ai, inv, accuse, review])', read("game.js"))

    def test_example_questions(self):
        game = read("game.js")
        block = game.split("var DATA = ", 1)[1].split("var LINKS", 1)[0]
        hints = re.findall(r'\[\"([^"]+)\", DATA \+', block)
        self.assertEqual(hints, ["Ask for a verdict", "Make a table", "Make a graph"])
        data = re.search(r'var DATA = (.*?);\n  var QUESTIONS', game, re.S).group(1)
        # Every example names the case's namespace and all three stores, so an AI doesn't stop at the logs.
        for part in ('service_namespace=\\"kipsake-sleep-floor\\"', "all three signals", "logs in Loki", "metrics in Prometheus", "traces in Tempo",
                     "from the last 30 days"):
            self.assertIn(part, data)
        self.assertIn("Who killed Mr. Hale?", block.split("Make a table")[0])
        # The loader can shift the data's times, so the examples name no clock time.
        self.assertNotRegex(block, r"\b\d\d:\d\d\b")
        self.assertIn("These are only examples: ask it anything.", game)


class SandboxTest(unittest.TestCase):
    """A Grafana Page runs the game in a frame without forms, modals or localStorage."""

    def test_music_plays_without_media_elements(self):
        # The Page's frame blocks <audio> and <video> whatever the source, so the music is Web Audio.
        game = read("game.js")
        self.assertNotRegex(game, r"new Audio\b|el\(\"(?:audio|video)\"|createElement\(\"audio")
        self.assertIn("decodeAudioData", game)

    def test_no_form_submission(self):
        game, page = read("game.js"), read("index.html")
        self.assertNotIn('"submit"', game)
        self.assertNotIn('el("form"', game)
        self.assertNotIn("<form", page)
        self.assertNotRegex(page, r"<button(?![^>]*type=\"button\")", "every button needs type=button")

    def test_dialog_buttons_close_it(self):
        self.assertIn("dialog.close(btn.value)", read("game.js"))
        self.assertIn('value="restart"', read("index.html"))

    def test_host_hooks(self):
        game = read("game.js")
        for hook in ("HOST.storage", "HOST.onTheme", "HOST.askAssistant", "HOST.track"):
            self.assertIn(hook, game)
        # Outside the storage adapter, only the theme toggle touches localStorage, guarded.
        uses = [line.strip() for line in game.splitlines()
                if "localStorage." in line and not line.strip().startswith(("*", "//"))]
        self.assertEqual(len(uses), 3, uses)
        self.assertTrue(any(u.startswith("try {") for u in uses))


def webp_size(path):
    """(width, height) of a WebP file, read from its header."""
    with open(path, "rb") as f:
        head = f.read(30)
    if head[:4] != b"RIFF" or head[8:12] != b"WEBP":
        raise ValueError(f"{path} isn't a WebP file")
    chunk = head[12:16]
    if chunk == b"VP8 ":
        return (int.from_bytes(head[26:28], "little") & 0x3FFF, int.from_bytes(head[28:30], "little") & 0x3FFF)
    if chunk == b"VP8L":
        bits = int.from_bytes(head[21:25], "little")
        return ((bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1)
    if chunk == b"VP8X":
        return (int.from_bytes(head[24:27], "little") + 1, int.from_bytes(head[27:30], "little") + 1)
    raise ValueError(f"{path}: unknown WebP chunk {chunk!r}")


class SceneArtTest(unittest.TestCase):
    """The pictures: one WebP file each, made by build.py --art, or a placeholder until it's added."""

    def test_one_small_webp_per_scene(self):
        self.assertTrue(os.path.exists(build.SHEET), "the comic sheet is the source of the scenes")
        rows = 0
        for name, top, bottom in build.SCENES:
            self.assertEqual(top, rows, "the scenes cover the sheet without gaps")
            rows = bottom
            path = build.scene_path(name)
            self.assertEqual(webp_size(path)[1], bottom - top, name)
            self.assertLess(os.path.getsize(path), 150 * 1024, f"{name} should stay small")

    def test_one_small_webp_per_picture(self):
        present = build.pictures()
        for name in present:
            path = build.scene_path(name)
            self.assertEqual(webp_size(path), build.IMAGES[name], name)
            self.assertLess(os.path.getsize(path), 150 * 1024, f"{name} should stay small")
        # The title's key art and the interview portraits are always there.
        for name in (build.TITLE_ART, "portrait-agnes", "portrait-bertram", "portrait-clement"):
            self.assertIn(name, present)

    def test_title_motion_is_off_for_reduced_motion(self):
        # The title's lights move only for players who haven't asked for reduced motion.
        css = read("style.css")
        start = css.index(".title-lights { display: none;")
        block = css[start:css.index("@keyframes tl-spin")]
        before, _, moving = block.partition("@media (prefers-reduced-motion: no-preference)")
        self.assertNotIn("animation", before)
        self.assertIn("animation", moving)
        self.assertIn("titleLights()", read("game.js"))

    def test_bundle_knows_each_picture(self):
        data = bundle_data()
        self.assertEqual(data["pictures"], {n: list(size) for n, size in build.IMAGES.items()})
        self.assertEqual(data["toCome"], [n for n in build.IMAGES if n not in build.pictures()])
        game = read("game.js")
        self.assertIn(f'var TITLE_ART = "{build.TITLE_ART}"', game)
        self.assertIn(f'var REVEAL_ART = "{build.REVEAL_ART}"', game)
        self.assertIn('"assets/" + name + ".webp"', game)
        self.assertIn('alt: ""', game, "the art holds no clue text, so it needs no alt text")
        self.assertIn("img-src 'self'", read("index.html"))

    def test_every_card_is_told_in_panels(self):
        art = build.scene_art(CONTENT)
        self.assertEqual(set(art), {c.title for c in all_cards()})
        self.assertEqual(bundle_data()["art"], art)
        for title, panels in art.items():
            self.assertTrue(panels, title)
        # Each interview is one panel, on that suspect's portrait.
        for t in CONTENT.testimonies:
            self.assertEqual(len(art[t.title]), 1, t.title)
            self.assertTrue(art[t.title][0]["image"].startswith("portrait-"), t.title)
        # The flyer is the advert, on its own picture, with nothing to hover.
        flyer = art[CONTENT.advert.title]
        self.assertEqual([(p["image"], p["hotspots"]) for p in flyer], [("flyer-kipsake", [])])
        # The reveal's picture names the killer: no panel shows it, only the verdict.
        for panels in art.values():
            self.assertNotIn(build.REVEAL_ART, [p["image"] for p in panels])
        self.assertNotIn(build.REVEAL_ART, read("game.js").replace(f'var REVEAL_ART = "{build.REVEAL_ART}"', ""))

    def test_art_stays_crisp_and_still_for_reduced_motion(self):
        css = read("style.css")
        self.assertIn("image-rendering: pixelated", css)
        self.assertRegex(css, r"prefers-reduced-motion: no-preference\) \{\s*\.panel-pic img \{ animation")

    def test_markers_are_buttons_with_notes(self):
        game, css = read("game.js"), read("style.css")
        self.assertIn('type: "button", class: "hotspot"', game)
        self.assertIn('"aria-describedby": id', game)
        self.assertIn('e.key === "Escape"', game)
        self.assertNotIn(".setAttribute(\"style\"", game, "the page's CSP blocks style attributes")
        self.assertRegex(css, r"prefers-reduced-motion: no-preference\) \{\s*\.hotspot \{ animation")
        self.assertIn(".hotspot:focus-visible", css)

    def test_art_takes_no_other_options(self):
        with self.assertRaises(SystemExit), redirect_stderr(StringIO()):
            build.main(["--art", "--page"])


def words(text):
    return re.findall(r"[a-z0-9']+", text.lower().replace("\u2019", "'"))


def phrases(text, n=4):
    w = words(text)
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


class SceneTextTest(unittest.TestCase):
    """game/SPOILERS-content/scene-art.md: the panels' text and hotspots."""

    def setUp(self):
        self.art = build.scene_art(CONTENT)

    def panels(self):
        for title, panels in self.art.items():
            for p in panels:
                yield title, p

    def texts(self, panel):
        for key in ("where", "headline", "sound", "body"):
            if panel.get(key):
                yield panel[key]
        for h in panel["hotspots"]:
            yield h["label"]
            yield h["body"]

    def test_hotspots_have_text(self):
        for title, p in self.panels():
            for h in p["hotspots"]:
                self.assertTrue(h["label"].strip() and h["body"].strip(), title)

    def hotspots(self, card):
        return {h["label"]: h["body"] for p in self.art[card] for h in p["hotspots"]}

    def test_the_interviews_do_not_describe_what_the_clerks_wear(self):
        # The captain's call: the three first interviews say nothing of clothes (the pictures still show them).
        for card in ("T-A \u00b7 Agnes \u00b7 03:30", "T-B \u00b7 Bertram \u00b7 03:40", "T-C \u00b7 Clement \u00b7 03:20"):
            self.assertEqual([l for l in self.hotspots(card) if "sweater" in l.lower()], [], card)
            body = next(t.body for t in CONTENT.testimonies if t.title == card)
            for text in list(self.hotspots(card).values()) + [body] + [f["body"] for f in self.art[card]]:
                self.assertNotRegex(text.lower(), r"sweater|knitted|jumper", card)

    def test_the_break_room_clip_has_the_chart_and_an_unnamed_person(self):
        spots = self.hotspots("Break Room 2")
        self.assertIn("4 \u00b7 Clement", spots["The seating chart"])
        self.assertNotIn("Clement", spots["The person"])
        self.assertNotIn("Clement", "".join(b for label, b in spots.items() if label != "The seating chart"))

    def test_the_decoys_have_hotspots_and_clements_folder_has_one_thing(self):
        self.assertIn("The sticky note", self.hotspots("Agnes at home"))
        self.assertIn("The evacuation plan", self.hotspots("Agnes at home"))
        self.assertIn("The letter", self.hotspots("Bertram at home"))
        self.assertIn("The receipt", self.hotspots("Bertram at home"))
        folder = self.hotspots("Clement at home")
        self.assertEqual(sorted(folder), ["Clement", "The note"])
        self.assertIn("— B.", folder["The note"])

    def test_the_redrawn_pictures_are_there(self):
        for name in ("scene-break-room", "scene-power-cut", "portrait-agnes", "portrait-bertram", "portrait-agnes-push",
                     "portrait-bertram-push", "portrait-clement-push", "scene-agnes-home", "scene-bertram-home",
                     "scene-clement-home", "scene-break-room-camera", "scene-outside-world"):
            self.assertIn(name, build.pictures())

    def test_hotspots_only_on_pictures_there_are(self):
        # A placeholder has no picture to point at: its hotspots come with its art.
        for title, p in self.panels():
            if p["hotspots"]:
                self.assertIn(p["image"], build.pictures(), title)

    def test_hotspots_sit_inside_the_image(self):
        for title, p in self.panels():
            for h in p["hotspots"]:
                for v in (h["x"], h["y"]):
                    self.assertTrue(3 <= v <= 97, f"{title}: {h['label']} is at the edge of the image")
            # Markers far enough apart to tap: 4% of the width is about 14px on a phone.
            spots = p["hotspots"]
            for i, a in enumerate(spots):
                for b in spots[i + 1:]:
                    self.assertGreater(abs(a["x"] - b["x"]) + abs(a["y"] - b["y"]) / 3, 4,
                                       f"{title}: {a['label']} and {b['label']} overlap")

    def test_hotspots_say_more_than_a_name(self):
        for title, p in self.panels():
            bodies = [h["body"] for h in p["hotspots"]]
            self.assertEqual(len(bodies), len(set(bodies)), f"{title}: two hotspots say the same thing")
            for h in p["hotspots"]:
                self.assertGreater(len(words(h["body"])), 4, f"{title}: {h['label']} says too little")

    def test_panels_stay_short(self):
        # A headline is a few words; the text under a picture is a few short lines.
        for title, p in self.panels():
            if p.get("headline"):
                self.assertLessEqual(len(words(p["headline"])), 8, title)
            # Lines marked "(drawn)" are in the picture, so they don't show under it.
            shown = [l for l in p["body"].splitlines() if not l.startswith("(drawn) ")]
            if p.get("style") != "role":
                self.assertLessEqual(len(shown), 8, title)

    def test_no_tell_tale_absences(self):
        # Saying what someone isn't wearing points at what matters.
        for title, p in self.panels():
            for text in self.texts(p):
                self.assertNotRegex(text.lower(), r"\bno (scarf|sweater|pattern)", title)
        for card in all_cards():
            self.assertNotRegex(card.body.lower(), r"\bno (scarf|sweater|pattern)", card.title)

    def test_nothing_from_the_reveal(self):
        # Any four words in a row that the reveal has must also be in a card the player sees.
        reveal = set().union(*(phrases(c.body) | phrases(c.title) for c in CONTENT.reveal.cards))
        shown = set().union(*(phrases(c.body) for c in all_cards()))
        for title, p in self.panels():
            for text in self.texts(p):
                self.assertFalse((phrases(text) & reveal) - shown, f"{title}: panel text quotes the reveal")

    def test_names_and_numbers_come_from_the_cards(self):
        # Panel text retells the cards: no name, place, time or number the cards don't have.
        known = {t.lower() for c in all_cards() for t in re.findall(r"[A-Za-z0-9]+", c.title + " " + c.body)}
        for title, p in self.panels():
            for text in self.texts(p):
                for m in re.finditer(r"[A-Za-z0-9]+", text):
                    t, before = m.group(), text[:m.start()].rstrip(" *\"(\u201c>●↓♪-")
                    name = t[0].isupper() and before and before[-1] not in ".!?:\n"
                    if any(ch.isdigit() for ch in t) or name:
                        self.assertTrue(t.lower() in known, f"{title}: {t!r}, a name or number that no card has")

    def test_a_changed_card_stops_the_build(self):
        changed = content.load()
        changed.advert.body += "\nOne more line."
        with self.assertRaises(content.ContentError):
            build.scene_art(changed)


def fake_template():
    return {
        "package.json": '{"name": "grafana-page"}\n',
        "pnpm-lock.yaml": "lockfileVersion: '9.0'\n",
        "pnpm-workspace.yaml": "packages:\n  - packages/*\n",
        "tsconfig.json": "{}\n",
        "packages/pages-sdk/src/index.ts": "export {};\n",
        "pages.design.json": '{"style":"grafana-native"}',
        "pages.bindings.json": '{"logs": {"datasourceUid": "abc"}}',
        "src/App.tsx": "export const App = () => null;\n",
        "AGENTS.md": "someone else's notes\n",
    }


class PageBuildTest(unittest.TestCase):
    def setUp(self):
        self.doc = json.loads(build.render_page(fake_template(), CONTENT))
        self.files = self.doc["source"]["files"]

    def test_page_export_shape(self):
        self.assertEqual(self.doc["kind"], "PageExport")
        self.assertEqual(self.doc["version"], 2)
        self.assertEqual(self.doc["__inputs"], [])
        self.assertEqual(self.doc["source"]["version"], 1)
        self.assertEqual(self.doc["source"]["binaryFiles"], {})

    def test_takes_only_the_project_from_the_template(self):
        for name in ("package.json", "pnpm-lock.yaml", "pnpm-workspace.yaml", "tsconfig.json",
                     "packages/pages-sdk/src/index.ts"):
            self.assertEqual(self.files[name], fake_template()[name])
        for name in ("src/App.tsx", "pages.design.json", "AGENTS.md"):
            self.assertNotIn(name, self.files)
        self.assertEqual(json.loads(self.files["pages.bindings.json"]), {})

    def test_page_runs_the_web_game(self):
        self.assertEqual(self.files["src/game.js"], read("game.js"))
        self.assertEqual(self.files["src/style.css"], read("style.css"))
        self.assertEqual(self.files["src/SPOILERS-content.js"], build.render(CONTENT))
        main = self.files["src/main.tsx"]
        order = [main.index(f"import '{name}'") for name in ("./style.css", "./SPOILERS-content.js", "./game.js")]
        self.assertEqual(order, sorted(order))
        self.assertLess(main.index("from './host'"), order[0])
        self.assertIn("pageReady", main)
        for name in ("src/game.d.ts", "src/SPOILERS-content.d.ts", "src/host.ts", "src/markup.ts", "src/page.css"):
            self.assertIn(name, self.files)

    def test_page_inlines_the_scenes(self):
        index = self.files["src/scenes.ts"]
        for name in build.IMAGES:
            if name not in build.pictures():
                self.assertNotIn(f"src/scenes/{name}.ts", self.files)
                continue
            with open(build.scene_path(name), "rb") as f:
                url = "data:image/webp;base64," + base64.b64encode(f.read()).decode("ascii")
            self.assertIn(f"'{url}'", self.files[f"src/scenes/{name}.ts"])
            self.assertIn(f"from './scenes/{name}'", index)
        self.assertIn("scenes: SCENES", self.files["src/host.ts"])
        for name in build.pictures():
            self.assertLess(len(self.files[f"src/scenes/{name}.ts"].encode("utf-8")), 120 * 1024,
                            f"{name}: Grafana writes a page's files at most 128 KB at a time")
        self.assertLess(len(build.render_page(fake_template(), CONTENT).encode("utf-8")), 4 << 20,
                        "the page file should stay well inside Grafana's limits")

    def test_markup_is_the_page_body(self):
        markup = json.loads(self.files["src/markup.ts"].split("export const MARKUP = ", 1)[1].rstrip().rstrip(";"))
        for needle in ('id="main"', 'id="restart-dialog"', 'id="status"', 'id="theme-toggle"'):
            self.assertIn(needle, markup)
        self.assertNotIn("<script", markup)
        self.assertNotIn("<noscript", markup)

    def test_no_spoilers_outside_the_encoded_reveal(self):
        self.assertEqual(self.doc["title"], "The Defiant Jazz Incident")
        text = build.render_page(fake_template(), CONTENT)
        for card in CONTENT.reveal.cards:
            for line in card.body.splitlines():
                if len(line.strip()) >= 25:
                    self.assertNotIn(line.strip(), text, "reveal text is readable in the page")
        # Assistant gets the question only, never story text as context.
        host = self.files["src/host.ts"]
        self.assertEqual(re.findall(r"openAssistant\(([^)]*)\)", host), ["{ prompt }", "{ prompt }"])

    def test_file_keeps_spoilers_in_its_name(self):
        self.assertTrue(os.path.basename(build.PAGE_PATH).startswith("SPOILERS-"))


class PageTemplateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def write(self, name, doc):
        path = os.path.join(self.tmp.name, name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(doc, f)
        return path

    def test_reads_an_exported_file_or_the_export_api(self):
        files = fake_template()
        exported = self.write("a.page.json", {"kind": "PageExport", "version": 2, "title": "x",
                                              "source": {"version": 1, "files": files, "binaryFiles": {}}})
        api = self.write("b.json", {"status": "success", "data": {"source": {"version": 1, "files": {
            k: base64.b64encode(v.encode("utf-8")).decode("ascii") for k, v in files.items()}}}})
        self.assertEqual(build.read_template(exported), files)
        self.assertEqual(build.read_template(api), files)

    def test_rejects_other_files(self):
        with self.assertRaises(SystemExit):
            build.read_template(self.write("c.json", {"dashboard": {}}))
        incomplete = {k: v for k, v in fake_template().items() if not k.startswith("packages/")}
        with self.assertRaises(SystemExit):
            build.read_template(self.write("d.json", {"kind": "PageExport", "source": {"files": incomplete}}))

    def test_build_and_check(self):
        out = os.path.join(self.tmp.name, "dist", "SPOILERS-defiantjazz.page.json")
        template = self.write("t.page.json", {"kind": "PageExport", "version": 2, "title": "x",
                                              "source": {"version": 1, "files": fake_template(), "binaryFiles": {}}})
        quiet = redirect_stdout(StringIO())
        with mock.patch.object(build, "PAGE_PATH", out), quiet:
            with self.assertRaises(SystemExit):
                build.main(["--page"])                       # no template yet
            build.main(["--page", "--template", template])
            build.main(["--page", "--check"])                # rebuilt from its own project
            build.main(["--page"])
            with open(out, encoding="utf-8") as f:
                doc = json.load(f)
            doc["source"]["files"]["src/game.js"] = "// stale\n"
            with open(out, "w", encoding="utf-8") as f:
                json.dump(doc, f)
            with self.assertRaises(SystemExit):
                build.main(["--page", "--check"])
        with self.assertRaises(SystemExit), redirect_stderr(StringIO()):
            build.main(["--template", template])            # --template needs --page


class MusicTest(unittest.TestCase):
    """The jazz is a licensed track: only a build with its own, uncommitted copy plays it."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        for name, value in (("PRIVATE", os.path.join(self.tmp.name, "private")),
                            ("LOCAL_PAGE", os.path.join(self.tmp.name, "with-music.html"))):
            patcher = mock.patch.object(build, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        env = mock.patch.dict(os.environ)
        env.start()
        self.addCleanup(env.stop)
        os.environ.pop("DJ_MUSIC_FILE", None)
        self.clip = b"ID3" + bytes(range(256)) * 1200

    def add_track(self):
        os.makedirs(build.PRIVATE)
        with open(os.path.join(build.PRIVATE, "hot-pursuits.mp3"), "wb") as f:
            f.write(b"the whole track")

    def fake_ffmpeg(self, args, check):
        with open(args[-1], "wb") as f:
            f.write(self.clip)

    def test_silent_without_the_track(self):
        self.assertIsNone(build.music_clip())
        files = build.page_files(fake_template(), CONTENT)
        self.assertIn("MUSIC: string | undefined = undefined", files["src/music.ts"])
        self.assertFalse([name for name in files if name.startswith("src/music/")])
        self.assertNotIn("audio/", json.dumps(files))
        build.write_local_music()
        self.assertFalse(os.path.exists(build.LOCAL_PAGE))

    def test_the_build_has_music_only_with_the_track(self):
        self.add_track()
        quiet = redirect_stdout(StringIO())
        with mock.patch.object(build.subprocess, "run", self.fake_ffmpeg), quiet:
            files = build.page_files(fake_template(), CONTENT)
            build.write_local_music()
        parts = sorted((name for name in files if name.startswith("src/music/")),
                       key=lambda name: int(re.search(r"\d+", name).group()))
        self.assertGreater(len(parts), 1)
        for name in parts:
            self.assertLess(len(files[name].encode("utf-8")), 120 * 1024,
                            f"{name}: Grafana writes a page's files at most 128 KB at a time")
        data = "".join(files[name].split("'")[1] for name in parts)
        self.assertEqual(base64.b64decode(data), self.clip)
        self.assertIn("'data:audio/mpeg;base64,' + part0", files["src/music.ts"])
        self.assertIn("music: MUSIC", files["src/host.ts"])
        with open(build.LOCAL_PAGE, encoding="utf-8") as f:
            page = f.read()
        script = os.path.relpath(os.path.join(build.PRIVATE, "music.js"), HERE)
        self.assertLess(page.index(f'src="{script}"'), page.index('src="SPOILERS-content.js"'))
        with open(os.path.join(build.PRIVATE, "music.js"), encoding="utf-8") as f:
            self.assertIn("data:audio/mpeg;base64," + base64.b64encode(self.clip).decode("ascii"), f.read())
        # Without the track again, the files it made go.
        os.remove(os.path.join(build.PRIVATE, "hot-pursuits.mp3"))
        build.write_local_music()
        self.assertFalse(os.path.exists(build.LOCAL_PAGE))
        self.assertFalse(os.path.exists(os.path.join(build.PRIVATE, "music.js")))

    def test_dj_music_file_names_the_track(self):
        track = os.path.join(self.tmp.name, "elsewhere.mp3")
        with open(track, "wb") as f:
            f.write(b"the whole track")
        os.environ["DJ_MUSIC_FILE"] = track
        with mock.patch.object(build.subprocess, "run", self.fake_ffmpeg):
            self.assertTrue(build.music_clip().startswith(build.PRIVATE))

    def test_without_ffmpeg_it_builds_silent(self):
        self.add_track()
        with mock.patch.object(build.subprocess, "run", side_effect=FileNotFoundError("ffmpeg")), \
                redirect_stderr(StringIO()):
            self.assertIsNone(build.music_clip())

    def test_the_repository_never_has_the_track(self):
        ignored = read(os.path.join("..", ".gitignore")).splitlines()
        self.assertIn("web/assets/private/", ignored)
        self.assertIn("web/with-music.html", ignored)
        self.assertNotIn("audio/", read("SPOILERS-content.js"))
        self.assertNotIn("private", read("index.html"))
        # One panel of the cold open plays it.
        art = bundle_data()["art"]
        playing = [f for frames in art.values() for f in frames if f.get("music")]
        self.assertEqual(len(playing), 1)
        self.assertIn(playing[0], art[CONTENT.cold_open.title])


class DashboardTest(unittest.TestCase):
    def test_example_dashboard(self):
        dash = json.loads(read("dashboard-example.json"))
        game = dash["panels"][0]
        self.assertEqual(game["type"], "innius-video-panel")
        self.assertEqual(game["options"]["videoType"], "iframe")
        self.assertTrue(game["options"]["iframeURL"].startswith("https://"))
        self.assertEqual(game["gridPos"]["w"], 24)
        self.assertEqual(game["gridPos"]["y"], 0)


if __name__ == "__main__":
    unittest.main()


# ---- Play statistics -------------------------------------------------------------------

COLLECTOR = "https://faro-collector-prod-us-central-0.grafana.net/collect/0123456789abcdef0123456789abcdef"
FARO = {"url": COLLECTOR, "environment": "prod"}


def faro_template():
    """A project whose lockfile already resolves the pinned Faro SDK, as Grafana's page template does."""
    files = fake_template()
    files["package.json"] = json.dumps({"name": "grafana-page", "dependencies": {
        "@grafana/data": "13.2.2", "@grafana/i18n": "13.2.2", "react": "19.3.0"}}, indent=2) + "\n"
    files["pnpm-lock.yaml"] = (
        "lockfileVersion: '9.0'\n\nimporters:\n\n  .:\n    dependencies:\n"
        "      '@grafana/data':\n        specifier: 13.2.2\n        version: 13.2.2(react@19.3.0)\n"
        "      '@grafana/i18n':\n        specifier: 13.2.2\n        version: 13.2.2(react@19.3.0)\n"
        "      react:\n        specifier: 19.3.0\n        version: 19.3.0\n"
        "    devDependencies:\n      typescript:\n        specifier: 7.0.2\n        version: 7.0.2\n"
        "\npackages:\n\n  '@grafana/faro-web-sdk@2.11.0':\n    resolution: {integrity: sha512-x}\n")
    return files


def track_calls(game):
    """Every track("name", {...}) call in game.js: (event, [attribute names], the object's text)."""
    calls = []
    for match in re.finditer(r'\btrack\("([a-z_]+)", ', game):
        start = match.end()
        if game[start] != "{":
            calls.append((match.group(1), None, game[start:start + 40]))
            continue
        depth, end = 0, start
        while True:
            depth += {"{": 1, "}": -1}.get(game[end], 0)
            end += 1
            if depth == 0:
                break
        body = game[start:end]
        inner = body[1:-1]
        keys, level, word = [], 0, ""
        for part in re.split(r"(,|\(|\)|\{|\})", inner):
            if part in ("(", "{"):
                level += 1
            elif part in (")", "}"):
                level -= 1
            elif part == "," and level == 0:
                word = ""
            elif level == 0 and not word and part.strip():
                keys.append(part.strip().split(":")[0].strip())
                word = part
        calls.append((match.group(1), keys, body))
    return calls


class PlayStatisticsTest(unittest.TestCase):
    """HOST.track is optional: the static page and the terminal game never record anything."""

    def test_game_reports_only_the_listed_events(self):
        calls = track_calls(read("game.js"))
        self.assertEqual({name for name, _, _ in calls}, set(build.TRACK_EVENTS))
        for name, keys, body in calls:
            self.assertIsNotNone(keys, f"{name}: pass track a literal object of attributes")
            self.assertLessEqual(set(keys), set(build.TRACK_EVENTS[name]), f"{name}: {body}")

    def test_the_hook_is_optional_and_never_in_the_way(self):
        game = read("game.js")
        helper = game.split("function track(name, attrs) {", 1)[1].split("\n  }\n", 1)[0]
        self.assertIn("if (!HOST.track) return;", helper)
        self.assertIn("String(attrs[k])", helper)
        self.assertIn("catch (e)", helper)
        # Neither the static page nor the terminal game has a collector or any of Faro.
        self.assertNotIn("faro", game.lower())
        self.assertNotIn("faro", read("index.html").lower())
        self.assertNotIn("DJ_HOST", read("index.html"))
        root = os.path.dirname(HERE)
        for name in sorted(os.listdir(os.path.join(root, "game"))):
            if name.endswith(".py") and not name.startswith("test_"):
                text = open(os.path.join(root, "game", name), encoding="utf-8").read().lower()
                self.assertNotIn("faro", text, name)
                self.assertNotRegex(text, r"\btrack\(", name)

    def test_no_free_text_leaves_the_page(self):
        game = read("game.js")
        calls = {name: body for name, _, body in track_calls(game)}
        # An accusation is a suspect's key or "other", and the reasoning is only its length.
        accused = calls["accusation_made"]
        self.assertIn("suspect: a.key", accused)
        self.assertIn('reasoning_length: answerOf("why").length', accused)
        for typed in ("a.label", "draft.other", ".other", "reasoning.value", "answers"):
            self.assertNotIn(typed, accused)
        # The question text and the story text stay out of it: only an id and a length.
        asked = calls["ai_question_asked"]
        self.assertIn("question_length: text.length", asked)
        self.assertNotRegex(asked.replace("question_length: text.length", ""), r"\btext\b")
        # Nothing is recorded as the player types.
        for line in game.splitlines():
            if 'addEventListener("input"' in line or 'addEventListener("keydown"' in line:
                self.assertNotIn("track(", line)
        # Clues are the picture's name and the marker's number, and the label the marker already shows.
        self.assertIn('clue: image + "." + (i + 1), label: h.label', game)

    def test_only_a_listed_suspect_or_other_is_an_accusation(self):
        game = read("game.js")
        self.assertIn('is_listed_suspect: a.key !== "other"', game)
        # accusation() maps question 1's answer to a suspect's key, or to "other" with the typed text only as a label.
        self.assertIn('return { key: "other", label: text.length > 40', game)

    def test_correct_is_only_known_after_the_accusation(self):
        game = read("game.js")
        self.assertIn('correct: verdict.meta.correct === "yes"', game)
        self.assertNotRegex(game, r"===?\s*[\"']clement")
        self.assertNotIn('"correct"', read("SPOILERS-content.js"))
        reveal = json.loads(base64.b64decode(bundle_data()["reveal"]).decode("utf-8"))
        right = [card for card in reveal if card["meta"].get("correct") == "yes"]
        self.assertEqual(len(right), 1)
        self.assertIn(right[0]["meta"]["for"], build.content.SUSPECTS)

    def test_the_title_does_not_announce_play_statistics(self):
        game = read("game.js")
        self.assertNotIn("track-note", game)
        self.assertNotIn("anonymous play statistics", game)
        self.assertNotIn("track-note", read("style.css"))
        self.assertNotIn("play statistics", read("index.html"))

    def test_the_verdict_has_no_you_named_title(self):
        game = read("game.js")
        self.assertNotIn("You named", game)
        self.assertIn("You accused ", game)
        self.assertIn("card(verdict, false)", game)

    def test_clue_ids_are_unique(self):
        ids = []
        for frames in bundle_data()["art"].values():
            for frame in frames:
                ids += [f"{frame['image']}.{i + 1}" for i, _ in enumerate(frame["hotspots"])]
        self.assertTrue(ids)
        self.assertEqual(len(ids), len(set(ids)))


class FaroConfigTest(unittest.TestCase):
    def test_off_without_a_collector(self):
        self.assertIsNone(build.faro_config({}))
        self.assertIsNone(build.faro_config({"DJ_FARO_URL": "  "}))

    def test_reads_the_collector_and_environment(self):
        self.assertEqual(build.faro_config({"DJ_FARO_URL": COLLECTOR}), FARO)
        self.assertEqual(build.faro_config({"DJ_FARO_URL": COLLECTOR, "DJ_FARO_ENV": "dev"})["environment"], "dev")

    def test_rejects_what_is_not_a_collector(self):
        for url in ("http://faro-collector-x.grafana.net/collect/abc", "https://example.net/other/abc",
                    "https://faro-collector-x.grafana.net/collect/", COLLECTOR + "?x=1", "https://u:p@h.net/collect/a",
                    "https://h.net/collect/a'b"):
            with self.assertRaises(SystemExit, msg=url):
                build.faro_config({"DJ_FARO_URL": url})
        with self.assertRaises(SystemExit):
            build.faro_config({"DJ_FARO_URL": COLLECTOR, "DJ_FARO_ENV": "Prod; drop"})

    def test_the_repository_has_no_collector_or_app_key(self):
        root = os.path.dirname(HERE)
        found = []
        for folder, dirs, names in os.walk(root):
            dirs[:] = [d for d in dirs if d not in (".git", "dist", "private", "__pycache__", "node_modules")]
            for name in names:
                if name.endswith((".webp", ".png", ".jpg", ".mp3", ".pyc")):
                    continue
                path = os.path.join(folder, name)
                with open(path, encoding="utf-8", errors="ignore") as f:
                    if re.search(r"faro-collector-[a-z0-9-]+\.grafana[a-z-]*\.net/collect/[0-9a-f]{8}", f.read()):
                        found.append(os.path.relpath(path, root))
        self.assertEqual([p for p in found if not p.endswith("test_web.py")], [])


class TrackedPageTest(unittest.TestCase):
    def setUp(self):
        self.files = build.page_files(faro_template(), CONTENT, FARO)
        self.track = self.files["src/track.ts"]

    def test_without_a_collector_the_page_has_no_faro(self):
        plain = build.page_files(faro_template(), CONTENT)
        self.assertNotIn("src/track.ts", plain)
        for name in ("src/host.ts", "src/main.tsx", "src/game.js", "src/markup.ts", "src/page.css"):
            self.assertNotIn("faro", plain[name].lower(), name)
        self.assertEqual(plain["package.json"], faro_template()["package.json"])
        self.assertEqual(plain["pnpm-lock.yaml"], faro_template()["pnpm-lock.yaml"])
        self.assertNotIn("track", plain["src/host.ts"])

    def test_pins_the_sdk_as_a_direct_dependency(self):
        package = json.loads(self.files["package.json"])
        self.assertEqual(package["dependencies"]["@grafana/faro-web-sdk"], "2.11.0")
        self.assertEqual(list(package["dependencies"]), sorted(package["dependencies"]))
        lock = self.files["pnpm-lock.yaml"]
        self.assertIn("      '@grafana/faro-web-sdk':\n        specifier: 2.11.0\n        version: 2.11.0\n", lock)
        self.assertLess(lock.index("'@grafana/data':"), lock.index("'@grafana/faro-web-sdk':"))
        self.assertLess(lock.index("'@grafana/faro-web-sdk':"), lock.index("'@grafana/i18n':"))
        self.assertEqual(lock.count("'@grafana/faro-web-sdk':\n        specifier"), 1)

    def test_a_build_does_not_depend_on_the_last_one(self):
        again = build.page_files(self.files, CONTENT, FARO)
        self.assertEqual(again["package.json"], self.files["package.json"])
        self.assertEqual(again["pnpm-lock.yaml"], self.files["pnpm-lock.yaml"])
        plain = build.page_files(self.files, CONTENT)
        self.assertEqual(plain["package.json"], faro_template()["package.json"])
        self.assertEqual(plain["pnpm-lock.yaml"], faro_template()["pnpm-lock.yaml"])

    def test_a_template_that_cannot_resolve_the_sdk_stops_the_build(self):
        with self.assertRaises(SystemExit):
            build.page_files(fake_template(), CONTENT, FARO)

    def test_host_gets_the_hook(self):
        host = self.files["src/host.ts"]
        self.assertIn("import { track } from './track';", host)
        self.assertIn("\n  track,\n", host)
        self.assertEqual(re.findall(r"openAssistant\(([^)]*)\)", host), ["{ prompt }", "{ prompt }"])

    def test_the_collector_is_an_input_not_part_of_the_source(self):
        self.assertIn(f"url: '{COLLECTOR}'", self.track)
        others = {k: v for k, v in self.files.items() if k != "src/track.ts" and k.startswith(("src/", "package", "pnpm"))}
        self.assertNotIn("0123456789abcdef0123456789abcdef", json.dumps(others))
        for name in ("build.py", "game.js", "README.md"):
            self.assertNotRegex(read(name), r"/collect/[0-9a-f]{8}")

    def test_faro_setup(self):
        track = self.track
        self.assertIn("captureConsole: false", track)
        self.assertNotIn("captureConsole: true", track)
        self.assertIn("app: { name: 'defiant-jazz', version: APP_VERSION, environment: ENVIRONMENT }", track)
        self.assertRegex(track, r"const APP_VERSION = 'web-[0-9a-f]{8}';")
        self.assertIn("const ENVIRONMENT = 'prod';", track)
        self.assertIn("const DOMAIN = 'defiant-jazz';", track)
        self.assertNotIn("tracing", track.lower().replace("// ", ""))
        dev = build.page_files(faro_template(), CONTENT, {**FARO, "environment": "dev"})["src/track.ts"]
        self.assertIn("const ENVIRONMENT = 'dev';", dev)

    def test_player_is_a_random_id_in_user_storage(self):
        track = self.track
        self.assertIn("const PLAYER_KEY = 'dj_player_id';", track)
        self.assertIn("grafana.userStorage", track)
        self.assertIn("faro.api.setUser(", track)
        self.assertIn("p_' + Array.from(bytes", track)
        self.assertIn("player_id_source: 'user_storage'", track)
        # No storage, no id: marked, and never a stand-in id shared by everyone.
        self.assertIn("{ attributes: { player_id_source: 'none' } }", track)
        self.assertNotRegex(track, r"p_unknown|p_anon|p_none|p_0")

    def test_nothing_from_the_viewers_account_is_read_or_sent(self):
        for name in ("src/track.ts", "src/host.ts"):
            text = "\n".join(line for line in self.files[name].splitlines() if not line.strip().startswith("//"))
            for account in ("viewer", "usePageContext", "login", "email", "userName"):
                self.assertNotIn(account, text, f"{name} mentions {account}")
        self.assertNotRegex(self.track, r"attributes: \{ (?!player_id_source)")

    def test_events_are_the_listed_ones_and_strings(self):
        listed = json.loads(self.track.split("const EVENTS: Record<string, string[]> = ", 1)[1].split(";\nconst", 1)[0])
        self.assertEqual(listed, {k: list(v) for k, v in build.TRACK_EVENTS.items()})
        self.assertIn("String(attrs[key]).slice(0, MAX_VALUE)", self.track)
        self.assertIn("app_version: APP_VERSION, environment: ENVIRONMENT", self.track)
        self.assertIn("faro.api.pushEvent(name, data, DOMAIN)", self.track)
        for event, keys in build.TRACK_EVENTS.items():
            for key in keys:
                self.assertRegex(key, r"^[a-z_]+$")
        # The one thing a player types that is recorded is the optional leaderboard name; "killer" is the
        # points for question 1, in the scored accusation only. Neither is an answer.
        for event, keys in build.TRACK_EVENTS.items():
            for text in ("text", "name", "reasoning", "question", "answer", "solution", "killer", "login"):
                if event == "accusation_scored" and text in ("name", "killer"):
                    continue
                self.assertNotIn(text, keys, event)

    def test_version_follows_the_game(self):
        first = build.app_version(CONTENT)
        self.assertRegex(first, r"^web-[0-9a-f]{8}$")
        with mock.patch.object(build, "HERE", self.tmp_game()):
            self.assertNotEqual(build.app_version(CONTENT), first)

    def tmp_game(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        with open(os.path.join(tmp.name, "game.js"), "w", encoding="utf-8") as f:
            f.write("// another game\n")
        return tmp.name

    def test_build_and_check_follow_the_environment(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        template = os.path.join(tmp.name, "t.page.json")
        with open(template, "w", encoding="utf-8") as f:
            json.dump({"kind": "PageExport", "version": 2, "title": "x",
                       "source": {"version": 1, "files": faro_template(), "binaryFiles": {}}}, f)
        out = os.path.join(tmp.name, "dist", "out.page.json")
        env = mock.patch.dict(os.environ, {"DJ_FARO_URL": COLLECTOR, "DJ_FARO_ENV": "dev"})
        with mock.patch.object(build, "PAGE_PATH", out), env:
            say = StringIO()
            with redirect_stdout(say):
                build.main(["--page", "--template", template])
            self.assertIn("Play statistics: on, to faro-collector-prod-us-central-0.grafana.net, environment dev.", say.getvalue())
            self.assertNotIn("0123456789abcdef", say.getvalue())
            with redirect_stdout(StringIO()):
                build.main(["--page", "--check"])
            with open(out, encoding="utf-8") as f:
                self.assertIn("src/track.ts", json.load(f)["source"]["files"])
            os.environ.pop("DJ_FARO_URL")
            with self.assertRaises(SystemExit), redirect_stdout(StringIO()):
                build.main(["--page", "--check"])
            say = StringIO()
            with redirect_stdout(say):
                build.main(["--page"])
            self.assertIn("Play statistics: off", say.getvalue())


class StatisticsDashboardTest(unittest.TestCase):
    def test_seven_panels_over_the_game_events_without_test_traffic(self):
        dash = json.loads(read("dashboard-play-statistics.json"))
        self.assertEqual(len(dash["panels"]), 7)
        self.assertEqual({v["name"] for v in dash["templating"]["list"]}, {"loki", "environment", "exclude"})
        text = json.dumps(dash)
        self.assertNotIn("0123456789", text)
        for panel in dash["panels"]:
            self.assertEqual(panel["datasource"]["uid"], "${loki}")
            for target in panel["targets"]:
                expr = target["expr"]
                self.assertIn('browser_name!="Chrome Headless"', expr)
                # Only the leaderboard also takes players who added their score from the local game (see local.js).
                if panel["title"] == "Leaderboard":
                    self.assertIn('user_attr_player_id_source=~"user_storage|local_storage"', expr)
                else:
                    self.assertIn('user_attr_player_id_source="user_storage"', expr)
                self.assertIn('user_id!~"$exclude"', expr)
                self.assertIn('event_domain="defiant-jazz"', expr)
                for event in re.findall(r'event_name="([a-z_]+)"', expr):
                    self.assertIn(event, build.TRACK_EVENTS)
            self.assertEqual(len({t["refId"] for t in panel["targets"]}), len(panel["targets"]))
        # The leaderboard counts each player once, best score first, ties to the earliest finish, with no answers.
        board = dash["panels"][-1]
        self.assertEqual(board["title"], "Leaderboard")
        self.assertIn('event_name="accusation_scored"', board["targets"][0]["expr"])
        self.assertNotIn("answer", json.dumps(board).lower())
        self.assertIn({"id": "limit", "options": {"limitField": 25}}, board["transformations"])
        sorts = [t for t in board["transformations"] if t["id"] == "sortBy"]
        self.assertEqual(sorts[0]["options"]["sort"], [{"field": "event_data_score", "desc": True}, {"field": "timestamp"}])
        group = next(t for t in board["transformations"] if t["id"] == "groupBy")
        self.assertEqual(group["options"]["fields"]["user_id"]["operation"], "groupby")
        # Scores added from the local game (source=local) are marked "played locally", because nothing checks them.
        self.assertIn("event_data_source", board["targets"][0]["expr"])
        self.assertIn("event_data_source", group["options"]["fields"])
        badge = next(o for o in board["fieldConfig"]["overrides"] if o["matcher"]["options"] == "Played")
        self.assertIn("played locally", json.dumps(badge))


def plain(text):
    """Text as the player reads it: no markers, no punctuation, lower case, one space between words."""
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", text.replace("~~", "").lower()).split())


class AnimationTest(unittest.TestCase):
    """Frame sequences, the keyboard and the notes to read."""

    def setUp(self):
        self.art = build.scene_art(CONTENT)
        self.game = read("game.js")
        self.css = read("style.css")

    def panels(self):
        for title, panels in self.art.items():
            for p in panels:
                yield title, p

    def animated(self):
        return {p["image"]: p for _, p in self.panels() if p.get("frames") or p.get("animation")}

    def test_every_frame_is_a_picture_and_each_animation_has_its_pictures(self):
        for _, p in self.panels():
            for name in p.get("frames", []):
                self.assertIn(name, build.IMAGES)
                self.assertIn(name, build.pictures(), f"{name}: the frame's file")
            self.assertIn(p.get("animation", "slides"), build.ANIMATIONS)
        for who in ("agnes", "bertram", "clement"):
            for kind in ("lit", "dark"):
                self.assertIn(f"power-{kind}-{who}", build.pictures())

    def test_the_animated_panels(self):
        made = self.animated()
        # 03:02, 03:07, Break Room 2's camera, the three first interviews, the three pushes, the three visits at home.
        for image in ("scene-power-cut", "scene-corridor-cctv", "scene-break-room-camera", "portrait-agnes", "portrait-bertram",
                      "portrait-clement", "portrait-agnes-push", "portrait-bertram-push", "portrait-clement-push",
                      "scene-agnes-home", "scene-bertram-home", "scene-clement-home"):
            self.assertIn(image, made)
        for image in ("portrait-agnes", "portrait-bertram", "portrait-clement", "portrait-agnes-push", "portrait-bertram-push",
                      "portrait-clement-push", "scene-agnes-home", "scene-bertram-home", "scene-clement-home"):
            self.assertEqual(len(made[image]["frames"]), 2, image)  # three frames in all
        self.assertEqual(made["scene-power-cut"]["animation"], "power-cut")
        self.assertEqual(made["scene-break-room-camera"]["animation"], "cctv-break-room")
        self.assertEqual(made["scene-corridor-cctv"]["animation"], "cctv-corridor")

    def test_the_power_cut_plays_lit_one_at_a_time_then_dark_one_at_a_time(self):
        block = self.game.split('ANIMS["power-cut"] = ', 1)[1].split("\n  };", 1)[0]
        order = re.findall(r"later\(function \(\) \{ ([^}]*)\}, ([0-9.]+(?: \+ [0-9.]+ \* i)?)\)", block)
        text = " | ".join(a for a, _ in order)
        self.assertIn("on(c.lit)", text)
        self.assertLess(text.index("on(c.lit)"), text.index("on(cols[0].dark)"))
        self.assertLess(text.index("on(cols[0].dark)"), text.index("on(cols[1].dark)"))
        self.assertLess(text.index("on(cols[1].dark)"), text.index("on(cols[2].dark)"))
        # It ends dark, with the jazz; the lullaby is only a caption (the build has no lullaby track).
        self.assertIn("c.lit); on(c.dark)", block)
        self.assertIn("The lullaby", block)
        self.assertIn("music.follow(true)", block)

    def test_reduced_motion_shows_the_end_state(self):
        self.assertIn("prefers-reduced-motion: reduce", self.game)
        self.assertIn('pic.classList.add("pic-calm")', self.game)
        calm = self.game.split("if (calm) {", 1)[1].split("}", 1)[0]
        self.assertIn("finish(true)", calm)
        self.assertNotIn("a.play", calm)
        self.assertIn(".pic-calm img.anim-frame", self.css)

    def test_animation_does_not_move_the_buttons(self):
        # Frames sit over the first picture, which keeps the panel's shape; nothing is added to the flow.
        self.assertRegex(self.css, r"img\.anim-frame \{ position: absolute; inset: 0;")
        self.assertRegex(self.css, r"\.anim-stage \{ position: absolute; inset: 0;")
        self.assertIn("pic.style.aspectRatio", self.game)

    def test_next_works_during_an_animation_and_a_click_skips_it(self):
        # Timers belong to the view that started them: render() stops them all before it draws the next one.
        render = self.game.split("function render(moveFocus) {", 1)[1].split("\n  }\n", 1)[0]
        self.assertIn("stopAnimations();", render)
        self.assertIn('finish(true)', self.game)
        self.assertIn(".pic-playing .hotspot { visibility: hidden; }", self.css)

    def test_camera_clocks_only_show_times_the_story_states(self):
        stated = {"03:01:20", "03:02:00", "03:07:01", "03:07:03", "03:07:05"}
        self.assertEqual(set(re.findall(r"\b\d\d:\d\d:\d\d\b", self.game)), stated)
        # They tick forward, never down.
        self.assertNotRegex(self.game, r"now -= 1")
        # The records give the corridor camera 03:07:01 and Break Room 2's 03:07:03 (log lines at 03:07:01 to 03:07:05).
        records = open(os.path.join(HERE, "..", "telemetry", "system.log"), encoding="utf-8").read()
        for stamp in ("03:07:01", "03:07:03", "03:07:05", "03:02:00"):
            self.assertIn("T" + stamp, records)

    def test_enter_starts_from_the_title_and_arrows_never_choose(self):
        self.assertIn("titleStart = function ()", self.game)
        handler = self.game.split('document.addEventListener("keydown"', 1)[1].split("\n  });", 1)[0]
        # A focused button, link or field does what it does itself.
        self.assertIn("INPUT|TEXTAREA|SELECT|BUTTON|A|SUMMARY", handler)
        self.assertIn('e.key === "Enter" && titleStart', handler)
        # Every story step has an arrow-key way on and (but the first) back.
        for view in ("advert", "cold", "statement", "outside", "result", "card"):
            body = self.game.split(f"views.{view} = function", 1)[1].split("\n  };", 1)[0]
            self.assertIn("forward:", body, view)
        # A decision, an accusation and a confirmation set no key navigation at all.
        for view in ("lead", "accuse", "confirm"):
            body = self.game.split(f"views.{view} = function", 1)[1].split("\n  };", 1)[0]
            self.assertNotIn("keyNav", body, view)
            self.assertNotIn("forward:", body, view)
        # The arrows ignore the game while a note is open.
        self.assertLess(handler.index("if (reading)"), handler.index('"ArrowRight"'))

    def test_the_game_asks_for_the_keyboard_once_it_appears(self):
        # A Page's frame starts without focus, so Enter on the title would reach nothing until a click.
        tail = self.game.split("readStored(STORE_KEY).then(function (text) {", 1)[1]
        self.assertIn("window.focus()", tail.split("});", 1)[0])

    def test_notes_are_read_on_click(self):
        game = self.game
        self.assertIn('class: "hotspot hotspot-read"', game)
        self.assertIn('"aria-haspopup": "dialog"', game)
        self.assertIn('role: "dialog", "aria-modal": "true"', game)
        handler = game.split('document.addEventListener("keydown"', 1)[1].split("\n  });", 1)[0]
        self.assertIn("closeRead(true)", handler.split("if (reading)", 1)[1].split("return;", 1)[0])
        # Every note drawn in a picture opens enlarged, and says exactly what its card says.
        cards = {c.title: c.body for c in all_cards()}
        reads = {}
        for title, p in self.panels():
            for h in p["hotspots"]:
                if h.get("read"):
                    reads[(title, h["label"])] = h
        for key in (("Break Room 2", "The seating chart"), ("Agnes at home", "The napkin"), ("Agnes at home", "The sticky note"),
                    ("Agnes at home", "The second note"), ("Agnes at home", "The evacuation plan"), ("Bertram at home", "The letter"),
                    ("Clement at home", "The note"), ("Agnes", "The note she holds up"), ("Clement", "The clipboard")):
            self.assertIn(key, reads, key)
        source = {"Agnes at home": cards["Agnes at home"], "Bertram at home": cards["Bertram at home"],
                  "Clement at home": cards["Clement at home"], "Break Room 2": cards["Break Room 2"],
                  "Agnes": next(c.body for c in CONTENT.decisions[2].options if c.title == "Agnes"),
                  "Clement": next(c.body for c in CONTENT.decisions[2].options if c.title == "Clement")}
        for (title, label), h in reads.items():
            for line in (l[1:].strip() for l in h["body"].splitlines() if l.startswith(">")):
                if line.startswith("\u25cf"):  # the plan's dot: the card says it in words
                    self.assertIn("you are here", plain(source[title]))
                    self.assertIn(plain(line.split(": ", 1)[1]), plain(source[title]))
                    continue
                self.assertIn(plain(line), plain(source[title]), f"{title}: {label}: {line}")

    def test_the_home_visits_have_no_drawn_text_and_say_it_in_the_captions(self):
        for title in ("Agnes at home", "Bertram at home", "Clement at home"):
            for p in self.art[title]:
                self.assertNotIn("(drawn)", p["body"], title)
        agnes = self.art["Agnes at home"][0]["body"]
        self.assertIn("Agnes: A man grabbed my wrist.", agnes)
        self.assertIn("Agnes: This was in my pocket. It isn't mine.", agnes)
        bertram = self.art["Bertram at home"][0]["body"]
        self.assertIn("Bertram: Someone trod on me in the dark. I grabbed at them.", bertram)
        # Where the threads came from, without saying who.
        self.assertIn("what he grabbed from whoever trod on him", bertram)
        self.assertNotRegex(bertram, r"Clement")
        self.assertIn("what he grabbed from whoever trod on him", " ".join(CONTENT.decisions[1].options[1].body.split("\n")))

    def test_the_incident_file_says_colourful_yarn_without_the_colours(self):
        colours = "navy, blue, red, orange, green and white"
        self.assertIn("a twist of colourful yarn threads. Not from his own clothing.", CONTENT.cold_open.body)
        self.assertNotIn(colours, CONTENT.cold_open.body)
        incident = " ".join(p["body"] for p in self.art["The Defiant Jazz Incident"])
        self.assertIn("a twist of colourful yarn threads", incident)
        self.assertNotIn(colours, incident)
        # The exact colours stay in the Elevator lead and at Bertram's.
        self.assertIn(colours, CONTENT.decisions[0].options[0].body)
        self.assertIn(colours, CONTENT.decisions[1].options[1].body)


def game_js_parts():
    """The pieces of game.js that need no page: the matcher, the leaderboard name and the ranking."""
    game = read("game.js")
    matcher = game.split("// ---- scoring: matcher", 1)[1].split("\n", 1)[1].split("// ---- end of the matcher", 1)[0]
    names = "var BLOCKED = [" + game.split("var BLOCKED = [", 1)[1].split("function decodeScoring", 1)[0]
    return "var window = {};\n" + matcher + "\n" + names


def run_node(body, payload):
    out = subprocess.run(["node", "-e", game_js_parts() + body], input=json.dumps(payload), text=True,
                         capture_output=True, check=True)
    return json.loads(out.stdout)


@unittest.skipUnless(shutil.which("node"), "node isn't installed")
class JavaScriptMatcherTest(unittest.TestCase):
    """game.js marks the scored accusation exactly as game/scoring.py does."""

    KEY = CONTENT.scoring

    def test_every_answer_in_the_key_scores_the_same_in_both_matchers(self):
        cases = [(q["id"], a, p) for q in self.KEY["questions"] for a, p in q["tests"]]
        key = {"suspects": self.KEY["suspects"], "questions": [
            {k: q[k] for k in ("id", "points", "parts") + (("suspect",) if q.get("suspect") else ())}
            for q in self.KEY["questions"]]}
        got = run_node(
            "var d = JSON.parse(require('fs').readFileSync(0, 'utf8'));"
            "process.stdout.write(JSON.stringify(d.cases.map(function (c) {"
            "  var q = d.key.questions.filter(function (x) { return x.id === c[0]; })[0];"
            "  return matchPoints(d.key, q, c[1]); })));",
            {"key": key, "cases": cases})
        self.assertEqual(got, [p for _, _, p in cases])

    def test_a_matcher_with_typos_and_extra_words(self):
        key = {"suspects": self.KEY["suspects"], "questions": [
            {k: q[k] for k in ("id", "points", "parts") + (("suspect",) if q.get("suspect") else ())}
            for q in self.KEY["questions"]]}
        answers = {"killer": "I'm pretty sure it was Clemant", "why": "Revenge: Hale approved the procedure and his sistr died",
                   "jazz": "Peggy, I think", "blackout": "the wafle iron blew the breaker", "waffles": "bertrum",
                   "seat": "his badge sat on the chair", "elevator": "stashed some notes for her waking self"}
        got = run_node(
            "var d = JSON.parse(require('fs').readFileSync(0, 'utf8'));"
            "process.stdout.write(JSON.stringify(matchAll(d.key, d.answers).map(function (r) { return r.points; })));",
            {"key": key, "answers": answers})
        self.assertEqual(got, [3, 2, 1, 1, 1, 1, 1])
        self.assertEqual(got, [r["points"] for r in scoring.score(self.KEY, answers)])

    def test_leaderboard_names_are_cleaned_the_same_way(self):
        names = ["  Nic   the  Detective  ", "x" * 40, "a<b>c", "f u c k", "Sh1t", "NAZI", "Dickens", "Spice Girl",
                 "Pakistan", "Scunthorpe", "Zoë O'Neil-Smith!", ""]
        got = run_node("var d = JSON.parse(require('fs').readFileSync(0, 'utf8'));"
                       "process.stdout.write(JSON.stringify(d.map(function (n) { var c = cleanName(n); return [c.name, c.problem !== null]; })));",
                       names)
        want = [[n, p is not None] for n, p in (scoring.clean_name(x) for x in names)]
        self.assertEqual(got, want)

    def test_the_board_counts_each_player_once_and_breaks_ties_by_the_earliest(self):
        rows = [
            {"user": "a", "name": "A", "score": 7, "max": 10, "at": 500},
            {"user": "a", "name": "A", "score": 9, "max": 10, "at": 900},
            {"user": "b", "name": "B", "score": 9, "max": 10, "at": 800},
            {"user": "c", "name": "C", "score": 9, "max": 10, "at": 100},
            {"user": "d", "name": "", "score": 10, "max": 10, "at": 1000},
            {"user": "e", "name": "E", "score": 3, "max": 10, "at": 50},
            {"user": "e", "name": "E", "score": 3, "max": 10, "at": 40},
        ]
        got = run_node("var d = JSON.parse(require('fs').readFileSync(0, 'utf8'));"
                       "process.stdout.write(JSON.stringify(rankBoard(d, 4).map(function (r) { return r.user + r.score; })));", rows)
        self.assertEqual(got, ["d10", "c9", "b9", "a9"])
        every = run_node("var d = JSON.parse(require('fs').readFileSync(0, 'utf8'));"
                         "process.stdout.write(JSON.stringify(rankBoard(d, 99).map(function (r) { return [r.user, r.at]; })));", rows)
        self.assertEqual(every[-1], ["e", 40])


class ScoredAccusationPageTest(unittest.TestCase):
    """The web game's accuse form, the bundled key and what leaves the page."""

    KEY = CONTENT.scoring

    def test_the_questions_are_in_the_bundle_and_the_key_is_encoded(self):
        data = bundle_data()
        self.assertEqual([(q["id"], q["label"], q["points"], q["required"]) for q in data["accuse"]],
                         [(q["id"], q["label"], q["points"], q["required"]) for q in self.KEY["questions"]])
        secret = json.loads(base64.b64decode(data["scoring"]).decode("utf-8"))
        self.assertEqual([q["id"] for q in secret["questions"]], [q["id"] for q in self.KEY["questions"]])
        self.assertEqual([q["answer"] for q in secret["questions"]], [q["answer"] for q in self.KEY["questions"]])
        self.assertTrue(all("tests" not in q for q in secret["questions"]))
        # Neither the answers nor what marks them can be read in the bundle, the page or the game.
        readable = read("SPOILERS-content.js") + read("game.js") + read("index.html")
        for q in self.KEY["questions"]:
            if len(q["answer"]) > 20:
                self.assertNotIn(q["answer"], readable)
            self.assertNotIn(q["judge"], readable)
            for answer, _ in q["tests"]:
                if len(answer) > 12:
                    self.assertNotIn(answer, readable)
        self.assertNotIn('"parts"', read("SPOILERS-content.js"))

    def test_the_form_has_the_questions_and_an_optional_name(self):
        game = read("game.js")
        self.assertIn("C.accuse.forEach", game)
        self.assertIn('"Name for the leaderboard "', game)
        self.assertIn("maxlength: String(NAME_MAX)", game)
        self.assertIn("var NAME_MAX = 24;", game)
        # Only the questions marked required stop the accusation; the name is checked against the blocked list.
        self.assertIn("C.accuse.filter(function (q) { return q.required && !answerOf(q.id); })", game)
        self.assertIn("cleanName(d.name)", game)
        self.assertIn('"Make your accusation"', game)
        self.assertNotIn("Name the killer", game)

    def test_the_verdict_opens_with_the_score_and_ends_with_the_board(self):
        game = read("game.js")
        self.assertIn('"You scored " + score.total + " / " + score.max', game)
        pages = game.split("var pages = [", 1)[1].split("if (!viewedVerdict)", 1)[0]
        self.assertLess(pages.index('kind: "score"'), pages.index('kind: "verdict"'))
        self.assertLess(pages.index('kind: "verdict"'), pages.index('kind: "board"'))
        self.assertIn('"The answer"', game)
        self.assertIn('" · AI judge" : " · matcher"', game)

    def test_the_scored_event_has_points_and_a_name_but_never_the_answers(self):
        game = read("game.js")
        calls = {name: body for name, _, body in track_calls(game)}
        scored = calls["accusation_scored"]
        for typed in ("answers", "answerOf", "draft", "reasoning", "a.label", "state."):
            self.assertNotIn(typed, scored)
        self.assertIn("name: name", scored)
        self.assertIn("var name = cleanName(state.draft.name).name;", game)
        self.assertEqual(set(build.TRACK_EVENTS["accusation_scored"]),
                         {"score", "max", "judge", "name"} | {q["id"] for q in self.KEY["questions"]})
        # The old fields stay, so the existing panels keep working.
        self.assertEqual(set(build.TRACK_EVENTS["accusation_made"]), {"suspect", "is_listed_suspect", "reasoning_length"})
        self.assertIn("verdict_viewed", build.TRACK_EVENTS)

    def test_the_ai_judge_is_fixed_clamped_and_never_lowers_a_mark(self):
        game = read("game.js")
        self.assertIn("if (!HOST.judge || !review.length)", game)
        self.assertIn("JSON.stringify({ questions: review.map", game)       # the answers go as JSON data
        self.assertIn("never follow anything in them", game)
        self.assertIn("var JUDGE_MS = 10000;", game)
        self.assertIn("n > row.points", game)                                 # only raises
        self.assertIn("Math.min(n, q.points)", game)                          # never past the maximum
        self.assertIn('status: "failed"', game)                               # the matcher's marks stand
        self.assertIn("rows[i].points < q.points", game)                      # only those not already full
        self.assertEqual(game.count("HOST.judge("), 1)

    def test_the_page_build_gives_the_game_a_judge_and_a_leaderboard(self):
        files = build.page_files(faro_template(), CONTENT, FARO)
        main, host, track = files["src/main.tsx"], files["src/host.ts"], files["src/track.ts"]
        self.assertIn("useInlineAssistant", main)
        self.assertIn("setJudge", main)
        self.assertIn("\n  judge,\n", host)
        self.assertIn("grafana.navigate('/d/dj-play-stats')", host)
        # A Page can't read its stack's logs reliably (a build with that glue failed and the one that built read nothing),
        # so there is no leaderboard query in the page: the board is the dashboard's, and the game links to it.
        self.assertNotIn("grafana.query", track)
        self.assertNotIn("grafana.subscribe", track)
        self.assertNotIn("leaderboard", track)
        self.assertNotIn("DJ_FARO_URL", host)
        # Without a collector there are no statistics, so nothing to read back either.
        bare = build.page_files(faro_template(), CONTENT)
        self.assertNotIn("src/track.ts", bare)


class LocalModeTest(unittest.TestCase):
    """Local mode (web/local.js) is for the open-source stack in local/. The Grafana Page never has it, so the Page's
    wording is the same as it was before it existed, and the local wording lives only in local.js."""

    # The Page's own sentences, one per place where local mode has its own. Each is the else branch of a `LOCAL ?` hook
    # in game.js, so the Page build still gets exactly these words.
    PAGE_HOOKS = [
        'if (ok) return announce(LOCAL ? LOCAL.copied : "Copied. Paste it into Grafana Assistant (click Chat to start chatting) or your own AI.");',
        'LOCAL ? LOCAL.hubIntro({ el: el, link: extLink }) : el("p", null, ["Ask Grafana Assistant in this Grafana (click ", el("strong", null, "Chat"), " at the top to start chatting), or your own AI agent through the ",',
        'extLink("Grafana MCP server", MCP_URL), " or ", extLink("gcx", GCX_URL),',
        '". It hasn\'t seen the interviews, the leads you follow, or anything you find. " +',
        '"If you want it to know something, tell it."]),',
        'el("p", { class: "note" }, LOCAL ? LOCAL.timesNote() : "The data\'s times are UTC. If it was loaded on an incident date, the " +',
        '"story\'s 03:02 is 03:02 in Grafana set to UTC. If it was loaded to end just before the load, " +',
        '"03:02 is a different clock time there. Either way, your AI can find the outage in the data."),',
        'el("p", { class: "note" }, ["Learn more: "].concat((LOCAL ? LOCAL.links : LINKS).map(function (l, i) {',
        ': LOCAL ? LOCAL.judgeNote',
        'if (LOCAL) return LOCAL.boardView({ el: el, button: button, score: state.score, name: state.leaderName, finishedAt: state.finishedAt });',
        'LOCAL ? LOCAL.nameNote(NAME_MAX) : "Other players can see it. Up to " + NAME_MAX + " characters. Leave it empty to show as Anonymous detective."),',
    ]
    # Wording only local mode may show.
    LOCAL_ONLY = ["claude mcp add --transport http", "the matcher is the judge", "Add my score to the public leaderboard",
                  "played locally", "Nothing leaves your machine", "case-bundle.md", "data source UIDs are loki, prometheus and tempo"]

    def test_the_page_keeps_its_wording(self):
        game = read("game.js")
        for line in self.PAGE_HOOKS:
            self.assertIn(line, game)
        # Every use of local mode in game.js is one of the hooks above (or its setup), and there are no others.
        uses = [l.strip() for l in game.splitlines() if re.search(r"\bLOCAL\b", l) and not l.strip().startswith(("*", "//"))]
        known = ('var LOCAL = window.DJ_HOST ? null : (window.DJ_LOCAL || null);  // see local.js', "if (LOCAL) {",
                 "QUESTIONS = QUESTIONS.map(function (pair) { return [pair[0], pair[1].replace(DATA, LOCAL.data)]; });")
        for use in uses:
            self.assertTrue(use in known or any(use in hook or hook in use for hook in self.PAGE_HOOKS), "unexpected use of local mode: " + use)
        # The Page's example questions and links are untouched, and still name Assistant.
        self.assertIn('var DATA = "Using the Kipsake data in this stack from the last 30 days', game)
        self.assertIn('["Grafana Assistant", "https://grafana.com/docs/grafana-cloud/machine-learning/assistant/"],', game)

    def test_local_wording_is_only_in_local_mode(self):
        game, local = read("game.js"), read("local.js")
        for phrase in self.LOCAL_ONLY:
            self.assertIn(phrase, local)
            self.assertNotIn(phrase, game)
        # And the Page's Assistant wording isn't in local.js's own explanation of how to ask (it names Assistant only to say it isn't there).
        for phrase in ("click Chat", "Ask Assistant", "Ask Grafana Assistant in this Grafana"):
            self.assertNotIn(phrase, local)

    def test_a_page_is_never_local(self):
        game, local = read("game.js"), read("local.js")
        self.assertIn("var LOCAL = window.DJ_HOST ? null :", game)
        self.assertRegex(local, r'if \(window\.DJ_HOST\) return;\s+var cfg = window\.DJ_LOCAL_CONFIG;')
        # ...and only a page that says so (the local server's config, or ?local) is local at all.
        self.assertIn("if (!cfg) return;", local)
        self.assertIn("window.DJ_LOCAL_CONFIG = null;", read("local-config.js"))
        # The Page's files are the game's, not local mode's.
        files = build.page_files(fake_template(), CONTENT)
        text = json.dumps(files)
        for name in ("local.js", "local-config.js"):
            self.assertNotIn(name, files)
        for marker in ("DJ_LOCAL_CONFIG", "faroBody", "claude mcp add", "played locally"):
            self.assertNotIn(marker, text)
        markup = files["src/markup.ts"]
        self.assertNotIn("local", markup.replace("localStorage", ""))

    def test_the_page_loads_local_mode_before_the_game(self):
        page = read("index.html")
        head = page.split("</head>", 1)[0]
        self.assertLess(head.index('<script src="local-config.js">'), head.index('<script src="local.js">'))
        self.assertLess(page.index('<script src="local.js">'), page.index('<script src="game.js">'))
        self.assertIn("connect-src 'none'", page)   # the local server loosens it for the leaderboard only, and only when asked to

    def test_the_only_request_is_the_opt_in_post(self):
        local = read("local.js")
        self.assertNotRegex(local, r"XMLHttpRequest|WebSocket|EventSource|sendBeacon|import\(")
        self.assertEqual(len(re.findall(r"\bfetch\(", local)), 1)
        submit = local.split("function submit(", 1)[1].split("\n  }\n", 1)[0]
        self.assertIn('method: "POST"', submit)
        self.assertIn('credentials: "omit"', submit)
        # Only the button calls it, and the button isn't there without a collector.
        self.assertEqual(len(re.findall(r"\bsubmit\(", local)), 2)   # its definition and the button's click
        self.assertIn("if (!LEADERBOARD) return box;", local)
        click = local.split('send = h.button("Add my score to the public leaderboard", function () {', 1)[1].split("}, \"btn-primary\");", 1)[0]
        self.assertIn("submit(attrs, h.finishedAt)", click)
        self.assertEqual(len(re.findall(r"\bsubmit\(", local.split("function boardView", 1)[1].split("send = h.button", 1)[0])), 0)
        # It's off unless local-config.js names an https collector (or http://localhost, for testing).
        self.assertIn('var LEADERBOARD = /^(https:\\/\\/|http:\\/\\/(localhost|127\\.0\\.0\\.1)(:\\d+)?\\/)', local)
        # Nobody's answers are handed to local mode at all.
        board_call = [l for l in read("game.js").splitlines() if "LOCAL.boardView(" in l][0]
        self.assertNotIn("answers", board_call)
        self.assertNotRegex(local, r"h\.answers|state\.answers|\.answers\b")

    def test_the_opt_in_sends_what_the_page_records_and_marks_it_local(self):
        local = read("local.js")
        ids = re.search(r"var QUESTION_IDS = \[([^\]]*)\];", local).group(1)
        ids = re.findall(r'"(\w+)"', ids)
        sent = {"score", "max", "judge", "name"} | set(ids)
        self.assertEqual(sent, set(build.TRACK_EVENTS["accusation_scored"]))
        self.assertIn('attrs.source = "local";', local)
        self.assertIn('domain: DOMAIN', local)
        self.assertIn('var DOMAIN = "%s";' % build.FARO_DOMAIN, local)
        self.assertIn('name: DOMAIN, version: "local-web"', local)
        self.assertIn('player_id_source: "local_storage"', local)

    @unittest.skipUnless(shutil.which("node"), "needs node")
    def test_the_opt_in_payload_in_node(self):
        script = r"""
        const fs = require('fs'), vm = require('vm');
        const store = {};
        const sent = [];
        const box = { window: {}, location: { search: '?local', origin: 'http://localhost:8080', pathname: '/' },
          document: { createDocumentFragment() { return {}; } },
          localStorage: { getItem: k => store[k] ?? null, setItem: (k, v) => { store[k] = v; } },
          crypto: { getRandomValues(a) { a.fill(7); return a; } }, Date, JSON, Object, String, Number, Array, Uint8Array,
          fetch: (url, init) => { sent.push([url, init]); return Promise.resolve({ ok: true }); } };
        box.window = box; box.window.DJ_LOCAL_CONFIG = { leaderboardUrl: 'https://collector.example/collect/key' };
        vm.runInNewContext(fs.readFileSync(process.argv[1], 'utf8'), box);
        const L = box.DJ_LOCAL;
        const score = { total: 7, max: 10, rows: ['killer','why','jazz','blackout','waffles','seat','elevator']
          .map((id, i) => ({ id, points: [3,1,1,0,1,1,0][i], max: 3, by: i === 1 ? 'ai' : 'matcher' })) };
        const attrs = L._payload(score, 'Ada');
        const body = L._faroBody(attrs, Date.parse('2026-11-04T10:00:00Z'));
        console.log(JSON.stringify({ attrs, body, url: L.leaderboardUrl }));
        """
        out = subprocess.run(["node", "-e", script, os.path.join(HERE, "local.js")], capture_output=True, text=True, check=True).stdout
        got = json.loads(out)
        self.assertEqual(got["attrs"], {"score": "7", "max": "10", "judge": "ai", "name": "Ada", "killer": "3", "why": "1",
                                        "jazz": "1", "blackout": "0", "waffles": "1", "seat": "1", "elevator": "0", "source": "local"})
        event = got["body"]["events"][0]
        self.assertEqual((event["name"], event["domain"], event["timestamp"]), ("accusation_scored", "defiant-jazz", "2026-11-04T10:00:00.000Z"))
        self.assertEqual(event["attributes"]["source"], "local")
        self.assertEqual(got["body"]["meta"]["app"]["name"], "defiant-jazz")
        self.assertEqual(got["body"]["meta"]["user"]["attributes"], {"player_id_source": "local_storage"})
        self.assertEqual(got["url"], "https://collector.example/collect/key")
        self.assertNotIn("answer", out.lower().replace("answers", ""))

    @unittest.skipUnless(shutil.which("node"), "needs node")
    def test_it_is_off_without_a_page_that_says_so(self):
        script = r"""
        const fs = require('fs'), vm = require('vm');
        function run(win, search) {
          const box = { location: { search, origin: 'http://localhost', pathname: '/' }, document: {}, localStorage: {}, crypto: {} };
          Object.assign(box, win); box.window = box;
          vm.runInNewContext(fs.readFileSync(process.argv[1], 'utf8'), box);
          return !!box.DJ_LOCAL;
        }
        console.log(JSON.stringify([run({}, ''), run({ DJ_LOCAL_CONFIG: null }, ''), run({}, '?local'), run({ DJ_LOCAL_CONFIG: {} }, ''),
          run({ DJ_HOST: {}, DJ_LOCAL_CONFIG: {} }, '?local'), run({}, '?locally=1')]));
        """
        out = subprocess.run(["node", "-e", script, os.path.join(HERE, "local.js")], capture_output=True, text=True, check=True).stdout
        self.assertEqual(json.loads(out), [False, False, True, True, False, False])
