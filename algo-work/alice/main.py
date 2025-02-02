#!/usr/bin/env python3
"""
Solution for the Maze problem.
The maze is modeled as an explicit weighted directed graph using NetworkX.
Each vertex is a triple (r,c,s) indicating that Alice is in cell (r,c) with stride s.
An edge from (r,c,s) to (r',c',s') exists if from cell (r,c) with stride s one of the allowed moves
(with cost s) lands in (r',c') and, upon applying that cell’s effect (I, D, or N),
results in new stride s'. (A move is allowed only if it remains inside the maze.)
A super-goal vertex 'G' is added with zero‐weight edges from every vertex at the goal cell.
Then we use networkx’s dijkstra_path to find the shortest (lowest–energy) path.
"""

import sys
import networkx as nx

# --- Helper functions ---

def parse_input():
    """
    Parses the input from stdin.
    The first line is of the form:
       R C :: start_row start_col :: goal_row goal_col
    Each subsequent line describes one cell:
       row col :: <allowed directions> :: <effect>
    Returns (R, C, start, goal, cell_info) where cell_info is a dict mapping (r,c) -> (allowed, effect).
    """
    lines = sys.stdin.read().strip().splitlines()
    if not lines:
        sys.exit("Empty input")
    # Process first line:
    first_line = lines[0].strip()
    sections = first_line.split("::")
    if len(sections) != 3:
        sys.exit("Error in first line format")
    # First section: R C
    R, C = map(int, sections[0].strip().split())
    # Second section: start coordinates
    start_parts = sections[1].strip().split()
    start = (int(start_parts[0]), int(start_parts[1]))
    # Third section: goal coordinates
    goal_parts = sections[2].strip().split()
    goal = (int(goal_parts[0]), int(goal_parts[1]))
    
    # Process cell descriptions:
    cell_info = {}
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = line.split("::")
        if len(parts) != 3:
            continue  # skip malformatted lines
        r, c = map(int, parts[0].strip().split())
        allowed = parts[1].strip().split()
        effect = parts[2].strip()
        cell_info[(r, c)] = (allowed, effect)
    return R, C, start, goal, cell_info

def compute_max_stride_for_cell(r, c, R, C, allowed_dirs):
    """
    For a cell at (r,c) with allowed directions (unless the cell is marked "X"),
    compute the maximum positive integer s (stride) for which at least one allowed
    move is valid (i.e. lands inside the maze). (If allowed_dirs == ["X"], return 0.)
    """
    if allowed_dirs == ["X"]:
        return 0
    # Mapping from direction string to (dr, dc)
    dir_map = {
        'N': (-1, 0),
        'S': (1, 0),
        'E': (0, 1),
        'W': (0, -1),
        'NE': (-1, 1),
        'NW': (-1, -1),
        'SE': (1, 1),
        'SW': (1, -1)
    }
    max_stride = 0
    for d in allowed_dirs:
        if d not in dir_map:
            continue
        dr, dc = dir_map[d]
        # For a move to remain in bounds, we need:
        #   1 <= r + dr*s <= R   and   1 <= c + dc*s <= C.
        # If dr > 0 then s <= R - r; if dr < 0 then s <= r - 1; if dr==0 then no row constraint.
        # Likewise for dc.
        candidates = []
        if dr > 0:
            candidates.append(R - r)
        elif dr < 0:
            candidates.append(r - 1)
        if dc > 0:
            candidates.append(C - c)
        elif dc < 0:
            candidates.append(c - 1)
        if not candidates:
            s_max = 0
        else:
            s_max = min(candidates)
        if s_max > max_stride:
            max_stride = s_max
    return max_stride

# --- Main function ---

def main():
    R, C, start, goal, cell_info = parse_input()
    
    # Compute a global bound on stride.
    # For every cell that is not "X", compute its max stride; take the overall maximum.
    global_max_bound = 1
    for r in range(1, R+1):
        for c in range(1, C+1):
            if (r, c) not in cell_info:
                continue
            allowed, _ = cell_info[(r, c)]
            if allowed == ["X"]:
                # (Unless the cell is the goal, dead–ends are not used.)
                if (r, c) == goal:
                    continue
                else:
                    continue
            ms = compute_max_stride_for_cell(r, c, R, C, allowed)
            if ms > global_max_bound:
                global_max_bound = ms

    # Build the explicit graph.
    # Each vertex is a tuple (r, c, s).
    G = nx.DiGraph()
    
    # For every cell we add vertices:
    # For non-goal cells with allowed moves (i.e. not ["X"]), add all states (r,c,s)
    # for s = 1 to (cell’s max stride). For the goal cell (even if its allowed moves are "X"),
    # add states for s = 1 ... global_max_bound.
    for r in range(1, R+1):
        for c in range(1, C+1):
            if (r, c) not in cell_info:
                continue
            allowed, _ = cell_info[(r, c)]
            if (r, c) == goal:
                for s in range(1, global_max_bound + 1):
                    G.add_node((r, c, s))
            else:
                if allowed == ["X"]:
                    # Dead–end (unless it is the start; we add start separately)
                    continue
                ms = compute_max_stride_for_cell(r, c, R, C, allowed)
                for s in range(1, ms + 1):
                    G.add_node((r, c, s))
    # Ensure that the start vertex exists even if the start cell would otherwise be a dead–end.
    start_vertex = (start[0], start[1], 1)
    if start_vertex not in G.nodes:
        G.add_node(start_vertex)
    
    # Mapping for directions.
    dir_map = {
        'N': (-1, 0),
        'S': (1, 0),
        'E': (0, 1),
        'W': (0, -1),
        'NE': (-1, 1),
        'NW': (-1, -1),
        'SE': (1, 1),
        'SW': (1, -1)
    }
    
    # Now add edges.
    # From every vertex (r,c,s) that is not at the goal, for each allowed direction in that cell,
    # try to “jump” exactly s squares. If the destination (r+dr*s, c+dc*s) is in bounds then:
    #   let new_s = s+1 if the destination cell’s effect is "I", s-1 if "D", or s if "N".
    # If new_s < 1, skip. Also only add the edge if the destination vertex exists in our graph.
    for node in list(G.nodes):
        r, c, s = node
        if (r, c) == goal:
            continue  # do not add outgoing edges from the goal
        allowed, _ = cell_info[(r, c)]
        if allowed == ["X"]:
            continue
        for d in allowed:
            if d not in dir_map:
                continue
            dr, dc = dir_map[d]
            new_r = r + dr * s
            new_c = c + dc * s
            if not (1 <= new_r <= R and 1 <= new_c <= C):
                continue
            # Look up the destination cell’s effect.
            if (new_r, new_c) not in cell_info:
                continue
            _, dest_effect = cell_info[(new_r, new_c)]
            if dest_effect == "I":
                new_s = s + 1
            elif dest_effect == "D":
                new_s = s - 1
            else:
                new_s = s
            if new_s < 1:
                continue
            # Make sure the destination vertex exists.
            if (new_r, new_c) == goal:
                if new_s > global_max_bound:
                    continue
                dest_node = (new_r, new_c, new_s)
            else:
                dest_allowed, _ = cell_info[(new_r, new_c)]
                if dest_allowed == ["X"]:
                    continue
                ms_dest = compute_max_stride_for_cell(new_r, new_c, R, C, dest_allowed)
                if new_s > ms_dest:
                    continue
                dest_node = (new_r, new_c, new_s)
            if dest_node in G.nodes:
                # The weight of the edge is the stride length s.
                G.add_edge(node, dest_node, weight=s)
    
    # Add a super–goal vertex 'G' and connect every vertex corresponding to the goal cell to it with weight 0.
    G.add_node('G')
    for node in G.nodes:
        if node == 'G':
            continue
        if isinstance(node, tuple) and node[0:2] == goal:
            G.add_edge(node, 'G', weight=0)
    
    # If no start vertex, then no path.
    if start_vertex not in G.nodes:
        print("NO PATH")
        return

    # Run Dijkstra's algorithm.
    try:
        shortest_path = nx.dijkstra_path(G, start_vertex, 'G', weight='weight')
    except nx.NetworkXNoPath:
        print("NO PATH")
        return

    # Compute total cost (do not count the final zero–cost edge to 'G')
    total_cost = 0
    for i in range(len(shortest_path) - 1):
        u = shortest_path[i]
        v = shortest_path[i+1]
        if u == 'G' or v == 'G':
            continue
        total_cost += G[u][v]['weight']
    
    # The vertices on the path (except the super-goal) are of the form (r,c,s).
    # We output only the cell coordinates.
    cell_path = []
    for node in shortest_path:
        if node == 'G':
            continue
        cell_path.append((node[0], node[1]))
    
    # Output: first line: total_cost and the number of cells on the path.
    print(f"{total_cost} {len(cell_path)}")
    for r, c in cell_path:
        print(f"{r} {c}")

if __name__ == '__main__':
    main()

