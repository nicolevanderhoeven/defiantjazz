"""Choosing the AI: detection order, the no-AI message, and each AI's command line.

No spoilers here, and no real AI is ever run: `which` and the subprocess runner are stubs.
"""

import io
import os
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ai  # noqa: E402
import play  # noqa: E402

BUNDLE = "<<the case bundle>>"

CODEX_FEATURES = """\
apps                                     stable             true
shell_tool                               stable             true
unified_exec                             stable             true
web_search_cached                        deprecated         false
"""


def which_of(*installed):
    return lambda name: f"/usr/bin/{name}" if name in installed else None


class Runner:
    """Stands in for subprocess.run. Answers `codex features list` and records every other call."""

    def __init__(self):
        self.calls = []

    def __call__(self, argv, input=None, cwd=None, **kwargs):
        if argv[1:] == ["features", "list"]:
            return subprocess.CompletedProcess(argv, 0, CODEX_FEATURES, "")
        self.calls.append({"argv": argv, "input": input, "cwd": cwd,
                           "cwd_files": os.listdir(cwd)})
        return subprocess.CompletedProcess(argv, 0, "an answer\n", "")


@mock.patch.dict(os.environ, {"DJ_CLAUDE": "", "DJ_AI": "", "DJ_AI_CMD": ""})
class DetectTest(unittest.TestCase):
    def pick(self, *installed, **kwargs):
        the_ai = ai.from_settings(BUNDLE, which=which_of(*installed), runner=Runner(), **kwargs)
        if hasattr(the_ai, "workdir"):
            self.addCleanup(the_ai.close)
        return the_ai

    def test_detection_order(self):
        self.assertEqual(ai.detect(which_of("claude", "codex", "gemini")), "claude")
        self.assertEqual(ai.detect(which_of("codex", "gemini")), "codex")
        self.assertEqual(ai.detect(which_of("gemini")), "gemini")
        self.assertIsNone(ai.detect(which_of("ollama")))

    def test_picks_the_first_installed(self):
        self.assertIsInstance(self.pick("claude", "codex", "gemini"), ai.ClaudeAI)
        self.assertEqual(self.pick("codex", "gemini").argv[:2], ["codex", "exec"])
        self.assertEqual(self.pick("gemini").argv[0], "gemini")

    def test_choice_and_command_override_detection(self):
        self.assertEqual(self.pick("claude", "codex", choice="codex").argv[0], "codex")
        self.assertEqual(self.pick("claude", command="my-ai --flag").argv, ["my-ai", "--flag"])
        with mock.patch.dict(os.environ, {"DJ_CLAUDE": "/opt/claude"}):
            self.assertEqual(self.pick("codex").command, "/opt/claude")
        with self.assertRaisesRegex(ai.AIError, "Unknown AI"):
            self.pick("claude", choice="clippy")

    def test_no_ai_found(self):
        the_ai = self.pick()
        self.assertIsInstance(the_ai, ai.MissingAI)
        for text in ("No AI found", "--ai-cmd", "DJ_AI_CMD", "game/README.md"):
            self.assertIn(text, the_ai.check())
        with self.assertRaisesRegex(ai.AIError, "No AI found"):
            the_ai.ask("hello?")

    def test_play_explains_instead_of_failing(self):
        out = io.StringIO()
        with mock.patch.object(ai.shutil, "which", which_of()), \
                mock.patch.object(play.Game, "run") as run, redirect_stdout(out):
            play.main([])
        run.assert_called_once()
        self.assertIn("Note: No AI found", out.getvalue())
        self.assertIn("You can still play", out.getvalue())


@mock.patch.dict(os.environ, {"DJ_CLAUDE": "", "DJ_AI": "", "DJ_AI_CMD": ""})
class CommandLineTest(unittest.TestCase):
    def test_codex_is_read_only_with_no_tools(self):
        argv = ai.codex_argv("gpt-x", runner=Runner())
        for flags in (["-s", "read-only"], ["-c", "web_search=disabled"], ["--ephemeral"],
                      ["--ignore-user-config"], ["--disable", "shell_tool"],
                      ["--disable", "unified_exec"], ["--disable", "apps"], ["-m", "gpt-x"]):
            self.assertIn(flags, [argv[i:i + len(flags)] for i in range(len(argv))])
        # A feature this Codex doesn't list is left out: Codex refuses unknown names.
        self.assertNotIn("browser_use", argv)
        self.assertEqual(argv[-1], "-")
        self.assertNotIn("-m", ai.codex_argv(runner=Runner()))

    def test_gemini_plan_mode_and_model(self):
        self.assertEqual(ai.gemini_argv(), ["gemini", "--approval-mode", "plan"])
        self.assertEqual(ai.gemini_argv("flash")[-2:], ["-m", "flash"])

    def test_sends_only_the_prompt_bundle_and_questions_from_an_empty_dir(self):
        runner = Runner()
        the_ai = ai.from_settings(BUNDLE, which=which_of("codex"), runner=runner)
        self.addCleanup(the_ai.close)
        self.assertEqual(the_ai.ask("who?"), "an answer")
        the_ai.ask("why?")
        first, second = runner.calls
        self.assertEqual(first["cwd_files"], [])
        self.assertTrue(first["input"].startswith(ai.SYSTEM_PROMPT))
        self.assertIn(BUNDLE, first["input"])
        self.assertIn("My first question: who?", first["input"])
        self.assertIn("Your answer: an answer\n\nMy next question: why?", second["input"])


if __name__ == "__main__":
    unittest.main()
