
from parseAll import *
from plot import *

if __name__ == '__main__':

    dirs = sys.argv[1:]
    if len(dirs) == 0:
        exit()

    qpsLatency = []
    for dir in dirs:
        dir += '/'
        qpsLatency.append(getQpsLatency(dir))

    step = 50

    x = list(range(len(qpsLatency[0])))
    qps = [step*(i+1) for i in x]

    plotLabelsN(qpsLatency, 'serverLatency95', dirs, x=x, xw=qps)
