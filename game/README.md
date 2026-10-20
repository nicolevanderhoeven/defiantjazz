# The Defiant Jazz Incident: terminal game

A local text adventure for demoing and playtesting the mystery. This page is spoiler-free.

> [!WARNING]
> **`SPOILERS-content/` contains spoilers.** It holds the clips you unlock in the game and `SPOILERS-reveal.md`, the solution. Don't open it before you play. `ai-evidence/` is safe: it's only the telemetry the AI is given.

## Play

```sh
python3 game/play.py
```

Python 3.9 or later, standard library only. The AI needs [Claude Code](https://docs.claude.com/en/docs/claude-code) installed and signed in (`claude`, then `/login`).

The game opens with the cold open and three security interviews. After that you choose what to do:

| Command | What it does |
|---|---|
| `ask <question>` | Ask the AI. It has Kipsake's telemetry, and nothing you've seen. |
| `investigate` | Take the next decision. There are three, each with three choices, and each choice unlocks one clip. |
| `review` | Re-read the cold open, the interviews, and anything you've unlocked. |
| `accuse <name>` | Name the killer and explain why. You can do this at any time, and it ends the game. |
| `help`, `quit` | |

The first `ask` sends the AI the whole case file (about 250 KB), so it can take a minute or two. Later questions are faster. Ctrl-C cancels a question.

## Options

```
--model MODEL     model for Claude Code, for example claude-opus-5-5 (env DJ_AI_MODEL)
--ai-cmd CMD      use another headless AI instead of Claude Code (env DJ_AI_CMD)
--timeout SECS    how long to wait for each answer, default 900 (env DJ_AI_TIMEOUT)
--no-ai           play without the AI
--no-color        plain text
--log FILE        append a transcript of the game to FILE (it will contain spoilers)
```

## What the AI sees

The AI only ever gets:
- a short system prompt (in `ai.py`)
- `ai-evidence/case-bundle.md`: the incident brief and a curated export of the telemetry, the same files an investigator would query. It includes the Story's pending data changes, so a few lines differ from `telemetry/`.
- what you type after `ask`, exactly as typed

It never gets a clip, the Outside World, the reveal, or your accusation and reasoning.

By default the game runs Claude Code in print mode with no tools, no MCP servers, and no user or project settings or hooks:

```
claude -p --tools "" --strict-mcp-config --setting-sources "" --output-format json --system-prompt "…"
```

Follow-up questions continue the same session with `--resume <session-id>`. Every call runs from a new, empty temporary directory, which is deleted when the game ends. Claude Code keeps its own session history under `~/.claude/projects/`. Set `DJ_CLAUDE` to use a `claude` binary that isn't on your `PATH`.

### Using another AI

`--ai-cmd` (or `DJ_AI_CMD`) takes any command that reads a prompt on stdin and prints its answer on stdout, for example:

```sh
DJ_AI_CMD='codex exec --skip-git-repo-check -s read-only -' python3 game/play.py
```

The command keeps no session, so the game sends the system prompt, the bundle and the earlier questions and answers each time. It's up to you to run that AI without tools or web access.

## Files

| Path | Contents |
|---|---|
| `play.py` | Entry point and options |
| `engine.py` | The game loop and commands |
| `content.py` | Loads the text cards |
| `ai.py` | Runs the AI |
| `test_game.py` | Self-check, below |
| `ai-evidence/case-bundle.md` | What the AI sees |
| `SPOILERS-content/` | **Spoilers:** the cold open, interviews, the three decisions, the Outside World handout and `SPOILERS-reveal.md` |

The cards are Markdown, one file per part of the game. `content.py` describes the format.

## Self-check

```sh
python3 -m unittest discover -s game
```

It loads every card, plays one full game with a stand-in AI, and checks that nothing the AI is sent contains human-only text. It never calls a real AI.
