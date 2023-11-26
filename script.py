# ------------------------------- IMPORTS ---------------------------------------------------------#

import os
from typing import Tuple

import pygame
from pygame.locals import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.ticker import FormatStrFormatter
from sklearn.linear_model import LinearRegression

from LabyrinthDisplay import LabyrinthDisplay
from GALabyrinthSolver import GALabyrinthSolver

# ------------------------------- WINDOW TITLE FOR THE PYGAME ------------------------------------- #

WINDOW_TITLE: str = "Genetische Algorithmen - Labyrinthlöser"

# ------------------------------- VARIABLES FOR THE LABYRINTH ------------------------------------- #

CELL_SIZE: int = 15
LABYRINTH_WIDTH: int = 42
LABYRINTH_HEIGHT: int = 42
START_POSITION: Tuple[int, int] = (1, 1)
GOAL_POSITION: Tuple[int, int] = (LABYRINTH_HEIGHT - 1, LABYRINTH_WIDTH - 1)

# ------------------------------- VARIABLES FOR GENETIC ALGORITHM --------------------------------- #

POPULATION_COUNT: int = 80
TOTAL_GENERATIONS: int = 30
MUTATION_PROBABILITY: float = 0.04

# ------------------------------- VARIABLES FOR PYPLOT -------------------------------------------- #

fitness_scores: np.ndarray = np.array([])
generations_numbers: np.ndarray = np.array([])
font_prop = fm.FontProperties(fname='Montserrat-SemiBold.ttf')

# ------------------------------- SIMULATION CODE ------------------------------------------------- #

if __name__ == '__main__':
    # Center the Simulation Window
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Initialise the Simulation
    pygame.init()
    window = LabyrinthDisplay(WINDOW_TITLE, LABYRINTH_WIDTH,
                              LABYRINTH_HEIGHT, CELL_SIZE)
    window.draw_labyrinth()

    # Initialise the genetic algorithm
    genetic_algorithm = GALabyrinthSolver(
        TOTAL_GENERATIONS, POPULATION_COUNT, MUTATION_PROBABILITY, START_POSITION, GOAL_POSITION, window.maze)

    # Set up the simulation loop
    run = True
    clock = pygame.time.Clock()

    # Start the Simulation #
    while run and genetic_algorithm.current_generation < genetic_algorithm.generation \
            and not genetic_algorithm.found_solution:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        # Print the current generation and highest fitness
        print("Current generation: {} | Current Fitness: {}".format(
            genetic_algorithm.current_generation, round(genetic_algorithm.get_highest_fitness(), 2)))

        # Update the plot data
        new_gen_val = np.array([genetic_algorithm.current_generation])
        new_fit_val = np.array([genetic_algorithm.get_highest_fitness()])
        generations_numbers = np.append(generations_numbers, new_gen_val)
        fitness_scores = np.append(fitness_scores, new_fit_val)

        # Create the next generation of paths
        genetic_algorithm.create_next_generation()

        # Draw the new paths on the simulation window
        toReset = set()
        for p in genetic_algorithm.population:
            for y, x in p.path:
                toReset.add((y, x))
                window.draw_rectangle(x * window.cell_size, y * window.cell_size, window.cell_size, window.cell_size,
                                      p.color)
        for y, x in toReset:
            window.draw_rectangle(x * window.cell_size, y * window.cell_size, window.cell_size, window.cell_size,
                                  (255, 255, 255))

        # Update the display
        pygame.display.update()

    # Add the final generation and highest fitness to the plot data
    generations_numbers = np.append(
        generations_numbers, [genetic_algorithm.current_generation])
    fitness_scores = np.append(
        fitness_scores, genetic_algorithm.get_highest_fitness())

    # Print the best path found | FOR DEBUGGING!!
    # print("Best path found", genetic_algorithm.optimal_solution)

    # Close the Pygame window
    pygame.quit()

    # Perform linear regression on the plot data and display the plot
    linearReg = LinearRegression().fit(
        generations_numbers.reshape(-1, 1), fitness_scores)

    plt.style.use('seaborn-darkgrid')
    fig, ax = plt.subplots(figsize=(12, 8))
    plt.locator_params(axis="both", integer=True, tight=True)

    ax.scatter(generations_numbers, fitness_scores, c='#ff2975',
               s=50, zorder=5, label='Fitnesswerte')
    ax.plot(generations_numbers, fitness_scores, c='#ff2975',
            linewidth=4, label='Fitnesswerte im Laufe der Generationen')

    ax.plot(generations_numbers, linearReg.predict(
        generations_numbers.reshape(-1, 1)), '-', color='#ffd319', label='Lineare Regression', linewidth=6)

    ax.fill_between(generations_numbers, fitness_scores, linearReg.predict(
        generations_numbers.reshape(-1, 1)), color='#ffd319', alpha=0.2)

    max_idx = np.argmax(fitness_scores)
    min_idx = np.argmin(fitness_scores)
    ax.annotate(f'Höchster Wert: {fitness_scores[max_idx]:.2f}', (generations_numbers[max_idx], fitness_scores[max_idx]),
                textcoords="offset points", xytext=(0, 10), ha='center', fontsize=12, color='#333')
    ax.annotate(f'Niedrigster Wert: {fitness_scores[min_idx]:.2f}', (generations_numbers[min_idx], fitness_scores[min_idx]),
                textcoords="offset points", xytext=(0, -15), ha='center', fontsize=12, color='#333')

    ax.grid(True, which="both", linestyle='--', linewidth=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel("Generationen", fontsize=22, fontproperties=font_prop)
    ax.set_ylabel("Fitnesswerte", fontsize=22, fontproperties=font_prop)
    ax.set_title("Auswertung der Simulation",
                 fontsize=28, fontweight='bold', fontproperties=font_prop)

    # Increase size of ticks on x and y-axis
    ax.tick_params(axis='both', labelsize=16, length=10)
    ax.set_yticks(np.arange(0, 1.25, 0.25))
    y_format = FormatStrFormatter('%g')
    ax.yaxis.set_major_formatter(y_format)
    ax.legend(loc='upper left', frameon=True,
              facecolor="white", fontsize=18, framealpha=0.8)

    # Set limit for x-axis to start at 0
    ax.set_xlim(0, generations_numbers[-1])
    ax.set_ylim(0, 1.2)

    plt.show()
