"""Parametric uncertainty: ±20% in K and J, 1000 trials."""

import numpy as np
import pandas as pd

from .metrics import calc_metrics, is_unstable
from .plants import build_perturbed_plant
from .simulation import simulate


def run_monte_carlo(cfg: dict, C_pid, C_robust, t, r, d) -> pd.DataFrame:
    mc = cfg["monte_carlo"]
    p = cfg["plant"]
    rng = np.random.default_rng(mc["seed"])
    n = int(mc["n_trials"])

    rows = []
    for i in range(n):
        K = p["K"] * rng.uniform(1 - mc["k_variation"], 1 + mc["k_variation"])
        J = p["J"] * rng.uniform(1 - mc["j_variation"], 1 + mc["j_variation"])
        G = build_perturbed_plant(cfg, K, J)

        for name, C in (("PID", C_pid), ("Robust", C_robust)):
            try:
                y = simulate(G, C, t, r, d)
                settling, overshoot, iae = calc_metrics(
                    y, t, cfg["simulation"]["step_amplitude"], cfg["simulation"]["settling_band"]
                )
                unstable = is_unstable(y, mc["instability_error_limit"], cfg["simulation"]["step_amplitude"])
            except Exception:
                settling, overshoot, iae, unstable = np.nan, np.nan, np.nan, True

            rows.append(
                {
                    "trial": i,
                    "Controller": name,
                    "K": K,
                    "J": J,
                    "Settling Time (s)": settling,
                    "Overshoot (%)": overshoot,
                    "IAE": iae,
                    "Unstable": unstable,
                }
            )

    return pd.DataFrame(rows)


def summarize_monte_carlo(df: pd.DataFrame) -> pd.DataFrame:
    out = []
    for name, g in df.groupby("Controller"):
        n = len(g)
        n_unstable = int(g["Unstable"].sum())
        stable = g.loc[~g["Unstable"]]
        out.append(
            {
                "Controller": name,
                "Settling Time (s)": stable["Settling Time (s)"].mean() if len(stable) else np.nan,
                "Overshoot (%)": stable["Overshoot (%)"].mean() if len(stable) else np.nan,
                "IAE": stable["IAE"].mean() if len(stable) else np.nan,
                "Unstable Cases (%)": 100.0 * n_unstable / n,
            }
        )
    return pd.DataFrame(out).round(3)
