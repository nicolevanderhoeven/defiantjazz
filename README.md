# The Defiant Jazz Incident

An observability murder mystery set on the Sleep Floor at Kipsake.

Kipsake rents your sleep: at night its Dreamers sleep in pods while their sleepwalking selves work the floor. During the Cocoa Hour, the floor's middle-of-the-night holiday party in Break Room 2, the floor loses power for five minutes. When the power comes back, the night supervisor, Mr. Reginald Hale, is dead in the elevator. Kipsake recorded everything it could: badges, doors, chat, sleep rings, power, microphones, cameras, sleep bands, personnel records. Your job is to work out who killed him.

This repo contains the telemetry and the tools to load it into Grafana: Loki for logs, Prometheus or Mimir for metrics, and Tempo for traces. You can load it into Grafana Cloud or a local Docker stack, then investigate with Grafana, Grafana Assistant, the [Grafana MCP server](https://gra.fan/mcprepo), [`gcx`](https://gra.fan/gcxrepo), or the AI agent of your choice. It also has the game itself, in a terminal version for demos and playtests and a web version to embed in a Grafana dashboard.

> [!WARNING]
> **Spoilers live in `game/SPOILERS-content/`, `game/test_SPOILERS_game.py`, `web/SPOILERS-content.js` and, once you build it, `web/dist/SPOILERS-defiantjazz.page.json`.** The folder holds the human-only story clips and `SPOILERS-reveal.md`, which names the killer and explains the solution. The test names the killer too, and the web bundle and page file are built from that folder. Don't open them if you want to play.
>
> Everything else is safe to read: `CASE-BRIEF.md`, `telemetry/`, `loader/`, `local/` and `game/ai-evidence/` hold only what an investigator is given, never the solution. The rest of `web/` is spoiler-free too.

## Play it locally, fully open source

The whole game runs on your own machine, from open-source parts only: Loki, Prometheus, Tempo, Grafana, the Grafana MCP server and the game's web server, started together by Docker Compose. Nothing in it connects to Grafana Cloud. You bring your own AI agent (and its API key, if it needs one).

1. Clone this repository.
2. Start everything: `cd local && docker compose up -d`. The first start pulls the images and builds the small loader; the case is loaded within about two minutes (`docker compose ps -a` shows the `loader` as `Exited (0)`). You need Docker with Compose, and nothing else: no Python.
3. Connect your AI agent to the Grafana MCP server at `http://localhost:8000/mcp`, for example `claude mcp add --transport http grafana-local http://localhost:8000/mcp` (or use [`gcx`](#gcx-on-the-local-stack-cli-alternative)). Then open the game at <http://localhost:8080>.

The game shows example questions to give your agent, which investigates the case in Grafana at <http://localhost:3000>. Anyone on your machine can look around there without signing in. Sign in as `admin` / `admin` to change things. Every port is bound to `127.0.0.1`, so nothing is reachable from your network.

> [!WARNING]
> **Start your agent outside this repo's folder.** An agent with file access can read the spoiler files, and it doesn't need them: the MCP server gives it the telemetry. No MCP-capable agent? Paste [`game/ai-evidence/case-bundle.md`](game/ai-evidence/case-bundle.md) into any chatbot instead, with nothing to install.

`docker compose down` stops the stack and keeps the case, and `docker compose down -v` also wipes it (the next `up` loads it again). [Loading into a local stack](#loading-into-a-local-stack) has the details, including moving a port that's already taken.

**One optional exception, off unless you turn it on:** at the end, the game can offer to add your score to the public leaderboard. Nothing is sent unless you click that button, and it only shows once a collector address is set in `local/.env` (`DJ_LEADERBOARD_URL`, see [`local/.env.example`](local/.env.example)). It sends your score, the points for each question, your chosen name and a random player id, never your answers, and the leaderboard marks it "played locally". Until a collector is set, nothing in the stack talks to Grafana Cloud.

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
  # A local model with Ollama: set its context length to 32k or more first (see game/README.md)
  python3 game/play.py --ai-cmd 'ollama run --hidethinking --nowordwrap llama3.2:3b'
  ```

- **No AI:** `--no-ai`.

> [!WARNING]
> **Don't run your own agent inside this repo's folder.** An agent with file access can read the spoiler files. Give it only `game/ai-evidence/case-bundle.md`, or have it investigate through Grafana with the [Grafana MCP server](#grafana-mcp-server-on-the-local-stack).

### In the browser or a Grafana dashboard

The same game as a static web page, made to embed in a Grafana dashboard panel next to the telemetry. There's no AI inside it: players ask Grafana Assistant, or their own agent through the [Grafana MCP server](https://gra.fan/mcprepo) or [`gcx`](https://gra.fan/gcxrepo), and the page offers example questions to copy. To play it locally:

```sh
python3 -m http.server 8080 --bind 127.0.0.1 --directory web
```

Then open <http://localhost:8080/>. The [local stack](#play-it-locally-fully-open-source) serves the same page itself, in a local mode that points at your own AI agent instead of Grafana Assistant (add `?local` to the address to see that mode from any static server). [`web/README.md`](web/README.md) covers embedding it in a dashboard with the example dashboard, and building it as a Grafana Page with Grafana Assistant beside it. It has no spoilers.

> [!WARNING]
> **`web/SPOILERS-content.js` contains spoilers.** It's built from `game/SPOILERS-content/` and includes the solution, so don't open it if you want to play.

## What's in it

| Path | Contents |
|---|---|
| `CASE-BRIEF.md` | The incident brief Floor Security hands to investigators |
| `game/` | The terminal game. **`game/SPOILERS-content/` and `game/test_SPOILERS_game.py` contain spoilers.** |
| `web/` | The web version, for a browser, a Grafana dashboard panel or a Grafana Page. **`web/SPOILERS-content.js` and `web/dist/` contain spoilers.** |
| `telemetry/door-and-badge-events.log` | Door readers, badge journeys and trace spans |
| `telemetry/chat.log` | Floor chat |
| `telemetry/metrics.csv` | Time series (`ts,metric,labels,value,ingested_at`) |
| `telemetry/system.log` | Sleep rings, power, outlets, floor events, seat sensors, emergency speakers, elevator, cameras, security, medical |
| `telemetry/ambient-mic.log` | Ambient compliance-microphone transcripts, 03:02 to 03:10 (buffered during the outage, live after it) |
| `telemetry/records.log` | Personnel, detention, Hush Room, supervisor feedback, perks, keystroke drafts, calendar, Cocoa Hour seats and festive wear, procedure revisions |
| `loader/` | `load.py` sends everything over OTLP; `test_load.py` checks its time shift |
| `local/` | The open-source Docker Compose stack: Loki, Prometheus, Tempo, Grafana, the Grafana MCP server, a loader that loads the case and the game's web server. Grafana Assistant is an optional profile |

That's about 4,300 lines across the four people on the Sleep Floor's night shift and 14 weeks of nights. Query it rather than reading it end to end.

## How the data maps to Grafana

- **Loki:** every log line, unchanged except for timestamp shifting (see below). Each source (`door`, `chat`, `ring`, `power`, `ambient-mic`, `security`, `personnel`, `hush-room`, …) is its own `service_name`, all under `service_namespace="kipsake-sleep-floor"`. Lines are logfmt, so `| logfmt` works.
  - Records are a database pull, not a stream, so they are ingested as one export at the end of the incident. Their own dates are kept in each line.
- **Prometheus / Mimir:** every row of `metrics.csv` as a gauge, for example `badge_accel_variance`, `sleep_band_heart_rate_bpm`, `circuit_power_watts` and `quota_file_progress`. Samples recorded on a device during the outage and uploaded late carry `buffered="true"`.
- **Tempo:** one trace per badge per night shift (`service.name="kipsake-badge-tracking"`), with a span for each door-reader or elevator-reader event. A night shift crosses midnight, so journeys are grouped by the data's own shift, and neither midnight nor a time shift splits one.

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

**Time shifting.** Grafana Cloud rejects metric samples more than about 2 hours behind the newest sample, and log lines more than 7 days old. So by default the loader shifts every timestamp so the incident happened just before "now". Timestamps inside log lines move by the same amount, so the data stays consistent. This moves the times of day too: the story's 03:02 lands at whatever time you loaded it. The loader prints the mode and the shift it used.

Because of those limits, Grafana Cloud gets:
- the last 7 days of logs (less one hour), which includes the whole incident, every record and the earlier nights
- the last 2 hours of metrics, which includes the whole incident window
- the last 7 days of traces, so the badge journeys of earlier nights are there too

Older history is skipped, and the loader reports how much. To see the full 14 weeks, use the local stack.

**Logs in Grafana Cloud.** Cloud Loki rejects log lines more than 7 days old, so the loader sends just under 7 days of logs. Lines from the last few hours are queryable straight away. Older lines are stored too, but they only show up in queries a few hours after loading, once Loki flushes them to storage. Until then a query for the earlier nights finds nothing, and Loki can keep serving that empty answer from its cache, so change the query slightly to see fresh results. To send less, use `--cloud-log-hours HOURS` or set `DJ_CLOUD_LOG_HOURS` in `loader/.env`.

To find out what was really stored, set the optional `GRAFANA_LOKI_URL`, `GRAFANA_LOKI_USER` and `GRAFANA_LOKI_READ_TOKEN` (a token with `logs:read`) in `loader/.env`; see `loader/.env.example`. After loading, the loader then counts this load's lines from the last 2 hours in Loki (by `service_namespace` and `case_run`), retrying briefly while they're ingested, and warns if fewer were stored than sent. Older lines can't be counted yet, because they aren't queryable until Loki flushes them. Without those settings it skips the check and says so.

**Traces in Grafana Cloud.** The badge-journey traces can be opened by trace ID right away. Because their timestamps are hours or days old, they can take up to about an hour after loading to show up in TraceQL search. Every door-event log line also carries its journey's `trace_id`, so in Loki you can jump from a door event to its trace.

**Pinning a load.** After every load, Cloud or local, the loader prints the incident night's absolute time window and the load's `case_run`, with links to the example dashboard and to Explore pinned to both. Set `GRAFANA_URL` in `loader/.env` to your stack's URL (for example `https://<your-stack>.grafana.net`) so the Cloud links are ready to open. The example dashboard's **Load (case_run)** drop-down lists the loads in its time range, newest first, and every panel shows only that load. Open the pinned dashboard link and save the dashboard with that time range, and the same load stays playable for as long as the stack keeps its data: about 30 days in Grafana Cloud (logs 31 days, traces 30 days, metrics 13 months).

**Before a demo.** Load once, at least about 1.5 hours before the session, so the earlier nights' logs have flushed and show up in queries. Then use the printed links, or pin the dashboard to the printed window and `case_run`. Reload only when the story data changes or the 30 days are nearly up. There's no need to reload on a schedule: only a relative time range such as "last 6 hours" goes stale, not the data.

**macOS note.** If the loader fails with `CERTIFICATE_VERIFY_FAILED`, install the requirements, which include `certifi`. The python.org build of Python doesn't use the system certificate store.

## Loading into a local stack

```sh
cd local && docker compose up -d
```

That starts Loki 3.7, Prometheus 3, Tempo 2, Grafana 13.3, the Grafana MCP server and the game, and a one-shot `loader` loads the case into the three stores (with `--incident-date latest`, so you get the full 14 weeks of history) and exits. It waits for the stores to be ready, and it skips any signal that's already loaded, so repeating `up` is safe. Watch it with `docker compose logs -f loader`.

| What | Where |
|---|---|
| The game | <http://localhost:8080> |
| Grafana (Viewer without signing in, `admin` / `admin` to change things) | <http://localhost:3000> |
| Grafana MCP server (read-only) | <http://localhost:8000/mcp> |
| Loki, Prometheus, Tempo | `localhost:3100`, `localhost:9090`, `localhost:3200` (and OTLP on `4318`) |

Every port is bound to `127.0.0.1`, so nothing is reachable from your network. If a port is already in use on your machine, move it in `local/.env` (copy [`local/.env.example`](local/.env.example)) with `DJ_GAME_PORT`, `DJ_GRAFANA_PORT`, `DJ_MCP_PORT`, `DJ_LOKI_PORT`, `DJ_PROMETHEUS_PORT`, `DJ_TEMPO_PORT` or `DJ_OTLP_PORT`. The game and its links follow, but the home dashboard's text assumes the default ports.

Grafana's home dashboard, **Kipsake Sleep Floor**, links to the game, the MCP endpoint and the data sources (`loki`, `prometheus` and `tempo`, already provisioned), so <http://localhost:3000> explains itself.

**Nothing phones home.** Grafana's usage reports, update checks and news feed are off, so are Loki's and Tempo's usage reports and the MCP server's usage statistics, and Grafana doesn't download any plugins on start-up. The default stack never calls Grafana Cloud.

**Sign-in:** anyone on your machine gets the Viewer role without signing in, which is enough to use Explore. The admin login is **admin / admin**. To use your own password, copy `local/.env.example` to `local/.env` (git-ignored) before the first `docker compose up`. Grafana only reads it when its data volume is created. To change the password later, run:

```sh
docker compose exec grafana grafana cli admin reset-admin-password '<new password>'
```

**Restarting.** Loki, Prometheus, Tempo and Grafana keep their data in Docker volumes. `docker compose down` followed by `docker compose up -d` keeps the case, and the loader notices it's there and does nothing. `docker compose down -v` deletes the volumes, and the next `up` loads the case again from scratch. If the data is gone but the volumes aren't (for example after you removed only one of them), the loader loads whichever signals are missing.

**Loading by hand.** To load the case again, or into a different stack, run the loader from the host. It needs Python 3 and the loader's two dependencies, and the stack's OTLP ports:

```sh
python3 -m pip install -r loader/requirements.txt
python3 loader/load.py --target local
```

If you load the same stack more than once, filter on `case_run` to see one load.

**Dates.** The raw files are dated around one canonical incident night: the blackout is at 03:02 on Thursday 2026-10-08. The local stack accepts the full history, so it can keep the story's times of day:

```sh
python3 loader/load.py --target local --incident-date latest
```

`--incident-date` moves every date by whole weeks so the incident falls on the Thursday you name (`YYYY-MM-DD`), or with `latest` on the most recent Thursday whose data has all happened. Times of day and weekdays stay the story's own, so the blackout is at 03:02 UTC on a Thursday. You can also set it with `DJ_INCIDENT_DATE`. A date that isn't a Thursday is refused, unless you add `--any-weekday`. Set Grafana's time zone to UTC (the home dashboard already is) so the times on screen match the story's. Add `--no-shift` to keep the original 2026 dates instead.

Every signal carries the load's incident date as the resource attribute `case_run` (a label on the local stack's metrics).

### Optional: Grafana Assistant (needs Grafana Cloud)

Everything above is open source and works without Grafana Cloud. Grafana Assistant is the one part that doesn't: it runs its AI backend in Grafana Cloud. If you want it anyway, start the optional `assistant` profile, which adds a second Grafana with the Assistant plugin installed at <http://localhost:3001> (the same data sources, a separate volume), and connect it once to a Grafana Cloud stack where Assistant is enabled. A free account works.

```sh
cd local && docker compose --profile assistant up -d
```

1. Sign in to <http://localhost:3001> as `admin` / `admin` (Assistant doesn't support anonymous access).
2. Open **Administration > Plugins and data > Plugins > Grafana Assistant > Connection**, or go straight to <http://localhost:3001/plugins/grafana-assistant-app>.
3. Click **Connect to Grafana Cloud** and approve the connection.

Your telemetry stays in the local stack. Prompts and the query context Assistant needs are sent to Grafana Cloud, and usage counts against the connected stack. The connection is stored in the `grafana-assistant-data` volume, so it survives restarts. `docker compose down -v` removes it. Move the port with `DJ_ASSISTANT_PORT`.

Some Assistant features, such as Investigations, aren't available on self-managed Grafana. See the [self-managed Assistant docs](https://grafana.com/docs/grafana-cloud/machine-learning/assistant/self-managed/).

### Grafana MCP server on the local stack

The stack also runs the open-source [Grafana MCP server](https://gra.fan/mcprepo), so any MCP-capable AI agent (Claude Code, Cursor, Codex and others) can investigate the case through Grafana.

- **Endpoint:** `http://localhost:8000/mcp` (streamable HTTP), reachable only from this machine.
- **Read-only:** write tools are disabled, so agents can query Loki, Prometheus and Tempo, but can't change anything in Grafana.
- **Sign-in:** it uses the Grafana admin login from `local/.env` (admin / admin by default) to read Grafana.
- **Usage statistics:** turned off.
- **Port:** `8000`, or `DJ_MCP_PORT`.

Start your agent outside this repo's folder, so it can't read the spoiler files. Add the server to Claude Code with:

```sh
claude mcp add --transport http grafana-local http://localhost:8000/mcp
```

For other clients, point an MCP "HTTP" or "streamable-http" server entry at the same URL. To require a bearer token, set `MCP_SERVER_TOKEN` in `local/.env`, run `docker compose up -d mcp-grafana`, and have the client send `Authorization: Bearer <token>`.

The data source UIDs are `loki`, `prometheus` and `tempo`.

In the local Tempo, TraceQL searches limited to a time range may not find the historical badge traces. A search without a time range (for example `curl 'localhost:3200/api/search?q={span.badge="hale_r"}'`) or opening a trace by ID works. Every door-event log line in Loki carries its trace's `trace_id`.

### gcx on the local stack (CLI alternative)

The Grafana MCP server above is the main way to connect an agent. Use [`gcx`](https://gra.fan/gcxrepo) instead if your agent has no MCP support, or you prefer a command line. It talks to the local Grafana directly, with a service-account token. A Viewer token is enough.

> **Don't run a shell-capable agent inside this repo's folder.** It can read the spoiler files. Start it somewhere else, and give it only `gcx` and the commands below.

1. In Grafana (<http://localhost:3000>), open **Administration > Users and access > Service accounts**, add a service account with the **Viewer** role, and add a token to it. Copy the token.
2. Log gcx in to the local stack:

   ```sh
   gcx login dj-local --server http://localhost:3000 --token <token>
   ```

3. Check it can see the data sources (`loki`, `prometheus` and `tempo`):

   ```sh
   gcx datasources list
   ```

Then ask your agent to investigate with commands like these. Pass the data source UID with `-d`:

```sh
# Logs (LogQL)
gcx logs query -d loki '{service_namespace="kipsake-sleep-floor"} |= "hale"' --since 24h --limit 20 -o raw

# Log counts (a metric query over logs uses `gcx logs metrics`)
gcx logs metrics -d loki 'sum(count_over_time({service_namespace="kipsake-sleep-floor"}[1h]))' --since 24h --step 1h

# Metrics (PromQL)
gcx metrics query -d prometheus 'max(sleep_band_heart_rate_bpm{service_namespace="kipsake-sleep-floor"})' --since 24h --step 1m

# Traces (TraceQL). Leave out --since: a time range may not find the historical badge traces
gcx traces query -d tempo '{ span.badge = "hale" }' --limit 5
gcx traces get -d tempo <trace id>
```

Commands for Grafana Cloud products, such as `gcx assistant` and SLOs, don't work against a local stack. Everything above does.

## Loader options

```
--target cloud|local     where to send the data (required)
--signals logs,metrics,traces
--incident-date DATE     move by whole weeks so the incident falls on this Thursday, or 'latest' (env DJ_INCIDENT_DATE)
--any-weekday            allow an --incident-date that isn't a Thursday
--no-shift               keep original timestamps (local only)
--incident-end ISO       pin the time that 2026-10-08T03:50:00Z maps to (default: now)
--cloud-log-hours HOURS  cloud only: hours of logs to send (default 167; env DJ_CLOUD_LOG_HOURS)
--dry-run                build and validate every payload without sending
--wait SECONDS           local only: wait up to this long for Loki, Prometheus and Tempo to be ready
--skip-if-loaded         local only: skip each signal that already has this case's data (case_run is set)
```

## Investigating

Start with `CASE-BRIEF.md`, then go where the data takes you. Some things worth knowing:
- Several devices lost clock sync during the outage, and their records say so.
- Data recorded during the outage arrived late.
- Not everyone on the Sleep Floor remembers what their body did.
