"""
Project 4: Trim, Thrust Required and Power Required Analysis
of a 3.5 kg Cropped Delta Wing UAV (steady level flight, sea level).

Run from the repository root:   python src/project4_solver.py
Outputs: results.csv, cropped_delta_uav_performance.png
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- 1. Given data ----------------
m, g, rho = 3.5, 10.0, 1.225            # kg, m/s^2, kg/m^3
Cr, Ct, b, e = 0.9, 0.15, 1.5, 0.89     # m, m, m, -
CD0, Cm0 = 0.03, 0.01
CL_alpha, CL_de = 2.92, 0.265           # 1/rad
Cm_alpha, Cm_de = -0.292, -0.4          # 1/rad
W = m * g

# ---------------- 2. Geometry ----------------
lam = Ct / Cr
S = (b / 2.0) * Cr * (1.0 + lam)
AR = b**2 / S
k = 1.0 / (np.pi * e * AR)

# ---------------- 3. Trim sweep ----------------
alpha_deg = np.arange(0.0, 12.0 + 0.5, 0.5)
alpha = np.radians(alpha_deg)

de = -(Cm0 + Cm_alpha * alpha) / Cm_de          # rad (elevon deflection, no separate tail)
CL = CL_alpha * alpha + CL_de * de
V = np.sqrt(2.0 * W / (rho * S * CL))
CD = CD0 + k * CL**2
Tr = 0.5 * rho * V**2 * S * CD
Pr = Tr * V
L_D = CL / CD
CL15_CD = CL**1.5 / CD

df = pd.DataFrame({
    "alpha_deg": alpha_deg,
    "delta_e_deg": np.degrees(de),
    "CL": CL, "V_ms": V, "CD": CD,
    "Tr_N": Tr, "Pr_W": Pr,
    "CL_CD": L_D, "CL1.5_CD": CL15_CD,
})

print(f"lambda = {lam:.4f}  S = {S:.4f} m^2  AR = {AR:.4f}  k = {k:.5f}  W = {W:.1f} N\n")
print(df.round({"alpha_deg": 1, "delta_e_deg": 2, "CL": 4, "V_ms": 2, "CD": 4,
                "Tr_N": 2, "Pr_W": 2, "CL_CD": 2, "CL1.5_CD": 2}).to_string(index=False))

# ---------------- 4. Key operating points ----------------
i_tr, i_ld, i_pr, i_en = np.argmin(Tr), np.argmax(L_D), np.argmin(Pr), np.argmax(CL15_CD)
print(f"\nMin thrust  : {Tr[i_tr]:.2f} N at alpha = {alpha_deg[i_tr]:.1f} deg, V = {V[i_tr]:.2f} m/s")
print(f"Max CL/CD   : {L_D[i_ld]:.2f} at alpha = {alpha_deg[i_ld]:.1f} deg")
print(f"Lowest power in sweep: {Pr[i_pr]:.2f} W at alpha = {alpha_deg[i_pr]:.1f} deg, V = {V[i_pr]:.2f} m/s")
print(f"Max CL^1.5/CD in sweep: {CL15_CD[i_en]:.2f} at alpha = {alpha_deg[i_en]:.1f} deg")
if i_pr == len(alpha) - 1:
    print("NOTE: power is still falling at the last sweep point, so this is the sweep boundary, not the true optimum.")

# Analytical optima (parabolic polar), for comparison
CL_r, CL_e = np.sqrt(CD0 / k), np.sqrt(3.0 * CD0 / k)
V_of = lambda c: np.sqrt(2 * W / (rho * S * c))
D_of = lambda c: 0.5 * rho * V_of(c)**2 * S * (CD0 + k * c**2)
# alpha for a given trim CL: CL = (CL_alpha - CL_de*Cm_alpha/Cm_de)*alpha - CL_de*Cm0/Cm_de
a_slope = CL_alpha - CL_de * Cm_alpha / Cm_de
a_int = -CL_de * Cm0 / Cm_de
a_of = lambda c: np.degrees((c - a_int) / a_slope)
print(f"\nAnalytical min thrust : CL = {CL_r:.3f}, alpha = {a_of(CL_r):.1f} deg, V = {V_of(CL_r):.2f} m/s, Tr = {D_of(CL_r):.2f} N")
print(f"Analytical min power  : CL = {CL_e:.3f}, alpha = {a_of(CL_e):.1f} deg, V = {V_of(CL_e):.2f} m/s, Pr = {D_of(CL_e)*V_of(CL_e):.2f} W (outside the 0-12 deg sweep)")

# ---------------- 5. Save results ----------------
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
df.to_csv(os.path.join(root, "results.csv"), index=False)

# ---------------- 6. Plots ----------------
sel = alpha_deg >= 1.0     # V-based plots omit alpha < 1 deg (CL ~ 0, V > 35 m/s) so the useful region is readable
fig, ax = plt.subplots(3, 2, figsize=(13, 13))
fig.suptitle("Cropped Delta Wing UAV: Trim & Performance (3.5 kg, sea level, level flight)", fontsize=14, fontweight="bold")

def panel(a, x, y, xl, yl, title, style, note=None, xy=None, xytext=None):
    a.plot(x, y, style, ms=4, lw=1.6)
    a.set_xlabel(xl); a.set_ylabel(yl); a.set_title(title, fontsize=11, fontweight="bold")
    a.grid(True, alpha=0.4)
    if note:
        a.annotate(note, xy=xy, xytext=xytext, textcoords="axes fraction", fontsize=9,
                   arrowprops=dict(arrowstyle="->"), bbox=dict(boxstyle="round", fc="white", ec="gray"))

panel(ax[0, 0], alpha_deg, np.degrees(de), r"$\alpha$ (deg)", r"Trim $\delta_e$ (deg)",
      r"Trim elevator/elevon deflection vs $\alpha$", "o-")
panel(ax[0, 1], alpha_deg, V, r"$\alpha$ (deg)", "Velocity V (m/s)", r"Trim velocity vs $\alpha$", "s-")
panel(ax[1, 0], V[sel], Tr[sel], "Velocity V (m/s)", "Thrust required (N)", "Thrust required vs V", "^-",
      f"Min Tr = {Tr[i_tr]:.2f} N\nat V = {V[i_tr]:.1f} m/s", (V[i_tr], Tr[i_tr]), (0.45, 0.65))
panel(ax[1, 1], V[sel], Pr[sel], "Velocity V (m/s)", "Power required (W)", "Power required vs V", "d-",
      f"Lowest in sweep: {Pr[i_pr]:.1f} W\nat V = {V[i_pr]:.1f} m/s (alpha = 12 deg)", (V[i_pr], Pr[i_pr]), (0.35, 0.65))
panel(ax[2, 0], V[sel], L_D[sel], "Velocity V (m/s)", r"$C_L/C_D$", r"$C_L/C_D$ vs V", "h-",
      f"Max = {L_D[i_ld]:.2f}\nat V = {V[i_ld]:.1f} m/s", (V[i_ld], L_D[i_ld]), (0.45, 0.68))
panel(ax[2, 1], V[sel], CL15_CD[sel], "Velocity V (m/s)", r"$C_L^{1.5}/C_D$", r"$C_L^{1.5}/C_D$ vs V", "p-",
      f"Max in sweep = {CL15_CD[i_en]:.2f}\nat V = {V[i_en]:.1f} m/s (sweep boundary)", (V[i_en], CL15_CD[i_en]), (0.35, 0.80))
fig.text(0.01, 0.005, "V-based panels omit alpha < 1 deg (CL ~ 0, V > 35 m/s). Power and CL^1.5/CD are still improving at alpha = 12 deg.",
         fontsize=8, style="italic", color="gray")
plt.tight_layout(rect=[0, 0.015, 1, 0.97])
plt.savefig(os.path.join(root, "cropped_delta_uav_performance.png"), dpi=200)
print("\nSaved results.csv and cropped_delta_uav_performance.png")
plt.show()
