"""
Time-Series Decomposition: Mauna Loa Atmospheric CO2
=====================================================

Dataset: Weekly atmospheric CO2 concentrations (ppm) recorded at
         the Mauna Loa Observatory, Hawaii, 1958 to 2001.
         Source: Keeling & Whorf (2004), via statsmodels.

This is the canonical example of structural time-series decomposition.
The signal has two clear components:
  (1) A rising trend driven by fossil fuel emissions
  (2) An annual seasonal cycle driven by Northern Hemisphere
      vegetation uptake and release of CO2

We use the Kalman filter (via statsmodels UnobservedComponents) to
separate these components, then also build a from-scratch version
to show the underlying mechanics.

Requirements: numpy, matplotlib, statsmodels, pandas
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.statespace.structural import UnobservedComponents


# ============================================================
# Load and prepare data
# ============================================================

co2_raw = sm.datasets.co2.load_pandas().data["co2"]

# Resample to monthly (the raw data is weekly with some missing values).
# Monthly averaging smooths over within-month variation and fills most
# of the 59 missing weekly observations.
co2_monthly = co2_raw.resample("MS").mean()

# A few months may still be NaN after averaging; interpolate linearly
# for the initial data prep (the Kalman filter can handle NaN too,
# but a clean series makes the from-scratch example simpler).
co2_monthly = co2_monthly.interpolate(method="linear")

# Drop any leading/trailing NaNs
co2_monthly = co2_monthly.dropna()

print(f"Monthly CO2 series: {len(co2_monthly)} observations")
print(f"Date range: {co2_monthly.index[0].strftime('%Y-%m')} to {co2_monthly.index[-1].strftime('%Y-%m')}")
print(f"Range: {co2_monthly.min():.1f} to {co2_monthly.max():.1f} ppm\n")

y = co2_monthly.values
dates = co2_monthly.index
n = len(y)


# ============================================================
# APPROACH 1: statsmodels UnobservedComponents
# ============================================================
# This is the practical, production-ready approach. The model uses
# maximum likelihood to learn the noise covariances automatically.

model_sm = UnobservedComponents(
    co2_monthly,
    level="local linear trend",  # trend = level + slope
    seasonal=12,                 # 12-month seasonal cycle
    stochastic_seasonal=True,    # allow the seasonal shape to evolve
)
results_sm = model_sm.fit(disp=False)

trend_sm = results_sm.level["smoothed"]
seasonal_sm = results_sm.seasonal["smoothed"]
resid_sm = y - trend_sm - seasonal_sm

print("statsmodels parameter estimates:")
print(results_sm.summary().tables[1])
print()


# ============================================================
# APPROACH 2: From-scratch Kalman filter + RTS smoother
# ============================================================
# State vector: [level, slope, s_1, s_2, ..., s_11]
# Dimension: 2 (trend) + 11 (seasonal dummies for period 12) = 13
#
# Dynamics:
#   level_k = level_{k-1} + slope_{k-1} + eta_level
#   slope_k = slope_{k-1} + eta_slope
#   s_1,k   = -(s_1,{k-1} + ... + s_11,{k-1}) + eta_seasonal
#   s_j,k   = s_{j-1,k-1}   for j = 2..11  (shift register)
#
# Observation: y_k = level_k + s_1,k + epsilon

period = 12
state_dim = 2 + (period - 1)  # 13

# State transition matrix F
F = np.zeros((state_dim, state_dim))
F[0, 0] = 1.0   # level persists
F[0, 1] = 1.0   # slope feeds into level
F[1, 1] = 1.0   # slope persists
for j in range(period - 1):
    F[2, 2 + j] = -1.0  # seasonal: sum to zero constraint
for j in range(1, period - 1):
    F[2 + j, 2 + j - 1] = 1.0  # shift older seasons down

# Observation matrix H: y = level + s_1
H = np.zeros((1, state_dim))
H[0, 0] = 1.0
H[0, 2] = 1.0

# Noise covariances (use values close to what statsmodels estimated,
# or tune manually; these produce good results for CO2)
sigma2_level = 0.05
sigma2_slope = 0.001
sigma2_seasonal = 0.01
sigma2_obs = 0.3

Q = np.zeros((state_dim, state_dim))
Q[0, 0] = sigma2_level
Q[1, 1] = sigma2_slope
Q[2, 2] = sigma2_seasonal

R = np.array([[sigma2_obs]])

# Diffuse initialization
x_hat = np.zeros(state_dim)
x_hat[0] = y[0]
P = np.eye(state_dim) * 1e6

# Storage
x_filt = np.zeros((n, state_dim))
P_filt = np.zeros((n, state_dim, state_dim))
x_pred = np.zeros((n, state_dim))
P_pred = np.zeros((n, state_dim, state_dim))

# Forward pass (Kalman filter)
for k in range(n):
    x_prior = F @ x_hat
    P_prior = F @ P @ F.T + Q

    x_pred[k] = x_prior
    P_pred[k] = P_prior

    inn = y[k] - H @ x_prior
    S = H @ P_prior @ H.T + R
    K = P_prior @ H.T @ np.linalg.inv(S)

    x_hat = x_prior + (K @ inn).flatten()
    P = (np.eye(state_dim) - K @ H) @ P_prior

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

trend_scratch = x_smooth[:, 0]
seasonal_scratch = x_smooth[:, 2]
resid_scratch = y - trend_scratch - seasonal_scratch


# ============================================================
# Plot results
# ============================================================

fig, axes = plt.subplots(4, 2, figsize=(16, 13), sharex=True)
fig.suptitle(
    "Mauna Loa CO₂: Structural Decomposition via Kalman Filter",
    fontsize=17, fontweight="bold", y=0.98,
)

axes[0, 0].set_title("From Scratch (NumPy)", fontsize=13, fontweight="bold")
axes[0, 1].set_title("statsmodels UnobservedComponents", fontsize=13, fontweight="bold")

# Row 0: Observed
for col in range(2):
    axes[0, col].plot(dates, y, color="#64748B", linewidth=0.7)
    axes[0, col].set_ylabel("CO₂ (ppm)")
    axes[0, col].text(
        0.02, 0.92, "Observed", transform=axes[0, col].transAxes,
        fontsize=10, fontweight="bold", color="#374151",
        verticalalignment="top",
    )

# Row 1: Trend
axes[1, 0].plot(dates, y, color="#CBD5E1", linewidth=0.4)
axes[1, 0].plot(dates, trend_scratch, color="#16A34A", linewidth=1.8, label="Estimated trend")
axes[1, 0].set_ylabel("Trend (ppm)")
axes[1, 0].legend(loc="upper left", fontsize=9)

axes[1, 1].plot(dates, y, color="#CBD5E1", linewidth=0.4)
axes[1, 1].plot(dates, trend_sm, color="#16A34A", linewidth=1.8, label="Estimated trend")
axes[1, 1].set_ylabel("Trend (ppm)")
axes[1, 1].legend(loc="upper left", fontsize=9)

# Row 2: Seasonal
axes[2, 0].plot(dates, seasonal_scratch, color="#EA580C", linewidth=0.9)
axes[2, 0].axhline(0, color="#D1D5DB", linewidth=0.7)
axes[2, 0].set_ylabel("Seasonal (ppm)")
axes[2, 0].set_ylim(-5, 5)

axes[2, 1].plot(dates, seasonal_sm, color="#EA580C", linewidth=0.9)
axes[2, 1].axhline(0, color="#D1D5DB", linewidth=0.7)
axes[2, 1].set_ylabel("Seasonal (ppm)")
axes[2, 1].set_ylim(-5, 5)

# Row 3: Residual
axes[3, 0].plot(dates, resid_scratch, color="#7C3AED", linewidth=0.6, alpha=0.7)
axes[3, 0].axhline(0, color="#D1D5DB", linewidth=0.7)
axes[3, 0].set_ylabel("Residual (ppm)")

axes[3, 1].plot(dates, resid_sm, color="#7C3AED", linewidth=0.6, alpha=0.7)
axes[3, 1].axhline(0, color="#D1D5DB", linewidth=0.7)
axes[3, 1].set_ylabel("Residual (ppm)")

for ax in axes[3]:
    ax.set_xlabel("Year")
    ax.tick_params(axis="x", rotation=30)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("co2_decomposition.png", dpi=150, bbox_inches="tight")
plt.show()


# ============================================================
# Zoomed seasonal plot (to show individual cycles)
# ============================================================

fig2, ax2 = plt.subplots(figsize=(14, 4))
zoom_start = "1990-01"
zoom_end = "1996-01"
mask = (dates >= zoom_start) & (dates < zoom_end)

ax2.plot(dates[mask], y[mask], "o", color="#94A3B8", markersize=4, label="Observed")
ax2.plot(dates[mask], trend_sm[mask], color="#16A34A", linewidth=2, label="Trend")
ax2.plot(
    dates[mask], trend_sm[mask] + seasonal_sm[mask],
    color="#2563EB", linewidth=1.5, label="Trend + Seasonal",
)
ax2.fill_between(
    dates[mask], trend_sm[mask], trend_sm[mask] + seasonal_sm[mask],
    alpha=0.15, color="#EA580C", label="Seasonal component",
)
ax2.set_title("Zoomed View: 1990 to 1996", fontsize=14, fontweight="bold")
ax2.set_ylabel("CO₂ (ppm)")
ax2.legend(loc="upper left", fontsize=9)
ax2.tick_params(axis="x", rotation=30)

plt.tight_layout()
plt.savefig("co2_seasonal_zoom.png", dpi=150, bbox_inches="tight")
plt.show()

print("\nDecomposition complete.")
print(f"Trend range: {trend_sm.min():.1f} to {trend_sm.max():.1f} ppm")
print(f"Seasonal amplitude: ±{np.abs(seasonal_sm).max():.1f} ppm")
print(f"Residual std: {np.std(resid_sm):.2f} ppm")
