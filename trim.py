"""Cut the blower-fan end off the backplate and shroud with one straight plane.

Both parts share the same Y axis (length of the card). The fan housing is at the
negative-Y end. Everything below CUT_Y is removed, the two long sides are clipped to straight
lines, and every cut is capped so the result is a closed, printable solid.

CUT_Y = -85: the PCB end is concave around the fan, and its longest corner (PCIe
side) reaches the backplate's end wall at Y = -84. Cutting at -85 keeps 1 mm of
that wall as an end stop.

At that Y the round fan opening in each part crosses the cut line, which would leave
a ~35 mm wide notch in the end. FILLS closes it with a floor-level block from the
cut to Y = -79, where each floor is continuous again, so the end is straight and solid.

Usage: python3 trim.py [cut_y]
Needs: pip install manifold3d trimesh numpy scipy networkx shapely mapbox_earcut
"""
import sys
from pathlib import Path

import manifold3d as mf
import numpy as np
import trimesh

CUT_Y = float(sys.argv[1]) if len(sys.argv) > 1 else -85.0
ROOT = Path(__file__).parent
OUT = ROOT / "trimmed"
OUT.mkdir(exist_ok=True)

FILL_TO_Y = -79.0  # both floors are continuous from here toward the PCB
# name -> (x_lo, x_hi, z_lo, z_hi) of the block that closes the fan-opening notch.
# Each block also covers the shallow dome on the outer face under the fan, so no
# pockets are left: the backplate block reaches the fan ring's top (z = -21), and the
# shroud block is wide enough to cover its dome and sits at the floor top next to the opening.
FILLS = {
    "backplate": (-207.0, -146.0, -27.85, -21.0),
    "shroud": (-86.0, -22.0, -34.5, -28.3),
}

for name in ("backplate", "shroud"):
    mesh = trimesh.load(ROOT / "original" / f"{name}.stl")
    # Keep the side the normal points to (+Y, the PCB section), cap the cut.
    cut = mesh.slice_plane(plane_origin=[0, CUT_Y, 0], plane_normal=[0, 1, 0], cap=True)
    cut.merge_vertices()
    # The outer side walls flare outward from about Y = -42 toward the fan (up to
    # 0.75 mm at the cut), and one stretch of edge sits 0.1 mm proud. Clip both long
    # sides to the straight edge measured near the far (bracket) end, so the outline
    # is a true rectangle. The inner wall faces are straight, so walls keep their
    # nominal thickness.
    far = mesh.section(plane_origin=[0, mesh.bounds[1, 1] - 30, 0], plane_normal=[0, 1, 0])
    x_min, x_max = far.vertices[:, 0].min(), far.vertices[:, 0].max()
    # Clip with a box using manifold3d: it handles the clip planes landing exactly
    # on existing wall faces, where trimesh's capping leaves sliver triangles.
    solid = mf.Manifold(mf.Mesh(vert_properties=np.asarray(cut.vertices, np.float32),
                                tri_verts=np.asarray(cut.faces, np.uint32)))
    if solid.status() != mf.Error.NoError:
        raise SystemExit(f"{name}: Y cut is not a valid solid ({solid.status()})")
    lo = np.array([x_min, CUT_Y - 1, mesh.bounds[0, 2] - 1])
    hi = np.array([x_max, mesh.bounds[1, 1] + 1, mesh.bounds[1, 2] + 1])
    box = mf.Manifold.cube(hi - lo).translate(lo)
    solid = solid ^ box
    if CUT_Y < FILL_TO_Y:
        x0, x1, z0, z1 = FILLS[name]
        f_lo, f_hi = np.array([x0, CUT_Y, z0]), np.array([x1, FILL_TO_Y, z1])
        solid = solid + mf.Manifold.cube(f_hi - f_lo).translate(f_lo)
    out = solid.to_mesh()
    cut = trimesh.Trimesh(out.vert_properties[:, :3], out.tri_verts)
    dst = OUT / f"{name}.stl"
    cut.export(dst)
    # Verify the file as written, not the in-memory mesh.
    check = trimesh.load(dst)
    if not check.is_watertight or len(check.split(only_watertight=False)) != 1:
        raise SystemExit(f"{name}: written STL is not a single watertight solid")
    ext = cut.extents
    print(f"{name}: {len(cut.faces)} faces, {ext[0]:.1f} x {ext[1]:.1f} x {ext[2]:.1f} mm, "
          f"watertight, volume {cut.volume / 1000:.1f} cm^3 -> {dst.relative_to(ROOT)}")
