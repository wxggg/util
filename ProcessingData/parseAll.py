import os
from parseOne import *


def getStats(logdir):
    logdir += '/'

    files = [logdir + f for f in os.listdir(logdir) if len(
        f.split('-')) == 3 and len(f.split('.')) == 1]

    stats = {}
    for f in files:
        name, qps, iters = f.split('-')
        qps = int(qps)
        stats[qps] = getStat(f)

    return stats


def getQpsLatency(logdir):
    stats = getStats(logdir)

    qpsLatency = []
    for qps in sorted(stats.keys()):
        stat = stats[qps]
        row = {}
        row['qps'] = qps
        row['avgQps'] = stat['avgQps']
        row['processTime50'] = stat['processTimePerc']['50']
        row['processTime95'] = stat['processTimePerc']['95']
        row['processTime99'] = stat['processTimePerc']['99']
        row['serverLatency50'] = stat['serverLatencyPerc']['50']
        row['serverLatency95'] = stat['serverLatencyPerc']['95']
        row['serverLatency99'] = stat['serverLatencyPerc']['99']
        row['utilization'] = stat['utilization']
        row['ipc'] = stat['ipcPerc']['50']
        qpsLatency.append(row)
    return pd.DataFrame(qpsLatency)


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print('python3 parseAll.py logdir')
        exit()

    qpsLatency = getQpsLatency(sys.argv[1])
    qpsLatency.to_csv('qpsLatency.csv', index=False)
