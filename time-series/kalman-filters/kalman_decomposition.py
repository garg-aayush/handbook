"""
Time-Series Decomposition with the Kalman Filter
==================================================

This script demonstrates two approaches to structural time-series decomposition:

1. From scratch using NumPy (to see the mechanics)
2. Using statsmodels.tsa.UnobservedComponents (the practical approach)

Both decompose a synthetic series into trend + seasonal + residual.
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# Generate synthetic data: trend + seasonal + noise
# ============================================================

np.random.seed(42)
n = 200
t = np.arange(n)

# True components
true_trend = 0.05 * t + 2 * np.sin(0.02 * t)  # slowly rising with a curve
true_seasonal = 3 * np.sin(2 * np.pi * t / 12)  # period of 12
true_noise = np.random.normal(0, 0.8, n)

y = true_trend + true_seasonal + true_noise


# ============================================================
# APPROACH 1: From-scratch Kalman filter/smoother
# ============================================================
# State vector: [level, slope, s1, s2, ..., s11]
# where s1..s11 are the seasonal states for period 12.
#
# Dynamics:
#   level_k  = level_{k-1} + slope_{k-1} + eta_level
#   slope_k  = slope_{k-1} + eta_slope
#   seasonal: s1_k = -(s1_{k-1} + s2_{k-1} + ... + s11_{k-1}) + eta_seasonal
#             s2_k = s1_{k-1}, s3_k = s2_{k-1}, ... (shift register)
#
# Observation:
#   y_k = level_k + s1_k + epsilon

period = 12
state_dim = 2 + (period - 1)  # level, slope, 11 seasonal states

# Build F (state transition matrix)
F = np.zeros((state_dim, state_dim))
# Trend block: level = level + slope, slope = slope
F[0, 0] = 1.0
F[0, 1] = 1.0
F[1, 1] = 1.0
# Seasonal block: first seasonal state = negative sum of all others
for j in range(period - 1):
    F[2, 2 + j] = -1.0
# Shift the rest down
for j in range(1, period - 1):
    F[2 + j, 2 + j - 1] = 1.0

# Build H (observation matrix): y = level + s1
H = np.zeros((1, state_dim))
H[0, 0] = 1.0  # level
H[0, 2] = 1.0  # first seasonal state

# Noise covariances (these would normally be estimated via MLE;
# here we set reasonable values for the synthetic data)
sigma2_level = 0.01
sigma2_slope = 0.001
sigma2_seasonal = 0.01
sigma2_obs = 0.5

Q = np.zeros((state_dim, state_dim))
Q[0, 0] = sigma2_level
Q[1, 1] = sigma2_slope
Q[2, 2] = sigma2_seasonal

R = np.array([[sigma2_obs]])

# Initialization (diffuse)
x_hat = np.zeros(state_dim)
x_hat[0] = y[0]  # start level at first observation
P = np.eye(state_dim) * 1e6  # large initial uncertainty

# Storage for filtered and predicted values
x_filtered = np.zeros((n, state_dim))
P_filtered = np.zeros((n, state_dim, state_dim))
x_predicted = np.zeros((n, state_dim))
P_predicted = np.zeros((n, state_dim, state_dim))

# ---- Forward pass (Kalman filter) ----
for k in range(n):
    # Predict
    x_prior = F @ x_hat
    P_prior = F @ P @ F.T + Q

    # Store predictions (needed for smoother)
    x_predicted[k] = x_prior
    P_predicted[k] = P_prior

    # Update
    innovation = y[k] - H @ x_prior
    S = H @ P_prior @ H.T + R
    K = P_prior @ H.T @ np.linalg.inv(S)

    x_hat = x_prior + (K @ innovation).flatten()
    P = (np.eye(state_dim) - K @ H) @ P_prior

    # Store filtered estimates
    x_filtered[k] = x_hat
    P_filtered[k] = P

# ---- Backward pass (RTS smoother) ----
x_smoothed = np.zeros((n, state_dim))
P_smoothed = np.zeros((n, state_dim, state_dim))

x_smoothed[-1] = x_filtered[-1]
P_smoothed[-1] = P_filtered[-1]

for k in range(n - 2, -1, -1):
    G = P_filtered[k] @ F.T @ np.linalg.inv(P_predicted[k + 1])
    x_smoothed[k] = x_filtered[k] + G @ (x_smoothed[k + 1] - x_predicted[k + 1])
    P_smoothed[k] = P_filtered[k] + G @ (P_smoothed[k + 1] - P_predicted[k + 1]) @ G.T

# Extract components from the smoothed state
est_trend_scratch = x_smoothed[:, 0]          # level component
est_seasonal_scratch = x_smoothed[:, 2]       # first seasonal state
est_residual_scratch = y - est_trend_scratch - est_seasonal_scratch


# ============================================================
# APPROACH 2: statsmodels UnobservedComponents
# ============================================================
from statsmodels.tsa.statespace.structural import UnobservedComponents

model = UnobservedComponents(
    y,
    level="local linear trend",   # trend = level + slope
    seasonal=period,              # seasonal period
    stochastic_seasonal=True,
)
results = model.fit(disp=False)

# The smoothed state gives us the decomposition
est_trend_sm = results.level["smoothed"]
est_seasonal_sm = results.seasonal["smoothed"]
est_residual_sm = results.resid


# ============================================================
# Plot results
# ============================================================
fig, axes = plt.subplots(4, 2, figsize=(16, 12), sharex=True)
fig.suptitle(
    "Time-Series Decomposition via Kalman Filter",
    fontsize=16, fontweight="bold", y=0.98,
)

# Column titles
axes[0, 0].set_title("From Scratch (NumPy)", fontsize=13, fontweight="bold")
axes[0, 1].set_title("statsmodels UnobservedComponents", fontsize=13, fontweight="bold")

# Row 0: Observed
for col in range(2):
    axes[0, col].plot(t, y, color="#94A3B8", linewidth=0.8, label="Observed")
    axes[0, col].set_ylabel("Observed")
    axes[0, col].legend(loc="upper left", fontsize=9)

# Row 1: Trend
axes[1, 0].plot(t, true_trend, "k--", linewidth=1, alpha=0.5, label="True trend")
axes[1, 0].plot(t, est_trend_scratch, color="#16A34A", linewidth=1.5, label="Estimated trend")
axes[1, 0].legend(loc="upper left", fontsize=9)
axes[1, 0].set_ylabel("Trend")

axes[1, 1].plot(t, true_trend, "k--", linewidth=1, alpha=0.5, label="True trend")
axes[1, 1].plot(t, est_trend_sm, color="#16A34A", linewidth=1.5, label="Estimated trend")
axes[1, 1].legend(loc="upper left", fontsize=9)
axes[1, 1].set_ylabel("Trend")

# Row 2: Seasonal
axes[2, 0].plot(t, true_seasonal, "k--", linewidth=1, alpha=0.5, label="True seasonal")
axes[2, 0].plot(t, est_seasonal_scratch, color="#EA580C", linewidth=1.5, label="Estimated seasonal")
axes[2, 0].axhline(0, color="#D1D5DB", linewidth=0.8)
axes[2, 0].legend(loc="upper left", fontsize=9)
axes[2, 0].set_ylabel("Seasonal")

axes[2, 1].plot(t, true_seasonal, "k--", linewidth=1, alpha=0.5, label="True seasonal")
axes[2, 1].plot(t, est_seasonal_sm, color="#EA580C", linewidth=1.5, label="Estimated seasonal")
axes[2, 1].axhline(0, color="#D1D5DB", linewidth=0.8)
axes[2, 1].legend(loc="upper left", fontsize=9)
axes[2, 1].set_ylabel("Seasonal")

# Row 3: Residual
axes[3, 0].plot(t, est_residual_scratch, color="#7C3AED", linewidth=0.8, alpha=0.7)
axes[3, 0].axhline(0, color="#D1D5DB", linewidth=0.8)
axes[3, 0].set_ylabel("Residual")
axes[3, 0].set_xlabel("Time step")

axes[3, 1].plot(t, est_residual_sm, color="#7C3AED", linewidth=0.8, alpha=0.7)
axes[3, 1].axhline(0, color="#D1D5DB", linewidth=0.8)
axes[3, 1].set_ylabel("Residual")
axes[3, 1].set_xlabel("Time step")

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("decomposition_result.png", dpi=150, bbox_inches="tight")
plt.show()

print("\nstatsmodels estimated parameters:")
print(results.summary().tables[1])
