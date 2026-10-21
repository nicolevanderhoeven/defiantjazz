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
        urls = re.findall(r"\"(https?://[^\"]+)\"", game)
        self.assertTrue(urls)
        for url in urls:
            self.assertIn(f'"{url}"]', game, f"{url} should be in LINKS")
        self.assertIn('target: "_blank", rel: "noopener noreferrer"', game)


class SandboxTest(unittest.TestCase):
    """A Grafana Page runs the game in a frame without forms, modals or localStorage."""

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
        self.assertIn("openAssistant({ prompt })", self.files["src/host.ts"])

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
