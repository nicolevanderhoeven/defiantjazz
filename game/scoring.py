"""The scored accusation: its questions, its key and the matcher that marks a player's answers.

The key is game/SPOILERS-content/SPOILERS-scoring.json (see the comment at its top for the format). This
file is the Python matcher. The web game has the same one in web/game.js, between "scoring: matcher" and
"end of the matcher"; both must mark every (answer, points) pair in the key's "tests" the same way.

Matching is meant to be forgiving and cheap, never clever. Text is lower-cased, stripped of accents and
punctuation and cut into words. A group is hit when any of its words or phrases is among them, and a part
is earned when every group of one of its alternatives is hit. Names allow typos, and a name that follows
"not" or "never" is ruled out.
"""

import json
import os
import re
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(HERE, "SPOILERS-content", "SPOILERS-scoring.json")

NEGATORS = {"not", "no", "never", "nor", "neither", "isnt", "wasnt", "arent", "dont", "didnt", "than",
            "except", "besides", "without"}
NAME_MAX = 24

# A small list of words that can't be a leaderboard name. Whole words, after leet-speak is undone.
BLOCKED = ("fuck", "fucker", "fucking", "shit", "shite", "cunt", "bitch", "bastard", "whore", "slut",
           "nigger", "nigga", "faggot", "fag", "retard", "retarded", "rapist", "nazi", "hitler", "kike", "spic",
           "chink", "paki", "dyke", "tranny", "cum", "twat", "wanker", "bollocks")
# These are blocked wherever they appear in a name, even with the spaces taken out.
BLOCKED_ANYWHERE = ("fuck", "nigger", "nigga", "faggot")


class KeyError_(Exception):
    pass


def normalize(text):
    text = unicodedata.normalize("NFKD", str(text or ""))
    text = "".join(c for c in text if not unicodedata.combining(c)).lower()
    text = text.replace("'", "").replace("’", "")
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def _lev(a, b, limit):
    """Edit distance between two short words, or limit + 1 once it's clear it's more than limit."""
    if abs(len(a) - len(b)) > limit:
        return limit + 1
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        if min(cur) > limit:
            return limit + 1
        prev = cur
    return prev[-1]


def _kind(raw):
    """(kind, normalised words) for a synonym of the key: name, exact, prefix or plain."""
    raw = raw.strip()
    kind = "plain"
    if raw.startswith("~"):
        kind, raw = "name", raw[1:]
    elif raw.startswith("="):
        kind, raw = "exact", raw[1:]
    elif raw.endswith("*"):
        kind, raw = "prefix", raw[:-1]
    return kind, normalize(raw).split()


def _word(kind, token, want):
    if token == want:
        return True
    if kind == "exact":
        return False
    if kind == "prefix":
        return len(want) >= 3 and token.startswith(want)
    if token[:1] != want[:1]:
        return False
    if kind == "name":
        limit = 2 if len(want) >= 6 else 1 if len(want) >= 4 else 0
    else:
        limit = 1 if len(want) >= 5 else 0
    return limit > 0 and len(token) >= 4 and _lev(token, want, limit) <= limit


def _negated(tokens, i):
    return any(t in NEGATORS for t in tokens[max(0, i - 3):i])


def _find(tokens, synonym):
    kind, words = _kind(synonym)
    if not words:
        return False
    for i in range(len(tokens) - len(words) + 1):
        if all(_word(kind, tokens[i + j], w) for j, w in enumerate(words)):
            if kind == "name" and _negated(tokens, i):
                continue
            return True
    return False


def part_earned(part, tokens):
    return any(all(any(_find(tokens, s) for s in group) for group in alternative)
               for alternative in part["match"])


def named_suspects(key, tokens):
    """The suspects the text names (and doesn't rule out), by the names in the key."""
    return {who for who, names in key["suspects"].items() if any(_find(tokens, "~" + n) for n in names)}


def score_question(key, question, answer):
    """The points one answer earns by the matcher, and which parts earned them."""
    tokens = normalize(answer).split()
    parts = [False] * len(question["parts"])
    if not tokens:
        return 0, parts
    if question.get("suspect") and len(named_suspects(key, tokens)) > 1:
        return 0, parts
    parts = [part_earned(p, tokens) for p in question["parts"]]
    return sum(p["points"] for p, ok in zip(question["parts"], parts) if ok), parts


def score(key, answers):
    """Mark every answer ({question id: text}). Returns [{id, points, max, by}] for the questions in order."""
    rows = []
    for q in key["questions"]:
        points, _ = score_question(key, q, answers.get(q["id"], ""))
        rows.append({"id": q["id"], "points": points, "max": q["points"], "by": "matcher"})
    return rows


def total(rows):
    return sum(r["points"] for r in rows)


def maximum(key):
    return sum(q["points"] for q in key["questions"])


def validate(key, source=KEY_PATH):
    ids = [q.get("id") for q in key.get("questions", [])]
    if len(ids) != len(set(ids)) or not all(re.fullmatch(r"[a-z]+", str(i)) for i in ids):
        raise KeyError_(f"{source}: every question needs its own lower-case id")
    if set(key.get("suspects", {})) != {"agnes", "bertram", "clement"}:
        raise KeyError_(f"{source}: 'suspects' must name agnes, bertram and clement")
    for q in key["questions"]:
        for field in ("label", "short", "points", "answer", "judge", "parts"):
            if field not in q:
                raise KeyError_(f"{source}: question {q['id']!r} is missing {field!r}")
        if sum(p["points"] for p in q["parts"]) != q["points"]:
            raise KeyError_(f"{source}: question {q['id']!r}: its parts don't add up to its points")
        for part in q["parts"]:
            if not part["match"] or not all(alt and all(g for g in alt) for alt in part["match"]):
                raise KeyError_(f"{source}: question {q['id']!r}: a part has an empty alternative or group")
    if ids[:2] != ["killer", "why"] or [q.get("required") for q in key["questions"]] != [True, True] + [False] * (len(ids) - 2):
        raise KeyError_(f"{source}: the first two questions, and only they, are required")


def load_key(path=KEY_PATH):
    with open(path, encoding="utf-8") as f:
        key = json.load(f)
    validate(key, path)
    return key


def clean_name(text):
    """The leaderboard name for what the player typed: trimmed, simple characters, up to NAME_MAX of them.
    Returns (name, problem): problem is None, or why the name can't be used."""
    name = re.sub(r"\s+", " ", re.sub(r"[^\w .'’!-]", "", str(text or ""), flags=re.UNICODE)).strip()[:NAME_MAX].strip()
    flat = normalize(name.translate(str.maketrans("0134578@$", "oieastbas")))
    words = set(flat.split())
    despaced = flat.replace(" ", "")
    if words & set(BLOCKED) or despaced in BLOCKED or any(b in despaced for b in BLOCKED_ANYWHERE):
        return "", "That name isn't allowed. Pick another."
    return name, None
