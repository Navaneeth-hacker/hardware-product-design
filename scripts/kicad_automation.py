"""
KiCad Headless Automation CLI Wrapper
Executes ERC, DRC, and fabrication exports (Gerbers, Drill, Centroid, STEP) via kicad-cli.
"""

import os
import sys
import subprocess
import argparse
import shutil

def find_kicad_cli():
    """Locate kicad-cli on system PATH or default Windows installation paths."""
    which_cli = shutil.which("kicad-cli")
    if which_cli:
        return which_cli

    # Search common Windows default paths
    candidates = [
        r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe",
        r"C:\Program Files\KiCad\8.0\bin\kicad-cli.exe",
        r"C:\Program Files\KiCad\7.0\bin\kicad-cli.exe",
        r"C:\Program Files (x86)\KiCad\8.0\bin\kicad-cli.exe"
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

def run_erc(kicad_cli: str, sch_path: str):
    """Run Electrical Rules Check (ERC)."""
    print(f"[ERC] Running Electrical Rules Check on: {sch_path}")
    cmd = [kicad_cli, "sch", "erc", "--severity-all", "--exit-code-violations", sch_path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print("[ERC] PASSED: Zero violations.")
        return True
    else:
        print("[ERC] FAILED: Violations detected:")
        print(res.stdout)
        print(res.stderr)
        return False

def run_drc(kicad_cli: str, pcb_path: str):
    """Run Design Rules Check (DRC)."""
    print(f"[DRC] Running Design Rules Check on: {pcb_path}")
    cmd = [kicad_cli, "pcb", "drc", "--severity-all", "--exit-code-violations", pcb_path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print("[DRC] PASSED: Zero violations.")
        return True
    else:
        print("[DRC] FAILED: Violations detected:")
        print(res.stdout)
        print(res.stderr)
        return False

def export_fab(kicad_cli: str, pcb_path: str, out_dir: str):
    """Export Gerbers, Drill files, Centroid, and STEP model."""
    os.makedirs(out_dir, exist_ok=True)
    gerber_dir = os.path.join(out_dir, "gerbers")
    os.makedirs(gerber_dir, exist_ok=True)

    print(f"[FAB] Exporting Gerbers to: {gerber_dir}")
    subprocess.run([kicad_cli, "pcb", "export", "gerbers", "-o", gerber_dir, pcb_path], check=True)

    print(f"[FAB] Exporting Excellon Drill files to: {gerber_dir}")
    subprocess.run([kicad_cli, "pcb", "export", "drill", "-o", gerber_dir, pcb_path], check=True)

    cpl_file = os.path.join(out_dir, "cpl.csv")
    print(f"[FAB] Exporting Component Placement (CPL) to: {cpl_file}")
    subprocess.run([kicad_cli, "pcb", "export", "pos", "--format", "csv", "--units", "mm", "-o", cpl_file, pcb_path], check=True)

    step_file = os.path.join(out_dir, "board.step")
    print(f"[FAB] Exporting 3D STEP solid to: {step_file}")
    subprocess.run([kicad_cli, "pcb", "export", "step", "--subst-models", "-o", step_file, pcb_path], check=True)

    print("[FAB] All fabrication deliverables exported successfully.")

def main():
    parser = argparse.ArgumentParser(description="KiCad Headless Verification & Export Automation")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_erc = subparsers.add_parser("erc", help="Run ERC on schematic")
    p_erc.add_argument("schematic", help="Path to .kicad_sch file")

    p_drc = subparsers.add_parser("drc", help="Run DRC on PCB")
    p_drc.add_argument("pcb", help="Path to .kicad_pcb file")

    p_fab = subparsers.add_parser("export", help="Export full manufacturing release")
    p_fab.add_argument("pcb", help="Path to .kicad_pcb file")
    p_fab.add_argument("--out", "-o", default="fab", help="Output directory (default: fab)")

    args = parser.parse_args()

    kicad_cli = find_kicad_cli()
    if not kicad_cli:
        print("ERROR: kicad-cli was not found in PATH or standard installation folders.", file=sys.stderr)
        print("Please install KiCad 8.x or 9.x and add kicad-cli to your system PATH.", file=sys.stderr)
        sys.exit(1)

    print(f"Using kicad-cli: {kicad_cli}")

    if args.command == "erc":
        success = run_erc(kicad_cli, args.schematic)
        sys.exit(0 if success else 1)
    elif args.command == "drc":
        success = run_drc(kicad_cli, args.pcb)
        sys.exit(0 if success else 1)
    elif args.command == "export":
        export_fab(kicad_cli, args.pcb, args.out)

if __name__ == "__main__":
    main()
