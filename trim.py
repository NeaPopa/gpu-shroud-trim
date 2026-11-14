"""Cut the blower-fan end off the backplate and shroud with one straight plane.

Both parts share the same Y axis (length of the card). The fan housing is at the
negative-Y end. Everything below CUT_Y is removed, the two long sides are clipped to straight
lines, and every cut is capped so the result is a closed, printable solid.

CUT_Y = -66 is where the straight PCB section ends on both parts: past it the
outer walls start to flare out and the fan housing features begin (Y <= -67).
The backplate's PCB recess ends around Y = -63, so -66 leaves a ~3 mm end wall.

Usage: python3 trim.py [cut_y]
Needs: pip install manifold3d trimesh numpy scipy networkx shapely mapbox_earcut
"""
import sys
from pathlib import Path

import manifold3d as mf
import numpy as np
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
    out = (solid ^ box).to_mesh()
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
