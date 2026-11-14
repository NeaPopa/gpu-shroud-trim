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

`python3 trim.py [cut_y]` (needs `pip install trimesh numpy scipy networkx shapely mapbox_earcut`) writes
`trimmed/backplate.stl` and `trimmed/shroud.stl` (binary STL).

Both parts are cut at **Y = -66 mm**, where the straight PCB section ends: past that the outer walls start to flare
out and the fan housing begins. The backplate's PCB recess ends at about Y = -63, so the backplate keeps a ~3 mm end
wall. Both outputs are single watertight bodies, 200.9 mm long (was 300.3 mm), 98.8 mm wide.

| File | Extents (mm) | Faces |
|---|---|---|
| `trimmed/backplate.stl` | 98.8 × 200.9 × 16.3 | 4,140 |
| `trimmed/shroud.stl` | 98.8 × 200.9 × 36.2 | 4,754 |

To leave more length, pass a lower value, e.g. `python3 trim.py -75`. Anything below -66 keeps part of the fan flare.
