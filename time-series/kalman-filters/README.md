# Kalman Filters and Smoothing for Time-Series Data

Runnable code behind my blog post [Kalman Filters and Smoothing for Time-Series Data](https://aayushgarg.dev/posts/2026-07-15-kalman-filters-time-series/). The post builds the Kalman filter and RTS smoother from first principles and applies them to two classic datasets; these scripts are the full implementations.

## Scripts

| Script | What it does |
|--------|--------------|
| `kalman_co2_decomposition.py` | Example 1 from the post: decomposes the Mauna Loa CO2 series into trend + seasonality with a structural state-space model (`statsmodels UnobservedComponents`), plus a from-scratch Kalman filter/smoother for comparison |
| `kalman_airpassengers_interpolation.py` | Example 2 from the post: deletes chunks of the AirPassengers series and reconstructs them with Kalman smoothing, compared against linear interpolation |
| `forecast_vs_linear.py` | Backs the "forecast as persistence" note in the post: RMSE comparison of causal methods (Kalman filtered, naive/seasonal persistence) vs future-peeking methods (linear interpolation, Kalman smoothed) inside each gap |
| `kalman_decomposition.py` | Synthetic-data version of the decomposition example, useful for stepping through the mechanics without download dependencies |
| `kalman_interpolation.py` | Synthetic-data version of the gap-filling example |

## Running

Requires numpy, pandas, matplotlib, statsmodels. With `uv` there is nothing to install:

```bash
uv run --with numpy --with pandas --with matplotlib --with statsmodels kalman_co2_decomposition.py
```

Each script writes PNG plots to the working directory and prints summary statistics. The CO2 example loads its dataset from statsmodels; the AirPassengers example downloads its CSV from Rdatasets. `forecast_vs_linear.py` must be run from this directory since it reuses the interpolation script's setup.
