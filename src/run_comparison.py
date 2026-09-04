"""Main entry point: compare PID and the H-infinity inspired controller."""

from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.controllers import build_pid, build_robust
from src.io_utils import load_config
from src.metrics import calc_metrics
from src.monte_carlo import run_monte_carlo, summarize_monte_carlo
from src.plants import build_nominal_plant, build_real_plant
from src.plot_results import plot_comparison
from src.simulation import reference_and_disturbance, simulate, time_vector


def main(run_mc: bool = True):
    cfg = load_config()
    fig_dir = ROOT / cfg["paths"]["figures_dir"]
    fig_dir.mkdir(parents=True, exist_ok=True)

    G_nom = build_nominal_plant(cfg)
    G_real = build_real_plant(cfg)
    C_pid = build_pid(cfg)
    C_rob = build_robust(cfg)

    t = time_vector(cfg)
    r, d = reference_and_disturbance(cfg, t)

    y_pid_nom = simulate(G_nom, C_pid, t, r, d)
    y_rob_nom = simulate(G_nom, C_rob, t, r, d)
    y_pid_real = simulate(G_real, C_pid, t, r, d)
    y_rob_real = simulate(G_real, C_rob, t, r, d)

    band = cfg["simulation"]["settling_band"]
    ref = cfg["simulation"]["step_amplitude"]
    rows = []
    for plant, ctrl, y in (
        ("Nominal", "PID", y_pid_nom),
        ("Nominal", "Robust", y_rob_nom),
        ("Real (Resonance)", "PID", y_pid_real),
        ("Real (Resonance)", "Robust", y_rob_real),
    ):
        settling, overshoot, iae = calc_metrics(y, t, ref, band)
        rows.append(
            {
                "Plant": plant,
                "Controller": ctrl,
                "Settling Time (s)": settling,
                "Overshoot (%)": overshoot,
                "IAE": iae,
            }
        )
    summary = pd.DataFrame(rows).round(3)
    summary_path = ROOT / cfg["paths"]["summary_csv"]
    summary.to_csv(summary_path, index=False)
    print("Time-domain metrics")
    print(summary)

    fig_path = fig_dir / "nominal_vs_resonance.png"
    plot_comparison(
        t, r, y_pid_nom, y_rob_nom, y_pid_real, y_rob_real, G_real, C_pid, C_rob, cfg, str(fig_path)
    )
    print(f"Saved figure: {fig_path}")

    if run_mc:
        print(f"Running Monte Carlo ({cfg['monte_carlo']['n_trials']} trials)...")
        mc_df = run_monte_carlo(cfg, C_pid, C_rob, t, r, d)
        mc_summary = summarize_monte_carlo(mc_df)
        mc_path = ROOT / cfg["paths"]["monte_carlo_csv"]
        mc_summary.to_csv(mc_path, index=False)
        print(mc_summary)
        print(f"Saved Monte Carlo summary: {mc_path}")


if __name__ == "__main__":
    # Pass --fast to skip the 1000-run Monte Carlo.
    main(run_mc="--fast" not in sys.argv)
