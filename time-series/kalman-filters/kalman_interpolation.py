"""
Time-Series Interpolation (Gap Filling) with the Kalman Smoother
=================================================================

This script demonstrates how to fill gaps in a time series using
the Kalman filter and RTS smoother. Two approaches:

1. From scratch using NumPy (to see exactly how missing data is handled)
2. Using statsmodels (the practical, production-ready approach)

The key insight: when a measurement is missing, skip the update step.
The predict step still runs, propagating the state through the gap.
The backward smoother pass then pulls information from future
measurements back through the gap, producing a principled interpolation
with uncertainty estimates.
"""

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# Generate synthetic data with gaps
# ============================================================

np.random.seed(123)
n = 300
t = np.arange(n)

# True underlying signal: smooth trend with some curvature
true_signal = 5 + 0.03 * t + 2 * np.sin(2 * np.pi * t / 60) + 0.8 * np.sin(2 * np.pi * t / 25)

# Noisy observations
noise_std = 0.6
y_full = true_signal + np.random.normal(0, noise_std, n)

# Create gaps (missing data regions)
gap_ranges = [(80, 120), (180, 210), (250, 265)]  # three gaps of varying size
is_observed = np.ones(n, dtype=bool)
for start, end in gap_ranges:
    is_observed[start:end] = False

y_observed = y_full.copy()
y_observed[~is_observed] = np.nan


# ============================================================
# APPROACH 1: From-scratch Kalman filter/smoother
# ============================================================
# State: [position, velocity, acceleration]
# This is a "constant acceleration" model, which provides smooth
# interpolation that respects the signal's local curvature.
#
# Dynamics (with dt = 1):
#   pos_k  = pos_{k-1} + vel_{k-1} + 0.5*acc_{k-1}
#   vel_k  = vel_{k-1} + acc_{k-1}
#   acc_k  = acc_{k-1} + noise
#
# Observation:
#   y_k = pos_k + measurement_noise

state_dim = 3
dt = 1.0

F = np.array([
    [1, dt, 0.5 * dt**2],
    [0, 1,  dt],
    [0, 0,  1],
])

H = np.array([[1.0, 0.0, 0.0]])

# Process noise: only on acceleration (jerk noise model)
q_acc = 0.001  # controls smoothness (smaller = smoother interpolation)
Q = np.zeros((3, 3))
# Discrete noise matrix for piecewise constant jerk
Q[0, 0] = (dt**5) / 20
Q[0, 1] = (dt**4) / 8
Q[0, 2] = (dt**3) / 6
Q[1, 0] = (dt**4) / 8
Q[1, 1] = (dt**3) / 3
Q[1, 2] = (dt**2) / 2
Q[2, 0] = (dt**3) / 6
Q[2, 1] = (dt**2) / 2
Q[2, 2] = dt
Q *= q_acc

R = np.array([[noise_std**2]])

# Initialization
x_hat = np.array([y_full[0], 0.0, 0.0])
P = np.eye(state_dim) * 100.0

# Storage
x_filtered = np.zeros((n, state_dim))
P_filtered = np.zeros((n, state_dim, state_dim))
x_predicted = np.zeros((n, state_dim))
P_predicted = np.zeros((n, state_dim, state_dim))

# ---- Forward pass ----
for k in range(n):
    # Predict
    x_prior = F @ x_hat
    P_prior = F @ P @ F.T + Q

    x_predicted[k] = x_prior
    P_predicted[k] = P_prior

    if is_observed[k]:
        # Update (measurement available)
        innovation = y_observed[k] - H @ x_prior
        S = H @ P_prior @ H.T + R
        K = P_prior @ H.T @ np.linalg.inv(S)
        x_hat = x_prior + (K @ innovation).flatten()
        P = (np.eye(state_dim) - K @ H) @ P_prior
    else:
        # No measurement: skip update, prior becomes posterior
        x_hat = x_prior
        P = P_prior

    x_filtered[k] = x_hat
    P_filtered[k] = P

# ---- Backward pass (RTS smoother) ----
x_smoothed = np.zeros((n, state_dim))
P_smoothed = np.zeros((n, state_dim, state_dim))

x_smoothed[-1] = x_filtered[-1]
P_smoothed[-1] = P_filtered[-1]

for k in range(n - 2, -1, -1):
    P_pred_inv = np.linalg.inv(P_predicted[k + 1])
    G = P_filtered[k] @ F.T @ P_pred_inv
    x_smoothed[k] = x_filtered[k] + G @ (x_smoothed[k + 1] - x_predicted[k + 1])
    P_smoothed[k] = P_filtered[k] + G @ (P_smoothed[k + 1] - P_predicted[k + 1]) @ G.T

# Extract position estimate and uncertainty
pos_smoothed = x_smoothed[:, 0]
pos_std = np.sqrt(P_smoothed[:, 0, 0])
pos_filtered = x_filtered[:, 0]
pos_filtered_std = np.sqrt(P_filtered[:, 0, 0])


# ============================================================
# APPROACH 2: statsmodels
# ============================================================
from statsmodels.tsa.statespace.structural import UnobservedComponents

# statsmodels handles np.nan as missing data automatically
model = UnobservedComponents(
    y_observed,
    level="local linear trend",
)
results = model.fit(disp=False)

# Smoothed state (uses all data, including future observations)
sm_smoothed = results.level["smoothed"]
# Filtered state (uses only past data)
sm_filtered = results.level["filtered"]


# ============================================================
# Plot results
# ============================================================
fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=True)
fig.suptitle(
    "Kalman Smoother Interpolation: Filling Gaps in Time Series",
    fontsize=16, fontweight="bold", y=0.98,
)

# Shade the gap regions on all panels
for ax in axes:
    for start, end in gap_ranges:
        ax.axvspan(start, end, alpha=0.12, color="#F59E0B", zorder=0)

# ---- Panel 1: Raw data with gaps ----
ax = axes[0]
ax.scatter(
    t[is_observed], y_observed[is_observed],
    s=8, color="#94A3B8", alpha=0.6, zorder=2, label="Observed",
)
ax.plot(t, true_signal, "k--", linewidth=1, alpha=0.4, label="True signal")
ax.set_ylabel("Value")
ax.set_title("Observed Data (with gaps highlighted in amber)", fontsize=12)
ax.legend(loc="upper left", fontsize=9)

# ---- Panel 2: From-scratch results ----
ax = axes[1]
ax.scatter(
    t[is_observed], y_observed[is_observed],
    s=6, color="#94A3B8", alpha=0.4, zorder=2,
)
ax.plot(t, true_signal, "k--", linewidth=1, alpha=0.3, label="True signal")
ax.plot(t, pos_filtered, color="#2563EB", linewidth=1, alpha=0.5, label="Filtered (causal)")
ax.plot(t, pos_smoothed, color="#7C3AED", linewidth=1.8, label="Smoothed (uses all data)")
ax.fill_between(
    t, pos_smoothed - 2 * pos_std, pos_smoothed + 2 * pos_std,
    alpha=0.15, color="#7C3AED", label="95% confidence band",
)
ax.set_ylabel("Value")
ax.set_title("From Scratch: Kalman Filter vs Smoother", fontsize=12)
ax.legend(loc="upper left", fontsize=9)

# ---- Panel 3: statsmodels results ----
ax = axes[2]
ax.scatter(
    t[is_observed], y_observed[is_observed],
    s=6, color="#94A3B8", alpha=0.4, zorder=2,
)
ax.plot(t, true_signal, "k--", linewidth=1, alpha=0.3, label="True signal")
ax.plot(t, sm_filtered, color="#2563EB", linewidth=1, alpha=0.5, label="Filtered (causal)")
ax.plot(t, sm_smoothed, color="#16A34A", linewidth=1.8, label="Smoothed (uses all data)")
ax.set_ylabel("Value")
ax.set_xlabel("Time step")
ax.set_title("statsmodels: UnobservedComponents", fontsize=12)
ax.legend(loc="upper left", fontsize=9)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("interpolation_result.png", dpi=150, bbox_inches="tight")
plt.show()


# ============================================================
# Print gap-filling accuracy
# ============================================================
print("\nInterpolation accuracy (RMSE in gap regions):")
print("=" * 50)
for start, end in gap_ranges:
    gap_slice = slice(start, end)
    rmse_scratch = np.sqrt(np.mean((pos_smoothed[gap_slice] - true_signal[gap_slice])**2))
    rmse_sm = np.sqrt(np.mean((sm_smoothed[gap_slice] - true_signal[gap_slice])**2))
    rmse_linear = np.sqrt(np.mean(
        (np.interp(t[gap_slice], t[is_observed], y_observed[is_observed]) - true_signal[gap_slice])**2
    ))
    print(f"\nGap t={start} to {end} ({end - start} points missing):")
    print(f"  Kalman smoother (scratch):     RMSE = {rmse_scratch:.4f}")
    print(f"  Kalman smoother (statsmodels): RMSE = {rmse_sm:.4f}")
    print(f"  Linear interpolation:          RMSE = {rmse_linear:.4f}")

print("\n\nKey observations:")
print("  (1) The smoother outperforms the filter in gap regions because")
print("      it uses future data to constrain the interpolation.")
print("  (2) The confidence band widens inside gaps and narrows near")
print("      observed data, correctly reflecting higher uncertainty.")
print("  (3) The Kalman smoother typically beats linear interpolation,")
print("      especially for curved signals, because it respects the")
print("      signal dynamics (velocity and acceleration continuity).")
