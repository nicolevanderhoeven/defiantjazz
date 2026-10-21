# The Defiant Jazz Incident: terminal game

A local text adventure for demoing and playtesting the mystery.

> [!WARNING]
> **`SPOILERS-content/` and `test_SPOILERS_game.py` contain spoilers.** The folder holds the clips you unlock in the game, the names the game accepts for each suspect, and `SPOILERS-reveal.md`, the solution. The test names the killer. Don't open either before you play. `ai-evidence/` is safe: it's only the telemetry the AI is given.

## Play

```sh
python3 game/play.py
```

Python 3.9 or later, standard library only. For the AI, use any one you like (see [Choosing the AI](#choosing-the-ai)). With nothing set, the game uses the first of Claude Code, Codex and Gemini CLI that's installed. If none is, it tells you how to plug one in, and you can still play.

The game opens with a Kipsake advert, the cold open and your three interviews. After that you choose what to do:

| Command | What it does |
|---|---|
| `ask <question>` | Ask your AI assistant anything. It has read Kipsake's records (the telemetry), and nothing else: it hasn't seen the interviews, the leads you follow, or anything you find. If you want it to know something, tell it. |
| `investigate` | Follow up your next lead. There are three, one at a time, each with three choices, and each choice unlocks one clip. |
| `review` | Re-read the advert, the cold open, the interviews, and anything you've unlocked. |
| `accuse <name>` | When you're ready, name the killer and say why. You can do this at any time, and it ends the game. |
| `help`, `quit` | |

The first `ask` sends the AI the whole case file (about 80 KB), so it can take up to a minute. Later questions are faster. Ctrl-C cancels a question.

## Options

```
--ai NAME         claude, codex or gemini (env DJ_AI). Default: the first one installed
--ai-cmd CMD      use any other headless AI (env DJ_AI_CMD). Overrides --ai
--model MODEL     model for Claude Code, Codex or Gemini CLI, for example claude-opus-5-5 (env DJ_AI_MODEL)
--timeout SECS    how long to wait for each answer, default 900 (env DJ_AI_TIMEOUT)
--no-ai           play without the AI
--no-color        plain text
--log FILE        append a transcript of the game to FILE (it will contain spoilers)
```

## What the AI sees

The AI only ever gets:
- a short system prompt (in `ai.py`)
- `ai-evidence/case-bundle.md`: the incident brief and a curated excerpt of `telemetry/` (from the Paper Test), the same kind of files an investigator would query.
- what you type after `ask`, exactly as typed

It never gets a clip, the Outside World, the reveal, or your accusation and reasoning.

Every call runs from a new, empty temporary directory, which is deleted when the game ends.

## Choosing the AI

With no `--ai` or `--ai-cmd`, the game looks for these on your `PATH`, in this order, and uses the first it finds. Each one runs headless, with no tools and no web access as far as the tool allows. `--model` is passed to whichever one runs.

**Claude Code** (`claude`, signed in with `/login`). It runs in print mode with no tools, no MCP servers, and no user or project settings or hooks:

```
claude -p --tools "" --strict-mcp-config --setting-sources "" --output-format json --system-prompt "…"
```

Follow-up questions continue the same session with `--resume <session-id>`. Claude Code keeps its own session history under `~/.claude/projects/`. Set `DJ_CLAUDE` to use a `claude` binary that isn't on your `PATH`.

**Codex** (`codex`, signed in). It runs `codex exec` read-only, with web search off, its user config and rules ignored, no saved session, and every tool feature that the installed version lists turned off (`shell_tool`, `unified_exec`, `apps`, `browser_use`, `plugins` and the rest, listed in `ai.py`):

```
codex exec --ephemeral --ignore-user-config --ignore-rules --skip-git-repo-check -s read-only -c web_search=disabled --disable shell_tool --disable unified_exec … -
```

**Gemini CLI** (`gemini`, signed in). It runs in plan mode, which is read-only:

```
gemini --approval-mode plan
```

Gemini CLI has no flag to turn its read-only tools off, so it can still read files in its empty temporary folder or search the web. This one is untested.

Codex and Gemini CLI keep no session for the game, so it sends the system prompt, the bundle and the earlier questions and answers each time.

### Using another AI

`--ai-cmd` (or `DJ_AI_CMD`) takes any command that reads a prompt on stdin and prints its answer on stdout. It works like Codex and Gemini above: the whole conversation is sent each time, from an empty temporary folder. It's up to you to run that AI without tools or web access, and `--model` doesn't apply, so put the model in the command. Some examples:

```sh
# Codex, read-only with no shell and no web search
DJ_AI_CMD='codex exec --ephemeral --skip-git-repo-check -s read-only -c web_search=disabled --disable shell_tool --disable unified_exec -' python3 game/play.py
# Gemini CLI with a chosen model (untested)
DJ_AI_CMD='gemini --approval-mode plan -m pro' python3 game/play.py
# A local model with Ollama
DJ_AI_CMD='ollama run --hidethinking --nowordwrap llama3.2:3b' python3 game/play.py
```

**Ollama needs a long context.** The bundle is about 14,000 tokens, and Ollama's default context is much shorter, so it silently drops most of the case files. Set the context length to 32k or more, in the Ollama app's settings or with `OLLAMA_CONTEXT_LENGTH=32768 ollama serve`. On a laptop, the first answer can take many minutes.

### Using your own agent

> [!WARNING]
> **Don't run an agent with file access inside this repo's folder.** It can read `SPOILERS-content/` and the other spoiler files. Give it only `ai-evidence/case-bundle.md`, for example by copying that file into an empty folder and starting the agent there. Or have it investigate through Grafana with the Grafana MCP server (see the main README).

## Files

| Path | Contents |
|---|---|
| `play.py` | Entry point and options |
| `engine.py` | The game loop and commands |
| `content.py` | Loads the text cards |
| `ai.py` | Runs the AI |
| `test_SPOILERS_game.py` | **Spoilers:** the self-check, below |
| `test_ai.py` | How the game picks the AI and builds each command line. No spoilers |
| `ai-evidence/case-bundle.md` | What the AI sees |
| `SPOILERS-content/` | **Spoilers:** the advert and cold open, interviews, the three decisions, the Outside World handout, `suspect-names.json` and `SPOILERS-reveal.md` |

The cards are Markdown, one file per part of the game. `content.py` describes the format.

## Self-check

```sh
python3 -m unittest discover -s game
```

It loads every card, plays one full game with a stand-in AI, and checks that nothing the AI is sent contains human-only text. It also checks the order the game looks for an AI in and the message when there's none. It never calls a real AI.
