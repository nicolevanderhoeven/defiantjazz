"""Self-check for the loader's time shift. Builds payloads in memory, never sends.

    python3 -m unittest discover -s loader
"""

import argparse
import contextlib
import io
import os
import sys
import unittest
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
        self.assertEqual(shift.text("2026-10-07T11:42:16 ingested_at=2026-10-08T15:07:41"),
                         "2026-10-21T11:42:16 ingested_at=2026-10-22T15:07:41")
        self.assertEqual(shift.text("2026-09-24T09:00:00"), "2026-10-08T09:00:00")  # across a month end

    def test_logs_keep_count_order_and_times_of_day(self):
        plain = load.read_logs(DATA, load.Shifter(timedelta(0)))
        moved = load.read_logs(DATA, load.Shifter(WEEKS_2))
        self.assertEqual(len(moved), len(plain))
        for (ts_a, src_a, _, body_a, trace_a), (ts_b, src_b, _, body_b, trace_b) in zip(plain, moved):
            self.assertEqual(ts_b, ts_a + WEEKS_2)
            self.assertEqual((src_b, trace_b), (src_a, trace_a))
            self.assertEqual(load.DATE_OR_ISO.sub("D", body_a), load.DATE_OR_ISO.sub("D", body_b))
        self.assertEqual({ts.weekday() for ts, *_ in moved}, {0, 1, 2, 3, 4})  # still Monday to Friday

    def test_metrics_keep_count_and_order(self):
        plain = load.read_metrics(DATA, load.Shifter(timedelta(0)))
        moved = load.read_metrics(DATA, load.Shifter(WEEKS_2))
        self.assertEqual([(ts + WEEKS_2, n, a, v) for ts, n, a, v in plain], moved)


class Traces(unittest.TestCase):
    def test_midnight_crossing_shift_keeps_one_trace_per_badge_day(self):
        plain = load.read_spans(DATA, load.Shifter(timedelta(0)))
        # the recent mode at 03:04 UTC maps 15:50 to 03:02 and moves the workday across midnight
        overnight = load.read_spans(DATA, load.Shifter(timedelta(hours=-12, minutes=-48)))
        roots = lambda spans: sum(1 for s in spans if s.name == "badge-journey")  # noqa: E731
        self.assertEqual(roots(overnight), roots(plain))
        self.assertEqual(len({s.trace_id for s in overnight}), len({s.trace_id for s in plain}))


class IncidentDate(unittest.TestCase):
    END = datetime(2026, 10, 8, 17, 0, tzinfo=timezone.utc)

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
        self.assertEqual(latest("2026-10-22T16:59:00"), date(2026, 10, 15))  # Thursday, data still running
        self.assertEqual(latest("2026-10-22T17:00:00"), date(2026, 10, 22))
        self.assertEqual(latest("2027-02-01T00:00:00").weekday(), load.THURSDAY)

    def test_modes(self):
        now = datetime(2026, 10, 21, 9, 0, tzinfo=timezone.utc)
        os.environ.pop("DJ_INCIDENT_DATE", None)
        with contextlib.redirect_stdout(io.StringIO()) as out:  # the data would end after now
            delta, day, _ = load.choose_shift(args(incident_date="2026-10-22"), now, DATA)
        self.assertIn("skipped", out.getvalue())
        self.assertEqual((delta, day), (WEEKS_2, date(2026, 10, 22)))
        self.assertEqual(load.choose_shift(args(no_shift=True), now, DATA)[:2], (timedelta(0), date(2026, 10, 8)))
        delta, day, _ = load.choose_shift(args(), now, DATA)  # recent: 15:50 -> 08:58
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


if __name__ == "__main__":
    unittest.main()
