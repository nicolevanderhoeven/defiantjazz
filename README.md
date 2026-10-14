# The Defiant Jazz Incident

An observability murder mystery set on a severed floor at Lumon Industries.

During a Defiant Jazz Music Dance Experience, the floor loses power for five minutes. When the lights come back, Floor Supervisor Mr. Reginald Hale is dead in the elevator. Lumon recorded everything it could: badges, doors, chat, chips, power, microphones, cameras, wellness bands, personnel records. Your job is to work out who killed him.

This repo contains **only the telemetry** and the tools to load it into Grafana: Loki for logs, Prometheus or Mimir for metrics, and Tempo for traces. You can load it into Grafana Cloud or a local Docker stack, then investigate with Grafana, Grafana Assistant, an MCP server, `gcx`, or the AI agent of your choice.

> No spoilers here. The solution is not in this repo.

## What's in it

| Path | Contents |
|---|---|
| `CASE-BRIEF.md` | The incident brief Floor Security hands to investigators |
| `telemetry/door-and-badge-events.log` | Door readers, badge journeys and trace spans |
| `telemetry/chat.log` | Floor chat |
| `telemetry/metrics.csv` | Time series (`ts,metric,labels,value,ingested_at`) |
| `telemetry/system.log` | Severance chips, power, outlets, the MDE, elevator, cameras, security, medical |
| `telemetry/ambient-mic.log` | Ambient compliance-microphone transcripts recorded during the outage |
| `telemetry/records.log` | Personnel, Break Room, wellness, supervisor feedback, perks, keystroke drafts, calendar |
| `loader/` | `load.py` sends everything over OTLP |
| `local/` | Docker Compose stack: Loki, Prometheus, Tempo, Grafana |

That's about 127,000 lines across roughly 120 employees and 14 weeks. Reading it end to end isn't practical, so query it.

## How the data maps to Grafana

- **Loki:** every log line, unchanged except for timestamp shifting (see below). Each source (`door`, `chat`, `chip`, `power`, `ambient-mic`, `security`, `personnel`, `wellness`, …) is its own `service_name`, all under `service_namespace="lumon-severed-floor"`. Lines are logfmt, so `| logfmt` works.
  - Records are a database pull, not a stream, so they are ingested as one export at the end of the incident. Their own dates are kept in each line.
- **Prometheus / Mimir:** every row of `metrics.csv` as a gauge, for example `badge_accel_variance`, `wellness_band_heart_rate_bpm`, `circuit_power_watts` and `quota_file_progress`. Samples recorded on a device during the outage and uploaded late carry `buffered="true"`.
- **Tempo:** one trace per badge per day (`service.name="lumon-badge-tracking"`), with a span for each door-reader or elevator-reader event.

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

**Traces in Grafana Cloud.** Grafana Cloud Traces stores the badge-journey traces, and you can open any of them by trace ID. It doesn't index spans with old timestamps for TraceQL search, though, and these spans are hours or days old by the time they're loaded. Every door-event log line carries its journey's `trace_id`, so in Loki you can jump from a door event to its trace.

**macOS note.** If the loader fails with `CERTIFICATE_VERIFY_FAILED`, install the requirements, which include `certifi`. The python.org build of Python doesn't use the system certificate store.

## Loading into a local stack

```sh
cd local && docker compose up -d && cd ..
python3 -m pip install -r loader/requirements.txt
python3 loader/load.py --target local
```

Grafana runs at <http://localhost:3000> with no login, and the Loki, Prometheus and Tempo data sources are already provisioned. The local stack accepts the full history. Add `--no-shift` to keep the original 2026 dates.

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
- Not everyone on a severed floor remembers what their body did.
