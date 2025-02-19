import sys
import networkx as nx

def main():
    # Read input from standard input and split into individual lines
    data = sys.stdin.read().strip().splitlines()
    if not data:
        return

    # Parse the first line which provides the maze dimensions, start, and goal.
    # Format is "R C :: start_r start_c :: goal_r goal_c""
    # R and C: number of rows and columns of the maze
    # start_r, start_c: coordinates of the starting cell
    # goal_r, goal_c: coordinates of the goal cell
    first_line = data[0].strip()
    parts = [p.strip() for p in first_line.split("::")]
    if len(parts) < 3:
        print("NO PATH")
        return

    try:
        # Maze dimensions
        R, C = map(int, parts[0].split())
        # Starting cell coordinates
        start_r, start_c = map(int, parts[1].split())
        # Goal cell coordinates
        goal_r, goal_c = map(int, parts[2].split())
    except Exception:
        print("NO PATH")
        return

    # Parse the subsequent lines that provide cell-specific information
    # Format is "row col :: allowed_directions :: effect"
    # allowed_directions: list of directions
    # effect: "I", "D", or "N"
    # Build out maze info that maps each cell to a tuple (list of allowed directions, effect value)
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

    # If the starting cell is not in the maze, there is no valid path.
    if (start_r, start_c) not in maze_info:
        print("NO PATH")
        return

    # Determine the initial state for Alice
    # Initial stride is adjusted by the cell's effect
    _, start_effect = maze_info[(start_r, start_c)]
    init_stride = 1 + start_effect
    if init_stride < 1:
        print("NO PATH")
        return
    start_state = (start_r, start_c, init_stride)

    # Define mapping from direction strings to their corresponding row and column deltas
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

    # Build the explicit graph representation of the maze
    # Vertices:
    #   - Each vertex represents a state (r, c, stride), where:
    #       - (r, c) is the cell location
    #       - stride is the number of cells Alice will move from that cell
    # Edges:
    #   - A directed edge from vertex A to vertex B exists if:
    #       - There is an allowed movement from cell A in one of it's permitted directions
    #       - Alice can move exactly stride cells in that direction
    edge_list = []
    for (r, c), (directions, _) in maze_info.items():
        # If the only allowed direction is "X", then no moves can be made from this cell.
        if len(directions) == 1 and directions[0] == "X":
            continue
        for d in directions:
            if d == "X" or d not in dir_map:
                continue
            dr, dc = dir_map[d]
            # Determine the maximum number of steps possible in the given direction without leaving the maze boundaries
            if dr > 0:
                max_s_row = R - r # Moving downwards: Max steps limited by bottom edge
            elif dr < 0:
                max_s_row = r - 1 # Moving upwards: Max steps limited by top edge
            else:
                max_s_row = float('inf') # No vertical movement
            if dc > 0:
                max_s_col = C - c # Moving right: max steps limited by right edge
            elif dc < 0:
                max_s_col = c - 1 # Moving left: max steps limited by left edge
            else:
                max_s_col = float('inf') # No horizontal movement
            s_max_possible = int(min(max_s_row, max_s_col))
            # For every possible stride length from 1 to s_max_possible, create an edge
            for s in range(1, s_max_possible + 1):
                nr = r + s * dr # New row after moving s steps
                nc = c + s * dc # New column after moving s steps
                # Only consider moves that land on a valid cell in the maze
                if (nr, nc) not in maze_info:
                    continue
                # Retrieve the effect of the destination cell and update the stride accordingly
                _, dest_effect = maze_info[(nr, nc)]
                new_stride = s + dest_effect
                # Skip transitions that would result in non-positive stride
                if new_stride < 1:
                    continue
                # Add an edge
                #   - From: (r, c, s) represents leaving cell (r, c) with stride s
                #   - To: (nr, nc, new_stride) represents landing on cell (nr, nc) with updated stride
                #   - Weight: s (the stride length)
                edge_list.append(((r, c, s), (nr, nc, new_stride), s))

    # Create a graph using NetworkX
    G = nx.DiGraph()
    # Add the start state as a node in the graph
    G.add_node(start_state)
    # Add all the computed edges to the graph
    if edge_list:
        G.add_weighted_edges_from(edge_list)

    # Use Dijkstra's algorithm to find the shortest path from the start state.
    try:
        distances, paths = nx.single_source_dijkstra(G, start_state)
    except Exception:
        print("NO PATH")
        return

    # Among the reached vertices, select those that are at the goal cell coordinates
    goal_candidates = [(state, cost) for state, cost in distances.items()
                       if state[0] == goal_r and state[1] == goal_c]
    # If no state at the goal is reached, then there is no valid path
    if not goal_candidates:
        print("NO PATH")
        return

    # Choose the goal candidate with the smallest total cost
    best_state, best_distance = min(goal_candidates, key=lambda x: x[1])
    best_path = paths[best_state]  
    # Extract only cell coordinates from the path
    coord_path = [(r, c) for (r, c, s) in best_path]

    # Output the results
    print(f"{best_distance} {len(coord_path)}")
    for (r, c) in coord_path:
        print(f"{r} {c}")

if __name__ == "__main__":
    main()

