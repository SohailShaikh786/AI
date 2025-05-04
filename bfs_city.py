import heapq
import networkx as nx
import matplotlib.pyplot as plt

# Heuristic function: Manhattan Distance (can be replaced with a custom heuristic)
def heuristic(node, goal):
    return abs(node - goal)

# Best-First Search (BestFS)
def best_first_search(graph, source, goal, num_vertices):
    parent = [-1] * num_vertices
    distance = [float('inf')] * num_vertices
    pq = []
    heapq.heappush(pq, (heuristic(source, goal), source))  # (heuristic, node)
    distance[source] = 0

    while pq:
        _, node = heapq.heappop(pq)

        if node == goal:
            break

        for neighbor in graph[node]:
            if distance[neighbor] == float('inf'):  # Not visited yet
                parent[neighbor] = node
                distance[neighbor] = distance[node] + 1
                heapq.heappush(pq, (heuristic(neighbor, goal), neighbor))

    return parent, distance

# Reconstruct the path from source to destination
def reconstruct_path(parent, dest):
    path = []
    current = dest
    while current != -1:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path

# Visualize the graph and the shortest path
def visualize_graph(graph_adj_list, path):
    G = nx.Graph()

    for u in range(len(graph_adj_list)):
        for v in graph_adj_list[u]:
            G.add_edge(u, v)

    pos = nx.spring_layout(G)

    # Draw full graph
    nx.draw(G, pos, with_labels=True, node_color='lightgray', edge_color='gray', node_size=800, font_weight='bold')

    # Highlight the shortest path
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='skyblue')
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='blue', width=2)

    plt.title("Graph with Shortest Path Highlighted")
    plt.show()

# Function to print the shortest distance and path
def print_shortest_distance(graph, source, dest, num_vertices):
    parent, distance = best_first_search(graph, source, dest, num_vertices)

    if distance[dest] == float('inf'):
        print("❌ No path found between Source and Destination.")
        return

    path = reconstruct_path(parent, dest)

    print(f"\n✅ Shortest Path from {source} to {dest} (length {distance[dest]}):")
    print(" -> ".join(map(str, path)))

    visualize_graph(graph, path)

# Main driver code
if __name__ == "__main__":
    try:
        V = int(input("Enter the number of vertices: "))
        E = int(input("Enter the number of edges: "))

        graph = [[] for _ in range(V)]

        print("Enter the edges (format: u v):")
        for _ in range(E):
            u, v = map(int, input().split())
            if 0 <= u < V and 0 <= v < V:
                graph[u].append(v)
                graph[v].append(u)
            else:
                print("Invalid edge! Vertex out of range.")

        S = int(input("Enter source vertex: "))
        D = int(input("Enter destination vertex: "))

        if 0 <= S < V and 0 <= D < V:
            print_shortest_distance(graph, S, D, V)
        else:
            print("❌ Invalid source or destination vertex.")

    except ValueError:
        print("❌ Invalid input! Please enter integers only.")
