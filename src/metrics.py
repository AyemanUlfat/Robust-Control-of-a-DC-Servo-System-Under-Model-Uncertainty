"""Settling time, overshoot, IAE, and a simple instability flag."""

import numpy as np


def calc_metrics(y: np.ndarray, t: np.ndarray, reference: float = 1.0, band: float = 0.02):
    y = np.asarray(y).squeeze()
    err = np.abs(y - reference)
    outside = np.where(err > band)[0]
    settling = float(t[outside[-1]]) if len(outside) else float(t[-1])
    overshoot = float(max(0.0, np.max(y) - reference) * 100.0)
    iae = float(np.trapezoid(err, t))
    return settling, overshoot, iae


def is_unstable(y: np.ndarray, error_limit: float = 0.5, reference: float = 1.0) -> bool:
    y = np.asarray(y).squeeze()
    if not np.all(np.isfinite(y)):
        return True
    return float(np.abs(y[-1] - reference)) > error_limit or float(np.max(np.abs(y))) > 10.0
