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

Both parts are cut at **Y = -85 mm**. The PCB's fan end is concave (it wraps around the fan), so its corners reach
past the start of the fan ring: the longest corner (PCIe side) stops at the backplate's end wall at Y = -84. Cutting at
-85 keeps 1 mm of that wall as an end stop, and keeps the outer wall of the fan ring that the PCB's curved edge sits against.

Other changes, all so the end is straight and solid:

* **Fan opening filled.** At Y = -85 the round fan opening in each part crosses the cut line, which would leave a
  ~35 mm notch in the end. A floor-level block from the cut to Y = -79 closes it (backplate up to the ring top,
  z = -21; shroud up to the floor top next to the opening, z = -28.3). The blocks also cover the shallow dome on each
  part's outer face under the fan, so no pockets are left.
* **Side walls clipped straight.** The originals' outer walls flare outward toward the fan from about Y = -42, and one
  stretch of edge sits 0.1 mm proud. Both long sides are clipped to the straight edge measured at the bracket end. The
  inner wall faces were already straight, so walls keep their thickness. The only remaining feature on the edge is the
  original notch at Y = -25 to -5.

Both outputs are single watertight solids (checked on the written files), 219.9 mm long (was 300.3 mm), 97.9 mm wide.

| File | Extents (mm) | Faces |
|---|---|---|
| `trimmed/backplate.stl` | 97.9 × 219.9 × 16.3 | 4,808 |
| `trimmed/shroud.stl` | 97.9 × 219.9 × 36.2 | 9,428 |

The shroud keeps a short, thin piece of the blower's curved wall standing near the end (original geometry, about
8 mm long).
