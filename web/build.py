#!/usr/bin/env python3
"""Bundle the game's story cards into web/SPOILERS-content.js for the web version.

    python3 web/build.py           # write web/SPOILERS-content.js
    python3 web/build.py --check   # exit 1 if it's out of date

SPOILERS: the bundle holds every card in game/SPOILERS-content/, including the
reveal. The reveal is base64-encoded so a glance at the file doesn't spoil it,
and the page only decodes it after the player accuses and confirms.

The cards are parsed by game/content.py, the same loader the terminal game uses,
so game/SPOILERS-content/ stays the one source of truth. Run this after editing
any card there.
"""

import argparse
import base64
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "SPOILERS-content.js")
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "game"))

import content  # noqa: E402
import engine  # noqa: E402

HEADER = """\
// SPOILERS: generated from game/SPOILERS-content/ by web/build.py. Don't edit by hand.
// The reveal is base64-encoded JSON; the page decodes it only after the player accuses.
"""


def _card(card):
    return {"title": card.title, "body": card.body, "meta": card.meta}


def data(cards=None):
    """Everything the web page needs, as plain JSON-ready values."""
    cards = cards or content.load()
    reveal = json.dumps([_card(c) for c in cards.reveal.cards], ensure_ascii=False)
    return {
        "banner": engine.BANNER,
        "suspects": content.SUSPECTS,
        "leadKinds": engine.LEAD_KIND,
        "leadShort": engine.DECISION_SHORT,
        "coldOpen": _card(cards.cold_open),
        "testimonyIntro": cards.testimony_intro,
        "testimonies": [_card(c) for c in cards.testimonies],
        "outsideWorld": _card(cards.outside_world),
        "decisions": [
            {"title": d.title, "prompt": d.prompt, "options": [_card(c) for c in d.options]}
            for d in cards.decisions
        ],
        "aliases": cards.aliases,
        "reveal": base64.b64encode(reveal.encode("utf-8")).decode("ascii"),
    }


def render(cards=None):
    body = json.dumps(data(cards), ensure_ascii=False, indent=1)
    return f"{HEADER}window.DJ_CONTENT = {body};\n"


def main(argv=None):
    p = argparse.ArgumentParser(description="Bundle game/SPOILERS-content/ for the web game.")
    p.add_argument("--check", action="store_true", help="exit 1 if the bundle is out of date")
    args = p.parse_args(argv)
    text = render()
    if args.check:
        try:
            with open(OUT_PATH, encoding="utf-8") as f:
                current = f.read()
        except FileNotFoundError:
            current = None
        if current != text:
            sys.exit(f"{os.path.relpath(OUT_PATH)} is out of date: run python3 web/build.py")
        print(f"{os.path.relpath(OUT_PATH)} is up to date.")
        return
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Wrote {os.path.relpath(OUT_PATH)}.")


if __name__ == "__main__":
    main()
