"""Time-domain simulation of tracking plus load-disturbance rejection."""

import numpy as np
from control import feedback, forced_response


def time_vector(cfg: dict) -> np.ndarray:
    sim = cfg["simulation"]
    return np.linspace(0.0, sim["t_end"], int(sim["n_samples"]))


def reference_and_disturbance(cfg: dict, t: np.ndarray):
    sim = cfg["simulation"]
    r = sim["step_amplitude"] * np.ones_like(t)
    d = sim["disturbance_amplitude"] * ((t >= sim["disturbance_start"]) & (t < sim["disturbance_end"]))
    return r, d.astype(float)


def simulate(G, C, t: np.ndarray, r: np.ndarray, d: np.ndarray) -> np.ndarray:
    """y = T r + G S d, with T = GC/(1+GC) and S = 1/(1+GC)."""
    T = feedback(G * C, 1)
    S_load = G * feedback(1, G * C)
    y_ref = forced_response(T, T=t, U=r).outputs
    y_dist = forced_response(S_load, T=t, U=d).outputs
    return np.asarray(y_ref).squeeze() + np.asarray(y_dist).squeeze()
