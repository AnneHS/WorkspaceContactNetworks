import cProfile, pstats, io
import pstats
import io

from model_single import ContactModel
from agent_single import Pedestrian

N = 145 #145 #75 #145 #75
EXP = 1.6
GRID_SIZE = 139
STEPS = 10000 #00 #10000  #10000

def main():
        model = ContactModel(N, GRID_SIZE, GRID_SIZE, EXP, STEPS, seed=8)
        model.run(STEPS)

if __name__ == '__main__':
    '''
    pr = cProfile.Profile()
    pr.enable()
    main()
    pr.disable()

    s=io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
    ps.print_stats()
    filename = 'profile_test.prof'
    ps.dump__stats(filename)
    print(s.getvalue())
    '''
    pr = cProfile.Profile()
    pr.enable()
    main()
    pr.disable()
    s=io.StringIO()
    sortby = 'tottime'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    filename = f'profile{N}_{EXP}_{GRID_SIZE}_{STEPS}_0_SINGLE_GRID_updated.prof'
    ps.dump_stats(filename)  # dump the stats to a file named stats.dmp
