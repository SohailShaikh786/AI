import matplotlib.pyplot as plt
import networkx as nx


def is_valid(assignment, var, value, neighbors):
    for neighbor in neighbors.get(var, []):
        if neighbor in assignment and assignment[neighbor] == value:
            return False
    return True


def backtrack(assignment, variables, domains, neighbors):
    if len(assignment) == len(variables):
        return assignment

    unassigned = [v for v in variables if v not in assignment]
    var = unassigned[0]

    for value in domains[var]:
        if is_valid(assignment, var, value, neighbors):
            assignment[var] = value
            result = backtrack(assignment, variables, domains, neighbors)
            if result:
                return result
            del assignment[var]

    return None


def take_input():
    variables = input("Enter region names (separated by space): ").split()
    colors = input("Enter available colors (separated by space): ").split()

    domains = {var: colors[:] for var in variables}

    neighbors = {}
    print("\nDefine neighbors for each region (enter as space-separated neighbors or 'none'):")
    for var in variables:
        entry = input(f"Neighbors of {var}: ").strip()
        if entry.lower() != "none":
            neighbors[var] = entry.split()
        else:
            neighbors[var] = []

    return variables, domains, neighbors


def visualize_map(variables, neighbors, solution):
    G = nx.Graph()

   
    for var in variables:
        G.add_node(var)

    for var, neighbor_list in neighbors.items():
        for neighbor in neighbor_list:
            G.add_edge(var, neighbor)

    node_colors = [solution.get(node, 'gray') for node in G.nodes()]

    pos = nx.spring_layout(G, seed=42)  
    nx.draw(G, pos, with_labels=True, node_color=node_colors,
            node_size=1000, font_weight='bold')
    plt.title("Map Coloring Visualization")
    plt.show()


if __name__ == "__main__":
    print(" MAP COLORING CSP SOLVER WITH VISUALIZATION")
    variables, domains, neighbors = take_input()
    solution = backtrack({}, variables, domains, neighbors)

    print("\n Result:")
    if solution:
        for region in variables:
            print(f"{region}: {solution[region]}")
        visualize_map(variables, neighbors, solution)
    else:
        print(" No valid coloring found.")
