"""Self-check for the game. Never calls a real AI. Contains spoilers.

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
    "Called me something, like a pet's name",
    "Clement. 'Chill out, Waffles.' He's the only one who calls me that",
    "Clement calls him 'Waffles'",
    "checked on Bertram (shoulder)",
    "Someone was screaming by the elevator",
    "survived by her brother, Clement",
    "Procedure Revision 114",
    "Port Quiet Gazette",
    "THE GOLDEN WAFFLE",
    "a single digit",
    "navy Christmas sweater",
    "a twist of five or six yarn threads",
    "cycle timer: started 03:01:47",
    "Clement killed Mr. Hale",
    "It took a human to know which question to ask",
]

REASONING = "My secret theory: the sweater threads give it away."


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
               "result": f"**Answer {len(self.calls)}.** It was Agnes.\n\n- Evidence: the cable."}
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
        self.assertIn("June, 41.", CONTENT.outside_world.body)
        self.assertEqual(CONTENT.advert.meta.get("style"), "advert")
        self.assertIn("Earn while you sleep.", CONTENT.advert.body)

    def test_bundle_has_no_human_only_text(self):
        for phrase in SENTINELS:
            self.assertNotIn(phrase, BUNDLE)
        for line in human_only_lines():
            self.assertNotIn(line, BUNDLE)

    def test_suspect_names(self):
        self.assertEqual(CONTENT.resolve_suspect("Clement"), "clement")
        self.assertEqual(CONTENT.resolve_suspect("peggy"), "agnes")
        self.assertEqual(CONTENT.resolve_suspect("Agnes."), "agnes")
        self.assertEqual(CONTENT.resolve_suspect("Waffles"), "bertram")
        self.assertIsNone(CONTENT.resolve_suspect("Mr. Hale"))


TELEMETRY = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "telemetry")


def telemetry(name):
    with open(os.path.join(TELEMETRY, name), encoding="utf-8") as f:
        return f.read()


class ClueSplitTest(unittest.TestCase):
    """Every clue against the killer has a clip half and a data half: neither source solves it alone."""

    def clips(self):
        return "\n".join(c.body for c in list(CONTENT.testimonies) + [CONTENT.outside_world]
                         + [o for d in CONTENT.decisions for o in d.options])

    def test_telemetry_never_links_the_killer(self):
        everything = "\n".join(telemetry(n) for n in ("records.log", "ambient-mic.log", "chat.log",
                                                       "system.log", "door-and-badge-events.log"))
        self.assertNotRegex(everything, r"\bJune\b")
        self.assertNotRegex(telemetry("chat.log"), r"(?i)waffles\b(?!\s+were)")
        self.assertNotRegex(everything, r"(?i)yarn|thread|napkin")
        self.assertNotRegex(telemetry("ambient-mic.log") + telemetry("records.log"), r"(?i)clement.*(sister|brother)")

    def test_telemetry_holds_the_data_halves(self):
        records = telemetry("records.log")
        self.assertIn('seat=4 position="chair by the speaker" assigned=clement', records)
        self.assertIn('employee=clement item="Christmas sweater" colours="navy, blue, red, orange, green, white"', records)
        self.assertIn("procedure-revision id=114 title", records)
        self.assertIn("approved_by=hale", records)
        mic = telemetry("ambient-mic.log")
        self.assertIn("Sorry, Waffles", mic)
        dark = [l for l in mic.splitlines() if "[screaming]" in l]
        self.assertTrue(dark)
        for line in dark:  # screaming is only ever in the dark: 03:03 to 03:05
            self.assertRegex(line, r"T03:0[345]:")
        self.assertIn("[shouting] Nobody move!", mic)

    def test_clips_hold_only_their_halves(self):
        clips = self.clips()
        for phrase in ("only C", "R. Hale", "goes by Peggy", "Who's Waffles",
                       "single block capital", "checked on Waffles", "circled", "in pen"):
            self.assertNotIn(phrase, clips)
        self.assertEqual(clips.count("Peggy"), 2)  # only his crossed-out word, and the line that says so
        self.assertNotIn("route", clips.lower())

    def test_each_lead_says_the_choice_is_final(self):
        for decision in CONTENT.decisions:
            self.assertIn("You can choose only one.", decision.prompt)
            self.assertIn("your choice is final", decision.prompt)


class FullPathTest(unittest.TestCase):
    def setUp(self):
        self.runner = FakeClaude()
        self.ai = ai.ClaudeAI(BUNDLE, runner=self.runner)
        answers = [
            "", "", "", "", "",                 # advert, cold open and three testimonies
            "ask Who killed Mr. Hale?",
            "investigate", "1",                 # Elevator car 1
            "ask What did the corridor-e mic hear?",
            "investigate", "", "2",             # Outside World handout, then Bertram at home
            "investigate", "clement",           # push Clement
            "review", "all",
            "investigate",                      # all used
            "accuse clement.", "y",
            REASONING, "", "Second paragraph.", ".",
            "", "",                             # the reveal's cards
        ]
        self.game, self.output = play(answers, self.ai)
        self.ai.close()

    def test_walks_the_whole_game(self):
        self.assertEqual([c.meta["option"] for _, c in self.game.chosen],
                         ["Elevator car 1", "Bertram at home", "Clement"])
        self.assertEqual(self.game.accused, "clement")
        self.assertIn("You're right.", self.output)
        self.assertIn("How it's solved", self.output)
        self.assertIn("all three leads used", self.output)
        self.assertIn("Answer 2.", self.output)

    def test_opening_and_separators(self):
        before_turn = self.output.split("── Your turn")[0]
        self.assertIn("I N C I D E N T", before_turn)
        self.assertIn("Your role", before_turn)
        self.assertIn("You can accuse before you've used them all.", " ".join(before_turn.split()))
        flat = " ".join(before_turn.split())
        self.assertIn("If you want it to know something, tell it.", flat)
        self.assertIn("hot cocoa", before_turn)
        self.assertLess(flat.index("KIPSAKE · ADVERT"), flat.index("Earn while you sleep."))
        self.assertLess(flat.index("Join our team of Dreamers in time for the holidays."), flat.index("What happened that night"))
        self.assertNotIn("power cut", flat)
        interviews = " ".join(before_turn.split("── Interviews", 1)[1].split())
        self.assertLess(interviews.index("First, your interviews."),
                        interviews.index("You: Agnes. Where were you"))
        for label in ("Cold open", "Interviews", "Your turn", "AI assistant",
                      "Lead 1 of 3", "Outside World handout", "Review", "The verdict"):
            self.assertIn(f"── {label} ─", self.output)
        for line in self.output.splitlines():
            self.assertLessEqual(len(line), 80)
        self.assertNotIn("\x1b[", self.output)

    def test_example_questions(self):
        before_turn, after_turn = self.output.split("── Your turn", 1)
        self.assertNotIn("Neither of you", self.output)
        flat = " ".join(after_turn.split())
        self.assertIn("You can ask anything.", flat)
        self.assertIn("ask Who killed Mr. Hale?", flat)
        evidence = "ask What happened near the elevator between 03:02 and 03:07?"
        self.assertEqual(flat.count(evidence), 1)
        self.assertLess(flat.index("Answer 1."), flat.index(evidence))

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
        before = self.output.split("You accused Clement.")[0]
        for card in CONTENT.reveal.cards:
            self.assertNotIn(card.title, before)
        for phrase in ("Clement wants Hale alone", "The human leap", "You're right."):
            self.assertNotIn(phrase, before)


class OtherPathsTest(unittest.TestCase):
    def test_early_accusation_of_agnes(self):
        game, output = play(["", "", "", "", "", "accuse peggy", "y", "She had the cable.", "", "", "", ""],
                            None)
        self.assertEqual(game.accused, "agnes")
        self.assertIn("You still have 3 leads to follow up", output)
        self.assertIn("the mistake the case is built around", output)
        self.assertNotIn("Outside World handout", output)

    def test_accused_label_has_one_full_stop(self):
        self.assertIn("You accused Clement.", game_output := play(
            ["", "", "", "", "", "accuse clement", "y", "x", ".", "", ""], None)[1])
        self.assertNotIn("Clement..", game_output)

    def test_reasoning_keeps_paragraphs_until_terminator(self):
        game, output = play(["", "", "", "", "", "accuse agnes", "y",
                             "First.", "", "Second.", "", "", "", ""], None)
        self.assertEqual(game.reasoning, "First.\n\nSecond.")
        self.assertIn("Second.", output)
        game, _ = play(["", "", "", "", "", "accuse agnes", "y", "One.", "", "Two.", " . ", "", ""],
                       None)
        self.assertEqual(game.reasoning, "One.\n\nTwo.")

    def test_hint_wraps_between_commands(self):
        output = []
        game = Game(CONTENT, None, input_fn=Script([]), write=output.append, width=60)
        game.hint()
        for line in output:
            self.assertFalse(line.rstrip().endswith("accuse"))
            self.assertLessEqual(len(line), 60)
        self.assertIn("accuse <name>", "\n".join(output))

    def test_hint_counts_leads_down_then_suggests_accuse(self):
        expected = [
            "Leads left: 3 of 3 · type investigate for the next one (a crime scene)",
            "Leads left: 2 of 3 · type investigate for the next one (a home visit)",
            "Leads left: 1 of 3 · type investigate for the next one (one last interview)",
            "Leads left: 0 of 3 · all three leads used · type accuse <name> when you're ready",
        ]
        for n, text in enumerate(expected):
            output = []
            game = Game(CONTENT, None, input_fn=Script([]), write=output.append, width=88)
            game.chosen = [None] * n
            game.hint()
            self.assertIn(text, output)
            if n == 3:
                self.assertNotIn("for the next one", "\n".join(output))

    def test_quit_and_unknown_command(self):
        game, output = play(["", "", "", "", "", "dance", "ask", "", "quit", "y"], None)
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
        play(["", "", "", "", "", "ask one?", "investigate", "2", "ask two?", "quit", "y"], the_ai)
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
        game, output = play(["", "", "", "", "", "ask hello?", "quit", "y"], the_ai)
        self.assertIn("Your AI assistant couldn't answer", output)


if __name__ == "__main__":
    unittest.main()
