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
