"""Controllers designed on the nominal plant only."""

from control import tf


def build_pid(cfg: dict):
    """Filtered PID: Kp + Ki/s + Kd s / (Tf s + 1)."""
    p = cfg["pid"]
    s = tf("s")
    return p["Kp"] + p["Ki"] / s + (p["Kd"] * s) / (p["Tf"] * s + 1)


def build_robust(cfg: dict):
    """H-infinity inspired loop-shaping controller from the report.

    C(s) = gain * (s + z) / (s + p) * (1 / (s/w + 1))^n
    """
    r = cfg["robust"]
    s = tf("s")
    lead = (s + r["zero"]) / (s + r["pole"])
    rolloff = (1 / (s / r["rolloff_omega"] + 1)) ** r["rolloff_order"]
    return r["gain"] * lead * rolloff


def build_hinfinity_mixsyn(G_nom, cfg: dict):
    """Optional formal mixed-sensitivity synthesis (can fail numerically)."""
    from control import mixsyn

    w = cfg["hinfinity_weights"]
    W1 = tf(w["W1_num"], w["W1_den"])
    W2 = tf([w["W2"]], [1])
    W3 = tf([1], [1 / w["W3_omega"], 1])
    C, CL, gamma = mixsyn(G_nom, W1, W2, W3)
    return C, CL, gamma
