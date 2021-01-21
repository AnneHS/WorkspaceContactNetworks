import timeit

from model import ContactModel
from agent import Pedestrian
from helpers import save_data, printProgressBar

# Params
NUMBER_OF_AGENTS = [145] #145
ITERATIONS = 1 #5
STEPS = 10000
EXPONENT = [1.6] #1.5, 1.6, 1.7, 1.8, 1.9, 2.0, #1.5, 1.6
GRID_SIZES = [139]#, 161] # 8m^2, 12m^2, 16m^2


if __name__ == '__main__':

    start = timeit.default_timer()

    print('RUNNING')
    for N in NUMBER_OF_AGENTS:
        for exp in EXPONENT:
            for grid_size in GRID_SIZES:
                print(N, exp, grid_size)
                for i in range(ITERATIONS):
                    printProgressBar(i, ITERATIONS, prefix = 'Progress:', suffix = 'Complete', length = 50)
                    model = ContactModel(N, grid_size, grid_size, exp)
                    model.run(STEPS)
                    save_data(model, N, i, exp, grid_size)

    stop = timeit.default_timer()
    print()
    print('Time: ', stop - start)

# first run (N145_exp1.6_114x114) end 00:00
