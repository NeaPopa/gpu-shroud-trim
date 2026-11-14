# GPU shroud trim

Two printed parts that fit together around a GPU PCB:

| File | Extents (mm) | Notes |
|---|---|---|
| `original/backplate.stl` | 112.3 × 300.3 × 16.3 | ASCII STL, 12,792 faces, not watertight |
| `original/shroud.stl` | 112.3 × 300.3 × 36.3 | ASCII STL, 15,436 faces, not watertight |

The two parts share the same Y range (-165.31 to 134.94); in the files they sit side by side along X.

## Goal

Make both parts shorter, with a straight cut across the length (Y) axis, and remove the blower fan mount end
(the round fan housing). Keep only the part that covers the PCB. Both parts get cut at the same plane so they still
fit together. The cut faces must be closed (capped) so the result prints.

Outputs go to `trimmed/`.

## Result

`python3 trim.py [cut_y]` (needs `pip install manifold3d trimesh numpy scipy networkx shapely mapbox_earcut`) writes
`trimmed/backplate.stl` and `trimmed/shroud.stl` (binary STL).

Both parts are cut at **Y = -66 mm**, where the PCB section ends: past that the fan housing begins. The backplate's
PCB recess ends at about Y = -63, so the backplate keeps a ~3 mm end wall.

The outer side walls of the originals are not quite straight: from about Y = -42 they flare outward toward the fan
(0.75 mm by Y = -66), and one stretch of edge sits 0.1 mm proud. Both long sides are clipped to the straight edge
measured at the bracket end, so the outline is a true rectangle. The inner wall faces were already straight, so the
walls keep their thickness. The only remaining feature on the edge is the original notch at Y = -25 to -5.

Both outputs are single watertight solids (checked on the written files), 200.9 mm long (was 300.3 mm), 97.9 mm wide.

| File | Extents (mm) | Faces |
|---|---|---|
| `trimmed/backplate.stl` | 97.9 × 200.9 × 16.3 | 4,138 |
| `trimmed/shroud.stl` | 97.9 × 200.9 × 36.2 | 4,742 |

To leave more length, pass a lower value, e.g. `python3 trim.py -75`; the sides are still clipped straight.
