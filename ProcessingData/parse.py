import os
import sys
import csv
import numpy as np
import itertools

from collections import defaultdict


def distribution(input_list):
    dist = defaultdict(list)

    unique_items, counts = np.unique(input_list, return_counts=True)
    percent = (counts / len(input_list))
    accupercent = list(itertools.accumulate(percent))

    dist['items'] = list(unique_items)
    dist['percent'] = list(percent)
    dist['accu_percent'] = list(accupercent)

    items_time = np.array(unique_items) * np.array(percent)
    total_time = np.sum(items_time)
    items_time_percent = items_time / total_time

    dist['times'] = list(items_time)
    dist['time_percent'] = list(items_time_percent)

    accu_time_percent = list(itertools.accumulate(items_time_percent))
    reverse_accu_time_percent = list(
        np.ones(len(accu_time_percent)) - np.array(accu_time_percent))

    dist['accu_time_percent'] = list(accu_time_percent)
    dist['reverse_accu_time_percent'] = reverse_accu_time_percent

    return dist


def percent(vals):
    vals = vals[1139:]
    average_latency = np.average(vals)
    sorted_vals = sorted(enumerate(vals), key=lambda i: i[1])
#    sorted_vals = sorted(vals);
    mean_index = int(len(sorted_vals)*0.5)
    per_95_index = int(len(sorted_vals)*0.95)
    per_99_index = int(len(sorted_vals)*0.99)
    return {"avg": average_latency, "50": sorted_vals[mean_index][1], "95": sorted_vals[per_95_index][1], "99": sorted_vals[per_99_index][1], "perc_index": [sorted_vals[mean_index][0], sorted_vals[per_95_index][0], sorted_vals[per_99_index][0]]}


def parse_log(fname):

    columns = defaultdict(list)

    with open(fname) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=':')
        for row in reader:
            for k, v in row.items():
                columns[k].append(int(v))

    length = len(columns['taskID'])

    clientLatency = np.array(columns['clientLatency'])
    serverLatency = (np.array(
        columns['finishStamp']) - np.array(columns['receiveStamp'])) / (1000*1000)
    serverProcessTime = (np.array(
        columns['finishStamp']) - np.array(columns['processStamp'])) / (1000*1000)
    serverQueryTime = (np.array(
        columns['processStamp']) - np.array(columns['receiveStamp'])) / (1000*1000)
    cpuTime = np.array(columns['retiredCycles']) / (3.4*1000*1000)

    columns['serverLatency'] = list(serverLatency)
    columns['serverProcessTime'] = list(serverProcessTime)
    columns['serverQueryTime'] = list(serverQueryTime)
    columns['cpuTime'] = list(cpuTime)

    with open(logdir+'./rtime.csv', 'w') as f:
        f.write('clientLatency,serverLatency,serverProcessTime,serverQueryTime\n')
        for i in range(length):
            f.write(str(clientLatency[i])+','
                    + str(serverLatency[i])+','
                    + str(serverProcessTime[i])+','
                    + str(serverQueryTime[i])+'\n')

    window = int(length / 100)

    clientLatency_sortedIndex = np.argsort(clientLatency)
    clientLatency_sorted = np.sort(clientLatency)
    with open(logdir+'./client-time-max.csv', 'w') as f:
        f.write('percent,taskID,clientLatency,serverLatency,' +
                'serverQueryTime,avg_serverQueryTime,cpuTime\n')

        for i in range(100):
            first = window * i
            last = window * (i+1) - 1
            index = clientLatency_sortedIndex[last]

            sum_serverQueryTime = 0  # sum of server query time
            for j in range(first, last+1):
                sum_serverQueryTime += serverQueryTime[clientLatency_sortedIndex[j]]

            f.write(str(i+1) + ','
                    + str(columns['taskID'][index]) + ','
                    + str(clientLatency_sorted[last]) + ','
                    + str(serverLatency[index]) + ','
                    + str(serverQueryTime[index]) + ','
                    + str(sum_serverQueryTime/window) + ','
                    + str(cpuTime[index]) + '\n')

    with open(logdir+'./client-time-dist.csv', 'w') as f:
        f.write('bin,percent,accum_percent\n')
        dist = distribution(clientLatency)
        for i in range(len(dist['items'])):
            f.write('%d,%.3f,%.3f\n' % (
                dist['items'][i], 100*dist['time_percent'][i], 100*dist['accu_time_percent'][i]))

    with open(logdir+'./top.csv', 'w') as f:
        for i in range(window):
            ri = length - window + i
            index = clientLatency_sortedIndex[ri]
            f.write(str(i+1) + ','
                    + str(columns['taskID'][index]) + ','
                    + str(clientLatency_sorted[ri]) + ','
                    + str(serverLatency[index]) + ','
                    + str(serverQueryTime[index]) + ','
                    + str(cpuTime[index]) + ','
                    + str(serverQueryTime[index] + cpuTime[index]) + '\n')

    return columns


def parse_lucene_log(fname, expected_qps, expected_iter, logdir):
    columns = parse_log(fname)

    length = len(columns['taskID'])
    total_cycle = columns['finishStamp'][-1] - columns['receiveStamp'][0]
    total_sec = total_cycle / (1000*1000*1000)
    avg_qps = length / total_sec

    print('iters:%d (%d), tasks:%d, cycles:%d, qps:%f, (%d)\n' % (
        length/1141, expected_iter, length, total_cycle, avg_qps, expected_qps))

    nr_cycles = np.sum(np.array(columns['retiredCycles']))
    nr_wall_cycles = columns['processStamp'][-1] - columns['processStamp'][0]
    utilization = nr_cycles/(nr_wall_cycles*3.4)

    print('total_cycle:%d, wall_cycles:%d\n utilization:%f' %
          (nr_cycles, nr_wall_cycles, utilization))

    ptimeMS = np.array(columns['serverProcessTime'])
    ptimeNS = ptimeMS * (1000*1000)

    ptime_hist = distribution(ptimeMS)
    ptime_perc = percent(ptimeNS)
    print('serverProcessTime 50:' + str(ptime_perc['50']))

    ltimeMS = np.array(columns['serverLatency'])
    ltimeNS = ltimeMS * (1000*1000)

    ltime_hist = distribution(ltimeMS)
    ltime_perc = percent(ltimeNS)

    ipc = np.array(columns['retiredInstruction']) / \
        np.array(columns['retiredCycles'])
    ipc_perc = percent(ipc)
    # print(ipc)

    stat = {}

    stat['ptime_hist'] = ptime_hist
    stat['ptime_perc'] = ptime_perc
    stat['ltime_hist'] = ltime_hist
    stat['ltime_perc'] = ltime_perc
    stat['ipc_perc'] = ipc_perc

    stat['measured_qps'] = avg_qps
    stat['utilization'] = utilization

    return stat


def parse_logs(names, logdir):
    logs = {}
    for f in names:
        sf = f.split('-')
        iters = int(sf[-1])
        qps = int(sf[-2])
        print('parse log file=' + str(f) + ' qps=' +
              str(qps) + ' invoks '+str(iters))
        logs[qps] = parse_lucene_log(f, qps, iters, logdir)
    return logs


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print('python3 parse.py logdir')
        exit()

    logdir = sys.argv[1] + '/'

    files = [logdir + f for f in os.listdir(logdir) if len(
        f.split('-')) == 3 and len(f.split('.')) == 1]

    logs = parse_logs(files, logdir)

    # qps = sorted(logs.keys())

    with open(logdir + './qps-latency.csv', 'w') as f:
        f.write(
            'qps,realqps,ptime_50,ptime_95,ptime_99,ltime_50,ltime_95,ltime_99,utilization,ipc\n')
        for qps in sorted(logs.keys()):
            log = logs[qps]
            f.write('%d,%d,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%d\n' % (
                log['measured_qps'], qps,
                log['ptime_perc']['50'], log['ptime_perc']['95'], log['ptime_perc']['99'],
                log['ltime_perc']['50'], log['ltime_perc']['95'], log['ltime_perc']['99'],
                log['utilization'], log['ipc_perc']['50']))
