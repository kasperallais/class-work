import sys
import networkx as nx

def main():
    # read the entire input
    lines = sys.stdin.read().strip().splitlines()
    if not lines:
        return

    # parse the first line
    first_line = lines[0].strip()
    parts = [p.strip() for p in first_line.split("::")]
    if len(parts) < 3:
        print("NO PATH")
        return

    try:
        R, C = map(int, parts[0].split())
        start_r, start_c = map(int, parts[1].split())
        goal_r, goal_c = map(int, parts[2].split())
    except Exception:
        print("NO PATH")
        return

    # parse cell descriptions
    maze_info = {}
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split("::")]
        if len(parts) < 3:
            continue
        try:
            r, c = map(int, parts[0].split())
        except Exception:
            continue
        directions_str = parts[1]
        directions = directions_str.split()
        effect_letter = parts[2]
        # map letters to integers
        if effect_letter == "I":
            effect_val = 1
        elif effect_letter == "D":
            effect_val = -1
        else:
            effect_val = 0
        maze_info[(r, c)] = (directions, effect_val)

    # build the explicit weighted directed graph
    # the veritices are tuples (r, c, s) - cell coordinates and current stride
    # an edge from (r, c, S) to (nr, nc, s') exists if from cell (r, c) with stide s
    # an allowed move in one of the cell's directions lands on (nr, nc) and updates stride to s'
    # the weight on that edge is s
    G = nx.DiGraph()
    
    # ensure that the start state is in the graph
    start_state = (start_r, start_c, 1)
    G.add_node(start_state)
    
    # define direction mappings
    dir_map = {
        "N":  (-1,  0),
        "S":  ( 1,  0),
        "E":  ( 0,  1),
        "W":  ( 0, -1),
        "NE": (-1,  1),
        "NW": (-1, -1),
        "SE": ( 1,  1),
        "SW": ( 1, -1)
    }
    
    # for each cell in the grid, add edges corresponding to every allowed move from that cell and for every stride value that would keep the direction in bounds
    for r in range(1, R+1):
        for c in range(1, C+1):
            if (r, c) not in maze_info:
                continue
            directions, _ = maze_info[(r, c)]
            # "X" means no allowed moves from that cell.
            if len(directions) == 1 and directions[0] == "X":
                continue
            for d in directions:
                if d not in dir_map:
                    continue
                dr, dc = dir_map[d]
                if dr > 0:
                    max_s_row = R - r
                elif dr < 0:
                    max_s_row = r - 1
                else:
                    max_s_row = float('inf')
                if dc > 0:
                    max_s_col = C - c
                elif dc < 0:
                    max_s_col = c - 1
                else:
                    max_s_col = float('inf')
                s_max_possible = int(min(max_s_row, max_s_col))
                for s in range(1, s_max_possible + 1):
                    nr = r + s * dr
                    nc = c + s * dc
                    if not (1 <= nr <= R and 1 <= nc <= C):
                        continue
                    if (nr, nc) not in maze_info:
                        continue
                    _, dest_effect = maze_info[(nr, nc)]
                    new_stride = s + dest_effect
                    if new_stride < 1:
                        continue
                    G.add_edge((r, c, s), (nr, nc, new_stride), weight=s)

    
    # use dijkstra's
    try:
        distances, paths = nx.single_source_dijkstra(G, start_state)
    except Exception:
        print("NO PATH")
        return

    goal_candidates = [(v, d) for v, d in distances.items() if v[0] == goal_r and v[1] == goal_c]
    if not goal_candidates:
        print("NO PATH")
        return

    best_state, best_distance = min(goal_candidates, key=lambda x: x[1])
    best_path = paths[best_state]
    
    coord_path = [(r, c) for (r, c, s) in best_path]

    # output
    print(f"{best_distance} {len(coord_path)}")
    for (r, c) in coord_path:
        print(f"{r} {c}")

if __name__ == "__main__":
    main()

