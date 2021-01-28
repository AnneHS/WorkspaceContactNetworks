import cProfile
import pstats
import io

from model2 import ContactModel
from agent2 import Pedestrian

N = 145 #75 #145 #75
EXP = 1.6
GRID_SIZE = 139
STEPS = 10000 #5000 #10000 #2#5000

def main():
        model = ContactModel(N, GRID_SIZE, GRID_SIZE, EXP, STEPS, seed=8)
        model.run(STEPS)

if __name__ == '__main__':
    pr = cProfile.Profile()
    pr.enable()
    main()
    pr.disable()

    s=io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
    ps.print_stats()
    print(s.getvalue())
