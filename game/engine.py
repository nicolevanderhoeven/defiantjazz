"""The text adventure: cold open, testimonies, then a guided command loop."""

import re
import shutil
import textwrap

from ai import AIError
from content import SUSPECTS, resolve_suspect

DECISION_SHORT = ["check a scene", "the outside world", "push one sleepwalker"]

HELP = """\
Commands:
  ask <question>    Ask the AI. It has Kipsake's telemetry and has never seen
                    the clips, the Outside World or anything you write here.
  investigate       Take the next decision (three in all) and watch one clip.
  review [n|all]    Re-read the cold open, testimonies and clips you've unlocked.
  accuse <name>     Name the killer and explain why. You can do this any time,
                    even before using all three decisions. It ends the game.
  help              Show this list.
  quit              Leave without accusing."""

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

    def pause(self):
        self.read("[Enter] to continue ")

    # ---- flow -----------------------------------------------------------------

    def run(self):
        try:
            self.intro()
            self.loop()
        except Quit:
            self.say()
            self.say("Case closed without an accusation. The answer is still in the SPOILERS files.")
        except KeyboardInterrupt:
            self.say()
            self.say("Interrupted. Bye.")

    def intro(self):
        self.say(self._style("THE DEFIANT JAZZ INCIDENT", "1"))
        self.say("A murder mystery in Kipsake's telemetry. You hold the human-only evidence;")
        self.say("the AI holds the telemetry. Neither has seen the other's.")
        self.card(self.content.cold_open)
        self.pause()
        self.say()
        self.say(self._style("Floor Security interviewed the three persons of interest.", "1"))
        for testimony in self.content.testimonies:
            self.card(testimony)
            self.pause()
        self.say()
        self.paragraphs(
            "**Your turn.** The AI has Kipsake's telemetry: badges and doors, chat, metrics, "
            "system logs, microphone transcripts and records. It has never seen the clips. "
            "Ask it anything, then investigate when you want more evidence. You get three "
            "decisions, each with three choices, and you can name the killer whenever you're ready.")
        self.say()
        self.paragraphs("Try: ask Who killed Mr. Hale?")

    def hint(self):
        n = len(self.chosen)
        if n < 3:
            inv = f"investigate ({n + 1} of 3: {DECISION_SHORT[n]})"
        else:
            inv = "investigate (all three used)"
        text = f"What next? ask <question> · {inv} · review · accuse <name> · help · quit"
        self.say()
        for line in textwrap.wrap(text, self.width, subsequent_indent="           "):
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
                self.say(f"I don't know \"{command}\". To ask the AI, start with `ask`, "
                         "for example: ask Where was Clement W. at 15:04?")
                continue
            handler(arg)

    # ---- commands -------------------------------------------------------------

    def do_help(self, _arg=""):
        self.say()
        self.say(HELP)

    def do_quit(self, _arg=""):
        if self.read("Quit without naming the killer? (y/n) ").lower().startswith("y"):
            raise Quit()

    def do_ask(self, question):
        if self.ai is None:
            self.say("The AI is turned off for this game (--no-ai).")
            return
        if not question:
            question = self.read("Your question for the AI: ")
            if not question:
                return
        if not self.ai.started:
            self.say(self._style("(The AI is reading the case files for the first time. "
                                 "This answer can take a minute or two. Ctrl-C cancels.)", "2"))
        else:
            self.say(self._style("(Asking the AI… Ctrl-C cancels.)", "2"))
        try:
            answer = self.ai.ask(question)
        except AIError as e:
            self.say(f"The AI couldn't answer: {e}")
            return
        except KeyboardInterrupt:
            self.say("(Cancelled.)")
            return
        self.asked.append((question, answer))
        self.say()
        self.say(self._style("AI:", "1"))
        self.paragraphs(answer)

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
            self.say("You've used all three decisions. When you're ready: accuse <name>.")
            return
        if n == 1 and not self.outside_shown:
            self.say()
            self.say(self._style("Before the next decision, a handout from outside Kipsake.", "1"))
            self.card(self.content.outside_world)
            self.outside_shown = True
            self.pause()
        decision = self.content.decisions[n]
        self.say()
        self.say(self._style(decision.title, "1"))
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
        self.card(picked, heading=f"Decision {n + 1} · {picked.title}")
        if n < 2:
            self.say(f"Ask the AI about anything here, or investigate again "
                     f"(decision {n + 2}: {DECISION_SHORT[n + 1]}).")
        else:
            self.say("That was your last decision. Ask the AI anything else, then accuse <name>.")

    def review_items(self):
        items = [("Cold open", self.content.cold_open)]
        items += [(t.title, t) for t in self.content.testimonies]
        if self.outside_shown:
            items.append(("Outside World handout", self.content.outside_world))
        for n, card in self.chosen:
            items.append((f"Decision {n + 1} · {card.title}", card))
        return items

    def do_review(self, arg=""):
        items = self.review_items()
        if not arg:
            self.say()
            for i, (label, _) in enumerate(items, 1):
                self.say(f"  {i}) {label}")
            if self.asked:
                self.say(f"  {len(items) + 1}) Your questions to the AI ({len(self.asked)})")
            arg = self.read("Which one? (a number, 'all', or [Enter] to go back) ")
            if not arg:
                return
        if arg.lower() == "all":
            for label, card in items:
                self.card(card, heading=label)
            return
        if arg.isdigit() and 1 <= int(arg) <= len(items):
            label, card = items[int(arg) - 1]
            self.card(card, heading=label)
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
        key = resolve_suspect(name)
        if key:
            label = SUSPECTS[key]
        else:
            label = name
            if not self.read(f"{name} isn't one of the three persons of interest. "
                             "Accuse them anyway? (y/n) ").lower().startswith("y"):
                return
            key = "other"
        left = 3 - len(self.chosen)
        if left:
            self.say(f"You still have {left} decision{'s' if left > 1 else ''} left. "
                     "You can accuse now or keep investigating.")
        if not self.read(f"Accuse {label}? This ends the game. (y/n) ").lower().startswith("y"):
            return
        self.say("Why? Explain your reasoning. Finish with an empty line.")
        lines = []
        while True:
            line = self.read("  ")
            if not line:
                break
            lines.append(line)
        self.accused = key
        self.reasoning = "\n".join(lines)
        self.reveal(label)

    def reveal(self, label):
        cards = self.content.reveal.cards
        verdict = next(c for c in cards if c.meta.get("for") == self.accused)
        self.say()
        self.say(self._style(f"You accused {label}.", "1"))
        if self.reasoning:
            self.paragraphs("> " + self.reasoning.replace("\n", " "))
        self.card(verdict, heading=verdict.title if self.accused != "other" else
                  f"You named {label}")
        for card in cards:
            if card.meta.get("for") == "all":
                self.pause()
                self.card(card)
        self.say("Thanks for playing.")
