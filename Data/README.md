# Data

This project is simulation-only. There is no experimental motor dataset.

## What belongs here

| Path | Contents |
|------|----------|
| `results/` | Generated figures (PNG) and metric tables (CSV) |
| `README.md` | This file |

Simulation outputs created by `src/run_comparison.py` and the notebook:

- `results/nominal_vs_resonance.png`
- `results/performance_summary.csv`
- `results/monte_carlo_summary.csv`

Figures from the report and presentation can also be stored under `results/` if you export them.

## Why `.gitkeep` exists

Git does not track empty folders. `.gitkeep` keeps `results/` in the repository until real files appear.
