from typing import Tuple

import pygame

from LabyrinthGenerator import LabyrinthGenerator


class LabyrinthDisplay:
    """A class for displaying a labyrinth generated by a `LabyrinthGenerator`.
    """
    START_COLOR = (0, 255, 0)
    END_COLOR = (0, 255, 0)
    width: int = 100
    height: int = 100
    cell_size: int = 40
    title: str = ""
    display: pygame.Surface = None
    pixelArray: pygame.PixelArray = None
    maze: LabyrinthGenerator = None

    def __init__(self, title: str, width: int, height: int, block_size: int):
        """Initializes a new LabyrinthDisplay object with the specified parameters.

        Args:
        - title: A string that will be used as the window title.
        - width: An integer representing the width of the labyrinth (in cells).
        - height: An integer representing the height of the labyrinth (in cells).
        - block_size: An integer representing the size of each cell (in pixels).
        """
        self.title = title
        self.maze = LabyrinthGenerator(width, height)
        self.cell_size = block_size
        self.width = self.maze.width * self.cell_size
        self.height = self.maze.height * self.cell_size
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        self.pixelArray = pygame.PixelArray(self.display)

    def _draw_pixel(self, x_coordinate: int, y_coordinate: int, color: Tuple[int, int, int]):
        """Draws a single pixel with the specified color at the specified coordinates.

        Args:
        - x_coordinate: An integer representing the x-coordinate of the pixel to be drawn.
        - y_coordinate: An integer representing the y-coordinate of the pixel to be drawn.
        - color: A tuple of three integers representing the RGB color value of the pixel.
        """
        if 0 <= x_coordinate < self.width and 0 <= y_coordinate < self.height:
            self.pixelArray[x_coordinate, y_coordinate] = color

    def draw_rectangle(self, sx: int, sy: int, width: int, height: int, color: Tuple[int, int, int]):
        """Draws a rectangle with the specified dimensions and color.

        Args:
        - sx: An integer representing the x-coordinate of the top-left corner of the rectangle.
        - sy: An integer representing the y-coordinate of the top-left corner of the rectangle.
        - width: An integer representing the width of the rectangle (in pixels).
        - height: An integer representing the height of the rectangle (in pixels).
        - color: A tuple of three integers representing the RGB color value of the rectangle.
        """
        pygame.draw.rect(self.display, color, (sx, sy, width, height))
        pygame.display.update()

    def draw_labyrinth(self):
        """Draws the labyrinth on the screen using the current LabyrinthGenerator object.
        """
        generating_maze = True
        while generating_maze:
            pygame.time.Clock()
            for game_event in pygame.event.get():
                if game_event.type == pygame.QUIT:
                    generating_maze = False
                    break
            for y_coordinate, x_coordinate in self.maze.get_cells_to_draw():
                self.draw_rectangle(x_coordinate * self.cell_size, y_coordinate * self.cell_size,
                                    self.cell_size, self.cell_size,
                                    self.maze.get_cell_color(y_coordinate, x_coordinate))
            self.draw_rectangle(615, 615, self.cell_size,
                                self.cell_size, (124, 252, 0))
            if len(self.maze.frontier_cells) == 0:
                break
            pygame.display.update()
            self.maze.work_one_step()
