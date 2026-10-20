"""The AI investigator: a headless CLI that sees only the telemetry evidence bundle.

The AI is sent exactly three kinds of text: the system prompt below, the
evidence bundle (game/ai-evidence/case-bundle.md), and whatever the player
types after `ask`. It never gets a content card, the reveal or the player's
reasoning. Every call runs from an empty temporary directory.
"""

import json
import os
import shlex
import shutil
import subprocess
import tempfile

SYSTEM_PROMPT = (
    "You are the AI investigator in a murder-mystery game. The player is a human detective. "
    "Answer their questions using only the case files you were given, and say when the files "
    "don't answer something. Cite timestamps and sources where you can. Keep answers short "
    "enough to read in a terminal (about 250 words) unless the player asks for more."
)

SEED = (
    "You are investigating a death on the Sleep Floor at Kipsake. These are the case files: "
    "Kipsake's telemetry export. Use only them to answer my questions.\n\n"
    "<case_files>\n{bundle}\n</case_files>\n\n"
    "My first question: {question}"
)

# Flags proven to run Claude Code headless with no tools, no MCP servers and no
# user or project settings or hooks (see the blind AI test round).
CLAUDE_FLAGS = [
    "-p",
    "--tools", "",
    "--strict-mcp-config",
    "--setting-sources", "",
    "--output-format", "json",
]

NOT_LOGGED_IN = (
    "Claude Code doesn't seem to be logged in. Run `claude` once, sign in with /login, "
    "then try again. To use a different AI, set DJ_AI_CMD (see game/README.md)."
)


class AIError(Exception):
    pass


def _looks_like_auth_error(text):
    text = text.lower()
    return any(s in text for s in ("not logged in", "/login", "log in", "login", "authenticat",
                                   "api key", "credential", "unauthorized", "oauth"))


class _BaseAI:
    def __init__(self, bundle, timeout=900, runner=subprocess.run):
        self.bundle = bundle
        self.timeout = timeout
        self.runner = runner
        self.workdir = tempfile.mkdtemp(prefix="defiant-jazz-ai-")
        self.started = False

    def close(self):
        shutil.rmtree(self.workdir, ignore_errors=True)

    def _run(self, argv, stdin):
        try:
            return self.runner(
                argv, input=stdin, capture_output=True, text=True,
                cwd=self.workdir, timeout=self.timeout,
            )
        except FileNotFoundError:
            raise AIError(f"Couldn't run `{argv[0]}`: command not found.")
        except subprocess.TimeoutExpired:
            raise AIError(f"The AI didn't answer within {self.timeout} seconds.")


class ClaudeAI(_BaseAI):
    """Claude Code in print mode. One session per game, continued with --resume."""

    name = "Claude Code (headless, no tools)"

    def __init__(self, bundle, command="claude", model=None, **kwargs):
        super().__init__(bundle, **kwargs)
        self.command = command
        self.model = model
        self.session_id = None

    def check(self):
        if not shutil.which(self.command):
            return (f"`{self.command}` isn't on your PATH, so `ask` won't work. Install Claude Code, "
                    "or set DJ_AI_CMD to another headless AI (see game/README.md).")
        return None

    def ask(self, question):
        argv = [self.command] + CLAUDE_FLAGS + ["--system-prompt", SYSTEM_PROMPT]
        if self.model:
            argv += ["--model", self.model]
        if self.session_id:
            argv += ["--resume", self.session_id]
            stdin = question
        else:
            stdin = SEED.format(bundle=self.bundle, question=question)
        proc = self._run(argv, stdin)
        try:
            data = json.loads(proc.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            data = None
        if not isinstance(data, dict):
            detail = (proc.stderr or proc.stdout or "").strip()
            if _looks_like_auth_error(detail):
                raise AIError(NOT_LOGGED_IN)
            raise AIError(f"`{self.command}` exited with code {proc.returncode}: {detail[:500]}")
        result = str(data.get("result") or "")
        if data.get("is_error") or proc.returncode != 0:
            if _looks_like_auth_error(result):
                raise AIError(NOT_LOGGED_IN)
            raise AIError(f"The AI returned an error: {result[:500] or proc.stderr.strip()[:500]}")
        self.session_id = data.get("session_id") or self.session_id
        self.started = True
        return result.strip()


class CommandAI(_BaseAI):
    """Any headless CLI that reads a prompt on stdin and prints its answer on stdout.

    It keeps no session of its own, so every call sends the bundle plus the
    earlier questions and answers.
    """

    def __init__(self, bundle, command, **kwargs):
        super().__init__(bundle, **kwargs)
        self.argv = shlex.split(command)
        if not self.argv:
            raise AIError("DJ_AI_CMD is empty.")
        self.name = command
        self.history = []

    def check(self):
        if not shutil.which(self.argv[0]):
            return f"`{self.argv[0]}` isn't on your PATH, so `ask` won't work."
        return None

    def ask(self, question):
        turns = self.history + [(question, None)]
        prompt = SYSTEM_PROMPT + "\n\n" + SEED.format(bundle=self.bundle, question=turns[0][0])
        for i, (q, a) in enumerate(turns):
            if i:
                prompt += f"\n\nMy next question: {q}"
            if a is not None:
                prompt += f"\n\nYour answer: {a}"
        proc = self._run(self.argv, prompt)
        answer = (proc.stdout or "").strip()
        if proc.returncode != 0 or not answer:
            detail = (proc.stderr or proc.stdout or "").strip()
            raise AIError(f"`{self.argv[0]}` exited with code {proc.returncode}: {detail[:500]}")
        self.history.append((question, answer))
        self.started = True
        return answer


def from_settings(bundle, command=None, model=None, timeout=900):
    if command:
        return CommandAI(bundle, command, timeout=timeout)
    return ClaudeAI(bundle, command=os.environ.get("DJ_CLAUDE", "claude"), model=model,
                    timeout=timeout)
