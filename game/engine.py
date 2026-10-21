"""The text adventure: the Kipsake advert, cold open, testimonies, then a guided command loop."""

import re
import shutil
import textwrap

from ai import AIError
from content import SUSPECTS

DECISION_SHORT = ["check a scene", "the outside world", "push one sleepwalker"]
LEAD_KIND = ["a crime scene", "a home visit", "one last interview"]

HELP = """\
Commands:
  ask <question>    Ask your AI assistant anything. It has read Kipsake's
                    records, and nothing else: it hasn't seen the interviews,
                    the leads you follow, or anything you find. If you want it
                    to know something, tell it.
  investigate       Follow up the next of your three leads, in order: a crime
                    scene, a home visit, one last interview. Each time, you
                    pick one of three options and see only that one. Use them
                    whenever you like, between questions.
  review [n|all]    Re-read the advert, cold open, interviews and clips you've
                    unlocked.
  accuse <name>     When you're ready, name the killer and say why. You can do
                    this any time, even before all three leads. It ends the game.
  help              Show this list.
  quit              Leave without accusing."""

BANNER = r"""
  T  H  E
 ___   ___  ___  ___    _    _  _  _____        _    _    ____  ____
|   \ | __|| __||_ _|  /_\  | \| ||_   _|    _ | |  /_\  |_  / |_  /
| |) || _| | _|  | |  / _ \ | .` |  | |     | || | / _ \  / /   / /
|___/ |___||_|  |___|/_/ \_\|_|\_|  |_|      \__/ /_/ \_\/___| /___|
                                                  I N C I D E N T
"""[1:-1]

_STYLE = {"**": "1", "*": "3", "~~": "9"}
_TOKEN = re.compile(r"(\*\*|~~|\*)")
_SPEAKER = re.compile(r"^([A-Z][A-Za-z.' ]{0,24}): ")


class Quit(Exception):
    pass


class Game:
    def __init__(self, content, ai, input_fn=input, write=print, color=False, width=None,
                 log=None):
        self.content = content
        self.ai = ai
        self.input_fn = input_fn
        self.write = write
        self.color = color
        self.width = width or min(shutil.get_terminal_size((88, 24)).columns, 88)
        self.log = log
        self.chosen = []  # (decision index, Card)
        self.outside_shown = False
        self.asked = []  # (question, answer)
        self.accused = None
        self.reasoning = ""

    # ---- output ---------------------------------------------------------------

    def say(self, text=""):
        self.write(text)
        if self.log:
            self.log.write(re.sub(r"\x1b\[[0-9;]*m", "", text) + "\n")
            self.log.flush()

    def read(self, prompt):
        try:
            # \001 and \002 tell readline the escape codes take no space.
            styled = f"\001\x1b[1m\002{prompt}\001\x1b[0m\002" if self.color else prompt
            answer = self.input_fn(styled)
        except EOFError:
            raise Quit()
        if self.log:
            self.log.write(f"{prompt}{answer}\n")
            self.log.flush()
        return answer.strip()

    def _style(self, text, code):
        return f"\x1b[{code}m{text}\x1b[0m" if self.color else text

    def _inline(self, lines, base=""):
        """Turn **bold**, *italic* and ~~struck~~ into ANSI (or plain text), line by line."""
        def codes():
            styles = ([base] if base else []) + [_STYLE[t] for t in active]
            return f"\x1b[{';'.join(styles)}m" if styles else ""

        out, active = [], []
        for line in lines:
            if not self.color:
                out.append(_TOKEN.sub(lambda m: m.group(0) if m.group(0) == "~~" else "", line))
                continue
            parts = [codes()]
            for piece in _TOKEN.split(line):
                if piece in _STYLE:
                    if piece in active:
                        active.remove(piece)
                    else:
                        active.append(piece)
                    parts.append("\x1b[0m" + codes())
                else:
                    parts.append(piece)
            parts.append("\x1b[0m")
            out.append("".join(parts))
        return out

    def _wrap(self, text, indent="", hang=None, base=""):
        hang = indent if hang is None else hang
        lines = textwrap.wrap(text, self.width, initial_indent=indent, subsequent_indent=hang,
                              break_on_hyphens=False) or [indent]
        return self._inline(lines, base)

    def paragraphs(self, text):
        """Print free text (an AI answer, a card body) wrapped to the terminal."""
        for raw in text.splitlines():
            line = raw.rstrip()
            if not line.strip():
                self.say()
                continue
            stripped = line.lstrip()
            lead = line[: len(line) - len(stripped)]
            bullet = re.match(r"^([-*•]|\d+[.)])\s+", stripped)
            if line.startswith("[") and line.endswith("]"):
                for out in self._wrap(line, base="2;3"):
                    self.say(out)
            elif line.startswith(">"):
                for out in self._wrap(line[1:].strip(), indent="  │ "):
                    self.say(out)
            elif bullet:
                if bullet.group(1) == "*":
                    stripped = "-" + stripped[1:]
                hang = lead + " " * len(bullet.group(0))
                for out in self._wrap(stripped, indent=lead, hang=hang):
                    self.say(out)
            elif _SPEAKER.match(line):
                name = _SPEAKER.match(line).group(1)
                body = line[len(name) + 2:]
                lines = self._wrap(f"{name}: {body}", hang="    ")
                if self.color:
                    lines[0] = lines[0].replace(f"{name}:", self._style(f"{name}:", "1"), 1)
                for out in lines:
                    self.say(out)
            else:
                for out in self._wrap(stripped, indent=lead):
                    self.say(out)

    def card(self, card, heading=None):
        title = heading or card.title
        self.say()
        self.say(self._style(title, "1"))
        self.say(self._style("─" * min(len(title) + 4, self.width), "2"))
        self.paragraphs(card.body)
        self.say()

    def advert(self, card):
        """A card boxed like a TV advert: each line its own paragraph, centred."""
        inner = self.width - 4
        label = f" {card.title.upper()} · ADVERT "

        def edge(text):
            return self._style(text, "2")

        blank = edge("│") + " " * (inner + 2) + edge("│")
        self.say()
        self.say(edge("╭─" + label + "─" * max(inner - len(label), 0) + "─╮"))
        self.say(blank)
        for raw in card.body.splitlines():
            line = raw.strip()
            if not line:
                continue
            stage = line.startswith("[") and line.endswith("]")
            for piece in textwrap.wrap(line, inner, break_on_hyphens=False):
                pad = inner - len(re.sub(r"\*\*|\*", "", piece))
                text = self._inline([piece], base="2;3" if stage else "")[0]
                self.say(edge("│") + " " * (1 + pad // 2) + text + " " * (pad - pad // 2 + 1) + edge("│"))
            self.say(blank)
        self.say(edge("╰" + "─" * (inner + 2) + "╯"))
        self.say()

    def show(self, card, heading=None):
        if card.meta.get("style") == "advert":
            self.advert(card)
        else:
            self.card(card, heading)

    def rule(self, label=""):
        """A dim line that marks the start of a new block of output."""
        text = f"── {label} " if label else ""
        self.say(self._style(text + "─" * max(self.width - len(text), 3), "2"))

    def pause(self):
        self.read("[Enter] to continue ")

    # ---- flow -----------------------------------------------------------------

    def run(self):
        try:
            self.intro()
            self.loop()
        except Quit:
            self.say()
            self.say("Case closed without an accusation. Run the game again to keep investigating.")
        except KeyboardInterrupt:
            self.say()
            self.say("Interrupted. Bye.")

    def intro(self):
        if self.width >= max(len(line) for line in BANNER.splitlines()):
            self.say(self._style(BANNER, "1"))
        else:
            self.say(self._style("THE DEFIANT JAZZ INCIDENT", "1"))
        self.say()
        self.rule("Cold open")
        self.advert(self.content.advert)
        self.pause()
        self.card(self.content.cold_open)
        self.pause()
        self.say()
        self.rule("Interviews")
        self.paragraphs(self.content.testimony_intro)
        for i, testimony in enumerate(self.content.testimonies):
            if i:
                self.say()
                self.rule()
            self.card(testimony)
            self.pause()
        self.say()
        self.rule("Your turn")
        self.paragraphs(
            "Your AI assistant has read Kipsake's records: badges and doors, chat, metrics, "
            "system logs, microphone transcripts and other records. It hasn't seen the interviews, "
            "the leads you follow, or anything you find. If you want it to know something, tell "
            "it. You have three leads to follow up, one at a time, whenever you're ready: type "
            "investigate. When you're ready, accuse the killer and say why.")
        self.say()
        self.paragraphs("You can ask anything. If you're not sure where to start, you could ask it "
                        "who it thinks did it: ask Who killed Mr. Hale?")

    def hint(self):
        n = len(self.chosen)
        if n < 3:
            leads = (f"Leads left: {3 - n} of 3 · type investigate for the next one "
                     f"({LEAD_KIND[n]})")
        else:
            leads = "Leads left: 0 of 3 · all three leads used · type accuse <name> when you're ready"
        parts = ["ask <question>", "investigate", "review", "accuse <name>", "help", "quit"]
        self.say()
        self.rule()
        for row in textwrap.wrap(leads, self.width, subsequent_indent="  "):
            self.say(self._style(row, "2"))
        # Wrap between commands, never inside one.
        line = "What next? " + parts[0]
        for part in parts[1:]:
            if len(line) + 3 + len(part) + 2 > self.width:  # room for the trailing " ·"
                self.say(self._style(line + " ·", "2"))
                line = "           " + part
            else:
                line += " · " + part
        self.say(self._style(line, "2"))

    def loop(self):
        while self.accused is None:
            self.hint()
            line = self.read("> ")
            if not line:
                continue
            command, _, arg = line.partition(" ")
            command, arg = command.lower(), arg.strip()
            handler = {
                "ask": self.do_ask, "investigate": self.do_investigate, "inv": self.do_investigate,
                "review": self.do_review, "accuse": self.do_accuse, "help": self.do_help,
                "quit": self.do_quit, "exit": self.do_quit,
            }.get(command)
            if handler is None:
                self.say(f"I don't know \"{command}\". To ask your AI assistant, start with `ask`, "
                         "for example: ask What happened at 03:02?")
                continue
            handler(arg)

    # ---- commands -------------------------------------------------------------

    def do_help(self, _arg=""):
        self.say()
        self.rule("Help")
        self.say(HELP)

    def do_quit(self, _arg=""):
        if self.read("Quit without naming the killer? (y/n) ").lower().startswith("y"):
            raise Quit()

    def do_ask(self, question):
        if self.ai is None:
            self.say("Your AI assistant is turned off for this game (--no-ai).")
            return
        if not question:
            question = self.read("Your question for your AI assistant: ")
            if not question:
                return
        if not self.ai.started:
            for line in self._wrap("(Your AI assistant is reading Kipsake's records for the first "
                                   "time. This answer can take up to a minute. Ctrl-C cancels.)",
                                   base="2"):
                self.say(line)
        else:
            self.say(self._style("(Asking your AI assistant… Ctrl-C cancels.)", "2"))
        try:
            answer = self.ai.ask(question)
        except AIError as e:
            self.say(f"Your AI assistant couldn't answer: {e}")
            return
        except KeyboardInterrupt:
            self.say("(Cancelled.)")
            return
        self.asked.append((question, answer))
        self.say()
        self.rule("AI assistant")
        self.paragraphs(answer)
        if len(self.asked) == 1:
            self.say()
            self.paragraphs("Ask whatever you like next. For example, to look at the evidence, "
                            "you could ask: ask What happened near the elevator between 03:02 "
                            "and 03:07?")

    def _choose(self, decision, arg):
        options = decision.options

        def match(text):
            text = text.lower().strip().rstrip(".")
            if text.isdigit() and 1 <= int(text) <= len(options):
                return options[int(text) - 1]
            for card in options:
                names = [card.meta["option"].lower(), card.title.lower()]
                names += [a.strip() for a in card.meta.get("aliases", "").lower().split(",")]
                if text in names:
                    return card
            return None

        if arg:
            picked = match(arg)
            if picked:
                return picked
        while True:
            answer = self.read("Choose 1, 2 or 3 ([Enter] to decide later): ")
            if not answer:
                return None
            picked = match(answer)
            if picked:
                return picked
            self.say("Pick 1, 2 or 3.")

    def do_investigate(self, arg=""):
        n = len(self.chosen)
        if n >= 3:
            self.say("You've followed up all three leads. "
                     "When you're ready: accuse <name>.")
            return
        if n == 1 and not self.outside_shown:
            self.say()
            self.rule("Outside World handout")
            self.say(self._style("Before the next lead, a handout from outside Kipsake.", "1"))
            self.card(self.content.outside_world)
            self.outside_shown = True
            self.pause()
        decision = self.content.decisions[n]
        self.say()
        self.rule(f"Lead {n + 1} of 3")
        self.say(self._style(decision.title.split(" · ", 1)[-1], "1"))
        self.paragraphs(decision.prompt)
        self.say()
        for i, card in enumerate(decision.options, 1):
            note = card.meta.get("note")
            self.say(f"  {i}) {card.meta['option']}" + (f"  ({note})" if note else ""))
        self.say()
        picked = self._choose(decision, arg)
        if picked is None:
            self.say("No rush. Type investigate when you're ready.")
            return
        self.chosen.append((n, picked))
        self.card(picked, heading=f"Lead {n + 1} · {picked.title}")
        if n < 2:
            self.paragraphs(f"Ask your AI assistant about anything here, or investigate again "
                            f"(lead {n + 2}: {DECISION_SHORT[n + 1]}).")
        else:
            self.say("That was the last lead. Ask your AI assistant anything else, "
                     "then accuse <name>.")

    def review_items(self):
        items = [("The Kipsake advert", self.content.advert), ("Cold open", self.content.cold_open)]
        items += [(t.title, t) for t in self.content.testimonies]
        if self.outside_shown:
            items.append(("Outside World handout", self.content.outside_world))
        for n, card in self.chosen:
            items.append((f"Lead {n + 1} · {card.title}", card))
        return items

    def do_review(self, arg=""):
        items = self.review_items()
        self.say()
        self.rule("Review")
        if not arg:
            for i, (label, _) in enumerate(items, 1):
                self.say(f"  {i}) {label}")
            if self.asked:
                self.say(f"  {len(items) + 1}) Your questions to your AI assistant "
                         f"({len(self.asked)})")
            arg = self.read("Which one? (a number, 'all', or [Enter] to go back) ")
            if not arg:
                return
        if arg.lower() == "all":
            for label, card in items:
                self.show(card, heading=label)
            return
        if arg.isdigit() and 1 <= int(arg) <= len(items):
            label, card = items[int(arg) - 1]
            self.show(card, heading=label)
        elif arg.isdigit() and int(arg) == len(items) + 1 and self.asked:
            for q, a in self.asked:
                self.say()
                self.say(self._style(f"You: {q}", "1"))
                self.paragraphs(a)
        else:
            self.say("There's nothing with that number. Type review to see the list.")

    def do_accuse(self, arg=""):
        name = arg or self.read("Who killed Mr. Hale? (Agnes, Bertram or Clement) ")
        if not name:
            return
        key = self.content.resolve_suspect(name)
        if key:
            label = SUSPECTS[key]
        else:
            label = name
            if not self.read(f"{name} isn't one of the three suspects. "
                             "Accuse them anyway? (y/n) ").lower().startswith("y"):
                return
            key = "other"
        left = 3 - len(self.chosen)
        if left:
            self.paragraphs(f"You still have {left} lead{'s' if left > 1 else ''} to "
                            "follow up. You can accuse now or keep investigating.")
        if not self.read(f"Accuse {label}? This ends the game. (y/n) ").lower().startswith("y"):
            return
        self.paragraphs("Why? Explain your reasoning. Finish with a line containing only \".\" "
                        "or with two empty lines in a row.")
        lines = []
        while True:
            line = self.read("  ")
            if line.strip() == ".":
                break
            if not line.strip() and lines and not lines[-1].strip():
                break
            lines.append(line)
        self.accused = key
        self.reasoning = "\n".join(lines).strip()
        self.reveal(label)

    def reveal(self, label):
        cards = self.content.reveal.cards
        verdict = next(c for c in cards if c.meta.get("for") == self.accused)
        self.say()
        self.rule("The verdict")
        stop = "" if label.endswith(".") else "."
        self.say(self._style(f"You accused {label}{stop}", "1"))
        for para in re.split(r"\n\s*\n", self.reasoning):
            if para.strip():
                self.paragraphs("> " + " ".join(para.split()))
        self.card(verdict, heading=verdict.title if self.accused != "other" else
                  f"You named {label}")
        for card in cards:
            if card.meta.get("for") == "all":
                self.pause()
                self.say()
                self.rule()
                self.card(card)
        self.say("Thanks for playing.")
