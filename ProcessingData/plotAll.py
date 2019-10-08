import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns

from parseAll import *

from plot import *


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('python3 plotAll.py logdir')
        exit()

    logdir = sys.argv[1] + '/'

    stats = getStats(logdir)
    qpsLatency = getQpsLatency(logdir)

    step = 10
    x = list(range(len(qpsLatency)))
    qps = [step*(i+1) for i in x]

    print(qpsLatency['processTime50'])

    # plotLabels(qpsLatency, ['processTime50',
    #                         'processTime95', 'processTime99'], x=x, xw=qps)

    plotLabels(qpsLatency, ['serverLatency50',
                            'serverLatency95', 'serverLatency99'], x=x, xw=qps)

    # plotLabels(qpsLatency, ['utilization'], x=x, xw=qps)

    # plotLabelsSub(qpsLatency, ['serverLatency99'],
    #               ['utilization'], x=x, xw=qps)
