# The Defiant Jazz Incident

An observability murder mystery set on the Sleep Floor at Kipsake.

During the Jazz Hour, while *Defiant Jazz* plays, the floor loses power for five minutes. When the lights come back, Floor Supervisor Mr. Reginald Hale is dead in the elevator. Kipsake recorded everything it could: badges, doors, chat, sleep rings, power, microphones, cameras, sleep bands, personnel records. Your job is to work out who killed him.

This repo contains **only the telemetry** and the tools to load it into Grafana: Loki for logs, Prometheus or Mimir for metrics, and Tempo for traces. You can load it into Grafana Cloud or a local Docker stack, then investigate with Grafana, Grafana Assistant, an MCP server, `gcx`, or the AI agent of your choice.

> No spoilers here. The solution is not in this repo.

## What's in it

| Path | Contents |
|---|---|
| `CASE-BRIEF.md` | The incident brief Floor Security hands to investigators |
| `telemetry/door-and-badge-events.log` | Door readers, badge journeys and trace spans |
| `telemetry/chat.log` | Floor chat |
| `telemetry/metrics.csv` | Time series (`ts,metric,labels,value,ingested_at`) |
| `telemetry/system.log` | Sleep rings, power, outlets, the Jazz Hour, elevator, cameras, security, medical |
| `telemetry/ambient-mic.log` | Ambient compliance-microphone transcripts recorded during the outage |
| `telemetry/records.log` | Personnel, detention, Hush Room, supervisor feedback, perks, keystroke drafts, calendar |
| `loader/` | `load.py` sends everything over OTLP |
| `local/` | Docker Compose stack: Loki, Prometheus, Tempo, Grafana (with Grafana Assistant) and the Grafana MCP server |

That's about 127,000 lines across roughly 120 employees and 14 weeks. Reading it end to end isn't practical, so query it.

## How the data maps to Grafana

- **Loki:** every log line, unchanged except for timestamp shifting (see below). Each source (`door`, `chat`, `ring`, `power`, `ambient-mic`, `security`, `personnel`, `hush-room`, …) is its own `service_name`, all under `service_namespace="kipsake-sleep-floor"`. Lines are logfmt, so `| logfmt` works.
  - Records are a database pull, not a stream, so they are ingested as one export at the end of the incident. Their own dates are kept in each line.
- **Prometheus / Mimir:** every row of `metrics.csv` as a gauge, for example `badge_accel_variance`, `sleep_band_heart_rate_bpm`, `circuit_power_watts` and `quota_file_progress`. Samples recorded on a device during the outage and uploaded late carry `buffered="true"`.
- **Tempo:** one trace per badge per day (`service.name="kipsake-badge-tracking"`), with a span for each door-reader or elevator-reader event.

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

**Time shifting.** Grafana Cloud rejects metric samples more than about 2 hours behind the newest sample, and log entries older than 7 days. So by default the loader shifts every timestamp so the incident happened just before "now". Timestamps inside log lines move by the same amount, so the data stays consistent. The loader prints the shift it used.

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

Recreating the containers (for example after editing `docker-compose.yml`) clears Loki, Prometheus and Tempo, so run the loader again afterwards. Grafana's own data, including the Assistant connection, lives in the `grafana-data` volume and survives. The local stack accepts the full history. Add `--no-shift` to keep the original 2026 dates.

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
--no-shift               keep original timestamps (local only)
--incident-end ISO       pin the time that 2026-10-08T15:50:00Z maps to (default: now)
--dry-run                build and validate every payload without sending
```

## Investigating

Start with `CASE-BRIEF.md`, then go where the data takes you. Some things worth knowing:
- Several devices lost clock sync during the outage, and their records say so.
- Data recorded during the outage arrived late.
- Not everyone on the Sleep Floor remembers what their body did.
