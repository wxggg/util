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

    # plotLabels(log, ['serverLatency', 'cpuTime'])
    # plotLabels(log, ['serverLatency', 'queueSize'])

    # plotBars(log, ['cpuTime', 'serverLatency'], list(range(20)))

    # plotDist(log, 'serverLatency')

    queLatency = {}
    for i in range(100):
        queLatency[i] = []

    for i in range(len(log)):
        queueSize = log['queueSize'][i]
        if queueSize < 100:
            queLatency[queueSize].append(log['serverLatency'][i])

    que= {}
    que['queueLatency'] = []
    for i in range(100):
        if 0 == len(queLatency[i]):
            break
        que['queueLatency'].append(np.mean(queLatency[i]))
    que = pd.DataFrame(que)

    plotLabels(que, ['queueLatency'])
