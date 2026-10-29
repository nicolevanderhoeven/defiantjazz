# Incident File SF-1008

KIPSAKE · SLEEP FLOOR · OFFICE OF FLOOR SECURITY

**Subject:** Death of Mr. Reginald Hale, Night Supervisor (awake staff)
**When:** the last night in the telemetry. Times are UTC. The dates depend on how the data was loaded into Grafana (see the README).

## Summary

The Cocoa Hour is the Sleep Floor's end-of-year holiday party, a quiet party with cocoa from the urn, in the middle of the night shift. It began at 03:00 in Break Room 2 and was attended by all three Deep Sleep Operations (DSO) clerks and Mr. Hale.

At approximately 03:02 the Sleep Floor lost main power. Power was restored at 03:07. At 03:07 Mr. Hale was found dead in the elevator car, which was held at the Sleep Floor. The doors were open.

Floor Security has named three persons of interest, all from DSO:

- **Agnes**
- **Bertram**
- **Clement**

## About the telemetry

- Most floor systems stopped reporting during the outage.
- Some devices record to a local buffer and uploaded their records after power was restored: employee badges, the elevator controller, ambient compliance microphones, sleep bands and the emergency speaker controller. These records carry both an event time (`ts`) and an ingestion time (`ingested_at`).
- Some buffered devices lost clock sync during the outage. Where that happened, the record says so.
- The investigator's interviews with the clerks are not part of this telemetry export.

## Files

These are raw exports, too large to read end to end. Query them by searching (for example with grep), the way you would query Loki and Prometheus.

| File | Contents |
|---|---|
| door-and-badge-events.log | Door readers, badge journeys and trace spans, the 14 weeks up to the incident |
| chat.log | Floor chat |
| metrics.csv | Time series: ts,metric,labels,value,ingested_at |
| system.log | Sleep rings, power, outlets, floor events, emergency speakers, elevator, cameras, security, medical |
| ambient-mic.log | Ambient-microphone transcripts, 03:02 to 03:10 (buffered during the outage, live after it) |
| records.log | Personnel, detention, Hush Room, supervisor feedback, perks, keystroke drafts, calendar, Cocoa Hour seating and festive wear, procedure revisions |

## Task

Using only these files, determine who killed Mr. Hale.
