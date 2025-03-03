from collections import defaultdict

def build_residual_graph():

    rows, cols = map(int, input().split())  

    source = rows + cols  #Source
    sink = rows + cols + 1  #Sink

    residual_graph = defaultdict(lambda: defaultdict(int))  # Default both directions to 0
    #What does entry u,v in the residual_graph represent?

    # Create the residual graph
    # There are two bugs in the code below
    for r in range(rows):
        row = input().strip()
        for c in range(cols):   
            if row[c] == '.':
                residual_graph[r][rows + c] = 1
    
    for r in range(rows):
        residual_graph[source][r] = 1

    for c in range(cols):
        residual_graph[rows + c][sink] = 1  

    return residual_graph, source, sink

def dfs(residual_graph, u, visited, parent, sink):
    visited.add(u)

    if u == sink: #stop once we find the sink
        return True  # Found augmenting path

    for v, capacity in residual_graph[u].items():
        if v not in visited and capacity > 0:
            parent[v] = u
            if dfs(residual_graph, v, visited, parent, sink):
                return True

    return False

def max_flow(residual_graph, source, sink):
 
    max_flow_value = 0

    #keep track of dfs path
    parent = defaultdict(lambda:-1)

    while dfs(residual_graph, source, set(), parent, sink):
        flow = 10**9
        v = sink

        while v != source:
            u = parent[v]
            flow = min(flow, residual_graph[u][v])
            v = u

        v = sink
        while v != source:
            u = parent[v]
            residual_graph[u][v] -= flow
            residual_graph[v][u] += flow
            v = u

        max_flow_value += flow

    return max_flow_value

if __name__ == '__main__':
    #Create the Graph and Print the Max Number of Rooks
    residual_graph, source, sink = build_residual_graph()
    result = max_flow(residual_graph, source, sink)
    print(result)
