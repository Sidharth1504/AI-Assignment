import copy

class EightPuzzle:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.rows, self.cols = 3, 3

    def print_state(self, state):
        for row in state:
            print(row)
        print()

    def get_blank_position(self, state):
        for i in range(self.rows):
            for j in range(self.cols):
                if state[i][j] == 0:
                    return i, j

    def manhattan_distance(self, state):
        distance = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if state[i][j] != 0:  
                    for x in range(self.rows):
                        for y in range(self.cols):
                            if self.goal_state[x][y] == state[i][j]:
                                distance += abs(x - i) + abs(y - j)
        return distance

    def get_neighbors(self, state):
        neighbors = []
        x, y = self.get_blank_position(state)
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]  
        for dx, dy in moves:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.rows and 0 <= new_y < self.cols:
                new_state = copy.deepcopy(state)
                new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
                neighbors.append(new_state)
        return neighbors

    def hill_climbing(self):
        current_state = self.initial_state
        current_heuristic = self.manhattan_distance(current_state)

        while True:
            print("Current State:")
            self.print_state(current_state)
            print(f"Heuristic Value: {current_heuristic}\n")

            if current_state == self.goal_state:
                print("Goal State Reached!")
                return True

            neighbors = self.get_neighbors(current_state)
            best_neighbor = None
            best_heuristic = float('inf')

            for neighbor in neighbors:
                heuristic = self.manhattan_distance(neighbor)
                if heuristic < best_heuristic:
                    best_neighbor = neighbor
                    best_heuristic = heuristic

            if best_heuristic >= current_heuristic:
                print("Stuck at local maxima or plateau.")
                return False

            current_state = best_neighbor
            current_heuristic = best_heuristic

if __name__ == "__main__":
    initial_state = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 8, 5]
    ]  

    goal_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    puzzle = EightPuzzle(initial_state, goal_state)
    success = puzzle.hill_climbing()

    if not success:
        print("Failed to reach the goal state.")

