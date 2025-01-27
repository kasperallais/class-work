import networkx as nx
from collections import deque

# Breadth First Search Algorithm 
def bfs(graph, start):
    visited = set()
    distances = {}
    parent = {}
    traversal_order = []

    visited.add(start)
    distances[start] = 0
    parent[start] = None

    queue = deque([start])

    while queue:
        node = queue.popleft()
        traversal_order.append(node)
    
        for neighbor in sorted(graph[node]):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                distances[neighbor] = distances[node] + 1
                parent[neighbor] = node

    return traversal_order, distances, parent

#Initialize the graph
graph = nx.Graph()

# Input
start_node = int(input())
num_edges = int(input())
for edge in range(num_edges):
    edge = input().split(':')
    node1 = int(edge[0])
    node2 = int(edge[1])
    graph.add_edge(node1, node2)

# Perform BFS
traversal_order, distances, parent = bfs(graph, start_node)

#Output
print("Traversal:")
print(" ".join(map(str, traversal_order)))

print("Distances:")
for node in sorted(graph.nodes):
    print(f"Node {node}: {distances.get(node, 'inf')}")

print("Parents:")
for node in sorted(graph.nodes):
    print(f"Node {node}: {parent.get(node, 'None')}")
