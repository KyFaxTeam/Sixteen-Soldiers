"""best agent ai v5"""
import random
from typing import Dict, List
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier

DEPTH = 1
STDEV = 0.05
SLIGHTLY_STDEV = 0.01
TIE_BREAKING_CRITERIA = 1
CORNER_POSITIONS = ['c1', 'c5', 'g1', 'g5']

class Agent(BaseAgent):
    """Enhanced AI agent implementing minimax with loop avoidance, evaluation function"""

    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "IFRI"
        self.recent_move: Dict = {}

        # Initial weights
        self.params = {
            'W1': 0.4, 
            'W2': -0.3,
            'W3': 1.0,
            'CENTER_BONUS': 0.1,
            'CAPTURE_SOLDIER_BONUS': 0.5,
            'CORNERS_BONUS': 1.0
        }

        if self.params.get("OPPONENT") is None:
            self.params["OPPONENT"] = Soldier.RED if self.soldier_value == Soldier.BLUE \
                else Soldier.BLUE

    # ------------------------------------------------------------------------
    # BEST ACTION'S CHOICE SECTION
    # ------------------------------------------------------------------------

    def choose_action(self, board: Board) -> Dict:
        """
        Choose an action from valid moves using minimax algorithm with loop avoidance
        and time management.
        Args:
            board: Current game board state
        Returns:
            Chosen valid action for the soldier_value
        """
        valid_actions = board.get_valid_actions()
        if not valid_actions:
            return {}  # No moves => game over or pass scenario

        best_action = None
        best_score = float('-inf')
        same_score_actions = []

        for action in valid_actions:
            # if len(valid_actions) > 1 and self.is_looping_action(action):
            #     continue  # Skip actions that lead to loops

            simulated_board = self.simulate_action(board, action)
            score = self.minimax(simulated_board, depth=DEPTH, maximizing=False)

            if score > best_score:
                best_score = score
                best_action = action
                same_score_actions = [action]
            elif score == best_score:
                same_score_actions.append(action)

        # Tie-breaker if multiple actions have the same score
        if len(same_score_actions) > TIE_BREAKING_CRITERIA:
            best_action = self._best_action(board, same_score_actions)

        # Update history to avoid loops
        if best_action:
            self.update_move_history(best_action)

        # -- STREAMING PARAMETER ADAPTATION --
        # After we've chosen an action, try to adapt params on the fly.
        self.streaming_param_update(board)

        return best_action if best_action else random.choice(valid_actions)

    def _best_action(self, board: Board, actions: List[Dict]) -> Dict:
        """
        Tie-breaking function that prioritizes capturing moves.
        """
        random.shuffle(actions)  # Shuffle to ensure randomness among equals

        def tie_break_score(act):
            score = self.capture_bonus(act)
            score += self.reward_action_logic(board, act)
            if self.threatens_opponent(board, act):
                score += 0.2
            return score

        return max(actions, key=tie_break_score)

    def update_move_history(self, action: Dict):
        """
        Update the move history to track recent moves and avoid loops.
        Args:
            action: The action to add to the history
        """
        self.recent_move = action

    # ------------------------------------------------------------------------
    # STRATEGY SECTION
    # ------------------------------------------------------------------------

    def minimax(self, board: Board, depth: int, maximizing: bool) -> float:
        """
        Minimax algorithm with fixed depth for decision-making.
        Args:
            board: Current game board state
            depth: Depth of search
            maximizing: Boolean, True if maximizing player, False if minimizing
        Returns:
            Score of the board state
        """
        # Terminal check or max depth
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        valid_actions = board.get_valid_actions()
        if not valid_actions:  # No moves => use evaluation
            return self.evaluate_board(board)

        random.shuffle(valid_actions)

        if maximizing:
            return max(
                self.minimax(self.simulate_action(board, action), depth - 1, False)
                for action in valid_actions
            )

        return min(
            self.minimax(self.simulate_action(board, action), depth - 1, True)
            for action in valid_actions
        )

    # ------------------------------------------------------------------------
    # EVALUATION AND REWARD SECTION
    # ------------------------------------------------------------------------

    def threatens_opponent(self, board: Board, action: Dict) -> bool:
        """
        Check if this move threatens an opponent soldier.
        """
        simulated_board = self.simulate_action(board, action)
        neighbors = simulated_board.get_neighbors(action['to_pos'])
        return len(neighbors[self.params["OPPONENT"].name]) > 0

    def reward_action_logic(self, board: Board, action: Dict) -> float:
        """
        Some tie-break scoring logic:
        - Evaluate the number of empty neighbors (the more, the better).
        - Evaluate if the move is in a corner (maybe a smaller bonus).
        """
        # Simulate the board after the action
        simulated_board = self.simulate_action(board, action)
        neighbors = simulated_board.get_neighbors(action['to_pos'])

        empty_count = len(neighbors[Soldier.EMPTY.name])
        opponent_count = len(neighbors[self.params["OPPONENT"].name])
        corner_score = self.params['CORNERS_BONUS'] if action['to_pos'] in [
            'c1', 'c5', 'g1', 'g5'] else 0

        return (empty_count * self.params["W1"]) + \
            (opponent_count * self.params["W2"]) + \
                (corner_score * self.params["W3"])

    def capture_bonus(self, action: Dict) -> float:
        """
        Returns a bonus if the action is a soldier capture.
        You can tune the bonus value to make capturing more/less appealing.
        """
        if action['type'] == 'CAPTURE_SOLDIER':
            return self.params['CAPTURE_SOLDIER_BONUS']
        return 0.0

    def is_looping_action(self, action: Dict) -> bool:
        """
        Check if the new action simply reverses the immediately preceding move.
        This simpler check only compares the new move to the last move.
        """
        if not self.recent_move:
            return False

        return (
            action['from_pos'] == self.recent_move['to_pos']
            and action['to_pos'] == self.recent_move['from_pos']
        )

    def evaluate_board(self, board: Board) -> float:
        """
        Evaluate the desirability of a board state for the agent.
        Args:
            board: Current game board state
        Returns:
            Evaluation score
        """
        my_soldiers = board.count_soldiers(self.soldier_value)
        opponent_soldiers = board.count_soldiers(self.params["OPPONENT"])
        # Soldier advantage
        soldier_diff = my_soldiers - opponent_soldiers

        return soldier_diff

    # ------------------------------------------------------------------------
    # ACTIONS' SIMULATION SECTION
    # ------------------------------------------------------------------------

    def simulate_action(self, board: Board, action: Dict) -> Board:
        """
        Simulate the result of an action on the board.
        Args:
            board: Current game board state
            action: Action to simulate
        Returns:
            A new board object representing the state after the action
        """
        simulated_board = Board()
        simulated_board.battle_field = board.battle_field
        simulated_board.soldiers = board.soldiers.copy()
        simulated_board.last_action = board.last_action
        simulated_board.is_multiple_capture = board.is_multiple_capture

        if action['type'] == 'CAPTURE_SOLDIER':
            simulated_board.capture_soldier(action)
        else:
            simulated_board.move_soldier(action)

        return simulated_board

    # ------------------------------------------------------------------------
    # STREAMING PARAMETER ADAPTATION SECTION
    # ------------------------------------------------------------------------

    def streaming_param_update(self, board: Board):
        """
        Self-adaptive parameter control using evolutionary computation.
        Each parameter and its mutation rate evolve together.
        """
        # Step 1: Current parameters and fitness
        old_params = self.params.copy()
        old_fitness = self.get_short_term_fitness(board)

        # Step 2: Create new parameters via self-adaptive mutation
        new_params = {}
        mutation_rates = {k: STDEV for k in old_params}  # Default mutation rates

        for key, value in old_params.items():
            if isinstance(value, (int, float)):
                # Apply Gaussian mutation
                sigma = mutation_rates[key]
                new_value = value + random.gauss(0, sigma)

                # Ensure parameters remain within valid ranges if necessary
                if key in ['W1', 'W2', 'W3',
                'CENTER_BONUS', 'CAPTURE_SOLDIER_BONUS', 'CORNERS_BONUS']:
                    new_value = max(-2, min(new_value, 2)) # [-2, 2]

                new_params[key] = new_value

                # Self-adapt mutation rates (e.g., increase variability if stagnating)
                mutation_rates[key] *= (1.0 + random.gauss(0, SLIGHTLY_STDEV))
            else:
                # Keep non-numeric parameters (e.g., "OPPONENT") unchanged
                new_params[key] = value

        # Step 3: Evaluate new parameters
        self.params.update(new_params)
        new_fitness = self.get_short_term_fitness(board)

        # Step 4: Survivor selection
        if new_fitness >= old_fitness:
            # Accept new parameters if fitness improves
            print(f"Accepted new parameters: {new_params}, Fitness: {new_fitness}")
        else:
            # Revert to old parameters if fitness declines
            self.params.update(old_params)
            print(f"Reverted to old parameters: {old_params}, Fitness: {old_fitness}")

    def get_short_term_fitness(self, board: Board) -> float:
        """
        Fitness function to evaluate short-term performance.
        You can define this based on real-time metrics (e.g., board evaluation).
        """
        return self.evaluate_board(board)
