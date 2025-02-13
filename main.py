def parse_grid(grid_str):
    """
    Parse a grid string representation into a list-of-lists.

    The string should have rows separated by newline characters,
    and each row consists of numbers (0 or 1) separated by whitespace.

    Example:
        "0 1\n1 0"

    Returns:
        A list-of-lists grid, e.g., [[0, 1], [1, 0]]
    """
    grid = []
    for line in grid_str.strip().splitlines():
        row = [int(cell) for cell in line.split()]
        grid.append(row)
    return grid


def print_grid(grid):
    """
    Print the grid in a readable format.

    Each row is printed on a new line.
    """
    for row in grid:
        print(" ".join(str(cell) for cell in row))
    print()  # Blank line after the grid


def find_solution(grid, start, num_moves, target=0):
    """
    Find a sequence of moves (each one of "up", "down", "left", "right")
    such that, starting from the given 'start' coordinate and making
    num_moves moves (each move causing a flip in the landing cell),
    the grid becomes solved (every cell equals the target value).

    Parameters:
      grid: A list-of-lists representing your NxM grid.
      start: Tuple (row, col) as the starting coordinates.
      num_moves: The number of moves allowed.
      target: The target cell value (0 or 1) for a solved grid.

    Returns:
      A list of moves (strings) if a solution exists; otherwise None.
    """
    n = len(grid)
    m = len(grid[0])

    # Directions mapping
    directions = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1)
    }

    def is_target_state(g):
        """Return True if every cell in grid g equals the target value."""
        return all(cell == target for row in g for cell in row)

    def grid_to_tuple(grid_list):
        """Convert a list-of-lists grid into a tuple-of-tuples (immutable and hashable)."""
        return tuple(tuple(row) for row in grid_list)

    start_grid = grid_to_tuple(grid)

    from functools import lru_cache
    import sys
    sys.setrecursionlimit(10000)

    @lru_cache(maxsize=None)
    def dfs(r, c, grid_state, moves_left):
        if moves_left == 0:
            return [] if is_target_state(grid_state) else None

        current_grid = [list(row) for row in grid_state]

        for move, (dr, dc) in directions.items():
            nr, nc = r + dr, c + dc
            if not (0 <= nr < n and 0 <= nc < m):
                continue  # Skip out-of-bound moves

            new_grid = [row[:] for row in current_grid]
            # Flip the value on the destination cell.
            new_grid[nr][nc] = 1 - new_grid[nr][nc]

            new_grid_state = grid_to_tuple(new_grid)
            result = dfs(nr, nc, new_grid_state, moves_left - 1)
            if result is not None:
                return [move] + result

        return None

    return dfs(start[0], start[1], start_grid, num_moves)


def simulate_moves(grid, start, move_sequence):
    """
    Simulate applying the move sequence on the grid, printing the board state after each move.

    Parameters:
      grid: A list-of-lists representing the grid.
      start: Tuple (row, col) as the starting position.
      move_sequence: List of moves (each one "up", "down", "left", or "right").

    Returns:
      The final grid after applying all moves.
    """
    directions = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1)
    }

    final_grid = [row[:] for row in grid]
    r, c = start
    n = len(grid)
    m = len(grid[0])

    print("\nInitial board state:")
    print_grid(final_grid)

    for step, move in enumerate(move_sequence, start=1):
        dr, dc = directions[move]
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < m:
            r, c = nr, nc
            final_grid[r][c] = 1 - final_grid[r][c]
            print(f"After move {step} ('{move}'):")
            print_grid(final_grid)
        else:
            print(f"Move {step} ('{move}') is out-of-bounds. Skipping.")

    return final_grid


def read_grid_from_console():
    """
    Read grid rows from the console. The user types rows (numbers separated by spaces)
    and must enter an empty line when done.

    Returns:
      A 2D grid (list-of-lists) of integers.
    """
    print("Enter grid rows (numbers separated by spaces).")
    print("Press Enter on an empty line to finish.\n")

    grid_lines = []
    while True:
        line = input().strip()
        if line == "":
            break
        grid_lines.append(line)

    if not grid_lines:
        raise ValueError("No grid data entered.")

    grid_str = "\n".join(grid_lines)
    return parse_grid(grid_str)


def read_starting_position():
    """
    Prompt the user to enter the starting position as 'row col'.

    If the user provides no input (empty line), default to (0, 0).

    Returns:
      A tuple (row, col) representing the starting position.
    """
    print("Enter the starting position (row and column separated by a space) [default: 0 0]:")
    start_input = input().strip()
    if start_input == "":
        return (0, 0)

    parts = start_input.split()
    if len(parts) != 2:
        print("Invalid input. Defaulting to (0, 0).")
        return (0, 0)

    try:
        row, col = int(parts[0]), int(parts[1])
        return (row, col)
    except ValueError:
        print("Invalid numbers. Defaulting to (0, 0).")
        return (0, 0)


def read_number_of_moves():
    """
    Prompt the user to enter the number of moves allowed.

    If no input is given, default to 15 moves.

    Returns:
      An integer representing the number of moves.
    """
    print("Enter the number of moves allowed [default: 15]:")
    moves_input = input().strip()
    if moves_input == "":
        return 15

    try:
        return int(moves_input)
    except ValueError:
        print("Invalid input. Defaulting to 15 moves.")
        return 15


def read_target_value():
    """
    Prompt the user to enter the target value (0 or 1) for the grid to be solved.

    If no input is given, default to 0.

    Returns:
      0 or 1 representing the desired target state for each grid cell.
    """
    print("Enter the target value (0 or 1) for the grid to be solved [default: 0]:")
    target_input = input().strip()
    if target_input == "":
        return 0

    try:
        target_value = int(target_input)
        if target_value not in (0, 1):
            print("Target value must be 0 or 1. Defaulting to 0.")
            return 0
        return target_value
    except ValueError:
        print("Invalid input. Defaulting to 0.")
        return 0


def main():
    print("=== Grid Solver Console Program ===\n")

    try:
        grid = read_grid_from_console()
    except ValueError as e:
        print(e)
        return

    start = read_starting_position()
    moves = read_number_of_moves()
    target_value = read_target_value()

    print("\nSearching for a solution...")
    solution = find_solution(grid, start, moves, target=target_value)

    if solution is not None:
        print("\nSolution found!")
        print("\nSimulating moves:")
        simulate_moves(grid, start, solution)
        print("Sequence of moves:", solution)

    else:
        print(f"\nNo solution exists with {moves} moves to reach a grid of all {target_value}'s.")


if __name__ == "__main__":
    main()
