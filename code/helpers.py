import sys
import os
import csv
import numpy as np

def save_data(model, N, i, exp, grid_size, xmin):

    # Model directory
    model_name = f'N{N}_exp{exp}_{grid_size}x{grid_size}'
    directory = f'../results/xmin{xmin}/{model_name}'
    if not os.path.isdir(directory):
         os.mkdir(directory)

    # Iteration directory
    iteration_dir = directory +  f'/{i}'
    os.mkdir(iteration_dir)

    # Agent areas directory
    agent_areas_dir = iteration_dir + '/agent_trips'
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

    # Save adjacency matrix, x locs and y locs
    np.savetxt(iteration_dir + '/adjacency.csv', new_matrix, delimiter=";")
    np.savetxt(iteration_dir + '/x_locs.csv', model.x_locs, delimiter=";")
    np.savetxt(iteration_dir + '/y_locs.csv', model.y_locs, delimiter=";")
    np.savetxt(iteration_dir + '/trip_lengths.csv', model.trip_lengths, delimiter=";")

    # Save area matrices
    for agent in model.schedule.agents:
        np.savetxt(agent_areas_dir + f'/agent{agent.unique_id}_trip_lengths.csv', agent.trip_lengths_covered, delimiter=";")
        np.savetxt(agent_areas_dir + f'/agent{agent.unique_id}_steps.csv', agent.steps_covered, delimiter=";")

def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    # source: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()
