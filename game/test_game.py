"""Self-check for the game. Never calls a real AI.

    python3 -m unittest discover -s game
"""

import json
import os
import re
import subprocess
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ai  # noqa: E402
import content  # noqa: E402
from engine import Game  # noqa: E402

CONTENT = content.load()
BUNDLE = content.load_bundle()

# Human-only text that must never reach the AI.
SENTINELS = [
    "Called me Waffles, as usual",
    "WAFFLES — ice. — C.W.",
    "Who's Waffles?",
    "He's the only one who calls me that",
    "Clement calls him 'Waffles'",
    "checked on Waffles",
    "Someone was screaming by the elevator",
    "June Whitlow",
    "Procedure Revision 114",
    "Port Quiet Gazette",
    "THE GOLDEN WAFFLE",
    "C.A.W.",
    "fringed scarf",
    "Clement Arthur Whitlow killed Mr. Hale",
    "It took a human to know which question to ask",
]

REASONING = "My secret theory: the scarf threads give it away."


def human_only_lines():
    """Every line of every card the player sees, except the cold open (which is public)."""
    cards = list(CONTENT.testimonies) + [CONTENT.outside_world]
    for decision in CONTENT.decisions:
        cards += decision.options
    cards += CONTENT.reveal.cards
    lines = set()
    for card in cards:
        for line in card.body.splitlines():
            text = re.sub(r"^\[|\]$|^> |^- |\*\*|\*|~~", "", line.strip())
            text = re.sub(r"^[A-Z][A-Za-z. ]{0,24}: ", "", text).strip()
            if len(text) >= 25:
                lines.add(text)
    return lines


class FakeClaude:
    """Stands in for subprocess.run. Records each call and answers like `claude -p`."""

    def __init__(self):
        self.calls = []

    def __call__(self, argv, input, cwd, **kwargs):
        self.calls.append({"argv": argv, "input": input, "cwd_files": os.listdir(cwd), "cwd": cwd})
        out = {"type": "result", "is_error": False, "session_id": "sess-123",
               "result": f"**Answer {len(self.calls)}.** It was Agnes K.\n\n- Evidence: the cable."}
        return subprocess.CompletedProcess(argv, 0, json.dumps(out), "")


class Script:
    def __init__(self, answers):
        self.answers = list(answers)
        self.prompts = []

    def __call__(self, prompt):
        self.prompts.append(prompt)
        if not self.answers:
            raise EOFError
        return self.answers.pop(0)


def play(answers, the_ai):
    output = []
    game = Game(CONTENT, the_ai, input_fn=Script(answers), write=output.append, width=80)
    game.run()
    return game, "\n".join(output)


class ContentTest(unittest.TestCase):
    def test_everything_loads(self):
        self.assertEqual([t.title.split(" ·")[0] for t in CONTENT.testimonies], ["T-A", "T-B", "T-C"])
        self.assertEqual(len(CONTENT.decisions), 3)
        for decision in CONTENT.decisions:
            self.assertEqual(len(decision.options), 3)
            self.assertTrue(decision.prompt)
            for card in decision.options:
                self.assertTrue(card.body)
        self.assertIn("June Whitlow", CONTENT.outside_world.body)

    def test_bundle_has_no_human_only_text(self):
        for phrase in SENTINELS:
            self.assertNotIn(phrase, BUNDLE)
        for line in human_only_lines():
            self.assertNotIn(line, BUNDLE)

    def test_suspect_names(self):
        self.assertEqual(content.resolve_suspect("Clement W."), "clement")
        self.assertEqual(content.resolve_suspect("peggy"), "agnes")
        self.assertEqual(content.resolve_suspect("Mr. Lindqvist"), "bertram")
        self.assertIsNone(content.resolve_suspect("Fern"))


class FullPathTest(unittest.TestCase):
    def setUp(self):
        self.runner = FakeClaude()
        self.ai = ai.ClaudeAI(BUNDLE, runner=self.runner)
        answers = [
            "", "", "", "",                     # cold open and three testimonies
            "ask Who killed Mr. Hale?",
            "investigate", "1",                 # Elevator car 1
            "ask What did the corridor-e mic hear?",
            "investigate", "", "2",             # Outside World handout, then Mr. Lindqvist
            "investigate", "clement",           # push Clement
            "review", "all",
            "investigate",                      # all used
            "accuse clement w.", "y",
            REASONING, "",
            "", "",                             # the reveal's cards
        ]
        self.game, self.output = play(answers, self.ai)
        self.ai.close()

    def test_walks_the_whole_game(self):
        self.assertEqual([c.meta["option"] for _, c in self.game.chosen],
                         ["Elevator car 1", "Mr. Lindqvist", "Clement"])
        self.assertEqual(self.game.accused, "clement")
        self.assertIn("You're right.", self.output)
        self.assertIn("How it's solved", self.output)
        self.assertIn("all three used", self.output)
        self.assertIn("Answer 2.", self.output)

    def test_ai_is_headless_isolated_and_resumed(self):
        first, second = self.runner.calls
        for call in (first, second):
            argv = call["argv"]
            self.assertEqual(argv[0], "claude")
            self.assertIn("-p", argv)
            self.assertEqual(argv[argv.index("--tools") + 1], "")
            self.assertEqual(argv[argv.index("--setting-sources") + 1], "")
            self.assertIn("--strict-mcp-config", argv)
            self.assertEqual(call["cwd_files"], [])
        self.assertNotIn("--resume", first["argv"])
        self.assertIn(BUNDLE, first["input"])
        self.assertTrue(first["input"].endswith("Who killed Mr. Hale?"))
        self.assertEqual(second["argv"][second["argv"].index("--resume") + 1], "sess-123")
        self.assertEqual(second["input"], "What did the corridor-e mic hear?")
        self.assertFalse(os.path.exists(first["cwd"]))  # removed by close()

    def test_ai_never_sees_human_only_text(self):
        sent = "\n".join(c["input"] + "\n" + " ".join(c["argv"]) for c in self.runner.calls)
        for phrase in SENTINELS + [REASONING]:
            self.assertNotIn(phrase, sent)
        for line in human_only_lines():
            self.assertNotIn(line, sent)

    def test_reveal_only_after_accusing(self):
        before = self.output.split("You accused Clement W.")[0]
        for card in CONTENT.reveal.cards:
            self.assertNotIn(card.title, before)
        for phrase in ("Clement wants Hale alone", "The human leap", "You're right."):
            self.assertNotIn(phrase, before)


class OtherPathsTest(unittest.TestCase):
    def test_early_accusation_of_agnes(self):
        game, output = play(["", "", "", "", "accuse peggy", "y", "She had the cable.", "", "", ""],
                            None)
        self.assertEqual(game.accused, "agnes")
        self.assertIn("You still have 3 decisions left", output)
        self.assertIn("the mistake the case is built around", output)
        self.assertNotIn("Outside World handout", output)

    def test_quit_and_unknown_command(self):
        game, output = play(["", "", "", "", "dance", "ask", "", "quit", "y"], None)
        self.assertIsNone(game.accused)
        self.assertIn("I don't know \"dance\"", output)
        self.assertNotIn("You're right.", output)

    def test_command_ai_sends_history(self):
        calls = []

        def runner(argv, input, cwd, **kwargs):
            calls.append(input)
            return subprocess.CompletedProcess(argv, 0, f"answer {len(calls)}\n", "")

        the_ai = ai.CommandAI(BUNDLE, "my-ai --flag", runner=runner)
        self.addCleanup(the_ai.close)
        play(["", "", "", "", "ask one?", "investigate", "2", "ask two?", "quit", "y"], the_ai)
        self.assertEqual(len(calls), 2)
        self.assertIn(BUNDLE, calls[1])
        self.assertIn("My first question: one?\n\nYour answer: answer 1\n\nMy next question: two?",
                      calls[1])
        for phrase in SENTINELS:
            self.assertNotIn(phrase, calls[1])
        for line in human_only_lines():
            self.assertNotIn(line, calls[1])


class ErrorTest(unittest.TestCase):
    def test_missing_claude(self):
        the_ai = ai.ClaudeAI(BUNDLE, command="no-such-claude-binary")
        self.addCleanup(the_ai.close)
        self.assertIn("isn't on your PATH", the_ai.check())
        with self.assertRaisesRegex(ai.AIError, "command not found"):
            the_ai.ask("hello?")

    def test_not_logged_in(self):
        def runner(argv, **kwargs):
            out = {"type": "result", "is_error": True, "result": "Not logged in · Please run /login"}
            return subprocess.CompletedProcess(argv, 1, json.dumps(out), "")

        the_ai = ai.ClaudeAI(BUNDLE, runner=runner)
        self.addCleanup(the_ai.close)
        with self.assertRaisesRegex(ai.AIError, "logged in"):
            the_ai.ask("hello?")
        game, output = play(["", "", "", "", "ask hello?", "quit", "y"], the_ai)
        self.assertIn("The AI couldn't answer", output)


if __name__ == "__main__":
    unittest.main()
