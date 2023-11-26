import random
from random import randint
from typing import Tuple, List, Any


class LabyrinthGenerator:
    """The LabyrinthGenerator class generates a labyrinth using the depth-first search algorithm.
    """

    WALL_COLOR, PATH_COLOR = (0, 0, 0), (255, 255, 255)
    DIRECTIONS = [(0, 2), (0, -2), (-2, 0), (2, 0)]

    def __init__(self, width: int, height: int):
        """Initializes a LabyrinthGenerator object with the given width and height.

        Args:
        - width (int): The width of the labyrinth. If even, it will be increased by 1.
        - height (int): The height of the labyrinth. If even, it will be increased by 1.
        """
        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1

        self.width = width
        self.height = height

        start_x, start_y = randint(
            1, self.width - 2), randint(1, self.height - 2)
        if not start_x % 2:
            start_x += 1
        if not start_y % 2:
            start_y += 1

        self.frontier_cells = set()

        self.visited_cells = set()

        self.cells_to_draw = set()

        self.labyrinth = [
            [LabyrinthGenerator.WALL_COLOR if y % 2 + x % 2 < 2 else LabyrinthGenerator.PATH_COLOR for x in
             range(self.width)]
            for y in
            range(self.height)]

        self.visited_cells.add((start_y, start_x))
        self.cells_to_draw.add((start_y, start_x))
        self._add_unvisited_adjacent_cells(start_y, start_x)

    @staticmethod
    def _clamp(value: int, minimum: int, maximum: int) -> int:
        """Returns the given value clamped between the minimum and maximum values.

        Args:
        - value (int): The value to be clamped.
        - minimum (int): The minimum value that the result can be.
        - maximum (int): The maximum value that the result can be.

        Returns:
        - int: The clamped value.
        """
        return min(max(minimum, value), maximum)

    def _add_unvisited_adjacent_cells(self, row: int, column: int):
        """Adds unvisited adjacent cells to the frontier_cells set.

        Args:
        - row (int): The row of the cell to add adjacent cells to.
        - column (int): The column of the cell to add adjacent cells to.
        """
        for neighbor_offset in LabyrinthGenerator.DIRECTIONS:
            neighbor = (row + neighbor_offset[0], column + neighbor_offset[1])
            if self._within_bounds(neighbor[0], neighbor[
                1]) and neighbor not in self.visited_cells and neighbor not in self.frontier_cells and \
                    self.labyrinth[neighbor[0]][neighbor[1]] == LabyrinthGenerator.PATH_COLOR:
                self.frontier_cells.add(neighbor)

    def _get_visited_adjacent_cells(self, y: int, x: int) -> List[Tuple[int, int]]:
        """Returns a list of adjacent cells that have already been visited.

        Args:
        - y (int): The row of the cell to check for visited neighbors.
        - x (int): The column of the cell to check for visited neighbors.

        Returns:
        - List[Tuple[int, int]]: A list of the visited neighboring cells.
        """
        return [(y + o[0], x + o[1]) for o in LabyrinthGenerator.DIRECTIONS if
                (y + o[0], x + o[1]) in self.visited_cells]

    def _within_bounds(self, y: int, x: int) -> bool:
        """Returns True if the given cell is within the bounds of the labyrinth, False otherwise.

        Args:
        - y (int): The row of the cell to check for boundary.
        - x (int): The column of the cell to check for boundary.

        Returns:
        - bool: True if the cell is within the bounds of the labyrinth, False otherwise.
        """
        return 0 <= y < self.height and 0 <= x < self.width

    def get_labyrinth(self) -> List[List[Tuple[int, int, int]]]:
        """Returns the labyrinth as a list of lists of tuples, where each tuple is an RGB color code.

        Returns:
        - List[List[Tuple[int, int, int]]]: The labyrinth as a list of RGB color code tuples.
        """
        return self.labyrinth

    def get_frontier_cells(self) -> set[Any]:
        """Returns the frontier_cells set.

        Returns:
        - set[Any]: The set of frontier cells.
        """
        return self.frontier_cells

    def get_cells_to_draw(self) -> set[tuple[int, int]]:
        """Returns the cells_to_draw set.

        Returns:
        - set[tuple[int, int]]: The set of cells to draw.
        """
        return self.cells_to_draw

    def get_cell_color(self, y: int, x: int) -> Tuple[int, int, int]:
        """Returns the RGB color code of the cell at the given row and column indices.

        Parameters:
        - y (int): The row of the cell to get the color of.
        - x (int): The column of the cell to get the color of.

        Returns:
        - Tuple[int, int, int]: The RGB color code of the cell at the given row and column indices.
        """
        return self.labyrinth[y][x]

    def work_one_step(self):
        """Performs one step of the labyrinth generation algorithm.

        Selects a cell randomly from the frontier_cells set, and connects it to a randomly chosen visited cell.
        The connected cells are added to the visited_cells set.

        Unvisited adjacent cells of the newly connected cell are added to the frontier_cells set.
        """
        self.cells_to_draw.clear()
        frontier_length = len(self.frontier_cells)
        if frontier_length == 0:
            return
        cell = self.frontier_cells.pop()
        nearby = self._get_visited_adjacent_cells(cell[0], cell[1])
        in_maze = random.choice(nearby)

        dy, dx = LabyrinthGenerator._clamp(
            cell[0] - in_maze[0], -1, 1), LabyrinthGenerator._clamp(cell[1] - in_maze[1], -1, 1)

        if dy != 0:
            self.labyrinth[in_maze[0] + dy][in_maze[1]
                                            ] = LabyrinthGenerator.PATH_COLOR
            self.cells_to_draw.add((in_maze[0] + dy, in_maze[1]))
        if dx != 0:
            self.labyrinth[in_maze[0]][in_maze[1] +
                                       dx] = LabyrinthGenerator.PATH_COLOR
            self.cells_to_draw.add((in_maze[0], in_maze[1] + dx))

        self.visited_cells.add(cell)
        self.cells_to_draw.add(cell)

        self._add_unvisited_adjacent_cells(cell[0], cell[1])
