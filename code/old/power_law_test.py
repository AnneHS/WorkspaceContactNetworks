import powerlaw
import math
import matplotlib.pyplot as plt
import numpy as np

EXPONENT = [1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
ITERATIONS = 1000

draws = []
for exp in EXPONENT:
    trip_lengths = powerlaw.Power_Law(xmin=7, parameters=[exp])
    trip_draws=[]
    for i in range(ITERATIONS):
        draw = int(trip_lengths.generate_random(1)[0])
        if draw <= 200:
            trip_draws.append(draw)

    trip_draws.sort()
    data = np.asarray(trip_draws)
    w = 10
    n=math.ceil((data.max() - data.min())/w)
    plt.title(f"Exp = {exp}, xmin = 7")
    plt.hist(data, bins=n)
    plt.xlabel('trip length')
    plt.savefig(f'../plots/Power_Law/exp={exp}_xmin7.png')
    plt.close()

for exp in EXPONENT:
    trip_lengths = powerlaw.Power_Law(parameters=[exp])
    trip_draws=[]
    for i in range(ITERATIONS):
        draw = int(trip_lengths.generate_random(1)[0])
        if draw <= 200:
            trip_draws.append(draw)

    trip_draws.sort()
    data = np.asarray(trip_draws)
    w = 10
    n=math.ceil((data.max() - data.min())/w)
    plt.title(f"Exp = {exp}, xmin = 0")
    plt.hist(data, bins=n)
    plt.xlabel('trip length')
    plt.savefig(f'../plots/Power_Law/exp={exp}_xmin0.png')
    plt.close()
