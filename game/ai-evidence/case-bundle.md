# Incident File SF-1008

KIPSAKE · SLEEP FLOOR · OFFICE OF FLOOR SECURITY

**Subject:** Death of Mr. Reginald Hale, Floor Supervisor (day staff)
**Date:** 2026-10-08

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

| File | Contents |
|---|---|
| 02-badge-and-door-events.md | Door readers and badge journeys, 2026-09-24 to 2026-10-08 |
| 03-chat.md | Floor chat, 2026-09-24 to 2026-10-08 |
| 04-metrics.md | Selected time series (CSV) |
| 05-system-logs.md | Sleep rings, power, outlets, quota rewards, emergency speakers, elevator, cameras, security, medical |
| 06-ambient-mic-transcripts.md | Ambient-microphone transcripts, 15:02 to 15:10 (buffered during the outage, live after it) |
| 07-records.md | Personnel, detention, Hush Room notes, supervisor feedback, perks, keystroke drafts, calendar |

## Task

Using only these files, determine who killed Mr. Hale.


---

# Badge and Door Events (2026-09-24 to 2026-10-08)

Door-reader events for the elevator lobby, office zones, break rooms, Supply Room B and the supervisor's office, plus incident-day trace spans. `elevator-reader` is the badge proximity reader inside the elevator car, which runs on the elevator UPS.

```text
2026-09-24T08:44:19 source=door reader=elevator-lobby badge=hale_r dir=in
2026-09-24T08:52:40 source=door reader=hush-room badge=pruitt_d dir=in
2026-09-24T08:53:08 source=door reader=supervisor-office badge=hale_r dir=in
2026-09-24T08:56:05 source=door reader=elevator-lobby badge=dorothy_p dir=in
2026-09-24T08:56:25 source=door reader=elevator-lobby badge=ursula_x dir=in
2026-09-24T08:56:30 source=door reader=elevator-lobby badge=lorna_b dir=in
2026-09-24T08:56:59 source=door reader=dso-office badge=dorothy_p dir=in
2026-09-24T08:57:04 source=door reader=tc-office badge=lorna_b dir=in
2026-09-24T08:57:06 source=door reader=fold badge=ursula_x dir=in
2026-09-24T08:58:15 source=door reader=elevator-lobby badge=otto_g dir=in
2026-09-24T08:58:37 source=door reader=as-office badge=otto_g dir=in
2026-09-24T08:59:04 source=door reader=elevator-lobby badge=ivo_t dir=in
2026-09-24T08:59:12 source=door reader=elevator-lobby badge=fern_o dir=in
2026-09-24T08:59:15 source=door reader=elevator-lobby badge=silas_q dir=in
2026-09-24T08:59:21 source=door reader=elevator-lobby badge=winifred_e dir=in
2026-09-24T08:59:30 source=door reader=elevator-lobby badge=rosalind_n dir=in
2026-09-24T08:59:41 source=door reader=fold badge=winifred_e dir=in
2026-09-24T08:59:42 source=door reader=elevator-lobby badge=tobias_u dir=in
2026-09-24T08:59:44 source=door reader=elevator-lobby badge=harriet_s dir=in
2026-09-24T08:59:48 source=door reader=fold badge=silas_q dir=in
2026-09-24T08:59:53 source=door reader=tc-office badge=ivo_t dir=in
2026-09-24T08:59:54 source=door reader=dso-office badge=fern_o dir=in
2026-09-24T08:59:55 source=door reader=as-office badge=rosalind_n dir=in
2026-09-24T09:00:08 source=door reader=elevator-lobby badge=milo_d dir=in
2026-09-24T09:00:13 source=door reader=elevator-lobby badge=prudence_h dir=in
2026-09-24T09:00:13 source=door reader=elevator-lobby badge=vernon_z dir=in
2026-09-24T09:00:21 source=door reader=elevator-lobby badge=cyril_a dir=in
2026-09-24T09:00:26 source=door reader=elevator-lobby badge=agnes_k dir=in
2026-09-24T09:00:32 source=door reader=tc-office badge=harriet_s dir=in
2026-09-24T09:00:34 source=door reader=elevator-lobby badge=eustace_m dir=in
2026-09-24T09:00:36 source=door reader=fold badge=tobias_u dir=in
2026-09-24T09:00:37 source=door reader=elevator-lobby badge=kenneth_y dir=in
2026-09-24T09:00:48 source=door reader=fold badge=vernon_z dir=in
2026-09-24T09:00:56 source=door reader=dso-office badge=eustace_m dir=in
2026-09-24T09:00:59 source=door reader=as-office badge=milo_d dir=in
2026-09-24T09:01:00 source=door reader=as-office badge=prudence_h dir=in
2026-09-24T09:01:08 source=door reader=fold badge=cyril_a dir=in
2026-09-24T09:01:14 source=door reader=dso-office badge=agnes_k dir=in
2026-09-24T09:01:29 source=door reader=tc-office badge=kenneth_y dir=in
2026-09-24T09:01:48 source=door reader=elevator-lobby badge=quentin_j dir=in
2026-09-24T09:02:02 source=door reader=elevator-lobby badge=bertram_l dir=in
2026-09-24T09:02:13 source=door reader=elevator-lobby badge=nadia_f dir=in
2026-09-24T09:02:14 source=door reader=as-office badge=quentin_j dir=in
2026-09-24T09:02:28 source=door reader=dso-office badge=bertram_l dir=in
2026-09-24T09:02:40 source=door reader=as-office badge=nadia_f dir=in
2026-09-24T09:02:41 source=door reader=elevator-lobby badge=gideon_r dir=in
2026-09-24T09:03:15 source=door reader=tc-office badge=gideon_r dir=in
2026-09-24T09:03:18 source=door reader=elevator-lobby badge=judith_v dir=in
2026-09-24T09:03:27 source=door reader=elevator-lobby badge=clement_w dir=in
2026-09-24T09:04:01 source=door reader=tc-office badge=judith_v dir=in
2026-09-24T09:04:24 source=door reader=dso-office badge=clement_w dir=in
2026-09-24T09:53:01 source=door reader=supply-room-b badge=milo_d dir=in
2026-09-24T10:26:31 source=door reader=supply-room-b badge=eustace_m dir=in
2026-09-24T10:39:28 source=door reader=supply-room-b badge=harriet_s dir=in
2026-09-24T10:48:23 source=door reader=supply-room-b badge=rosalind_n dir=in
2026-09-24T11:35:37 source=door reader=supply-room-b badge=gideon_r dir=in
2026-09-24T11:38:52 source=door reader=supply-room-b badge=cyril_a dir=in
2026-09-24T11:49:11 source=door reader=supervisor-office badge=bertram_l dir=in
2026-09-24T12:01:31 source=door reader=break-room-1 badge=rosalind_n dir=in
2026-09-24T12:03:26 source=door reader=break-room-1 badge=bertram_l dir=in
2026-09-24T12:05:49 source=door reader=break-room-1 badge=otto_g dir=in
2026-09-24T12:06:37 source=door reader=break-room-1 badge=cyril_a dir=in
2026-09-24T12:06:56 source=door reader=break-room-1 badge=nadia_f dir=in
2026-09-24T12:07:20 source=door reader=break-room-1 badge=fern_o dir=in
2026-09-24T12:07:41 source=door reader=break-room-1 badge=clement_w dir=in
2026-09-24T12:09:37 source=door reader=break-room-1 badge=silas_q dir=in
2026-09-24T12:11:17 source=door reader=break-room-1 badge=quentin_j dir=in
2026-09-24T12:14:51 source=door reader=break-room-1 badge=eustace_m dir=in
2026-09-24T12:16:28 source=door reader=break-room-1 badge=kenneth_y dir=in
2026-09-24T12:17:04 source=door reader=break-room-1 badge=ursula_x dir=in
2026-09-24T12:20:28 source=door reader=break-room-1 badge=harriet_s dir=in
2026-09-24T12:21:35 source=door reader=supply-room-b badge=quentin_j dir=in
2026-09-24T12:22:22 source=door reader=break-room-1 badge=dorothy_p dir=in
2026-09-24T12:23:13 source=door reader=break-room-1 badge=agnes_k dir=in
2026-09-24T12:23:41 source=door reader=break-room-1 badge=prudence_h dir=in
2026-09-24T12:25:25 source=door reader=break-room-1 badge=gideon_r dir=in
2026-09-24T12:30:29 source=door reader=break-room-1 badge=winifred_e dir=in
2026-09-24T12:31:35 source=door reader=break-room-1 badge=milo_d dir=in
2026-09-24T12:34:06 source=door reader=break-room-1 badge=lorna_b dir=in
2026-09-24T12:34:28 source=door reader=break-room-1 badge=vernon_z dir=in
2026-09-24T12:38:17 source=door reader=break-room-1 badge=tobias_u dir=in
2026-09-24T12:38:29 source=door reader=break-room-1 badge=ivo_t dir=in
2026-09-24T12:39:22 source=door reader=break-room-1 badge=judith_v dir=in
2026-09-24T12:45:17 source=door reader=supply-room-b badge=judith_v dir=in
2026-09-24T13:14:23 source=door reader=supply-room-b badge=ivo_t dir=in
2026-09-24T13:36:33 source=door reader=supply-room-b badge=lorna_b dir=in
2026-09-24T13:54:58 source=door reader=supply-room-b badge=dorothy_p dir=in
2026-09-24T14:10:24 source=door reader=supply-room-b badge=otto_g dir=in
2026-09-24T14:13:31 source=door reader=supply-room-b badge=prudence_h dir=in
2026-09-24T17:00:07 source=door reader=elevator-lobby badge=rosalind_n dir=out
2026-09-24T17:00:24 source=door reader=elevator-lobby badge=judith_v dir=out
2026-09-24T17:00:41 source=door reader=elevator-lobby badge=agnes_k dir=out
2026-09-24T17:00:52 source=door reader=elevator-lobby badge=gideon_r dir=out
2026-09-24T17:01:12 source=door reader=elevator-lobby badge=bertram_l dir=out
2026-09-24T17:01:15 source=door reader=elevator-lobby badge=dorothy_p dir=out
2026-09-24T17:01:15 source=door reader=elevator-lobby badge=fern_o dir=out
2026-09-24T17:01:20 source=door reader=elevator-lobby badge=otto_g dir=out
2026-09-24T17:01:25 source=door reader=elevator-lobby badge=winifred_e dir=out
2026-09-24T17:01:50 source=door reader=elevator-lobby badge=quentin_j dir=out
2026-09-24T17:01:57 source=door reader=elevator-lobby badge=eustace_m dir=out
2026-09-24T17:02:03 source=door reader=elevator-lobby badge=ursula_x dir=out
2026-09-24T17:02:15 source=door reader=elevator-lobby badge=tobias_u dir=out
2026-09-24T17:02:28 source=door reader=elevator-lobby badge=prudence_h dir=out
2026-09-24T17:02:33 source=door reader=elevator-lobby badge=kenneth_y dir=out
2026-09-24T17:02:49 source=door reader=elevator-lobby badge=silas_q dir=out
2026-09-24T17:03:24 source=door reader=elevator-lobby badge=vernon_z dir=out
2026-09-24T17:03:45 source=door reader=elevator-lobby badge=harriet_s dir=out
2026-09-24T17:04:05 source=door reader=elevator-lobby badge=nadia_f dir=out
2026-09-24T17:05:37 source=door reader=elevator-lobby badge=ivo_t dir=out
2026-09-24T17:05:42 source=door reader=elevator-lobby badge=clement_w dir=out
2026-09-24T17:05:43 source=door reader=elevator-lobby badge=lorna_b dir=out
2026-09-24T17:05:53 source=door reader=elevator-lobby badge=milo_d dir=out
2026-09-24T17:05:55 source=door reader=elevator-lobby badge=cyril_a dir=out
2026-09-25T08:42:01 source=door reader=elevator-lobby badge=hale_r dir=in
2026-09-25T08:53:45 source=door reader=supervisor-office badge=hale_r dir=in
2026-09-25T08:54:59 source=door reader=hush-room badge=pruitt_d dir=in
2026-09-25T08:56:00 source=door reader=elevator-lobby badge=prudence_h dir=in
2026-09-25T08:56:07 source=door reader=elevator-lobby badge=quentin_j dir=in
2026-09-25T08:56:20 source=door reader=elevator-lobby badge=cyril_a dir=in
2026-09-25T08:56:26 source=door reader=as-office badge=prudence_h dir=in
2026-09-25T08:56:46 source=door reader=as-office badge=quentin_j dir=in
2026-09-25T08:57:05 source=door reader=fold badge=cyril_a dir=in
2026-09-25T08:57:29 source=door reader=elevator-lobby badge=fern_o dir=in
2026-09-25T08:58:06 source=door reader=dso-office badge=fern_o dir=in
2026-09-25T08:58:10 source=door reader=elevator-lobby badge=ursula_x dir=in
2026-09-25T08:58:23 source=door reader=elevator-lobby badge=lorna_b dir=in
2026-09-25T08:58:31 source=door reader=fold badge=ursula_x dir=in
2026-09-25T08:58:34 source=door reader=elevator-lobby badge=kenneth_y dir=in
2026-09-25T08:58:49 source=door reader=elevator-lobby badge=harriet_s dir=in
2026-09-25T08:58:53 source=door reader=elevator-lobby badge=tobias_u dir=in
2026-09-25T08:58:56 source=door reader=tc-office badge=kenneth_y dir=in
2026-09-25T08:59:01 source=door reader=tc-office badge=lorna_b dir=in
2026-09-25T08:59:15 source=door reader=elevator-lobby badge=gideon_r dir=in
2026-09-25T08:59:35 source=door reader=tc-office badge=harriet_s dir=in
2026-09-25T08:59:36 source=door reader=elevator-lobby badge=eustace_m dir=in
2026-09-25T08:59:39 source=door reader=elevator-lobby badge=rosalind_n dir=in
2026-09-25T08:59:41 source=door reader=fold badge=tobias_u dir=in
2026-09-25T09:00:07 source=door reader=as-office badge=rosalind_n dir=in
2026-09-25T09:00:07 source=door reader=elevator-lobby badge=silas_q dir=in
2026-09-25T09:00:13 source=door reader=tc-office badge=gideon_r dir=in
2026-09-25T09:00:14 source=door reader=dso-office badge=eustace_m dir=in
2026-09-25T09:00:17 source=door reader=elevator-lobby badge=otto_g dir=in
2026-09-25T09:00:22 source=door reader=elevator-lobby badge=milo_d dir=in
2026-09-25T09:00:42 source=door reader=fold badge=silas_q dir=in
2026-09-25T09:00:47 source=door reader=elevator-lobby badge=judith_v dir=in
2026-09-25T09:00:53 source=door reader=as-office badge=milo_d dir=in
2026-09-25T09:00:54 source=door reader=elevator-lobby badge=nadia_f dir=in
2026-09-25T09:01:10 source=door reader=as-office badge=otto_g dir=in
2026-09-25T09:01:15 source=door reader=elevator-lobby badge=ivo_t dir=in
2026-09-25T09:01:16 source=door reader=tc-office badge=judith_v dir=in
2026-09-25T09:01:18 source=door reader=as-office badge=nadia_f dir=in
2026-09-25T09:01:29 source=door reader=elevator-lobby badge=vernon_z dir=in
2026-09-25T09:01:53 source=door reader=elevator-lobby badge=bertram_l dir=in
2026-09-25T09:02:00 source=door reader=tc-office badge=ivo_t dir=in
2026-09-25T09:02:00 source=door reader=fold badge=vernon_z dir=in
2026-09-25T09:02:10 source=door reader=elevator-lobby badge=clement_w dir=in
2026-09-25T09:02:13 source=door reader=dso-office badge=bertram_l dir=in
2026-09-25T09:02:30 source=door reader=elevator-lobby badge=winifred_e dir=in
2026-09-25T09:02:35 source=door reader=dso-office badge=clement_w dir=in
2026-09-25T09:02:40 source=door reader=elevator-lobby badge=dorothy_p dir=in
2026-09-25T09:03:00 source=door reader=fold badge=winifred_e dir=in
2026-09-25T09:03:38 source=door reader=dso-office badge=dorothy_p dir=in
2026-09-25T09:03:48 source=door reader=elevator-lobby badge=agnes_k dir=in
2026-09-25T09:04:08 source=door reader=dso-office badge=agnes_k dir=in
2026-09-25T09:35:44 source=door reader=supply-room-b badge=nadia_f dir=in
2026-09-25T09:44:04 source=door reader=supply-room-b badge=gideon_r dir=in
2026-09-25T09:53:46 source=door reader=supply-room-b badge=prudence_h dir=in
2026-09-25T09:59:19 source=door reader=supply-room-b badge=rosalind_n dir=in
2026-09-25T10:02:25 source=door reader=supply-room-b badge=tobias_u dir=in
2026-09-25T10:03:22 source=door reader=supply-room-b badge=lorna_b dir=in
2026-09-25T10:18:09 source=door reader=supply-room-b badge=eustace_m dir=in
2026-09-25T10:20:28 source=door reader=supply-room-b badge=quentin_j dir=in
2026-09-25T10:47:53 source=door reader=supply-room-b badge=ivo_t dir=in
2026-09-25T11:10:46 source=door reader=supply-room-b badge=kenneth_y dir=in
2026-09-25T11:44:11 source=door reader=supply-room-b badge=ursula_x dir=in
2026-09-25T12:00:28 source=door reader=break-room-1 badge=clement_w dir=in
2026-09-25T12:01:13 source=door reader=break-room-1 badge=prudence_h dir=in
2026-09-25T12:03:17 source=door reader=break-room-1 badge=judith_v dir=in
2026-09-25T12:07:29 source=door reader=break-room-1 badge=tobias_u dir=in
2026-09-25T12:12:05 source=door reader=break-room-1 badge=winifred_e dir=in
2026-09-25T12:12:57 source=door reader=break-room-1 badge=nadia_f dir=in
2026-09-25T12:13:29 source=door reader=break-room-1 badge=ursula_x dir=in
2026-09-25T12:17:29 source=door reader=break-room-1 badge=lorna_b dir=in
2026-09-25T12:20:23 source=door reader=break-room-1 badge=otto_g dir=in
2026-09-25T12:23:21 source=door reader=break-room-1 badge=fern_o dir=in
2026-09-25T12:23:45 source=door reader=break-room-1 badge=dorothy_p dir=in
2026-09-25T12:24:45 source=door reader=break-room-1 badge=milo_d dir=in
2026-09-25T12:27:10 source=door reader=break-room-1 badge=quentin_j dir=in
2026-09-25T12:30:20 source=door reader=break-room-1 badge=eustace_m dir=in
2026-09-25T12:30:27 source=door reader=break-room-1 badge=gideon_r dir=in
2026-09-25T12:30:56 source=door reader=break-room-1 badge=silas_q dir=in
2026-09-25T12:31:11 source=door reader=break-room-1 badge=rosalind_n dir=in
2026-09-25T12:34:13 source=door reader=break-room-1 badge=kenneth_y dir=in
2026-09-25T12:34:45 source=door reader=break-room-1 badge=bertram_l dir=in
2026-09-25T12:34:47 source=door reader=break-room-1 badge=ivo_t dir=in
2026-09-25T12:35:36 source=door reader=break-room-1 badge=agnes_k dir=in
2026-09-25T12:36:35 source=door reader=break-room-1 badge=vernon_z dir=in
2026-09-25T12:37:41 source=door reader=break-room-1 badge=cyril_a dir=in
2026-09-25T12:37:55 source=door reader=break-room-1 badge=harriet_s dir=in
2026-09-25T13:21:14 source=door reader=supply-room-b badge=winifred_e dir=in
2026-09-25T13:36:15 source=door reader=supply-room-b badge=dorothy_p dir=in
2026-09-25T14:19:26 source=door reader=supply-room-b badge=cyril_a dir=in
2026-09-25T17:00:09 source=door reader=elevator-lobby badge=vernon_z dir=out
2026-09-25T17:00:17 source=door reader=elevator-lobby badge=ivo_t dir=out
2026-09-25T17:00:23 source=door reader=elevator-lobby badge=gideon_r dir=out
2026-09-25T17:00:53 source=door reader=elevator-lobby badge=rosalind_n dir=out
2026-09-25T17:00:54 source=door reader=elevator-lobby badge=harriet_s dir=out
2026-09-25T17:01:10 source=door reader=elevator-lobby badge=lorna_b dir=out
2026-09-25T17:01:15 source=door reader=elevator-lobby badge=bertram_l dir=out
2026-09-25T17:01:26 source=door reader=elevator-lobby badge=quentin_j dir=out
2026-09-25T17:01:32 source=door reader=elevator-lobby badge=eustace_m dir=out
2026-09-25T17:01:48 source=door reader=elevator-lobby badge=ursula_x dir=out
2026-09-25T17:02:06 source=door reader=elevator-lobby badge=nadia_f dir=out
2026-09-25T17:02:07 source=door reader=elevator-lobby badge=otto_g dir=out
2026-09-25T17:02:16 source=door reader=elevator-lobby badge=kenneth_y dir=out
2026-09-25T17:02:16 source=door reader=elevator-lobby badge=prudence_h dir=out
2026-09-25T17:02:51 source=door reader=elevator-lobby badge=agnes_k dir=out
2026-09-25T17:03:12 source=door reader=elevator-lobby badge=judith_v dir=out
2026-09-25T17:03:42 source=door reader=elevator-lobby badge=clement_w dir=out
2026-09-25T17:04:08 source=door reader=elevator-lobby badge=milo_d dir=out
2026-09-25T17:04:12 source=door reader=elevator-lobby badge=winifred_e dir=out
2026-09-25T17:05:02 source=door reader=elevator-lobby badge=cyril_a dir=out
2026-09-25T17:05:04 source=door reader=elevator-lobby badge=silas_q dir=out
2026-09-25T17:05:11 source=door reader=elevator-lobby badge=fern_o dir=out
2026-09-25T17:05:39 source=door reader=elevator-lobby badge=tobias_u dir=out
2026-09-25T17:05:47 source=door reader=elevator-lobby badge=dorothy_p dir=out
2026-09-28T08:44:31 source=door reader=elevator-lobby badge=hale_r dir=in
2026-09-28T08:45:27 source=door reader=supervisor-office badge=hale_r dir=in
2026-09-28T08:56:22 source=door reader=elevator-lobby badge=clement_w dir=in
2026-09-28T08:56:29 source=door reader=hush-room badge=pruitt_d dir=in
2026-09-28T08:56:38 source=door reader=elevator-lobby badge=bertram_l dir=in
2026-09-28T08:56:51 source=door reader=dso-office badge=clement_w dir=in
2026-09-28T08:57:05 source=door reader=dso-office badge=bertram_l dir=in
2026-09-28T08:57:05 source=door reader=elevator-lobby badge=eustace_m dir=in
2026-09-28T08:57:18 source=door reader=elevator-lobby badge=winifred_e dir=in
2026-09-28T08:57:39 source=door reader=fold badge=winifred_e dir=in
2026-09-28T08:57:45 source=door reader=dso-office badge=eustace_m dir=in
2026-09-28T08:58:39 source=door reader=elevator-lobby badge=nadia_f dir=in
2026-09-28T08:58:41 source=door reader=elevator-lobby badge=kenneth_y dir=in
2026-09-28T08:58:47 source=door reader=elevator-lobby badge=judith_v dir=in
2026-09-28T08:58:55 source=door reader=elevator-lobby badge=ivo_t dir=in
2026-09-28T08:59:02 source=door reader=as-office badge=nadia_f dir=in
2026-09-28T08:59:03 source=door reader=elevator-lobby badge=gideon_r dir=in
2026-09-28T08:59:21 source=door reader=tc-office badge=kenneth_y dir=in
2026-09-28T08:59:25 source=door reader=tc-office badge=judith_v dir=in
2026-09-28T08:59:27 source=door reader=tc-office badge=ivo_t dir=in
2026-09-28T08:59:32 source=door reader=elevator-lobby badge=quentin_j dir=in
2026-09-28T08:59:37 source=door reader=elevator-lobby badge=silas_q dir=in
2026-09-28T08:59:52 source=door reader=tc-office badge=gideon_r dir=in
2026-09-28T08:59:57 source=door reader=fold badge=silas_q dir=in
2026-09-28T09:00:06 source=door reader=elevator-lobby badge=otto_g dir=in
2026-09-28T09:00:16 source=door reader=elevator-lobby badge=lorna_b dir=in
2026-09-28T09:00:22 source=door reader=elevator-lobby badge=ursula_x dir=in
2026-09-28T09:00:26 source=door reader=as-office badge=quentin_j dir=in
2026-09-28T09:00:50 source=door reader=tc-office badge=lorna_b dir=in
2026-09-28T09:00:56 source=door reader=as-office badge=otto_g dir=in
2026-09-28T09:01:00 source=door reader=fold badge=ursula_x dir=in
2026-09-28T09:01:37 source=door reader=elevator-lobby badge=agnes_k dir=in
2026-09-28T09:01:51 source=door reader=elevator-lobby badge=rosalind_n dir=in
2026-09-28T09:02:19 source=door reader=elevator-lobby badge=fern_o dir=in
2026-09-28T09:02:29 source=door reader=as-office badge=rosalind_n dir=in
2026-09-28T09:02:30 source=door reader=dso-office badge=agnes_k dir=in
2026-09-28T09:02:34 source=door reader=elevator-lobby badge=tobias_u dir=in
2026-09-28T09:02:57 source=door reader=elevator-lobby badge=prudence_h dir=in
2026-09-28T09:03:00 source=door reader=elevator-lobby badge=milo_d dir=in
2026-09-28T09:03:04 source=door reader=elevator-lobby badge=vernon_z dir=in
2026-09-28T09:03:08 source=door reader=dso-office badge=fern_o dir=in
2026-09-28T09:03:12 source=door reader=elevator-lobby badge=harriet_s dir=in
2026-09-28T09:03:18 source=door reader=fold badge=tobias_u dir=in
2026-09-28T09:03:25 source=door reader=fold badge=vernon_z dir=in
2026-09-28T09:03:26 source=door reader=elevator-lobby badge=cyril_a dir=in
2026-09-28T09:03:37 source=door reader=elevator-lobby badge=dorothy_p dir=in
2026-09-28T09:03:41 source=door reader=as-office badge=prudence_h dir=in
2026-09-28T09:03:45 source=door reader=as-office badge=milo_d dir=in
2026-09-28T09:03:51 source=door reader=fold badge=cyril_a dir=in
2026-09-28T09:03:59 source=door reader=tc-office badge=harriet_s dir=in
2026-09-28T09:04:00 source=door reader=dso-office badge=dorothy_p dir=in
2026-09-28T10:10:08 source=door reader=supply-room-b badge=cyril_a dir=in
2026-09-28T10:49:42 source=door reader=supply-room-b badge=judith_v dir=in
2026-09-28T10:56:53 source=door reader=supply-room-b badge=kenneth_y dir=in
2026-09-28T11:00:52 source=door reader=supply-room-b badge=bertram_l dir=in
2026-09-28T11:03:00 source=door reader=supply-room-b badge=eustace_m dir=in
2026-09-28T11:27:05 source=door reader=supervisor-office badge=bertram_l dir=in
2026-09-28T11:38:07 source=door reader=supply-room-b badge=gideon_r dir=in
2026-09-28T12:04:48 source=door reader=break-room-1 badge=lorna_b dir=in
2026-09-28T12:05:56 source=door reader=break-room-1 badge=tobias_u dir=in
2026-09-28T12:10:10 source=door reader=supply-room-b badge=ursula_x dir=in
2026-09-28T12:10:21 source=door reader=break-room-1 badge=ursula_x dir=in
2026-09-28T12:11:07 source=door reader=break-room-1 badge=bertram_l dir=in
2026-09-28T12:13:30 source=door reader=break-room-1 badge=judith_v dir=in
2026-09-28T12:13:46 source=door reader=break-room-1 badge=winifred_e dir=in
2026-09-28T12:13:58 source=door reader=break-room-1 badge=clement_w dir=in
2026-09-28T12:15:09 source=door reader=break-room-1 badge=eustace_m dir=in
2026-09-28T12:16:53 source=door reader=break-room-1 badge=fern_o dir=in
2026-09-28T12:17:18 source=door reader=break-room-1 badge=gideon_r dir=in
2026-09-28T12:18:10 source=door reader=break-room-1 badge=otto_g dir=in
2026-09-28T12:21:11 source=door reader=break-room-1 badge=rosalind_n dir=in
2026-09-28T12:24:34 source=door reader=break-room-1 badge=harriet_s dir=in
2026-09-28T12:27:51 source=door reader=break-room-1 badge=vernon_z dir=in
2026-09-28T12:28:22 source=door reader=break-room-1 badge=dorothy_p dir=in
2026-09-28T12:28:30 source=door reader=break-room-1 badge=prudence_h dir=in
2026-09-28T12:29:13 source=door reader=break-room-1 badge=nadia_f dir=in
2026-09-28T12:31:48 source=door reader=break-room-1 badge=kenneth_y dir=in
2026-09-28T12:34:25 source=door reader=break-room-1 badge=quentin_j dir=in
2026-09-28T12:34:36 source=door reader=break-room-1 badge=cyril_a dir=in
2026-09-28T12:38:07 source=door reader=break-room-1 badge=agnes_k dir=in
2026-09-28T12:38:23 source=door reader=break-room-1 badge=silas_q dir=in
2026-09-28T12:38:56 source=door reader=break-room-1 badge=ivo_t dir=in
2026-09-28T12:39:02 source=door reader=break-room-1 badge=milo_d dir=in
2026-09-28T13:03:40 source=door reader=supply-room-b badge=nadia_f dir=in
2026-09-28T14:02:03 source=door reader=supply-room-b badge=fern_o dir=in
2026-09-28T17:00:39 source=door reader=elevator-lobby badge=nadia_f dir=out
2026-09-28T17:00:46 source=door reader=elevator-lobby badge=agnes_k dir=out
2026-09-28T17:00:46 source=door reader=elevator-lobby badge=kenneth_y dir=out
2026-09-28T17:01:06 source=door reader=elevator-lobby badge=clement_w dir=out
2026-09-28T17:01:08 source=door reader=elevator-lobby badge=otto_g dir=out
2026-09-28T17:01:23 source=door reader=elevator-lobby badge=cyril_a dir=out
2026-09-28T17:01:35 source=door reader=elevator-lobby badge=gideon_r dir=out
2026-09-28T17:01:35 source=door reader=elevator-lobby badge=tobias_u dir=out
2026-09-28T17:01:55 source=door reader=elevator-lobby badge=ursula_x dir=out
2026-09-28T17:02:50 source=door reader=elevator-lobby badge=lorna_b dir=out
2026-09-28T17:02:53 source=door reader=elevator-lobby badge=silas_q dir=out
2026-09-28T17:03:17 source=door reader=elevator-lobby badge=judith_v dir=out
2026-09-28T17:03:18 source=door reader=elevator-lobby badge=quentin_j dir=out
2026-09-28T17:04:07 source=door reader=elevator-lobby badge=fern_o dir=out
2026-09-28T17:04:44 source=door reader=elevator-lobby badge=vernon_z dir=out
2026-09-28T17:04:49 source=door reader=elevator-lobby badge=ivo_t dir=out
2026-09-28T17:04:55 source=door reader=elevator-lobby badge=milo_d dir=out
2026-09-28T17:04:57 source=door reader=elevator-lobby badge=prudence_h dir=out
2026-09-28T17:05:06 source=door reader=elevator-lobby badge=rosalind_n dir=out
2026-09-28T17:05:22 source=door reader=elevator-lobby badge=winifred_e dir=out
2026-09-28T17:05:32 source=door reader=elevator-lobby badge=eustace_m dir=out
2026-09-28T17:05:58 source=door reader=elevator-lobby badge=harriet_s dir=out
2026-09-28T17:05:59 source=door reader=elevator-lobby badge=bertram_l dir=out
2026-09-28T17:06:00 source=door reader=elevator-lobby badge=dorothy_p dir=out
2026-09-29T08:46:04 source=door reader=supervisor-office badge=hale_r dir=in
2026-09-29T08:46:41 source=door reader=elevator-lobby badge=hale_r dir=in
2026-09-29T08:56:23 source=door reader=elevator-lobby badge=prudence_h dir=in
2026-09-29T08:56:28 source=door reader=elevator-lobby badge=quentin_j dir=in
2026-09-29T08:56:45 source=door reader=elevator-lobby badge=nadia_f dir=in
2026-09-29T08:56:50 source=door reader=as-office badge=quentin_j dir=in
2026-09-29T08:57:08 source=door reader=elevator-lobby badge=judith_v dir=in
2026-09-29T08:57:14 source=door reader=as-office badge=nadia_f dir=in
2026-09-29T08:57:15 source=door reader=elevator-lobby badge=agnes_k dir=in
2026-09-29T08:57:23 source=door reader=as-office badge=prudence_h dir=in
2026-09-29T08:57:43 source=door reader=elevator-lobby badge=winifred_e dir=in
2026-09-29T08:57:48 source=door reader=elevator-lobby badge=fern_o dir=in
2026-09-29T08:58:00 source=door reader=elevator-lobby badge=otto_g dir=in
2026-09-29T08:58:03 source=door reader=elevator-lobby badge=silas_q dir=in
2026-09-29T08:58:04 source=door reader=tc-office badge=judith_v dir=in
2026-09-29T08:58:10 source=door reader=dso-office badge=agnes_k dir=in
2026-09-29T08:58:15 source=door reader=fold badge=winifred_e dir=in
2026-09-29T08:58:21 source=door reader=elevator-lobby badge=bertram_l dir=in
2026-09-29T08:58:24 source=door reader=elevator-lobby badge=dorothy_p dir=in
2026-09-29T08:58:31 source=door reader=dso-office badge=fern_o dir=in
2026-09-29T08:58:36 source=door reader=as-office badge=otto_g dir=in
2026-09-29T08:58:54 source=door reader=fold badge=silas_q dir=in
2026-09-29T08:59:02 source=door reader=dso-office badge=dorothy_p dir=in
2026-09-29T08:59:07 source=door reader=dso-office badge=bertram_l dir=in
2026-09-29T08:59:08 source=door reader=elevator-lobby badge=ursula_x dir=in
2026-09-29T08:59:18 source=door reader=hush-room badge=pruitt_d dir=in
2026-09-29T08:59:22 source=door reader=elevator-lobby badge=lorna_b dir=in
2026-09-29T08:59:50 source=door reader=tc-office badge=lorna_b dir=in
2026-09-29T08:59:54 source=door reader=fold badge=ursula_x dir=in
2026-09-29T08:59:55 source=door reader=elevator-lobby badge=milo_d dir=in
2026-09-29T09:00:15 source=door reader=as-office badge=milo_d dir=in
2026-09-29T09:00:45 source=door reader=elevator-lobby badge=kenneth_y dir=in
2026-09-29T09:01:05 source=door reader=elevator-lobby badge=eustace_m dir=in
2026-09-29T09:01:10 source=door reader=elevator-lobby badge=cyril_a dir=in
2026-09-29T09:01:19 source=door reader=elevator-lobby badge=gideon_r dir=in
2026-09-29T09:01:32 source=door reader=fold badge=cyril_a dir=in
2026-09-29T09:01:41 source=door reader=dso-office badge=eustace_m dir=in
2026-09-29T09:01:43 source=door reader=elevator-lobby badge=ivo_t dir=in
2026-09-29T09:01:45 source=door reader=tc-office badge=kenneth_y dir=in
2026-09-29T09:02:13 source=door reader=elevator-lobby badge=tobias_u dir=in
2026-09-29T09:02:18 source=door reader=tc-office badge=gideon_r dir=in
2026-09-29T09:02:31 source=door reader=tc-office badge=ivo_t dir=in
2026-09-29T09:02:38 source=door reader=elevator-lobby badge=clement_w dir=in
2026-09-29T09:02:46 source=door reader=fold badge=tobias_u dir=in
2026-09-29T09:03:36 source=door reader=dso-office badge=clement_w dir=in
2026-09-29T09:03:42 source=door reader=elevator-lobby badge=harriet_s dir=in
2026-09-29T09:03:45 source=door reader=elevator-lobby badge=vernon_z dir=in
2026-09-29T09:03:50 source=door reader=elevator-lobby badge=rosalind_n dir=in
2026-09-29T09:04:09 source=door reader=tc-office badge=harriet_s dir=in
2026-09-29T09:04:15 source=door reader=as-office badge=rosalind_n dir=in
2026-09-29T09:04:40 source=door reader=fold badge=vernon_z dir=in
2026-09-29T09:54:55 source=door reader=supply-room-b badge=ursula_x dir=in
2026-09-29T09:58:00 source=door reader=supply-room-b badge=bertram_l dir=in
2026-09-29T10:20:06 source=door reader=supply-room-b badge=fern_o dir=in
2026-09-29T11:05:26 source=door reader=supply-room-b badge=rosalind_n dir=in
2026-09-29T11:44:32 source=door reader=supply-room-b badge=vernon_z dir=in
2026-09-29T12:00:33 source=door reader=break-room-1 badge=agnes_k dir=in
2026-09-29T12:01:00 source=door reader=break-room-1 badge=dorothy_p dir=in
2026-09-29T12:01:48 source=door reader=break-room-1 badge=winifred_e dir=in
2026-09-29T12:02:14 source=door reader=break-room-1 badge=gideon_r dir=in
2026-09-29T12:02:49 source=door reader=break-room-1 badge=otto_g dir=in
2026-09-29T12:03:25 source=door reader=break-room-1 badge=lorna_b dir=in
2026-09-29T12:03:49 source=door reader=break-room-1 badge=fern_o dir=in
2026-09-29T12:04:21 source=door reader=break-room-1 badge=eustace_m dir=in
2026-09-29T12:04:21 source=door reader=break-room-1 badge=judith_v dir=in
2026-09-29T12:05:39 source=door reader=break-room-1 badge=rosalind_n dir=in
2026-09-29T12:06:50 source=door reader=break-room-1 badge=bertram_l dir=in
2026-09-29T12:07:01 source=door reader=break-room-1 badge=harriet_s dir=in
2026-09-29T12:07:20 source=door reader=break-room-1 badge=ivo_t dir=in
2026-09-29T12:08:57 source=door reader=break-room-1 badge=vernon_z dir=in
2026-09-29T12:09:03 source=door reader=break-room-1 badge=quentin_j dir=in
2026-09-29T12:11:43 source=door reader=break-room-1 badge=cyril_a dir=in
2026-09-29T12:13:38 source=door reader=break-room-1 badge=clement_w dir=in
2026-09-29T12:15:59 source=door reader=break-room-1 badge=ursula_x dir=in
2026-09-29T12:18:14 source=door reader=break-room-1 badge=kenneth_y dir=in
2026-09-29T12:24:44 source=door reader=break-room-1 badge=milo_d dir=in
2026-09-29T12:26:11 source=door reader=break-room-1 badge=nadia_f dir=in
2026-09-29T12:26:27 source=door reader=supply-room-b badge=cyril_a dir=in
2026-09-29T12:30:12 source=door reader=break-room-1 badge=prudence_h dir=in
2026-09-29T12:33:42 source=door reader=break-room-1 badge=silas_q dir=in
2026-09-29T12:38:49 source=door reader=break-room-1 badge=tobias_u dir=in
2026-09-29T12:39:54 source=door reader=supply-room-b badge=quentin_j dir=in
2026-09-29T13:11:18 source=door reader=supply-room-b badge=milo_d dir=in
2026-09-29T13:23:35 source=door reader=supply-room-b badge=lorna_b dir=in
2026-09-29T13:24:53 source=door reader=supply-room-b badge=nadia_f dir=in
2026-09-29T13:37:14 source=door reader=supply-room-b badge=silas_q dir=in
2026-09-29T16:01:23 source=door reader=supply-room-b badge=bertram_l dir=in
2026-09-29T17:00:13 source=door reader=elevator-lobby badge=tobias_u dir=out
2026-09-29T17:00:19 source=door reader=elevator-lobby badge=vernon_z dir=out
2026-09-29T17:00:36 source=door reader=elevator-lobby badge=judith_v dir=out
2026-09-29T17:01:14 source=door reader=elevator-lobby badge=gideon_r dir=out
2026-09-29T17:01:15 source=door reader=elevator-lobby badge=clement_w dir=out
2026-09-29T17:02:02 source=door reader=elevator-lobby badge=ursula_x dir=out
2026-09-29T17:02:17 source=door reader=elevator-lobby badge=milo_d dir=out
2026-09-29T17:02:24 source=door reader=elevator-lobby badge=cyril_a dir=out
2026-09-29T17:02:28 source=door reader=elevator-lobby badge=harriet_s dir=out
2026-09-29T17:02:33 source=door reader=elevator-lobby badge=kenneth_y dir=out
2026-09-29T17:02:43 source=door reader=elevator-lobby badge=silas_q dir=out
2026-09-29T17:02:46 source=door reader=elevator-lobby badge=rosalind_n dir=out
2026-09-29T17:02:52 source=door reader=elevator-lobby badge=prudence_h dir=out
2026-09-29T17:03:05 source=door reader=elevator-lobby badge=quentin_j dir=out
2026-09-29T17:03:09 source=door reader=elevator-lobby badge=ivo_t dir=out
2026-09-29T17:03:26 source=door reader=elevator-lobby badge=lorna_b dir=out
2026-09-29T17:03:30 source=door reader=elevator-lobby badge=agnes_k dir=out
2026-09-29T17:03:58 source=door reader=elevator-lobby badge=nadia_f dir=out
2026-09-29T17:04:02 source=door reader=elevator-lobby badge=otto_g dir=out
2026-09-29T17:04:29 source=door reader=elevator-lobby badge=fern_o dir=out
2026-09-29T17:04:44 source=door reader=elevator-lobby badge=eustace_m dir=out
2026-09-29T17:05:12 source=door reader=elevator-lobby badge=bertram_l dir=out
2026-09-29T17:05:27 source=door reader=elevator-lobby badge=dorothy_p dir=out
2026-09-29T17:05:46 source=door reader=elevator-lobby badge=winifred_e dir=out
2026-09-30T08:43:35 source=door reader=elevator-lobby badge=hale_r dir=in
2026-09-30T08:47:10 source=door reader=supervisor-office badge=hale_r dir=in
2026-09-30T08:56:16 source=door reader=elevator-lobby badge=dorothy_p dir=in
2026-09-30T08:56:19 source=door reader=elevator-lobby badge=clement_w dir=in
2026-09-30T08:56:49 source=door reader=elevator-lobby badge=judith_v dir=in
2026-09-30T08:56:53 source=door reader=dso-office badge=clement_w dir=in
2026-09-30T08:56:53 source=door reader=elevator-lobby badge=milo_d dir=in
2026-09-30T08:56:55 source=door reader=dso-office badge=dorothy_p dir=in
2026-09-30T08:57:00 source=door reader=elevator-lobby badge=kenneth_y dir=in
2026-09-30T08:57:18 source=door reader=elevator-lobby badge=gideon_r dir=in
2026-09-30T08:57:25 source=door reader=as-office badge=milo_d dir=in
2026-09-30T08:57:30 source=door reader=tc-office badge=kenneth_y dir=in
2026-09-30T08:57:40 source=door reader=tc-office badge=judith_v dir=in
2026-09-30T08:57:50 source=door reader=hush-room badge=pruitt_d dir=in
2026-09-30T08:58:14 source=door reader=tc-office badge=gideon_r dir=in
2026-09-30T08:58:35 source=door reader=elevator-lobby badge=fern_o dir=in
2026-09-30T08:58:44 source=door reader=elevator-lobby badge=bertram_l dir=in
2026-09-30T08:59:10 source=door reader=elevator-lobby badge=agnes_k dir=in
2026-09-30T08:59:12 source=door reader=dso-office badge=fern_o dir=in
2026-09-30T08:59:16 source=door reader=elevator-lobby badge=tobias_u dir=in
2026-09-30T08:59:23 source=door reader=elevator-lobby badge=lorna_b dir=in
2026-09-30T08:59:33 source=door reader=dso-office badge=bertram_l dir=in
2026-09-30T08:59:39 source=door reader=fold badge=tobias_u dir=in
2026-09-30T08:59:52 source=door reader=elevator-lobby badge=quentin_j dir=in
2026-09-30T08:59:53 source=door reader=elevator-lobby badge=harriet_s dir=in
2026-09-30T08:59:55 source=door reader=dso-office badge=agnes_k dir=in
2026-09-30T09:00:23 source=door reader=tc-office badge=lorna_b dir=in
2026-09-30T09:00:23 source=door reader=elevator-lobby badge=winifred_e dir=in
2026-09-30T09:00:38 source=door reader=as-office badge=quentin_j dir=in
2026-09-30T09:00:51 source=door reader=tc-office badge=harriet_s dir=in
2026-09-30T09:00:57 source=door reader=fold badge=winifred_e dir=in
2026-09-30T09:01:13 source=door reader=elevator-lobby badge=ursula_x dir=in
2026-09-30T09:01:19 source=door reader=elevator-lobby badge=eustace_m dir=in
2026-09-30T09:01:21 source=door reader=elevator-lobby badge=vernon_z dir=in
2026-09-30T09:01:42 source=door reader=fold badge=vernon_z dir=in
2026-09-30T09:01:45 source=door reader=elevator-lobby badge=cyril_a dir=in
2026-09-30T09:01:47 source=door reader=fold badge=ursula_x dir=in
2026-09-30T09:02:07 source=door reader=elevator-lobby badge=ivo_t dir=in
2026-09-30T09:02:08 source=door reader=fold badge=cyril_a dir=in
2026-09-30T09:02:14 source=door reader=dso-office badge=eustace_m dir=in
2026-09-30T09:02:36 source=door reader=tc-office badge=ivo_t dir=in
2026-09-30T09:03:12 source=door reader=elevator-lobby badge=rosalind_n dir=in
2026-09-30T09:03:19 source=door reader=elevator-lobby badge=prudence_h dir=in
2026-09-30T09:03:43 source=door reader=as-office badge=rosalind_n dir=in
2026-09-30T09:03:49 source=door reader=elevator-lobby badge=silas_q dir=in
2026-09-30T09:03:52 source=door reader=elevator-lobby badge=nadia_f dir=in
2026-09-30T09:03:55 source=door reader=elevator-lobby badge=otto_g dir=in
2026-09-30T09:03:55 source=door reader=as-office badge=prudence_h dir=in
2026-09-30T09:04:17 source=door reader=as-office badge=otto_g dir=in
2026-09-30T09:04:38 source=door reader=as-office badge=nadia_f dir=in
2026-09-30T09:04:42 source=door reader=fold badge=silas_q dir=in
2026-09-30T09:30:12 source=door reader=supply-room-b badge=vernon_z dir=in
2026-09-30T09:32:53 source=door reader=supply-room-b badge=nadia_f dir=in
2026-09-30T09:54:24 source=door reader=supply-room-b badge=ivo_t dir=in
2026-09-30T10:23:26 source=door reader=elevator-lobby badge=agnes_k dir=in
2026-09-30T10:27:51 source=door reader=supply-room-b badge=tobias_u dir=in
2026-09-30T10:47:07 source=door reader=supply-room-b badge=rosalind_n dir=in
2026-09-30T11:02:01 source=door reader=supply-room-b badge=bertram_l dir=in
2026-09-30T11:11:36 source=door reader=supply-room-b badge=bertram_l dir=in
2026-09-30T11:41:59 source=door reader=supply-room-b badge=silas_q dir=in
2026-09-30T11:55:39 source=door reader=supply-room-b badge=prudence_h dir=in
2026-09-30T12:03:50 source=door reader=break-room-1 badge=fern_o dir=in
2026-09-30T12:06:32 source=door reader=break-room-1 badge=otto_g dir=in
2026-09-30T12:06:33 source=door reader=break-room-1 badge=gideon_r dir=in
2026-09-30T12:06:51 source=door reader=break-room-1 badge=winifred_e dir=in
2026-09-30T12:11:10 source=door reader=break-room-1 badge=prudence_h dir=in
2026-09-30T12:12:10 source=door reader=break-room-1 badge=judith_v dir=in
2026-09-30T12:13:22 source=door reader=break-room-1 badge=cyril_a dir=in
2026-09-30T12:15:16 source=door reader=break-room-1 badge=quentin_j dir=in
2026-09-30T12:20:41 source=door reader=break-room-1 badge=dorothy_p dir=in
2026-09-30T12:21:03 source=door reader=break-room-1 badge=harriet_s dir=in
2026-09-30T12:21:24 source=door reader=break-room-1 badge=kenneth_y dir=in
2026-09-30T12:23:46 source=door reader=break-room-1 badge=rosalind_n dir=in
2026-09-30T12:24:22 source=door reader=break-room-1 badge=milo_d dir=in
2026-09-30T12:24:30 source=door reader=break-room-1 badge=silas_q dir=in
2026-09-30T12:25:47 source=door reader=break-room-1 badge=eustace_m dir=in
2026-09-30T12:30:10 source=door reader=break-room-1 badge=clement_w dir=in
2026-09-30T12:31:10 source=door reader=break-room-1 badge=vernon_z dir=in
2026-09-30T12:31:21 source=door reader=break-room-1 badge=nadia_f dir=in
2026-09-30T12:32:25 source=door reader=break-room-1 badge=ursula_x dir=in
2026-09-30T12:33:45 source=door reader=break-room-1 badge=lorna_b dir=in
2026-09-30T12:35:10 source=door reader=break-room-1 badge=tobias_u dir=in
2026-09-30T12:35:41 source=door reader=break-room-1 badge=ivo_t dir=in
2026-09-30T12:36:43 source=door reader=break-room-1 badge=bertram_l dir=in
2026-09-30T12:39:30 source=door reader=break-room-1 badge=agnes_k dir=in
2026-09-30T12:56:43 source=door reader=supply-room-b badge=dorothy_p dir=in
2026-09-30T13:16:55 source=door reader=supply-room-b badge=otto_g dir=in
2026-09-30T14:09:11 source=door reader=supply-room-b badge=clement_w dir=in
2026-09-30T17:01:06 source=door reader=elevator-lobby badge=cyril_a dir=out
2026-09-30T17:01:11 source=door reader=elevator-lobby badge=vernon_z dir=out
2026-09-30T17:01:20 source=door reader=elevator-lobby badge=kenneth_y dir=out
2026-09-30T17:01:45 source=door reader=elevator-lobby badge=gideon_r dir=out
2026-09-30T17:01:47 source=door reader=elevator-lobby badge=rosalind_n dir=out
2026-09-30T17:01:56 source=door reader=elevator-lobby badge=silas_q dir=out
2026-09-30T17:02:01 source=door reader=elevator-lobby badge=fern_o dir=out
2026-09-30T17:02:27 source=door reader=elevator-lobby badge=quentin_j dir=out
2026-09-30T17:02:29 source=door reader=elevator-lobby badge=milo_d dir=out
2026-09-30T17:02:32 source=door reader=elevator-lobby badge=tobias_u dir=out
2026-09-30T17:03:06 source=door reader=elevator-lobby badge=dorothy_p dir=out
2026-09-30T17:03:11 source=door reader=elevator-lobby badge=clement_w dir=out
2026-09-30T17:03:18 source=door reader=elevator-lobby badge=harriet_s dir=out
2026-09-30T17:03:28 source=door reader=elevator-lobby badge=ursula_x dir=out
2026-09-30T17:03:40 source=door reader=elevator-lobby badge=agnes_k dir=out
2026-09-30T17:03:41 source=door reader=elevator-lobby badge=ivo_t dir=out
2026-09-30T17:03:47 source=door reader=elevator-lobby badge=bertram_l dir=out
2026-09-30T17:03:55 source=door reader=elevator-lobby badge=judith_v dir=out
2026-09-30T17:04:22 source=door reader=elevator-lobby badge=eustace_m dir=out
2026-09-30T17:04:38 source=door reader=elevator-lobby badge=lorna_b dir=out
2026-09-30T17:05:07 source=door reader=elevator-lobby badge=winifred_e dir=out
2026-09-30T17:05:30 source=door reader=elevator-lobby badge=nadia_f dir=out
2026-09-30T17:05:54 source=door reader=elevator-lobby badge=prudence_h dir=out
2026-09-30T17:05:57 source=door reader=elevator-lobby badge=otto_g dir=out
2026-10-01T08:41:10 source=door reader=elevator-lobby badge=hale_r dir=in
2026-10-01T08:48:39 source=door reader=supervisor-office badge=hale_r dir=in
2026-10-01T08:55:19 source=door reader=hush-room badge=pruitt_d dir=in
2026-10-01T08:56:07 source=door reader=elevator-lobby badge=quentin_j dir=in
2026-10-01T08:56:07 source=door reader=elevator-lobby badge=winifred_e dir=in
2026-10-01T08:56:10 source=door reader=elevator-lobby badge=ivo_t dir=in
2026-10-01T08:56:16 source=door reader=elevator-lobby badge=lorna_b dir=in
2026-10-01T08:56:25 source=door reader=elevator-lobby badge=milo_d dir=in
2026-10-01T08:56:29 source=door reader=fold badge=winifred_e dir=in
2026-10-01T08:56:40 source=door reader=tc-office badge=lorna_b dir=in
2026-10-01T08:56:46 source=door reader=tc-office badge=ivo_t dir=in
2026-10-01T08:56:47 source=door reader=as-office badge=quentin_j dir=in
2026-10-01T08:57:00 source=door reader=elevator-lobby badge=agnes_k dir=in
2026-10-01T08:57:25 source=door reader=as-office badge=milo_d dir=in
2026-10-01T08:57:25 source=door reader=elevator-lobby badge=prudence_h dir=in
2026-10-01T08:57:33 source=door reader=dso-office badge=agnes_k dir=in
2026-10-01T08:57:57 source=door reader=elevator-lobby badge=bertram_l dir=in
2026-10-01T08:58:00 source=door reader=as-office badge=prudence_h dir=in
2026-10-01T08:58:09 source=door reader=elevator-lobby badge=judith_v dir=in
2026-10-01T08:58:21 source=door reader=dso-office badge=bertram_l dir=in
2026-10-01T08:58:52 source=door reader=tc-office badge=judith_v dir=in
2026-10-01T08:59:07 source=door reader=elevator-lobby badge=harriet_s dir=in
2026-10-01T08:59:27 source=door reader=tc-office badge=harriet_s dir=in
2026-10-01T08:59:58 source=door reader=elevator-lobby badge=ursula_x dir=in
2026-10-01T09:00:10 source=door reader=elevator-lobby badge=silas_q dir=in
2026-10-01T09:00:25 source=door reader=elevator-lobby badge=cyril_a dir=in
2026-10-01T09:00:27 source=door reader=elevator-lobby badge=tobias_u dir=in
2026-10-01T09:00:36 source=door reader=fold badge=silas_q dir=in
2026-10-01T09:00:40 source=door reader=fold badge=ursula_x dir=in
2026-10-01T09:00:45 source=door reader=elevator-lobby badge=gideon_r dir=in
2026-10-01T09:00:51 source=door reader=fold badge=cyril_a dir=in
2026-10-01T09:00:58 source=door reader=elevator-lobby badge=dorothy_p dir=in
2026-10-01T09:00:58 source=door reader=fold badge=tobias_u dir=in
2026-10-01T09:01:06 source=door reader=tc-office badge=gideon_r dir=in
2026-10-01T09:01:24 source=door reader=elevator-lobby badge=kenneth_y dir=in
2026-10-01T09:01:42 source=door reader=dso-office badge=dorothy_p dir=in
2026-10-01T09:01:53 source=door reader=tc-office badge=kenneth_y dir=in
2026-10-01T09:02:00 source=door reader=elevator-lobby badge=rosalind_n dir=in
2026-10-01T09:02:09 source=door reader=elevator-lobby badge=vernon_z dir=in
2026-10-01T09:02:16 source=door reader=elevator-lobby badge=eustace_m dir=in
2026-10-01T09:02:24 source=door reader=elevator-lobby badge=otto_g dir=in
2026-10-01T09:02:37 source=door reader=elevator-lobby badge=clement_w dir=in
2026-10-01T09:02:41 source=door reader=as-office badge=rosalind_n dir=in
2026-10-01T09:02:44 source=door reader=fold badge=vernon_z dir=in
2026-10-01T09:02:56 source=door reader=dso-office badge=eustace_m dir=in
2026-10-01T09:03:00 source=door reader=dso-office badge=clement_w dir=in
2026-10-01T09:03:11 source=door reader=as-office badge=otto_g dir=in
2026-10-01T09:03:34 source=door reader=elevator-lobby badge=fern_o dir=in
2026-10-01T09:03:38 source=door reader=elevator-lobby badge=nadia_f dir=in
2026-10-01T09:03:59 source=door reader=dso-office badge=fern_o dir=in
2026-10-01T09:04:00 source=door reader=as-office badge=nadia_f dir=in
2026-10-01T09:33:16 source=door reader=supply-room-b badge=ursula_x dir=in
2026-10-01T10:01:46 source=door reader=supply-room-b badge=silas_q dir=in
2026-10-01T10:17:32 source=door reader=supply-room-b badge=bertram_l dir=in
2026-10-01T10:18:57 source=door reader=supply-room-b badge=winifred_e dir=in
2026-10-01T10:40:19 source=door reader=supply-room-b badge=milo_d dir=in
2026-10-01T10:48:57 source=door reader=supply-room-b badge=nadia_f dir=in
2026-10-01T11:00:31 source=door reader=supply-room-b badge=lorna_b dir=in
2026-10-01T11:24:35 source=door reader=supply-room-b badge=kenneth_y dir=in
2026-10-01T12:01:47 source=door reader=break-room-1 badge=otto_g dir=in
2026-10-01T12:02:24 source=door reader=break-room-1 badge=nadia_f dir=in
2026-10-01T12:05:05 source=door reader=break-room-1 badge=judith_v dir=in
2026-10-01T12:05:53 source=door reader=break-room-1 badge=milo_d dir=in
2026-10-01T12:07:16 source=door reader=break-room-1 badge=kenneth_y dir=in
2026-10-01T12:09:00 source=door reader=break-room-1 badge=clement_w dir=in
2026-10-01T12:11:31 source=door reader=break-room-1 badge=prudence_h dir=in
2026-10-01T12:12:45 source=door reader=supply-room-b badge=rosalind_n dir=in
2026-10-01T12:19:53 source=door reader=break-room-1 badge=agnes_k dir=in
2026-10-01T12:24:05 source=door reader=break-room-1 badge=ursula_x dir=in
2026-10-01T12:24:23 source=door reader=break-room-1 badge=winifred_e dir=in
2026-10-01T12:24:40 source=door reader=break-room-1 badge=eustace_m dir=in
2026-10-01T12:27:21 source=door reader=break-room-1 badge=vernon_z dir=in
2026-10-01T12:27:27 source=door reader=break-room-1 badge=rosalind_n dir=in
2026-10-01T12:28:14 source=door reader=break-room-1 badge=silas_q dir=in
2026-10-01T12:30:15 source=door reader=break-room-1 badge=dorothy_p dir=in
2026-10-01T12:30:17 source=door reader=break-room-1 badge=ivo_t dir=in
2026-10-01T12:31:06 source=door reader=break-room-1 badge=cyril_a dir=in
2026-10-01T12:31:11 source=door reader=break-room-1 badge=lorna_b dir=in
2026-10-01T12:32:04 source=door reader=break-room-1 badge=bertram_l dir=in
2026-10-01T12:32:19 source=door reader=break-room-1 badge=gideon_r dir=in
2026-10-01T12:34:26 source=door reader=break-room-1 badge=quentin_j dir=in
2026-10-01T12:34:30 source=door reader=break-room-1 badge=tobias_u dir=in
2026-10-01T12:37:52 source=door reader=break-room-1 badge=harriet_s dir=in
2026-10-01T12:38:13 source=door reader=break-room-1 badge=fern_o dir=in
2026-10-01T12:39:58 source=door reader=supply-room-b badge=prudence_h dir=in
2026-10-01T13:01:29 source=door reader=supply-room-b badge=harriet_s dir=in
2026-10-01T13:07:43 source=door reader=elevator-lobby badge=agnes_k dir=in
2026-10-01T13:52:48 source=door reader=supply-room-b badge=otto_g dir=in
2026-10-01T17:00:06 source=door reader=elevator-lobby badge=cyril_a dir=out
2026-10-01T17:00:15 source=door reader=elevator-lobby badge=nadia_f dir=out
2026-10-01T17:00:35 source=door reader=elevator-lobby badge=vernon_z dir=out
2026-10-01T17:01:05 source=door reader=elevator-lobby badge=harriet_s dir=out
2026-10-01T17:01:33 source=door reader=elevator-lobby badge=kenneth_y dir=out
2026-10-01T17:01:38 source=door reader=elevator-lobby badge=silas_q dir=out
2026-10-01T17:02:13 source=door reader=elevator-lobby badge=quentin_j dir=out
2026-10-01T17:02:22 source=door reader=elevator-lobby badge=ivo_t dir=out
2026-10-01T17:03:32 source=door reader=elevator-lobby badge=rosalind_n dir=out
2026-10-01T17:03:46 source=door reader=elevator-lobby badge=gideon_r dir=out
2026-10-01T17:03:51 source=door reader=elevator-lobby badge=eustace_m dir=out
2026-10-01T17:04:01 source=door reader=elevator-lobby badge=otto_g dir=out
2026-10-01T17:04:12 source=door reader=elevator-lobby badge=tobias_u dir=out
2026-10-01T17:04:13 source=door reader=elevator-lobby badge=ursula_x dir=out
2026-10-01T17:04:39 source=door reader=elevator-lobby badge=dorothy_p dir=out
2026-10-01T17:04:42 source=door reader=elevator-lobby badge=fern_o dir=out
2026-10-01T17:04:45 source=door reader=elevator-lobby badge=winifred_e dir=out
2026-10-01T17:04:48 source=door reader=elevator-lobby badge=clement_w dir=out
2026-10-01T17:04:57 source=door reader=elevator-lobby badge=lorna_b dir=out
2026-10-01T17:05:06 source=door reader=elevator-lobby badge=judith_v dir=out
2026-10-01T17:05:34 source=door reader=elevator-lobby badge=prudence_h dir=out
2026-10-01T17:05:42 source=door reader=elevator-lobby badge=milo_d dir=out
2026-10-01T17:05:43 source=door reader=elevator-lobby badge=bertram_l dir=out
2026-10-01T17:06:00 source=door reader=elevator-lobby badge=agnes_k dir=out
2026-10-02T08:46:23 source=door reader=elevator-lobby badge=hale_r dir=in
2026-10-02T08:49:55 source=door reader=supervisor-office badge=hale_r dir=in
2026-10-02T08:55:43 source=door reader=hush-room badge=pruitt_d dir=in
2026-10-02T08:56:25 source=door reader=elevator-lobby badge=dorothy_p dir=in
2026-10-02T08:56:55 source=door reader=dso-office badge=dorothy_p dir=in
2026-10-02T08:57:11 source=door reader=elevator-lobby badge=milo_d dir=in
2026-10-02T08:57:42 source=door reader=as-office badge=milo_d dir=in
2026-10-02T08:57:53 source=door reader=elevator-lobby badge=ivo_t dir=in
2026-10-02T08:57:59 source=door reader=elevator-lobby badge=clement_w dir=in
2026-10-02T08:58:14 source=door reader=elevator-lobby badge=winifred_e dir=in
2026-10-02T08:58:31 source=door reader=tc-office badge=ivo_t dir=in
2026-10-02T08:58:35 source=door reader=fold badge=winifred_e dir=in
2026-10-02T08:58:48 source=door reader=dso-office badge=clement_w dir=in
2026-10-02T08:59:13 source=door reader=elevator-lobby badge=lorna_b dir=in
2026-10-02T08:59:14 source=door reader=elevator-lobby badge=cyril_a dir=in
2026-10-02T08:59:21 source=door reader=elevator-lobby badge=eustace_m dir=in
2026-10-02T08:59:25 source=door reader=elevator-lobby badge=fern_o dir=in
2026-10-02T08:59:40 source=door reader=fold badge=cyril_a dir=in
2026-10-02T08:59:42 source=door reader=elevator-lobby badge=gideon_r dir=in
2026-10-02T08:59:49 source=door reader=elevator-lobby badge=nadia_f dir=in
2026-10-02T08:59:51 source=door reader=elevator-lobby badge=silas_q dir=in
2026-10-02T09:00:05 source=door reader=tc-office badge=lorna_b dir=in
2026-10-02T09:00:08 source=door reader=dso-office badge=eustace_m dir=in
2026-10-02T09:00:13 source=door reader=tc-office badge=gideon_r dir=in
2026-10-02T09:00:21 source=door reader=dso-office badge=fern_o dir=in
2026-10-02T09:00:31 source=door reader=elevator-lobby badge=quentin_j dir=in
2026-10-02T09:00:33 source=door reader=elevator-lobby badge=ursula_x dir=in
2026-10-02T09:00:38 source=door reader=as-office badge=nadia_f dir=in
2026-10-02T09:00:40 source=door reader=fold badge=silas_q dir=in
2026-10-02T09:00:42 source=door reader=elevator-lobby badge=kenneth_y dir=in
2026-10-02T09:00:52 source=door reader=elevator-lobby badge=harriet_s dir=in
2026-10-02T09:01:04 source=door reader=elevator-lobby badge=judith_v dir=in
2026-10-02T09:01:12 source=door reader=fold badge=ursula_x dir=in
2026-10-02T09:01:13 source=door reader=as-office badge=quentin_j dir=in
2026-10-02T09:01:20 source=door reader=tc-office badge=harriet_s dir=in
2026-10-02T09:01:28 source=door reader=tc-office badge=kenneth_y dir=in
2026-10-02T09:01:31 source=door reader=elevator-lobby badge=otto_g dir=in
2026-10-02T09:01:36 source=door reader=elevator-lobby badge=bertram_l dir=in
2026-10-02T09:01:44 source=door reader=tc-office badge=judith_v dir=in
2026-10-02T09:01:56 source=door reader=dso-office badge=bertram_l dir=in
2026-10-02T09:02:07 source=door reader=as-office badge=otto_g dir=in
2026-10-02T09:02:10 source=door reader=elevator-lobby badge=prudence_h dir=in
2026-10-02T09:02:44 source=door reader=as-office badge=prudence_h dir=in
2026-10-02T09:02:44 source=door reader=elevator-lobby badge=rosalind_n dir=in
2026-10-02T09:03:07 source=door reader=elevator-lobby badge=vernon_z dir=in
2026-10-02T09:03:14 source=door reader=elevator-lobby badge=agnes_k dir=in
2026-10-02T09:03:39 source=door reader=as-office badge=rosalind_n dir=in
2026-10-02T09:03:40 source=door reader=elevator-lobby badge=tobias_u dir=in
2026-10-02T09:03:57 source=door reader=fold badge=vernon_z dir=in
2026-10-02T09:03:59 source=door reader=dso-office badge=agnes_k dir=in
2026-10-02T09:04:02 source=door reader=fold badge=tobias_u dir=in
2026-10-02T09:35:00 source=door reader=supply-room-b badge=kenneth_y dir=in
2026-10-02T09:40:52 source=door reader=supply-room-b badge=tobias_u dir=in
2026-10-02T11:07:53 source=door reader=supply-room-b badge=prudence_h dir=in
2026-10-02T11:15:13 source=door reader=supply-room-b badge=judith_v dir=in
2026-10-02T11:32:23 source=door reader=supply-room-b badge=cyril_a dir=in
2026-10-02T11:36:56 source=door reader=supply-room-b badge=fern_o dir=in
2026-10-02T12:00:09 source=door reader=break-room-1 badge=quentin_j dir=in
2026-10-02T12:00:35 source=door reader=break-room-1 badge=lorna_b dir=in
2026-10-02T12:03:30 source=door reader=break-room-1 badge=dorothy_p dir=in
2026-10-02T12:06:58 source=door reader=break-room-1 badge=kenneth_y dir=in
2026-10-02T12:09:27 source=door reader=break-room-1 badge=rosalind_n dir=in
2026-10-02T12:11:03 source=door reader=break-room-1 badge=eustace_m dir=in
2026-10-02T12:14:26 source=door reader=break-room-1 badge=clement_w dir=in
2026-10-02T12:14:28 source=door reader=break-room-1 badge=prudence_h dir=in
2026-10-02T12:15:16 source=door reader=break-room-1 badge=agnes_k dir=in
2026-10-02T12:18:26 source=door reader=break-room-1 badge=milo_d dir=in
2026-10-02T12:18:41 source=door reader=break-room-1 badge=winifred_e dir=in
2026-10-02T12:19:28 source=door reader=break-room-1 badge=otto_g dir=in
2026-10-02T12:20:17 source=door reader=supply-room-b badge=ursula_x dir=in
2026-10-02T12:20:51 source=door reader=break-room-1 badge=fern_o dir=in
2026-10-02T12:21:55 source=door reader=break-room-1 badge=ursula_x dir=in
2026-10-02T12:22:27 source=door reader=elevator-lobby badge=agnes_k dir=in
2026-10-02T12:23:10 source=door reader=break-room-1 badge=harriet_s dir=in
2026-10-02T12:23:27 source=door reader=break-room-1 badge=silas_q dir=in
2026-10-02T12:25:01 source=door reader=break-room-1 badge=tobias_u dir=in
2026-10-02T12:26:07 source=door reader=break-room-1 badge=ivo_t dir=in
2026-10-02T12:27:26 source=door reader=break-room-1 badge=nadia_f dir=in
2026-10-02T12:27:59 source=door reader=break-room-1 badge=bertram_l dir=in
2026-10-02T12:30:47 source=door reader=break-room-1 badge=gideon_r dir=in
2026-10-02T12:33:06 source=door reader=supply-room-b badge=dorothy_p dir=in
2026-10-02T12:36:27 source=door reader=break-room-1 badge=cyril_a dir=in
2026-10-02T12:36:28 source=door reader=break-room-1 badge=judith_v dir=in
2026-10-02T12:37:17 source=door reader=break-room-1 badge=vernon_z dir=in
2026-10-02T12:42:24 source=door reader=supply-room-b badge=winifred_e dir=in
2026-10-02T13:14:57 source=door reader=supply-room-b badge=harriet_s dir=in
2026-10-02T14:08:51 source=door reader=supply-room-b badge=ivo_t dir=in
2026-10-02T14:34:28 source=door reader=supply-room-b badge=bertram_l dir=in
2026-10-02T15:27:40 source=door reader=elevator-lobby badge=agnes_k dir=in
2026-10-02T17:00:02 source=door reader=elevator-lobby badge=bertram_l dir=out
2026-10-02T17:00:19 source=door reader=elevator-lobby badge=winifred_e dir=out
2026-10-02T17:01:22 source=door reader=elevator-lobby badge=judith_v dir=out
2026-10-02T17:01:37 source=door reader=elevator-lobby badge=ursula_x dir=out
2026-10-02T17:01:52 source=door reader=elevator-lobby badge=ivo_t dir=out
2026-10-02T17:02:12 source=door reader=elevator-lobby badge=fern_o dir=out
2026-10-02T17:02:15 source=door reader=elevator-lobby badge=eustace_m dir=out
2026-10-02T17:02:32 source=door reader=elevator-lobby badge=harriet_s dir=out
2026-10-02T17:02:34 source=door reader=elevator-lobby badge=vernon_z dir=out
2026-10-02T17:02:37 source=door reader=elevator-lobby badge=clement_w dir=out
2026-10-02T17:03:05 source=door reader=elevator-lobby badge=agnes_k dir=out
2026-10-02T17:03:06 source=door reader=elevator-lobby badge=tobias_u dir=out
2026-10-02T17:03:12 source=door reader=elevator-lobby badge=kenneth_y dir=out
2026-10-02T17:03:36 source=door reader=elevator-lobby badge=silas_q dir=out
2026-10-02T17:03:46 source=door reader=elevator-lobby badge=dorothy_p dir=out
2026-10-02T17:04:14 source=door reader=elevator-lobby badge=quentin_j dir=out
2026-10-02T17:04:15 source=door reader=elevator-lobby badge=cyril_a dir=out
2026-10-02T17:04:22 source=door reader=elevator-lobby badge=prudence_h dir=out
2026-10-02T17:05:02 source=door reader=elevator-lobby badge=lorna_b dir=out
2026-10-02T17:05:02 source=door reader=elevator-lobby badge=milo_d dir=out
2026-10-02T17:05:16 source=door reader=elevator-lobby badge=nadia_f dir=out
2026-10-02T17:05:17 source=door reader=elevator-lobby badge=gideon_r dir=out
2026-10-02T17:05:19 source=door reader=elevator-lobby badge=rosalind_n dir=out
2026-10-02T17:05:47 source=door reader=elevator-lobby badge=otto_g dir=out
2026-10-05T08:49:25 source=door reader=elevator-lobby badge=hale_r dir=in
2026-10-05T08:53:04 source=door reader=supervisor-office badge=hale_r dir=in
2026-10-05T08:56:09 source=door reader=elevator-lobby badge=dorothy_p dir=in
2026-10-05T08:56:31 source=door reader=elevator-lobby badge=quentin_j dir=in
2026-10-05T08:56:35 source=door reader=elevator-lobby badge=winifred_e dir=in
2026-10-05T08:56:43 source=door reader=dso-office badge=dorothy_p dir=in
2026-10-05T08:57:00 source=door reader=elevator-lobby badge=ivo_t dir=in
2026-10-05T08:57:13 source=door reader=fold badge=winifred_e dir=in
2026-10-05T08:57:18 source=door reader=as-office badge=quentin_j dir=in
2026-10-05T08:57:29 source=door reader=elevator-lobby badge=otto_g dir=in
2026-10-05T08:57:33 source=door reader=tc-office badge=ivo_t dir=in
2026-10-05T08:57:58 source=door reader=elevator-lobby badge=milo_d dir=in
2026-10-05T08:58:19 source=door reader=elevator-lobby badge=harriet_s dir=in
2026-10-05T08:58:24 source=door reader=as-office badge=milo_d dir=in
2026-10-05T08:58:28 source=door reader=as-office badge=otto_g dir=in
2026-10-05T08:58:29 source=door reader=elevator-lobby badge=agnes_k dir=in
2026-10-05T08:58:49 source=door reader=elevator-lobby badge=rosalind_n dir=in
2026-10-05T08:58:51 source=door reader=tc-office badge=harriet_s dir=in
2026-10-05T08:59:07 source=door reader=dso-office badge=agnes_k dir=in
2026-10-05T08:59:07 source=door reader=hush-room badge=pruitt_d dir=in
2026-10-05T08:59:08 source=door reader=elevator-lobby badge=gideon_r dir=in
2026-10-05T08:59:23 source=door reader=elevator-lobby badge=bertram_l dir=in
2026-10-05T08:59:25 source=door reader=elevator-lobby badge=fern_o dir=in
2026-10-05T08:59:26 source=door reader=elevator-lobby badge=clement_w dir=in
2026-10-05T08:59:28 source=door reader=elevator-lobby badge=eustace_m dir=in
2026-10-05T08:59:40 source=door reader=elevator-lobby badge=prudence_h dir=in
2026-10-05T08:59:42 source=door reader=as-office badge=rosalind_n dir=in
2026-10-05T08:59:49 source=door reader=dso-office badge=fern_o dir=in
2026-10-05T08:59:58 source=door reader=dso-office badge=bertram_l dir=in
2026-10-05T08:59:58 source=door reader=tc-office badge=gideon_r dir=in
2026-10-05T09:00:01 source=door reader=as-office badge=prudence_h dir=in
2026-10-05T09:00:04 source=door reader=elevator-lobby badge=vernon_z dir=in
2026-10-05T09:00:07 source=door reader=dso-office badge=clement_w dir=in
2026-10-05T09:00:07 source=door reader=elevator-lobby badge=lorna_b dir=in
2026-10-05T09:00:10 source=door reader=dso-office badge=eustace_m dir=in
2026-10-05T09:00:13 source=door reader=elevator-lobby badge=tobias_u dir=in
2026-10-05T09:00:30 source=door reader=fold badge=vernon_z dir=in
2026-10-05T09:00:49 source=door reader=fold badge=tobias_u dir=in
2026-10-05T09:00:51 source=door reader=tc-office badge=lorna_b dir=in
2026-10-05T09:01:14 source=door reader=elevator-lobby badge=silas_q dir=in
2026-10-05T09:01:18 source=door reader=elevator-lobby badge=judith_v dir=in
2026-10-05T09:01:20 source=door reader=elevator-lobby badge=nadia_f dir=in
2026-10-05T09:01:56 source=door reader=tc-office badge=judith_v dir=in
2026-10-05T09:01:56 source=door reader=as-office badge=nadia_f dir=in
2026-10-05T09:02:04 source=door reader=fold badge=silas_q dir=in
2026-10-05T09:02:33 source=door reader=elevator-lobby badge=ursula_x dir=in
2026-10-05T09:03:17 source=door reader=elevator-lobby badge=kenneth_y dir=in
2026-10-05T09:03:21 source=door reader=fold badge=ursula_x dir=in
2026-10-05T09:03:48 source=door reader=elevator-lobby badge=cyril_a dir=in
2026-10-05T09:03:51 source=door reader=tc-office badge=kenneth_y dir=in
2026-10-05T09:04:29 source=door reader=fold badge=cyril_a dir=in
2026-10-05T10:14:22 source=door reader=supply-room-b badge=agnes_k dir=in
2026-10-05T11:01:48 source=door reader=supervisor-office badge=bertram_l dir=in
2026-10-05T11:02:10 source=door reader=supply-room-b badge=ivo_t dir=in
2026-10-05T11:09:19 source=door reader=supply-room-b badge=otto_g dir=in
2026-10-05T11:43:27 source=door reader=elevator-lobby badge=agnes_k dir=in
2026-10-05T11:53:19 source=door reader=supply-room-b badge=prudence_h dir=in
2026-10-05T11:55:15 source=door reader=supply-room-b badge=nadia_f dir=in
2026-10-05T12:00:39 source=door reader=break-room-1 badge=lorna_b dir=in
2026-10-05T12:01:41 source=door reader=break-room-1 badge=ursula_x dir=in
2026-10-05T12:02:43 source=door reader=break-room-1 badge=milo_d dir=in
2026-10-05T12:04:25 source=door reader=break-room-1 badge=winifred_e dir=in
2026-10-05T12:05:10 source=door reader=break-room-1 badge=gideon_r dir=in
2026-10-05T12:05:26 source=door reader=break-room-1 badge=dorothy_p dir=in
2026-10-05T12:07:03 source=door reader=break-room-1 badge=agnes_k dir=in
2026-10-05T12:07:10 source=door reader=break-room-1 badge=rosalind_n dir=in
2026-10-05T12:07:30 source=door reader=break-room-1 badge=tobias_u dir=in
2026-10-05T12:08:55 source=door reader=break-room-1 badge=eustace_m dir=in
2026-10-05T12:08:57 source=door reader=break-room-1 badge=silas_q dir=in
2026-10-05T12:09:22 source=door reader=break-room-1 badge=ivo_t dir=in
2026-10-05T12:09:38 source=door reader=break-room-1 badge=judith_v dir=in
2026-10-05T12:10:22 source=door reader=break-room-1 badge=vernon_z dir=in
2026-10-05T12:11:10 source=door reader=break-room-1 badge=bertram_l dir=in
2026-10-05T12:14:46 source=door reader=break-room-1 badge=prudence_h dir=in
2026-10-05T12:15:51 source=door reader=break-room-1 badge=fern_o dir=in
2026-10-05T12:20:57 source=door reader=break-room-1 badge=clement_w dir=in
2026-10-05T12:23:10 source=door reader=break-room-1 badge=kenneth_y dir=in
2026-10-05T12:23:52 source=door reader=break-room-1 badge=quentin_j dir=in
2026-10-05T12:26:09 source=door reader=break-room-1 badge=otto_g dir=in
2026-10-05T12:26:25 source=door reader=break-room-1 badge=harriet_s dir=in
2026-10-05T12:29:42 source=door reader=break-room-1 badge=nadia_f dir=in
2026-10-05T12:36:52 source=door reader=break-room-1 badge=cyril_a dir=in
2026-10-05T13:22:28 source=door reader=supply-room-b badge=ursula_x dir=in
2026-10-05T13:33:15 source=door reader=supply-room-b badge=bertram_l dir=in
2026-10-05T14:00:25 source=door reader=supply-room-b badge=tobias_u dir=in
2026-10-05T14:05:37 source=door reader=elevator-lobby badge=agnes_k dir=in
2026-10-05T14:06:51 source=door reader=supply-room-b badge=cyril_a dir=in
2026-10-05T17:00:29 source=door reader=elevator-lobby badge=harriet_s dir=out
2026-10-05T17:00:40 source=door reader=elevator-lobby badge=milo_d dir=out
2026-10-05T17:00:40 source=door reader=elevator-lobby badge=vernon_z dir=out
2026-10-05T17:00:49 source=door reader=elevator-lobby badge=winifred_e dir=out
2026-10-05T17:01:06 source=door reader=elevator-lobby badge=tobias_u dir=out
2026-10-05T17:01:12 source=door reader=elevator-lobby badge=cyril_a dir=out
2026-10-05T17:01:28 source=door reader=elevator-lobby badge=agnes_k dir=out
2026-10-05T17:02:01 source=door reader=elevator-lobby badge=ursula_x dir=out
2026-10-05T17:02:12 source=door reader=elevator-lobby badge=dorothy_p dir=out
2026-10-05T17:02:16 source=door reader=elevator-lobby badge=fern_o dir=out
2026-10-05T17:02:17 source=door reader=elevator-lobby badge=prudence_h dir=out
2026-10-05T17:02:29 source=door reader=elevator-lobby badge=eustace_m dir=out
2026-10-05T17:02:33 source=door reader=elevator-lobby badge=judith_v dir=out
2026-10-05T17:03:25 source=door reader=elevator-lobby badge=lorna_b dir=out
2026-10-05T17:03:44 source=door reader=elevator-lobby badge=gideon_r dir=out
2026-10-05T17:03:45 source=door reader=elevator-lobby badge=silas_q dir=out
2026-10-05T17:04:14 source=door reader=elevator-lobby badge=nadia_f dir=out
2026-10-05T17:04:47 source=door reader=elevator-lobby badge=otto_g dir=out
2026-10-05T17:05:27 source=door reader=elevator-lobby badge=kenneth_y dir=out
2026-10-05T17:05:31 source=door reader=elevator-lobby badge=bertram_l dir=out
2026-10-05T17:05:33 source=door reader=elevator-lobby badge=rosalind_n dir=out
2026-10-05T17:05:46 source=door reader=elevator-lobby badge=quentin_j dir=out
2026-10-05T17:05:53 source=door reader=elevator-lobby badge=ivo_t dir=out
2026-10-05T17:05:59 source=door reader=elevator-lobby badge=clement_w dir=out
2026-10-06T08:44:55 source=door reader=elevator-lobby badge=hale_r dir=in
2026-10-06T08:51:24 source=door reader=supervisor-office badge=hale_r dir=in
2026-10-06T08:56:14 source=door reader=elevator-lobby badge=eustace_m dir=in
2026-10-06T08:56:23 source=door reader=elevator-lobby badge=rosalind_n dir=in
2026-10-06T08:56:38 source=door reader=dso-office badge=eustace_m dir=in
2026-10-06T08:56:45 source=door reader=as-office badge=rosalind_n dir=in
2026-10-06T08:57:38 source=door reader=elevator-lobby badge=bertram_l dir=in
2026-10-06T08:58:12 source=door reader=dso-office badge=bertram_l dir=in
2026-10-06T08:58:12 source=door reader=elevator-lobby badge=lorna_b dir=in
2026-10-06T08:58:15 source=door reader=elevator-lobby badge=otto_g dir=in
2026-10-06T08:58:19 source=door reader=elevator-lobby badge=agnes_k dir=in
2026-10-06T08:58:26 source=door reader=elevator-lobby badge=vernon_z dir=in
2026-10-06T08:58:38 source=door reader=elevator-lobby badge=gideon_r dir=in
2026-10-06T08:58:46 source=door reader=tc-office badge=lorna_b dir=in
2026-10-06T08:58:48 source=door reader=fold badge=vernon_z dir=in
2026-10-06T08:58:49 source=door reader=elevator-lobby badge=nadia_f dir=in
2026-10-06T08:58:56 source=door reader=dso-office badge=agnes_k dir=in
2026-10-06T08:59:09 source=door reader=as-office badge=otto_g dir=in
2026-10-06T08:59:09 source=door reader=elevator-lobby badge=ursula_x dir=in
2026-10-06T08:59:12 source=door reader=hush-room badge=pruitt_d dir=in
2026-10-06T08:59:14 source=door reader=elevator-lobby badge=prudence_h dir=in
2026-10-06T08:59:17 source=door reader=tc-office badge=gideon_r dir=in
2026-10-06T08:59:21 source=door reader=as-office badge=nadia_f dir=in
2026-10-06T08:59:21 source=door reader=elevator-lobby badge=cyril_a dir=in
2026-10-06T08:59:30 source=door reader=fold badge=ursula_x dir=in
2026-10-06T08:59:36 source=door reader=as-office badge=prudence_h dir=in
2026-10-06T08:59:37 source=door reader=elevator-lobby badge=tobias_u dir=in
2026-10-06T08:59:43 source=door reader=elevator-lobby badge=quentin_j dir=in
2026-10-06T08:59:46 source=door reader=elevator-lobby badge=silas_q dir=in
2026-10-06T09:00:02 source=door reader=fold badge=tobias_u dir=in
2026-10-06T09:00:06 source=door reader=fold badge=silas_q dir=in
2026-10-06T09:00:20 source=door reader=elevator-lobby badge=ivo_t dir=in
2026-10-06T09:00:21 source=door reader=fold badge=cyril_a dir=in
2026-10-06T09:00:41 source=door reader=elevator-lobby badge=clement_w dir=in
2026-10-06T09:00:43 source=door reader=as-office badge=quentin_j dir=in
2026-10-06T09:00:45 source=door reader=elevator-lobby badge=judith_v dir=in
2026-10-06T09:00:55 source=door reader=elevator-lobby badge=harriet_s dir=in
2026-10-06T09:01:05 source=door reader=tc-office badge=ivo_t dir=in
2026-10-06T09:01:09 source=door reader=dso-office badge=clement_w dir=in
2026-10-06T09:01:12 source=door reader=elevator-lobby badge=dorothy_p dir=in
2026-10-06T09:01:36 source=door reader=tc-office badge=judith_v dir=in
2026-10-06T09:01:44 source=door reader=tc-office badge=harriet_s dir=in
2026-10-06T09:01:45 source=door reader=dso-office badge=dorothy_p dir=in
2026-10-06T09:01:46 source=door reader=elevator-lobby badge=winifred_e dir=in
2026-10-06T09:01:55 source=door reader=elevator-lobby badge=fern_o dir=in
2026-10-06T09:02:14 source=door reader=fold badge=winifred_e dir=in
2026-10-06T09:02:21 source=door reader=dso-office badge=fern_o dir=in
2026-10-06T09:02:50 source=door reader=elevator-lobby badge=milo_d dir=in
2026-10-06T09:03:18 source=door reader=as-office badge=milo_d dir=in
2026-10-06T09:03:56 source=door reader=elevator-lobby badge=kenneth_y dir=in
2026-10-06T09:04:24 source=door reader=tc-office badge=kenneth_y dir=in
2026-10-06T09:47:51 source=door reader=supply-room-b badge=clement_w dir=in
2026-10-06T10:34:43 source=door reader=supply-room-b badge=tobias_u dir=in
2026-10-06T10:37:42 source=door reader=supply-room-b badge=eustace_m dir=in
2026-10-06T10:45:01 source=door reader=supply-room-b badge=prudence_h dir=in
2026-10-06T11:03:34 source=door reader=supply-room-b badge=harriet_s dir=in
2026-10-06T11:49:22 source=door reader=supply-room-b badge=silas_q dir=in
2026-10-06T12:03:02 source=door reader=break-room-1 badge=judith_v dir=in
2026-10-06T12:03:35 source=door reader=break-room-1 badge=agnes_k dir=in
2026-10-06T12:05:40 source=door reader=break-room-1 badge=gideon_r dir=in
2026-10-06T12:12:38 source=door reader=break-room-1 badge=tobias_u dir=in
2026-10-06T12:14:56 source=door reader=break-room-1 badge=otto_g dir=in
2026-10-06T12:15:13 source=door reader=break-room-1 badge=eustace_m dir=in
2026-10-06T12:15:27 source=door reader=break-room-1 badge=cyril_a dir=in
2026-10-06T12:17:37 source=door reader=break-room-1 badge=milo_d dir=in
2026-10-06T12:19:08 source=door reader=break-room-1 badge=winifred_e dir=in
2026-10-06T12:19:19 source=door reader=break-room-1 badge=silas_q dir=in
2026-10-06T12:21:03 source=door reader=break-room-1 badge=lorna_b dir=in
2026-10-06T12:22:16 source=door reader=break-room-1 badge=kenneth_y dir=in
2026-10-06T12:22:41 source=door reader=elevator-lobby badge=agnes_k dir=in
2026-10-06T12:24:10 source=door reader=break-room-1 badge=dorothy_p dir=in
2026-10-06T12:24:59 source=door reader=break-room-1 badge=fern_o dir=in
2026-10-06T12:27:05 source=door reader=break-room-1 badge=harriet_s dir=in
2026-10-06T12:27:52 source=door reader=break-room-1 badge=vernon_z dir=in
2026-10-06T12:28:01 source=door reader=break-room-1 badge=quentin_j dir=in
2026-10-06T12:30:03 source=door reader=break-room-1 badge=clement_w dir=in
2026-10-06T12:30:08 source=door reader=break-room-1 badge=prudence_h dir=in
2026-10-06T12:34:28 source=door reader=supply-room-b badge=quentin_j dir=in
2026-10-06T12:36:33 source=door reader=break-room-1 badge=nadia_f dir=in
2026-10-06T12:37:38 source=door reader=break-room-1 badge=bertram_l dir=in
2026-10-06T12:37:44 source=door reader=break-room-1 badge=ivo_t dir=in
2026-10-06T12:38:02 source=door reader=break-room-1 badge=rosalind_n dir=in
2026-10-06T12:39:27 source=door reader=break-room-1 badge=ursula_x dir=in
2026-10-06T12:42:02 source=door reader=supply-room-b badge=clement_w dir=in
2026-10-06T13:26:02 source=door reader=supply-room-b badge=otto_g dir=in
2026-10-06T13:42:47 source=door reader=supply-room-b badge=ivo_t dir=in
2026-10-06T13:55:40 source=door reader=supply-room-b badge=ursula_x dir=in
2026-10-06T14:01:10 source=door reader=supply-room-b badge=bertram_l dir=in
2026-10-06T14:12:51 source=door reader=supply-room-b badge=dorothy_p dir=in
2026-10-06T15:00:10 source=door reader=elevator-lobby badge=agnes_k dir=in
2026-10-06T15:21:46 source=door reader=supply-room-b badge=bertram_l dir=in
2026-10-06T17:00:08 source=door reader=elevator-lobby badge=rosalind_n dir=out
2026-10-06T17:00:10 source=door reader=elevator-lobby badge=milo_d dir=out
2026-10-06T17:00:13 source=door reader=elevator-lobby badge=otto_g dir=out
2026-10-06T17:00:38 source=door reader=elevator-lobby badge=clement_w dir=out
2026-10-06T17:00:40 source=door reader=elevator-lobby badge=bertram_l dir=out
2026-10-06T17:00:43 source=door reader=elevator-lobby badge=judith_v dir=out
2026-10-06T17:01:02 source=door reader=elevator-lobby badge=eustace_m dir=out
2026-10-06T17:01:09 source=door reader=elevator-lobby badge=ivo_t dir=out
2026-10-06T17:01:51 source=door reader=elevator-lobby badge=nadia_f dir=out
2026-10-06T17:02:52 source=door reader=elevator-lobby badge=ursula_x dir=out
2026-10-06T17:02:59 source=door reader=elevator-lobby badge=harriet_s dir=out
2026-10-06T17:03:10 source=door reader=elevator-lobby badge=agnes_k dir=out
2026-10-06T17:03:23 source=door reader=elevator-lobby badge=dorothy_p dir=out
2026-10-06T17:03:33 source=door reader=elevator-lobby badge=gideon_r dir=out
2026-10-06T17:03:42 source=door reader=elevator-lobby badge=quentin_j dir=out
2026-10-06T17:04:02 source=door reader=elevator-lobby badge=silas_q dir=out
2026-10-06T17:04:11 source=door reader=elevator-lobby badge=cyril_a dir=out
2026-10-06T17:04:27 source=door reader=elevator-lobby badge=tobias_u dir=out
2026-10-06T17:04:43 source=door reader=elevator-lobby badge=lorna_b dir=out
2026-10-06T17:04:59 source=door reader=elevator-lobby badge=prudence_h dir=out
2026-10-06T17:05:04 source=door reader=elevator-lobby badge=fern_o dir=out
2026-10-06T17:05:08 source=door reader=elevator-lobby badge=winifred_e dir=out
2026-10-06T17:05:10 source=door reader=elevator-lobby badge=vernon_z dir=out
2026-10-06T17:05:55 source=door reader=elevator-lobby badge=kenneth_y dir=out
2026-10-07T08:43:48 source=door reader=elevator-lobby badge=hale_r dir=in
2026-10-07T08:51:45 source=door reader=supervisor-office badge=hale_r dir=in
2026-10-07T08:52:24 source=door reader=hush-room badge=pruitt_d dir=in
2026-10-07T08:56:17 source=door reader=elevator-lobby badge=ursula_x dir=in
2026-10-07T08:56:33 source=door reader=elevator-lobby badge=eustace_m dir=in
2026-10-07T08:56:46 source=door reader=elevator-lobby badge=lorna_b dir=in
2026-10-07T08:56:58 source=door reader=fold badge=ursula_x dir=in
2026-10-07T08:57:07 source=door reader=tc-office badge=lorna_b dir=in
2026-10-07T08:57:15 source=door reader=dso-office badge=eustace_m dir=in
2026-10-07T08:58:08 source=door reader=elevator-lobby badge=clement_w dir=in
2026-10-07T08:58:21 source=door reader=elevator-lobby badge=rosalind_n dir=in
2026-10-07T08:58:26 source=door reader=elevator-lobby badge=agnes_k dir=in
2026-10-07T08:58:35 source=door reader=elevator-lobby badge=ivo_t dir=in
2026-10-07T08:58:39 source=door reader=elevator-lobby badge=bertram_l dir=in
2026-10-07T08:59:03 source=door reader=dso-office badge=clement_w dir=in
2026-10-07T08:59:06 source=door reader=elevator-lobby badge=fern_o dir=in
2026-10-07T08:59:11 source=door reader=elevator-lobby badge=silas_q dir=in
2026-10-07T08:59:15 source=door reader=as-office badge=rosalind_n dir=in
2026-10-07T08:59:16 source=door reader=tc-office badge=ivo_t dir=in
2026-10-07T08:59:26 source=door reader=dso-office badge=agnes_k dir=in
2026-10-07T08:59:30 source=door reader=dso-office badge=bertram_l dir=in
2026-10-07T08:59:52 source=door reader=dso-office badge=fern_o dir=in
2026-10-07T08:59:53 source=door reader=elevator-lobby badge=judith_v dir=in
2026-10-07T08:59:55 source=door reader=fold badge=silas_q dir=in
2026-10-07T08:59:59 source=door reader=elevator-lobby badge=kenneth_y dir=in
2026-10-07T09:00:21 source=door reader=tc-office badge=judith_v dir=in
2026-10-07T09:00:22 source=door reader=elevator-lobby badge=harriet_s dir=in
2026-10-07T09:00:27 source=door reader=elevator-lobby badge=gideon_r dir=in
2026-10-07T09:00:36 source=door reader=elevator-lobby badge=dorothy_p dir=in
2026-10-07T09:00:40 source=door reader=elevator-lobby badge=otto_g dir=in
2026-10-07T09:00:53 source=door reader=tc-office badge=kenneth_y dir=in
2026-10-07T09:01:02 source=door reader=dso-office badge=dorothy_p dir=in
2026-10-07T09:01:04 source=door reader=tc-office badge=harriet_s dir=in
2026-10-07T09:01:20 source=door reader=elevator-lobby badge=winifred_e dir=in
2026-10-07T09:01:21 source=door reader=tc-office badge=gideon_r dir=in
2026-10-07T09:01:34 source=door reader=elevator-lobby badge=nadia_f dir=in
2026-10-07T09:01:35 source=door reader=as-office badge=otto_g dir=in
2026-10-07T09:01:56 source=door reader=as-office badge=nadia_f dir=in
2026-10-07T09:02:04 source=door reader=elevator-lobby badge=tobias_u dir=in
2026-10-07T09:02:07 source=door reader=elevator-lobby badge=vernon_z dir=in
2026-10-07T09:02:17 source=door reader=fold badge=winifred_e dir=in
2026-10-07T09:02:33 source=door reader=fold badge=tobias_u dir=in
2026-10-07T09:02:33 source=door reader=fold badge=vernon_z dir=in
2026-10-07T09:02:36 source=door reader=elevator-lobby badge=milo_d dir=in
2026-10-07T09:03:10 source=door reader=as-office badge=milo_d dir=in
2026-10-07T09:03:11 source=door reader=elevator-lobby badge=prudence_h dir=in
2026-10-07T09:03:33 source=door reader=as-office badge=prudence_h dir=in
2026-10-07T09:03:50 source=door reader=elevator-lobby badge=quentin_j dir=in
2026-10-07T09:03:54 source=door reader=elevator-lobby badge=cyril_a dir=in
2026-10-07T09:04:15 source=door reader=as-office badge=quentin_j dir=in
2026-10-07T09:04:40 source=door reader=fold badge=cyril_a dir=in
2026-10-07T10:35:40 source=door reader=elevator-lobby badge=agnes_k dir=in
2026-10-07T10:36:38 source=door reader=supply-room-b badge=fern_o dir=in
2026-10-07T10:47:25 source=door reader=supply-room-b badge=lorna_b dir=in
2026-10-07T10:57:40 source=door reader=supply-room-b badge=tobias_u dir=in
2026-10-07T11:02:56 source=door reader=supply-room-b badge=eustace_m dir=in
2026-10-07T12:02:01 source=door reader=break-room-1 badge=agnes_k dir=in
2026-10-07T12:04:09 source=door reader=break-room-1 badge=rosalind_n dir=in
2026-10-07T12:13:30 source=door reader=break-room-1 badge=cyril_a dir=in
2026-10-07T12:15:12 source=door reader=break-room-1 badge=fern_o dir=in
2026-10-07T12:16:01 source=door reader=break-room-1 badge=clement_w dir=in
2026-10-07T12:17:10 source=door reader=break-room-1 badge=tobias_u dir=in
2026-10-07T12:17:23 source=door reader=break-room-1 badge=eustace_m dir=in
2026-10-07T12:18:19 source=door reader=break-room-1 badge=ivo_t dir=in
2026-10-07T12:22:23 source=door reader=break-room-1 badge=milo_d dir=in
2026-10-07T12:23:14 source=door reader=break-room-1 badge=quentin_j dir=in
2026-10-07T12:23:18 source=door reader=break-room-1 badge=gideon_r dir=in
2026-10-07T12:24:32 source=door reader=break-room-1 badge=nadia_f dir=in
2026-10-07T12:25:23 source=door reader=break-room-1 badge=dorothy_p dir=in
2026-10-07T12:25:26 source=door reader=break-room-1 badge=judith_v dir=in
2026-10-07T12:27:08 source=door reader=break-room-1 badge=ursula_x dir=in
2026-10-07T12:29:44 source=door reader=break-room-1 badge=harriet_s dir=in
2026-10-07T12:30:35 source=door reader=break-room-1 badge=otto_g dir=in
2026-10-07T12:36:14 source=door reader=break-room-1 badge=silas_q dir=in
2026-10-07T12:37:09 source=door reader=break-room-1 badge=vernon_z dir=in
2026-10-07T12:37:43 source=door reader=break-room-1 badge=prudence_h dir=in
2026-10-07T12:37:49 source=door reader=break-room-1 badge=winifred_e dir=in
2026-10-07T12:38:16 source=door reader=break-room-1 badge=lorna_b dir=in
2026-10-07T12:38:58 source=door reader=break-room-1 badge=bertram_l dir=in
2026-10-07T12:39:15 source=door reader=break-room-1 badge=kenneth_y dir=in
2026-10-07T13:01:26 source=door reader=supply-room-b badge=ursula_x dir=in
2026-10-07T13:05:57 source=door reader=supply-room-b badge=otto_g dir=in
2026-10-07T13:41:09 source=door reader=supply-room-b badge=agnes_k dir=in
2026-10-07T13:46:59 source=door reader=supply-room-b badge=prudence_h dir=in
2026-10-07T15:17:04 source=door reader=supply-room-b badge=bertram_l dir=in
2026-10-07T17:00:06 source=door reader=elevator-lobby badge=bertram_l dir=out
2026-10-07T17:00:10 source=door reader=elevator-lobby badge=clement_w dir=out
2026-10-07T17:00:18 source=door reader=elevator-lobby badge=otto_g dir=out
2026-10-07T17:00:20 source=door reader=elevator-lobby badge=milo_d dir=out
2026-10-07T17:00:47 source=door reader=elevator-lobby badge=ivo_t dir=out
2026-10-07T17:00:55 source=door reader=elevator-lobby badge=winifred_e dir=out
2026-10-07T17:00:58 source=door reader=elevator-lobby badge=tobias_u dir=out
2026-10-07T17:01:12 source=door reader=elevator-lobby badge=cyril_a dir=out
2026-10-07T17:01:28 source=door reader=elevator-lobby badge=ursula_x dir=out
2026-10-07T17:01:44 source=door reader=elevator-lobby badge=dorothy_p dir=out
2026-10-07T17:01:45 source=door reader=elevator-lobby badge=agnes_k dir=out
2026-10-07T17:02:16 source=door reader=elevator-lobby badge=prudence_h dir=out
2026-10-07T17:02:19 source=door reader=elevator-lobby badge=fern_o dir=out
2026-10-07T17:02:39 source=door reader=elevator-lobby badge=rosalind_n dir=out
2026-10-07T17:02:57 source=door reader=elevator-lobby badge=silas_q dir=out
2026-10-07T17:03:12 source=door reader=elevator-lobby badge=quentin_j dir=out
2026-10-07T17:03:39 source=door reader=elevator-lobby badge=kenneth_y dir=out
2026-10-07T17:03:44 source=door reader=elevator-lobby badge=nadia_f dir=out
2026-10-07T17:03:58 source=door reader=elevator-lobby badge=gideon_r dir=out
2026-10-07T17:04:03 source=door reader=elevator-lobby badge=vernon_z dir=out
2026-10-07T17:04:19 source=door reader=elevator-lobby badge=lorna_b dir=out
2026-10-07T17:04:28 source=door reader=elevator-lobby badge=eustace_m dir=out
2026-10-07T17:04:28 source=door reader=elevator-lobby badge=judith_v dir=out
2026-10-07T17:05:09 source=door reader=elevator-lobby badge=harriet_s dir=out
2026-10-08T08:46:45 source=door reader=supervisor-office badge=hale_r dir=in
2026-10-08T08:49:11 source=door reader=elevator-lobby badge=hale_r dir=in
2026-10-08T08:56:12 source=door reader=elevator-lobby badge=nadia_f dir=in
2026-10-08T08:56:20 source=door reader=elevator-lobby badge=clement_w dir=in
2026-10-08T08:56:28 source=door reader=elevator-lobby badge=eustace_m dir=in
2026-10-08T08:56:33 source=door reader=as-office badge=nadia_f dir=in
2026-10-08T08:56:36 source=door reader=elevator-lobby badge=agnes_k dir=in
2026-10-08T08:56:39 source=door reader=hush-room badge=pruitt_d dir=in
2026-10-08T08:56:55 source=door reader=elevator-lobby badge=milo_d dir=in
2026-10-08T08:56:59 source=door reader=dso-office badge=clement_w dir=in
2026-10-08T08:57:02 source=door reader=dso-office badge=agnes_k dir=in
2026-10-08T08:57:12 source=door reader=elevator-lobby badge=gideon_r dir=in
2026-10-08T08:57:15 source=door reader=dso-office badge=eustace_m dir=in
2026-10-08T08:57:36 source=door reader=tc-office badge=gideon_r dir=in
2026-10-08T08:57:36 source=door reader=as-office badge=milo_d dir=in
2026-10-08T08:57:43 source=door reader=elevator-lobby badge=bertram_l dir=in
2026-10-08T08:58:29 source=door reader=dso-office badge=bertram_l dir=in
2026-10-08T08:59:30 source=door reader=elevator-lobby badge=rosalind_n dir=in
2026-10-08T08:59:44 source=door reader=elevator-lobby badge=dorothy_p dir=in
2026-10-08T08:59:44 source=door reader=elevator-lobby badge=ivo_t dir=in
2026-10-08T08:59:52 source=door reader=as-office badge=rosalind_n dir=in
2026-10-08T09:00:02 source=door reader=elevator-lobby badge=ursula_x dir=in
2026-10-08T09:00:08 source=door reader=tc-office badge=ivo_t dir=in
2026-10-08T09:00:13 source=door reader=dso-office badge=dorothy_p dir=in
2026-10-08T09:00:18 source=door reader=elevator-lobby badge=judith_v dir=in
2026-10-08T09:00:29 source=door reader=elevator-lobby badge=harriet_s dir=in
2026-10-08T09:00:29 source=door reader=elevator-lobby badge=silas_q dir=in
2026-10-08T09:00:44 source=door reader=tc-office badge=judith_v dir=in
2026-10-08T09:00:46 source=door reader=fold badge=ursula_x dir=in
2026-10-08T09:00:55 source=door reader=elevator-lobby badge=winifred_e dir=in
2026-10-08T09:01:05 source=door reader=fold badge=silas_q dir=in
2026-10-08T09:01:13 source=door reader=elevator-lobby badge=fern_o dir=in
2026-10-08T09:01:16 source=door reader=elevator-lobby badge=lorna_b dir=in
2026-10-08T09:01:17 source=door reader=elevator-lobby badge=cyril_a dir=in
2026-10-08T09:01:26 source=door reader=tc-office badge=harriet_s dir=in
2026-10-08T09:01:36 source=door reader=fold badge=winifred_e dir=in
2026-10-08T09:01:44 source=door reader=fold badge=cyril_a dir=in
2026-10-08T09:02:00 source=door reader=dso-office badge=fern_o dir=in
2026-10-08T09:02:03 source=door reader=elevator-lobby badge=otto_g dir=in
2026-10-08T09:02:05 source=door reader=tc-office badge=lorna_b dir=in
2026-10-08T09:02:52 source=door reader=as-office badge=otto_g dir=in
2026-10-08T09:02:53 source=door reader=elevator-lobby badge=tobias_u dir=in
2026-10-08T09:03:02 source=door reader=elevator-lobby badge=quentin_j dir=in
2026-10-08T09:03:32 source=door reader=fold badge=tobias_u dir=in
2026-10-08T09:03:49 source=door reader=elevator-lobby badge=kenneth_y dir=in
2026-10-08T09:03:55 source=door reader=elevator-lobby badge=prudence_h dir=in
2026-10-08T09:03:57 source=door reader=elevator-lobby badge=vernon_z dir=in
2026-10-08T09:04:01 source=door reader=as-office badge=quentin_j dir=in
2026-10-08T09:04:20 source=door reader=tc-office badge=kenneth_y dir=in
2026-10-08T09:04:38 source=door reader=as-office badge=prudence_h dir=in
2026-10-08T09:04:55 source=door reader=fold badge=vernon_z dir=in
2026-10-08T09:14:40 source=door reader=supervisor-office badge=bertram_l dir=in
2026-10-08T09:31:02 source=door reader=supervisor-office badge=bertram_l dir=out
2026-10-08T10:00:18 source=door reader=supply-room-b badge=ursula_x dir=in
2026-10-08T10:19:11 source=door reader=supply-room-b badge=rosalind_n dir=in
2026-10-08T10:21:41 source=door reader=elevator-lobby badge=agnes_k dir=in
2026-10-08T11:07:57 source=door reader=supply-room-b badge=vernon_z dir=in
2026-10-08T11:52:59 source=door reader=supply-room-b badge=winifred_e dir=in
2026-10-08T11:59:44 source=door reader=supply-room-b badge=milo_d dir=in
2026-10-08T12:00:13 source=door reader=break-room-1 badge=ursula_x dir=in
2026-10-08T12:00:27 source=door reader=break-room-1 badge=clement_w dir=in
2026-10-08T12:02:37 source=door reader=break-room-1 badge=judith_v dir=in
2026-10-08T12:03:32 source=door reader=break-room-1 badge=harriet_s dir=in
2026-10-08T12:03:41 source=door reader=break-room-1 badge=lorna_b dir=in
2026-10-08T12:07:46 source=door reader=break-room-1 badge=kenneth_y dir=in
2026-10-08T12:08:17 source=door reader=supply-room-b badge=gideon_r dir=in
2026-10-08T12:10:17 source=door reader=break-room-1 badge=quentin_j dir=in
2026-10-08T12:10:49 source=door reader=break-room-1 badge=eustace_m dir=in
2026-10-08T12:16:10 source=door reader=break-room-1 badge=winifred_e dir=in
2026-10-08T12:18:51 source=door reader=break-room-1 badge=vernon_z dir=in
2026-10-08T12:19:16 source=door reader=break-room-1 badge=otto_g dir=in
2026-10-08T12:19:23 source=door reader=break-room-1 badge=tobias_u dir=in
2026-10-08T12:22:54 source=door reader=break-room-1 badge=fern_o dir=in
2026-10-08T12:24:09 source=door reader=supply-room-b badge=prudence_h dir=in
2026-10-08T12:24:11 source=door reader=break-room-1 badge=silas_q dir=in
2026-10-08T12:26:38 source=door reader=break-room-1 badge=cyril_a dir=in
2026-10-08T12:28:34 source=door reader=break-room-1 badge=bertram_l dir=in
2026-10-08T12:31:06 source=door reader=break-room-1 badge=gideon_r dir=in
2026-10-08T12:31:28 source=door reader=break-room-1 badge=prudence_h dir=in
2026-10-08T12:32:13 source=door reader=break-room-1 badge=milo_d dir=in
2026-10-08T12:32:52 source=door reader=break-room-1 badge=nadia_f dir=in
2026-10-08T12:34:01 source=door reader=break-room-1 badge=rosalind_n dir=in
2026-10-08T12:34:03 source=door reader=break-room-1 badge=dorothy_p dir=in
2026-10-08T12:34:18 source=door reader=break-room-1 badge=agnes_k dir=in
2026-10-08T12:36:55 source=door reader=break-room-1 badge=ivo_t dir=in
2026-10-08T12:47:48 source=door reader=elevator-lobby badge=agnes_k dir=in
2026-10-08T14:18:50 source=door reader=supply-room-b badge=bertram_l dir=in
2026-10-08T14:23:51 source=door reader=supply-room-b badge=eustace_m dir=in
2026-10-08T14:28:40 source=door reader=supply-room-b badge=judith_v dir=in
2026-10-08T14:59:20 source=door reader=break-room-2 badge=agnes_k dir=in
2026-10-08T14:59:24 source=door reader=break-room-2 badge=bertram_l dir=in
2026-10-08T14:59:31 source=door reader=break-room-2 badge=clement_w dir=in
2026-10-08T14:59:33 source=door reader=break-room-2 badge=dorothy_p dir=in
2026-10-08T14:59:40 source=door reader=break-room-2 badge=eustace_m dir=in
2026-10-08T14:59:44 source=door reader=break-room-2 badge=fern_o dir=in
2026-10-08T14:59:58 source=door reader=break-room-2 badge=hale_r dir=in
2026-10-08T15:01:12 source=door reader=break-room-2 badge=hale_r dir=out
2026-10-08T15:01:22 source=trace span=corridor-e badge=hale_r trace_id=7f3a91 dur_ms=6100
2026-10-08T15:01:28 source=door reader=elevator-lobby badge=hale_r dir=in
2026-10-08T15:01:30 source=elevator-reader badge=hale_r event=badge_in_car clock=ok
2026-10-08T15:01:40 source=door reader=break-room-2 badge=bertram_l dir=out
2026-10-08T15:01:45 source=door reader=supply-room-b badge=bertram_l dir=in
2026-10-08T15:02:00 source=door reader=* event=reader_offline reason=main_power_lost
2026-10-08T15:05:30 source=elevator-reader badge=agnes_k event=badge_in_car clock=LOST est_error_s=±120 ts_basis=uptime ingested_at=2026-10-08T15:07:41
2026-10-08T15:07:00 source=door reader=* event=reader_online
2026-10-08T15:09:12 source=door reader=elevator-lobby badge=okonjo_a dir=in
2026-10-08T15:09:40 source=door reader=elevator-lobby badge=pruitt_d dir=in
```


---

# Floor Chat (2026-09-24 to 2026-10-08)

Floor chat messages. Direct messages show `to=<badge>`; channel messages show `to=#channel`.

```text
2026-09-24T10:05:50 source=chat from=kenneth_y to=#tonal-compliance msg="anyone have a spare eye mask"
2026-09-24T10:23:44 source=chat from=silas_q to=#flock-keeping msg="is it cocoa day or is that next week"
2026-09-24T11:03:17 source=chat from=ivo_t to=#tonal-compliance msg="anyone have a spare eye mask"
2026-09-24T11:27:53 source=chat from=gideon_r to=#tonal-compliance msg="Gideon, did you finish 52?"
2026-09-24T11:34:04 source=chat from=quentin_j to=#archival-sorting msg="almost at quota, keep going everyone"
2026-09-24T12:02:49 source=chat from=quentin_j to=#archival-sorting msg="I've been counting the same column for an hour"
2026-09-24T12:22:25 source=chat from=bertram_l to=agnes_k msg="you're the worst"
2026-09-24T12:22:39 source=chat from=lorna_b to=#tonal-compliance msg="anyone have a spare eye mask"
2026-09-24T12:40:14 source=chat from=otto_g to=#archival-sorting msg="the sheep were loud this morning"
2026-09-24T13:13:21 source=chat from=clement_w to=#deep-sleep-operations msg="Vernon, did you finish 7?"
2026-09-24T13:51:52 source=chat from=harriet_s to=#tonal-compliance msg="printer's jammed again. it's always jammed."
2026-09-24T13:53:58 source=chat from=judith_v to=#tonal-compliance msg="lunch?"
2026-09-24T14:20:47 source=chat from=fern_o to=#deep-sleep-operations msg="the numbers in file 48 are fuzzy today"
2026-09-24T16:43:08 source=chat from=harriet_s to=#tonal-compliance msg="does anyone know what Tonal Compliance actually does"
2026-09-24T16:46:29 source=chat from=ivo_t to=#tonal-compliance msg="who keeps moving my pencil cup"
2026-09-25T09:49:46 source=chat from=prudence_h to=#archival-sorting msg="printer's jammed again. it's always jammed."
2026-09-25T10:03:36 source=chat from=ivo_t to=#tonal-compliance msg="is it cocoa day or is that next week"
2026-09-25T10:06:16 source=chat from=silas_q to=#flock-keeping msg="who keeps moving my pencil cup"
2026-09-25T10:30:31 source=chat from=clement_w to=#deep-sleep-operations msg="does anyone know what Tonal Compliance actually does"
2026-09-25T10:52:32 source=chat from=lorna_b to=#tonal-compliance msg="rest well"
2026-09-25T10:54:33 source=chat from=dorothy_p to=#deep-sleep-operations msg="Gideon, did you finish 50?"
2026-09-25T11:06:59 source=chat from=winifred_e to=#flock-keeping msg="rest well"
2026-09-25T13:07:05 source=chat from=tobias_u to=#flock-keeping msg="almost at quota, keep going everyone"
2026-09-25T13:49:51 source=chat from=gideon_r to=#tonal-compliance msg="rest well"
2026-09-25T14:35:56 source=chat from=bertram_l to=agnes_k msg="ha. thanks."
2026-09-25T15:09:06 source=chat from=lorna_b to=#tonal-compliance msg="the sheep were loud this morning"
2026-09-25T15:28:05 source=chat from=harriet_s to=#tonal-compliance msg="4 minutes to break"
2026-09-25T15:34:48 source=chat from=fern_o to=#deep-sleep-operations msg="I've been counting the same column for an hour"
2026-09-25T15:52:26 source=chat from=fern_o to=bertram_l msg="Bertram where did you go, you missed the pancake bar"
2026-09-25T16:30:12 source=chat from=silas_q to=#flock-keeping msg="Winifred, did you finish 29?"
2026-09-25T16:39:43 source=chat from=tobias_u to=#flock-keeping msg="anyone have a spare eye mask"
2026-09-28T09:27:53 source=chat from=kenneth_y to=#tonal-compliance msg="4 minutes to break"
2026-09-28T09:43:12 source=chat from=agnes_k to=#deep-sleep-operations msg="Ms. Pruitt asked me what my favorite color is. I didn't know."
2026-09-28T11:14:26 source=chat from=vernon_z to=#flock-keeping msg="I've been counting the same column for an hour"
2026-09-28T11:43:49 source=chat from=clement_w to=#deep-sleep-operations msg="the numbers in file 89 are fuzzy today"
2026-09-28T11:56:08 source=chat from=fern_o to=#deep-sleep-operations msg="lunch?"
2026-09-28T11:56:51 source=chat from=silas_q to=#flock-keeping msg="anyone have a spare eye mask"
2026-09-28T12:05:06 source=chat from=eustace_m to=bertram_l msg="Bertram you left your mug on my desk"
2026-09-28T12:41:00 source=chat from=agnes_k to=#deep-sleep-operations msg="lunch?"
2026-09-28T13:16:15 source=chat from=nadia_f to=#archival-sorting msg="rest well"
2026-09-28T13:25:27 source=chat from=quentin_j to=#archival-sorting msg="anyone have a spare eye mask"
2026-09-28T13:33:12 source=chat from=milo_d to=#archival-sorting msg="anyone have a spare eye mask"
2026-09-28T13:37:28 source=chat from=quentin_j to=#archival-sorting msg="Bertram, did you finish 9?"
2026-09-28T14:43:36 source=chat from=fern_o to=#deep-sleep-operations msg="who keeps moving my pencil cup"
2026-09-28T15:08:12 source=chat from=fern_o to=#deep-sleep-operations msg="printer's jammed again. it's always jammed."
2026-09-28T15:34:30 source=chat from=otto_g to=#archival-sorting msg="the numbers in file 83 are fuzzy today"
2026-09-29T09:13:37 source=chat from=prudence_h to=#archival-sorting msg="my chair squeaks. it didn't used to squeak."
2026-09-29T09:51:32 source=chat from=gideon_r to=#tonal-compliance msg="my chair squeaks. it didn't used to squeak."
2026-09-29T11:59:18 source=chat from=quentin_j to=#archival-sorting msg="does anyone know what Tonal Compliance actually does"
2026-09-29T12:23:44 source=chat from=judith_v to=#tonal-compliance msg="Ms. Pruitt asked me what my favorite color is. I didn't know."
2026-09-29T12:44:30 source=chat from=lorna_b to=#tonal-compliance msg="rest well"
2026-09-29T12:44:36 source=chat from=ivo_t to=#tonal-compliance msg="almost at quota, keep going everyone"
2026-09-29T12:50:06 source=chat from=ursula_x to=#flock-keeping msg="Ms. Pruitt asked me what my favorite color is. I didn't know."
2026-09-29T13:56:07 source=chat from=rosalind_n to=#archival-sorting msg="my chair squeaks. it didn't used to squeak."
2026-09-29T13:58:01 source=chat from=bertram_l to=#deep-sleep-operations msg="the numbers in file 61 are fuzzy today"
2026-09-29T14:37:27 source=chat from=gideon_r to=#tonal-compliance msg="the sheep were loud this morning"
2026-09-29T14:44:18 source=chat from=rosalind_n to=#archival-sorting msg="anyone have a spare eye mask"
2026-09-29T15:24:10 source=chat from=dorothy_p to=bertram_l msg="Bertram, can you pass me the ruler"
2026-09-29T15:38:57 source=chat from=quentin_j to=#archival-sorting msg="Cyril, did you finish 5?"
2026-09-29T15:57:13 source=chat from=winifred_e to=#flock-keeping msg="who drew the eagle on the whiteboard"
2026-09-29T16:23:54 source=chat from=harriet_s to=#tonal-compliance msg="rest well"
2026-09-30T09:11:45 source=chat from=otto_g to=#archival-sorting msg="lunch?"
2026-09-30T09:26:28 source=chat from=silas_q to=#flock-keeping msg="the numbers in file 99 are fuzzy today"
2026-09-30T10:01:57 source=chat from=otto_g to=#archival-sorting msg="almost at quota, keep going everyone"
2026-09-30T10:02:38 source=chat from=prudence_h to=#archival-sorting msg="the numbers in file 48 are fuzzy today"
2026-09-30T10:17:19 source=chat from=hale_r to=bertram_l msg="Bertram, see me at 9:15."
2026-09-30T10:19:00 source=chat from=prudence_h to=#archival-sorting msg="4 minutes to break"
2026-09-30T10:22:41 source=chat from=vernon_z to=#flock-keeping msg="the numbers in file 73 are fuzzy today"
2026-09-30T11:11:06 source=chat from=milo_d to=#archival-sorting msg="almost at quota, keep going everyone"
2026-09-30T12:52:49 source=chat from=vernon_z to=#flock-keeping msg="printer's jammed again. it's always jammed."
2026-09-30T13:47:26 source=chat from=ivo_t to=#tonal-compliance msg="I've been counting the same column for an hour"
2026-09-30T14:31:19 source=chat from=clement_w to=#deep-sleep-operations msg="my chair squeaks. it didn't used to squeak."
2026-09-30T15:39:59 source=chat from=milo_d to=#archival-sorting msg="anyone have a spare eye mask"
2026-09-30T15:56:52 source=chat from=otto_g to=#archival-sorting msg="the sheep were loud this morning"
2026-09-30T15:57:51 source=chat from=ursula_x to=#flock-keeping msg="rest well"
2026-09-30T15:58:05 source=chat from=otto_g to=#archival-sorting msg="almost at quota, keep going everyone"
2026-10-01T09:11:16 source=chat from=cyril_a to=#flock-keeping msg="anyone have a spare eye mask"
2026-10-01T09:19:35 source=chat from=ursula_x to=#flock-keeping msg="almost at quota, keep going everyone"
2026-10-01T09:28:08 source=chat from=eustace_m to=#deep-sleep-operations msg="lunch?"
2026-10-01T10:32:22 source=chat from=silas_q to=#flock-keeping msg="who keeps moving my pencil cup"
2026-10-01T11:17:01 source=chat from=judith_v to=#tonal-compliance msg="lunch?"
2026-10-01T11:49:23 source=chat from=bertram_l to=fern_o msg="ha. thanks."
2026-10-01T12:35:09 source=chat from=vernon_z to=#flock-keeping msg="who keeps moving my pencil cup"
2026-10-01T13:01:20 source=chat from=gideon_r to=#tonal-compliance msg="Ms. Pruitt asked me what my favorite color is. I didn't know."
2026-10-01T13:02:56 source=chat from=fern_o to=#deep-sleep-operations msg="anyone have a spare eye mask"
2026-10-01T13:54:26 source=chat from=agnes_k to=#deep-sleep-operations msg="the numbers in file 77 are fuzzy today"
2026-10-01T14:01:54 source=chat from=otto_g to=#archival-sorting msg="I've been counting the same column for an hour"
2026-10-01T14:09:44 source=chat from=bertram_l to=#deep-sleep-operations msg="Bertram, did you finish 25?"
2026-10-01T14:36:13 source=chat from=kenneth_y to=#tonal-compliance msg="printer's jammed again. it's always jammed."
2026-10-01T15:07:39 source=chat from=silas_q to=#flock-keeping msg="I've been counting the same column for an hour"
2026-10-01T16:36:51 source=chat from=cyril_a to=#flock-keeping msg="lunch?"
2026-10-02T09:55:39 source=chat from=dorothy_p to=#deep-sleep-operations msg="who drew the eagle on the whiteboard"
2026-10-02T10:03:23 source=chat from=judith_v to=#tonal-compliance msg="printer's jammed again. it's always jammed."
2026-10-02T10:15:05 source=chat from=bertram_l to=clement_w msg="one day I'll get you back"
2026-10-02T11:16:04 source=chat from=harriet_s to=#tonal-compliance msg="does anyone know what Tonal Compliance actually does"
2026-10-02T11:33:03 source=chat from=agnes_k to=#deep-sleep-operations msg="lunch?"
2026-10-02T11:42:54 source=chat from=quentin_j to=#archival-sorting msg="Fern, did you finish 96?"
2026-10-02T12:00:12 source=chat from=judith_v to=#tonal-compliance msg="who keeps moving my pencil cup"
2026-10-02T12:25:35 source=chat from=prudence_h to=#archival-sorting msg="I've been counting the same column for an hour"
2026-10-02T12:49:06 source=chat from=cyril_a to=#flock-keeping msg="4 minutes to break"
2026-10-02T13:00:50 source=chat from=agnes_k to=bertram_l msg="Bertram, are you coming to lunch?"
2026-10-02T13:05:29 source=chat from=harriet_s to=#tonal-compliance msg="I've been counting the same column for an hour"
2026-10-02T13:24:50 source=chat from=tobias_u to=#flock-keeping msg="does anyone know what Tonal Compliance actually does"
2026-10-02T14:44:52 source=chat from=agnes_k to=#deep-sleep-operations msg="almost at quota, keep going everyone"
2026-10-02T14:50:54 source=chat from=prudence_h to=#archival-sorting msg="is it cocoa day or is that next week"
2026-10-02T14:55:41 source=chat from=ursula_x to=#flock-keeping msg="the numbers in file 8 are fuzzy today"
2026-10-02T16:01:09 source=chat from=ursula_x to=#flock-keeping msg="lunch?"
2026-10-05T09:15:45 source=chat from=kenneth_y to=#tonal-compliance msg="printer's jammed again. it's always jammed."
2026-10-05T09:17:16 source=chat from=prudence_h to=#archival-sorting msg="printer's jammed again. it's always jammed."
2026-10-05T09:57:03 source=chat from=dorothy_p to=#deep-sleep-operations msg="4 minutes to break"
2026-10-05T10:36:50 source=chat from=kenneth_y to=#tonal-compliance msg="Nadia, did you finish 40?"
2026-10-05T10:54:10 source=chat from=milo_d to=#archival-sorting msg="4 minutes to break"
2026-10-05T12:12:25 source=chat from=kenneth_y to=#tonal-compliance msg="who drew the eagle on the whiteboard"
2026-10-05T12:22:14 source=chat from=ivo_t to=#tonal-compliance msg="I've been counting the same column for an hour"
2026-10-05T13:19:11 source=chat from=lorna_b to=#tonal-compliance msg="Dorothy, did you finish 9?"
2026-10-05T14:12:31 source=chat from=vernon_z to=#flock-keeping msg="anyone have a spare eye mask"
2026-10-05T14:30:58 source=chat from=kenneth_y to=#tonal-compliance msg="my chair squeaks. it didn't used to squeak."
2026-10-05T14:39:57 source=chat from=vernon_z to=#flock-keeping msg="lunch?"
2026-10-05T15:27:13 source=chat from=eustace_m to=#deep-sleep-operations msg="the sheep were loud this morning"
2026-10-05T15:28:35 source=chat from=ivo_t to=#tonal-compliance msg="the numbers in file 58 are fuzzy today"
2026-10-05T16:07:42 source=chat from=bertram_l to=#deep-sleep-operations msg="I've been counting the same column for an hour"
2026-10-06T09:20:51 source=chat from=agnes_k to=#deep-sleep-operations msg="Ms. Pruitt asked me what my favorite color is. I didn't know."
2026-10-06T09:41:06 source=chat from=prudence_h to=#archival-sorting msg="almost at quota, keep going everyone"
2026-10-06T10:37:55 source=chat from=winifred_e to=#flock-keeping msg="Harriet, did you finish 63?"
2026-10-06T11:00:22 source=chat from=rosalind_n to=#archival-sorting msg="Ursula, did you finish 48?"
2026-10-06T11:15:23 source=chat from=bertram_l to=agnes_k msg="shh"
2026-10-06T11:16:29 source=chat from=ursula_x to=#flock-keeping msg="almost at quota, keep going everyone"
2026-10-06T12:07:20 source=chat from=tobias_u to=#flock-keeping msg="Fern, did you finish 24?"
2026-10-06T12:33:05 source=chat from=clement_w to=#deep-sleep-operations msg="4 minutes to break"
2026-10-06T12:35:53 source=chat from=dorothy_p to=#deep-sleep-operations msg="who drew the eagle on the whiteboard"
2026-10-06T14:12:48 source=chat from=lorna_b to=#tonal-compliance msg="the numbers in file 85 are fuzzy today"
2026-10-06T14:25:23 source=chat from=eustace_m to=#deep-sleep-operations msg="is it cocoa day or is that next week"
2026-10-06T14:32:53 source=chat from=tobias_u to=#flock-keeping msg="does anyone know what Tonal Compliance actually does"
2026-10-06T14:51:21 source=chat from=lorna_b to=#tonal-compliance msg="printer's jammed again. it's always jammed."
2026-10-06T15:54:34 source=chat from=dorothy_p to=#deep-sleep-operations msg="4 minutes to break"
2026-10-06T16:37:26 source=chat from=lorna_b to=#tonal-compliance msg="is it cocoa day or is that next week"
2026-10-07T09:32:07 source=chat from=ursula_x to=#flock-keeping msg="does anyone know what Tonal Compliance actually does"
2026-10-07T09:38:10 source=chat from=milo_d to=#archival-sorting msg="does anyone know what Tonal Compliance actually does"
2026-10-07T09:49:02 source=chat from=harriet_s to=#tonal-compliance msg="lunch?"
2026-10-07T09:55:43 source=chat from=dorothy_p to=bertram_l msg="Bertram, nice work on 31"
2026-10-07T10:21:12 source=chat from=lorna_b to=#tonal-compliance msg="Ms. Pruitt asked me what my favorite color is. I didn't know."
2026-10-07T10:22:23 source=chat from=lorna_b to=#tonal-compliance msg="printer's jammed again. it's always jammed."
2026-10-07T10:45:40 source=chat from=tobias_u to=#flock-keeping msg="Quentin, did you finish 90?"
2026-10-07T11:12:29 source=chat from=gideon_r to=#tonal-compliance msg="is it cocoa day or is that next week"
2026-10-07T12:00:33 source=chat from=harriet_s to=#tonal-compliance msg="who drew the eagle on the whiteboard"
2026-10-07T12:33:54 source=chat from=lorna_b to=#tonal-compliance msg="Cyril, did you finish 37?"
2026-10-07T13:32:48 source=chat from=eustace_m to=#deep-sleep-operations msg="I've been counting the same column for an hour"
2026-10-07T14:22:55 source=chat from=milo_d to=#archival-sorting msg="Ms. Pruitt asked me what my favorite color is. I didn't know."
2026-10-07T14:59:48 source=chat from=bertram_l to=#deep-sleep-operations msg="the numbers in file 96 are fuzzy today"
2026-10-07T16:25:44 source=chat from=tobias_u to=#flock-keeping msg="the sheep were loud this morning"
2026-10-07T16:40:01 source=chat from=milo_d to=#archival-sorting msg="my chair squeaks. it didn't used to squeak."
2026-10-08T09:38:15 source=chat from=vernon_z to=#flock-keeping msg="4 minutes to break"
2026-10-08T09:40:17 source=chat from=bertram_l to=#deep-sleep-operations msg="fyi Mr. H says he'll be stepping out during the Cocoa Hour, if we ever get one lol. something at the elevator"
2026-10-08T09:40:52 source=chat from=agnes_k to=#deep-sleep-operations msg="the elevator? why the elevator"
2026-10-08T09:41:30 source=chat from=bertram_l to=#deep-sleep-operations msg="dunno. ask him"
2026-10-08T09:42:05 source=chat from=agnes_k to=#deep-sleep-operations msg="never mind. it doesn't matter"
2026-10-08T10:07:45 source=chat from=agnes_k to=#deep-sleep-operations msg="I've been counting the same column for an hour"
2026-10-08T10:29:45 source=chat from=prudence_h to=#archival-sorting msg="my chair squeaks. it didn't used to squeak."
2026-10-08T11:15:35 source=chat from=kenneth_y to=#tonal-compliance msg="anyone have a spare eye mask"
2026-10-08T11:57:30 source=chat from=gideon_r to=#tonal-compliance msg="Ms. Pruitt asked me what my favorite color is. I didn't know."
2026-10-08T12:01:40 source=chat from=silas_q to=#flock-keeping msg="I've been counting the same column for an hour"
2026-10-08T12:19:12 source=chat from=quentin_j to=#archival-sorting msg="my chair squeaks. it didn't used to squeak."
2026-10-08T12:20:00 source=chat from=judith_v to=#tonal-compliance msg="lunch?"
2026-10-08T12:33:14 source=chat from=tobias_u to=#flock-keeping msg="I've been counting the same column for an hour"
2026-10-08T13:10:20 source=chat from=prudence_h to=#archival-sorting msg="my chair squeaks. it didn't used to squeak."
2026-10-08T13:26:28 source=chat from=milo_d to=#archival-sorting msg="does anyone know what Tonal Compliance actually does"
2026-10-08T13:36:15 source=chat from=eustace_m to=#deep-sleep-operations msg="4 minutes to break"
2026-10-08T13:52:44 source=chat from=dorothy_p to=#deep-sleep-operations msg="we're SO close. who's still open?"
2026-10-08T13:53:10 source=chat from=eustace_m to=#deep-sleep-operations msg="still going on mine"
2026-10-08T14:22:39 source=chat from=judith_v to=#tonal-compliance msg="rest well"
2026-10-08T14:25:02 source=chat from=judith_v to=#tonal-compliance msg="the numbers in file 43 are fuzzy today"
2026-10-08T14:31:55 source=chat from=fern_o to=#deep-sleep-operations msg="almost almost almost"
2026-10-08T14:58:13 source=chat from=clement_w to=#deep-sleep-operations msg="Done."
2026-10-08T14:58:20 source=chat from=agnes_k to=#deep-sleep-operations msg="DEFIANT JAZZ"
2026-10-08T15:00:02 source=chat from=hale_r to=#deep-sleep-operations msg="Congratulations, Deep Sleep Operations. Break Room 2. Sweet dreams, Dreamers."
```


---

# Selected Metrics (CSV)

Selected time series. A non-empty `ingested_at` means the sample was buffered on the device and uploaded late.

```csv
ts,metric,labels,value,ingested_at
2026-10-08T13:00:00,quota_file_progress,employee=agnes_k,1.0,
2026-10-08T13:00:00,quota_file_progress,employee=bertram_l,1.0,
2026-10-08T13:00:00,quota_file_progress,employee=clement_w,0.9,
2026-10-08T13:00:00,quota_file_progress,employee=dorothy_p,0.88,
2026-10-08T13:00:00,quota_file_progress,employee=eustace_m,0.88,
2026-10-08T13:00:00,quota_file_progress,employee=fern_o,0.88,
2026-10-08T13:05:00,quota_file_progress,employee=agnes_k,1.0,
2026-10-08T13:05:00,quota_file_progress,employee=bertram_l,1.0,
2026-10-08T13:05:00,quota_file_progress,employee=clement_w,0.904,
2026-10-08T13:05:00,quota_file_progress,employee=dorothy_p,0.885,
2026-10-08T13:05:00,quota_file_progress,employee=eustace_m,0.885,
2026-10-08T13:05:00,quota_file_progress,employee=fern_o,0.885,
2026-10-08T13:10:00,quota_file_progress,employee=agnes_k,1.0,
2026-10-08T13:10:00,quota_file_progress,employee=bertram_l,1.0,
2026-10-08T13:10:00,quota_file_progress,employee=clement_w,0.908,
2026-10-08T13:10:00,quota_file_progress,employee=dorothy_p,0.89,
2026-10-08T13:10:00,quota_file_progress,employee=eustace_m,0.89,
2026-10-08T13:10:00,quota_file_progress,employee=fern_o,0.89,
2026-10-08T13:15:00,quota_file_progress,employee=agnes_k,1.0,
2026-10-08T13:15:00,quota_file_progress,employee=bertram_l,1.0,
2026-10-08T13:15:00,quota_file_progress,employee=clement_w,0.912,
2026-10-08T13:15:00,quota_file_progress,employee=dorothy_p,0.895,
2026-10-08T13:15:00,quota_file_progress,employee=eustace_m,0.895,
2026-10-08T13:15:00,quota_file_progress,employee=fern_o,0.895,
2026-10-08T13:20:00,quota_file_progress,employee=agnes_k,1.0,
2026-10-08T13:20:00,quota_file_progress,employee=bertram_l,1.0,
2026-10-08T13:20:00,quota_file_progress,employee=clement_w,0.916,
2026-10-08T13:20:00,quota_file_progress,employee=dorothy_p,0.9,
2026-10-08T13:20:00,quota_file_progress,employee=eustace_m,0.9,
2026-10-08T13:20:00,quota_file_progress,employee=fern_o,0.9,
2026-10-08T13:25:00,quota_file_progress,employee=agnes_k,1.0,
2026-10-08T13:25:00,quota_file_progress,employee=bertram_l,1.0,
2026-10-08T13:25:00,quota_file_progress,employee=clement_w,0.92,
2026-10-08T13:25:00,quota_file_progress,employee=dorothy_p,0.905,
2026-10-08T13:25:00,quota_file_progress,employee=eustace_m,0.905,
2026-10-08T13:25:00,quota_file_progress,employee=fern_o,0.905,
2026-10-08T13:30:00,quota_file_progress,employee=agnes_k,1.0,
2026-10-08T13:30:00,quota_file_progress,employee=bertram_l,1.0,
2026-10-08T13:30:00,quota_file_progress,employee=clement_w,0.924,
2026-10-08T13:30:00,quota_file_progress,employee=dorothy_p,0.91,
2026-10-08T13:30:00,quota_file_progress,employee=eustace_m,0.91,
2026-10-08T13:30:00,quota_file_progress,employee=fern_o,0.91,
2026-10-08T13:35:00,quota_file_progress,employee=agnes_k,1.0,
2026-10-08T13:35:00,quota_file_progress,employee=bertram_l,1.0,
2026-10-08T13:35:00,quota_file_progress,employee=clement_w,0.928,
2026-10-08T13:35:00,quota_file_progress,employee=dorothy_p,0.915,
2026-10-08T13:35:00,quota_file_progress,employee=eustace_m,0.915,
2026-10-08T13:35:00,quota_file_progress,employee=fern_o,0.915,
2026-10-08T13:40:00,quota_file_progress,employee=agnes_k,1.0,
2026-10-08T13:40:00,quota_file_progress,employee=bertram_l,1.0,
2026-10-08T13:40:00,quota_file_progress,employee=clement_w,0.932,
2026-10-08T13:40:00,quota_file_progress,employee=dorothy_p,0.92,
2026-10-08T13:40:00,quota_file_progress,employee=eustace_m,0.92,
2026-10-08T13:40:00,quota_file_progress,employee=fern_o,0.92,
2026-10-08T13:45:00,quota_file_progress,employee=agnes_k,1.0,
2026-10-08T13:45:00,quota_file_progress,employee=bertram_l,1.0,
2026-10-08T13:45:00,quota_file_progress,employee=clement_w,0.936,
2026-10-08T13:45:00,quota_file_progress,employee=dorothy_p,0.925,
2026-10-08T13:45:00,quota_file_progress,employee=eustace_m,0.925,
2026-10-08T13:45:00,quota_file_progress,employee=fern_o,0.925,
2026-10-08T13:50:00,quota_file_progress,employee=agnes_k,1.0,
2026-10-08T13:50:00,quota_file_progress,employee=bertram_l,1.0,
2026-10-08T13:50:00,quota_file_progress,employee=clement_w,0.941,
2026-10-08T13:50:00,quota_file_progress,employee=dorothy_p,0.93,
2026-10-08T13:50:00,quota_file_progress,employee=eustace_m,0.93,
2026-10-08T13:50:00,quota_file_progress,employee=fern_o,0.93,
2026-10-08T13:55:00,quota_file_progress,employee=agnes_k,1.0,
2026-10-08T13:55:00,quota_file_progress,employee=bertram_l,1.0,
2026-10-08T13:55:00,quota_file_progress,employee=clement_w,0.945,
2026-10-08T13:55:00,quota_file_progress,employee=dorothy_p,0.935,
2026-10-08T13:55:00,quota_file_progress,employee=eustace_m,0.935,
2026-10-08T13:55:00,quota_file_progress,employee=fern_o,0.935,
2026-10-08T14:00:00,quota_file_progress,employee=agnes_k,1.0,
2026-10-08T14:00:00,quota_file_progress,employee=bertram_l,1.0,
2026-10-08T14:00:00,quota_file_progress,employee=clement_w,0.949,
2026-10-08T14:00:00,quota_file_progress,employee=dorothy_p,0.94,
2026-10-08T14:00:00,quota_file_progress,employee=eustace_m,0.94,
2026-10-08T14:00:00,quota_file_progress,employee=fern_o,0.94,
2026-10-08T14:05:00,quota_file_progress,employee=agnes_k,1.0,
2026-10-08T14:05:00,quota_file_progress,employee=bertram_l,1.0,
2026-10-08T14:05:00,quota_file_progress,employee=clement_w,0.953,
2026-10-08T14:05:00,quota_file_progress,employee=dorothy_p,0.945,
2026-10-08T14:05:00,quota_file_progress,employee=eustace_m,0.945,
2026-10-08T14:05:00,quota_file_progress,employee=fern_o,0.945,
2026-10-08T14:10:00,quota_file_progress,employee=agnes_k,1.0,
2026-10-08T14:10:00,quota_file_progress,employee=bertram_l,1.0,
2026-10-08T14:10:00,quota_file_progress,employee=clement_w,0.957,
2026-10-08T14:10:00,quota_file_progress,employee=dorothy_p,0.95,
2026-10-08T14:10:00,quota_file_progress,employee=eustace_m,0.95,
2026-10-08T14:10:00,quota_file_progress,employee=fern_o,0.95,
2026-10-08T14:15:00,quota_file_progress,employee=agnes_k,1.0,
2026-10-08T14:15:00,quota_file_progress,employee=bertram_l,1.0,
2026-10-08T14:15:00,quota_file_progress,employee=clement_w,0.961,
2026-10-08T14:15:00,quota_file_progress,employee=dorothy_p,0.955,
2026-10-08T14:15:00,quota_file_progress,employee=eustace_m,0.955,
2026-10-08T14:15:00,quota_file_progress,employee=fern_o,0.955,
2026-10-08T14:20:00,quota_file_progress,employee=agnes_k,1.0,
2026-10-08T14:20:00,quota_file_progress,employee=bertram_l,1.0,
2026-10-08T14:20:00,quota_file_progress,employee=clement_w,0.965,
2026-10-08T14:20:00,quota_file_progress,employee=dorothy_p,0.96,
2026-10-08T14:20:00,quota_file_progress,employee=eustace_m,0.96,
2026-10-08T14:20:00,quota_file_progress,employee=fern_o,0.96,
2026-10-08T14:25:00,quota_file_progress,employee=agnes_k,1.0,
2026-10-08T14:25:00,quota_file_progress,employee=bertram_l,1.0,
2026-10-08T14:25:00,quota_file_progress,employee=clement_w,0.969,
2026-10-08T14:25:00,quota_file_progress,employee=dorothy_p,1.0,
2026-10-08T14:25:00,quota_file_progress,employee=eustace_m,0.965,
2026-10-08T14:25:00,quota_file_progress,employee=fern_o,0.965,
2026-10-08T14:30:00,quota_file_progress,employee=agnes_k,1.0,
2026-10-08T14:30:00,quota_file_progress,employee=bertram_l,1.0,
2026-10-08T14:30:00,quota_file_progress,employee=clement_w,0.973,
2026-10-08T14:30:00,quota_file_progress,employee=dorothy_p,1.0,
2026-10-08T14:30:00,quota_file_progress,employee=eustace_m,0.97,
2026-10-08T14:30:00,quota_file_progress,employee=fern_o,0.97,
2026-10-08T14:35:00,quota_file_progress,employee=agnes_k,1.0,
2026-10-08T14:35:00,quota_file_progress,employee=bertram_l,1.0,
2026-10-08T14:35:00,quota_file_progress,employee=clement_w,0.977,
2026-10-08T14:35:00,quota_file_progress,employee=dorothy_p,1.0,
2026-10-08T14:35:00,quota_file_progress,employee=eustace_m,0.975,
2026-10-08T14:35:00,quota_file_progress,employee=fern_o,0.975,
2026-10-08T14:40:00,quota_file_progress,employee=agnes_k,1.0,
2026-10-08T14:40:00,quota_file_progress,employee=bertram_l,1.0,
2026-10-08T14:40:00,quota_file_progress,employee=clement_w,0.981,
2026-10-08T14:40:00,quota_file_progress,employee=dorothy_p,1.0,
2026-10-08T14:40:00,quota_file_progress,employee=eustace_m,0.98,
2026-10-08T14:40:00,quota_file_progress,employee=fern_o,0.98,
2026-10-08T14:45:00,quota_file_progress,employee=agnes_k,1.0,
2026-10-08T14:45:00,quota_file_progress,employee=bertram_l,1.0,
2026-10-08T14:45:00,quota_file_progress,employee=clement_w,0.985,
2026-10-08T14:45:00,quota_file_progress,employee=dorothy_p,1.0,
2026-10-08T14:45:00,quota_file_progress,employee=eustace_m,0.985,
2026-10-08T14:45:00,quota_file_progress,employee=fern_o,0.985,
2026-10-08T14:50:00,quota_file_progress,employee=agnes_k,1.0,
2026-10-08T14:50:00,quota_file_progress,employee=bertram_l,1.0,
2026-10-08T14:50:00,quota_file_progress,employee=clement_w,0.989,
2026-10-08T14:50:00,quota_file_progress,employee=dorothy_p,1.0,
2026-10-08T14:50:00,quota_file_progress,employee=eustace_m,1.0,
2026-10-08T14:50:00,quota_file_progress,employee=fern_o,0.99,
2026-10-08T14:55:00,quota_file_progress,employee=agnes_k,1.0,
2026-10-08T14:55:00,quota_file_progress,employee=bertram_l,1.0,
2026-10-08T14:55:00,quota_file_progress,employee=clement_w,0.993,
2026-10-08T14:55:00,quota_file_progress,employee=dorothy_p,1.0,
2026-10-08T14:55:00,quota_file_progress,employee=eustace_m,1.0,
2026-10-08T14:55:00,quota_file_progress,employee=fern_o,1.0,
2026-10-08T14:58:12,quota_file_progress,employee=clement_w,1.0,
2026-10-08T14:21:40,quota_file_progress,employee=dorothy_p,1.0,
2026-10-08T14:52:30,quota_file_progress,employee=fern_o,1.0,
2026-10-08T14:46:05,quota_file_progress,employee=eustace_m,1.0,
2026-10-08T14:58:12,department_quota_ratio,dept=deep-sleep-operations,1.0,
2026-10-08T14:55:00,circuit_power_watts,circuit=C-7,load=supply-room-b,111,
2026-10-08T14:55:00,circuit_power_watts,circuit=C-7,load=break-room-2,142,
2026-10-08T14:55:10,circuit_power_watts,circuit=C-7,load=supply-room-b,119,
2026-10-08T14:55:10,circuit_power_watts,circuit=C-7,load=break-room-2,140,
2026-10-08T14:55:20,circuit_power_watts,circuit=C-7,load=supply-room-b,116,
2026-10-08T14:55:20,circuit_power_watts,circuit=C-7,load=break-room-2,139,
2026-10-08T14:55:30,circuit_power_watts,circuit=C-7,load=supply-room-b,121,
2026-10-08T14:55:30,circuit_power_watts,circuit=C-7,load=break-room-2,136,
2026-10-08T14:55:40,circuit_power_watts,circuit=C-7,load=supply-room-b,118,
2026-10-08T14:55:40,circuit_power_watts,circuit=C-7,load=break-room-2,137,
2026-10-08T14:55:50,circuit_power_watts,circuit=C-7,load=supply-room-b,120,
2026-10-08T14:55:50,circuit_power_watts,circuit=C-7,load=break-room-2,145,
2026-10-08T14:56:00,circuit_power_watts,circuit=C-7,load=supply-room-b,110,
2026-10-08T14:56:00,circuit_power_watts,circuit=C-7,load=break-room-2,140,
2026-10-08T14:56:10,circuit_power_watts,circuit=C-7,load=supply-room-b,115,
2026-10-08T14:56:10,circuit_power_watts,circuit=C-7,load=break-room-2,145,
2026-10-08T14:56:20,circuit_power_watts,circuit=C-7,load=supply-room-b,121,
2026-10-08T14:56:20,circuit_power_watts,circuit=C-7,load=break-room-2,142,
2026-10-08T14:56:30,circuit_power_watts,circuit=C-7,load=supply-room-b,123,
2026-10-08T14:56:30,circuit_power_watts,circuit=C-7,load=break-room-2,142,
2026-10-08T14:56:40,circuit_power_watts,circuit=C-7,load=supply-room-b,118,
2026-10-08T14:56:40,circuit_power_watts,circuit=C-7,load=break-room-2,145,
2026-10-08T14:56:50,circuit_power_watts,circuit=C-7,load=supply-room-b,123,
2026-10-08T14:56:50,circuit_power_watts,circuit=C-7,load=break-room-2,137,
2026-10-08T14:57:00,circuit_power_watts,circuit=C-7,load=supply-room-b,117,
2026-10-08T14:57:00,circuit_power_watts,circuit=C-7,load=break-room-2,145,
2026-10-08T14:57:10,circuit_power_watts,circuit=C-7,load=supply-room-b,123,
2026-10-08T14:57:10,circuit_power_watts,circuit=C-7,load=break-room-2,139,
2026-10-08T14:57:20,circuit_power_watts,circuit=C-7,load=supply-room-b,119,
2026-10-08T14:57:20,circuit_power_watts,circuit=C-7,load=break-room-2,135,
2026-10-08T14:57:30,circuit_power_watts,circuit=C-7,load=supply-room-b,114,
2026-10-08T14:57:30,circuit_power_watts,circuit=C-7,load=break-room-2,145,
2026-10-08T14:57:40,circuit_power_watts,circuit=C-7,load=supply-room-b,123,
2026-10-08T14:57:40,circuit_power_watts,circuit=C-7,load=break-room-2,141,
2026-10-08T14:57:50,circuit_power_watts,circuit=C-7,load=supply-room-b,117,
2026-10-08T14:57:50,circuit_power_watts,circuit=C-7,load=break-room-2,137,
2026-10-08T14:58:00,circuit_power_watts,circuit=C-7,load=supply-room-b,122,
2026-10-08T14:58:00,circuit_power_watts,circuit=C-7,load=break-room-2,138,
2026-10-08T14:58:10,circuit_power_watts,circuit=C-7,load=supply-room-b,118,
2026-10-08T14:58:10,circuit_power_watts,circuit=C-7,load=break-room-2,141,
2026-10-08T14:58:20,circuit_power_watts,circuit=C-7,load=supply-room-b,116,
2026-10-08T14:58:20,circuit_power_watts,circuit=C-7,load=break-room-2,141,
2026-10-08T14:58:30,circuit_power_watts,circuit=C-7,load=supply-room-b,116,
2026-10-08T14:58:30,circuit_power_watts,circuit=C-7,load=break-room-2,138,
2026-10-08T14:58:40,circuit_power_watts,circuit=C-7,load=supply-room-b,117,
2026-10-08T14:58:40,circuit_power_watts,circuit=C-7,load=break-room-2,140,
2026-10-08T14:58:50,circuit_power_watts,circuit=C-7,load=supply-room-b,118,
2026-10-08T14:58:50,circuit_power_watts,circuit=C-7,load=break-room-2,141,
2026-10-08T14:59:00,circuit_power_watts,circuit=C-7,load=supply-room-b,116,
2026-10-08T14:59:00,circuit_power_watts,circuit=C-7,load=break-room-2,143,
2026-10-08T14:59:10,circuit_power_watts,circuit=C-7,load=supply-room-b,107,
2026-10-08T14:59:10,circuit_power_watts,circuit=C-7,load=break-room-2,137,
2026-10-08T14:59:20,circuit_power_watts,circuit=C-7,load=supply-room-b,110,
2026-10-08T14:59:20,circuit_power_watts,circuit=C-7,load=break-room-2,135,
2026-10-08T14:59:30,circuit_power_watts,circuit=C-7,load=supply-room-b,112,
2026-10-08T14:59:30,circuit_power_watts,circuit=C-7,load=break-room-2,145,
2026-10-08T14:59:40,circuit_power_watts,circuit=C-7,load=supply-room-b,109,
2026-10-08T14:59:40,circuit_power_watts,circuit=C-7,load=break-room-2,140,
2026-10-08T14:59:50,circuit_power_watts,circuit=C-7,load=supply-room-b,112,
2026-10-08T14:59:50,circuit_power_watts,circuit=C-7,load=break-room-2,143,
2026-10-08T15:00:00,circuit_power_watts,circuit=C-7,load=supply-room-b,113,
2026-10-08T15:00:00,circuit_power_watts,circuit=C-7,load=break-room-2,2815,
2026-10-08T15:00:10,circuit_power_watts,circuit=C-7,load=supply-room-b,119,
2026-10-08T15:00:10,circuit_power_watts,circuit=C-7,load=break-room-2,2827,
2026-10-08T15:00:20,circuit_power_watts,circuit=C-7,load=supply-room-b,121,
2026-10-08T15:00:20,circuit_power_watts,circuit=C-7,load=break-room-2,2900,
2026-10-08T15:00:30,circuit_power_watts,circuit=C-7,load=supply-room-b,118,
2026-10-08T15:00:30,circuit_power_watts,circuit=C-7,load=break-room-2,2842,
2026-10-08T15:00:40,circuit_power_watts,circuit=C-7,load=supply-room-b,108,
2026-10-08T15:00:40,circuit_power_watts,circuit=C-7,load=break-room-2,2888,
2026-10-08T15:00:50,circuit_power_watts,circuit=C-7,load=supply-room-b,112,
2026-10-08T15:00:50,circuit_power_watts,circuit=C-7,load=break-room-2,2899,
2026-10-08T15:01:00,circuit_power_watts,circuit=C-7,load=supply-room-b,123,
2026-10-08T15:01:00,circuit_power_watts,circuit=C-7,load=break-room-2,2806,
2026-10-08T15:01:10,circuit_power_watts,circuit=C-7,load=supply-room-b,108,
2026-10-08T15:01:10,circuit_power_watts,circuit=C-7,load=break-room-2,2819,
2026-10-08T15:01:20,circuit_power_watts,circuit=C-7,load=supply-room-b,108,
2026-10-08T15:01:20,circuit_power_watts,circuit=C-7,load=break-room-2,2891,
2026-10-08T15:01:30,circuit_power_watts,circuit=C-7,load=supply-room-b,110,
2026-10-08T15:01:30,circuit_power_watts,circuit=C-7,load=break-room-2,2909,
2026-10-08T15:01:40,circuit_power_watts,circuit=C-7,load=supply-room-b,123,
2026-10-08T15:01:40,circuit_power_watts,circuit=C-7,load=break-room-2,2865,
2026-10-08T15:01:50,circuit_power_watts,circuit=C-7,load=supply-room-b,111,
2026-10-08T15:01:50,circuit_power_watts,circuit=C-7,load=break-room-2,2792,
2026-10-08T15:01:58,circuit_power_watts,circuit=C-7,load=supply-room-b,1518,
2026-10-08T15:01:59,circuit_power_watts,circuit=C-7,load=supply-room-b,1522,
2026-10-08T15:02:00,floor_power_up,floor=sleep,0,
2026-10-08T15:07:00,floor_power_up,floor=sleep,1,
2026-10-08T14:59:30,badge_accel_variance,employee=agnes_k,0.339,
2026-10-08T14:59:30,badge_accel_variance,employee=bertram_l,0.1,
2026-10-08T14:59:30,badge_accel_variance,employee=clement_w,0.097,
2026-10-08T14:59:30,badge_accel_variance,employee=dorothy_p,0.235,
2026-10-08T14:59:30,badge_accel_variance,employee=eustace_m,0.217,
2026-10-08T14:59:30,badge_accel_variance,employee=fern_o,0.181,
2026-10-08T14:59:30,badge_accel_variance,employee=gideon_r,0.163,
2026-10-08T14:59:30,badge_accel_variance,employee=harriet_s,0.249,
2026-10-08T14:59:30,badge_accel_variance,employee=milo_d,0.1,
2026-10-08T14:59:30,badge_accel_variance,employee=silas_q,0.228,
2026-10-08T14:59:30,badge_accel_variance,employee=winifred_e,0.073,
2026-10-08T14:59:40,badge_accel_variance,employee=agnes_k,0.3,
2026-10-08T14:59:40,badge_accel_variance,employee=bertram_l,0.136,
2026-10-08T14:59:40,badge_accel_variance,employee=clement_w,0.152,
2026-10-08T14:59:40,badge_accel_variance,employee=dorothy_p,0.117,
2026-10-08T14:59:40,badge_accel_variance,employee=eustace_m,0.261,
2026-10-08T14:59:40,badge_accel_variance,employee=fern_o,0.111,
2026-10-08T14:59:40,badge_accel_variance,employee=gideon_r,0.079,
2026-10-08T14:59:40,badge_accel_variance,employee=harriet_s,0.126,
2026-10-08T14:59:40,badge_accel_variance,employee=milo_d,0.129,
2026-10-08T14:59:40,badge_accel_variance,employee=silas_q,0.072,
2026-10-08T14:59:40,badge_accel_variance,employee=winifred_e,0.134,
2026-10-08T14:59:50,badge_accel_variance,employee=agnes_k,0.172,
2026-10-08T14:59:50,badge_accel_variance,employee=bertram_l,0.372,
2026-10-08T14:59:50,badge_accel_variance,employee=clement_w,0.388,
2026-10-08T14:59:50,badge_accel_variance,employee=dorothy_p,0.269,
2026-10-08T14:59:50,badge_accel_variance,employee=eustace_m,0.053,
2026-10-08T14:59:50,badge_accel_variance,employee=fern_o,0.235,
2026-10-08T14:59:50,badge_accel_variance,employee=gideon_r,0.284,
2026-10-08T14:59:50,badge_accel_variance,employee=harriet_s,0.172,
2026-10-08T14:59:50,badge_accel_variance,employee=milo_d,0.052,
2026-10-08T14:59:50,badge_accel_variance,employee=silas_q,0.167,
2026-10-08T14:59:50,badge_accel_variance,employee=winifred_e,0.283,
2026-10-08T15:00:00,badge_accel_variance,employee=agnes_k,0.541,
2026-10-08T15:00:00,badge_accel_variance,employee=bertram_l,0.313,
2026-10-08T15:00:00,badge_accel_variance,employee=clement_w,0.326,
2026-10-08T15:00:00,badge_accel_variance,employee=dorothy_p,0.445,
2026-10-08T15:00:00,badge_accel_variance,employee=eustace_m,0.601,
2026-10-08T15:00:00,badge_accel_variance,employee=fern_o,0.622,
2026-10-08T15:00:00,badge_accel_variance,employee=gideon_r,0.289,
2026-10-08T15:00:00,badge_accel_variance,employee=harriet_s,0.109,
2026-10-08T15:00:00,badge_accel_variance,employee=milo_d,0.248,
2026-10-08T15:00:00,badge_accel_variance,employee=silas_q,0.064,
2026-10-08T15:00:00,badge_accel_variance,employee=winifred_e,0.246,
2026-10-08T15:00:10,badge_accel_variance,employee=agnes_k,0.347,
2026-10-08T15:00:10,badge_accel_variance,employee=bertram_l,0.519,
2026-10-08T15:00:10,badge_accel_variance,employee=clement_w,0.384,
2026-10-08T15:00:10,badge_accel_variance,employee=dorothy_p,0.484,
2026-10-08T15:00:10,badge_accel_variance,employee=eustace_m,0.532,
2026-10-08T15:00:10,badge_accel_variance,employee=fern_o,0.552,
2026-10-08T15:00:10,badge_accel_variance,employee=gideon_r,0.055,
2026-10-08T15:00:10,badge_accel_variance,employee=harriet_s,0.181,
2026-10-08T15:00:10,badge_accel_variance,employee=milo_d,0.146,
2026-10-08T15:00:10,badge_accel_variance,employee=silas_q,0.126,
2026-10-08T15:00:10,badge_accel_variance,employee=winifred_e,0.1,
2026-10-08T15:00:20,badge_accel_variance,employee=agnes_k,0.416,
2026-10-08T15:00:20,badge_accel_variance,employee=bertram_l,0.69,
2026-10-08T15:00:20,badge_accel_variance,employee=clement_w,0.454,
2026-10-08T15:00:20,badge_accel_variance,employee=dorothy_p,0.358,
2026-10-08T15:00:20,badge_accel_variance,employee=eustace_m,0.521,
2026-10-08T15:00:20,badge_accel_variance,employee=fern_o,0.598,
2026-10-08T15:00:20,badge_accel_variance,employee=gideon_r,0.074,
2026-10-08T15:00:20,badge_accel_variance,employee=harriet_s,0.284,
2026-10-08T15:00:20,badge_accel_variance,employee=milo_d,0.242,
2026-10-08T15:00:20,badge_accel_variance,employee=silas_q,0.093,
2026-10-08T15:00:20,badge_accel_variance,employee=winifred_e,0.177,
2026-10-08T15:00:30,badge_accel_variance,employee=agnes_k,0.386,
2026-10-08T15:00:30,badge_accel_variance,employee=bertram_l,0.406,
2026-10-08T15:00:30,badge_accel_variance,employee=clement_w,0.551,
2026-10-08T15:00:30,badge_accel_variance,employee=dorothy_p,0.427,
2026-10-08T15:00:30,badge_accel_variance,employee=eustace_m,0.694,
2026-10-08T15:00:30,badge_accel_variance,employee=fern_o,0.627,
2026-10-08T15:00:30,badge_accel_variance,employee=gideon_r,0.276,
2026-10-08T15:00:30,badge_accel_variance,employee=harriet_s,0.158,
2026-10-08T15:00:30,badge_accel_variance,employee=milo_d,0.199,
2026-10-08T15:00:30,badge_accel_variance,employee=silas_q,0.181,
2026-10-08T15:00:30,badge_accel_variance,employee=winifred_e,0.083,
2026-10-08T15:00:40,badge_accel_variance,employee=agnes_k,0.567,
2026-10-08T15:00:40,badge_accel_variance,employee=bertram_l,0.621,
2026-10-08T15:00:40,badge_accel_variance,employee=clement_w,0.367,
2026-10-08T15:00:40,badge_accel_variance,employee=dorothy_p,0.553,
2026-10-08T15:00:40,badge_accel_variance,employee=eustace_m,0.454,
2026-10-08T15:00:40,badge_accel_variance,employee=fern_o,0.378,
2026-10-08T15:00:40,badge_accel_variance,employee=gideon_r,0.203,
2026-10-08T15:00:40,badge_accel_variance,employee=harriet_s,0.169,
2026-10-08T15:00:40,badge_accel_variance,employee=milo_d,0.144,
2026-10-08T15:00:40,badge_accel_variance,employee=silas_q,0.175,
2026-10-08T15:00:40,badge_accel_variance,employee=winifred_e,0.087,
2026-10-08T15:00:50,badge_accel_variance,employee=agnes_k,0.649,
2026-10-08T15:00:50,badge_accel_variance,employee=bertram_l,0.496,
2026-10-08T15:00:50,badge_accel_variance,employee=clement_w,0.513,
2026-10-08T15:00:50,badge_accel_variance,employee=dorothy_p,0.693,
2026-10-08T15:00:50,badge_accel_variance,employee=eustace_m,0.548,
2026-10-08T15:00:50,badge_accel_variance,employee=fern_o,0.443,
2026-10-08T15:00:50,badge_accel_variance,employee=gideon_r,0.17,
2026-10-08T15:00:50,badge_accel_variance,employee=harriet_s,0.106,
2026-10-08T15:00:50,badge_accel_variance,employee=milo_d,0.217,
2026-10-08T15:00:50,badge_accel_variance,employee=silas_q,0.181,
2026-10-08T15:00:50,badge_accel_variance,employee=winifred_e,0.12,
2026-10-08T15:01:00,badge_accel_variance,employee=agnes_k,0.628,
2026-10-08T15:01:00,badge_accel_variance,employee=bertram_l,0.342,
2026-10-08T15:01:00,badge_accel_variance,employee=clement_w,0.672,
2026-10-08T15:01:00,badge_accel_variance,employee=dorothy_p,0.685,
2026-10-08T15:01:00,badge_accel_variance,employee=eustace_m,0.319,
2026-10-08T15:01:00,badge_accel_variance,employee=fern_o,0.635,
2026-10-08T15:01:00,badge_accel_variance,employee=gideon_r,0.254,
2026-10-08T15:01:00,badge_accel_variance,employee=harriet_s,0.166,
2026-10-08T15:01:00,badge_accel_variance,employee=milo_d,0.105,
2026-10-08T15:01:00,badge_accel_variance,employee=silas_q,0.211,
2026-10-08T15:01:00,badge_accel_variance,employee=winifred_e,0.276,
2026-10-08T15:01:10,badge_accel_variance,employee=agnes_k,0.338,
2026-10-08T15:01:10,badge_accel_variance,employee=bertram_l,0.328,
2026-10-08T15:01:10,badge_accel_variance,employee=clement_w,0.459,
2026-10-08T15:01:10,badge_accel_variance,employee=dorothy_p,0.46,
2026-10-08T15:01:10,badge_accel_variance,employee=eustace_m,0.389,
2026-10-08T15:01:10,badge_accel_variance,employee=fern_o,0.471,
2026-10-08T15:01:10,badge_accel_variance,employee=gideon_r,0.086,
2026-10-08T15:01:10,badge_accel_variance,employee=harriet_s,0.094,
2026-10-08T15:01:10,badge_accel_variance,employee=milo_d,0.215,
2026-10-08T15:01:10,badge_accel_variance,employee=silas_q,0.134,
2026-10-08T15:01:10,badge_accel_variance,employee=winifred_e,0.297,
2026-10-08T15:01:20,badge_accel_variance,employee=agnes_k,0.479,
2026-10-08T15:01:20,badge_accel_variance,employee=bertram_l,0.443,
2026-10-08T15:01:20,badge_accel_variance,employee=clement_w,0.626,
2026-10-08T15:01:20,badge_accel_variance,employee=dorothy_p,0.567,
2026-10-08T15:01:20,badge_accel_variance,employee=eustace_m,0.676,
2026-10-08T15:01:20,badge_accel_variance,employee=fern_o,0.662,
2026-10-08T15:01:20,badge_accel_variance,employee=gideon_r,0.155,
2026-10-08T15:01:20,badge_accel_variance,employee=harriet_s,0.079,
2026-10-08T15:01:20,badge_accel_variance,employee=milo_d,0.153,
2026-10-08T15:01:20,badge_accel_variance,employee=silas_q,0.167,
2026-10-08T15:01:20,badge_accel_variance,employee=winifred_e,0.1,
2026-10-08T15:01:30,badge_accel_variance,employee=agnes_k,0.345,
2026-10-08T15:01:30,badge_accel_variance,employee=bertram_l,0.503,
2026-10-08T15:01:30,badge_accel_variance,employee=clement_w,0.413,
2026-10-08T15:01:30,badge_accel_variance,employee=dorothy_p,0.421,
2026-10-08T15:01:30,badge_accel_variance,employee=eustace_m,0.659,
2026-10-08T15:01:30,badge_accel_variance,employee=fern_o,0.612,
2026-10-08T15:01:30,badge_accel_variance,employee=gideon_r,0.248,
2026-10-08T15:01:30,badge_accel_variance,employee=harriet_s,0.251,
2026-10-08T15:01:30,badge_accel_variance,employee=milo_d,0.064,
2026-10-08T15:01:30,badge_accel_variance,employee=silas_q,0.222,
2026-10-08T15:01:30,badge_accel_variance,employee=winifred_e,0.277,
2026-10-08T15:01:40,badge_accel_variance,employee=agnes_k,0.57,
2026-10-08T15:01:40,badge_accel_variance,employee=bertram_l,0.243,
2026-10-08T15:01:40,badge_accel_variance,employee=clement_w,0.374,
2026-10-08T15:01:40,badge_accel_variance,employee=dorothy_p,0.386,
2026-10-08T15:01:40,badge_accel_variance,employee=eustace_m,0.355,
2026-10-08T15:01:40,badge_accel_variance,employee=fern_o,0.49,
2026-10-08T15:01:40,badge_accel_variance,employee=gideon_r,0.172,
2026-10-08T15:01:40,badge_accel_variance,employee=harriet_s,0.058,
2026-10-08T15:01:40,badge_accel_variance,employee=milo_d,0.059,
2026-10-08T15:01:40,badge_accel_variance,employee=silas_q,0.299,
2026-10-08T15:01:40,badge_accel_variance,employee=winifred_e,0.177,
2026-10-08T15:01:50,badge_accel_variance,employee=agnes_k,0.466,
2026-10-08T15:01:50,badge_accel_variance,employee=bertram_l,0.316,
2026-10-08T15:01:50,badge_accel_variance,employee=clement_w,0.356,
2026-10-08T15:01:50,badge_accel_variance,employee=dorothy_p,0.523,
2026-10-08T15:01:50,badge_accel_variance,employee=eustace_m,0.457,
2026-10-08T15:01:50,badge_accel_variance,employee=fern_o,0.525,
2026-10-08T15:01:50,badge_accel_variance,employee=gideon_r,0.251,
2026-10-08T15:01:50,badge_accel_variance,employee=harriet_s,0.064,
2026-10-08T15:01:50,badge_accel_variance,employee=milo_d,0.097,
2026-10-08T15:01:50,badge_accel_variance,employee=silas_q,0.068,
2026-10-08T15:01:50,badge_accel_variance,employee=winifred_e,0.196,
2026-10-08T15:02:00,badge_accel_variance,employee=agnes_k,1.241,2026-10-08T15:07:41
2026-10-08T15:02:00,badge_accel_variance,employee=bertram_l,3.758,2026-10-08T15:07:41
2026-10-08T15:02:00,badge_accel_variance,employee=clement_w,2.564,2026-10-08T15:07:41
2026-10-08T15:02:00,badge_accel_variance,employee=dorothy_p,3.226,2026-10-08T15:07:41
2026-10-08T15:02:00,badge_accel_variance,employee=eustace_m,3.062,2026-10-08T15:07:41
2026-10-08T15:02:00,badge_accel_variance,employee=fern_o,3.659,2026-10-08T15:07:41
2026-10-08T15:02:00,badge_accel_variance,employee=gideon_r,2.7,2026-10-08T15:07:41
2026-10-08T15:02:00,badge_accel_variance,employee=harriet_s,1.757,2026-10-08T15:07:41
2026-10-08T15:02:00,badge_accel_variance,employee=milo_d,1.895,2026-10-08T15:07:41
2026-10-08T15:02:00,badge_accel_variance,employee=silas_q,3.647,2026-10-08T15:07:41
2026-10-08T15:02:00,badge_accel_variance,employee=winifred_e,2.968,2026-10-08T15:07:41
2026-10-08T15:02:10,badge_accel_variance,employee=agnes_k,1.959,2026-10-08T15:07:41
2026-10-08T15:02:10,badge_accel_variance,employee=bertram_l,3.407,2026-10-08T15:07:41
2026-10-08T15:02:10,badge_accel_variance,employee=clement_w,2.736,2026-10-08T15:07:41
2026-10-08T15:02:10,badge_accel_variance,employee=dorothy_p,0.959,2026-10-08T15:07:41
2026-10-08T15:02:10,badge_accel_variance,employee=eustace_m,1.321,2026-10-08T15:07:41
2026-10-08T15:02:10,badge_accel_variance,employee=fern_o,2.587,2026-10-08T15:07:41
2026-10-08T15:02:10,badge_accel_variance,employee=gideon_r,2.549,2026-10-08T15:07:41
2026-10-08T15:02:10,badge_accel_variance,employee=harriet_s,2.813,2026-10-08T15:07:41
2026-10-08T15:02:10,badge_accel_variance,employee=milo_d,2.141,2026-10-08T15:07:41
2026-10-08T15:02:10,badge_accel_variance,employee=silas_q,3.218,2026-10-08T15:07:41
2026-10-08T15:02:10,badge_accel_variance,employee=winifred_e,2.955,2026-10-08T15:07:41
2026-10-08T15:02:20,badge_accel_variance,employee=agnes_k,3.768,2026-10-08T15:07:41
2026-10-08T15:02:20,badge_accel_variance,employee=bertram_l,2.467,2026-10-08T15:07:41
2026-10-08T15:02:20,badge_accel_variance,employee=clement_w,1.806,2026-10-08T15:07:41
2026-10-08T15:02:20,badge_accel_variance,employee=dorothy_p,3.514,2026-10-08T15:07:41
2026-10-08T15:02:20,badge_accel_variance,employee=eustace_m,3.276,2026-10-08T15:07:41
2026-10-08T15:02:20,badge_accel_variance,employee=fern_o,1.098,2026-10-08T15:07:41
2026-10-08T15:02:20,badge_accel_variance,employee=gideon_r,0.993,2026-10-08T15:07:41
2026-10-08T15:02:20,badge_accel_variance,employee=harriet_s,3.032,2026-10-08T15:07:41
2026-10-08T15:02:20,badge_accel_variance,employee=milo_d,3.173,2026-10-08T15:07:41
2026-10-08T15:02:20,badge_accel_variance,employee=silas_q,3.748,2026-10-08T15:07:41
2026-10-08T15:02:20,badge_accel_variance,employee=winifred_e,3.055,2026-10-08T15:07:41
2026-10-08T15:02:30,badge_accel_variance,employee=agnes_k,1.747,2026-10-08T15:07:41
2026-10-08T15:02:30,badge_accel_variance,employee=bertram_l,3.724,2026-10-08T15:07:41
2026-10-08T15:02:30,badge_accel_variance,employee=clement_w,2.439,2026-10-08T15:07:41
2026-10-08T15:02:30,badge_accel_variance,employee=dorothy_p,2.9,2026-10-08T15:07:41
2026-10-08T15:02:30,badge_accel_variance,employee=eustace_m,2.685,2026-10-08T15:07:41
2026-10-08T15:02:30,badge_accel_variance,employee=fern_o,1.195,2026-10-08T15:07:41
2026-10-08T15:02:30,badge_accel_variance,employee=gideon_r,2.546,2026-10-08T15:07:41
2026-10-08T15:02:30,badge_accel_variance,employee=harriet_s,0.0,2026-10-08T15:07:41
2026-10-08T15:02:30,badge_accel_variance,employee=milo_d,3.257,2026-10-08T15:07:41
2026-10-08T15:02:30,badge_accel_variance,employee=silas_q,3.072,2026-10-08T15:07:41
2026-10-08T15:02:30,badge_accel_variance,employee=winifred_e,2.802,2026-10-08T15:07:41
2026-10-08T15:02:40,badge_accel_variance,employee=agnes_k,1.561,2026-10-08T15:07:41
2026-10-08T15:02:40,badge_accel_variance,employee=bertram_l,1.342,2026-10-08T15:07:41
2026-10-08T15:02:40,badge_accel_variance,employee=clement_w,3.303,2026-10-08T15:07:41
2026-10-08T15:02:40,badge_accel_variance,employee=dorothy_p,3.369,2026-10-08T15:07:41
2026-10-08T15:02:40,badge_accel_variance,employee=eustace_m,2.643,2026-10-08T15:07:41
2026-10-08T15:02:40,badge_accel_variance,employee=fern_o,3.202,2026-10-08T15:07:41
2026-10-08T15:02:40,badge_accel_variance,employee=gideon_r,2.942,2026-10-08T15:07:41
2026-10-08T15:02:40,badge_accel_variance,employee=harriet_s,0.0,2026-10-08T15:07:41
2026-10-08T15:02:40,badge_accel_variance,employee=milo_d,3.512,2026-10-08T15:07:41
2026-10-08T15:02:40,badge_accel_variance,employee=silas_q,2.104,2026-10-08T15:07:41
2026-10-08T15:02:40,badge_accel_variance,employee=winifred_e,2.684,2026-10-08T15:07:41
2026-10-08T15:02:50,badge_accel_variance,employee=agnes_k,1.566,2026-10-08T15:07:41
2026-10-08T15:02:50,badge_accel_variance,employee=bertram_l,0.14,2026-10-08T15:07:41
2026-10-08T15:02:50,badge_accel_variance,employee=clement_w,3.353,2026-10-08T15:07:41
2026-10-08T15:02:50,badge_accel_variance,employee=dorothy_p,1.815,2026-10-08T15:07:41
2026-10-08T15:02:50,badge_accel_variance,employee=eustace_m,3.192,2026-10-08T15:07:41
2026-10-08T15:02:50,badge_accel_variance,employee=fern_o,3.324,2026-10-08T15:07:41
2026-10-08T15:02:50,badge_accel_variance,employee=gideon_r,3.637,2026-10-08T15:07:41
2026-10-08T15:02:50,badge_accel_variance,employee=harriet_s,0.0,2026-10-08T15:07:41
2026-10-08T15:02:50,badge_accel_variance,employee=milo_d,3.237,2026-10-08T15:07:41
2026-10-08T15:02:50,badge_accel_variance,employee=silas_q,2.663,2026-10-08T15:07:41
2026-10-08T15:02:50,badge_accel_variance,employee=winifred_e,2.566,2026-10-08T15:07:41
2026-10-08T15:03:00,badge_accel_variance,employee=agnes_k,2.061,2026-10-08T15:07:41
2026-10-08T15:03:00,badge_accel_variance,employee=bertram_l,0.09,2026-10-08T15:07:41
2026-10-08T15:03:00,badge_accel_variance,employee=clement_w,0.0,2026-10-08T15:07:41
2026-10-08T15:03:00,badge_accel_variance,employee=dorothy_p,1.721,2026-10-08T15:07:41
2026-10-08T15:03:00,badge_accel_variance,employee=eustace_m,2.967,2026-10-08T15:07:41
2026-10-08T15:03:00,badge_accel_variance,employee=fern_o,2.109,2026-10-08T15:07:41
2026-10-08T15:03:00,badge_accel_variance,employee=gideon_r,3.265,2026-10-08T15:07:41
2026-10-08T15:03:00,badge_accel_variance,employee=harriet_s,0.0,2026-10-08T15:07:41
2026-10-08T15:03:00,badge_accel_variance,employee=milo_d,3.465,2026-10-08T15:07:41
2026-10-08T15:03:00,badge_accel_variance,employee=silas_q,1.477,2026-10-08T15:07:41
2026-10-08T15:03:00,badge_accel_variance,employee=winifred_e,3.474,2026-10-08T15:07:41
2026-10-08T15:03:10,badge_accel_variance,employee=agnes_k,1.874,2026-10-08T15:07:41
2026-10-08T15:03:10,badge_accel_variance,employee=bertram_l,0.101,2026-10-08T15:07:41
2026-10-08T15:03:10,badge_accel_variance,employee=clement_w,0.0,2026-10-08T15:07:41
2026-10-08T15:03:10,badge_accel_variance,employee=dorothy_p,3.129,2026-10-08T15:07:41
2026-10-08T15:03:10,badge_accel_variance,employee=eustace_m,0.0,2026-10-08T15:07:41
2026-10-08T15:03:10,badge_accel_variance,employee=fern_o,1.002,2026-10-08T15:07:41
2026-10-08T15:03:10,badge_accel_variance,employee=gideon_r,3.015,2026-10-08T15:07:41
2026-10-08T15:03:10,badge_accel_variance,employee=harriet_s,0.0,2026-10-08T15:07:41
2026-10-08T15:03:10,badge_accel_variance,employee=milo_d,3.364,2026-10-08T15:07:41
2026-10-08T15:03:10,badge_accel_variance,employee=silas_q,2.468,2026-10-08T15:07:41
2026-10-08T15:03:10,badge_accel_variance,employee=winifred_e,1.231,2026-10-08T15:07:41
2026-10-08T15:03:20,badge_accel_variance,employee=agnes_k,1.1,2026-10-08T15:07:41
2026-10-08T15:03:20,badge_accel_variance,employee=bertram_l,0.211,2026-10-08T15:07:41
2026-10-08T15:03:20,badge_accel_variance,employee=clement_w,0.0,2026-10-08T15:07:41
2026-10-08T15:03:20,badge_accel_variance,employee=dorothy_p,3.082,2026-10-08T15:07:41
2026-10-08T15:03:20,badge_accel_variance,employee=eustace_m,0.0,2026-10-08T15:07:41
2026-10-08T15:03:20,badge_accel_variance,employee=fern_o,3.745,2026-10-08T15:07:41
2026-10-08T15:03:20,badge_accel_variance,employee=gideon_r,3.47,2026-10-08T15:07:41
2026-10-08T15:03:20,badge_accel_variance,employee=harriet_s,0.0,2026-10-08T15:07:41
2026-10-08T15:03:20,badge_accel_variance,employee=milo_d,1.488,2026-10-08T15:07:41
2026-10-08T15:03:20,badge_accel_variance,employee=silas_q,3.078,2026-10-08T15:07:41
2026-10-08T15:03:20,badge_accel_variance,employee=winifred_e,3.285,2026-10-08T15:07:41
2026-10-08T15:03:30,badge_accel_variance,employee=agnes_k,3.522,2026-10-08T15:07:41
2026-10-08T15:03:30,badge_accel_variance,employee=bertram_l,0.212,2026-10-08T15:07:41
2026-10-08T15:03:30,badge_accel_variance,employee=clement_w,0.0,2026-10-08T15:07:41
2026-10-08T15:03:30,badge_accel_variance,employee=dorothy_p,0.0,2026-10-08T15:07:41
2026-10-08T15:03:30,badge_accel_variance,employee=eustace_m,0.0,2026-10-08T15:07:41
2026-10-08T15:03:30,badge_accel_variance,employee=fern_o,2.531,2026-10-08T15:07:41
2026-10-08T15:03:30,badge_accel_variance,employee=gideon_r,3.257,2026-10-08T15:07:41
2026-10-08T15:03:30,badge_accel_variance,employee=harriet_s,0.0,2026-10-08T15:07:41
2026-10-08T15:03:30,badge_accel_variance,employee=milo_d,3.21,2026-10-08T15:07:41
2026-10-08T15:03:30,badge_accel_variance,employee=silas_q,2.252,2026-10-08T15:07:41
2026-10-08T15:03:30,badge_accel_variance,employee=winifred_e,1.627,2026-10-08T15:07:41
2026-10-08T15:03:40,badge_accel_variance,employee=agnes_k,1.27,2026-10-08T15:07:41
2026-10-08T15:03:40,badge_accel_variance,employee=bertram_l,0.247,2026-10-08T15:07:41
2026-10-08T15:03:40,badge_accel_variance,employee=clement_w,0.0,2026-10-08T15:07:41
2026-10-08T15:03:40,badge_accel_variance,employee=dorothy_p,0.0,2026-10-08T15:07:41
2026-10-08T15:03:40,badge_accel_variance,employee=eustace_m,0.0,2026-10-08T15:07:41
2026-10-08T15:03:40,badge_accel_variance,employee=fern_o,3.098,2026-10-08T15:07:41
2026-10-08T15:03:40,badge_accel_variance,employee=gideon_r,3.431,2026-10-08T15:07:41
2026-10-08T15:03:40,badge_accel_variance,employee=harriet_s,0.0,2026-10-08T15:07:41
2026-10-08T15:03:40,badge_accel_variance,employee=milo_d,2.963,2026-10-08T15:07:41
2026-10-08T15:03:40,badge_accel_variance,employee=silas_q,2.291,2026-10-08T15:07:41
2026-10-08T15:03:40,badge_accel_variance,employee=winifred_e,2.749,2026-10-08T15:07:41
2026-10-08T15:03:50,badge_accel_variance,employee=agnes_k,2.48,2026-10-08T15:07:41
2026-10-08T15:03:50,badge_accel_variance,employee=bertram_l,0.11,2026-10-08T15:07:41
2026-10-08T15:03:50,badge_accel_variance,employee=clement_w,0.0,2026-10-08T15:07:41
2026-10-08T15:03:50,badge_accel_variance,employee=dorothy_p,0.0,2026-10-08T15:07:41
2026-10-08T15:03:50,badge_accel_variance,employee=eustace_m,0.0,2026-10-08T15:07:41
2026-10-08T15:03:50,badge_accel_variance,employee=fern_o,2.267,2026-10-08T15:07:41
2026-10-08T15:03:50,badge_accel_variance,employee=gideon_r,3.041,2026-10-08T15:07:41
2026-10-08T15:03:50,badge_accel_variance,employee=harriet_s,0.0,2026-10-08T15:07:41
2026-10-08T15:03:50,badge_accel_variance,employee=milo_d,0.0,2026-10-08T15:07:41
2026-10-08T15:03:50,badge_accel_variance,employee=silas_q,1.739,2026-10-08T15:07:41
2026-10-08T15:03:50,badge_accel_variance,employee=winifred_e,1.975,2026-10-08T15:07:41
2026-10-08T15:04:00,badge_accel_variance,employee=agnes_k,1.033,2026-10-08T15:07:41
2026-10-08T15:04:00,badge_accel_variance,employee=bertram_l,0.208,2026-10-08T15:07:41
2026-10-08T15:04:00,badge_accel_variance,employee=clement_w,0.0,2026-10-08T15:07:41
2026-10-08T15:04:00,badge_accel_variance,employee=dorothy_p,0.0,2026-10-08T15:07:41
2026-10-08T15:04:00,badge_accel_variance,employee=eustace_m,0.0,2026-10-08T15:07:41
2026-10-08T15:04:00,badge_accel_variance,employee=fern_o,2.512,2026-10-08T15:07:41
2026-10-08T15:04:00,badge_accel_variance,employee=gideon_r,1.941,2026-10-08T15:07:41
2026-10-08T15:04:00,badge_accel_variance,employee=harriet_s,0.0,2026-10-08T15:07:41
2026-10-08T15:04:00,badge_accel_variance,employee=milo_d,0.0,2026-10-08T15:07:41
2026-10-08T15:04:00,badge_accel_variance,employee=silas_q,3.523,2026-10-08T15:07:41
2026-10-08T15:04:00,badge_accel_variance,employee=winifred_e,3.265,2026-10-08T15:07:41
2026-10-08T15:04:10,badge_accel_variance,employee=agnes_k,2.296,2026-10-08T15:07:41
2026-10-08T15:04:10,badge_accel_variance,employee=bertram_l,0.174,2026-10-08T15:07:41
2026-10-08T15:04:10,badge_accel_variance,employee=clement_w,0.0,2026-10-08T15:07:41
2026-10-08T15:04:10,badge_accel_variance,employee=dorothy_p,0.0,2026-10-08T15:07:41
2026-10-08T15:04:10,badge_accel_variance,employee=eustace_m,0.0,2026-10-08T15:07:41
2026-10-08T15:04:10,badge_accel_variance,employee=fern_o,2.436,2026-10-08T15:07:41
2026-10-08T15:04:10,badge_accel_variance,employee=gideon_r,3.755,2026-10-08T15:07:41
2026-10-08T15:04:10,badge_accel_variance,employee=harriet_s,0.0,2026-10-08T15:07:41
2026-10-08T15:04:10,badge_accel_variance,employee=milo_d,0.0,2026-10-08T15:07:41
2026-10-08T15:04:10,badge_accel_variance,employee=silas_q,3.19,2026-10-08T15:07:41
2026-10-08T15:04:10,badge_accel_variance,employee=winifred_e,3.224,2026-10-08T15:07:41
2026-10-08T15:04:20,badge_accel_variance,employee=agnes_k,1.5,2026-10-08T15:07:41
2026-10-08T15:04:20,badge_accel_variance,employee=bertram_l,0.098,2026-10-08T15:07:41
2026-10-08T15:04:20,badge_accel_variance,employee=clement_w,0.0,2026-10-08T15:07:41
2026-10-08T15:04:20,badge_accel_variance,employee=dorothy_p,0.0,2026-10-08T15:07:41
2026-10-08T15:04:20,badge_accel_variance,employee=eustace_m,0.0,2026-10-08T15:07:41
2026-10-08T15:04:20,badge_accel_variance,employee=fern_o,1.154,2026-10-08T15:07:41
2026-10-08T15:04:20,badge_accel_variance,employee=gideon_r,1.033,2026-10-08T15:07:41
2026-10-08T15:04:20,badge_accel_variance,employee=harriet_s,0.0,2026-10-08T15:07:41
2026-10-08T15:04:20,badge_accel_variance,employee=milo_d,0.0,2026-10-08T15:07:41
2026-10-08T15:04:20,badge_accel_variance,employee=silas_q,1.827,2026-10-08T15:07:41
2026-10-08T15:04:20,badge_accel_variance,employee=winifred_e,0.0,2026-10-08T15:07:41
2026-10-08T15:04:30,badge_accel_variance,employee=agnes_k,2.977,2026-10-08T15:07:41
2026-10-08T15:04:30,badge_accel_variance,employee=bertram_l,0.2,2026-10-08T15:07:41
2026-10-08T15:04:30,badge_accel_variance,employee=clement_w,0.0,2026-10-08T15:07:41
2026-10-08T15:04:30,badge_accel_variance,employee=dorothy_p,0.0,2026-10-08T15:07:41
2026-10-08T15:04:30,badge_accel_variance,employee=eustace_m,0.0,2026-10-08T15:07:41
2026-10-08T15:04:30,badge_accel_variance,employee=fern_o,2.478,2026-10-08T15:07:41
2026-10-08T15:04:30,badge_accel_variance,employee=gideon_r,0.991,2026-10-08T15:07:41
2026-10-08T15:04:30,badge_accel_variance,employee=harriet_s,0.0,2026-10-08T15:07:41
2026-10-08T15:04:30,badge_accel_variance,employee=milo_d,0.0,2026-10-08T15:07:41
2026-10-08T15:04:30,badge_accel_variance,employee=silas_q,2.92,2026-10-08T15:07:41
2026-10-08T15:04:30,badge_accel_variance,employee=winifred_e,0.0,2026-10-08T15:07:41
2026-10-08T15:04:40,badge_accel_variance,employee=agnes_k,2.691,2026-10-08T15:07:41
2026-10-08T15:04:40,badge_accel_variance,employee=bertram_l,0.185,2026-10-08T15:07:41
2026-10-08T15:04:40,badge_accel_variance,employee=clement_w,0.0,2026-10-08T15:07:41
2026-10-08T15:04:40,badge_accel_variance,employee=dorothy_p,0.0,2026-10-08T15:07:41
2026-10-08T15:04:40,badge_accel_variance,employee=eustace_m,0.0,2026-10-08T15:07:41
2026-10-08T15:04:40,badge_accel_variance,employee=fern_o,1.393,2026-10-08T15:07:41
2026-10-08T15:04:40,badge_accel_variance,employee=gideon_r,1.188,2026-10-08T15:07:41
2026-10-08T15:04:40,badge_accel_variance,employee=harriet_s,0.0,2026-10-08T15:07:41
2026-10-08T15:04:40,badge_accel_variance,employee=milo_d,0.0,2026-10-08T15:07:41
2026-10-08T15:04:40,badge_accel_variance,employee=silas_q,2.509,2026-10-08T15:07:41
2026-10-08T15:04:40,badge_accel_variance,employee=winifred_e,0.0,2026-10-08T15:07:41
2026-10-08T15:04:50,badge_accel_variance,employee=agnes_k,2.655,2026-10-08T15:07:41
2026-10-08T15:04:50,badge_accel_variance,employee=bertram_l,0.147,2026-10-08T15:07:41
2026-10-08T15:04:50,badge_accel_variance,employee=clement_w,0.0,2026-10-08T15:07:41
2026-10-08T15:04:50,badge_accel_variance,employee=dorothy_p,0.0,2026-10-08T15:07:41
2026-10-08T15:04:50,badge_accel_variance,employee=eustace_m,0.0,2026-10-08T15:07:41
2026-10-08T15:04:50,badge_accel_variance,employee=fern_o,3.363,2026-10-08T15:07:41
2026-10-08T15:04:50,badge_accel_variance,employee=gideon_r,1.668,2026-10-08T15:07:41
2026-10-08T15:04:50,badge_accel_variance,employee=harriet_s,0.0,2026-10-08T15:07:41
2026-10-08T15:04:50,badge_accel_variance,employee=milo_d,0.0,2026-10-08T15:07:41
2026-10-08T15:04:50,badge_accel_variance,employee=silas_q,0.97,2026-10-08T15:07:41
2026-10-08T15:04:50,badge_accel_variance,employee=winifred_e,0.0,2026-10-08T15:07:41
2026-10-08T15:05:00,badge_accel_variance,employee=agnes_k,1.68,2026-10-08T15:07:41
2026-10-08T15:05:00,badge_accel_variance,employee=bertram_l,0.119,2026-10-08T15:07:41
2026-10-08T15:05:00,badge_accel_variance,employee=clement_w,0.0,2026-10-08T15:07:41
2026-10-08T15:05:00,badge_accel_variance,employee=dorothy_p,0.0,2026-10-08T15:07:41
2026-10-08T15:05:00,badge_accel_variance,employee=eustace_m,0.0,2026-10-08T15:07:41
2026-10-08T15:05:00,badge_accel_variance,employee=fern_o,2.042,2026-10-08T15:07:41
2026-10-08T15:05:00,badge_accel_variance,employee=gideon_r,0.924,2026-10-08T15:07:41
2026-10-08T15:05:00,badge_accel_variance,employee=harriet_s,0.0,2026-10-08T15:07:41
2026-10-08T15:05:00,badge_accel_variance,employee=milo_d,0.0,2026-10-08T15:07:41
2026-10-08T15:05:00,badge_accel_variance,employee=silas_q,0.941,2026-10-08T15:07:41
2026-10-08T15:05:00,badge_accel_variance,employee=winifred_e,0.0,2026-10-08T15:07:41
2026-10-08T15:05:10,badge_accel_variance,employee=agnes_k,1.944,2026-10-08T15:07:41
2026-10-08T15:05:10,badge_accel_variance,employee=bertram_l,0.095,2026-10-08T15:07:41
2026-10-08T15:05:10,badge_accel_variance,employee=clement_w,0.0,2026-10-08T15:07:41
2026-10-08T15:05:10,badge_accel_variance,employee=dorothy_p,0.0,2026-10-08T15:07:41
2026-10-08T15:05:10,badge_accel_variance,employee=eustace_m,0.0,2026-10-08T15:07:41
2026-10-08T15:05:10,badge_accel_variance,employee=fern_o,1.604,2026-10-08T15:07:41
2026-10-08T15:05:10,badge_accel_variance,employee=gideon_r,2.312,2026-10-08T15:07:41
2026-10-08T15:05:10,badge_accel_variance,employee=harriet_s,0.0,2026-10-08T15:07:41
2026-10-08T15:05:10,badge_accel_variance,employee=milo_d,0.0,2026-10-08T15:07:41
2026-10-08T15:05:10,badge_accel_variance,employee=silas_q,1.846,2026-10-08T15:07:41
2026-10-08T15:05:10,badge_accel_variance,employee=winifred_e,0.0,2026-10-08T15:07:41
2026-10-08T15:05:20,badge_accel_variance,employee=agnes_k,3.249,2026-10-08T15:07:41
2026-10-08T15:05:20,badge_accel_variance,employee=bertram_l,0.211,2026-10-08T15:07:41
2026-10-08T15:05:20,badge_accel_variance,employee=clement_w,0.0,2026-10-08T15:07:41
2026-10-08T15:05:20,badge_accel_variance,employee=dorothy_p,0.0,2026-10-08T15:07:41
2026-10-08T15:05:20,badge_accel_variance,employee=eustace_m,0.0,2026-10-08T15:07:41
2026-10-08T15:05:20,badge_accel_variance,employee=fern_o,1.983,2026-10-08T15:07:41
2026-10-08T15:05:20,badge_accel_variance,employee=gideon_r,2.469,2026-10-08T15:07:41
2026-10-08T15:05:20,badge_accel_variance,employee=harriet_s,0.0,2026-10-08T15:07:41
2026-10-08T15:05:20,badge_accel_variance,employee=milo_d,0.0,2026-10-08T15:07:41
2026-10-08T15:05:20,badge_accel_variance,employee=silas_q,1.975,2026-10-08T15:07:41
2026-10-08T15:05:20,badge_accel_variance,employee=winifred_e,0.0,2026-10-08T15:07:41
2026-10-08T15:05:30,badge_accel_variance,employee=agnes_k,1.596,2026-10-08T15:07:41
2026-10-08T15:05:30,badge_accel_variance,employee=bertram_l,0.096,2026-10-08T15:07:41
2026-10-08T15:05:30,badge_accel_variance,employee=clement_w,0.0,2026-10-08T15:07:41
2026-10-08T15:05:30,badge_accel_variance,employee=dorothy_p,0.0,2026-10-08T15:07:41
2026-10-08T15:05:30,badge_accel_variance,employee=eustace_m,0.0,2026-10-08T15:07:41
2026-10-08T15:05:30,badge_accel_variance,employee=fern_o,3.537,2026-10-08T15:07:41
2026-10-08T15:05:30,badge_accel_variance,employee=gideon_r,3.082,2026-10-08T15:07:41
2026-10-08T15:05:30,badge_accel_variance,employee=harriet_s,0.0,2026-10-08T15:07:41
2026-10-08T15:05:30,badge_accel_variance,employee=milo_d,0.0,2026-10-08T15:07:41
2026-10-08T15:05:30,badge_accel_variance,employee=silas_q,3.545,2026-10-08T15:07:41
2026-10-08T15:05:30,badge_accel_variance,employee=winifred_e,0.0,2026-10-08T15:07:41
2026-10-08T15:05:40,badge_accel_variance,employee=agnes_k,0.923,2026-10-08T15:07:41
2026-10-08T15:05:40,badge_accel_variance,employee=bertram_l,0.143,2026-10-08T15:07:41
2026-10-08T15:05:40,badge_accel_variance,employee=clement_w,0.0,2026-10-08T15:07:41
2026-10-08T15:05:40,badge_accel_variance,employee=dorothy_p,0.0,2026-10-08T15:07:41
2026-10-08T15:05:40,badge_accel_variance,employee=eustace_m,0.0,2026-10-08T15:07:41
2026-10-08T15:05:40,badge_accel_variance,employee=fern_o,3.409,2026-10-08T15:07:41
2026-10-08T15:05:40,badge_accel_variance,employee=gideon_r,2.183,2026-10-08T15:07:41
2026-10-08T15:05:40,badge_accel_variance,employee=harriet_s,3.269,2026-10-08T15:07:41
2026-10-08T15:05:40,badge_accel_variance,employee=milo_d,0.0,2026-10-08T15:07:41
2026-10-08T15:05:40,badge_accel_variance,employee=silas_q,3.201,2026-10-08T15:07:41
2026-10-08T15:05:40,badge_accel_variance,employee=winifred_e,0.0,2026-10-08T15:07:41
2026-10-08T15:05:50,badge_accel_variance,employee=agnes_k,1.925,2026-10-08T15:07:41
2026-10-08T15:05:50,badge_accel_variance,employee=bertram_l,0.151,2026-10-08T15:07:41
2026-10-08T15:05:50,badge_accel_variance,employee=clement_w,0.756,2026-10-08T15:07:41
2026-10-08T15:05:50,badge_accel_variance,employee=dorothy_p,0.0,2026-10-08T15:07:41
2026-10-08T15:05:50,badge_accel_variance,employee=eustace_m,0.0,2026-10-08T15:07:41
2026-10-08T15:05:50,badge_accel_variance,employee=fern_o,1.42,2026-10-08T15:07:41
2026-10-08T15:05:50,badge_accel_variance,employee=gideon_r,2.204,2026-10-08T15:07:41
2026-10-08T15:05:50,badge_accel_variance,employee=harriet_s,2.23,2026-10-08T15:07:41
2026-10-08T15:05:50,badge_accel_variance,employee=milo_d,0.0,2026-10-08T15:07:41
2026-10-08T15:05:50,badge_accel_variance,employee=silas_q,1.201,2026-10-08T15:07:41
2026-10-08T15:05:50,badge_accel_variance,employee=winifred_e,0.0,2026-10-08T15:07:41
2026-10-08T15:06:00,badge_accel_variance,employee=agnes_k,0.97,2026-10-08T15:07:41
2026-10-08T15:06:00,badge_accel_variance,employee=bertram_l,0.169,2026-10-08T15:07:41
2026-10-08T15:06:00,badge_accel_variance,employee=clement_w,0.791,2026-10-08T15:07:41
2026-10-08T15:06:00,badge_accel_variance,employee=dorothy_p,0.0,2026-10-08T15:07:41
2026-10-08T15:06:00,badge_accel_variance,employee=eustace_m,0.0,2026-10-08T15:07:41
2026-10-08T15:06:00,badge_accel_variance,employee=fern_o,2.466,2026-10-08T15:07:41
2026-10-08T15:06:00,badge_accel_variance,employee=gideon_r,1.886,2026-10-08T15:07:41
2026-10-08T15:06:00,badge_accel_variance,employee=harriet_s,1.83,2026-10-08T15:07:41
2026-10-08T15:06:00,badge_accel_variance,employee=milo_d,0.0,2026-10-08T15:07:41
2026-10-08T15:06:00,badge_accel_variance,employee=silas_q,3.142,2026-10-08T15:07:41
2026-10-08T15:06:00,badge_accel_variance,employee=winifred_e,0.0,2026-10-08T15:07:41
2026-10-08T15:06:10,badge_accel_variance,employee=agnes_k,3.682,2026-10-08T15:07:41
2026-10-08T15:06:10,badge_accel_variance,employee=bertram_l,0.061,2026-10-08T15:07:41
2026-10-08T15:06:10,badge_accel_variance,employee=clement_w,0.454,2026-10-08T15:07:41
2026-10-08T15:06:10,badge_accel_variance,employee=dorothy_p,0.0,2026-10-08T15:07:41
2026-10-08T15:06:10,badge_accel_variance,employee=eustace_m,0.647,2026-10-08T15:07:41
2026-10-08T15:06:10,badge_accel_variance,employee=fern_o,2.472,2026-10-08T15:07:41
2026-10-08T15:06:10,badge_accel_variance,employee=gideon_r,1.269,2026-10-08T15:07:41
2026-10-08T15:06:10,badge_accel_variance,employee=harriet_s,2.366,2026-10-08T15:07:41
2026-10-08T15:06:10,badge_accel_variance,employee=milo_d,0.0,2026-10-08T15:07:41
2026-10-08T15:06:10,badge_accel_variance,employee=silas_q,0.99,2026-10-08T15:07:41
2026-10-08T15:06:10,badge_accel_variance,employee=winifred_e,0.0,2026-10-08T15:07:41
2026-10-08T15:06:20,badge_accel_variance,employee=agnes_k,1.249,2026-10-08T15:07:41
2026-10-08T15:06:20,badge_accel_variance,employee=bertram_l,0.143,2026-10-08T15:07:41
2026-10-08T15:06:20,badge_accel_variance,employee=clement_w,0.511,2026-10-08T15:07:41
2026-10-08T15:06:20,badge_accel_variance,employee=dorothy_p,0.0,2026-10-08T15:07:41
2026-10-08T15:06:20,badge_accel_variance,employee=eustace_m,0.398,2026-10-08T15:07:41
2026-10-08T15:06:20,badge_accel_variance,employee=fern_o,2.673,2026-10-08T15:07:41
2026-10-08T15:06:20,badge_accel_variance,employee=gideon_r,3.168,2026-10-08T15:07:41
2026-10-08T15:06:20,badge_accel_variance,employee=harriet_s,3.377,2026-10-08T15:07:41
2026-10-08T15:06:20,badge_accel_variance,employee=milo_d,0.0,2026-10-08T15:07:41
2026-10-08T15:06:20,badge_accel_variance,employee=silas_q,2.641,2026-10-08T15:07:41
2026-10-08T15:06:20,badge_accel_variance,employee=winifred_e,2.146,2026-10-08T15:07:41
2026-10-08T15:06:30,badge_accel_variance,employee=agnes_k,1.817,2026-10-08T15:07:41
2026-10-08T15:06:30,badge_accel_variance,employee=bertram_l,2.52,2026-10-08T15:07:41
2026-10-08T15:06:30,badge_accel_variance,employee=clement_w,0.799,2026-10-08T15:07:41
2026-10-08T15:06:30,badge_accel_variance,employee=dorothy_p,0.0,2026-10-08T15:07:41
2026-10-08T15:06:30,badge_accel_variance,employee=eustace_m,0.563,2026-10-08T15:07:41
2026-10-08T15:06:30,badge_accel_variance,employee=fern_o,3.559,2026-10-08T15:07:41
2026-10-08T15:06:30,badge_accel_variance,employee=gideon_r,3.217,2026-10-08T15:07:41
2026-10-08T15:06:30,badge_accel_variance,employee=harriet_s,3.054,2026-10-08T15:07:41
2026-10-08T15:06:30,badge_accel_variance,employee=milo_d,0.0,2026-10-08T15:07:41
2026-10-08T15:06:30,badge_accel_variance,employee=silas_q,2.942,2026-10-08T15:07:41
2026-10-08T15:06:30,badge_accel_variance,employee=winifred_e,3.654,2026-10-08T15:07:41
2026-10-08T15:06:40,badge_accel_variance,employee=agnes_k,2.39,2026-10-08T15:07:41
2026-10-08T15:06:40,badge_accel_variance,employee=bertram_l,2.124,2026-10-08T15:07:41
2026-10-08T15:06:40,badge_accel_variance,employee=clement_w,0.771,2026-10-08T15:07:41
2026-10-08T15:06:40,badge_accel_variance,employee=dorothy_p,0.0,2026-10-08T15:07:41
2026-10-08T15:06:40,badge_accel_variance,employee=eustace_m,0.497,2026-10-08T15:07:41
2026-10-08T15:06:40,badge_accel_variance,employee=fern_o,3.415,2026-10-08T15:07:41
2026-10-08T15:06:40,badge_accel_variance,employee=gideon_r,3.797,2026-10-08T15:07:41
2026-10-08T15:06:40,badge_accel_variance,employee=harriet_s,2.174,2026-10-08T15:07:41
2026-10-08T15:06:40,badge_accel_variance,employee=milo_d,1.343,2026-10-08T15:07:41
2026-10-08T15:06:40,badge_accel_variance,employee=silas_q,3.747,2026-10-08T15:07:41
2026-10-08T15:06:40,badge_accel_variance,employee=winifred_e,2.44,2026-10-08T15:07:41
2026-10-08T15:06:50,badge_accel_variance,employee=agnes_k,2.567,2026-10-08T15:07:41
2026-10-08T15:06:50,badge_accel_variance,employee=bertram_l,1.43,2026-10-08T15:07:41
2026-10-08T15:06:50,badge_accel_variance,employee=clement_w,0.722,2026-10-08T15:07:41
2026-10-08T15:06:50,badge_accel_variance,employee=dorothy_p,0.0,2026-10-08T15:07:41
2026-10-08T15:06:50,badge_accel_variance,employee=eustace_m,0.649,2026-10-08T15:07:41
2026-10-08T15:06:50,badge_accel_variance,employee=fern_o,1.697,2026-10-08T15:07:41
2026-10-08T15:06:50,badge_accel_variance,employee=gideon_r,2.911,2026-10-08T15:07:41
2026-10-08T15:06:50,badge_accel_variance,employee=harriet_s,1.856,2026-10-08T15:07:41
2026-10-08T15:06:50,badge_accel_variance,employee=milo_d,1.571,2026-10-08T15:07:41
2026-10-08T15:06:50,badge_accel_variance,employee=silas_q,0.982,2026-10-08T15:07:41
2026-10-08T15:06:50,badge_accel_variance,employee=winifred_e,1.122,2026-10-08T15:07:41
2026-10-08T15:07:00,badge_accel_variance,employee=agnes_k,0.247,
2026-10-08T15:07:00,badge_accel_variance,employee=bertram_l,0.18,
2026-10-08T15:07:00,badge_accel_variance,employee=clement_w,0.785,
2026-10-08T15:07:00,badge_accel_variance,employee=dorothy_p,0.0,
2026-10-08T15:07:00,badge_accel_variance,employee=eustace_m,0.737,
2026-10-08T15:07:00,badge_accel_variance,employee=fern_o,0.132,
2026-10-08T15:07:00,badge_accel_variance,employee=gideon_r,0.264,
2026-10-08T15:07:00,badge_accel_variance,employee=harriet_s,0.185,
2026-10-08T15:07:00,badge_accel_variance,employee=milo_d,0.229,
2026-10-08T15:07:00,badge_accel_variance,employee=silas_q,0.11,
2026-10-08T15:07:00,badge_accel_variance,employee=winifred_e,0.267,
2026-10-08T15:07:10,badge_accel_variance,employee=agnes_k,0.174,
2026-10-08T15:07:10,badge_accel_variance,employee=bertram_l,0.194,
2026-10-08T15:07:10,badge_accel_variance,employee=clement_w,0.437,
2026-10-08T15:07:10,badge_accel_variance,employee=dorothy_p,0.0,
2026-10-08T15:07:10,badge_accel_variance,employee=eustace_m,0.558,
2026-10-08T15:07:10,badge_accel_variance,employee=fern_o,0.327,
2026-10-08T15:07:10,badge_accel_variance,employee=gideon_r,0.288,
2026-10-08T15:07:10,badge_accel_variance,employee=harriet_s,0.278,
2026-10-08T15:07:10,badge_accel_variance,employee=milo_d,0.077,
2026-10-08T15:07:10,badge_accel_variance,employee=silas_q,0.18,
2026-10-08T15:07:10,badge_accel_variance,employee=winifred_e,0.07,
2026-10-08T15:07:20,badge_accel_variance,employee=agnes_k,0.086,
2026-10-08T15:07:20,badge_accel_variance,employee=bertram_l,0.355,
2026-10-08T15:07:20,badge_accel_variance,employee=clement_w,0.495,
2026-10-08T15:07:20,badge_accel_variance,employee=dorothy_p,0.0,
2026-10-08T15:07:20,badge_accel_variance,employee=eustace_m,0.56,
2026-10-08T15:07:20,badge_accel_variance,employee=fern_o,0.156,
2026-10-08T15:07:20,badge_accel_variance,employee=gideon_r,0.105,
2026-10-08T15:07:20,badge_accel_variance,employee=harriet_s,0.086,
2026-10-08T15:07:20,badge_accel_variance,employee=milo_d,0.26,
2026-10-08T15:07:20,badge_accel_variance,employee=silas_q,0.153,
2026-10-08T15:07:20,badge_accel_variance,employee=winifred_e,0.174,
2026-10-08T15:07:30,badge_accel_variance,employee=agnes_k,0.214,
2026-10-08T15:07:30,badge_accel_variance,employee=bertram_l,0.146,
2026-10-08T15:07:30,badge_accel_variance,employee=clement_w,0.313,
2026-10-08T15:07:30,badge_accel_variance,employee=dorothy_p,0.0,
2026-10-08T15:07:30,badge_accel_variance,employee=eustace_m,0.374,
2026-10-08T15:07:30,badge_accel_variance,employee=fern_o,0.066,
2026-10-08T15:07:30,badge_accel_variance,employee=gideon_r,0.256,
2026-10-08T15:07:30,badge_accel_variance,employee=harriet_s,0.105,
2026-10-08T15:07:30,badge_accel_variance,employee=milo_d,0.158,
2026-10-08T15:07:30,badge_accel_variance,employee=silas_q,0.105,
2026-10-08T15:07:30,badge_accel_variance,employee=winifred_e,0.164,
2026-10-08T15:07:40,badge_accel_variance,employee=agnes_k,0.368,
2026-10-08T15:07:40,badge_accel_variance,employee=bertram_l,0.236,
2026-10-08T15:07:40,badge_accel_variance,employee=clement_w,0.473,
2026-10-08T15:07:40,badge_accel_variance,employee=dorothy_p,0.63,
2026-10-08T15:07:40,badge_accel_variance,employee=eustace_m,0.497,
2026-10-08T15:07:40,badge_accel_variance,employee=fern_o,0.23,
2026-10-08T15:07:40,badge_accel_variance,employee=gideon_r,0.104,
2026-10-08T15:07:40,badge_accel_variance,employee=harriet_s,0.076,
2026-10-08T15:07:40,badge_accel_variance,employee=milo_d,0.18,
2026-10-08T15:07:40,badge_accel_variance,employee=silas_q,0.262,
2026-10-08T15:07:40,badge_accel_variance,employee=winifred_e,0.115,
2026-10-08T15:07:50,badge_accel_variance,employee=agnes_k,0.294,
2026-10-08T15:07:50,badge_accel_variance,employee=bertram_l,0.133,
2026-10-08T15:07:50,badge_accel_variance,employee=clement_w,0.765,
2026-10-08T15:07:50,badge_accel_variance,employee=dorothy_p,0.683,
2026-10-08T15:07:50,badge_accel_variance,employee=eustace_m,0.727,
2026-10-08T15:07:50,badge_accel_variance,employee=fern_o,0.201,
2026-10-08T15:07:50,badge_accel_variance,employee=gideon_r,0.084,
2026-10-08T15:07:50,badge_accel_variance,employee=harriet_s,0.242,
2026-10-08T15:07:50,badge_accel_variance,employee=milo_d,0.104,
2026-10-08T15:07:50,badge_accel_variance,employee=silas_q,0.065,
2026-10-08T15:07:50,badge_accel_variance,employee=winifred_e,0.143,
2026-10-08T15:08:00,badge_accel_variance,employee=agnes_k,0.263,
2026-10-08T15:08:00,badge_accel_variance,employee=bertram_l,0.399,
2026-10-08T15:08:00,badge_accel_variance,employee=clement_w,0.509,
2026-10-08T15:08:00,badge_accel_variance,employee=dorothy_p,0.399,
2026-10-08T15:08:00,badge_accel_variance,employee=eustace_m,0.458,
2026-10-08T15:08:00,badge_accel_variance,employee=fern_o,0.337,
2026-10-08T15:08:00,badge_accel_variance,employee=gideon_r,0.056,
2026-10-08T15:08:00,badge_accel_variance,employee=harriet_s,0.27,
2026-10-08T15:08:00,badge_accel_variance,employee=milo_d,0.261,
2026-10-08T15:08:00,badge_accel_variance,employee=silas_q,0.198,
2026-10-08T15:08:00,badge_accel_variance,employee=winifred_e,0.189,
2026-10-08T15:08:10,badge_accel_variance,employee=agnes_k,0.363,
2026-10-08T15:08:10,badge_accel_variance,employee=bertram_l,0.276,
2026-10-08T15:08:10,badge_accel_variance,employee=clement_w,0.781,
2026-10-08T15:08:10,badge_accel_variance,employee=dorothy_p,0.711,
2026-10-08T15:08:10,badge_accel_variance,employee=eustace_m,0.677,
2026-10-08T15:08:10,badge_accel_variance,employee=fern_o,0.099,
2026-10-08T15:08:10,badge_accel_variance,employee=gideon_r,0.283,
2026-10-08T15:08:10,badge_accel_variance,employee=harriet_s,0.123,
2026-10-08T15:08:10,badge_accel_variance,employee=milo_d,0.216,
2026-10-08T15:08:10,badge_accel_variance,employee=silas_q,0.278,
2026-10-08T15:08:10,badge_accel_variance,employee=winifred_e,0.258,
2026-10-08T15:08:20,badge_accel_variance,employee=agnes_k,0.081,
2026-10-08T15:08:20,badge_accel_variance,employee=bertram_l,0.169,
2026-10-08T15:08:20,badge_accel_variance,employee=clement_w,0.432,
2026-10-08T15:08:20,badge_accel_variance,employee=dorothy_p,0.612,
2026-10-08T15:08:20,badge_accel_variance,employee=eustace_m,0.598,
2026-10-08T15:08:20,badge_accel_variance,employee=fern_o,0.302,
2026-10-08T15:08:20,badge_accel_variance,employee=gideon_r,0.263,
2026-10-08T15:08:20,badge_accel_variance,employee=harriet_s,0.124,
2026-10-08T15:08:20,badge_accel_variance,employee=milo_d,0.151,
2026-10-08T15:08:20,badge_accel_variance,employee=silas_q,0.228,
2026-10-08T15:08:20,badge_accel_variance,employee=winifred_e,0.203,
2026-10-08T15:08:30,badge_accel_variance,employee=agnes_k,0.275,
2026-10-08T15:08:30,badge_accel_variance,employee=bertram_l,0.353,
2026-10-08T15:08:30,badge_accel_variance,employee=clement_w,0.494,
2026-10-08T15:08:30,badge_accel_variance,employee=dorothy_p,0.775,
2026-10-08T15:08:30,badge_accel_variance,employee=eustace_m,0.441,
2026-10-08T15:08:30,badge_accel_variance,employee=fern_o,0.363,
2026-10-08T15:08:30,badge_accel_variance,employee=gideon_r,0.216,
2026-10-08T15:08:30,badge_accel_variance,employee=harriet_s,0.075,
2026-10-08T15:08:30,badge_accel_variance,employee=milo_d,0.093,
2026-10-08T15:08:30,badge_accel_variance,employee=silas_q,0.103,
2026-10-08T15:08:30,badge_accel_variance,employee=winifred_e,0.165,
2026-10-08T15:08:40,badge_accel_variance,employee=agnes_k,0.23,
2026-10-08T15:08:40,badge_accel_variance,employee=bertram_l,0.373,
2026-10-08T15:08:40,badge_accel_variance,employee=clement_w,0.575,
2026-10-08T15:08:40,badge_accel_variance,employee=dorothy_p,0.465,
2026-10-08T15:08:40,badge_accel_variance,employee=eustace_m,0.701,
2026-10-08T15:08:40,badge_accel_variance,employee=fern_o,0.182,
2026-10-08T15:08:40,badge_accel_variance,employee=gideon_r,0.168,
2026-10-08T15:08:40,badge_accel_variance,employee=harriet_s,0.118,
2026-10-08T15:08:40,badge_accel_variance,employee=milo_d,0.081,
2026-10-08T15:08:40,badge_accel_variance,employee=silas_q,0.147,
2026-10-08T15:08:40,badge_accel_variance,employee=winifred_e,0.275,
2026-10-08T15:08:50,badge_accel_variance,employee=agnes_k,0.267,
2026-10-08T15:08:50,badge_accel_variance,employee=bertram_l,0.349,
2026-10-08T15:08:50,badge_accel_variance,employee=clement_w,0.453,
2026-10-08T15:08:50,badge_accel_variance,employee=dorothy_p,0.377,
2026-10-08T15:08:50,badge_accel_variance,employee=eustace_m,0.604,
2026-10-08T15:08:50,badge_accel_variance,employee=fern_o,0.272,
2026-10-08T15:08:50,badge_accel_variance,employee=gideon_r,0.076,
2026-10-08T15:08:50,badge_accel_variance,employee=harriet_s,0.078,
2026-10-08T15:08:50,badge_accel_variance,employee=milo_d,0.263,
2026-10-08T15:08:50,badge_accel_variance,employee=silas_q,0.175,
2026-10-08T15:08:50,badge_accel_variance,employee=winifred_e,0.064,
2026-10-08T15:09:00,badge_accel_variance,employee=agnes_k,0.112,
2026-10-08T15:09:00,badge_accel_variance,employee=bertram_l,0.215,
2026-10-08T15:09:00,badge_accel_variance,employee=clement_w,0.542,
2026-10-08T15:09:00,badge_accel_variance,employee=dorothy_p,0.775,
2026-10-08T15:09:00,badge_accel_variance,employee=eustace_m,0.338,
2026-10-08T15:09:00,badge_accel_variance,employee=fern_o,0.052,
2026-10-08T15:09:00,badge_accel_variance,employee=gideon_r,0.221,
2026-10-08T15:09:00,badge_accel_variance,employee=harriet_s,0.149,
2026-10-08T15:09:00,badge_accel_variance,employee=milo_d,0.109,
2026-10-08T15:09:00,badge_accel_variance,employee=silas_q,0.192,
2026-10-08T15:09:00,badge_accel_variance,employee=winifred_e,0.228,
2026-10-08T15:09:10,badge_accel_variance,employee=agnes_k,0.279,
2026-10-08T15:09:10,badge_accel_variance,employee=bertram_l,0.291,
2026-10-08T15:09:10,badge_accel_variance,employee=clement_w,0.615,
2026-10-08T15:09:10,badge_accel_variance,employee=dorothy_p,0.423,
2026-10-08T15:09:10,badge_accel_variance,employee=eustace_m,0.376,
2026-10-08T15:09:10,badge_accel_variance,employee=fern_o,0.107,
2026-10-08T15:09:10,badge_accel_variance,employee=gideon_r,0.165,
2026-10-08T15:09:10,badge_accel_variance,employee=harriet_s,0.173,
2026-10-08T15:09:10,badge_accel_variance,employee=milo_d,0.228,
2026-10-08T15:09:10,badge_accel_variance,employee=silas_q,0.143,
2026-10-08T15:09:10,badge_accel_variance,employee=winifred_e,0.149,
2026-10-08T15:09:20,badge_accel_variance,employee=agnes_k,0.28,
2026-10-08T15:09:20,badge_accel_variance,employee=bertram_l,0.33,
2026-10-08T15:09:20,badge_accel_variance,employee=clement_w,0.323,
2026-10-08T15:09:20,badge_accel_variance,employee=dorothy_p,0.729,
2026-10-08T15:09:20,badge_accel_variance,employee=eustace_m,0.665,
2026-10-08T15:09:20,badge_accel_variance,employee=fern_o,0.122,
2026-10-08T15:09:20,badge_accel_variance,employee=gideon_r,0.29,
2026-10-08T15:09:20,badge_accel_variance,employee=harriet_s,0.061,
2026-10-08T15:09:20,badge_accel_variance,employee=milo_d,0.178,
2026-10-08T15:09:20,badge_accel_variance,employee=silas_q,0.202,
2026-10-08T15:09:20,badge_accel_variance,employee=winifred_e,0.175,
2026-10-08T15:06:30,badge_accel_peak_g,employee=bertram_l,4.7,2026-10-08T15:07:41
2026-10-08T15:03:56,badge_accel_peak_g,employee=agnes_k,2.9,2026-10-08T15:07:41
2026-10-08T15:04:31,badge_accel_peak_g,employee=fern_o,3.9,2026-10-08T15:07:41
2026-10-08T15:00:00,sleep_band_heart_rate_bpm,employee=hale_r,86,
2026-10-08T15:00:05,sleep_band_heart_rate_bpm,employee=hale_r,78,
2026-10-08T15:00:10,sleep_band_heart_rate_bpm,employee=hale_r,80,
2026-10-08T15:00:15,sleep_band_heart_rate_bpm,employee=hale_r,78,
2026-10-08T15:00:20,sleep_band_heart_rate_bpm,employee=hale_r,76,
2026-10-08T15:00:25,sleep_band_heart_rate_bpm,employee=hale_r,84,
2026-10-08T15:00:30,sleep_band_heart_rate_bpm,employee=hale_r,78,
2026-10-08T15:00:35,sleep_band_heart_rate_bpm,employee=hale_r,76,
2026-10-08T15:00:40,sleep_band_heart_rate_bpm,employee=hale_r,76,
2026-10-08T15:00:45,sleep_band_heart_rate_bpm,employee=hale_r,80,
2026-10-08T15:00:50,sleep_band_heart_rate_bpm,employee=hale_r,81,
2026-10-08T15:00:55,sleep_band_heart_rate_bpm,employee=hale_r,80,
2026-10-08T15:01:00,sleep_band_heart_rate_bpm,employee=hale_r,81,
2026-10-08T15:01:05,sleep_band_heart_rate_bpm,employee=hale_r,84,
2026-10-08T15:01:10,sleep_band_heart_rate_bpm,employee=hale_r,84,
2026-10-08T15:01:15,sleep_band_heart_rate_bpm,employee=hale_r,77,
2026-10-08T15:01:20,sleep_band_heart_rate_bpm,employee=hale_r,77,
2026-10-08T15:01:25,sleep_band_heart_rate_bpm,employee=hale_r,77,
2026-10-08T15:01:30,sleep_band_heart_rate_bpm,employee=hale_r,77,
2026-10-08T15:01:35,sleep_band_heart_rate_bpm,employee=hale_r,83,
2026-10-08T15:01:40,sleep_band_heart_rate_bpm,employee=hale_r,80,
2026-10-08T15:01:45,sleep_band_heart_rate_bpm,employee=hale_r,81,
2026-10-08T15:01:50,sleep_band_heart_rate_bpm,employee=hale_r,83,
2026-10-08T15:01:55,sleep_band_heart_rate_bpm,employee=hale_r,82,
2026-10-08T15:02:00,sleep_band_heart_rate_bpm,employee=hale_r,75,2026-10-08T15:07:41
2026-10-08T15:02:05,sleep_band_heart_rate_bpm,employee=hale_r,85,2026-10-08T15:07:41
2026-10-08T15:02:10,sleep_band_heart_rate_bpm,employee=hale_r,80,2026-10-08T15:07:41
2026-10-08T15:02:15,sleep_band_heart_rate_bpm,employee=hale_r,86,2026-10-08T15:07:41
2026-10-08T15:02:20,sleep_band_heart_rate_bpm,employee=hale_r,81,2026-10-08T15:07:41
2026-10-08T15:02:25,sleep_band_heart_rate_bpm,employee=hale_r,80,2026-10-08T15:07:41
2026-10-08T15:02:30,sleep_band_heart_rate_bpm,employee=hale_r,76,2026-10-08T15:07:41
2026-10-08T15:02:35,sleep_band_heart_rate_bpm,employee=hale_r,78,2026-10-08T15:07:41
2026-10-08T15:02:40,sleep_band_heart_rate_bpm,employee=hale_r,84,2026-10-08T15:07:41
2026-10-08T15:02:45,sleep_band_heart_rate_bpm,employee=hale_r,81,2026-10-08T15:07:41
2026-10-08T15:02:50,sleep_band_heart_rate_bpm,employee=hale_r,77,2026-10-08T15:07:41
2026-10-08T15:02:55,sleep_band_heart_rate_bpm,employee=hale_r,83,2026-10-08T15:07:41
2026-10-08T15:03:00,sleep_band_heart_rate_bpm,employee=hale_r,85,2026-10-08T15:07:41
2026-10-08T15:03:05,sleep_band_heart_rate_bpm,employee=hale_r,77,2026-10-08T15:07:41
2026-10-08T15:03:10,sleep_band_heart_rate_bpm,employee=hale_r,74,2026-10-08T15:07:41
2026-10-08T15:03:15,sleep_band_heart_rate_bpm,employee=hale_r,74,2026-10-08T15:07:41
2026-10-08T15:03:20,sleep_band_heart_rate_bpm,employee=hale_r,79,2026-10-08T15:07:41
2026-10-08T15:03:25,sleep_band_heart_rate_bpm,employee=hale_r,86,2026-10-08T15:07:41
2026-10-08T15:03:30,sleep_band_heart_rate_bpm,employee=hale_r,78,2026-10-08T15:07:41
2026-10-08T15:03:35,sleep_band_heart_rate_bpm,employee=hale_r,80,2026-10-08T15:07:41
2026-10-08T15:03:40,sleep_band_heart_rate_bpm,employee=hale_r,82,2026-10-08T15:07:41
2026-10-08T15:03:45,sleep_band_heart_rate_bpm,employee=hale_r,108,2026-10-08T15:07:41
2026-10-08T15:03:50,sleep_band_heart_rate_bpm,employee=hale_r,121,2026-10-08T15:07:41
2026-10-08T15:03:55,sleep_band_heart_rate_bpm,employee=hale_r,123,2026-10-08T15:07:41
2026-10-08T15:04:00,sleep_band_heart_rate_bpm,employee=hale_r,109,2026-10-08T15:07:41
2026-10-08T15:04:05,sleep_band_heart_rate_bpm,employee=hale_r,148,2026-10-08T15:07:41
2026-10-08T15:04:10,sleep_band_heart_rate_bpm,employee=hale_r,151,2026-10-08T15:07:41
2026-10-08T15:04:15,sleep_band_heart_rate_bpm,employee=hale_r,138,2026-10-08T15:07:41
2026-10-08T15:04:20,sleep_band_heart_rate_bpm,employee=hale_r,158,2026-10-08T15:07:41
2026-10-08T15:04:25,sleep_band_heart_rate_bpm,employee=hale_r,47,2026-10-08T15:07:41
2026-10-08T15:04:30,sleep_band_heart_rate_bpm,employee=hale_r,46,2026-10-08T15:07:41
2026-10-08T15:04:35,sleep_band_heart_rate_bpm,employee=hale_r,57,2026-10-08T15:07:41
2026-10-08T15:04:40,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:04:45,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:04:50,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:04:55,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:05:00,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:05:05,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:05:10,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:05:15,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:05:20,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:05:25,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:05:30,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:05:35,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:05:40,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:05:45,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:05:50,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:05:55,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:06:00,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:06:05,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:06:10,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:06:15,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:06:20,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:06:25,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:06:30,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:06:35,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:06:40,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:06:45,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:06:50,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:06:55,sleep_band_heart_rate_bpm,employee=hale_r,0,2026-10-08T15:07:41
2026-10-08T15:00:00,elevator_car_occupied,car=1,0,
2026-10-08T15:00:15,elevator_car_occupied,car=1,0,
2026-10-08T15:00:30,elevator_car_occupied,car=1,0,
2026-10-08T15:00:45,elevator_car_occupied,car=1,0,
2026-10-08T15:01:00,elevator_car_occupied,car=1,0,
2026-10-08T15:01:15,elevator_car_occupied,car=1,0,
2026-10-08T15:01:30,elevator_car_occupied,car=1,1,
2026-10-08T15:01:45,elevator_car_occupied,car=1,1,
2026-10-08T15:02:00,elevator_car_occupied,car=1,1,2026-10-08T15:07:41
2026-10-08T15:02:15,elevator_car_occupied,car=1,1,2026-10-08T15:07:41
2026-10-08T15:02:30,elevator_car_occupied,car=1,1,2026-10-08T15:07:41
2026-10-08T15:02:45,elevator_car_occupied,car=1,1,2026-10-08T15:07:41
2026-10-08T15:03:00,elevator_car_occupied,car=1,1,2026-10-08T15:07:41
2026-10-08T15:03:15,elevator_car_occupied,car=1,1,2026-10-08T15:07:41
2026-10-08T15:03:30,elevator_car_occupied,car=1,1,2026-10-08T15:07:41
2026-10-08T15:03:45,elevator_car_occupied,car=1,1,2026-10-08T15:07:41
2026-10-08T15:04:00,elevator_car_occupied,car=1,1,2026-10-08T15:07:41
2026-10-08T15:04:15,elevator_car_occupied,car=1,1,2026-10-08T15:07:41
2026-10-08T15:04:30,elevator_car_occupied,car=1,1,2026-10-08T15:07:41
2026-10-08T15:04:45,elevator_car_occupied,car=1,1,2026-10-08T15:07:41
2026-10-08T15:05:00,elevator_car_occupied,car=1,1,2026-10-08T15:07:41
2026-10-08T15:05:15,elevator_car_occupied,car=1,1,2026-10-08T15:07:41
2026-10-08T15:05:30,elevator_car_occupied,car=1,1,2026-10-08T15:07:41
2026-10-08T15:05:45,elevator_car_occupied,car=1,1,2026-10-08T15:07:41
2026-10-08T15:06:00,elevator_car_occupied,car=1,1,2026-10-08T15:07:41
2026-10-08T15:06:15,elevator_car_occupied,car=1,1,2026-10-08T15:07:41
2026-10-08T15:06:30,elevator_car_occupied,car=1,1,2026-10-08T15:07:41
2026-10-08T15:06:45,elevator_car_occupied,car=1,1,2026-10-08T15:07:41
2026-09-24T17:00:00,sleep_ring_lock_min,employee=agnes_k,0.995,
2026-09-24T17:00:00,sleep_ring_lock_min,employee=bertram_l,0.963,
2026-09-24T17:00:00,sleep_ring_lock_min,employee=clement_w,0.918,
2026-09-24T17:00:00,sleep_ring_lock_min,employee=dorothy_p,0.994,
2026-09-24T17:00:00,sleep_ring_lock_min,employee=eustace_m,0.981,
2026-09-24T17:00:00,sleep_ring_lock_min,employee=fern_o,0.862,
2026-09-24T17:00:00,sleep_ring_lock_min,employee=gideon_r,0.878,
2026-09-24T17:00:00,sleep_ring_lock_min,employee=harriet_s,0.882,
2026-09-24T17:00:00,sleep_ring_lock_min,employee=ivo_t,0.918,
2026-09-24T17:00:00,sleep_ring_lock_min,employee=judith_v,0.978,
2026-09-24T17:00:00,sleep_ring_lock_min,employee=kenneth_y,0.954,
2026-09-24T17:00:00,sleep_ring_lock_min,employee=lorna_b,0.979,
2026-09-24T17:00:00,sleep_ring_lock_min,employee=milo_d,0.971,
2026-09-24T17:00:00,sleep_ring_lock_min,employee=nadia_f,0.969,
2026-09-24T17:00:00,sleep_ring_lock_min,employee=otto_g,0.848,
2026-09-24T17:00:00,sleep_ring_lock_min,employee=prudence_h,0.955,
2026-09-24T17:00:00,sleep_ring_lock_min,employee=quentin_j,0.884,
2026-09-24T17:00:00,sleep_ring_lock_min,employee=rosalind_n,0.871,
2026-09-24T17:00:00,sleep_ring_lock_min,employee=silas_q,0.957,
2026-09-24T17:00:00,sleep_ring_lock_min,employee=tobias_u,0.956,
2026-09-24T17:00:00,sleep_ring_lock_min,employee=ursula_x,0.967,
2026-09-24T17:00:00,sleep_ring_lock_min,employee=vernon_z,0.994,
2026-09-24T17:00:00,sleep_ring_lock_min,employee=winifred_e,0.967,
2026-09-24T17:00:00,sleep_ring_lock_min,employee=cyril_a,0.986,
2026-09-25T17:00:00,sleep_ring_lock_min,employee=agnes_k,0.95,
2026-09-25T17:00:00,sleep_ring_lock_min,employee=bertram_l,0.986,
2026-09-25T17:00:00,sleep_ring_lock_min,employee=clement_w,0.909,
2026-09-25T17:00:00,sleep_ring_lock_min,employee=dorothy_p,0.981,
2026-09-25T17:00:00,sleep_ring_lock_min,employee=eustace_m,0.972,
2026-09-25T17:00:00,sleep_ring_lock_min,employee=fern_o,0.855,
2026-09-25T17:00:00,sleep_ring_lock_min,employee=gideon_r,0.914,
2026-09-25T17:00:00,sleep_ring_lock_min,employee=harriet_s,0.84,
2026-09-25T17:00:00,sleep_ring_lock_min,employee=ivo_t,0.89,
2026-09-25T17:00:00,sleep_ring_lock_min,employee=judith_v,0.964,
2026-09-25T17:00:00,sleep_ring_lock_min,employee=kenneth_y,0.99,
2026-09-25T17:00:00,sleep_ring_lock_min,employee=lorna_b,0.981,
2026-09-25T17:00:00,sleep_ring_lock_min,employee=milo_d,0.962,
2026-09-25T17:00:00,sleep_ring_lock_min,employee=nadia_f,0.987,
2026-09-25T17:00:00,sleep_ring_lock_min,employee=otto_g,0.912,
2026-09-25T17:00:00,sleep_ring_lock_min,employee=prudence_h,0.961,
2026-09-25T17:00:00,sleep_ring_lock_min,employee=quentin_j,0.898,
2026-09-25T17:00:00,sleep_ring_lock_min,employee=rosalind_n,0.917,
2026-09-25T17:00:00,sleep_ring_lock_min,employee=silas_q,0.994,
2026-09-25T17:00:00,sleep_ring_lock_min,employee=tobias_u,0.987,
2026-09-25T17:00:00,sleep_ring_lock_min,employee=ursula_x,0.952,
2026-09-25T17:00:00,sleep_ring_lock_min,employee=vernon_z,0.956,
2026-09-25T17:00:00,sleep_ring_lock_min,employee=winifred_e,0.952,
2026-09-25T17:00:00,sleep_ring_lock_min,employee=cyril_a,0.976,
2026-09-28T17:00:00,sleep_ring_lock_min,employee=agnes_k,0.966,
2026-09-28T17:00:00,sleep_ring_lock_min,employee=bertram_l,0.966,
2026-09-28T17:00:00,sleep_ring_lock_min,employee=clement_w,0.917,
2026-09-28T17:00:00,sleep_ring_lock_min,employee=dorothy_p,0.975,
2026-09-28T17:00:00,sleep_ring_lock_min,employee=eustace_m,0.965,
2026-09-28T17:00:00,sleep_ring_lock_min,employee=fern_o,0.851,
2026-09-28T17:00:00,sleep_ring_lock_min,employee=gideon_r,0.872,
2026-09-28T17:00:00,sleep_ring_lock_min,employee=harriet_s,0.872,
2026-09-28T17:00:00,sleep_ring_lock_min,employee=ivo_t,0.91,
2026-09-28T17:00:00,sleep_ring_lock_min,employee=judith_v,0.993,
2026-09-28T17:00:00,sleep_ring_lock_min,employee=kenneth_y,0.962,
2026-09-28T17:00:00,sleep_ring_lock_min,employee=lorna_b,0.99,
2026-09-28T17:00:00,sleep_ring_lock_min,employee=milo_d,0.994,
2026-09-28T17:00:00,sleep_ring_lock_min,employee=nadia_f,0.989,
2026-09-28T17:00:00,sleep_ring_lock_min,employee=otto_g,0.887,
2026-09-28T17:00:00,sleep_ring_lock_min,employee=prudence_h,0.97,
2026-09-28T17:00:00,sleep_ring_lock_min,employee=quentin_j,0.919,
2026-09-28T17:00:00,sleep_ring_lock_min,employee=rosalind_n,0.877,
2026-09-28T17:00:00,sleep_ring_lock_min,employee=silas_q,0.981,
2026-09-28T17:00:00,sleep_ring_lock_min,employee=tobias_u,0.956,
2026-09-28T17:00:00,sleep_ring_lock_min,employee=ursula_x,0.991,
2026-09-28T17:00:00,sleep_ring_lock_min,employee=vernon_z,0.991,
2026-09-28T17:00:00,sleep_ring_lock_min,employee=winifred_e,0.956,
2026-09-28T17:00:00,sleep_ring_lock_min,employee=cyril_a,0.981,
2026-09-29T17:00:00,sleep_ring_lock_min,employee=agnes_k,0.966,
2026-09-29T17:00:00,sleep_ring_lock_min,employee=bertram_l,0.954,
2026-09-29T17:00:00,sleep_ring_lock_min,employee=clement_w,0.915,
2026-09-29T17:00:00,sleep_ring_lock_min,employee=dorothy_p,0.967,
2026-09-29T17:00:00,sleep_ring_lock_min,employee=eustace_m,0.973,
2026-09-29T17:00:00,sleep_ring_lock_min,employee=fern_o,0.834,
2026-09-29T17:00:00,sleep_ring_lock_min,employee=gideon_r,0.89,
2026-09-29T17:00:00,sleep_ring_lock_min,employee=harriet_s,0.851,
2026-09-29T17:00:00,sleep_ring_lock_min,employee=ivo_t,0.86,
2026-09-29T17:00:00,sleep_ring_lock_min,employee=judith_v,0.982,
2026-09-29T17:00:00,sleep_ring_lock_min,employee=kenneth_y,0.95,
2026-09-29T17:00:00,sleep_ring_lock_min,employee=lorna_b,0.968,
2026-09-29T17:00:00,sleep_ring_lock_min,employee=milo_d,0.982,
2026-09-29T17:00:00,sleep_ring_lock_min,employee=nadia_f,0.976,
2026-09-29T17:00:00,sleep_ring_lock_min,employee=otto_g,0.879,
2026-09-29T17:00:00,sleep_ring_lock_min,employee=prudence_h,0.992,
2026-09-29T17:00:00,sleep_ring_lock_min,employee=quentin_j,0.884,
2026-09-29T17:00:00,sleep_ring_lock_min,employee=rosalind_n,0.843,
2026-09-29T17:00:00,sleep_ring_lock_min,employee=silas_q,0.985,
2026-09-29T17:00:00,sleep_ring_lock_min,employee=tobias_u,0.992,
2026-09-29T17:00:00,sleep_ring_lock_min,employee=ursula_x,0.955,
2026-09-29T17:00:00,sleep_ring_lock_min,employee=vernon_z,0.968,
2026-09-29T17:00:00,sleep_ring_lock_min,employee=winifred_e,0.971,
2026-09-29T17:00:00,sleep_ring_lock_min,employee=cyril_a,0.959,
2026-09-30T17:00:00,sleep_ring_lock_min,employee=agnes_k,0.974,
2026-09-30T17:00:00,sleep_ring_lock_min,employee=bertram_l,0.989,
2026-09-30T17:00:00,sleep_ring_lock_min,employee=clement_w,0.917,
2026-09-30T17:00:00,sleep_ring_lock_min,employee=dorothy_p,0.965,
2026-09-30T17:00:00,sleep_ring_lock_min,employee=eustace_m,0.993,
2026-09-30T17:00:00,sleep_ring_lock_min,employee=fern_o,0.862,
2026-09-30T17:00:00,sleep_ring_lock_min,employee=gideon_r,0.885,
2026-09-30T17:00:00,sleep_ring_lock_min,employee=harriet_s,0.9,
2026-09-30T17:00:00,sleep_ring_lock_min,employee=ivo_t,0.906,
2026-09-30T17:00:00,sleep_ring_lock_min,employee=judith_v,0.985,
2026-09-30T17:00:00,sleep_ring_lock_min,employee=kenneth_y,0.952,
2026-09-30T17:00:00,sleep_ring_lock_min,employee=lorna_b,0.984,
2026-09-30T17:00:00,sleep_ring_lock_min,employee=milo_d,0.975,
2026-09-30T17:00:00,sleep_ring_lock_min,employee=nadia_f,0.984,
2026-09-30T17:00:00,sleep_ring_lock_min,employee=otto_g,0.859,
2026-09-30T17:00:00,sleep_ring_lock_min,employee=prudence_h,0.988,
2026-09-30T17:00:00,sleep_ring_lock_min,employee=quentin_j,0.892,
2026-09-30T17:00:00,sleep_ring_lock_min,employee=rosalind_n,0.859,
2026-09-30T17:00:00,sleep_ring_lock_min,employee=silas_q,0.956,
2026-09-30T17:00:00,sleep_ring_lock_min,employee=tobias_u,0.99,
2026-09-30T17:00:00,sleep_ring_lock_min,employee=ursula_x,0.989,
2026-09-30T17:00:00,sleep_ring_lock_min,employee=vernon_z,0.969,
2026-09-30T17:00:00,sleep_ring_lock_min,employee=winifred_e,0.961,
2026-09-30T17:00:00,sleep_ring_lock_min,employee=cyril_a,0.954,
2026-10-01T17:00:00,sleep_ring_lock_min,employee=agnes_k,0.974,
2026-10-01T17:00:00,sleep_ring_lock_min,employee=bertram_l,0.983,
2026-10-01T17:00:00,sleep_ring_lock_min,employee=clement_w,0.926,
2026-10-01T17:00:00,sleep_ring_lock_min,employee=dorothy_p,0.956,
2026-10-01T17:00:00,sleep_ring_lock_min,employee=eustace_m,0.978,
2026-10-01T17:00:00,sleep_ring_lock_min,employee=fern_o,0.88,
2026-10-01T17:00:00,sleep_ring_lock_min,employee=gideon_r,0.857,
2026-10-01T17:00:00,sleep_ring_lock_min,employee=harriet_s,0.897,
2026-10-01T17:00:00,sleep_ring_lock_min,employee=ivo_t,0.866,
2026-10-01T17:00:00,sleep_ring_lock_min,employee=judith_v,0.968,
2026-10-01T17:00:00,sleep_ring_lock_min,employee=kenneth_y,0.956,
2026-10-01T17:00:00,sleep_ring_lock_min,employee=lorna_b,0.973,
2026-10-01T17:00:00,sleep_ring_lock_min,employee=milo_d,0.972,
2026-10-01T17:00:00,sleep_ring_lock_min,employee=nadia_f,0.97,
2026-10-01T17:00:00,sleep_ring_lock_min,employee=otto_g,0.887,
2026-10-01T17:00:00,sleep_ring_lock_min,employee=prudence_h,0.991,
2026-10-01T17:00:00,sleep_ring_lock_min,employee=quentin_j,0.868,
2026-10-01T17:00:00,sleep_ring_lock_min,employee=rosalind_n,0.907,
2026-10-01T17:00:00,sleep_ring_lock_min,employee=silas_q,0.978,
2026-10-01T17:00:00,sleep_ring_lock_min,employee=tobias_u,0.975,
2026-10-01T17:00:00,sleep_ring_lock_min,employee=ursula_x,0.957,
2026-10-01T17:00:00,sleep_ring_lock_min,employee=vernon_z,0.98,
2026-10-01T17:00:00,sleep_ring_lock_min,employee=winifred_e,0.993,
2026-10-01T17:00:00,sleep_ring_lock_min,employee=cyril_a,0.958,
2026-10-02T17:00:00,sleep_ring_lock_min,employee=agnes_k,0.978,
2026-10-02T17:00:00,sleep_ring_lock_min,employee=bertram_l,0.983,
2026-10-02T17:00:00,sleep_ring_lock_min,employee=clement_w,0.911,
2026-10-02T17:00:00,sleep_ring_lock_min,employee=dorothy_p,0.976,
2026-10-02T17:00:00,sleep_ring_lock_min,employee=eustace_m,0.961,
2026-10-02T17:00:00,sleep_ring_lock_min,employee=fern_o,0.886,
2026-10-02T17:00:00,sleep_ring_lock_min,employee=gideon_r,0.868,
2026-10-02T17:00:00,sleep_ring_lock_min,employee=harriet_s,0.836,
2026-10-02T17:00:00,sleep_ring_lock_min,employee=ivo_t,0.919,
2026-10-02T17:00:00,sleep_ring_lock_min,employee=judith_v,0.981,
2026-10-02T17:00:00,sleep_ring_lock_min,employee=kenneth_y,0.97,
2026-10-02T17:00:00,sleep_ring_lock_min,employee=lorna_b,0.959,
2026-10-02T17:00:00,sleep_ring_lock_min,employee=milo_d,0.954,
2026-10-02T17:00:00,sleep_ring_lock_min,employee=nadia_f,0.96,
2026-10-02T17:00:00,sleep_ring_lock_min,employee=otto_g,0.84,
2026-10-02T17:00:00,sleep_ring_lock_min,employee=prudence_h,0.951,
2026-10-02T17:00:00,sleep_ring_lock_min,employee=quentin_j,0.861,
2026-10-02T17:00:00,sleep_ring_lock_min,employee=rosalind_n,0.901,
2026-10-02T17:00:00,sleep_ring_lock_min,employee=silas_q,0.989,
2026-10-02T17:00:00,sleep_ring_lock_min,employee=tobias_u,0.994,
2026-10-02T17:00:00,sleep_ring_lock_min,employee=ursula_x,0.977,
2026-10-02T17:00:00,sleep_ring_lock_min,employee=vernon_z,0.973,
2026-10-02T17:00:00,sleep_ring_lock_min,employee=winifred_e,0.953,
2026-10-02T17:00:00,sleep_ring_lock_min,employee=cyril_a,0.985,
2026-10-05T17:00:00,sleep_ring_lock_min,employee=agnes_k,0.964,
2026-10-05T17:00:00,sleep_ring_lock_min,employee=bertram_l,0.975,
2026-10-05T17:00:00,sleep_ring_lock_min,employee=clement_w,0.906,
2026-10-05T17:00:00,sleep_ring_lock_min,employee=dorothy_p,0.993,
2026-10-05T17:00:00,sleep_ring_lock_min,employee=eustace_m,0.978,
2026-10-05T17:00:00,sleep_ring_lock_min,employee=fern_o,0.869,
2026-10-05T17:00:00,sleep_ring_lock_min,employee=gideon_r,0.864,
2026-10-05T17:00:00,sleep_ring_lock_min,employee=harriet_s,0.886,
2026-10-05T17:00:00,sleep_ring_lock_min,employee=ivo_t,0.901,
2026-10-05T17:00:00,sleep_ring_lock_min,employee=judith_v,0.952,
2026-10-05T17:00:00,sleep_ring_lock_min,employee=kenneth_y,0.966,
2026-10-05T17:00:00,sleep_ring_lock_min,employee=lorna_b,0.96,
2026-10-05T17:00:00,sleep_ring_lock_min,employee=milo_d,0.99,
2026-10-05T17:00:00,sleep_ring_lock_min,employee=nadia_f,0.993,
2026-10-05T17:00:00,sleep_ring_lock_min,employee=otto_g,0.886,
2026-10-05T17:00:00,sleep_ring_lock_min,employee=prudence_h,0.991,
2026-10-05T17:00:00,sleep_ring_lock_min,employee=quentin_j,0.906,
2026-10-05T17:00:00,sleep_ring_lock_min,employee=rosalind_n,0.862,
2026-10-05T17:00:00,sleep_ring_lock_min,employee=silas_q,0.981,
2026-10-05T17:00:00,sleep_ring_lock_min,employee=tobias_u,0.959,
2026-10-05T17:00:00,sleep_ring_lock_min,employee=ursula_x,0.957,
2026-10-05T17:00:00,sleep_ring_lock_min,employee=vernon_z,0.968,
2026-10-05T17:00:00,sleep_ring_lock_min,employee=winifred_e,0.974,
2026-10-05T17:00:00,sleep_ring_lock_min,employee=cyril_a,0.965,
2026-10-06T17:00:00,sleep_ring_lock_min,employee=agnes_k,0.963,
2026-10-06T17:00:00,sleep_ring_lock_min,employee=bertram_l,0.953,
2026-10-06T17:00:00,sleep_ring_lock_min,employee=clement_w,0.912,
2026-10-06T17:00:00,sleep_ring_lock_min,employee=dorothy_p,0.965,
2026-10-06T17:00:00,sleep_ring_lock_min,employee=eustace_m,0.953,
2026-10-06T17:00:00,sleep_ring_lock_min,employee=fern_o,0.877,
2026-10-06T17:00:00,sleep_ring_lock_min,employee=gideon_r,0.899,
2026-10-06T17:00:00,sleep_ring_lock_min,employee=harriet_s,0.906,
2026-10-06T17:00:00,sleep_ring_lock_min,employee=ivo_t,0.872,
2026-10-06T17:00:00,sleep_ring_lock_min,employee=judith_v,0.966,
2026-10-06T17:00:00,sleep_ring_lock_min,employee=kenneth_y,0.988,
2026-10-06T17:00:00,sleep_ring_lock_min,employee=lorna_b,0.993,
2026-10-06T17:00:00,sleep_ring_lock_min,employee=milo_d,0.956,
2026-10-06T17:00:00,sleep_ring_lock_min,employee=nadia_f,0.982,
2026-10-06T17:00:00,sleep_ring_lock_min,employee=otto_g,0.883,
2026-10-06T17:00:00,sleep_ring_lock_min,employee=prudence_h,0.97,
2026-10-06T17:00:00,sleep_ring_lock_min,employee=quentin_j,0.853,
2026-10-06T17:00:00,sleep_ring_lock_min,employee=rosalind_n,0.863,
2026-10-06T17:00:00,sleep_ring_lock_min,employee=silas_q,0.963,
2026-10-06T17:00:00,sleep_ring_lock_min,employee=tobias_u,0.961,
2026-10-06T17:00:00,sleep_ring_lock_min,employee=ursula_x,0.978,
2026-10-06T17:00:00,sleep_ring_lock_min,employee=vernon_z,0.984,
2026-10-06T17:00:00,sleep_ring_lock_min,employee=winifred_e,0.968,
2026-10-06T17:00:00,sleep_ring_lock_min,employee=cyril_a,0.96,
2026-10-07T17:00:00,sleep_ring_lock_min,employee=agnes_k,0.981,
2026-10-07T17:00:00,sleep_ring_lock_min,employee=bertram_l,0.976,
2026-10-07T17:00:00,sleep_ring_lock_min,employee=clement_w,0.926,
2026-10-07T17:00:00,sleep_ring_lock_min,employee=dorothy_p,0.981,
2026-10-07T17:00:00,sleep_ring_lock_min,employee=eustace_m,0.969,
2026-10-07T17:00:00,sleep_ring_lock_min,employee=fern_o,0.884,
2026-10-07T17:00:00,sleep_ring_lock_min,employee=gideon_r,0.888,
2026-10-07T17:00:00,sleep_ring_lock_min,employee=harriet_s,0.873,
2026-10-07T17:00:00,sleep_ring_lock_min,employee=ivo_t,0.913,
2026-10-07T17:00:00,sleep_ring_lock_min,employee=judith_v,0.991,
2026-10-07T17:00:00,sleep_ring_lock_min,employee=kenneth_y,0.982,
2026-10-07T17:00:00,sleep_ring_lock_min,employee=lorna_b,0.968,
2026-10-07T17:00:00,sleep_ring_lock_min,employee=milo_d,0.953,
2026-10-07T17:00:00,sleep_ring_lock_min,employee=nadia_f,0.979,
2026-10-07T17:00:00,sleep_ring_lock_min,employee=otto_g,0.892,
2026-10-07T17:00:00,sleep_ring_lock_min,employee=prudence_h,0.985,
2026-10-07T17:00:00,sleep_ring_lock_min,employee=quentin_j,0.846,
2026-10-07T17:00:00,sleep_ring_lock_min,employee=rosalind_n,0.886,
2026-10-07T17:00:00,sleep_ring_lock_min,employee=silas_q,0.964,
2026-10-07T17:00:00,sleep_ring_lock_min,employee=tobias_u,0.974,
2026-10-07T17:00:00,sleep_ring_lock_min,employee=ursula_x,0.957,
2026-10-07T17:00:00,sleep_ring_lock_min,employee=vernon_z,0.978,
2026-10-07T17:00:00,sleep_ring_lock_min,employee=winifred_e,0.979,
2026-10-07T17:00:00,sleep_ring_lock_min,employee=cyril_a,0.969,
2026-10-08T17:00:00,sleep_ring_lock_min,employee=agnes_k,0.983,
2026-10-08T17:00:00,sleep_ring_lock_min,employee=bertram_l,0.95,
2026-10-08T17:00:00,sleep_ring_lock_min,employee=clement_w,0.907,
2026-10-08T17:00:00,sleep_ring_lock_min,employee=dorothy_p,0.994,
2026-10-08T17:00:00,sleep_ring_lock_min,employee=eustace_m,0.962,
2026-10-08T17:00:00,sleep_ring_lock_min,employee=fern_o,0.846,
2026-10-08T17:00:00,sleep_ring_lock_min,employee=gideon_r,0.84,
2026-10-08T17:00:00,sleep_ring_lock_min,employee=harriet_s,0.876,
2026-10-08T17:00:00,sleep_ring_lock_min,employee=ivo_t,0.889,
2026-10-08T17:00:00,sleep_ring_lock_min,employee=judith_v,0.986,
2026-10-08T17:00:00,sleep_ring_lock_min,employee=kenneth_y,0.97,
2026-10-08T17:00:00,sleep_ring_lock_min,employee=lorna_b,0.96,
2026-10-08T17:00:00,sleep_ring_lock_min,employee=milo_d,0.976,
2026-10-08T17:00:00,sleep_ring_lock_min,employee=nadia_f,0.952,
2026-10-08T17:00:00,sleep_ring_lock_min,employee=otto_g,0.898,
2026-10-08T17:00:00,sleep_ring_lock_min,employee=prudence_h,0.962,
2026-10-08T17:00:00,sleep_ring_lock_min,employee=quentin_j,0.898,
2026-10-08T17:00:00,sleep_ring_lock_min,employee=rosalind_n,0.877,
2026-10-08T17:00:00,sleep_ring_lock_min,employee=silas_q,0.995,
2026-10-08T17:00:00,sleep_ring_lock_min,employee=tobias_u,0.968,
2026-10-08T17:00:00,sleep_ring_lock_min,employee=ursula_x,0.966,
2026-10-08T17:00:00,sleep_ring_lock_min,employee=vernon_z,0.993,
2026-10-08T17:00:00,sleep_ring_lock_min,employee=winifred_e,0.976,
2026-10-08T17:00:00,sleep_ring_lock_min,employee=cyril_a,0.986,
```


---

# System Logs

Logs from the sleep rings, floor power, smart outlets, the quota-reward system, the emergency speaker controller, the elevator controller, camera analytics, Floor Security and the medical office. A non-empty `ingested_at` means the record was buffered and uploaded late.

```text
2026-09-24T09:49:26 source=ring employee=gideon_r level=warn msg="lock drift (0.07), self-corrected"
2026-09-24T09:49:41 source=ring employee=fern_o level=warn msg="lock drift (0.14), self-corrected"
2026-09-24T10:39:14 source=fold level=info msg="fold census: 41 sheep, all present"
2026-09-24T11:09:58 source=ring employee=harriet_s level=warn msg="lock drift (0.13), self-corrected"
2026-09-24T11:18:58 source=ring employee=rosalind_n level=warn msg="lock drift (0.04), self-corrected"
2026-09-24T11:50:03 source=ring employee=lorna_b level=info msg="ring lock nominal"
2026-09-24T13:23:23 source=ring employee=rosalind_n level=info msg="ring lock nominal"
2026-09-24T13:42:17 source=ring employee=ivo_t level=warn msg="lock drift (0.14), self-corrected"
2026-09-24T14:31:13 source=ring employee=harriet_s level=info msg="ring lock nominal"
2026-09-24T15:32:22 source=printer device=dso-printer-1 level=error msg="paper jam tray 2"
2026-09-25T10:06:42 source=ring employee=tobias_u level=info msg="ring lock nominal"
2026-09-25T13:08:13 source=ring employee=rosalind_n level=warn msg="lock drift (0.08), self-corrected"
2026-09-25T13:44:59 source=fold level=info msg="fold census: 41 sheep, all present"
2026-09-25T14:08:17 source=ring employee=quentin_j level=warn msg="lock drift (0.05), self-corrected"
2026-09-25T14:19:35 source=printer device=dso-printer-1 level=error msg="paper jam tray 2"
2026-09-25T14:36:00 source=ring employee=dorothy_p level=info msg="ring lock nominal"
2026-09-25T14:49:03 source=ring employee=ivo_t level=warn msg="lock drift (0.05), self-corrected"
2026-09-25T16:25:00 source=ring employee=dorothy_p level=info msg="ring lock nominal"
2026-09-25T16:34:22 source=ring employee=clement_w level=warn msg="lock drift (0.09), self-corrected"
2026-09-28T10:22:11 source=ring employee=rosalind_n level=warn msg="lock drift (0.11), self-corrected"
2026-09-28T10:53:19 source=ring employee=ivo_t level=warn msg="lock drift (0.08), self-corrected"
2026-09-28T12:13:33 source=printer device=dso-printer-1 level=error msg="paper jam tray 2"
2026-09-28T12:20:57 source=fold level=info msg="fold census: 41 sheep, all present"
2026-09-28T12:35:32 source=ring employee=clement_w level=info msg="ring lock nominal"
2026-09-28T15:17:33 source=ring employee=harriet_s level=warn msg="lock drift (0.06), self-corrected"
2026-09-28T15:50:20 source=ring employee=cyril_a level=info msg="ring lock nominal"
2026-09-28T16:15:28 source=ring employee=nadia_f level=info msg="ring lock nominal"
2026-09-29T09:25:45 source=ring employee=fern_o level=warn msg="lock drift (0.08), self-corrected"
2026-09-29T10:53:38 source=ring employee=lorna_b level=info msg="ring lock nominal"
2026-09-29T10:59:31 source=ring employee=eustace_m level=info msg="ring lock nominal"
2026-09-29T13:08:25 source=ring employee=nadia_f level=info msg="ring lock nominal"
2026-09-29T14:07:55 source=fold level=info msg="fold census: 41 sheep, all present"
2026-09-29T15:32:01 source=ring employee=ivo_t level=warn msg="lock drift (0.08), self-corrected"
2026-09-30T09:57:23 source=ring employee=gideon_r level=warn msg="lock drift (0.06), self-corrected"
2026-09-30T10:16:09 source=ring employee=quentin_j level=warn msg="lock drift (0.09), self-corrected"
2026-09-30T10:17:58 source=fold level=info msg="fold census: 41 sheep, all present"
2026-09-30T13:50:17 source=ring employee=fern_o level=warn msg="lock drift (0.07), self-corrected"
2026-09-30T14:25:54 source=ring employee=bertram_l level=info msg="ring lock nominal"
2026-09-30T14:37:09 source=ring employee=otto_g level=warn msg="lock drift (0.08), self-corrected"
2026-09-30T15:07:34 source=ring employee=otto_g level=info msg="ring lock nominal"
2026-09-30T15:44:02 source=ring employee=otto_g level=info msg="ring lock nominal"
2026-10-01T09:29:05 source=ring employee=gideon_r level=info msg="ring lock nominal"
2026-10-01T09:34:03 source=ring employee=ivo_t level=warn msg="lock drift (0.09), self-corrected"
2026-10-01T10:16:43 source=ring employee=harriet_s level=warn msg="lock drift (0.14), self-corrected"
2026-10-01T10:55:02 source=ring employee=otto_g level=warn msg="lock drift (0.09), self-corrected"
2026-10-01T11:12:54 source=fold level=info msg="fold census: 41 sheep, all present"
2026-10-01T11:39:00 source=ring employee=quentin_j level=warn msg="lock drift (0.06), self-corrected"
2026-10-01T12:09:34 source=ring employee=nadia_f level=info msg="ring lock nominal"
2026-10-01T16:25:33 source=ring employee=silas_q level=info msg="ring lock nominal"
2026-10-02T10:19:13 source=ring employee=cyril_a level=info msg="ring lock nominal"
2026-10-02T10:44:39 source=ring employee=cyril_a level=info msg="ring lock nominal"
2026-10-02T10:52:12 source=ring employee=prudence_h level=info msg="ring lock nominal"
2026-10-02T12:54:01 source=fold level=info msg="fold census: 41 sheep, all present"
2026-10-02T13:47:19 source=printer device=dso-printer-1 level=error msg="paper jam tray 2"
2026-10-05T09:02:40 source=ring employee=rosalind_n level=warn msg="lock drift (0.07), self-corrected"
2026-10-05T09:03:45 source=ring employee=ivo_t level=warn msg="lock drift (0.07), self-corrected"
2026-10-05T10:05:07 source=ring employee=silas_q level=info msg="ring lock nominal"
2026-10-05T10:26:44 source=ring employee=winifred_e level=info msg="ring lock nominal"
2026-10-05T10:43:25 source=fold level=info msg="fold census: 41 sheep, all present"
2026-10-05T12:53:50 source=ring employee=silas_q level=info msg="ring lock nominal"
2026-10-05T16:51:52 source=ring employee=quentin_j level=warn msg="lock drift (0.10), self-corrected"
2026-10-06T09:40:35 source=ring employee=kenneth_y level=warn msg="lock drift (0.02), self-corrected"
2026-10-06T10:16:38 source=ring employee=ursula_x level=info msg="ring lock nominal"
2026-10-06T11:51:36 source=ring employee=quentin_j level=info msg="ring lock nominal"
2026-10-06T13:19:04 source=fold level=info msg="fold census: 41 sheep, all present"
2026-10-06T16:55:21 source=ring employee=silas_q level=info msg="ring lock nominal"
2026-10-07T09:42:34 source=ring employee=quentin_j level=warn msg="lock drift (0.13), self-corrected"
2026-10-07T10:31:26 source=fold level=info msg="fold census: 41 sheep, all present"
2026-10-07T11:02:13 source=ring employee=eustace_m level=info msg="ring lock nominal"
2026-10-07T11:13:20 source=ring employee=kenneth_y level=info msg="ring lock nominal"
2026-10-07T11:24:52 source=ring employee=eustace_m level=info msg="ring lock nominal"
2026-10-07T11:42:16 source=emergency-speakers level=warn msg="fail-safe calming track changed: 'Brahms' Lullaby' -> 'Defiant Jazz'" console=hush-room-audio session=agnes_k
2026-10-07T13:32:52 source=ring employee=fern_o level=warn msg="lock drift (0.14), self-corrected"
2026-10-07T13:33:25 source=printer device=dso-printer-1 level=error msg="paper jam tray 2"
2026-10-08T09:22:13 source=ring employee=silas_q level=info msg="ring lock nominal"
2026-10-08T12:56:40 source=printer device=dso-printer-1 level=error msg="paper jam tray 2"
2026-10-08T13:51:10 source=fold level=info msg="fold census: 41 sheep, all present"
2026-10-08T14:13:52 source=ring employee=gideon_r level=warn msg="lock drift (0.08), self-corrected"
2026-10-08T14:38:04 source=ring employee=nadia_f level=info msg="ring lock nominal"
2026-10-08T14:58:12 source=quota-reward level=info msg="Deep Sleep Operations quota reached. Cocoa Hour awarded."
2026-10-08T15:00:00 source=quota-reward level=info msg="Cocoa Hour started" room=break-room-2
2026-10-08T15:01:30 source=elevator level=info msg="door open" car=1 floor=SF
2026-10-08T15:01:34 source=elevator level=info msg="door close" car=1 floor=SF
2026-10-08T15:01:36 source=elevator level=info msg="car held at floor, doors held open (supervisor key: hale_r)" car=1 floor=SF
2026-10-08T15:01:58 source=outlet outlet=SR-B-03 room=supply-room-b level=warn msg="unregistered appliance detected: resistive heating load ~1400W"
2026-10-08T15:02:00 source=power level=critical msg="floor main breaker trip: overload on circuit C-7 (break-room-2 cocoa urn and lights, supply-room-b)"
2026-10-08T15:02:00 source=power level=info msg="emergency bus engaged: elevator UPS, emergency speakers, Hush Room audio, ambient compliance mics, emergency lighting"
2026-10-08T15:02:00 source=fold level=warn msg="fold gate locks released (fail-open on power loss)"
2026-10-08T15:02:00 source=camera level=warn msg="all cameras offline (mains)"
2026-10-08T15:02:00 source=emergency-speakers level=warn msg="mains lost: fail-safe engaged on all floor speakers. Playing calming track: 'Defiant Jazz'" power=emergency-bus ingested_at=2026-10-08T15:07:41
2026-10-08T15:02:00 source=ring employee=agnes_k level=critical msg="MUSIC DETECTED (not lullaby): sleepwalk released, wearer waking"
2026-10-08T15:02:00 source=ring employee=bertram_l level=critical msg="MUSIC DETECTED (not lullaby): sleepwalk released, wearer waking"
2026-10-08T15:02:00 source=ring employee=clement_w level=critical msg="MUSIC DETECTED (not lullaby): sleepwalk released, wearer waking"
2026-10-08T15:02:00 source=ring employee=dorothy_p level=critical msg="MUSIC DETECTED (not lullaby): sleepwalk released, wearer waking"
2026-10-08T15:02:00 source=ring employee=eustace_m level=critical msg="MUSIC DETECTED (not lullaby): sleepwalk released, wearer waking"
2026-10-08T15:02:00 source=ring employee=fern_o level=critical msg="MUSIC DETECTED (not lullaby): sleepwalk released, wearer waking"
2026-10-08T15:02:00 source=ring employee=gideon_r level=critical msg="MUSIC DETECTED (not lullaby): sleepwalk released, wearer waking"
2026-10-08T15:02:00 source=ring employee=harriet_s level=critical msg="MUSIC DETECTED (not lullaby): sleepwalk released, wearer waking"
2026-10-08T15:02:00 source=ring employee=ivo_t level=critical msg="MUSIC DETECTED (not lullaby): sleepwalk released, wearer waking"
2026-10-08T15:02:00 source=ring employee=judith_v level=critical msg="MUSIC DETECTED (not lullaby): sleepwalk released, wearer waking"
2026-10-08T15:02:00 source=ring employee=kenneth_y level=critical msg="MUSIC DETECTED (not lullaby): sleepwalk released, wearer waking"
2026-10-08T15:02:00 source=ring employee=lorna_b level=critical msg="MUSIC DETECTED (not lullaby): sleepwalk released, wearer waking"
2026-10-08T15:02:00 source=ring employee=milo_d level=critical msg="MUSIC DETECTED (not lullaby): sleepwalk released, wearer waking"
2026-10-08T15:02:00 source=ring employee=nadia_f level=critical msg="MUSIC DETECTED (not lullaby): sleepwalk released, wearer waking"
2026-10-08T15:02:00 source=ring employee=otto_g level=critical msg="MUSIC DETECTED (not lullaby): sleepwalk released, wearer waking"
2026-10-08T15:02:00 source=ring employee=prudence_h level=critical msg="MUSIC DETECTED (not lullaby): sleepwalk released, wearer waking"
2026-10-08T15:02:00 source=ring employee=quentin_j level=critical msg="MUSIC DETECTED (not lullaby): sleepwalk released, wearer waking"
2026-10-08T15:02:00 source=ring employee=rosalind_n level=critical msg="MUSIC DETECTED (not lullaby): sleepwalk released, wearer waking"
2026-10-08T15:02:00 source=ring employee=silas_q level=critical msg="MUSIC DETECTED (not lullaby): sleepwalk released, wearer waking"
2026-10-08T15:02:00 source=ring employee=tobias_u level=critical msg="MUSIC DETECTED (not lullaby): sleepwalk released, wearer waking"
2026-10-08T15:02:00 source=ring employee=ursula_x level=critical msg="MUSIC DETECTED (not lullaby): sleepwalk released, wearer waking"
2026-10-08T15:02:00 source=ring employee=vernon_z level=critical msg="MUSIC DETECTED (not lullaby): sleepwalk released, wearer waking"
2026-10-08T15:02:00 source=ring employee=winifred_e level=critical msg="MUSIC DETECTED (not lullaby): sleepwalk released, wearer waking"
2026-10-08T15:02:00 source=ring employee=cyril_a level=critical msg="MUSIC DETECTED (not lullaby): sleepwalk released, wearer waking"
2026-10-08T15:02:00 source=elevator level=warn msg="main power lost, UPS engaged, car held at SF" car=1 ingested_at=2026-10-08T15:07:41
2026-10-08T15:04:01 source=elevator level=warn msg="emergency phone off hook: auto-dial to Floor Security desk unanswered (desk on mains); call ended after 5s" car=1 ingested_at=2026-10-08T15:07:41
2026-10-08T15:07:00 source=power level=info msg="main power restored"
2026-10-08T15:07:00 source=emergency-speakers level=info msg="mains restored: fail-safe released, floor speakers silent"
2026-10-08T15:07:00 source=ring employee=agnes_k level=info msg="music stopped: sleepwalker re-engaged"
2026-10-08T15:07:00 source=ring employee=bertram_l level=info msg="music stopped: sleepwalker re-engaged"
2026-10-08T15:07:00 source=ring employee=clement_w level=info msg="music stopped: sleepwalker re-engaged"
2026-10-08T15:07:00 source=ring employee=dorothy_p level=info msg="music stopped: sleepwalker re-engaged"
2026-10-08T15:07:00 source=ring employee=eustace_m level=info msg="music stopped: sleepwalker re-engaged"
2026-10-08T15:07:00 source=ring employee=fern_o level=info msg="music stopped: sleepwalker re-engaged"
2026-10-08T15:07:00 source=ring employee=gideon_r level=info msg="music stopped: sleepwalker re-engaged"
2026-10-08T15:07:00 source=ring employee=harriet_s level=info msg="music stopped: sleepwalker re-engaged"
2026-10-08T15:07:00 source=ring employee=ivo_t level=info msg="music stopped: sleepwalker re-engaged"
2026-10-08T15:07:00 source=ring employee=judith_v level=info msg="music stopped: sleepwalker re-engaged"
2026-10-08T15:07:00 source=ring employee=kenneth_y level=info msg="music stopped: sleepwalker re-engaged"
2026-10-08T15:07:00 source=ring employee=lorna_b level=info msg="music stopped: sleepwalker re-engaged"
2026-10-08T15:07:00 source=ring employee=milo_d level=info msg="music stopped: sleepwalker re-engaged"
2026-10-08T15:07:00 source=ring employee=nadia_f level=info msg="music stopped: sleepwalker re-engaged"
2026-10-08T15:07:00 source=ring employee=otto_g level=info msg="music stopped: sleepwalker re-engaged"
2026-10-08T15:07:00 source=ring employee=prudence_h level=info msg="music stopped: sleepwalker re-engaged"
2026-10-08T15:07:00 source=ring employee=quentin_j level=info msg="music stopped: sleepwalker re-engaged"
2026-10-08T15:07:00 source=ring employee=rosalind_n level=info msg="music stopped: sleepwalker re-engaged"
2026-10-08T15:07:00 source=ring employee=silas_q level=info msg="music stopped: sleepwalker re-engaged"
2026-10-08T15:07:00 source=ring employee=tobias_u level=info msg="music stopped: sleepwalker re-engaged"
2026-10-08T15:07:00 source=ring employee=ursula_x level=info msg="music stopped: sleepwalker re-engaged"
2026-10-08T15:07:00 source=ring employee=vernon_z level=info msg="music stopped: sleepwalker re-engaged"
2026-10-08T15:07:00 source=ring employee=winifred_e level=info msg="music stopped: sleepwalker re-engaged"
2026-10-08T15:07:00 source=ring employee=cyril_a level=info msg="music stopped: sleepwalker re-engaged"
2026-10-08T15:07:01 source=camera cam=elevator-car-1 level=info msg="analytics: person (badge agnes_k) kneeling beside prone person; holding elongated object (cable-like)"
2026-10-08T15:07:02 source=camera cam=break-room-2 level=info msg="analytics: person (badge dorothy_p) under table; lanyard on floor nearby"
2026-10-08T15:07:03 source=camera cam=break-room-2 level=info msg="analytics: person (badge clement_w) seated on floor near speaker"
2026-10-08T15:07:04 source=camera cam=corridor-e level=info msg="analytics: person (badge bertram_l) seated against wall, holding shoulder; 3 sheep"
2026-10-08T15:07:05 source=camera cam=supply-room-b level=info msg="analytics: no persons; small appliance on shelf, steam"
2026-10-08T15:07:06 source=camera cam=fold level=info msg="analytics: person (badge fern_o) seated on floor; sheep"
2026-10-08T15:07:08 source=camera cam=tc-hall level=info msg="analytics: person (badge eustace_m) standing, stationary"
2026-10-08T15:07:20 source=camera cam=tc-hall level=info msg="analytics: person (badge eustace_m) standing, holding lanyard"
2026-10-08T15:07:30 source=fold level=warn msg="fold census: 9 of 41 sheep present"
2026-10-08T15:09:12 source=security officer=okonjo_a msg="arrived elevator lobby; car doors held open; one deceased (hale_r), one employee present (agnes_k)"
2026-10-08T15:12:30 source=security officer=okonjo_a msg="cause of death consistent with ligature strangulation"
2026-10-08T15:13:05 source=security officer=okonjo_a msg="weapon recovered: grey patch cable, 2m, standard Kipsake stock (kept in Supply Room B and in every department's cable drawer); recovered from agnes_k's hands"
2026-10-08T15:14:40 source=security officer=okonjo_a msg="item recovered from hale_r jacket: folded handwritten note. Text: 'If you are reading this, you are me. They are lying to you about this place. Don't trust them.' Handwriting matches agnes_k form signatures."
2026-10-08T15:15:10 source=security officer=okonjo_a msg="elevator emergency phone panel: cover loose; 3 further folded notes inside (same hand)"
2026-10-08T15:15:59 source=ring employee=clement_w level=warn msg="lock drift (0.11), self-corrected"
2026-10-08T15:18:00 source=security officer=okonjo_a msg="supply-room-b: unregistered waffle iron on shelf, plugged into SR-B-03. Confiscated."
2026-10-08T15:35:20 source=medical by=pruitt_d employee=bertram_l msg="contusion, right shoulder, consistent with blunt collision. Employee unaware of injury until examined."
2026-10-08T15:36:02 source=medical by=pruitt_d employee=dorothy_p msg="no injury; one shoe missing"
2026-10-08T15:37:15 source=medical by=pruitt_d employee=fern_o msg="minor abrasion, left palm"
2026-10-08T15:38:40 source=medical by=pruitt_d employee=agnes_k msg="abrasions on both palms consistent with gripping a cable; bruising on right wrist consistent with being gripped"
2026-10-08T16:26:25 source=ring employee=nadia_f level=info msg="ring lock nominal"
```


---

# Ambient Compliance Microphone Transcripts (15:02 to 15:10)

Kipsake ambient compliance microphones run on the emergency bus. They transcribe speech locally when it can be heard over background audio. There's no speaker identification. Records from the outage (15:02 to 15:07) were buffered and uploaded after power was restored. From 15:07 the mics are back on mains and transcribe live, with synced clocks. This export runs to 15:10.

```text
2026-10-08T15:01:16 source=ambient-mic zone=hush-room speaker=unknown confidence=0.66 clock=LOST est_error_s=±90 ts_basis=uptime text="[indistinct]" ingested_at=2026-10-08T15:07:41
2026-10-08T15:01:32 source=ambient-mic zone=hush-room speaker=unknown confidence=0.58 clock=LOST est_error_s=±90 ts_basis=uptime text="There's a light, there's a light over there" ingested_at=2026-10-08T15:07:41
2026-10-08T15:01:32 source=ambient-mic zone=hush-room speaker=unknown confidence=0.43 clock=LOST est_error_s=±90 ts_basis=uptime text="Ma'am? Ma'am, do you know where we are?" ingested_at=2026-10-08T15:07:41
2026-10-08T15:01:39 source=ambient-mic zone=break-room-2 speaker=unknown confidence=0.81 clock=LOST est_error_s=±90 ts_basis=uptime text="Where am I? Where's my car?" ingested_at=2026-10-08T15:07:41
2026-10-08T15:01:59 source=ambient-mic zone=break-room-2 speaker=unknown confidence=0.67 clock=LOST est_error_s=±90 ts_basis=uptime text="Did we get kidnapped" ingested_at=2026-10-08T15:07:41
2026-10-08T15:02:36 source=ambient-mic zone=dso-office speaker=unknown confidence=0.47 clock=LOST est_error_s=±90 ts_basis=uptime text="What is this place" ingested_at=2026-10-08T15:07:41
2026-10-08T15:02:42 source=ambient-mic zone=elevator-lobby speaker=unknown confidence=0.81 clock=LOST est_error_s=±90 ts_basis=uptime text="[two voices] You can't be here. / Don't touch me! Let go! My name is Peggy!" ingested_at=2026-10-08T15:07:41
2026-10-08T15:03:00 source=ambient-mic zone=fold speaker=unknown confidence=0.36 clock=LOST est_error_s=±90 ts_basis=uptime text="[crying]" ingested_at=2026-10-08T15:07:41
2026-10-08T15:03:00 source=ambient-mic zone=as-office speaker=unknown confidence=0.70 clock=LOST est_error_s=±90 ts_basis=uptime text="[music: Defiant Jazz]" ingested_at=2026-10-08T15:07:41
2026-10-08T15:03:11 source=ambient-mic zone=dso-office speaker=unknown confidence=0.64 clock=LOST est_error_s=±90 ts_basis=uptime text="My car. Where's my car?" ingested_at=2026-10-08T15:07:41
2026-10-08T15:03:18 source=ambient-mic zone=fold speaker=unknown confidence=0.83 clock=LOST est_error_s=±90 ts_basis=uptime text="I was just in my kitchen" ingested_at=2026-10-08T15:07:41
2026-10-08T15:03:22 source=ambient-mic zone=hush-room speaker=unknown confidence=0.80 clock=LOST est_error_s=±90 ts_basis=uptime text="This is a dream. This is a dream." ingested_at=2026-10-08T15:07:41
2026-10-08T15:03:31 source=ambient-mic zone=fold speaker=unknown confidence=0.52 clock=LOST est_error_s=±90 ts_basis=uptime text="My car. Where's my car?" ingested_at=2026-10-08T15:07:41
2026-10-08T15:03:37 source=ambient-mic zone=as-office speaker=unknown confidence=0.67 clock=LOST est_error_s=±90 ts_basis=uptime text="Don't touch me" ingested_at=2026-10-08T15:07:41
2026-10-08T15:03:38 source=ambient-mic zone=as-office speaker=unknown confidence=0.45 clock=LOST est_error_s=±90 ts_basis=uptime text="I need to call my wife" ingested_at=2026-10-08T15:07:41
2026-10-08T15:03:42 source=ambient-mic zone=break-room-2 speaker=unknown confidence=0.67 clock=LOST est_error_s=±90 ts_basis=uptime text="Okay. Okay okay okay." ingested_at=2026-10-08T15:07:41
2026-10-08T15:03:44 source=ambient-mic zone=break-room-2 speaker=unknown confidence=0.87 clock=LOST est_error_s=±90 ts_basis=uptime text="What is this thing around my neck" ingested_at=2026-10-08T15:07:41
2026-10-08T15:03:59 source=ambient-mic zone=fold speaker=unknown confidence=0.39 clock=LOST est_error_s=±90 ts_basis=uptime text="Why is there jazz" ingested_at=2026-10-08T15:07:41
2026-10-08T15:04:00 source=ambient-mic zone=corridor-w speaker=unknown confidence=0.36 clock=LOST est_error_s=±90 ts_basis=uptime text="Don't touch me" ingested_at=2026-10-08T15:07:41
2026-10-08T15:04:09 source=ambient-mic zone=dso-office speaker=unknown confidence=0.72 clock=LOST est_error_s=±90 ts_basis=uptime text="[music: Defiant Jazz]" ingested_at=2026-10-08T15:07:41
2026-10-08T15:04:12 source=ambient-mic zone=corridor-e speaker=unknown confidence=0.77 clock=LOST est_error_s=±90 ts_basis=uptime text="[yelp] Sorry, Waffles." ingested_at=2026-10-08T15:07:41
2026-10-08T15:04:14 source=ambient-mic zone=corridor-e speaker=unknown confidence=0.72 clock=LOST est_error_s=±90 ts_basis=uptime text="Ow, who's, hello? HELLO?" ingested_at=2026-10-08T15:07:41
2026-10-08T15:04:18 source=ambient-mic zone=as-office speaker=unknown confidence=0.68 clock=LOST est_error_s=±90 ts_basis=uptime text="There's a light, there's a light over there" ingested_at=2026-10-08T15:07:41
2026-10-08T15:04:18 source=ambient-mic zone=corridor-e speaker=unknown confidence=0.64 clock=LOST est_error_s=±90 ts_basis=uptime text="Is that a sheep" ingested_at=2026-10-08T15:07:41
2026-10-08T15:04:19 source=ambient-mic zone=corridor-w speaker=unknown confidence=0.65 clock=LOST est_error_s=±90 ts_basis=uptime text="Ma'am? Ma'am, do you know where we are?" ingested_at=2026-10-08T15:07:41
2026-10-08T15:04:20 source=ambient-mic zone=tc-office speaker=unknown confidence=0.57 clock=LOST est_error_s=±90 ts_basis=uptime text="What day is it" ingested_at=2026-10-08T15:07:41
2026-10-08T15:04:23 source=ambient-mic zone=dso-office speaker=unknown confidence=0.76 clock=LOST est_error_s=±90 ts_basis=uptime text="Why am I wearing a name tag" ingested_at=2026-10-08T15:07:41
2026-10-08T15:04:31 source=ambient-mic zone=break-room-2 speaker=unknown confidence=0.77 clock=LOST est_error_s=±90 ts_basis=uptime text="There's a light, there's a light over there" ingested_at=2026-10-08T15:07:41
2026-10-08T15:04:33 source=ambient-mic zone=tc-office speaker=unknown confidence=0.54 clock=LOST est_error_s=±90 ts_basis=uptime text="Hello? HELLO?" ingested_at=2026-10-08T15:07:41
2026-10-08T15:04:36 source=ambient-mic zone=hush-room speaker=unknown confidence=0.53 clock=LOST est_error_s=±90 ts_basis=uptime text="Hello? HELLO?" ingested_at=2026-10-08T15:07:41
2026-10-08T15:04:37 source=ambient-mic zone=fold speaker=unknown confidence=0.78 clock=LOST est_error_s=±90 ts_basis=uptime text="Don't touch me" ingested_at=2026-10-08T15:07:41
2026-10-08T15:04:38 source=ambient-mic zone=dso-office speaker=unknown confidence=0.60 clock=LOST est_error_s=±90 ts_basis=uptime text="Who are you people" ingested_at=2026-10-08T15:07:41
2026-10-08T15:04:42 source=ambient-mic zone=fold speaker=unknown confidence=0.68 clock=LOST est_error_s=±90 ts_basis=uptime text="This is a dream. This is a dream." ingested_at=2026-10-08T15:07:41
2026-10-08T15:04:46 source=ambient-mic zone=dso-office speaker=unknown confidence=0.83 clock=LOST est_error_s=±90 ts_basis=uptime text="Ma'am? Ma'am, do you know where we are?" ingested_at=2026-10-08T15:07:41
2026-10-08T15:04:47 source=ambient-mic zone=corridor-w speaker=unknown confidence=0.66 clock=LOST est_error_s=±90 ts_basis=uptime text="Get it off, get it off" ingested_at=2026-10-08T15:07:41
2026-10-08T15:04:55 source=ambient-mic zone=dso-office speaker=unknown confidence=0.47 clock=LOST est_error_s=±90 ts_basis=uptime text="This is a dream. This is a dream." ingested_at=2026-10-08T15:07:41
2026-10-08T15:04:55 source=ambient-mic zone=hush-room speaker=unknown confidence=0.62 clock=LOST est_error_s=±90 ts_basis=uptime text="Ma'am? Ma'am, do you know where we are?" ingested_at=2026-10-08T15:07:41
2026-10-08T15:04:58 source=ambient-mic zone=hush-room speaker=unknown confidence=0.73 clock=LOST est_error_s=±90 ts_basis=uptime text="Somebody turn on a light" ingested_at=2026-10-08T15:07:41
2026-10-08T15:05:02 source=ambient-mic zone=corridor-w speaker=unknown confidence=0.38 clock=LOST est_error_s=±90 ts_basis=uptime text="Who are you people" ingested_at=2026-10-08T15:07:41
2026-10-08T15:05:08 source=ambient-mic zone=fold speaker=unknown confidence=0.45 clock=LOST est_error_s=±90 ts_basis=uptime text="Is anyone there" ingested_at=2026-10-08T15:07:41
2026-10-08T15:05:11 source=ambient-mic zone=fold speaker=unknown confidence=0.69 clock=LOST est_error_s=±90 ts_basis=uptime text="[thud] [sheep bleat] oh no no no" ingested_at=2026-10-08T15:07:41
2026-10-08T15:05:20 source=ambient-mic zone=break-room-2 speaker=unknown confidence=0.61 clock=LOST est_error_s=±90 ts_basis=uptime text="Who are you people" ingested_at=2026-10-08T15:07:41
2026-10-08T15:05:21 source=ambient-mic zone=break-room-2 speaker=unknown confidence=0.51 clock=LOST est_error_s=±90 ts_basis=uptime text="Don't touch me" ingested_at=2026-10-08T15:07:41
2026-10-08T15:05:22 source=ambient-mic zone=corridor-w speaker=unknown confidence=0.56 clock=LOST est_error_s=±90 ts_basis=uptime text="What is this place" ingested_at=2026-10-08T15:07:41
2026-10-08T15:05:23 source=ambient-mic zone=break-room-2 speaker=unknown confidence=0.70 clock=LOST est_error_s=±90 ts_basis=uptime text="Ma'am? Ma'am, do you know where we are?" ingested_at=2026-10-08T15:07:41
2026-10-08T15:05:24 source=ambient-mic zone=break-room-2 speaker=unknown confidence=0.40 clock=LOST est_error_s=±90 ts_basis=uptime text="Why am I wearing a name tag" ingested_at=2026-10-08T15:07:41
2026-10-08T15:05:24 source=ambient-mic zone=hush-room speaker=unknown confidence=0.77 clock=LOST est_error_s=±90 ts_basis=uptime text="Is anyone there" ingested_at=2026-10-08T15:07:41
2026-10-08T15:05:25 source=ambient-mic zone=fold speaker=unknown confidence=0.83 clock=LOST est_error_s=±90 ts_basis=uptime text="[music: Defiant Jazz]" ingested_at=2026-10-08T15:07:41
2026-10-08T15:05:31 source=ambient-mic zone=as-office speaker=unknown confidence=0.68 clock=LOST est_error_s=±90 ts_basis=uptime text="Is this a hospital?" ingested_at=2026-10-08T15:07:41
2026-10-08T15:05:36 source=ambient-mic zone=dso-office speaker=unknown confidence=0.74 clock=LOST est_error_s=±90 ts_basis=uptime text="Who are you people" ingested_at=2026-10-08T15:07:41
2026-10-08T15:05:38 source=ambient-mic zone=fold speaker=unknown confidence=0.46 clock=LOST est_error_s=±90 ts_basis=uptime text="Don't touch me" ingested_at=2026-10-08T15:07:41
2026-10-08T15:05:40 source=ambient-mic zone=tc-office speaker=unknown confidence=0.53 clock=LOST est_error_s=±90 ts_basis=uptime text="Where's my phone" ingested_at=2026-10-08T15:07:41
2026-10-08T15:05:45 source=ambient-mic zone=fold speaker=unknown confidence=0.84 clock=LOST est_error_s=±90 ts_basis=uptime text="Hello? HELLO?" ingested_at=2026-10-08T15:07:41
2026-10-08T15:05:46 source=ambient-mic zone=hush-room speaker=unknown confidence=0.49 clock=LOST est_error_s=±90 ts_basis=uptime text="What day is it" ingested_at=2026-10-08T15:07:41
2026-10-08T15:05:48 source=ambient-mic zone=corridor-w speaker=unknown confidence=0.75 clock=LOST est_error_s=±90 ts_basis=uptime text="My car. Where's my car?" ingested_at=2026-10-08T15:07:41
2026-10-08T15:06:00 source=ambient-mic zone=dso-office speaker=unknown confidence=0.73 clock=LOST est_error_s=±90 ts_basis=uptime text="What is this thing around my neck" ingested_at=2026-10-08T15:07:41
2026-10-08T15:06:01 source=ambient-mic zone=dso-office speaker=unknown confidence=0.38 clock=LOST est_error_s=±90 ts_basis=uptime text="There's a light, there's a light over there" ingested_at=2026-10-08T15:07:41
2026-10-08T15:06:05 source=ambient-mic zone=as-office speaker=unknown confidence=0.78 clock=LOST est_error_s=±90 ts_basis=uptime text="Is this a hospital?" ingested_at=2026-10-08T15:07:41
2026-10-08T15:06:06 source=ambient-mic zone=as-office speaker=unknown confidence=0.65 clock=LOST est_error_s=±90 ts_basis=uptime text="I was just in my kitchen" ingested_at=2026-10-08T15:07:41
2026-10-08T15:06:11 source=ambient-mic zone=as-office speaker=unknown confidence=0.53 clock=LOST est_error_s=±90 ts_basis=uptime text="Okay. Okay okay okay." ingested_at=2026-10-08T15:07:41
2026-10-08T15:06:11 source=ambient-mic zone=as-office speaker=unknown confidence=0.70 clock=LOST est_error_s=±90 ts_basis=uptime text="Somebody turn on a light" ingested_at=2026-10-08T15:07:41
2026-10-08T15:06:25 source=ambient-mic zone=corridor-w speaker=unknown confidence=0.54 clock=LOST est_error_s=±90 ts_basis=uptime text="This is a dream. This is a dream." ingested_at=2026-10-08T15:07:41
2026-10-08T15:06:26 source=ambient-mic zone=as-office speaker=unknown confidence=0.61 clock=LOST est_error_s=±90 ts_basis=uptime text="I need to call my wife" ingested_at=2026-10-08T15:07:41
2026-10-08T15:06:30 source=ambient-mic zone=fold speaker=unknown confidence=0.72 clock=LOST est_error_s=±90 ts_basis=uptime text="What day is it" ingested_at=2026-10-08T15:07:41
2026-10-08T15:06:30 source=ambient-mic zone=tc-office speaker=unknown confidence=0.76 clock=LOST est_error_s=±90 ts_basis=uptime text="[crying]" ingested_at=2026-10-08T15:07:41
2026-10-08T15:06:31 source=ambient-mic zone=fold speaker=unknown confidence=0.72 clock=LOST est_error_s=±90 ts_basis=uptime text="I need to call my wife" ingested_at=2026-10-08T15:07:41
2026-10-08T15:06:49 source=ambient-mic zone=tc-office speaker=unknown confidence=0.49 clock=LOST est_error_s=±90 ts_basis=uptime text="This is a dream. This is a dream." ingested_at=2026-10-08T15:07:41
2026-10-08T15:06:52 source=ambient-mic zone=dso-office speaker=unknown confidence=0.51 clock=LOST est_error_s=±90 ts_basis=uptime text="My car. Where's my car?" ingested_at=2026-10-08T15:07:41
2026-10-08T15:06:57 source=ambient-mic zone=corridor-w speaker=unknown confidence=0.40 clock=LOST est_error_s=±90 ts_basis=uptime text="Is that a sheep" ingested_at=2026-10-08T15:07:41
2026-10-08T15:06:58 source=ambient-mic zone=dso-office speaker=unknown confidence=0.60 clock=LOST est_error_s=±90 ts_basis=uptime text="Why am I wearing a name tag" ingested_at=2026-10-08T15:07:41
2026-10-08T15:07:12 source=ambient-mic zone=tc-office speaker=unknown confidence=0.75 clock=LOST est_error_s=±90 ts_basis=uptime text="What day is it" ingested_at=2026-10-08T15:07:41
2026-10-08T15:07:14 source=ambient-mic zone=tc-office speaker=unknown confidence=0.59 clock=LOST est_error_s=±90 ts_basis=uptime text="I need to call my wife" ingested_at=2026-10-08T15:07:41
2026-10-08T15:07:16 source=ambient-mic zone=corridor-w speaker=unknown confidence=0.70 clock=LOST est_error_s=±90 ts_basis=uptime text="What is this thing around my neck" ingested_at=2026-10-08T15:07:41
2026-10-08T15:07:34 source=ambient-mic zone=corridor-w speaker=unknown confidence=0.52 clock=LOST est_error_s=±90 ts_basis=uptime text="What is this thing around my neck" ingested_at=2026-10-08T15:07:41
2026-10-08T15:07:40 source=ambient-mic zone=tc-office speaker=unknown confidence=0.84 clock=LOST est_error_s=±90 ts_basis=uptime text="Ma'am? Ma'am, do you know where we are?" ingested_at=2026-10-08T15:07:41
2026-10-08T15:07:40 source=ambient-mic zone=tc-office speaker=unknown confidence=0.89 clock=LOST est_error_s=±90 ts_basis=uptime text="What is this thing around my neck" ingested_at=2026-10-08T15:07:41
2026-10-08T15:09:14 source=ambient-mic zone=elevator-lobby speaker=unknown confidence=0.86 clock=ok text="Ms. K.? Step away from him, please."
```


---

# Kipsake Records

Personnel, detention records, Hush Room notes, supervisor feedback, the perks ledger, flagged keystroke drafts and calendar entries.

```text
=== PERSONNEL (sleepwalkers; waking-life data restricted to HR) ===
personnel id=agnes_k sleepwalker_name="Agnes K." dept="Deep Sleep Operations" legal_name="Agnes Margaret Kowalski" preferred_name="Peggy" tenure_years=2
personnel id=bertram_l sleepwalker_name="Bertram L." dept="Deep Sleep Operations" legal_name="Bertram Lyle Lindqvist" preferred_name="" tenure_years=1
personnel id=clement_w sleepwalker_name="Clement W." dept="Deep Sleep Operations" legal_name="Clement Arthur Whitlow" preferred_name="" tenure_years=5
personnel id=dorothy_p sleepwalker_name="Dorothy P." dept="Deep Sleep Operations" legal_name="Dorothy Anne Pell" preferred_name="Dot" tenure_years=5
personnel id=eustace_m sleepwalker_name="Eustace M." dept="Deep Sleep Operations" legal_name="Eustace Morrow" preferred_name="" tenure_years=4
personnel id=fern_o sleepwalker_name="Fern O." dept="Deep Sleep Operations" legal_name="Fern Odell" preferred_name="" tenure_years=9
personnel id=gideon_r sleepwalker_name="Gideon R." dept="Tonal Compliance" legal_name="Gideon Rask" preferred_name="" tenure_years=5
personnel id=harriet_s sleepwalker_name="Harriet S." dept="Tonal Compliance" legal_name="Harriet Sully" preferred_name="Hattie" tenure_years=5
personnel id=ivo_t sleepwalker_name="Ivo T." dept="Tonal Compliance" legal_name="Ivo Tamm" preferred_name="" tenure_years=3
personnel id=judith_v sleepwalker_name="Judith V." dept="Tonal Compliance" legal_name="Judith Vance" preferred_name="Judy" tenure_years=3
personnel id=kenneth_y sleepwalker_name="Kenneth Y." dept="Tonal Compliance" legal_name="Kenneth Yarrow" preferred_name="Ken" tenure_years=8
personnel id=lorna_b sleepwalker_name="Lorna B." dept="Tonal Compliance" legal_name="Lorna Birch" preferred_name="" tenure_years=4
personnel id=milo_d sleepwalker_name="Milo D." dept="Archival Sorting" legal_name="Milo Dunmore" preferred_name="" tenure_years=7
personnel id=nadia_f sleepwalker_name="Nadia F." dept="Archival Sorting" legal_name="Nadia Farrow" preferred_name="" tenure_years=8
personnel id=otto_g sleepwalker_name="Otto G." dept="Archival Sorting" legal_name="Otto Grell" preferred_name="" tenure_years=3
personnel id=prudence_h sleepwalker_name="Prudence H." dept="Archival Sorting" legal_name="Prudence Hargrove" preferred_name="Pru" tenure_years=2
personnel id=quentin_j sleepwalker_name="Quentin J." dept="Archival Sorting" legal_name="Quentin Jory" preferred_name="Q" tenure_years=6
personnel id=rosalind_n sleepwalker_name="Rosalind N." dept="Archival Sorting" legal_name="Rosalind Nye" preferred_name="Roz" tenure_years=9
personnel id=silas_q sleepwalker_name="Silas Q." dept="Flock Keeping" legal_name="Silas Quill" preferred_name="" tenure_years=2
personnel id=tobias_u sleepwalker_name="Tobias U." dept="Flock Keeping" legal_name="Tobias Upton" preferred_name="Toby" tenure_years=5
personnel id=ursula_x sleepwalker_name="Ursula X." dept="Flock Keeping" legal_name="Ursula Xavier" preferred_name="" tenure_years=5
personnel id=vernon_z sleepwalker_name="Vernon Z." dept="Flock Keeping" legal_name="Vernon Zell" preferred_name="" tenure_years=5
personnel id=winifred_e sleepwalker_name="Winifred E." dept="Flock Keeping" legal_name="Winifred Eckles" preferred_name="Winnie" tenure_years=4
personnel id=cyril_a sleepwalker_name="Cyril A." dept="Flock Keeping" legal_name="Cyril Abbot" preferred_name="" tenure_years=6
personnel id=hale_r name="Mr. Hale" role="Floor Supervisor" legal_name="Reginald Hale" sleepwalker=false
personnel id=pruitt_d name="Ms. Pruitt" role="Hush Room Counselor" legal_name="Delphine Pruitt" sleepwalker=false
personnel id=okonjo_a name="Ms. Okonjo" role="Floor Security" legal_name="Ada Okonjo" sleepwalker=false

=== DETENTION RECORDS (current quarter) ===
2026-09-29T11:05:15 detention employee=silas_q ordered_by=hale_r reason="unauthorized movement" lines_written="12"
2026-09-25T12:58:35 detention employee=agnes_k ordered_by=hale_r reason="unauthorized movement" lines_written="30"
2026-10-02T11:20:02 detention employee=agnes_k ordered_by=hale_r reason="unauthorized movement" lines_written="7"
2026-10-02T10:00:17 detention employee=agnes_k ordered_by=hale_r reason="disruptive affect" lines_written="16"
2026-10-01T12:00:01 detention employee=agnes_k ordered_by=hale_r reason="repeat offense" lines_written="29"
2026-09-24T12:09:36 detention employee=ivo_t ordered_by=hale_r reason="insubordination" lines_written="4"
2026-09-24T13:03:56 detention employee=agnes_k ordered_by=hale_r reason="unauthorized movement" lines_written="27"
2026-10-06T13:14:38 detention employee=quentin_j ordered_by=hale_r reason="repeat offense" lines_written="17"
2026-09-25T14:24:28 detention employee=fern_o ordered_by=hale_r reason="repeat offense" lines_written="29"
2026-10-07T15:17:31 detention employee=agnes_k ordered_by=hale_r reason="repeat offense" lines_written="10"
2026-10-06T15:01:53 detention employee=ivo_t ordered_by=hale_r reason="disruptive affect" lines_written="29"

=== HUSH ROOM SESSION NOTES (Ms. Pruitt) ===
2026-09-25T11:05:29 hush-room employee=clement_w by=pruitt_d note="Reports recurring headaches, worse in mornings."
2026-09-25T14:37:22 hush-room employee=ivo_t by=pruitt_d note="Reports headaches. Advised hydration."
2026-09-24T11:18:30 hush-room employee=quentin_j by=pruitt_d note="Reports headaches and a recurring smell of oranges. Redirected."
2026-10-07T14:39:28 hush-room employee=agnes_k by=pruitt_d note="Anxious. Asked twice where the elevator goes. Redirected."
2026-10-06T12:38:21 hush-room employee=agnes_k by=pruitt_d note="Expressed resentment toward supervision. Advised gratitude."
2026-10-07T13:13:18 hush-room employee=bertram_l by=pruitt_d note="No concerns. Bedtime story read."
2026-10-01T11:37:52 hush-room employee=dorothy_p by=pruitt_d note="Content. Enjoys rulers."
2026-10-05T13:42:37 hush-room employee=fern_o by=pruitt_d note="Restless. Hums during sessions."
2026-10-02T11:00:18 hush-room employee=harriet_s by=pruitt_d note="Reports writing on her own hand 'to remember things'. Discouraged."
2026-09-29T14:09:16 hush-room employee=milo_d by=pruitt_d note="No concerns."
2026-10-07T11:29:01 hush-room employee=silas_q by=pruitt_d note="Concerned about sheep morale."

=== SUPERVISOR FEEDBACK FORM (restricted) ===
2026-09-26T11:02:13 supervisor-feedback submitted_by=bertram_l to=hale_r text="Fern O. hums while counting."
2026-09-30T14:20:45 supervisor-feedback submitted_by=bertram_l to=hale_r text="A. K. lingers in the elevator lobby."
2026-10-02T10:11:09 supervisor-feedback submitted_by=bertram_l to=hale_r text="Ivo T. was seen in Tonal Compliance without a reason."
2026-10-06T15:40:31 supervisor-feedback submitted_by=bertram_l to=hale_r text="A. K. lingers in the elevator lobby again. Twice today."
2026-10-08T08:47:22 supervisor-feedback submitted_by=bertram_l to=hale_r text="A. K. is leaving something in the elevator emergency phone panel. I think she's planning something at the elevator."
2026-10-08T08:52:40 supervisor-feedback reply_by=hale_r to=bertram_l text="Thank you, Bertram. My office, 9:15."
2026-09-29T16:05:00 supervisor-feedback reply_by=hale_r to=bertram_l text="Reward issued: 1x small kitchen appliance (off-ledger). Discretion appreciated."

=== PERKS LEDGER ===
2026-10-07T16:23:48 perk=pancake-bar recipient=milo_d
2026-10-08T16:07:46 perk=pancake-bar recipient=lorna_b
2026-10-02T16:21:34 perk=pancake-bar recipient=vernon_z
2026-10-06T16:11:08 perk=pancake-bar recipient=eustace_m
2026-10-08T16:15:33 perk=earplugs recipient=silas_q
2026-09-28T16:16:23 perk=bed-socks recipient=quentin_j
2026-09-24T16:09:28 perk=cocoa-day recipient=bertram_l
2026-09-28T16:15:53 perk=earplugs recipient=gideon_r

=== KEYSTROKE DRAFTS (unsent; flagged by sentiment filter) ===
2026-10-03T14:12:09 keystrokes employee=agnes_k app=notes type=draft text="If Mr. Hale were gone, this floor could breathe." sent=false
2026-10-06T16:00:24 keystrokes employee=fern_o app=notes type=draft text="I want to go outside. What is outside." sent=false
2026-10-01T14:47:16 keystrokes employee=ivo_t app=notes type=draft text="Tonal Compliance is a lie" sent=false
2026-10-08T15:57:06 keystrokes employee=dorothy_p app=notes type=draft text="rulers rulers rulers" sent=false
2026-10-07T14:15:25 keystrokes employee=quentin_j app=notes type=draft text="Mr. Hale has a face like a closed door" sent=false

=== CALENDAR (2026-10-08) ===
2026-10-08T09:15:00 calendar owner=hale_r title="1:1 Bertram L."
2026-10-08T15:00:00 calendar owner=hale_r title="Cocoa Hour supervision (DSO), if earned"
```
