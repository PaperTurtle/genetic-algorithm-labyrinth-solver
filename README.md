# Genetic Algorithm Labyrinth Solver

> This project implements a genetic algorithm to solve a labyrinth. It includes a custom labyrinth generator and a solver that evolves a population of potential solutions over multiple generations, optimizing for the shortest path to the exit.

## Features

-  **Labyrinth Generation**: Utilizes a depth-first search algorithm to generate a unique labyrinth.
-  **Genetic Algorithm Solver**: Applies genetic operations like crossover and mutation to find an efficient path through the labyrinth.
-  **Visualization**: The labyrinth and the paths taken by the solutions in each generation are visually represented using Pygame.

## Dependencies

-  Python 3.x
-  Pygame
-  Numpy
-  Matplotlib
-  Scikit-Learn

## Installation

Ensure you have Python installed on your system. You can download and install Python from [here](https://www.python.org/downloads/).

Install the required Python libraries using pip:

```python
pip install -r requirements.txt
```

## Running the Simulation

-  Clone the repository or download the source code.

```bash
git clone https://github.com/PaperTurtle/genetic-algorithm-labyrinth-solver.git
```

-  Navigate to the project directory.

```python
cd genetic-algorithm-labyrinth-solver
```

-  Run the main script:

```python
python script.py
```

## How It Works

-  **Labyrinth Generation**: The LabyrinthGenerator class generates a labyrinth using a depth-first search algorithm.

-  **Path Finding**: The GALabyrinthSolver class attempts to solve the labyrinth using a genetic algorithm. It evolves a population of potential solutions (paths) over a specified number of generations.

-  **Visualization**: The LabyrinthDisplay class uses Pygame to display the labyrinth and the paths taken by the solutions.

## Customization

You can customize various parameters like labyrinth size, number of generations, mutation rate, etc., in the `script.py` file to see how they affect the algorithm's performance.
