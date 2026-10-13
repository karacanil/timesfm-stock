"""TimesFM 3.0 adapter. Batched univariate and joint multivariate experiments."""
from __future__ import annotations

import numpy as np

UPSTREAM_COMMIT = "e51928e27119cb17bebc005be2696b75e0a9e688"
QUANTILES = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]


class TimesFM:
    def __init__(self, config, revision):
        from timesfm3 import ModelConfig, TimesFM3Forecaster
        self.forecaster = TimesFM3Forecaster(ModelConfig(
            checkpoint_path=config["checkpoint"], revision=revision,
            device=config["device"], per_core_batch_size=config["batch_size"],
        ))
        if list(self.forecaster.config.quantiles) != QUANTILES:
            raise ValueError("Unexpected checkpoint quantile layout")

    def predict(self, matrix, horizon, modes):
        result = {}
        for mode in modes:
            inputs = [row.astype(np.float32) for row in matrix] if mode == "univariate" else [matrix.astype(np.float32)]
            outputs = list(self.forecaster.predict_batch(
                inputs, horizon=horizon, return_quantiles=True,
                use_symmetric_averaging=False, make_positive=True,
                sort_quantiles=True, use_znorm=False, padding_mode="none",
            ))
            if mode == "univariate":
                point = np.stack([o.forecast for o in outputs])
                quantiles = np.stack([o.quantiles for o in outputs])
            else:
                point, quantiles = outputs[0].forecast, outputs[0].quantiles
            point, quantiles = np.asarray(point), np.asarray(quantiles)
            expected = (matrix.shape[0], horizon)
            if point.shape != expected or quantiles.shape != (*expected, 9):
                raise ValueError(f"Unexpected TimesFM output shapes: {point.shape}, {quantiles.shape}")
            if not np.isfinite(point).all() or not np.isfinite(quantiles).all():
                raise ValueError("Non-finite TimesFM output")
            result[mode] = {"point": point.tolist(), "quantiles": quantiles.tolist()}
        return result


def resolve_revision(config):
    from huggingface_hub import HfApi
    # Resolve once, then use this exact weight commit throughout the experiment.
    return HfApi().model_info(config["checkpoint"], revision=config["checkpoint_revision"]).sha
