"""
Time-Series Interpolation: Box-Jenkins Airline Passengers
==========================================================

Dataset: Monthly totals of international airline passengers (thousands),
         January 1949 to December 1960.
         Source: Box, Jenkins, Reinsel & Ljung (2015), originally from
         the Federal Aviation Administration, via R's datasets package.

This is one of the most studied time series in statistics. It has:
  (1) A clear upward trend
  (2) A multiplicative 12-month seasonal cycle (summer peaks grow
      with the trend)
  (3) Smooth dynamics that a state-space model can exploit

We introduce three realistic gaps (simulating sensor failure or data
loss), then show how the Kalman smoother recovers the missing values,
compared against the known true values and naive linear interpolation.

Because the seasonal pattern is multiplicative, we work in log-space
(where it becomes additive) for the Kalman filter, then transform back.

Requirements: numpy, matplotlib, statsmodels, pandas
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.structural import UnobservedComponents


# ============================================================
# Load data
# ============================================================

url = (
    "https://raw.githubusercontent.com/vincentarelbundock/Rdatasets"
    "/master/csv/datasets/AirPassengers.csv"
)
df = pd.read_csv(url)

# Build a proper datetime index
dates = pd.date_range(start="1949-01", periods=len(df), freq="MS")
passengers = df["value"].values.astype(float)
n = len(passengers)

print(f"AirPassengers: {n} monthly observations")
print(f"Date range: {dates[0].strftime('%Y-%m')} to {dates[-1].strftime('%Y-%m')}")
print(f"Range: {passengers.min():.0f} to {passengers.max():.0f} thousand passengers\n")

# Log-transform: converts the multiplicative seasonal pattern into
# an additive one, which is what the linear Kalman filter assumes.
y_full = np.log(passengers)


# ============================================================
# Introduce gaps (simulating sensor failure / data loss)
# ============================================================

gap_specs = [
    ("1951-07", "1952-03", "8 months"),   # medium gap
    ("1955-01", "1955-10", "9 months"),   # larger gap spanning almost a year
    ("1958-06", "1958-10", "4 months"),   # short gap
]

is_observed = np.ones(n, dtype=bool)
gap_slices = []
for start_str, end_str, _ in gap_specs:
    start_idx = np.searchsorted(dates, pd.Timestamp(start_str))
    end_idx = np.searchsorted(dates, pd.Timestamp(end_str))
    is_observed[start_idx:end_idx] = False
    gap_slices.append(slice(start_idx, end_idx))

y_with_gaps = y_full.copy()
y_with_gaps[~is_observed] = np.nan

n_missing = (~is_observed).sum()
print(f"Introduced {n_missing} missing values across {len(gap_specs)} gaps:")
for (start_str, end_str, label), sl in zip(gap_specs, gap_slices):
    print(f"  {start_str} to {end_str} ({label}, indices {sl.start} to {sl.stop})")
print()


# ============================================================
# APPROACH 1: statsmodels Kalman smoother
# ============================================================
# statsmodels handles NaN as missing data automatically.

series_with_gaps = pd.Series(y_with_gaps, index=dates)

model = UnobservedComponents(
    series_with_gaps,
    level="local linear trend",
    seasonal=12,
    stochastic_seasonal=True,
)
results = model.fit(disp=False)

smoothed_sm = results.level["smoothed"] + results.seasonal["smoothed"]
filtered_sm = results.level["filtered"] + results.seasonal["filtered"]


# ============================================================
# APPROACH 2: From-scratch Kalman filter + RTS smoother
# ============================================================
# State: [level, slope, s_1, ..., s_11]  (same model as statsmodels)

period = 12
state_dim = 2 + (period - 1)

F = np.zeros((state_dim, state_dim))
F[0, 0] = 1.0
F[0, 1] = 1.0
F[1, 1] = 1.0
for j in range(period - 1):
    F[2, 2 + j] = -1.0
for j in range(1, period - 1):
    F[2 + j, 2 + j - 1] = 1.0

H = np.zeros((1, state_dim))
H[0, 0] = 1.0
H[0, 2] = 1.0

# Use noise parameters inspired by the statsmodels MLE fit
sigma2_level = 0.0001
sigma2_slope = 1e-7
sigma2_seasonal = 1e-6
sigma2_obs = 0.001

Q = np.zeros((state_dim, state_dim))
Q[0, 0] = sigma2_level
Q[1, 1] = sigma2_slope
Q[2, 2] = sigma2_seasonal
R = np.array([[sigma2_obs]])

# Initialization
x_hat = np.zeros(state_dim)
x_hat[0] = y_full[0]
P = np.eye(state_dim) * 1e4

x_filt = np.zeros((n, state_dim))
P_filt = np.zeros((n, state_dim, state_dim))
x_pred = np.zeros((n, state_dim))
P_pred = np.zeros((n, state_dim, state_dim))

# Forward pass
for k in range(n):
    x_prior = F @ x_hat
    P_prior = F @ P @ F.T + Q

    x_pred[k] = x_prior
    P_pred[k] = P_prior

    if is_observed[k]:
        inn = y_with_gaps[k] - (H @ x_prior).item()
        S = H @ P_prior @ H.T + R
        K = P_prior @ H.T @ np.linalg.inv(S)
        x_hat = x_prior + (K * inn).flatten()
        P = (np.eye(state_dim) - K @ H) @ P_prior
    else:
        # KEY: skip the update when data is missing
        x_hat = x_prior
        P = P_prior

    x_filt[k] = x_hat
    P_filt[k] = P

# Backward pass (RTS smoother)
x_smooth = np.zeros((n, state_dim))
P_smooth = np.zeros((n, state_dim, state_dim))
x_smooth[-1] = x_filt[-1]
P_smooth[-1] = P_filt[-1]

for k in range(n - 2, -1, -1):
    G = P_filt[k] @ F.T @ np.linalg.inv(P_pred[k + 1])
    x_smooth[k] = x_filt[k] + G @ (x_smooth[k + 1] - x_pred[k + 1])
    P_smooth[k] = P_filt[k] + G @ (P_smooth[k + 1] - P_pred[k + 1]) @ G.T

# Reconstruct y = level + seasonal
smoothed_scratch = x_smooth[:, 0] + x_smooth[:, 2]
filtered_scratch = x_filt[:, 0] + x_filt[:, 2]

# Uncertainty (in log-space, from the smoothed covariance)
var_smooth = P_smooth[:, 0, 0] + P_smooth[:, 2, 2] + 2 * P_smooth[:, 0, 2]
std_smooth = np.sqrt(var_smooth)


# ============================================================
# Naive baseline: linear interpolation
# ============================================================

y_linear_interp = y_full.copy()
y_linear_interp[~is_observed] = np.nan
y_linear_interp = pd.Series(y_linear_interp).interpolate(method="linear").values


# ============================================================
# Compute accuracy metrics (in original passenger-count space)
# ============================================================

print("Interpolation accuracy (RMSE in thousands of passengers):")
print("=" * 62)

for (start_str, end_str, label), sl in zip(gap_specs, gap_slices):
    true_vals = np.exp(y_full[sl])
    rmse_scratch = np.sqrt(np.mean((np.exp(smoothed_scratch[sl]) - true_vals) ** 2))
    rmse_sm = np.sqrt(np.mean((np.exp(smoothed_sm[sl]) - true_vals) ** 2))
    rmse_linear = np.sqrt(np.mean((np.exp(y_linear_interp[sl]) - true_vals) ** 2))

    print(f"\n  Gap: {start_str} to {end_str} ({label})")
    print(f"    Kalman smoother (scratch):     {rmse_scratch:7.1f}")
    print(f"    Kalman smoother (statsmodels): {rmse_sm:7.1f}")
    print(f"    Linear interpolation:          {rmse_linear:7.1f}")


# ============================================================
# Plot results (transform back to original passenger counts)
# ============================================================

fig, axes = plt.subplots(3, 1, figsize=(15, 13), sharex=True)
fig.suptitle(
    "AirPassengers: Gap Filling with the Kalman Smoother",
    fontsize=17, fontweight="bold", y=0.98,
)

# Shade gaps on all panels
for ax in axes:
    for (start_str, end_str, _), sl in zip(gap_specs, gap_slices):
        ax.axvspan(dates[sl.start], dates[sl.stop - 1], alpha=0.12, color="#F59E0B")

# Panel 1: Raw data
ax = axes[0]
ax.plot(dates[is_observed], passengers[is_observed], "o",
        color="#64748B", markersize=4, label="Observed")
ax.plot(dates, passengers, color="#CBD5E1", linewidth=0.8, zorder=0)
ax.set_ylabel("Passengers (thousands)")
ax.set_title("Observed Data (gaps highlighted in amber)", fontsize=12)
ax.legend(loc="upper left", fontsize=9)

# Panel 2: From-scratch Kalman smoother
ax = axes[1]
ax.scatter(dates[is_observed], passengers[is_observed],
           s=10, color="#94A3B8", alpha=0.5, zorder=2)
ax.plot(dates, passengers, color="#E2E8F0", linewidth=0.7, zorder=0, label="True (hidden in gaps)")
ax.plot(dates, np.exp(filtered_scratch), color="#93C5FD", linewidth=1,
        alpha=0.6, label="Filtered (causal only)")
ax.plot(dates, np.exp(smoothed_scratch), color="#7C3AED", linewidth=2,
        label="Smoothed (all data)")
ax.fill_between(
    dates,
    np.exp(smoothed_scratch - 2 * std_smooth),
    np.exp(smoothed_scratch + 2 * std_smooth),
    alpha=0.12, color="#7C3AED", label="95% confidence band",
)
ax.plot(dates, np.exp(y_linear_interp), color="#F97316", linewidth=1,
        linestyle=":", alpha=0.7, label="Linear interpolation")
ax.set_ylabel("Passengers (thousands)")
ax.set_title("From Scratch: Kalman Filter vs Smoother vs Linear", fontsize=12)
ax.legend(loc="upper left", fontsize=9)

# Panel 3: statsmodels
ax = axes[2]
ax.scatter(dates[is_observed], passengers[is_observed],
           s=10, color="#94A3B8", alpha=0.5, zorder=2)
ax.plot(dates, passengers, color="#E2E8F0", linewidth=0.7, zorder=0, label="True (hidden in gaps)")
ax.plot(dates, np.exp(filtered_sm), color="#93C5FD", linewidth=1,
        alpha=0.6, label="Filtered (causal only)")
ax.plot(dates, np.exp(smoothed_sm), color="#16A34A", linewidth=2,
        label="Smoothed (all data)")
ax.plot(dates, np.exp(y_linear_interp), color="#F97316", linewidth=1,
        linestyle=":", alpha=0.7, label="Linear interpolation")
ax.set_ylabel("Passengers (thousands)")
ax.set_xlabel("Date")
ax.set_title("statsmodels: UnobservedComponents", fontsize=12)
ax.legend(loc="upper left", fontsize=9)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("airpassengers_interpolation.png", dpi=150, bbox_inches="tight")
plt.show()


# ============================================================
# Zoomed gap comparison
# ============================================================

fig2, axes2 = plt.subplots(1, 3, figsize=(16, 4.5))
fig2.suptitle("Zoomed View of Each Gap", fontsize=14, fontweight="bold")

for i, ((start_str, end_str, label), sl) in enumerate(zip(gap_specs, gap_slices)):
    ax = axes2[i]
    # Show a window around the gap (5 months of padding on each side)
    pad = 5
    win = slice(max(0, sl.start - pad), min(n, sl.stop + pad))

    ax.axvspan(dates[sl.start], dates[sl.stop - 1], alpha=0.12, color="#F59E0B")

    ax.plot(dates[win], passengers[win], "o", color="#374151", markersize=5,
            zorder=3, label="True values")
    ax.plot(dates[win], np.exp(smoothed_scratch[win]), color="#7C3AED",
            linewidth=2, label="Kalman smoothed")
    ax.plot(dates[win], np.exp(y_linear_interp[win]), color="#F97316",
            linewidth=1.5, linestyle=":", label="Linear interp.")

    # Mark the hidden true values inside the gap
    ax.plot(dates[sl], passengers[sl], "x", color="#DC2626", markersize=8,
            zorder=4, label="Hidden truth")

    ax.set_title(f"{start_str} to {end_str} ({label})", fontsize=11)
    ax.tick_params(axis="x", rotation=30)
    if i == 0:
        ax.set_ylabel("Passengers (thousands)")
        ax.legend(fontsize=8, loc="upper left")

plt.tight_layout()
plt.savefig("airpassengers_gaps_zoomed.png", dpi=150, bbox_inches="tight")
plt.show()

print("\n\nKey takeaways:")
print("  (1) The Kalman smoother captures the seasonal shape inside gaps,")
print("      while linear interpolation ignores it completely.")
print("  (2) The 9-month gap (nearly a full seasonal cycle) is the hardest,")
print("      but the smoother still recovers the pattern because the model")
print("      encodes 12-month periodicity in its state dynamics.")
print("  (3) Confidence bands widen inside gaps and narrow at the edges,")
print("      correctly reflecting how far the nearest observations are.")
print("  (4) Working in log-space handles the multiplicative seasonal growth,")
print("      keeping the linear Kalman filter assumption valid.")
