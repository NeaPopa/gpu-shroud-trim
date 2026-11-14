"""Cut the blower-fan end off the backplate and shroud with one straight plane.

Both parts share the same Y axis (length of the card). The fan housing is at the
negative-Y end. Everything below CUT_Y is removed and the cut is capped so the
result is a closed, printable solid.

CUT_Y = -66 is where the straight PCB section ends on both parts: past it the
outer walls start to flare out and the fan housing features begin (Y <= -67).
The backplate's PCB recess ends around Y = -63, so -66 leaves a ~3 mm end wall.

Usage: python3 trim.py [cut_y]
Needs: pip install trimesh numpy scipy networkx shapely mapbox_earcut
"""
import sys
from pathlib import Path

import trimesh

CUT_Y = float(sys.argv[1]) if len(sys.argv) > 1 else -66.0
ROOT = Path(__file__).parent
OUT = ROOT / "trimmed"
OUT.mkdir(exist_ok=True)

for name in ("backplate", "shroud"):
    mesh = trimesh.load(ROOT / "original" / f"{name}.stl")
    # Keep the side the normal points to (+Y, the PCB section), cap the cut.
    cut = mesh.slice_plane(plane_origin=[0, CUT_Y, 0], plane_normal=[0, 1, 0], cap=True)
    cut.merge_vertices()
    if not cut.is_watertight:
        raise SystemExit(f"{name}: result is not watertight")
    dst = OUT / f"{name}.stl"
    cut.export(dst)
    ext = cut.extents
    print(f"{name}: {len(cut.faces)} faces, {ext[0]:.1f} x {ext[1]:.1f} x {ext[2]:.1f} mm, "
          f"watertight, volume {cut.volume / 1000:.1f} cm^3 -> {dst.relative_to(ROOT)}")
