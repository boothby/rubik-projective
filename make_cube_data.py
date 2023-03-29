#
# 0     1
#    5
#   4 3
#
#    2
#

import networkx as nx
from math import pi, sin, cos, sqrt
import json
def face_pos(dim):
    def radius(x, y, f):
        if f > 2:
            return x + y + 1
        else:
            return 4*dim - (x + y)
    def angle(x, y, f):
        if f > 2:
            base = 2 * f * pi / 3 + pi
            offset = x-y
        else:
            base = 2 * f * pi / 3
            offset = y-x
        return base + pi * offset / dim / 6

    return {
        (x, y, f): (r*sin(a), r*cos(a))
        for x in range(dim)
        for y in range(dim)
        for f in range(6)    
        for (r, a) in [(radius(x, y, f), angle(x, y, f))]
    }

def cube_face_graph(dim):
    rotation_cycles = [
        [
            (0, 1, 'y', 1),
            (5,-1, 'y',-1),
            (3,-1, 'x', 1),
            (2, 1, 'x',-1),
        ],
        [
            (1, 1, 'y', 1),
            (3,-1, 'y',-1),
            (4,-1, 'x', 1),
            (0, 1, 'x',-1),
        ],
        [
            (2, 1, 'y', 1),
            (4,-1, 'y',-1),
            (5,-1, 'x', 1),
            (1, 1, 'x',-1),
        ],
    ]

    edges = []
    for rot_axis, rot_cycle in enumerate(rotation_cycles):
        last_f, last_dw, last_face_axis, last_dz = rot_cycle[-1]
        for f, dw, face_axis, dz in rot_cycle:
            last_off_coord = dim-1 if last_dz == 1 else 0
            off_coord = 0 if dz == 1 else dim-1
            last_axis_coords = range(dim)[::last_dw]
            axis_coords = range(dim)[::dw]
            if last_face_axis == 'y':
                last_sites = [(c, last_off_coord) for c in last_axis_coords]
            else:
                last_sites = [(last_off_coord, c) for c in last_axis_coords]
            if face_axis == 'y':
                sites = [(c, off_coord) for c in axis_coords]
            else:
                sites = [(off_coord, c) for c in axis_coords]
            edges.extend((ls + (last_f,), s + (f,), rot_axis) for ls, s in zip(last_sites, sites))

            if dz == 1:
                Z = [*zip(range(dim-1), range(1, dim))]
            else:
                Z = [*zip(range(1, dim), range(dim-1))]
            for w in range(dim):
                if face_axis == 'y':
                    edges.extend(((w, z0, f), (w, z1, f), rot_axis) for z0, z1 in Z)
                else:
                    edges.extend(((z0, w, f), (z1, w, f), rot_axis) for z0, z1 in Z)

            last_f, last_dw, last_face_axis, last_dz = f, dw, face_axis, dz

    D = nx.DiGraph()
    for u, v, a in edges:
        D.add_edge(u, v, axis=a)
    return D
        
def moves(n, C = None):
    if C is None:
        C = cube_face_graph(n)
    axes = [[], [], []]
    for u, v, d in C.edges(data=True):
        axes[d['axis']].append((u, v))
    axis_graphs = [nx.DiGraph(a) for a in axes]
    base_cycles = [
        [[e[0] for e in nx.find_cycle(g.subgraph(c))] for c in nx.strongly_connected_components(g)]
        for g in axis_graphs
    ]
    assert all(len(c[0]) == 4*n for c in base_cycles)
    move_cycles = [
        [[(c[i], c[(i+n)%(4*n)]) for i in range(4*n)] for c in axis_cycles]
        for axis_cycles in base_cycles
    ]
    atomic_cycles = [
        [[(c[i], c[(i+1)%(4*n)]) for i in range(4*n)] for c in axis_cycles]
        for axis_cycles in base_cycles
    ]
    return atomic_cycles, move_cycles

if __name__ == '__main__':
    C = cube_face_graph(3)
    pos = face_pos(3)
    atomic_cycles, move_cycles = moves(3, C)
    
    int_label = dict(map(reversed, enumerate(C)))
    
    plot_data = {
        "node_labels": list(C),
        "node_positions": [pos[v] for v in C.nodes],
        "axis0_atomic_cycles": [[[int_label[u], int_label[v]] for u, v in cycle] for cycle in atomic_cycles[0]],
        "axis1_atomic_cycles": [[[int_label[u], int_label[v]] for u, v in cycle] for cycle in atomic_cycles[1]],
        "axis2_atomic_cycles": [[[int_label[u], int_label[v]] for u, v in cycle] for cycle in atomic_cycles[2]],

        "axis0_move_cycles": [[[int_label[u], int_label[v]] for u, v in cycle] for cycle in move_cycles[0]],
        "axis1_move_cycles": [[[int_label[u], int_label[v]] for u, v in cycle] for cycle in move_cycles[1]],
        "axis2_move_cycles": [[[int_label[u], int_label[v]] for u, v in cycle] for cycle in move_cycles[2]],    
    }
    
    with open("board_data.json", "w") as outfile:
        json.dump(plot_data, outfile)
