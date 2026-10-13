"""Fixed pilot decision policy with paired block bootstrap sensitivity checks."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .experiment import read, write_new


def freeze_policy(root, requested):
    root = Path(root)
    saved = root / 'decision_policy.json'
    if saved.exists():
        policy = read(saved)
        if policy != requested:
            raise ValueError('Decision policy changed; use a separate experiment')
        return policy
    # Freeze before results are assessed, alongside the unchanged forecasting manifest.
    write_new(saved, requested)
    return requested


def skill(model_error, baseline_error):
    denominator = float(np.mean(baseline_error))
    return 100 * (1 - float(np.mean(model_error)) / denominator) if denominator > 0 else None


def bootstrap_skill(model_error, baseline_error, block_length, repetitions, alpha, seed):
    """Resample contiguous origins, keeping every symbol together (paired errors).

    Circular moving blocks preserve local time dependence and cross-symbol correlation.
    The percentile interval is approximate, especially with few independent blocks.
    """
    n = len(model_error)
    if n < block_length or float(np.mean(baseline_error)) == 0:
        return None
    rng = np.random.default_rng(seed)
    blocks = int(np.ceil(n / block_length))
    starts = rng.integers(0, n, size=(repetitions, blocks))
    indices = ((starts[..., None] + np.arange(block_length)) % n).reshape(repetitions, -1)[:, :n]
    model_means = model_error[indices].mean(axis=(1, 2))
    baseline_means = baseline_error[indices].mean(axis=(1, 2))
    valid = baseline_means > 0
    if valid.mean() < 0.95:
        return None
    samples = 100 * (1 - model_means[valid] / baseline_means[valid])
    return [float(x) for x in np.quantile(samples, [alpha / 2, 1 - alpha / 2])]


def assess(rows, runs, manifest, policy, pending_primary=0, now=None):
    now = pd.Timestamp(now) if now is not None else pd.Timestamp.now(tz='UTC')
    config = manifest['config']
    symbols, modes = config['symbols'], config['modes']
    horizon = policy['primary_horizon']
    if horizon > config['horizon_sessions']:
        raise ValueError('Primary horizon is outside the experiment forecast horizon')
    bases = policy['baselines']
    if bases != ['last_price', 'drift']:
        raise ValueError('Expected fixed last-price and drift baselines')
    # Adjust for mode/baseline selection. Sensitivity checks must ALL pass.
    alpha = (1 - policy['family_confidence']) / (len(modes) * len(bases))
    collection_finished = now >= pd.Timestamp(manifest['collect_until'])
    output = {
        'schema_version': 1,
        'policy_sha256': hashlib.sha256(json.dumps(policy, sort_keys=True).encode()).hexdigest(),
        'primary_horizon': horizon, 'collection_finished': collection_finished,
        'pending_primary_outcomes': pending_primary,
        'interval_confidence_pct': 100 * (1 - alpha),
        'verdict': 'INCONCLUSIVE', 'modes': {},
        'scope': 'Pilot forecasting utility only; not trading profitability or long-term reliability.',
    }
    for mode in modes:
        selected = [r for r in rows if r['mode'] == mode and r['horizon'] == horizon]
        by_origin = {}
        for row in selected:
            group = by_origin.setdefault(row['origin'], {})
            if row['symbol'] in group:
                raise ValueError('Duplicate primary observation')
            group[row['symbol']] = row
        origins = sorted(o for o, group in by_origin.items() if set(group) == set(symbols))
        complete_fraction = len(origins) / len(runs) if runs else 0.
        result = {'verdict': 'INCONCLUSIVE', 'complete_origins': len(origins),
                  'complete_fraction': complete_fraction, 'comparisons': {}, 'reasons': []}
        output['modes'][mode] = result
        if not origins:
            result['reasons'].append('No complete primary-horizon origins yet.')
            continue
        grid = [[by_origin[o][s] for s in symbols] for o in origins]
        actual = np.array([[r['actual'] for r in group] for group in grid])
        anchor = np.array([[r['anchor'] for r in group] for group in grid])
        prediction = np.array([[r['prediction'] for r in group] for group in grid])
        model_error = np.abs(prediction - actual) / anchor
        for base in bases:
            baseline = anchor if base == 'last_price' else np.array([[r['drift_prediction'] for r in group] for group in grid])
            errors = np.abs(baseline - actual) / anchor
            intervals = {
                str(block): bootstrap_skill(model_error, errors, block,
                    policy['bootstrap_repetitions'], alpha, policy['seed'])
                for block in policy['block_lengths']
            }
            symbol_skills = {s: skill(model_error[:, i], errors[:, i]) for i, s in enumerate(symbols)}
            leave_one_out = {s: skill(np.delete(model_error, i, axis=1), np.delete(errors, i, axis=1))
                             for i, s in enumerate(symbols)} if len(symbols) > 1 else {}
            middle = len(origins) // 2
            halves = [skill(model_error[:middle], errors[:middle]), skill(model_error[middle:], errors[middle:])] if middle else [None, None]
            result['comparisons'][base] = {
                'skill_pct': skill(model_error, errors), 'intervals_pct': intervals,
                'symbol_skill_pct': symbol_skills,
                'winning_symbols': sum(v is not None and v > 0 for v in symbol_skills.values()),
                'leave_one_symbol_out_skill_pct': leave_one_out,
                'half_period_skill_pct': halves,
            }
        ready = True
        if not collection_finished:
            result['reasons'].append('Collection window still open; results are interim.')
            ready = False
        if pending_primary:
            result['reasons'].append('Primary-horizon outcomes remain pending.')
            ready = False
        if len(origins) < policy['minimum_complete_origins']:
            result['reasons'].append(f"Need {policy['minimum_complete_origins']} complete origins; have {len(origins)}.")
            ready = False
        if complete_fraction < policy['minimum_complete_fraction']:
            result['reasons'].append('Too many missing or excluded primary observations.')
            ready = False
        if not ready:
            continue
        passes, rejects = [], []
        needed_winners = int(np.ceil(len(symbols) * policy['minimum_winning_symbol_fraction']))
        for base, comparison in result['comparisons'].items():
            estimate = comparison['skill_pct']
            intervals = list(comparison['intervals_pct'].values())
            valid_intervals = all(interval is not None for interval in intervals)
            interval_positive = valid_intervals and all(interval[0] > 0 for interval in intervals)
            comparison['checks'] = {
                'at_least_5pct_improvement': estimate is not None and estimate >= policy['minimum_skill_pct'],
                'positive_lower_interval_both_blocks': bool(interval_positive),
                'wins_on_most_symbols': comparison['winning_symbols'] >= needed_winners,
                'positive_skill_both_halves': all(v is not None and v > 0 for v in comparison['half_period_skill_pct']),
                'positive_skill_after_removing_any_symbol': bool(comparison['leave_one_symbol_out_skill_pct']) and
                    all(v is not None and v > 0 for v in comparison['leave_one_symbol_out_skill_pct'].values()),
            }
            passes.append(all(comparison['checks'].values()))
            # Reject meaningful utility only if every block sensitivity excludes the required gain.
            rejects.append(valid_intervals and all(interval[1] < policy['minimum_skill_pct'] for interval in intervals))
            if not passes[-1]:
                failed = ', '.join(name for name, passed in comparison['checks'].items() if not passed)
                result['reasons'].append(f'{base}: failed checks: {failed}.')
        if all(passes):
            result['verdict'] = 'PROMISING'
            result['reasons'] = ['All pilot improvement and consistency gates passed against both baselines. Confirm on a fresh period.']
        elif any(rejects):
            result['verdict'] = 'NO_GO'
            result['reasons'].append(f"At least one baseline comparison excludes the required {policy['minimum_skill_pct']}% gain in both block checks.")
        else:
            result['reasons'].append('The evidence does not clearly support or exclude the required improvement.')
    verdicts = [r['verdict'] for r in output['modes'].values()]
    if 'PROMISING' in verdicts:
        output['verdict'] = 'PROMISING'
    elif verdicts and all(v == 'NO_GO' for v in verdicts):
        output['verdict'] = 'NO_GO'
    return output


def decision_markdown(decision):
    text = ['## Pilot decision', '', f"**{decision['verdict']}** — primary horizon: {decision['primary_horizon']} trading sessions.", '',
            'PROMISING supports a new untouched confirmation experiment before strategy research. '
            'NO_GO supports deprioritizing this setup. INCONCLUSIVE requires more evidence; it is not a pass.', '',
            '| Mode | Verdict | Complete origins | Last-price skill % | Drift skill % |',
            '|---|---|---:|---:|---:|']
    for mode, result in decision['modes'].items():
        def display(base):
            value = result['comparisons'].get(base, {}).get('skill_pct')
            return 'n/a' if value is None else f'{value:.2f}'
        text.append(f"| {mode} | {result['verdict']} | {result['complete_origins']} | {display('last_price')} | {display('drift')} |")
    text.extend(['', f"Approximate paired block intervals use {decision['interval_confidence_pct']:.2f}% confidence per comparison "
                 '(adjusted for the tested modes/baselines). Stocks are resampled together; block sizes 5 and 10 check sensitivity. '
                 'With a short pilot these intervals remain fragile, and cross-regime reliability is untested.', ''])
    for mode, result in decision['modes'].items():
        text.append(f"**{mode}:** {' '.join(result['reasons'])}")
    text.extend(['', 'See decision.json for uncertainty intervals, individual-stock results, half-period checks, and leave-one-stock-out checks.'])
    return text
