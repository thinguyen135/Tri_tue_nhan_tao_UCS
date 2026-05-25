from collections import deque
import tkinter as tk
from tkinter import ttk
import random
import heapq

goal = (
    1, 2, 3,
    4, 5, 6,
    7, 8, 0
)

moves = {
    "Left": -1,
    "Right": 1,
    "Up": -3,
    "Down": 3
}


class Node:
    def __init__(self, state, parent=None, action=None, step=0, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.step = step
        self.cost = cost


def goal_test(state):
    return state == goal


def valid_actions(state):
    i = state.index(0)
    actions = []

    if i % 3 != 0:
        actions.append("Left")
    if i % 3 != 2:
        actions.append("Right")
    if i >= 3:
        actions.append("Up")
    if i <= 5:
        actions.append("Down")

    return actions


def swap(state, action):
    state = list(state)
    i_0 = state.index(0)
    new_0 = i_0 + moves[action]

    swapped_tile = state[new_0]
    state[i_0], state[new_0] = state[new_0], state[i_0]

    return tuple(state), swapped_tile


def misplaced_tiles(state):
    count = 0
    for i in range(9):
        if state[i] != 0 and state[i] != goal[i]:
            count += 1
    return count


def child_node(node, action, use_cost=False):
    new_state, _ = swap(node.state, action)

    if use_cost:
        step_cost = misplaced_tiles(new_state)
        new_cost = node.cost + step_cost
    else:
        new_cost = node.cost

    return Node(
        state=new_state,
        parent=node,
        action=action,
        step=node.step + 1,
        cost=new_cost
    )


def solution(node):
    steps = []
    states = []
    costs = []

    while node is not None:
        states.append(node.state)
        costs.append(node.cost)

        if node.action is not None:
            steps.append(node.action)

        node = node.parent

    states.reverse()
    steps.reverse()
    costs.reverse()

    return steps, states, costs


def format_state(state):
    return (
        f"[{state[0]} {state[1]} {state[2]}]\n"
        f"[{state[3]} {state[4]} {state[5]}]\n"
        f"[{state[6]} {state[7]} {state[8]}]"
    )


def format_log_state(state):
    return format_state(state).replace("\n", " | ")


# ===================== BFS =====================

def bfs(initial_state):
    logs = []
    node = Node(initial_state)

    frontier = deque([node])
    frontier_states = {node.state}
    explored = set()

    logs.append("=== BFS SEARCH LOG ===")
    logs.append(f"Initial State: {format_log_state(initial_state)}")

    while frontier:
        node = frontier.popleft()
        frontier_states.remove(node.state)

        logs.append("\n--------------------------------")
        logs.append(f"Đang xét node ở step = {node.step}")
        logs.append(format_state(node.state))

        if goal_test(node.state):
            logs.append("=> Tìm thấy trạng thái đích!")
            steps, states, costs = solution(node)
            return steps, states, costs, logs

        explored.add(node.state)

        for action in valid_actions(node.state):
            child = child_node(node, action)

            new_zero = child.state.index(0)
            swapped_tile = node.state[new_zero]

            logs.append(f"\n  Thử move {action}:")
            logs.append(f"  Hoán đổi 0 với {swapped_tile}")
            logs.append(f"  Trạng thái tạo ra: {format_log_state(child.state)}")

            if child.state in explored:
                logs.append("  -> Bỏ qua: đã xét.")
            elif child.state in frontier_states:
                logs.append("  -> Bỏ qua: đã có trong frontier.")
            else:
                logs.append("  -> Thêm vào frontier.")
                frontier.append(child)
                frontier_states.add(child.state)

    return None


# ===================== DFS =====================

def dfs(initial_state):
    logs = []
    node = Node(initial_state)

    frontier = [node]
    frontier_states = {node.state}
    explored = set()

    logs.append("=== DFS SEARCH LOG ===")
    logs.append(f"Initial State: {format_log_state(initial_state)}")

    while frontier:
        node = frontier.pop()
        frontier_states.remove(node.state)

        logs.append("\n--------------------------------")
        logs.append(f"Đang xét node ở step = {node.step}")
        logs.append(format_state(node.state))

        if goal_test(node.state):
            logs.append("=> Tìm thấy trạng thái đích!")
            steps, states, costs = solution(node)
            return steps, states, costs, logs

        explored.add(node.state)

        for action in reversed(valid_actions(node.state)):
            child = child_node(node, action)

            new_zero = child.state.index(0)
            swapped_tile = node.state[new_zero]

            logs.append(f"\n  Thử move {action}:")
            logs.append(f"  Hoán đổi 0 với {swapped_tile}")
            logs.append(f"  Trạng thái tạo ra: {format_log_state(child.state)}")

            if child.state in explored:
                logs.append("  -> Bỏ qua: đã xét.")
            elif child.state in frontier_states:
                logs.append("  -> Bỏ qua: đã có trong stack.")
            else:
                logs.append("  -> Thêm vào stack.")
                frontier.append(child)
                frontier_states.add(child.state)

    return None


# ===================== UCS =====================

def ucs(initial_state):
    logs = []

    # Cost ban đầu = 0
    node = Node(
        state=initial_state,
        cost=0
    )

    frontier = []
    counter = 0

    heapq.heappush(frontier, (node.cost, counter, node))

    frontier_costs = {
        node.state: node.cost
    }

    explored = set()

    logs.append("=== UCS SEARCH LOG ===")
    logs.append(f"Initial State: {format_log_state(initial_state)}")
    logs.append("Cost ban đầu = 0")

    while frontier:
        current_cost, _, node = heapq.heappop(frontier)

        if node.state in explored:
            continue

        logs.append("\n--------------------------------")
        logs.append(f"Đang xét node ở step = {node.step}")
        logs.append(format_state(node.state))
        logs.append(f"Tổng cost hiện tại = {node.cost}")
        logs.append(f"Số ô khác goal = {misplaced_tiles(node.state)}")

        if goal_test(node.state):
            logs.append("=> Tìm thấy trạng thái đích!")
            steps, states, costs = solution(node)
            return steps, states, costs, logs

        explored.add(node.state)

        for action in valid_actions(node.state):
            child = child_node(node, action, use_cost=True)

            new_zero = child.state.index(0)
            swapped_tile = node.state[new_zero]
            state_cost = misplaced_tiles(child.state)

            logs.append(f"\n  Thử move {action}:")
            logs.append(f"  Hoán đổi 0 với {swapped_tile}")
            logs.append(f"  Trạng thái tạo ra: {format_log_state(child.state)}")
            logs.append(f"  Cost trạng thái này = {state_cost}")
            logs.append(f"  Tổng cost mới = {child.cost}")

            if child.state in explored:
                logs.append("  -> Bỏ qua: đã xét.")

            elif child.state not in frontier_costs or child.cost < frontier_costs[child.state]:
                counter += 1
                heapq.heappush(frontier, (child.cost, counter, child))
                frontier_costs[child.state] = child.cost
                logs.append("  -> Thêm vào priority queue.")

            else:
                logs.append("  -> Bỏ qua: cost không tốt hơn.")

    return None


# ===================== IDS =====================

def depth(node):
    return node.step


def is_cycle(node):
    current = node.parent

    while current is not None:
        if current.state == node.state:
            return True
        current = current.parent

    return False


def depth_limited_search(initial_state, limit):
    logs = []
    node = Node(initial_state)
    frontier = [node]

    logs.append(f"=== IDS LIMIT = {limit} ===")

    result = "failure"

    while frontier:
        node = frontier.pop()

        logs.append("\n--------------------------------")
        logs.append(f"Đang xét node ở depth = {node.step}")
        logs.append(format_state(node.state))

        if goal_test(node.state):
            logs.append("=> Tìm thấy trạng thái đích!")
            steps, states, costs = solution(node)
            return steps, states, costs, logs

        if depth(node) >= limit:
            logs.append("-> Cutoff vì đạt giới hạn độ sâu.")
            result = "cutoff"

        elif not is_cycle(node):
            for action in reversed(valid_actions(node.state)):
                child = child_node(node, action)

                new_zero = child.state.index(0)
                swapped_tile = node.state[new_zero]

                logs.append(f"\n  Thử move {action}:")
                logs.append(f"  Hoán đổi 0 với {swapped_tile}")
                logs.append(f"  Trạng thái tạo ra: {format_log_state(child.state)}")
                logs.append("  -> Thêm vào stack IDS.")

                frontier.append(child)

        else:
            logs.append("-> Bỏ qua vì bị lặp chu trình.")

    return result, logs


def iterative_deepening_search(initial_state, max_depth=50):
    all_logs = []

    for limit in range(max_depth + 1):
        result = depth_limited_search(initial_state, limit)

        if isinstance(result, tuple) and len(result) == 4:
            steps, states, costs, logs = result
            all_logs.extend(logs)
            return steps, states, costs, all_logs

        status, logs = result
        all_logs.extend(logs)

        if status != "cutoff":
            return "failure"

    return "failure"


# ===================== RANDOM STATE =====================

def generate_random_state():
    state = goal

    for _ in range(20):
        actions = valid_actions(state)
        action = random.choice(actions)
        state, _ = swap(state, action)

    return state


# ===================== GUI =====================

class EightPuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Puzzle Search Algorithms")

        self.current_state = generate_random_state()
        self.steps = []
        self.states = []
        self.costs = []
        self.index = 0

        title = tk.Label(
            root,
            text="8 Puzzle Solver: BFS - DFS - IDS - UCS",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        main_frame = tk.Frame(root)
        main_frame.pack(padx=10, pady=10)

        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, padx=10, sticky="n")

        self.board_frame = tk.Frame(left_frame)
        self.board_frame.pack()

        self.tiles = []

        for i in range(9):
            tile = tk.Label(
                self.board_frame,
                text="",
                width=5,
                height=2,
                font=("Arial", 28, "bold"),
                borderwidth=2,
                relief="ridge",
                bg="white"
            )
            tile.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.tiles.append(tile)

        control_frame = tk.Frame(left_frame)
        control_frame.pack(pady=10)

        tk.Label(
            control_frame,
            text="Algorithm:",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, padx=5)

        self.algorithm_box = ttk.Combobox(
            control_frame,
            values=["BFS", "DFS", "IDS", "UCS"],
            state="readonly",
            width=10,
            font=("Arial", 12)
        )
        self.algorithm_box.current(0)
        self.algorithm_box.grid(row=0, column=1, padx=5)

        self.random_button = tk.Button(
            control_frame,
            text="Tạo random",
            width=16,
            font=("Arial", 11, "bold"),
            command=self.generate_random
        )
        self.random_button.grid(row=1, column=0, padx=5, pady=8)

        self.solve_button = tk.Button(
            control_frame,
            text="Giải",
            width=16,
            font=("Arial", 11, "bold"),
            command=self.auto_solve
        )
        self.solve_button.grid(row=1, column=1, padx=5, pady=8)

        self.info = tk.Label(
            left_frame,
            text="",
            font=("Arial", 12),
            fg="blue"
        )
        self.info.pack(pady=5)

        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=1, padx=10, sticky="n")

        tk.Label(
            right_frame,
            text="Log xét trạng thái và hoán đổi",
            font=("Arial", 14, "bold")
        ).pack()

        self.log_text = tk.Text(
            right_frame,
            width=65,
            height=25,
            font=("Consolas", 9)
        )
        self.log_text.pack()

        result_frame = tk.Frame(root)
        result_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(
            result_frame,
            text="Kết quả từ trạng thái ban đầu đến đích",
            font=("Arial", 14, "bold")
        ).pack(anchor="w")

        self.result_text = tk.Text(
            result_frame,
            width=120,
            height=12,
            font=("Consolas", 10)
        )
        self.result_text.pack(fill="x")

        self.draw_board(self.current_state)
        self.info.config(text="Chọn thuật toán rồi bấm Auto Solve.")

    def draw_board(self, state):
        for i, value in enumerate(state):
            if value == 0:
                self.tiles[i].config(text="", bg="lightgray")
            else:
                self.tiles[i].config(text=str(value), bg="white")

    def generate_random(self):
        self.current_state = generate_random_state()

        self.steps = []
        self.states = []
        self.costs = []
        self.index = 0

        self.draw_board(self.current_state)

        self.log_text.delete("1.0", tk.END)
        self.result_text.delete("1.0", tk.END)

        self.info.config(text="Đã tạo trạng thái ngẫu nhiên.")

    def auto_solve(self):
        algorithm = self.algorithm_box.get()

        self.log_text.delete("1.0", tk.END)
        self.result_text.delete("1.0", tk.END)

        if algorithm == "BFS":
            result = bfs(self.current_state)
        elif algorithm == "DFS":
            result = dfs(self.current_state)
        elif algorithm == "IDS":
            result = iterative_deepening_search(self.current_state)
        elif algorithm == "UCS":
            result = ucs(self.current_state)
        else:
            self.info.config(text="Chưa chọn thuật toán.")
            return

        if result is None or result == "failure":
            self.info.config(text="Không tìm thấy lời giải.")
            return

        self.steps, self.states, self.costs, search_logs = result
        self.index = 0

        self.log_text.insert(tk.END, "\n".join(search_logs))
        self.log_text.insert(tk.END, "\n\n=== SOLUTION PATH ANIMATION ===\n\n")
        self.log_text.see(tk.END)

        self.random_button.config(state="disabled")
        self.solve_button.config(state="disabled")
        self.algorithm_box.config(state="disabled")

        self.show_result_path()
        self.show_step()

    def show_result_path(self):
        algorithm = self.algorithm_box.get()

        self.result_text.insert(tk.END, f"Thuật toán: {algorithm}\n")
        self.result_text.insert(tk.END, f"Tổng số bước đi: {len(self.steps)}\n")

        if algorithm == "UCS":
            self.result_text.insert(
                tk.END,
                f"Tổng chi phí UCS: {self.costs[-1]}\n"
            )

        self.result_text.insert(tk.END, "\nTrạng thái ban đầu:\n")
        self.result_text.insert(tk.END, format_state(self.states[0]))

        if algorithm == "UCS":
            self.result_text.insert(
                tk.END,
                f"\nCost ban đầu = {self.costs[0]}"
            )

        self.result_text.insert(tk.END, "\n\n")

        for i in range(1, len(self.states)):
            self.result_text.insert(
                tk.END,
                f"Step {i}: {self.steps[i - 1]}\n"
            )

            self.result_text.insert(tk.END, format_state(self.states[i]))

            if algorithm == "UCS":
                current_state_cost = misplaced_tiles(self.states[i])
                self.result_text.insert(
                    tk.END,
                    f"\nCost trạng thái = {current_state_cost}"
                    f"\nTổng cost = {self.costs[i]}"
                )

            self.result_text.insert(tk.END, "\n\n")

        self.result_text.insert(tk.END, "Đã tới trạng thái đích.\n")

    def show_step(self):
        if self.index < len(self.states):
            state = self.states[self.index]
            self.draw_board(state)

            algorithm = self.algorithm_box.get()

            if self.index == 0:
                self.info.config(
                    text=f"Initial State | Total moves: {len(self.steps)}"
                )

                self.log_text.insert(
                    tk.END,
                    f"Step 0 Solution: Initial State\n"
                    f"{format_state(state)}\n\n"
                )

            else:
                move = self.steps[self.index - 1]

                previous_state = self.states[self.index - 1]
                current_state = self.states[self.index]

                new_zero = current_state.index(0)
                swapped_tile = previous_state[new_zero]

                if algorithm == "UCS":
                    current_state_cost = misplaced_tiles(current_state)

                    self.info.config(
                        text=f"Step {self.index}/{len(self.steps)} | Move: {move} | Cost: {self.costs[self.index]}"
                    )

                    self.log_text.insert(
                        tk.END,
                        f"Step {self.index} Solution: Move {move}\n"
                        f"Hoán đổi 0 với {swapped_tile}\n"
                        f"Số ô khác goal = {current_state_cost}\n"
                        f"Tổng cost = {self.costs[self.index]}\n"
                        f"{format_state(current_state)}\n\n"
                    )

                else:
                    self.info.config(
                        text=f"Step {self.index}/{len(self.steps)} | Move: {move}"
                    )

                    self.log_text.insert(
                        tk.END,
                        f"Step {self.index} Solution: Move {move}\n"
                        f"Hoán đổi 0 với {swapped_tile}\n"
                        f"{format_state(current_state)}\n\n"
                    )

            self.log_text.see(tk.END)

            self.index += 1
            self.root.after(700, self.show_step)

        else:
            self.current_state = goal

            self.random_button.config(state="normal")
            self.solve_button.config(state="normal")
            self.algorithm_box.config(state="readonly")

            self.info.config(text="Đã giải xong!")


root = tk.Tk()
app = EightPuzzleApp(root)
root.mainloop()
