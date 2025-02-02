import sys
import networkx as nx

def main():
    data = sys.stdin.read().strip().splitlines()
    if not data:
        return

    first_line = data[0].strip()
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

    maze_info = {}
    for line in data[1:]:
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
        directions = parts[1].split() 
        effect_letter = parts[2]
        if effect_letter == "I":
            effect_val = 1
        elif effect_letter == "D":
            effect_val = -1
        else:
            effect_val = 0
        maze_info[(r, c)] = (directions, effect_val)

    if (start_r, start_c) not in maze_info:
        print("NO PATH")
        return
    _, start_effect = maze_info[(start_r, start_c)]
    init_stride = 1 + start_effect
    if init_stride < 1:
        print("NO PATH")
        return
    start_state = (start_r, start_c, init_stride)

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

    edge_list = []
    for (r, c), (directions, _) in maze_info.items():
        if len(directions) == 1 and directions[0] == "X":
            continue
        for d in directions:
            if d == "X" or d not in dir_map:
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
                if (nr, nc) not in maze_info:
                    continue
                _, dest_effect = maze_info[(nr, nc)]
                new_stride = s + dest_effect
                if new_stride < 1:
                    continue
                edge_list.append(((r, c, s), (nr, nc, new_stride), s))

    G = nx.DiGraph()
    G.add_node(start_state)
    if edge_list:
        G.add_weighted_edges_from(edge_list)

    try:
        distances, paths = nx.single_source_dijkstra(G, start_state)
    except Exception:
        print("NO PATH")
        return

    goal_candidates = [(state, cost) for state, cost in distances.items()
                       if state[0] == goal_r and state[1] == goal_c]
    if not goal_candidates:
        print("NO PATH")
        return

    best_state, best_distance = min(goal_candidates, key=lambda x: x[1])
    best_path = paths[best_state]  
    coord_path = [(r, c) for (r, c, s) in best_path]

    print(f"{best_distance} {len(coord_path)}")
    for (r, c) in coord_path:
        print(f"{r} {c}")

if __name__ == "__main__":
    main()

