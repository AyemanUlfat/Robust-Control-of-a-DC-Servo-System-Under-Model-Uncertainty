"""Nominal rigid-body plant and real plant with unmodeled resonance."""

from control import tf


def build_nominal_plant(cfg: dict):
    """Second-order design model G(s) = K / (s (J s + b))."""
    p = cfg["plant"]
    K, J, b = p["K"], p["J"], p["b"]
    s = tf("s")
    G = K / (s * (J * s + b))
    eps = p.get("regularization_eps", 0.0)
    if eps:
        G = G + eps
    return G


def build_flex_mode(cfg: dict):
    """Lightly damped resonant mode, excluded from controller design."""
    r = cfg["resonance"]
    wr, z = r["omega_r"], r["zeta"]
    s = tf("s")
    return wr**2 / (s**2 + 2 * z * wr * s + wr**2)


def build_real_plant(cfg: dict):
    """Nominal plant cascaded with the unmodeled flexible mode."""
    return build_nominal_plant(cfg) * build_flex_mode(cfg)


def build_perturbed_plant(cfg: dict, K: float, J: float):
    """Parametric plant used in Monte Carlo trials. Friction stays nominal."""
    b = cfg["plant"]["b"]
    s = tf("s")
    return K / (s * (J * s + b))
