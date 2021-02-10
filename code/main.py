import timeit

from model import ContactModel
from agent import Pedestrian
from helpers import save_data, printProgressBar
from multiprocessing import Pool, cpu_count

# Params
NUMBER_OF_AGENTS = [145]
STEPS = 10000
EXPONENT = [1.5, 1.6, 1.7, 1.8, 1.9, 2.0] #[1.5, 1.6, 1.7, 1.8, 1.9, 2.0] #1.5, 1.6, 1.7, 1.8, 1.9, 2.0, #1.5, 1.6
GRID_SIZES = [114, 139, 161] #[114, 139, 161]#, 161] # 8m^2, 12m^2, 16m^2
XMIN = [3] # [0, 3, 7]? #TODO: check notebook

def evaluate_mp(N, grid_size, exp, xmin):
    data = []
    cores_used = cpu_count()-3
    print(cores_used)
    for i in range(cores_used):
        data.append((N, grid_size, exp, xmin, i))
    p = Pool(cores_used)
    results = p.map(simulate_mp, data)
    p.close()
    p.join()

def simulate_mp(params):
    N, grid_size, exp, xmin, i = params
    model = ContactModel(N, grid_size, grid_size, exp, STEPS, xmin, seed=8)
    model.run(STEPS)
    save_data(model, N, i, exp, grid_size, xmin)

if __name__ == '__main__':

    sets = len(NUMBER_OF_AGENTS) * len(EXPONENT) * len(GRID_SIZES) * len(XMIN)
    #count=0

    start = timeit.default_timer()
    for N in NUMBER_OF_AGENTS:
        for exp in EXPONENT:
            for grid_size in GRID_SIZES:
                for xmin in XMIN:
                    printProgressBar(count, sets, prefix = 'Progress:', suffix = 'Complete', length = 50)
                    print(N, exp, grid_size, xmin)
                    print()
                    evaluate_mp(N, grid_size, exp, xmin)
                    count+=1
    printProgressBar(count, sets, prefix = 'Progress:', suffix = 'Complete', length = 50)
    stop = timeit.default_timer()
    print('Runtime: ', stop-start)


    '''
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
    '''

# first run (N145_exp1.6_114x114) end 00:00
