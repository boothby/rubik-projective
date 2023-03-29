Projective View Rubik's Cube
============================

Node data is stored in `node_data.json`.  It contains fields:

1. `"node_labels"` -- each node has a label `[x, y, f]` where `x` and `y` are coordinates local to the face number `f`.
2. `"node_positions"` -- each node has a position `[x_c, y_c]` where `x_c` and `y_c` are cartesian coordinates.  This drawing kinda sucks right now.
3. `"axis0_move_cycles"` etc -- each axis as associated to 3 different "moves" that correspond to rotating a slice of the rubik's cube.  These are represented `[[u1, v1], [u2, v2], ..., [u12, v12]]` where applying a move in the forward direction goes `u1 -> v1`, `u2 -> v2`, etc.  Rotating in the reverse direction goes `v1 -> u1`, `v2 -> u2`, etc.
4. `"axis0_atomic_cycles"` etc -- similar to the move cycles, we define 3 different "atomic cycles" per axis.  Each is conceptually one third of a move cycle -- it can be used to make an animation for the move cycle of the same axis and index.

