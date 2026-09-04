# Source

| Module | Role |
|--------|------|
| `plants.py` | Nominal plant and resonant “real” plant |
| `controllers.py` | PID, loop-shaping robust controller, optional `mixsyn` |
| `simulation.py` | Step reference + pulse disturbance |
| `metrics.py` | Settling time, overshoot, IAE, instability flag |
| `monte_carlo.py` | ±20% \(K\) and \(J\), 1000 trials |
| `plot_results.py` | Four-panel figure from the report |
| `io_utils.py` | Load `config/default.yaml` |
| `run_comparison.py` | Command-line entry point |

Run from the repository root:

```bash
python src/run_comparison.py --fast
```
