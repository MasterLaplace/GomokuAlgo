import math
import random
from enum import Enum
from game.game import Game

class Brain:
    class CommandType(Enum):
        UNKNOWN = 0
        ERROR = 1
        MESSAGE = 2
        DEBUG = 3
        SUGGEST = 4

    def __init__(self):
        self.name = "MonteCarloBrain"
        self.version = "0.1.0"
        self.author = "Enzotekrennes;MasterLaplace"
        self.country = "France"

    def start(self):
        print("OK - everything is good")

    def restart(self):
        pass

    def about(self):
        print(f"name=\"{self.name}\", version=\"{self.version}\", author=\"{self.author}\", country=\"{self.country}\"")

    @staticmethod
    def isMovesLeft(board: list[list[str]], size: tuple[int, int]) -> bool:
        for i in range(size[0]):
            for j in range(size[1]):
                if board[i][j] == Game.CaseSate.EMPTY:
                    return True
        return False

    @staticmethod
    def evaluate(board: list[list[str]], size: tuple[int, int]) -> Game.CaseSate:
        for i in range(size[0]):
            for j in range(size[1]):
                if j + 4 < size[1]:
                    if board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3] == board[i][j + 4]:
                        return Game.CaseSate.PLAYER1 if board[i][j] == Game.CaseSate.PLAYER1 else Game.CaseSate.PLAYER2
                if i + 4 < size[0]:
                    if board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j] == board[i + 4][j]:
                        return Game.CaseSate.PLAYER1 if board[i][j] == Game.CaseSate.PLAYER1 else Game.CaseSate.PLAYER2
                if i + 4 < size[0] and j + 4 < size[1]:
                    if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] == board[i + 4][j + 4]:
                        return Game.CaseSate.PLAYER1 if board[i][j] == Game.CaseSate.PLAYER1 else Game.CaseSate.PLAYER2
        return Game.CaseSate.EMPTY

    def findBestSolution(self, board: list[list[Game.CaseSate]], size: tuple[int, int]) -> tuple[int, int]:
        simulations = 1000
        root = Node(board, size)

        for _ in range(simulations):
            selected_node = self.selectAndExpand(root)
            simulation_result = self.simulate(selected_node)
            self.backpropagate(selected_node, simulation_result)

        best_child = max(root.children, key=lambda child: child.visits)
        return best_child.move

    def selectAndExpand(self, node: 'Node') -> 'Node':
        while not node.is_terminal() and node.is_fully_expanded():
            node = node.select_child()

        if not node.is_terminal():
            node = node.expand()

        return node

    def simulate(self, node: 'Node') -> int:
        simulation_board = [row.copy() for row in node.state]

        while True:
            result = Brain.evaluate(simulation_board, node.size)
            if result != Game.CaseSate.EMPTY:
                return 1 if result == Game.CaseSate.PLAYER1 else -1

            legal_moves = [(i, j) for i in range(node.size[0]) for j in range(node.size[1]) if simulation_board[i][j] == Game.CaseSate.EMPTY]
            if legal_moves:
                move = random.choice(legal_moves)
                simulation_board[move[0]][move[1]] = Game.CaseSate.PLAYER1
            else:
                return 0

    def backpropagate(self, node: 'Node', result: int):
        while node is not None:
            node.update(result)
            node = node.parent

class Node:
    def __init__(self, state: list[list[Game.CaseSate]], size: tuple[int, int], move: tuple[int, int] = None, parent: 'Node' = None):
        self.state = state
        self.size = size
        self.move = move
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def is_terminal(self) -> bool:
        return Brain.evaluate(self.state, self.size) != Game.CaseSate.EMPTY or not Brain.isMovesLeft(self.state, self.size)

    def is_fully_expanded(self) -> bool:
        return len(self.children) == len([(i, j) for i in range(self.size[0]) for j in range(self.size[1]) if self.state[i][j] == Game.CaseSate.EMPTY])

    def select_child(self) -> 'Node':
        exploration_constant = 1.0 / math.sqrt(2.0)
        return max(self.children, key=lambda child: (child.wins / child.visits) + exploration_constant * math.sqrt(math.log(self.visits) / child.visits))

    def expand(self) -> 'Node':
        legal_moves = [(i, j) for i in range(self.size[0]) for j in range(self.size[1]) if self.state[i][j] == Game.CaseSate.EMPTY]
        if legal_moves:
            move = random.choice(legal_moves)
            new_state = [row.copy() for row in self.state]
            new_state[move[0]][move[1]] = Game.CaseSate.PLAYER1
            child = Node(new_state, self.size, move, self)
            self.children.append(child)
            return child
        return self

    def update(self, result: int):
        self.visits += 1
        self.wins += result

