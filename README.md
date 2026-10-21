# The Defiant Jazz Incident

An observability murder mystery set on the Sleep Floor at Kipsake.

During the Cocoa Hour, a quiet quota reward in Break Room 2, the floor loses power for five minutes. When the power comes back, Floor Supervisor Mr. Reginald Hale is dead in the elevator. Kipsake recorded everything it could: badges, doors, chat, sleep rings, power, microphones, cameras, sleep bands, personnel records. Your job is to work out who killed him.

This repo contains the telemetry and the tools to load it into Grafana: Loki for logs, Prometheus or Mimir for metrics, and Tempo for traces. You can load it into Grafana Cloud or a local Docker stack, then investigate with Grafana, Grafana Assistant, an MCP server, `gcx`, or the AI agent of your choice. It also has the game itself, in a terminal version for demos and playtests and a web version to embed in a Grafana dashboard.

> [!WARNING]
> **Spoilers live in `game/SPOILERS-content/`, `game/test_SPOILERS_game.py` and `web/SPOILERS-content.js`.** The folder holds the human-only story clips and `SPOILERS-reveal.md`, which names the killer and explains the solution. The test names the killer too, and the web bundle is built from that folder. Don't open them if you want to play.
>
> Everything else is safe to read: `CASE-BRIEF.md`, `telemetry/`, `loader/`, `local/` and `game/ai-evidence/` hold only what an investigator is given, never the solution. The rest of `web/` is spoiler-free too.

## Play the game

A text adventure for running locally. You watch the testimonies and choose what to investigate, while an AI that sees only the telemetry answers your questions. You need Python 3, plus any AI you like.

```sh
python3 game/play.py
```

Type `help` in the game for the commands. [`game/README.md`](game/README.md) covers the AI options in full and has no spoilers.

### Bring your own AI

The game finds an AI on its own: [Claude Code](https://docs.claude.com/en/docs/claude-code), then [Codex](https://github.com/openai/codex), then [Gemini CLI](https://github.com/google-gemini/gemini-cli): it uses the first one that's installed (sign in to it first). It runs it headless, with no tools and no web access where the tool allows it, from an empty temporary folder. If it finds none, the game says how to plug one in, and you can still play without it.

- **Pick one:** `--ai claude`, `--ai codex` or `--ai gemini` (or `DJ_AI`), with `--model` to choose its model.
- **Any other AI:** `--ai-cmd` (or `DJ_AI_CMD`) takes any command that reads a prompt on stdin and prints its answer on stdout. For example:

  ```sh
  # Codex, read-only with no shell and no web search
  python3 game/play.py --ai-cmd 'codex exec --ephemeral --skip-git-repo-check -s read-only -c web_search=disabled --disable shell_tool --disable unified_exec -'
  # Gemini CLI in read-only plan mode (untested)
  python3 game/play.py --ai-cmd 'gemini --approval-mode plan'
  # A local model with Ollama: set its context length to 64k or more first (see game/README.md)
  python3 game/play.py --ai-cmd 'ollama run --hidethinking --nowordwrap llama3.2:3b'
  ```

- **No AI:** `--no-ai`.

> [!WARNING]
> **Don't run your own agent inside this repo's folder.** An agent with file access can read the spoiler files. Give it only `game/ai-evidence/case-bundle.md`, or have it investigate through Grafana with the [Grafana MCP server](#grafana-mcp-server-on-the-local-stack).

### In the browser or a Grafana dashboard

The same game as a static web page, made to embed in a Grafana dashboard panel next to the telemetry. There's no AI inside it: players ask Grafana Assistant, or their own agent through the Grafana MCP server or `gcx`, and the page offers example questions to copy. To play it locally:

```sh
python3 -m http.server 8080 --bind 127.0.0.1 --directory web
```

Then open <http://localhost:8080/>. [`web/README.md`](web/README.md) covers embedding it in a dashboard with the example dashboard, and has no spoilers.

> [!WARNING]
> **`web/SPOILERS-content.js` contains spoilers.** It's built from `game/SPOILERS-content/` and includes the solution, so don't open it if you want to play.

## What's in it

| Path | Contents |
|---|---|
| `CASE-BRIEF.md` | The incident brief Floor Security hands to investigators |
| `game/` | The terminal game. **`game/SPOILERS-content/` and `game/test_SPOILERS_game.py` contain spoilers.** |
| `web/` | The web version, for a browser or a Grafana dashboard panel. **`web/SPOILERS-content.js` contains spoilers.** |
| `telemetry/door-and-badge-events.log` | Door readers, badge journeys and trace spans |
| `telemetry/chat.log` | Floor chat |
| `telemetry/metrics.csv` | Time series (`ts,metric,labels,value,ingested_at`) |
| `telemetry/system.log` | Sleep rings, power, outlets, quota rewards, emergency speakers, elevator, cameras, security, medical |
| `telemetry/ambient-mic.log` | Ambient compliance-microphone transcripts, 15:02 to 15:10 (buffered during the outage, live after it) |
| `telemetry/records.log` | Personnel, detention, Hush Room, supervisor feedback, perks, keystroke drafts, calendar |
| `loader/` | `load.py` sends everything over OTLP; `test_load.py` checks its time shift |
| `local/` | Docker Compose stack: Loki, Prometheus, Tempo, Grafana (with Grafana Assistant) and the Grafana MCP server |

That's about 127,000 lines across roughly 120 employees and 14 weeks. Reading it end to end isn't practical, so query it.

## How the data maps to Grafana

- **Loki:** every log line, unchanged except for timestamp shifting (see below). Each source (`door`, `chat`, `ring`, `power`, `ambient-mic`, `security`, `personnel`, `hush-room`, …) is its own `service_name`, all under `service_namespace="kipsake-sleep-floor"`. Lines are logfmt, so `| logfmt` works.
  - Records are a database pull, not a stream, so they are ingested as one export at the end of the incident. Their own dates are kept in each line.
- **Prometheus / Mimir:** every row of `metrics.csv` as a gauge, for example `badge_accel_variance`, `sleep_band_heart_rate_bpm`, `circuit_power_watts` and `quota_file_progress`. Samples recorded on a device during the outage and uploaded late carry `buffered="true"`.
- **Tempo:** one trace per badge per day (`service.name="kipsake-badge-tracking"`), with a span for each door-reader or elevator-reader event. The days are the data's own, so a shift across midnight doesn't split a journey.

## Loading into Grafana Cloud

1. In the Grafana Cloud portal, open your stack's **OpenTelemetry** tile, generate a token with write access, and note the OTLP endpoint and instance ID.
2. Copy the env template and fill it in:
   ```sh
   cp loader/.env.example loader/.env   # never commit this file
   ```
3. Install and run:
   ```sh
   python3 -m pip install -r loader/requirements.txt
   python3 loader/load.py --target cloud
   ```

**Time shifting.** Grafana Cloud rejects metric samples more than about 2 hours behind the newest sample, and log entries older than 7 days. So by default the loader shifts every timestamp so the incident happened just before "now". Timestamps inside log lines move by the same amount, so the data stays consistent. This moves the times of day too: the story's 15:02 lands at whatever time you loaded it. The loader prints the mode and the shift it used.

Because of those limits, Grafana Cloud gets:
- the last 7 days of logs and traces, which includes all of the incident day and every record
- the last 2 hours of metrics, which includes the whole incident window

Older history is skipped, and the loader reports how much. To see the full 14 weeks, use the local stack.

**Traces in Grafana Cloud.** The badge-journey traces can be opened by trace ID right away. Because their timestamps are hours or days old, they can take up to about an hour after loading to show up in TraceQL search. Every door-event log line also carries its journey's `trace_id`, so in Loki you can jump from a door event to its trace.

**macOS note.** If the loader fails with `CERTIFICATE_VERIFY_FAILED`, install the requirements, which include `certifi`. The python.org build of Python doesn't use the system certificate store.

## Loading into a local stack

```sh
cd local && docker compose up -d && cd ..
python3 -m pip install -r loader/requirements.txt
python3 loader/load.py --target local
```

Grafana 13.2 runs at <http://localhost:3000>, and the Loki, Prometheus and Tempo data sources are already provisioned. Every port is bound to `127.0.0.1`, so nothing is reachable from your network.

**Sign-in:** the default is **admin / admin**. To use your own password, copy `local/.env.example` to `local/.env` (git-ignored) before the first `docker compose up`. Grafana only reads it when its data volume is created. To change the password later, run:

```sh
docker compose exec grafana grafana cli admin reset-admin-password '<new password>'
```

Recreating the containers (for example after editing `docker-compose.yml`) clears Loki, Prometheus and Tempo, so run the loader again afterwards. Grafana's own data, including the Assistant connection, lives in the `grafana-data` volume and survives.

**Dates.** The raw files are dated around one canonical incident day, Thursday 2026-10-08. The local stack accepts the full history, so it can keep the story's times of day:

```sh
python3 loader/load.py --target local --incident-date latest
```

`--incident-date` moves every date by whole weeks so the incident falls on the Thursday you name (`YYYY-MM-DD`), or with `latest` on the most recent Thursday whose data has all happened. Times of day and weekdays stay the story's own, so the blackout is at 15:02 UTC on a Thursday. You can also set it with `DJ_INCIDENT_DATE`. A date that isn't a Thursday is refused, unless you add `--any-weekday`. Set Grafana's time zone to UTC (the example dashboard already is) so the times on screen match the story's. Add `--no-shift` to keep the original 2026 dates instead.

Every signal carries the load's incident date as the resource attribute `case_run` (a label on the local stack's metrics). If you load the data into the same stack more than once, filter on `case_run` to see one load.

### Grafana Assistant on the local stack

The Grafana Assistant plugin (`grafana-assistant-app`) is preinstalled. Assistant still runs its AI backend in Grafana Cloud, so connect it once to a Grafana Cloud stack where Assistant is enabled. A free account works.

1. Sign in to <http://localhost:3000>.
2. Open **Administration > Plugins and data > Plugins > Grafana Assistant > Connection**, or go straight to <http://localhost:3000/plugins/grafana-assistant-app>.
3. Click **Connect to Grafana Cloud** and approve the connection.

Your telemetry stays in the local stack. Prompts and the query context Assistant needs are sent to Grafana Cloud, and usage counts against the connected stack. The connection is stored in the `grafana-data` Docker volume, so it survives restarts. `docker compose down -v` removes it.

Some Assistant features, such as Investigations, aren't available on self-managed Grafana. See the [self-managed Assistant docs](https://grafana.com/docs/grafana-cloud/machine-learning/assistant/self-managed/).

### Grafana MCP server on the local stack

The stack also runs the open-source [Grafana MCP server](https://github.com/grafana/mcp-grafana), so any MCP-capable AI agent (Claude Code, Cursor, Codex and others) can investigate the case through Grafana.

- **Endpoint:** `http://localhost:8000/mcp` (streamable HTTP), reachable only from this machine.
- **Read-only:** write tools are disabled, so agents can query Loki, Prometheus and Tempo, but can't change anything in Grafana.
- **Sign-in:** it uses the Grafana admin login from `local/.env`.
- **Usage statistics:** turned off.

Add it to Claude Code with:

```sh
claude mcp add --transport http grafana-local http://localhost:8000/mcp
```

For other clients, point an MCP "HTTP" or "streamable-http" server entry at the same URL. To require a bearer token, set `MCP_SERVER_TOKEN` in `local/.env`, run `docker compose up -d mcp-grafana`, and have the client send `Authorization: Bearer <token>`.

The data source UIDs are `loki`, `prometheus` and `tempo`.

In the local Tempo, TraceQL searches limited to a time range may not find the historical badge traces. A search without a time range (for example `curl 'localhost:3200/api/search?q={span.badge="hale_r"}'`) or opening a trace by ID works. Every door-event log line in Loki carries its trace's `trace_id`.

## Loader options

```
--target cloud|local     where to send the data (required)
--signals logs,metrics,traces
--incident-date DATE     move by whole weeks so the incident falls on this Thursday, or 'latest' (env DJ_INCIDENT_DATE)
--any-weekday            allow an --incident-date that isn't a Thursday
--no-shift               keep original timestamps (local only)
--incident-end ISO       pin the time that 2026-10-08T15:50:00Z maps to (default: now)
--dry-run                build and validate every payload without sending
```

## Investigating

Start with `CASE-BRIEF.md`, then go where the data takes you. Some things worth knowing:
- Several devices lost clock sync during the outage, and their records say so.
- Data recorded during the outage arrived late.
- Not everyone on the Sleep Floor remembers what their body did.
