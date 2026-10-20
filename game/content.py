"""Load the game's text cards from game/SPOILERS-content/.

Card format (Markdown, one file per section of the game):

    <!-- comments are ignored -->
    # File title
    key: value            # optional file metadata, right under the title

    ## Card title
    key: value            # optional card metadata, right under the heading
                          # (keys are lowercase, so "Agnes: ..." is dialogue)
    Body lines...

Body lines are shown as written. "[...]" lines are descriptions of what's on
screen, "> ..." lines are text shown on screen, and "Name: ..." lines are
spoken.
"""

import json
import os
import re
from dataclasses import dataclass, field

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(HERE, "SPOILERS-content")
BUNDLE_PATH = os.path.join(HERE, "ai-evidence", "case-bundle.md")

SUSPECTS = {
    "agnes": "Agnes K.",
    "bertram": "Bertram L.",
    "clement": "Clement W.",
}

_META = re.compile(r"^([a-z][a-z_]*):\s*(.*)$")
_COMMENT = re.compile(r"<!--.*?-->", re.S)


class ContentError(Exception):
    pass


@dataclass
class Card:
    title: str
    body: str
    meta: dict = field(default_factory=dict)


@dataclass
class Section:
    title: str
    meta: dict
    cards: list


@dataclass
class Decision:
    title: str
    prompt: str
    options: list  # of Card, each with "option" and "note" meta


@dataclass
class Content:
    cold_open: Card
    testimonies: list
    outside_world: Card
    decisions: list
    reveal: Section
    aliases: dict  # normalized name -> suspect key

    def resolve_suspect(self, text):
        """Return 'agnes', 'bertram' or 'clement' for a recognisable name, else None."""
        return self.aliases.get(normalize_name(text))


def _take_meta(lines):
    meta = {}
    while lines and _META.match(lines[0]):
        key, value = _META.match(lines.pop(0)).groups()
        meta[key] = value.strip()
    return meta


def parse_section(text, source="<text>"):
    lines = _COMMENT.sub("", text).splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines or not lines[0].startswith("# "):
        raise ContentError(f"{source}: must start with a '# ' title")
    title = lines.pop(0)[2:].strip()
    meta = _take_meta(lines)
    cards = []
    current = None
    for line in lines:
        if line.startswith("## "):
            current = [line[3:].strip(), []]
            cards.append(current)
        elif current is not None:
            current[1].append(line)
        elif line.strip():
            raise ContentError(f"{source}: text before the first '## ' card: {line!r}")
    parsed = []
    for card_title, body in cards:
        card_meta = _take_meta(body)
        parsed.append(Card(card_title, "\n".join(body).strip(), card_meta))
    if not parsed:
        raise ContentError(f"{source}: no cards")
    return Section(title, meta, parsed)


def _read(name, content_dir):
    path = os.path.join(content_dir, name)
    with open(path, encoding="utf-8") as f:
        return parse_section(f.read(), path)


def _decision(section, source):
    if "prompt" not in section.meta:
        raise ContentError(f"{source}: missing 'prompt:'")
    if len(section.cards) != 3:
        raise ContentError(f"{source}: a decision needs exactly three options")
    for card in section.cards:
        if "option" not in card.meta:
            raise ContentError(f"{source}: card {card.title!r} is missing 'option:'")
    return Decision(section.title, section.meta["prompt"], section.cards)


def _aliases(content_dir):
    # Names a player might use for a suspect, including their waking names.
    path = os.path.join(content_dir, "suspect-names.json")
    with open(path, encoding="utf-8") as f:
        names = json.load(f)
    if set(names) != set(SUSPECTS):
        raise ContentError(f"{path}: expected names for {', '.join(SUSPECTS)}")
    return {normalize_name(name): key for key, group in names.items() for name in group}


def load(content_dir=CONTENT_DIR):
    testimonies = _read("testimonies.md", content_dir).cards
    if len(testimonies) != 3:
        raise ContentError("testimonies.md: expected three testimonies")
    decisions = [
        _decision(_read(name, content_dir), name)
        for name in ("decision-1-scene.md", "decision-2-outside-world.md", "decision-3-push.md")
    ]
    reveal = _read("SPOILERS-reveal.md", content_dir)
    for key in list(SUSPECTS) + ["other", "all"]:
        if not any(c.meta.get("for") == key for c in reveal.cards):
            raise ContentError(f"SPOILERS-reveal.md: no card with 'for: {key}'")
    return Content(
        cold_open=_read("cold-open.md", content_dir).cards[0],
        testimonies=testimonies,
        outside_world=_read("outside-world.md", content_dir).cards[0],
        decisions=decisions,
        reveal=reveal,
        aliases=_aliases(content_dir),
    )


def load_bundle(path=BUNDLE_PATH):
    with open(path, encoding="utf-8") as f:
        return f.read()


def normalize_name(text):
    return re.sub(r"[^a-z ]", "", text.lower()).strip()
