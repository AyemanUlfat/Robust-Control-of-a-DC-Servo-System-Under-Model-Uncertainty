"""Figures used in the report: nominal, resonance, Bode, zoom."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from control import frequency_response


def plot_comparison(
    t,
    r,
    y_pid_nom,
    y_rob_nom,
    y_pid_real,
    y_rob_real,
    G_real,
    C_pid,
    C_robust,
    cfg: dict,
    out_path: str,
):
    wr = cfg["resonance"]["omega_r"]
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    ax = axes[0, 0]
    ax.plot(t, r, "k--", linewidth=1.5, label="Reference")
    ax.plot(t, y_pid_nom, "b", linewidth=2.2, label="PID")
    ax.plot(t, y_rob_nom, "r", linewidth=2.2, label="Robust")
    ax.set_title("Nominal Plant (No Resonance)")
    ax.set_ylabel("Position")
    ax.grid(True)
    ax.legend()

    ax = axes[0, 1]
    ax.plot(t, r, "k--", linewidth=1.5)
    ax.plot(t, y_pid_real, "b", linewidth=2.4, label="PID (heavy ringing)")
    ax.plot(t, y_rob_real, "r", linewidth=2.4, label="Robust (smooth)")
    ax.axvspan(cfg["simulation"]["disturbance_start"], cfg["simulation"]["disturbance_end"], alpha=0.2, color="orange")
    ax.set_title("Real Plant with Unmodeled Resonance")
    ax.grid(True)
    ax.legend()

    ax = axes[1, 0]
    resp_pid = frequency_response(G_real * C_pid)
    resp_rob = frequency_response(G_real * C_robust)
    ax.semilogx(resp_pid.frequency, 20 * np.log10(np.maximum(resp_pid.magnitude.squeeze(), 1e-12)), "b", linewidth=2, label="PID")
    ax.semilogx(resp_rob.frequency, 20 * np.log10(np.maximum(resp_rob.magnitude.squeeze(), 1e-12)), "r", linewidth=2, label="Robust")
    ax.axvline(wr, color="k", linestyle="--", linewidth=1.5, label="Resonance (~30 Hz)")
    ax.set_title("Open-Loop Bode Magnitude")
    ax.set_ylabel("Magnitude (dB)")
    ax.grid(True, which="both")
    ax.legend()

    ax = axes[1, 1]
    mask = (t >= 5.0) & (t <= 8.0)
    ax.plot(t[mask], y_pid_real[mask], "b", linewidth=2, label="PID ringing")
    ax.plot(t[mask], y_rob_real[mask], "r", linewidth=2, label="Robust damped")
    ax.set_title("Zoom: Post-Disturbance Behavior")
    ax.set_xlabel("Time (s)")
    ax.grid(True)
    ax.legend()

    fig.suptitle("Unmodeled Resonance: Robust Controller vs PID", fontsize=15)
    fig.tight_layout()
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=300)
    return fig
