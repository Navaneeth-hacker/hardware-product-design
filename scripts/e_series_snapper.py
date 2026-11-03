"""
Standard E-Series Passive Component Snapper
Snaps continuous optimal resistor/capacitor values to standard E12, E24, E96, or E192 component values.
"""

import math
import argparse
import sys

E_SERIES_BASE = {
    "E12": [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2],
    "E24": [
        1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
        3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1
    ],
    "E96": [
        1.00, 1.02, 1.05, 1.07, 1.10, 1.13, 1.15, 1.18, 1.21, 1.24, 1.27, 1.30,
        1.33, 1.37, 1.40, 1.43, 1.47, 1.50, 1.54, 1.58, 1.62, 1.65, 1.69, 1.74,
        1.78, 1.82, 1.87, 1.91, 1.96, 2.00, 2.05, 2.10, 2.15, 2.21, 2.26, 2.32,
        2.37, 2.43, 2.49, 2.55, 2.61, 2.67, 2.74, 2.80, 2.87, 2.94, 3.01, 3.09,
        3.16, 3.24, 3.32, 3.40, 3.48, 3.57, 3.65, 3.74, 3.83, 3.92, 4.02, 4.12,
        4.22, 4.32, 4.42, 4.53, 4.64, 4.75, 4.87, 4.99, 5.11, 5.23, 5.36, 5.49,
        5.62, 5.76, 5.90, 6.04, 6.19, 6.34, 6.49, 6.65, 6.81, 6.98, 7.15, 7.32,
        7.50, 7.68, 7.87, 8.06, 8.25, 8.45, 8.66, 8.87, 9.09, 9.31, 9.53, 9.76
    ]
}

def snap_to_series(val: float, series_name: str = "E96"):
    """
    Finds the nearest value in the specified E-series for an arbitrary positive float.
    Returns (nearest_val, percent_error).
    """
    if val <= 0:
        raise ValueError("Value must be strictly positive.")

    series_name = series_name.upper()
    if series_name not in E_SERIES_BASE:
        raise ValueError(f"Unknown series '{series_name}'. Choose from: {list(E_SERIES_BASE.keys())}")

    base_list = E_SERIES_BASE[series_name]
    decade = 10.0 ** math.floor(math.log10(val))
    norm_val = val / decade

    # Handle boundary conditions around 10.0
    best_candidate = None
    min_ratio_diff = float("inf")

    # Check decade below, current decade, and decade above
    for d_mult in [decade * 0.1, decade, decade * 10.0]:
        for b in base_list:
            candidate = b * d_mult
            diff = abs(candidate - val) / val
            if diff < min_ratio_diff:
                min_ratio_diff = diff
                best_candidate = candidate

    pct_error = ((best_candidate - val) / val) * 100.0
    return best_candidate, pct_error

def format_si(val: float, unit: str = "Ohm") -> str:
    """Format value with SI engineering prefix."""
    prefixes = [
        (1e9, "G"), (1e6, "M"), (1e3, "k"), (1.0, ""),
        (1e-3, "m"), (1e-6, "u"), (1e-9, "n"), (1e-12, "p")
    ]
    for factor, prefix in prefixes:
        if val >= factor * 0.999:
            scaled = val / factor
            if scaled >= 100:
                return f"{scaled:.1f} {prefix}{unit}"
            else:
                return f"{scaled:.2f} {prefix}{unit}"
    return f"{val:.2e} {unit}"

def main():
    parser = argparse.ArgumentParser(description="Snap continuous passive values to standard E-series.")
    parser.add_argument("--value", "-v", type=float, required=True, help="Target value (e.g. 4732.5)")
    parser.add_argument("--series", "-s", type=str, default="E96", choices=["E12", "E24", "E96"], help="Standard E-series (default: E96)")
    parser.add_argument("--unit", "-u", type=str, default="Ohm", help="Unit suffix (e.g. Ohm, F, H)")
    
    args = parser.parse_args()
    
    try:
        snapped, err = snap_to_series(args.value, args.series)
        print(f"Target Value:   {format_si(args.value, args.unit)} ({args.value:.4f})")
        print(f"Standard {args.series}: {format_si(snapped, args.unit)} ({snapped:.4f})")
        print(f"Tolerance Error: {err:+.3f}%")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
