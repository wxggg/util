import sys
import numpy as np
import pandas as pd


def getPercent(vals):
    vals = np.array(vals)
    average_latency = np.average(vals)
    sorted_vals = sorted(enumerate(vals), key=lambda i: i[1])
    mean_index = int(len(sorted_vals)*0.5)
    per_95_index = int(len(sorted_vals)*0.95)
    per_99_index = int(len(sorted_vals)*0.99)
    return {"avg": average_latency, "50": sorted_vals[mean_index][1], "95": sorted_vals[per_95_index][1], "99": sorted_vals[per_99_index][1], "perc_index": [sorted_vals[mean_index][0], sorted_vals[per_95_index][0], sorted_vals[per_99_index][0]]}


def parseLog(logfile):
    log = pd.read_csv(logfile, ':')

    log['serverLatency'] = log['finishStamp'] - log['receiveStamp']
    log['serverProcessTime'] = log['finishStamp'] - log['processStamp']
    log['serverQueueTime'] = log['processStamp'] - log['receiveStamp']

    log[['serverLatency', 'serverProcessTime',
         'serverQueueTime']] /= (1000*1000)
    log['cpuTime'] = log['retiredCycles'] / (3.4*1000*1000)
    return log


def getStat(logfile):
    log = parseLog(logfile)
    length = len(log)

    stat = {}

    total_cycle = log['finishStamp'][len(log)-1] - log['receiveStamp'][0]
    total_sec = total_cycle / (1000*1000*1000)

    nr_cycles = log['retiredCycles'].sum()

    nr_wall_cycles = log['processStamp'][len(log)-1] - log['processStamp'][0]
    stat['utilization'] = nr_cycles/(nr_wall_cycles*3.4)

    stat['avgQps'] = length / total_sec

    stat['processTimePerc'] = getPercent(list(log['serverProcessTime']))
    stat['serverLatencyPerc'] = getPercent(list(log['serverLatency']))

    ipc = log['retiredInstruction'] / log['retiredCycles']
    stat['ipcPerc'] = getPercent(ipc)
    return stat


if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print('python3 parseOne.py logfile')
        exit()

    log = parseLog(sys.argv[1])

    latencyLabels = ['taskID', 'clientLatency', 'serverLatency',
                     'serverProcessTime', 'serverQueueTime', 'cpuTime']
    log[latencyLabels].to_csv('./rtime.csv', index=False)

    latencySorted = log[latencyLabels].sort_values('clientLatency')

    length = len(log)
    window = int(length / 100)

    percent = pd.DataFrame(
        latencySorted.iloc[list(range(window-1, length, window))])

    clientLatency = list(latencySorted['clientLatency'])
    percent['avgServerQueueTime'] = [
        np.mean(clientLatency[i:i+window]) for i in range(0, length, window)][:100]

    percent['percent'] = list(range(1, 101))
    percent.to_csv('./client-time-max.csv', index=False)

    top = latencySorted.iloc[list(range(length-window, length))]
    top.to_csv('./top.csv', index=False)

    print(getStat(sys.argv[1]))
