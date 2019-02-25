
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.currentState.state == self.victoryCondition:
            return True
        potential_moves = self.gm.getMovables()
        child_depth = self.currentState.depth + 1
        next_move = False
        while not next_move:
            i = self.currentState.nextChildToVisit
            if len(potential_moves) <= i:
                if self.currentState.parent:
                    self.gm.reverseMove(self.currentState.requiredMovable)
                    potential_moves = self.gm.getMovables()
                    self.currentState = self.currentState.parent
                    child_depth = self.currentState.depth + 1
                    continue
                else:
                    return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.currentState.state == self.victoryCondition:
            return True
        depth = self.currentState.depth
        move_at_depth = False
        while self.currentState.parent:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            i = self.currentState.nextChildToVisit
            if len(self.currentState.children) > i:
                move_at_depth = True
                break
        if not move_at_depth:
            for state in self.visited.keys():
                state.nextChildToVisit = 0
            depth += 1
            if len(self.visited) == 1:
                potential_moves = self.gm.getMovables()
                for move in potential_moves:
                    self.gm.makeMove(move)
                    new_state = GameState(self.gm.getGameState(), depth, move)
                    new_state.parent = self.currentState
                    self.visited[new_state] = False
                    self.currentState.children.append(new_state)
                    self.gm.reverseMove(move)
        while depth != self.currentState.depth:
            i = self.currentState.nextChildToVisit
            self.currentState.nextChildToVisit += 1
            if len(self.currentState.children) > i:
                self.currentState = self.currentState.children[i]
                test_move = self.currentState.requiredMovable
                self.gm.makeMove(test_move)
            else:
                move_at_depth = False
                while self.currentState.parent:
                    self.gm.reverseMove(self.currentState.requiredMovable)
                    self.currentState = self.currentState.parent
                    if len(self.currentState.children) > self.currentState.nextChildToVisit:
                        move_at_depth = True
                        break
                if not move_at_depth:
                    return False
        if self.currentState.state == self.victoryCondition:
            return True
        else:
            self.visited[self.currentState] = True
            potential_moves = self.gm.getMovables()
            child_depth = depth + 1
            for move in potential_moves:
                self.gm.makeMove(move)
                new_state = GameState(self.gm.getGameState(), child_depth, move)
                if new_state not in self.visited:
                    self.visited[new_state] = False
                    new_state.parent = self.currentState
                    self.currentState.children.append(new_state)
                self.gm.reverseMove(move)
            return False