"""
Compare gap-filling strategies on the AirPassengers artificial gaps.

Reuses the setup from kalman_airpassengers_interpolation.py (runs it up to
the plotting section), then reports RMSE inside each gap for:

  - Kalman FILTERED estimate: predict-only through the gap, i.e. model-based
    persistence. Causal, uses only data up to the gap start.
  - Naive persistence: last observed value carried forward. Causal.
  - Seasonal persistence: value from 12 months earlier. Causal.
  - Linear interpolation: needs the far gap edge, i.e. future data.
  - Kalman SMOOTHED estimate: also uses future data.

Run from this directory:
  uv run --with numpy --with pandas --with matplotlib --with statsmodels forecast_vs_linear.py

The takeaway: the causal Kalman forecast beats linear interpolation in every
gap despite never seeing data past the gap start, because it carries the
whole state (level, slope, seasonal shape) forward instead of just the last
value.
"""
import numpy as np
import pandas as pd

src = open("kalman_airpassengers_interpolation.py").read()
src = src.split("# Plot results")[0]  # run everything up to the plotting
exec(src)

print("\nRMSE per gap (thousands of passengers):")
hdr = (f"{'gap':28s} {'kalman_filt':>11s} {'naive_pers':>10s} "
       f"{'seas_pers':>9s} {'linear':>7s} {'kalman_smooth':>13s}")
print(hdr)
print("-" * len(hdr))
for (start_str, end_str, label), sl in zip(gap_specs, gap_slices):
    true_vals = np.exp(y_full[sl])
    rmse = lambda est: np.sqrt(np.mean((est - true_vals) ** 2))
    r_filt = rmse(np.exp(filtered_scratch[sl]))
    last_obs = np.exp(y_full[sl.start - 1])
    r_naive = rmse(np.full(sl.stop - sl.start, last_obs))
    idx = np.arange(sl.start, sl.stop) - 12
    r_seas = rmse(np.exp(y_full[idx]))
    r_lin = rmse(np.exp(y_linear_interp[sl]))
    r_smooth = rmse(np.exp(smoothed_scratch[sl]))
    print(f"{start_str} to {end_str} ({label:9s}) {r_filt:11.1f} "
          f"{r_naive:10.1f} {r_seas:9.1f} {r_lin:7.1f} {r_smooth:13.1f}")
