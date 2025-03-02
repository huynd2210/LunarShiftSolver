from flask import Flask, request, render_template, redirect, url_for
import sys
sys.setrecursionlimit(10000)

app = Flask(__name__)

# ------ Solver Functions ------

def parse_grid(grid_str):
    """
    Parse a grid string representation into a list-of-lists.
    Each row should have numbers (0 or 1) separated by spaces.
    """
    grid = []
    for line in grid_str.strip().splitlines():
        row = [int(cell) for cell in line.split()]
        grid.append(row)
    return grid

def grid_to_tuple(grid_list):
    """Convert a list-of-lists grid into a hashable tuple-of-tuples."""
    return tuple(tuple(row) for row in grid_list)

def is_target_state(g, target=0):
    """Return True if every cell in grid g equals the target value (default 0)."""
    return all(cell == target for row in g for cell in row)

def find_solution(grid, start, num_moves, target=0):
    """
    Find a sequence of moves from the given start coordinate (fixed as (0,0))
    so that after num_moves moves (each move flips the landing cell),
    the grid becomes solved (every cell equals target, default 0).

    This version uses an explicit transposition table to memoize intermediate results.
    It also prunes search branches where the number of cells not at the target value
    exceeds the number of moves left (deadend), and prints out:
      - The total transposition table hits
      - The total number of branches pruned
    """
    n = len(grid)
    m = len(grid[0])
    directions = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1)
    }

    start_grid = grid_to_tuple(grid)
    transposition_table = {}
    transposition_hits = [0]
    pruned_branches = [0]  # Counter for deadends pruned

    def dfs(r, c, grid_state, moves_left):
        key = (r, c, grid_state, moves_left)
        if key in transposition_table:
            transposition_hits[0] += 1
            return transposition_table[key]

        if moves_left == 0:
            result = [] if is_target_state(grid_state, target) else None
            transposition_table[key] = result
            return result

        # Deadend check: count the number of cells not at the target value.
        num_incorrect = sum(1 for row in grid_state for cell in row if cell != target)
        if num_incorrect > moves_left:
            pruned_branches[0] += 1
            transposition_table[key] = None
            return None

        # Convert the grid state tuple back into a mutable list-of-lists.
        current_grid = [list(row) for row in grid_state]

        for move, (dr, dc) in directions.items():
            nr, nc = r + dr, c + dc
            if not (0 <= nr < n and 0 <= nc < m):
                continue

            # Copy the current grid state.
            new_grid = [row[:] for row in current_grid]
            # Flip the value at the new cell.
            new_grid[nr][nc] = 1 - new_grid[nr][nc]
            new_grid_state = grid_to_tuple(new_grid)

            result = dfs(nr, nc, new_grid_state, moves_left - 1)
            if result is not None:
                transposition_table[key] = [move] + result
                return transposition_table[key]

        transposition_table[key] = None
        return None

    solution = dfs(start[0], start[1], start_grid, num_moves)
    print(f"Transposition table hits: {transposition_hits[0]}")
    print(f"Branches pruned (deadends): {pruned_branches[0]}")
    return solution

def simulate_moves_history(grid, start, move_sequence):
    """
    Simulate the move sequence and record each board state.
    Returns a list of (description, grid_state) tuples.
    """
    directions = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1)
    }

    board = [row[:] for row in grid]
    history = [("Initial board state", [row[:] for row in board])]
    r, c = start
    n = len(board)
    m = len(board[0])

    for step, move in enumerate(move_sequence, start=1):
        dr, dc = directions[move]
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < m:
            r, c = nr, nc
            board[r][c] = 1 - board[r][c]
            history.append((f"After move {step} ('{move}')", [row[:] for row in board]))
        else:
            history.append((f"Move {step} ('{move}') out-of-bounds (state unchanged)", [row[:] for row in board]))
    return history

# ------ Flask Routes ------

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/solve", methods=["POST"])
def solve():
    grid_str = request.form.get("grid", "").strip()
    if not grid_str:
        return render_template("result.html", error="Grid data is required!", solution=None)

    try:
        grid = parse_grid(grid_str)
    except Exception as e:
        return render_template("result.html", error=f"Error parsing grid: {e}", solution=None)

    # Retrieve the number of moves; default to 15 if missing or invalid.
    moves_input = request.form.get("moves", "").strip()
    try:
        moves = int(moves_input) if moves_input != "" else 15
    except ValueError:
        moves = 15

    # Use default starting position (0,0) and target value 0.
    start = (0, 0)
    target = 0

    solution = find_solution(grid, start, moves, target=target)

    if solution is None:
        return render_template("result.html", error=None, solution=None)
    else:
        simulation = simulate_moves_history(grid, start, solution)
        return render_template("result.html", error=None, solution=solution, simulation=simulation)

if __name__ == "__main__":
    app.run(debug=True)
