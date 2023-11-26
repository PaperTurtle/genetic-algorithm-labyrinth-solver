from Solution import *
import random
from heapq import nlargest


class GALabyrinthSolver:
    """
    A class for solving a labyrinth using a genetic algorithm.
    """
    ELITISM_RATE = 0.1
    population: List[Solution] = []
    best_population: List[Tuple[int, int]] = []
    found_solution: bool = False
    optimal_solution: Solution = None

    def __init__(self, generation: int, population_size: int, mutation_rate: float, initial_coords: Tuple[int, int],
                 end: Tuple[int, int], labyrinth):
        """
        Initializes an instance of GALabyrinthSolver class.

        Args:
            - generation (int): Number of generations to evolve.
            - population_size (int): Size of the population.
            - mutation_rate (float): Probability of mutation.
            - initial_coords (Tuple[int, int]): Initial coordinates.
            - end (Tuple[int, int]): Final coordinates.
            - labyrinth (Labyrinth): The Labyrinth instance to solve.

        """
        self.generation = generation
        self.previous_best_fitness = 0
        self.current_generation = 0
        self.no_improvement_streak = 0
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.init = initial_coords
        self.end = end
        self.best_population = find_path(
            initial_coords, end, labyrinth.get_labyrinth())
        self.initialize_population(initial_coords, end, labyrinth)

    def initialize_population(self, init: Tuple[int, int], end: Tuple[int, int], maze) -> None:
        """Initializes the population with solutions based on the best known path.

        Args:
            - init (Tuple[int, int]): Initial coordinates.
            - end (Tuple[int, int]): Final coordinates.
            - maze (List[List[int]]): The maze.
        """
        self.population = [Solution(init, end, maze, self.best_population)
                           for _ in range(self.population_size)]
        self._update_fitness_scores()

    def get_highest_fitness(self) -> float:
        return max(p.fitness_score for p in self.population)

    def _select_parent(self) -> Solution:
        tournament_size = int(len(self.population) * 0.2)  # Adjust the tournament size as needed
        tournament_subset = random.sample(self.population, tournament_size)
        best_individual = max(tournament_subset, key=lambda p: p.fitness_score)
        return best_individual

    def _select_parents(self) -> Tuple[Solution, Solution]:
        parentA = self._select_parent()
        parentB = self._select_parent()
        while parentA == parentB:  # Ensure two distinct parents are selected
            parentB = self._select_parent()
        return parentA, parentB

    def _update_fitness_scores(self) -> None:
        for individual in self.population:
            individual.evaluate()

    def _parent_selection_and_crossover(self) -> None:
        # Elitism: Select the top solutions to carry over to the next generation
        num_elites = int(self.ELITISM_RATE * self.population_size)
        elites = nlargest(num_elites, self.population,
                          key=lambda p: p.fitness_score)

        # Crossover the rest of the population
        new_population = elites
        while len(new_population) < self.population_size:
            parentA, parentB = self._select_parents()
            child = parentA.crossover(parentB)
            new_population.append(child)

        self.population = new_population

    def _random_mutation(self):
        for individual in self.population:
            if random.random() <= self.mutation_rate:
                individual.mutate()

    def create_next_generation(self) -> None:
        self.current_generation += 1
        self._parent_selection_and_crossover()
        self.update_mutation_rate()
        self._random_mutation()
        self._update_fitness_scores()
        self.update_elitism_rate()
        self.optimal_solution = max(
            self.population, key=lambda x: x.fitness_score)
        if self.optimal_solution.fitness_score == 1:
            self.found_solution = True 

    def update_elitism_rate(self):
        current_best_fitness = max(p.fitness_score for p in self.population)
        if current_best_fitness <= self.previous_best_fitness:
            self.no_improvement_streak += 1
        else:
            self.no_improvement_streak = 0

        if self.no_improvement_streak > 5:  
            self.ELITISM_RATE = min(0.5, self.ELITISM_RATE + 0.05)  
        else:
            self.ELITISM_RATE = max(0.1, self.ELITISM_RATE - 0.01)  

        self.previous_best_fitness = current_best_fitness

    def update_mutation_rate(self):
        current_best_fitness = max(p.fitness_score for p in self.population)
        if current_best_fitness <= self.previous_best_fitness:
            self.mutation_rate = min(1, self.mutation_rate * 1.05)
        else:
            self.mutation_rate = max(0.01, self.mutation_rate * 0.95)
        self.previous_best_fitness = current_best_fitness