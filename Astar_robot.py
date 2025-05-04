import heapq
import math

class Node:
    def __init__(self, x, y, walkable=True):
        self.x = x
        self.y = y
        self.walkable = walkable
        self.g_score = float('inf')
        self.h_score = 0
        self.f_score = float('inf')
        self.parent = None

    def __lt__(self, other):
        return self.f_score < other.f_score

    def __eq__(self, other):
        return isinstance(other, Node) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

class Grid:
    def __init__(self, width, height, grid_data):
        self.width = width
        self.height = height
        self.nodes = {}
        for y in range(height):
            for x in range(width):
                walkable = grid_data[y][x] == '0'
                self.nodes[(x, y)] = Node(x, y, walkable)

    def get_node(self, x, y):
        return self.nodes.get((x, y))

    def get_neighbors(self, node):
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0),
                    (1, 1), (1, -1), (-1, -1), (-1, 1)]
        for dx, dy in directions:
            x, y = node.x + dx, node.y + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                neighbor = self.get_node(x, y)
                if neighbor and neighbor.walkable:
                    if abs(dx) == 1 and abs(dy) == 1:
                        if not self.get_node(node.x + dx, node.y).walkable or not self.get_node(node.x, node.y + dy).walkable:
                            continue
                    neighbors.append(neighbor)
        return neighbors

def euclidean_distance(a, b):
    return math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)

def reconstruct_path(node):
    path = []
    while node:
        path.append((node.x, node.y))
        node = node.parent
    return path[::-1]

def a_star(grid, start_pos, goal_pos):
    start_node = grid.get_node(*start_pos)
    goal_node = grid.get_node(*goal_pos)

    if not start_node or not goal_node or not start_node.walkable or not goal_node.walkable:
        return []

    start_node.g_score = 0
    start_node.h_score = euclidean_distance(start_node, goal_node)
    start_node.f_score = start_node.h_score

    open_set = []
    heapq.heappush(open_set, start_node)
    open_set_hash = {start_node}
    closed_set = set()

    while open_set:
        current = heapq.heappop(open_set)
        open_set_hash.remove(current)

        if current == goal_node:
            return reconstruct_path(current)

        closed_set.add(current)

        for neighbor in grid.get_neighbors(current):
            if neighbor in closed_set:
                continue

            is_diagonal = abs(neighbor.x - current.x) == 1 and abs(neighbor.y - current.y) == 1
            movement_cost = 1.4 if is_diagonal else 1.0
            tentative_g_score = current.g_score + movement_cost

            if neighbor not in open_set_hash or tentative_g_score < neighbor.g_score:
                neighbor.parent = current
                neighbor.g_score = tentative_g_score
                neighbor.h_score = euclidean_distance(neighbor, goal_node)
                neighbor.f_score = neighbor.g_score + neighbor.h_score

                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, neighbor)
                    open_set_hash.add(neighbor)

    return []

def display_grid(grid, path, start_pos, goal_pos):
    print("\n Grid Visualization:")
    for y in range(grid.height):
        row = ''
        for x in range(grid.width):
            pos = (x, y)
            node = grid.get_node(x, y)
            if pos == start_pos:
                row += 'S '
            elif pos == goal_pos:
                row += 'E '
            elif pos in path:
                row += '* '
            elif not node.walkable:
                row += 'O '
            else:
                row += '. '
        print(row)
    print()

def main():
    print("A* Robot Navigation")
    width = int(input("Enter grid width: "))
    height = int(input("Enter grid height: "))

    print("\nEnter grid row by row (use '0' for empty, '1' for obstacle):")
    grid_data = []
    for i in range(height):
        while True:
            row = input(f"Row {i}: ")
            if len(row) == width and all(c in '01' for c in row):
                grid_data.append(row)
                break
            print(f"Invalid input. Must be {width} characters of '0' or '1'.")

    grid = Grid(width, height, grid_data)

    while True:
        try:
            start_x, start_y = map(int, input("\nEnter Start (x,y): ").split(','))
            if 0 <= start_x < width and 0 <= start_y < height:
                break
            print("Invalid start coordinates.")
        except ValueError:
            print("Enter as x,y")

    while True:
        try:
            goal_x, goal_y = map(int, input("Enter Goal (x,y): ").split(','))
            if 0 <= goal_x < width and 0 <= goal_y < height:
                break
            print("Invalid goal coordinates.")
        except ValueError:
            print("Enter as x,y")

    path = a_star(grid, (start_x, start_y), (goal_x, goal_y))

    if path:
        print(f"\n Path found with {len(path)-1} steps:")
        for i, (x, y) in enumerate(path):
            print(f"Step {i}: ({x}, {y})")
    else:
        print("\nNo path found!")

    display_grid(grid, set(path), (start_x, start_y), (goal_x, goal_y))

if __name__ == "__main__":
    main()


