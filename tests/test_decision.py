import copy
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd

from timesfm_stock.decision import assess, bootstrap_skill, freeze_policy

POLICY = json.loads(Path('decision_policy.json').read_text())
SYMBOLS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'JPM', 'XOM', 'SPY']
MANIFEST = {'config': {'symbols': SYMBOLS, 'modes': ['univariate', 'multivariate'], 'horizon_sessions': 20},
            'collect_until': '2026-11-12T06:23:19Z'}
END = pd.Timestamp('2026-12-15T00:00Z')


def examples(count=20, prediction=105., actual=110., drift=100.):
    origins = [day.date().isoformat() for day in pd.bdate_range('2026-10-13', periods=count)]
    rows = [{'origin': origin, 'symbol': symbol, 'mode': mode, 'horizon': 5,
             'anchor': 100., 'actual': actual, 'prediction': prediction, 'drift_prediction': drift}
            for origin in origins for symbol in SYMBOLS for mode in MANIFEST['config']['modes']]
    return rows, origins


class DecisionTests(unittest.TestCase):
    def test_broad_clear_improvement_is_promising(self):
        rows, runs = examples()
        result = assess(rows, runs, MANIFEST, POLICY, now=END)
        self.assertEqual(result['verdict'], 'PROMISING')
        mode = result['modes']['univariate']
        self.assertEqual(mode['comparisons']['last_price']['winning_symbols'], 8)
        self.assertEqual(mode['comparisons']['last_price']['skill_pct'], 50.)
        self.assertAlmostEqual(result['interval_confidence_pct'], 98.75)

    def test_baseline_equivalence_is_no_go(self):
        rows, runs = examples(prediction=100.)
        result = assess(rows, runs, MANIFEST, POLICY, now=END)
        self.assertEqual(result['verdict'], 'NO_GO')

    def test_small_clear_gain_below_practical_threshold_is_no_go(self):
        rows, runs = examples(prediction=100.4)
        self.assertEqual(assess(rows, runs, MANIFEST, POLICY, now=END)['verdict'], 'NO_GO')

    def test_beating_last_price_but_losing_to_drift_is_no_go(self):
        rows, runs = examples(drift=109.)
        self.assertEqual(assess(rows, runs, MANIFEST, POLICY, now=END)['verdict'], 'NO_GO')

    def test_open_window_insufficient_sample_and_pending_are_inconclusive(self):
        rows, runs = examples()
        self.assertEqual(assess(rows, runs, MANIFEST, POLICY, now=pd.Timestamp('2026-10-20T00:00Z'))['verdict'], 'INCONCLUSIVE')
        self.assertEqual(assess(rows, runs, MANIFEST, POLICY, pending_primary=1, now=END)['verdict'], 'INCONCLUSIVE')
        rows, runs = examples(count=19)
        self.assertEqual(assess(rows, runs, MANIFEST, POLICY, now=END)['verdict'], 'INCONCLUSIVE')

    def test_missing_symbol_removes_entire_origin(self):
        rows, runs = examples()
        rows = [r for r in rows if not (r['origin'] == runs[0] and r['symbol'] == 'AAPL')]
        result = assess(rows, runs, MANIFEST, POLICY, now=END)
        self.assertEqual(result['verdict'], 'INCONCLUSIVE')
        self.assertEqual(result['modes']['univariate']['complete_origins'], 19)

    def test_one_stock_cannot_carry_the_success(self):
        rows, runs = examples()
        for row in rows:
            row['prediction'] = 110. if row['symbol'] == 'AAPL' else 100.
        result = assess(rows, runs, MANIFEST, POLICY, now=END)
        self.assertNotEqual(result['verdict'], 'PROMISING')
        self.assertEqual(result['modes']['univariate']['comparisons']['last_price']['winning_symbols'], 1)

    def test_bad_second_half_does_not_pass(self):
        rows, runs = examples(prediction=110.)
        for row in rows:
            if row['origin'] in runs[10:]:
                row['prediction'] = 99.
        self.assertNotEqual(assess(rows, runs, MANIFEST, POLICY, now=END)['verdict'], 'PROMISING')

    def test_zero_baseline_error_is_inconclusive(self):
        rows, runs = examples(prediction=100., actual=100.)
        self.assertEqual(assess(rows, runs, MANIFEST, POLICY, now=END)['verdict'], 'INCONCLUSIVE')

    def test_bootstrap_keeps_correlated_stocks_together(self):
        model = np.linspace(0.01, 0.09, 20)[:, None]
        base = np.full((20, 1), 0.06)
        one = bootstrap_skill(model, base, 5, 1000, 0.05, 42)
        many = bootstrap_skill(np.repeat(model, 8, axis=1), np.repeat(base, 8, axis=1), 5, 1000, 0.05, 42)
        np.testing.assert_allclose(one, many)
        self.assertEqual(one, bootstrap_skill(model, base, 5, 1000, 0.05, 42))

    def test_policy_freezes_and_rejects_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            freeze_policy(directory, POLICY)
            changed = copy.deepcopy(POLICY)
            changed['minimum_skill_pct'] = 1.
            with self.assertRaises(ValueError):
                freeze_policy(directory, changed)
            self.assertEqual(json.loads((Path(directory)/'decision_policy.json').read_text()), POLICY)

    def test_duplicate_primary_rows_rejected(self):
        rows, runs = examples()
        rows.append(dict(rows[0]))
        with self.assertRaises(ValueError):
            assess(rows, runs, MANIFEST, POLICY, now=END)


if __name__ == '__main__':
    unittest.main()
