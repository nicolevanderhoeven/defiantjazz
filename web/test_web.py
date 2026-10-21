"""Self-check for the web game. Spoiler-free: it compares files, never quotes the cards.

    python3 -m unittest discover -s web
"""

import base64
import json
import os
import re
import sys
import unittest

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
