
from parseAll import *
from plot import *

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('python3 plotTwo.py dir1 dir2')
        exit()

    dir1 = sys.argv[1] + '/'
    dir2 = sys.argv[2] + '/'

    qpsLatency1 = getQpsLatency(dir1)
    qpsLatency2 = getQpsLatency(dir2)

    step = 10

    x = list(range(len(qpsLatency1)))
    qps = [step*(i+1) for i in x]

    plotLabelsTwo(qpsLatency1, qpsLatency2, ['serverLatency95', 'serverLatency99'],
                  dir1, dir2, x=x, xw=qps)
    # plotLabelsTwo(qpsLatency1, qpsLatency2, [
    #               'utilization'], dir1, dir2, x=x, xw=qps)
