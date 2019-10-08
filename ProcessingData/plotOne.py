import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from parseOne import *

from plot import *


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('python3 plotOne.py logfile')
        exit()

    log = parseLog(sys.argv[1])

    # plotLabels(log, ['serverLatency', 'totalHitCount'])

    # plotBars(log, ['cpuTime', 'serverLatency'], list(range(20)))

    plotDist(log, 'serverLatency')
