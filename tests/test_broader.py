import copy
import json
from pathlib import Path
import tempfile
import unittest

import pandas as pd

from timesfm_stock.experiment import collect, evaluate, preflight, read, validate_config
from timesfm_stock.report import report
from test_experiment import CONFIG, FakeModel, NOW, fake_fetch
from test_decision import POLICY, examples
from timesfm_stock.decision import assess

BROAD = json.loads(Path('config-broad.json').read_text())


class BroaderStudyTests(unittest.TestCase):
    def test_balanced_universe_and_identical_model_settings(self):
        original = json.loads(Path('config.json').read_text())
        validate_config(BROAD)
        self.assertEqual(len(BROAD['symbols']), 22)
        self.assertEqual(set(BROAD['symbols']), set(BROAD['sectors']))
        self.assertNotIn('SPY', BROAD['symbols'])
        counts = list(BROAD['sectors'].values())
        self.assertEqual(len(set(counts)), 11)
        self.assertTrue(all(counts.count(sector) == 2 for sector in set(counts)))
        for key in ['context_sessions', 'horizon_sessions', 'modes', 'checkpoint', 'collection_days']:
            self.assertEqual(BROAD[key], original[key])
        self.assertEqual(BROAD['checkpoint_revision'], '43046b85ec22d584a13f8098c2ed39c889e129c2')

    def test_bad_sector_mapping_rejected(self):
        config = copy.deepcopy(BROAD)
        del config['sectors']['AAPL']
        with self.assertRaises(ValueError):
            validate_config(config)

    def test_open_session_waits_without_fetch_or_collection_clock(self):
        with tempfile.TemporaryDirectory() as directory:
            result = collect(BROAD, directory, now=pd.Timestamp('2026-10-13T17:00Z'),
                             fetch=lambda *args: self.fail('must not fetch during open target session'))
            self.assertIsNone(result)
            self.assertFalse((Path(directory)/'experiment.json').exists())

    def test_preflight_checks_all_symbols_without_issuing_forecast(self):
        config = copy.deepcopy(BROAD)
        config['context_sessions'] = 32
        with tempfile.TemporaryDirectory() as directory:
            payload = preflight(config, directory, now=NOW, fetch=fake_fetch)
            self.assertEqual(len(payload['symbols']), 22)
            self.assertFalse((Path(directory)/'experiment.json').exists())
            self.assertFalse((Path(directory)/'runs').exists())

    def test_studies_do_not_share_storage_and_sector_report_works(self):
        config = copy.deepcopy(BROAD)
        config.update(context_sessions=32, horizon_sessions=5)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            args = dict(now=NOW, fetch=fake_fetch, model_factory=FakeModel, resolve=lambda _: 'fixed')
            original = collect(CONFIG, root/'pilot', **args)
            before = original.read_bytes()
            collect(config, root/'broad', **args)
            evaluate(root/'broad', now=pd.Timestamp('2026-10-20T06:00Z'), fetch=fake_fetch)
            report(root/'broad', POLICY)
            self.assertEqual(original.read_bytes(), before)
            sector_csv = (root/'broad/reports/sector_summary.csv').read_text()
            self.assertIn('Information Technology', sector_csv)
            self.assertIn('Real Estate', sector_csv)
            self.assertIn('Sector diagnostics', (root/'broad/reports/report.md').read_text())
            self.assertFalse((root/'pilot/observations').exists())

    def test_breadth_rule_requires_fourteen_of_twenty_two(self):
        rows, runs = examples(prediction=110.)
        # Create the same clear test outcomes for this study's 22-stock panel.
        base = [r for r in rows if r['symbol'] == 'AAPL']
        rows = [{**r, 'symbol': symbol, 'prediction': 110. if i < 13 else 100.}
                for r in base for i, symbol in enumerate(BROAD['symbols'])]
        manifest = {'config': BROAD, 'collect_until': '2026-11-12T00:00Z'}
        result = assess(rows, runs, manifest, POLICY, now=pd.Timestamp('2026-12-15T00:00Z'))
        check = result['modes']['univariate']['comparisons']['last_price']['checks']
        self.assertFalse(check['wins_on_most_symbols'])
        for row in rows:
            if row['symbol'] == BROAD['symbols'][13]:
                row['prediction'] = 110.
        result = assess(rows, runs, manifest, POLICY, now=pd.Timestamp('2026-12-15T00:00Z'))
        self.assertTrue(result['modes']['univariate']['comparisons']['last_price']['checks']['wins_on_most_symbols'])


if __name__ == '__main__':
    unittest.main()
