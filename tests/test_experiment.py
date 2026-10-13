import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from timesfm_stock.data import aligned_context, completed_sessions, future_sessions
from timesfm_stock.experiment import collect, evaluate, read, write_new
from timesfm_stock.report import metrics, report

CONFIG = json.loads(Path('config.json').read_text())
CONFIG.update(symbols=['AAPL', 'MSFT'], context_sessions=32, horizon_sessions=5)
NOW = pd.Timestamp('2026-10-13T06:00:00Z')


class FakeModel:
    def __init__(self, config, revision):
        self.revision = revision

    def predict(self, matrix, horizon, modes):
        # Deliberately distinct modes to exercise report separation and shapes.
        result = {}
        for mode in modes:
            point = np.repeat(matrix[:, -1:], horizon, axis=1)
            quantiles = point[..., None] + np.arange(-4, 5)[None, None, :]
            result[mode] = {'point': point.tolist(), 'quantiles': quantiles.tolist()}
        return result


def fake_fetch(symbol, start, end):
    cal, sessions = completed_sessions('XNYS', pd.Timestamp(end, tz='UTC') + pd.Timedelta(days=2), start=start)
    sessions = sessions[sessions < pd.Timestamp(end)]
    return pd.DataFrame({'Close': np.arange(len(sessions), dtype=float) + 100,
                         'Stock Splits': 0.}, index=sessions)


class ExperimentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def collect(self, **kwargs):
        return collect(CONFIG, self.root, now=NOW, fetch=fake_fetch,
                       model_factory=FakeModel, resolve=lambda _: 'fixed-weight-sha', **kwargs)

    def test_close_delay_and_weekend_and_holiday(self):
        cal, before = completed_sessions('XNYS', pd.Timestamp('2026-10-12T20:30Z'))
        self.assertEqual(before[-1].date().isoformat(), '2026-10-09')
        _, after = completed_sessions('XNYS', pd.Timestamp('2026-10-12T21:01Z'))
        self.assertEqual(after[-1].date().isoformat(), '2026-10-12')
        # Thanksgiving and the weekend must be skipped; early close must count.
        self.assertEqual(future_sessions(cal, '2026-11-25', 2), ['2026-11-27', '2026-11-30'])
        _, early = completed_sessions('XNYS', pd.Timestamp('2026-11-27T19:01Z'))
        self.assertEqual(early[-1].date().isoformat(), '2026-11-27')

    def test_missing_session_rejected(self):
        _, sessions = completed_sessions('XNYS', NOW)
        frame = fake_fetch('AAPL', '2026-08-01', '2026-10-13')
        frame = frame.drop(sessions[-3])
        with self.assertRaises(ValueError):
            aligned_context(frame, sessions, 32)

    def test_immutable_and_idempotent(self):
        path = self.collect()
        original = path.read_bytes()
        with patch('timesfm_stock.experiment.TimesFM', side_effect=AssertionError('should not load')):
            self.collect()
        self.assertEqual(original, path.read_bytes())
        with self.assertRaises(FileExistsError):
            write_new(path, {'changed': True})
        self.assertEqual(original, path.read_bytes())
        run = read(path)
        self.assertEqual(run['origin'], '2026-10-12')
        self.assertEqual(run['target_dates'][0], '2026-10-13')
        self.assertEqual(run['weight_revision'], 'fixed-weight-sha')
        self.assertTrue(all(r['date'] <= run['origin'] for rows in run['history'].values() for r in rows))

    def test_config_changes_rejected_and_window_stops(self):
        self.collect()
        changed = copy.deepcopy(CONFIG)
        changed['horizon_sessions'] = 20
        with self.assertRaises(ValueError):
            collect(changed, self.root, now=NOW)
        result = collect(CONFIG, self.root, now=NOW + pd.Timedelta(days=31),
                         fetch=lambda *args: self.fail('expired window must not fetch'))
        self.assertIsNone(result)

    def test_pending_then_score_and_preserve_actuals(self):
        self.collect()
        evaluate(self.root, now=NOW, fetch=fake_fetch)
        self.assertFalse((self.root/'observations').exists())
        later = pd.Timestamp('2026-10-14T06:00Z')
        evaluate(self.root, now=later, fetch=fake_fetch)
        paths = sorted((self.root/'observations').rglob('*.json'))
        self.assertEqual(len(paths), 2)
        old = [p.read_bytes() for p in paths]
        evaluate(self.root, now=later, fetch=lambda *args: self.fail('all observations frozen'))
        self.assertEqual(old, [p.read_bytes() for p in paths])
        report(self.root)
        self.assertIn('univariate', (self.root/'reports/report.md').read_text())
        self.assertIn('multivariate', (self.root/'reports/report.md').read_text())

    def test_split_excluded_even_when_provider_rewrites_earlier_dates(self):
        self.collect()
        def split_fetch(symbol, start, end):
            frame = fake_fetch(symbol, start, end)
            frame.loc[pd.Timestamp('2026-10-14'), 'Stock Splits'] = 2.
            return frame
        evaluate(self.root, now=pd.Timestamp('2026-10-16T06:00Z'), fetch=split_fetch)
        outcomes = [read(p) for p in (self.root/'observations').rglob('*.json')]
        self.assertTrue(outcomes)
        self.assertTrue(all(x['status'] == 'excluded_split' for x in outcomes))

    def test_skill_and_quantile_coverage(self):
        rows = [{'actual': 110., 'prediction': 108., 'anchor': 100.,
                 'q10': 105., 'q90': 115., 'pinball_pct': 1.}]
        score = metrics(rows)
        self.assertAlmostEqual(score['mae_pct'], 2.)
        self.assertAlmostEqual(score['skill_pct'], 80.)
        self.assertEqual(score['direction_accuracy_pct'], 100.)
        self.assertEqual(score['coverage_80_pct'], 100.)
        rows[0]['actual'] = 100.
        self.assertIsNone(metrics(rows)['skill_pct'])

    def test_forecast_rejected_if_model_finishes_after_next_open(self):
        with patch('timesfm_stock.experiment.utc_now', side_effect=[NOW, pd.Timestamp('2026-10-13T14:00Z')]):
            with self.assertRaises(ValueError):
                collect(CONFIG, self.root, fetch=fake_fetch, model_factory=FakeModel,
                        resolve=lambda _: 'fixed')
        self.assertFalse((self.root/'runs').exists())


if __name__ == '__main__':
    unittest.main()
