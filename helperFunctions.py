from typing import Tuple, List, Union
import heapq


def manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x1 - x2) + abs(y1 - y2)


def map_scale(x: float, a: float, b: float, c: float, d: float) -> float:
    return (x - a) / (b - a) * (d - c) + c


def find_path(start: Tuple[int, int], goal: Tuple[int, int], map_grid: List[List[Tuple[int, int, int]]]) -> Union[List[Tuple[int, int]], bool]:
    closed_set = set()
    open_set = [(0, start)]
    g_scores = {start: 0}
    came_from = {}
    h_scores = {start: manhattan_distance(
        start[1], start[0], goal[1], goal[0])}
    f_scores = {start: h_scores[start]}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            return reconstruct_path(came_from, goal)
        closed_set.add(current)
        for neighbor in get_neighbors(current, map_grid):
            if neighbor in closed_set or map_grid[neighbor[0]][neighbor[1]] != (255, 255, 255):
                continue
            tentative_g_score = g_scores[current] + 1
            if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                came_from[neighbor] = current
                g_scores[neighbor] = tentative_g_score
                h_scores[neighbor] = manhattan_distance(
                    neighbor[1], neighbor[0], goal[1], goal[0])
                f_scores[neighbor] = g_scores[neighbor] + h_scores[neighbor]
                heapq.heappush(open_set, (f_scores[neighbor], neighbor))
    return False


def get_neighbors(coord: Tuple[int, int], map_grid: List[List[Tuple[int, int, int]]]) -> List[Tuple[int, int]]:
    offsets = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    return [(coord[0] + offset[0], coord[1] + offset[1]) for offset in offsets if 0 <= coord[1] + offset[1] < len(map_grid[0]) and 0 <= coord[0] + offset[0] < len(map_grid)]


def reconstruct_path(came_from: dict, current_node: tuple) -> list:
    path = [current_node]
    while current_node in came_from:
        current_node = came_from[current_node]
        path.append(current_node)
    return path[::-1]
