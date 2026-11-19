# Synopsis

**Trim, Thrust Required and Power Required Analysis of a Cropped Delta Wing UAV (Python and MATLAB)**

This project analyses the steady, level, trimmed flight of a 3.5 kg cropped delta wing UAV (wing alone, no separate tail) at sea level. For angles of attack from 0° to 12° in 0.5° steps, a numerical program computes the trim elevator (elevon) deflection from the pitching-moment balance, the trim lift coefficient, the level-flight speed from L = W, the drag from a parabolic polar, and the resulting thrust required, power required, CL/CD and CL^1.5/CD.

Within the sweep, minimum thrust is 4.29 N at 12.26 m/s (α = 10°, δe = −5.87°), which coincides with maximum CL/CD = 8.16 (best range). Power required keeps falling over the whole range, reaching 48.74 W at 11.21 m/s (α = 12°, δe = −7.33°); this is the lowest value within the sweep, and the theoretical optimum (about 45.8 W at 9.3 m/s, α ≈ 17.7°) lies beyond it. Minimum power therefore occurs at a lower speed than minimum thrust, so best endurance is flown slower than best range.

The model is linear with no stall limit and uses aerodynamic power only. Code, results table and plots are provided in Python and MATLAB.
