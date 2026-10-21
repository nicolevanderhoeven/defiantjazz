"""Self-check for the loader's time shift and Cloud log checks. Builds payloads in memory, never sends.

    python3 -m unittest discover -s loader
"""

import argparse
import contextlib
import io
import json
import os
import sys
import unittest
import urllib.error
from unittest import mock
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import load  # noqa: E402

DATA = HERE.parent / "telemetry"
WEEKS_2 = timedelta(weeks=2)


def args(**kw):
    base = dict(incident_date=None, no_shift=False, incident_end=None, any_weekday=False)
    base.update(kw)
    return argparse.Namespace(**base)


class WholeWeekShift(unittest.TestCase):
    """A whole-week shift changes only the dates: same lines, same order, same weekdays."""

    def test_text_shift_keeps_every_line(self):
        shift = load.Shifter(WEEKS_2)
        for path in sorted(DATA.iterdir()):
            original = path.read_text().splitlines()
            shifted = [shift.text(line) for line in original]
            self.assertEqual(len(shifted), len(original), path.name)
            for a, b in zip(original, shifted):
                # dates are fixed-width, and nothing but the dates changes
                self.assertEqual(len(a), len(b), path.name)
                self.assertEqual(load.DATE_OR_ISO.sub("D", a), load.DATE_OR_ISO.sub("D", b), path.name)

    def test_text_shift_moves_iso_and_bare_dates(self):
        shift = load.Shifter(WEEKS_2)
        self.assertEqual(shift.text("=== CALENDAR (2026-10-08) ==="), "=== CALENDAR (2026-10-22) ===")
        self.assertEqual(shift.text("2026-10-06T23:42:16 ingested_at=2026-10-08T03:07:41"),
                         "2026-10-20T23:42:16 ingested_at=2026-10-22T03:07:41")
        self.assertEqual(shift.text("2026-09-24T09:00:00"), "2026-10-08T09:00:00")  # across a month end

    def test_logs_keep_count_order_and_times_of_day(self):
        plain = load.read_logs(DATA, load.Shifter(timedelta(0)))
        moved = load.read_logs(DATA, load.Shifter(WEEKS_2))
        self.assertEqual(len(moved), len(plain))
        for (ts_a, src_a, _, body_a, trace_a), (ts_b, src_b, _, body_b, trace_b) in zip(plain, moved):
            self.assertEqual(ts_b, ts_a + WEEKS_2)
            self.assertEqual((src_b, trace_b), (src_a, trace_a))
            self.assertEqual(load.DATE_OR_ISO.sub("D", body_a), load.DATE_OR_ISO.sub("D", body_b))
        # still the nights from Sunday evening to Friday morning
        self.assertEqual({ts.weekday() for ts, *_ in moved}, {6, 0, 1, 2, 3, 4})

    def test_metrics_keep_count_and_order(self):
        plain = load.read_metrics(DATA, load.Shifter(timedelta(0)))
        moved = load.read_metrics(DATA, load.Shifter(WEEKS_2))
        self.assertEqual([(ts + WEEKS_2, n, a, v) for ts, n, a, v in plain], moved)


class Traces(unittest.TestCase):
    def test_one_trace_per_badge_per_night_shift(self):
        plain = load.read_spans(DATA, load.Shifter(timedelta(0)))
        roots = lambda spans: [s for s in spans if s.name == "badge-journey"]  # noqa: E731
        # a night shift crosses midnight, but each badge's night is one journey
        nights = {(dict((a.key, a.value.string_value) for a in s.attributes)["badge"], s.trace_id)
                  for s in roots(plain)}
        self.assertEqual(len(nights), len(roots(plain)))
        incident = [s for s in roots(plain) if s.start_time_unix_nano < load.nanos(load.INCIDENT_AT)
                    < s.end_time_unix_nano]
        self.assertTrue(incident)
        for s in incident:  # the incident night's journeys start the evening before
            self.assertLess(s.start_time_unix_nano, load.nanos(datetime(2026, 10, 8, tzinfo=timezone.utc)))
        # the recent mode at 15:04 UTC maps 03:50 to 15:02 and moves the night shift into the day
        daytime = load.read_spans(DATA, load.Shifter(timedelta(hours=11, minutes=12)))
        self.assertEqual(len(roots(daytime)), len(roots(plain)))
        self.assertEqual(len({s.trace_id for s in daytime}), len({s.trace_id for s in plain}))


class IncidentDate(unittest.TestCase):
    END = datetime(2026, 10, 8, 5, 0, tzinfo=timezone.utc)

    def test_thursday_only_unless_any_weekday(self):
        self.assertEqual(load.incident_day("2026-10-22", None, self.END), date(2026, 10, 22))
        with self.assertRaises(SystemExit):
            load.incident_day("2026-10-21", None, self.END)
        self.assertEqual(load.incident_day("2026-10-21", None, self.END, any_weekday=True), date(2026, 10, 21))
        with self.assertRaises(SystemExit):
            load.incident_day("22/10/2026", None, self.END)

    def test_latest_is_the_last_thursday_whose_data_has_happened(self):
        def latest(now):
            return load.incident_day("latest", datetime.fromisoformat(now).replace(tzinfo=timezone.utc), self.END)
        self.assertEqual(latest("2026-10-21T10:00:00"), date(2026, 10, 15))  # Wednesday
        self.assertEqual(latest("2026-10-22T04:59:00"), date(2026, 10, 15))  # Thursday, data still running
        self.assertEqual(latest("2026-10-22T05:00:00"), date(2026, 10, 22))
        self.assertEqual(latest("2027-02-01T00:00:00").weekday(), load.THURSDAY)

    def test_modes(self):
        now = datetime(2026, 10, 21, 9, 0, tzinfo=timezone.utc)
        os.environ.pop("DJ_INCIDENT_DATE", None)
        with contextlib.redirect_stdout(io.StringIO()) as out:  # the data would end after now
            delta, day, _ = load.choose_shift(args(incident_date="2026-10-22"), now, DATA)
        self.assertIn("skipped", out.getvalue())
        self.assertEqual((delta, day), (WEEKS_2, date(2026, 10, 22)))
        self.assertEqual(load.choose_shift(args(no_shift=True), now, DATA)[:2], (timedelta(0), date(2026, 10, 8)))
        delta, day, _ = load.choose_shift(args(), now, DATA)  # recent: 03:50 -> 08:58
        self.assertEqual((delta, day), (now - timedelta(minutes=2) - load.REFERENCE, date(2026, 10, 21)))
        os.environ["DJ_INCIDENT_DATE"] = "latest"
        try:
            self.assertEqual(load.choose_shift(args(), now, DATA)[:2], (timedelta(weeks=1), date(2026, 10, 15)))
            self.assertEqual(load.choose_shift(args(no_shift=True), now, DATA)[1], date(2026, 10, 8))
        finally:
            del os.environ["DJ_INCIDENT_DATE"]

    def test_case_run_on_every_resource(self):
        load.set_case_run(date(2026, 10, 22))
        try:
            for service in ("door", "kipsake-floor-telemetry", "kipsake-badge-tracking"):
                attrs = {a.key: a.value.string_value for a in load.resource(service).attributes}
                self.assertEqual(attrs["case_run"], "2026-10-22")
        finally:
            load.set_case_run(load.INCIDENT_AT.date())


CLOUD_ENV = {"GRAFANA_OTLP_ENDPOINT": "https://otlp.example/otlp", "GRAFANA_INSTANCE_ID": "1",
             "GRAFANA_API_TOKEN": "glc_write_secret"}
LOKI_ENV = {"GRAFANA_LOKI_URL": "https://logs.example/", "GRAFANA_LOKI_USER": "2",
            "GRAFANA_LOKI_READ_TOKEN": "glc_read_secret"}
SETTINGS = ("DJ_INCIDENT_DATE", "DJ_CLOUD_LOG_HOURS", *CLOUD_ENV, *LOKI_ENV)


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def loki_answer(count):
    result = [{"metric": {}, "value": [0, str(count)]}] if count is not None else []
    return FakeResponse(json.dumps({"status": "success", "data": {"resultType": "vector", "result": result}}).encode())


class CloudLogs(unittest.TestCase):
    """Cloud Loki drops old lines after a 204, so the loader caps the window and checks what was stored."""

    def setUp(self):
        saved = {k: os.environ.pop(k) for k in SETTINGS if k in os.environ}
        self.addCleanup(os.environ.update, saved)
        self.addCleanup(lambda: [os.environ.pop(k, None) for k in SETTINGS])
        self.addCleanup(load.set_case_run, load.INCIDENT_AT.date())
        self.addCleanup(load.set_namespace, load.NAMESPACE)
        sleep = mock.patch.object(load.time, "sleep")
        self.sleeps = sleep.start()
        self.addCleanup(sleep.stop)

    def run_main(self, *argv, env=(), loki=()):
        """Run the loader against stubs: returns (log items posted, Loki query URLs, output)."""
        os.environ.update(dict(env))
        posted, queries = [], []
        answers = list(loki)

        def post(sender, signal, message):
            if signal == "logs":
                posted.extend(r for rl in message.resource_logs for sl in rl.scope_logs for r in sl.log_records)
            return True

        def urlopen(req, **kw):
            queries.append(req)
            answer = answers.pop(0) if len(answers) > 1 else answers[0]
            if isinstance(answer, Exception):
                raise answer
            return loki_answer(answer)

        with mock.patch.object(load.Sender, "post", post), mock.patch.object(load, "load_env_file"), \
                mock.patch.object(load.urllib.request, "urlopen", urlopen), \
                mock.patch.object(sys, "argv", ["load.py", "--target", "cloud", "--signals", "logs", *argv]), \
                contextlib.redirect_stdout(io.StringIO()) as out, self.assertRaises(SystemExit) as done:
            load.main()
        self.assertEqual(done.exception.code, 0)
        return posted, queries, out.getvalue()

    def age_hours(self, posted):
        now = datetime.now(timezone.utc)
        return (now - datetime.fromtimestamp(min(r.time_unix_nano for r in posted) / 1e9, timezone.utc)) / timedelta(hours=1)

    def test_window_defaults_to_three_hours(self):
        posted, queries, out = self.run_main(env=CLOUD_ENV)
        self.assertTrue(posted)
        self.assertLessEqual(self.age_hours(posted), 3.01)
        self.assertGreater(self.age_hours(posted), 2.5)
        self.assertIn("only the last 3 h are sent", out)
        self.assertEqual(queries, [])

    def test_window_setting_flag_and_env(self):
        self.assertEqual(load.cloud_log_hours(None), 3.0)
        three_h, *_ = self.run_main(env=CLOUD_ENV)
        os.environ["DJ_CLOUD_LOG_HOURS"] = "12"
        self.assertEqual(load.cloud_log_hours(None), 12.0)
        self.assertEqual(load.cloud_log_hours("1.5"), 1.5)  # the flag wins over the env
        for bad in ("three", "0", "-1"):
            with self.assertRaises(SystemExit):
                load.cloud_log_hours(bad)
        twelve_h, *_ = self.run_main()
        one_h, *_ = self.run_main("--cloud-log-hours", "1")
        self.assertLess(len(one_h), len(three_h))
        self.assertLess(len(three_h), len(twelve_h))
        self.assertLessEqual(self.age_hours(one_h), 1.01)
        self.assertGreater(self.age_hours(twelve_h), 3.01)
        self.assertLessEqual(self.age_hours(twelve_h), 12.01)

    def test_warns_when_cloud_stored_fewer_lines(self):
        posted, queries, out = self.run_main(env={**CLOUD_ENV, **LOKI_ENV}, loki=[10, 50])
        sent = len(posted)
        self.assertGreater(sent, 50)
        self.assertIn(f"sent {sent} log lines, but Grafana Cloud stored only 50", out)
        self.assertIn("--target local", out)
        self.assertIn("reload just before a demo", out)
        self.assertEqual(len(queries), 6)  # retried for ingestion delay
        self.assertEqual(self.sleeps.call_count, 5)
        url = queries[0].full_url
        self.assertTrue(url.startswith("https://logs.example/loki/api/v1/query?"), url)
        query = load.urllib.parse.parse_qs(load.urllib.parse.urlsplit(url).query)["query"][0]
        self.assertIn('service_namespace="kipsake-sleep-floor"', query)
        self.assertIn(f'case_run="{load.CASE_RUN}"', query)
        self.assertNotIn("secret", out)

    def test_stops_retrying_once_everything_is_stored(self):
        posted, queries, out = self.run_main(env={**CLOUD_ENV, **LOKI_ENV}, loki=[None, 100000])
        self.assertEqual(len(queries), 2)
        self.assertIn(f"stored all {len(posted)} lines", out)
        self.assertNotIn("WARNING", out)

    def test_check_skipped_without_loki_settings(self):
        posted, queries, out = self.run_main(env={**CLOUD_ENV, "GRAFANA_LOKI_URL": "https://logs.example"})
        self.assertTrue(posted)
        self.assertEqual(queries, [])
        self.assertIn("stored-count check skipped: set GRAFANA_LOKI_URL, GRAFANA_LOKI_USER and GRAFANA_LOKI_READ_TOKEN", out)

    def test_check_skipped_when_loki_refuses(self):
        refused = urllib.error.HTTPError("https://logs.example", 401, "Unauthorized", {}, io.BytesIO(b""))
        _, queries, out = self.run_main(env={**CLOUD_ENV, **LOKI_ENV}, loki=[refused])
        self.assertEqual(len(queries), 1)
        self.assertIn("check skipped: Loki query returned HTTP 401 (the read token needs logs:read)", out)
        self.assertNotIn("secret", out)
        _, _, out = self.run_main(env={**CLOUD_ENV, **LOKI_ENV}, loki=[urllib.error.URLError("no route")])
        self.assertIn("check skipped: Loki query failed (no route)", out)

    def test_no_check_on_dry_run_or_local(self):
        _, queries, _ = self.run_main("--dry-run", env={**CLOUD_ENV, **LOKI_ENV}, loki=[0])
        self.assertEqual(queries, [])
        os.environ.update({**CLOUD_ENV, **LOKI_ENV})
        posted, queries = [], []
        with mock.patch.object(load.Sender, "post", lambda s, sig, m: posted.append(sig) or True), \
                mock.patch.object(load.urllib.request, "urlopen", lambda *a, **k: queries.append(a)), \
                mock.patch.object(sys, "argv", ["load.py", "--target", "local", "--signals", "logs"]), \
                contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit):
            load.main()
        self.assertEqual((posted, queries), (["logs"], []))


if __name__ == "__main__":
    unittest.main()
