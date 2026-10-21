#!/usr/bin/env python3
"""Play The Defiant Jazz Incident in the terminal.

    python3 game/play.py

SPOILERS: the story content lives in game/SPOILERS-content/. See game/README.md.
"""

import argparse
import os
import sys

try:
    import readline  # noqa: F401  (line editing and history for input())
except ImportError:
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ai as ai_module  # noqa: E402
import content  # noqa: E402
from engine import Game  # noqa: E402


def main(argv=None):
    p = argparse.ArgumentParser(description="The Defiant Jazz Incident: a text adventure "
                                            "with an AI investigator.")
    p.add_argument("--ai", choices=ai_module.KNOWN_AIS, default=os.environ.get("DJ_AI") or None,
                   help="which installed AI to use (env DJ_AI). Default: the first of claude, "
                        "codex, gemini that's installed.")
    p.add_argument("--ai-cmd", default=os.environ.get("DJ_AI_CMD"),
                   help="any headless AI command that reads a prompt on stdin and prints its "
                        "answer (env DJ_AI_CMD). Overrides --ai.")
    p.add_argument("--model", default=os.environ.get("DJ_AI_MODEL"),
                   help="model for Claude Code, Codex or Gemini CLI, for example "
                        "claude-opus-5-5 (env DJ_AI_MODEL). With --ai-cmd, put it in the command.")
    p.add_argument("--timeout", type=int, default=int(os.environ.get("DJ_AI_TIMEOUT", "900")),
                   help="seconds to wait for each AI answer (default 900)")
    p.add_argument("--no-ai", action="store_true", help="play without the AI")
    p.add_argument("--no-color", action="store_true", help="plain text output")
    p.add_argument("--log", metavar="FILE",
                   help="append a transcript of the game to FILE (it will contain spoilers)")
    args = p.parse_args(argv)

    cards = content.load()
    ai = None
    if not args.no_ai:
        try:
            ai = ai_module.from_settings(content.load_bundle(), command=args.ai_cmd,
                                         model=args.model, timeout=args.timeout, choice=args.ai)
        except ai_module.AIError as e:
            p.error(str(e))
        problem = ai.check()
        if problem:
            print(f"Note: {problem}\nYou can still play; use --no-ai to hide this.\n")
        else:
            print(f"Your AI assistant: {ai.name}.\n")

    color = (not args.no_color and sys.stdout.isatty() and not os.environ.get("NO_COLOR")
             and os.environ.get("TERM") != "dumb")
    log = open(args.log, "a", encoding="utf-8") if args.log else None
    try:
        Game(cards, ai, color=color, log=log).run()
    finally:
        if ai:
            ai.close()
        if log:
            log.close()


if __name__ == "__main__":
    main()
