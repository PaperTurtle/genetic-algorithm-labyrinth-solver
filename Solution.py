import random

from helperFunctions import *


class Solution:
    """A class representing a solution to the labyrinth problem.
    """

    def __init__(self, init: tuple, end: tuple,
                 labyrinth, best_path: List[Tuple[int, int]]):
        """Initializes a Solution object.

        Args:
        - init (tuple): The starting position for the solution.
        - end (tuple): The target position for the solution.
        - labyrinth: The labyrinth object representing the maze.
        - best_path (List[Tuple[int, int]]): The best path to the end position.
        """
        self.fitness_score = 0
        self.possible_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.can_move = True
        self.has_reached_end = False
        self.path = [init]
        self.labyrinth = labyrinth
        self.end = end
        self.color = (random.randrange(0, 255), random.randrange(
            0, 255), random.randrange(0, 255), random.uniform(0, 1))
        self.best_path = best_path
        self.best_distance = len(best_path)

    def __str__(self) -> str:
        """Returns a string representation of the Solution object.

        Returns:
        - str: A string containing the path and fitness score of the solution.
        """
        return f"{self.path} Fitness: {self.fitness_score}"

    @staticmethod
    def _is_valid_position(y: int, x: int, maze_height: int, maze_width: int) -> bool:
        """Returns whether a given position is valid.

        Args:
        - y (int): The y-coordinate of the position.
        - x (int): The x-coordinate of the position.
        - maze_height (int): The height of the maze.
        - maze_width (int): The width of the maze.

        Returns:
        - bool: True if the position is valid, False otherwise.
        """
        return 0 <= x < maze_width and 0 <= y < maze_height

    def _get_new_position(self, d: tuple) -> tuple:
        """Returns the new position after moving in a given direction.

        Args:
        - d (tuple): A tuple representing the direction to move in.

        Returns:
        - tuple: A tuple representing the new position.
        """
        return self.path[-1][0] + d[0], self.path[-1][1] + d[1]

    def _is_valid_direction(self, d: tuple) -> bool:
        """Returns whether a given direction is valid.

        Args:
        - d (tuple): A tuple representing the direction to check.

        Returns:
        - bool: True if the direction is valid, False otherwise.
        """
        new_position = self._get_new_position(d)
        maze = self.labyrinth.get_labyrinth()
        return (self._is_valid_position(new_position[0], new_position[1], self.labyrinth.height, self.labyrinth.width)
                and maze[new_position[0]][new_position[1]] == (255, 255, 255)
                and new_position not in self.path)

    def move(self) -> None:
        """Moves the solution in a random valid direction.
        """
        if self.can_move:
            valid_directions = [
                d for d in self.possible_directions if self._is_valid_direction(d)]
            if valid_directions:
                self.path.append(self._get_new_position(
                    random.choice(valid_directions)))
                if self.path[-1] == self.end:
                    self.can_move = False
                    self.has_reached_end = True
            else:
                self.can_move = False

    def solve(self) -> None:
        """Attempts to solve the maze by repeatedly moving the solution until it reaches the end position.
        """
        while self.can_move:
            self.move()

    def evaluate(self) -> None:
        """Evaluates the fitness score of the solution based on its distance to the end position.
        """
        self.solve()
        last_position = self.path[-1]
        distance = (len(find_path(last_position, self.end, self.labyrinth.get_labyrinth()))
                    if not self.has_reached_end else 0)
        self.fitness_score = min(1, max(
            0, (self.best_distance ** 2 - distance ** 2) / (self.best_distance ** 2)))

    def crossover(self, partner: "Solution") -> "Solution":
        """Performs crossover with another Solution object to create a child solution.

        Args:
        - partner (Solution): The other Solution object to perform crossover with.

        Returns:
        - Solution: A child Solution object created through crossover.
        """
        child = Solution(self.path[0], self.end,
                         self.labyrinth, self.best_path)
        max_parent = max(self, partner, key=lambda x: x.fitness_score)
        index = int(len(max_parent.path) * 0.8)
        child.path = max_parent.path[:index]
        return child

    def mutate(self):
        self.path = self.path[:int(map_scale(random.random(), 0, 1, 1, len(self.path)))]
