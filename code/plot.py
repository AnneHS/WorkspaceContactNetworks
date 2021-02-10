import csv
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os
import pandas as pd
import math
import sys

np.set_printoptions(threshold=sys.maxsize)

NUMBER_OF_AGENTS = [145]#[145] #145
ITERATIONS = 1#5
STEPS = 10000 #10000
EXPONENT = [2.0]#[1.5, 1.6, 1.7, 1.8, 1.9, 2.0] #1.5, 1.6, 1.7, 1.8, 1.9, 2.0, #1.5, 1.6
XMIN = [3]
GRID_SIZES = [161]#[114, 139, 161]

def plot_pedestrian_movement(model_name, model_directory, N,  exp, size):
    '''Plots location of each pedestrian with respect to time (x-axis) '''

    # Time
    t = np.arange(0, STEPS+1, 1)

    for i in range(ITERATIONS):

        # Read data (x- and y-coordinates pedestrians)
        x_df = pd.read_csv(f"../results/xmin3/{model_name}/{i}/x_locs.csv", header=None, delimiter=";")
        y_df = pd.read_csv(f"../results/xmin3/{model_name}/{i}/y_locs.csv", header=None, delimiter=";")
        x_locs = x_df.values
        y_locs = y_df.values

        # Create directory for plots
        iteration_directory = f'{model_directory}/{i}'
        if not os.path.isdir(iteration_directory):
             os.mkdir(iteration_directory)


        # Plot
        for n in range(N):

            trip_lengths_df = pd.read_csv(f"../results/xmin3/{model_name}/{i}/agent_trips/agent{n}_steps.csv")
            trip_lengths = trip_lengths_df.values.flatten()

            # Calculate time points for new trip
            time_points = [0]
            for trip_length in trip_lengths:
                next_time_point = int(time_points[-1]+trip_length)
                if next_time_point <= STEPS:
                    time_points.append(next_time_point)

            '''
            start = 3000
            end = 4000

            relevant_time_points = [x for x in time_points if (start<= x <= end)]
            tt = t[start:end]
            x = x_locs[n][start:end]
            y = y_locs[n][start:end]

            fig, axs = plt.subplots(2, 1)
            fig.suptitle(f'Pedestrian {n}')

            # Subplot: x-coordinate
            axs[0].plot(tt, x)
            axs[0].legend()
            axs[0].set_ylabel('x')

            # Subplot: y-coordinate
            axs[1].plot(tt, y)
            axs[1].set_ylabel('y')
            axs[1].set_xlabel('t')

            # Mark time points
            for time_point in relevant_time_points:
                axs[0].plot(time_point, x_locs[n][time_point], marker='o', color='r')
                axs[1].plot(time_point, y_locs[n][time_point], marker='o', color='r')
            plt.show()

            plt.show()
            #plt.savefig(f'{iteration_directory}/Pedestrian{n}.png')
            #plt.close(
            '''

            fig, axs = plt.subplots(2, 1)
            fig.suptitle(f'Pedestrian {n}')

            # Subplot: x-coordinate
            axs[0].plot(t, x_locs[n])
            axs[0].legend()
            axs[0].set_ylabel('x')

            # Subplot: y-coordinate
            axs[1].plot(t, y_locs[n])
            axs[1].set_ylabel('y')
            axs[1].set_xlabel('t')

            # Mark time points
            for time_point in time_points:
                axs[0].plot(time_point, x_locs[n][time_point], marker='o', color='r')
                axs[1].plot(time_point, y_locs[n][time_point], marker='o', color='r')
            plt.show()
            #'''

            #plt.savefig(f'{iteration_directory}/Pedestrian{n}.png')
            #plt.close()

        '''

        data_df = pd.read_csv(f"../results/xmin3/{model_name}/{i}/trip_lengths.csv", header=None, delimiter=";")
        data = data_df.values.flatten()
        data.sort()
        print(len(data))
        print(data[-1])
        print(data)
        trip_data = data[data <= 200]

        w = 5
        n =math.ceil((trip_data.max() - trip_data.min())/w)
        plt.title(f"Exp = {exp}, xmin = 3")
        plt.hist(trip_data, bins=n)
        plt.xlabel='trip length'
        plt.show()
        '''
        #plt.xlabel

        #H, X1 = np.histogram(trip_data, bins=100, normed=True)
        #dx = X1[1]-X1[0]
        #F1 = np.cumsum(H)*dx
        #plt.plot(X1[1:], F1)
        #plt.show()


        #print('Remove > 200')
        #trip_data = data[data <= 300]

        #print('Calculate n')
        #w = 10
        #n =math.ceil((trip_data.max() - trip_data.min())/w)
        #print('Plot...')
        #plt.title(f"Exp = {exp}, xmin = 3")
        #plt.hist(trip_data, bins=n)
        #plt.show()
        #plt.xlabel('trip length')
        #plt.show()
        #plt.savefig(f'../plots/Trip_Lengths/N{N}_exp{exp}_size{size}_xmin3.png')
        #plt.close()
        #print(trip_lengths)



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
                for xmin in XMIN:

                    # Create directory for plots
                    model_name = f'N{N}_exp{exp}_{grid_size}x{grid_size}'
                    model_directory = f'../plots/xmin{xmin}/{model_name}'
                    if not os.path.isdir(model_directory):
                         os.mkdir(model_directory)

                    #plot_network(model_name, model_directory)
                    plot_pedestrian_movement(model_name, model_directory, N, exp, grid_size)


plot()
