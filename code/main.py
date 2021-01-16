import sys
import os
import csv
import numpy as np
import timeit

from model import ContactModel
from agent import Pedestrian

NUMBER_OF_AGENTS = [75, 145]
ITERATIONS = 100
STEPS = 10000
EXPONENT = [1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
GRID_SIZES = [114, 139, 161] # 8m^2, 12m^2, 16m^2

def save_data(model, N, i, exp, grid_size):

    # Model directory
    model_name = f'N{N}_exp{exp}_{grid_size}x{grid_size}'
    directory = '../results/' + model_name
    if not os.path.isdir(directory):
         os.mkdir(directory)

    # Iteration directory
    iteration_dir = directory +  f'/{i}'
    os.mkdir(iteration_dir)

    # Agent areas directory
    agent_areas_dir = iteration_dir + '/agent_areas'
    os.mkdir(agent_areas_dir)

    # Save adjacency matrix
    matrix = np.asarray(model.adjacency_matrix)
    matrix[matrix==0]=['nan']

    # Add labels for nodes
    new_matrix = np.zeros((N+1, N+1))
    for i in range(N):
        new_matrix[0,i+1] = int(i)
        new_matrix[i+1, 0] = int(i)
    for i in range(1, N+1):
        for j in range(1, N+1):
            new_matrix[i, j] = matrix[i-1, j-1]

    # Save adjacency matrix
    np.savetxt(iteration_dir + '/adjacency.csv', new_matrix, delimiter=";")

    # Save area matrices
    for agent in model.schedule.agents:
        np.savetxt(agent_areas_dir + f'/agent{agent.unique_id}.csv', agent.area_traversed, delimiter=";")

if __name__ == '__main__':

    start = timeit.default_timer()

    print('RUNNING')
    for N in NUMBER_OF_AGENTS:
        for exp in EXPONENT:
            for grid_size in GRID_SIZES:
                print(N, exp, grid_size)
                for i in range(ITERATIONS):
                    model = ContactModel(N, grid_size, grid_size, exp)
                    model.run(STEPS)
                    save_data(model, N, i, exp, grid_size)

    stop = timeit.default_timer()
    print()
    print('Time: ', stop - start)
