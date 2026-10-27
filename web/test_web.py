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
            self.assertIn(f'"{url}"]', game, f"{url} should be in LINKS")
        self.assertIn('target: "_blank", rel: "noopener noreferrer"', game)

    def test_example_questions(self):
        game = read("game.js")
        block = game.split("var DATA = ", 1)[1].split("var LINKS", 1)[0]
        hints = re.findall(r'\[\"([^"]+)\", DATA \+', block)
        self.assertEqual(hints, ["Ask for a verdict", "Build a page", "Make a graph"])
        self.assertIn('var DATA = "Using the Kipsake data in this stack, ";', game)
        self.assertIn("Who killed Mr. Hale?", block.split("Build a page")[0])
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
        for hook in ("HOST.storage", "HOST.onTheme", "HOST.askAssistant"):
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
