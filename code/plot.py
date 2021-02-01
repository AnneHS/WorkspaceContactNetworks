import csv
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os
import pandas as pd

NUMBER_OF_AGENTS = [145]#[145] #145
ITERATIONS = 5
STEPS = 10000 #10000
EXPONENT = [1.5] #[1.5, 1.6, 1.7, 1.8, 1.9, 2.0] #1.5, 1.6, 1.7, 1.8, 1.9, 2.0, #1.5, 1.6
GRID_SIZES = [114]#[114, 139, 161]

def plot_pedestrian_movement(N, model_name, model_directory):
    '''Plots location of each pedestrian with respect to time (x-axis) '''

    t = np.arange(0, STEPS+1, 1)
    for i in range(ITERATIONS):

        # Read data (x- and y-coordinates pedestrians)
        x_df = pd.read_csv(f"../results/{model_name}/{i}/x_locs.csv", delimiter=";")
        y_df = pd.read_csv(f"../results/{model_name}/{i}/y_locs.csv", delimiter=";")
        x_locs = x_df.values
        y_locs = y_df.values

        # Create directory for plots
        iteration_directory = f'{model_directory}/{i}'
        if not os.path.isdir(iteration_directory):
             os.mkdir(iteration_directory)

        # Plot pedestrian movement (x-coorindate/y-coordinate vs time)
        for n in range(N):

            fig, axs = plt.subplots(2, 1)
            fig.suptitle(i)

            # x-coordinate
            axs[0].plot(t, x_locs[n])
            axs[0].set_ylabel('x')

            # y-coordinate
            axs[1].plot(t, y_locs[n])
            axs[1].set_ylabel('y')
            axs[1].set_xlabel('t')

            plt.savefig(f'{iteration_directory}/Pedestrian{n}.png')
            plt.close()

def plot_network(model_name, model_directory):
    '''Plots network for given adjacency matrix'''
    
    for i in range(1):#ITERATIONS):

        # Read data: adjacency matrix
        iteration_directory = f'{model_directory}/{i}'
        if not os.path.isdir(iteration_directory):
             os.mkdir(iteration_directory)
        adjacency_df = pd.read_csv(f"../results/{model_name}/{i}/adjacency.csv", delimiter=";")

        # Clean adjacency matrix
        adjacency_np = adjacency_df.to_numpy()
        adjacency_matrix = adjacency_np[:,1:] # Remove node labels
        adjacency_matrix[np.isnan(adjacency_matrix)] = 0

        # Plot network
        G = nx.from_numpy_matrix(adjacency_matrix, create_using=nx.DiGraph).to_undirected()
        layout = nx.spring_layout(G, k=0.08, iterations=20)
        nx.draw(G, layout)
        nx.draw_networkx_edge_labels(G, pos=layout)
        plt.savefig(f'{iteration_directory}/Network.png', dpi=1000)
        plt.close()


def plot():

    for N in NUMBER_OF_AGENTS:
        for exp in EXPONENT:
            for grid_size in GRID_SIZES:

                # Create directory for plots
                model_name = f'N{N}_exp{exp}_{grid_size}x{grid_size}'
                model_directory = f'../plots/{model_name}'
                if not os.path.isdir(model_directory):
                     os.mkdir(model_directory)

                #plot_network(model_name, model_directory)
                plot_pedestrian_movement(N, model_name, model_directory)


plot()
