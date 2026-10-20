# Incident File SF-1008

KIPSAKE · SLEEP FLOOR · OFFICE OF FLOOR SECURITY

**Subject:** Death of Mr. Reginald Hale, Floor Supervisor (day staff)
**When:** the last day in the telemetry. Times are UTC. The dates depend on how the data was loaded into Grafana (see the README).

## Summary

At 14:58 the Deep Sleep Operations (DSO) department reached its quarterly quota and was awarded a Cocoa Hour, a quiet quota reward with cocoa from the urn. It began at 15:00 in Break Room 2 and was attended by all six DSO clerks and Mr. Hale.

At approximately 15:02 the Sleep Floor lost main power. Power was restored at 15:07. At 15:07 Mr. Hale was found dead in the elevator car, which was held at the Sleep Floor. The doors were open.

Floor Security has named three persons of interest, all from DSO:

- **Agnes K.**
- **Bertram L.**
- **Clement W.**

## About the telemetry

- Most floor systems stopped reporting during the outage.
- Some devices record to a local buffer and uploaded their records after power was restored: employee badges, the elevator controller, ambient compliance microphones, sleep bands and the emergency speaker controller. These records carry both an event time (`ts`) and an ingestion time (`ingested_at`).
- Some buffered devices lost clock sync during the outage. Where that happened, the record says so.
- Security interview transcripts are held by Floor Security and are not part of this telemetry export.

## Files

These are raw exports, too large to read end to end. Query them by searching (for example with grep), the way you would query Loki and Prometheus.

| File | Contents |
|---|---|
| door-and-badge-events.log | Door readers, badge journeys and trace spans, the 14 weeks up to the incident |
| chat.log | Floor chat |
| metrics.csv | Time series: ts,metric,labels,value,ingested_at |
| system.log | Sleep rings, power, outlets, quota rewards, emergency speakers, elevator, cameras, security, medical |
| ambient-mic.log | Ambient-microphone transcripts, 15:02 to 15:10 (buffered during the outage, live after it) |
| records.log | Personnel, detention, Hush Room, supervisor feedback, perks, keystroke drafts, calendar |

## Task

Using only these files, determine who killed Mr. Hale.
