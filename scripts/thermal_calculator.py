"""
Thermal and Trace Capacity Calculator
Computes junction temperatures, required heatsink thermal resistance,
and IPC-2152 trace current capacity.
"""

import math
import argparse
import sys

def calculate_junction_temp(ambient_c: float, power_watts: float, r_theta_ja: float):
    """
    T_j = T_a + (P * R_theta_ja)
    """
    t_j = ambient_c + (power_watts * r_theta_ja)
    return t_j

def calculate_required_heatsink(max_t_j: float, ambient_c: float, power_watts: float, r_theta_jc: float, r_theta_cs: float = 0.5):
    """
    R_theta_sa = ( (T_j_max - T_ambient) / P ) - R_theta_jc - R_theta_cs
    """
    if power_watts <= 0:
        return 0.0
    total_budget = (max_t_j - ambient_c) / power_watts
    r_theta_sa = total_budget - r_theta_jc - r_theta_cs
    return r_theta_sa

def ipc2152_trace_width(current_amps: float, temp_rise_c: float = 10.0, copper_oz: float = 1.0, is_internal: bool = False):
    """
    Approximation based on IPC-2152 / IPC-2221 for external and internal traces.
    Area (mils^2) = ( Current / (k * (Temp_Rise ^ b)) ) ^ (1 / c)
    Thickness: 1 oz copper = ~1.37 mils (35 um)
    """
    if is_internal:
        k = 0.024
        b = 0.44
        c = 0.725
    else:
        k = 0.048
        b = 0.44
        c = 0.725

    area_mils2 = (current_amps / (k * (temp_rise_c ** b))) ** (1.0 / c)
    thickness_mils = copper_oz * 1.37
    width_mils = area_mils2 / thickness_mils
    width_mm = width_mils * 0.0254

    return width_mm, width_mils

def main():
    parser = argparse.ArgumentParser(description="Hardware Thermal and Trace Capacity Calculator")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Junction temp
    p_tj = subparsers.add_parser("junction", help="Calculate junction temperature")
    p_tj.add_argument("--ambient", "-a", type=float, default=25.0, help="Ambient temperature in °C (default: 25)")
    p_tj.add_argument("--power", "-p", type=float, required=True, help="Power dissipation in Watts")
    p_tj.add_argument("--rja", "-r", type=float, required=True, help="Junction-to-ambient thermal resistance (°C/W)")

    # Heatsink
    p_hs = subparsers.add_parser("heatsink", help="Calculate required heatsink thermal resistance")
    p_hs.add_argument("--max-tj", type=float, default=100.0, help="Max allowed junction temp in °C (default: 100)")
    p_hs.add_argument("--ambient", "-a", type=float, default=40.0, help="Max ambient temperature in °C (default: 40)")
    p_hs.add_argument("--power", "-p", type=float, required=True, help="Power dissipation in Watts")
    p_hs.add_argument("--rjc", type=float, required=True, help="Junction-to-case thermal resistance (°C/W)")
    p_hs.add_argument("--rcs", type=float, default=0.5, help="Case-to-sink thermal resistance of interface pad (°C/W)")

    # Trace width
    p_tr = subparsers.add_parser("trace", help="Calculate minimum trace width for current")
    p_tr.add_argument("--current", "-i", type=float, required=True, help="Continuous current in Amperes")
    p_tr.add_argument("--rise", "-t", type=float, default=10.0, help="Allowed temperature rise in °C (default: 10)")
    p_tr.add_argument("--copper", "-c", type=float, default=1.0, help="Copper weight in oz (default: 1.0 oz / 35 um)")
    p_tr.add_argument("--internal", action="store_true", help="Set if trace is in an internal layer")

    args = parser.parse_args()

    if args.command == "junction":
        tj = calculate_junction_temp(args.ambient, args.power, args.rja)
        print(f"Ambient Temperature:   {args.ambient:.1f} °C")
        print(f"Power Dissipation:     {args.power:.3f} W")
        print(f"Thermal Resistance:    {args.rja:.1f} °C/W")
        print(f"Estimated Junction Tj: {tj:.1f} °C")
        if tj > 105:
            print("WARNING: Junction temperature exceeds 105°C! Thermal throttling or failure likely.", file=sys.stderr)
        elif tj > 85:
            print("CAUTION: Junction temperature exceeds 85°C. Consider adding thermal vias or heatsinking.")
        else:
            print("STATUS: Thermal margin is safe (Tj <= 85°C).")

    elif args.command == "heatsink":
        rsa = calculate_required_heatsink(args.max_tj, args.ambient, args.power, args.rjc, args.rcs)
        print(f"Power: {args.power:.2f} W | Max Tj: {args.max_tj:.1f} °C | Ambient: {args.ambient:.1f} °C")
        if rsa <= 0:
            print("CRITICAL: Package cannot dissipate this power even with an ideal infinite heatsink!", file=sys.stderr)
        else:
            print(f"Required Heatsink R_theta_sa: <= {rsa:.2f} °C/W")

    elif args.command == "trace":
        w_mm, w_mils = ipc2152_trace_width(args.current, args.rise, args.copper, args.internal)
        layer_type = "Internal" if args.internal else "External"
        print(f"Layer Type:      {layer_type}")
        print(f"Current:         {args.current:.2f} A")
        print(f"Allowed Rise:    {args.rise:.1f} °C")
        print(f"Copper Weight:   {args.copper:.1f} oz")
        print(f"Min Trace Width: {w_mm:.3f} mm ({w_mils:.1f} mils)")

if __name__ == "__main__":
    main()
