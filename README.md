# Robust-Control-of-a-DC-Servo-System-Under-Model-Uncertainty

# Robust Control of a DC Servo System Under Model Uncertainty

A comparison between **PID** and an **H-infinity inspired** loop-shaping controller for a DC servo position loop.

Author: **Ayeman Ulfat**  
Department of AI and Automation, University West, Trollhättan, Sweden  
`ayul0001@student.hv.se`

Both controllers are designed on a **nominal second-order plant**. They are then tested on:

1. the nominal model
2. parametric uncertainty (±20% in motor gain \(K\) and inertia \(J\), 1000 Monte Carlo trials)
3. a plant with an **unmodeled lightly damped resonance** near 30 Hz

On the design model, PID is slightly faster. When the model is wrong, PID can ring or go unstable. The robust controller keeps high-frequency gain low and stays well damped.

## Repository layout

```text
config/          YAML parameters (plant, gains, simulation, Monte Carlo)
data/            simulation outputs and report tables
src/             reusable Python source
notebooks/       interactive walkthrough
docs/            place the final report PDF and slides here
requirements.txt Python dependencies
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Main comparison (skip 1000-run Monte Carlo with --fast)
python src/run_comparison.py --fast

# Full Monte Carlo from the report
python src/run_comparison.py
```

Open `notebooks/pid_vs_hinfinity_servo.ipynb` for the same study step by step.

Formal mixed-sensitivity synthesis (`control.mixsyn`) is optional and can fail on this plant without regularization. The report controller is the hand-shaped transfer function in `config/default.yaml`.

## Models

Nominal plant used for design:

\[
G_{\mathrm{nom}}(s)=\frac{100}{s^{2}+10s}
\]

Real plant with unmodeled resonance (\(\omega_r=188\,\mathrm{rad/s}\), \(\zeta=0.05\)):

\[
G_{\mathrm{real}}(s)=G_{\mathrm{nom}}(s)\cdot\frac{\omega_r^{2}}{s^{2}+2\zeta\omega_r s+\omega_r^{2}}
\]

PID (filtered derivative):

\[
C_{\mathrm{PID}}(s)=25+\frac{120}{s}+\frac{0.08s}{0.01s+1}
\]

Robust / H-infinity inspired:

\[
C_{\mathrm{robust}}(s)=40\cdot\frac{s+6}{s+60}\cdot\left(\frac{1}{s/120+1}\right)^{2}
\]

## Report findings (Monte Carlo means)

| Controller | Settling time (s) | Overshoot (%) | IAE   | Unstable cases (%) |
|------------|-------------------|---------------|-------|--------------------|
| PID        | 5.57              | 74.4          | 0.116 | 5–8                |
| Robust     | 5.78              | 59.6          | 0.172 | 0                  |


