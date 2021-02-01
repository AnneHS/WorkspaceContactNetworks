import timeit

from model import ContactModel
from agent import Pedestrian
from helpers import save_data, printProgressBar
from multiprocessing import Pool, cpu_count
# Params
NUMBER_OF_AGENTS = [145]#[145] #145
#ITERATIONS = 1 #5
STEPS = 10000 #10000
EXPONENT = [1.5, 1.6, 1.7, 1.8, 1.9, 2.0] #1.5, 1.6, 1.7, 1.8, 1.9, 2.0, #1.5, 1.6
GRID_SIZES = [114, 139, 161]#, 161] # 8m^2, 12m^2, 16m^2

def evaluate_mp(N, grid_size, exp):
    data = []
    for i in range(cpu_count()-3):
        data.append((N, grid_size, exp, i))
    p = Pool(cpu_count()-3)
    results = p.map(simulate_mp, data)
    p.close()
    p.join()

def simulate_mp(params):
    N, grid_size, exp, i = params
    model = ContactModel(N, grid_size, grid_size, exp, STEPS, seed=8)
    model.run(STEPS)
    save_data(model, N, i, exp, grid_size)

if __name__ == '__main__':

    sets = len(NUMBER_OF_AGENTS) * len(EXPONENT) * len(GRID_SIZES)
    count=0
    #p = Pool(cpu_count()-1)
    start = timeit.default_timer()
    for N in NUMBER_OF_AGENTS:
        for exp in EXPONENT:
            for grid_size in GRID_SIZES:
                printProgressBar(count, sets, prefix = 'Progress:', suffix = 'Complete', length = 50)
                print(N, exp, grid_size)
                print()
                evaluate_mp(N, grid_size, exp)
                count+=1
                #p =
                #data = [(N, grid_size, grid_size, exp),]*7
                #print(data)
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
