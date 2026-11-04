"""Self-check for the web game. Spoiler-free: it compares files, never quotes the cards.

    python3 -m unittest discover -s web
"""

import base64
import json
import os
import re
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
        self.assertIn("reasoning_length: (state.draft.reasoning || \"\").trim().length", accused)
        for typed in ("a.label", "draft.other", ".other", "reasoning.value"):
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
        # accusation() maps a typed name to a suspect's key, or to "other" with the typed name only as a label.
        self.assertIn('{ key: "other", label: name }', game)

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
        for text in ("text", "name", "reasoning", "question", "answer", "solution", "killer", "login"):
            self.assertNotIn(text, [k for keys in build.TRACK_EVENTS.values() for k in keys])

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
    def test_six_panels_over_the_game_events_without_test_traffic(self):
        dash = json.loads(read("dashboard-play-statistics.json"))
        self.assertEqual(len(dash["panels"]), 6)
        self.assertEqual({v["name"] for v in dash["templating"]["list"]}, {"loki", "environment", "exclude"})
        text = json.dumps(dash)
        self.assertNotIn("0123456789", text)
        for panel in dash["panels"]:
            self.assertEqual(panel["datasource"]["uid"], "${loki}")
            for target in panel["targets"]:
                expr = target["expr"]
                self.assertIn('browser_name!="Chrome Headless"', expr)
                self.assertIn('user_attr_player_id_source="user_storage"', expr)
                self.assertIn('user_id!~"$exclude"', expr)
                self.assertIn('event_domain="defiant-jazz"', expr)
                for event in re.findall(r'event_name="([a-z_]+)"', expr):
                    self.assertIn(event, build.TRACK_EVENTS)
            self.assertEqual(len({t["refId"] for t in panel["targets"]}), len(panel["targets"]))


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
