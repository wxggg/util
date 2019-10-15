import time
import random
import queue
import socket
import threading

MAX_BYTES = 70


class SendTasks:

    def __init__(self, serverHost, serverPort, runTimeSec, savFile):
        self.startTime = time.time()
        self.runTimeSec = runTimeSec

        self.sent = {}
        self.queue = queue.Queue()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((serverHost, serverPort))
        print('connect to ' + str(serverHost) + ':' + str(serverPort))

        t = threading.Thread(target=self.gatherResponses, args=())
        t.setDaemon(True)
        t.start()

        t = threading.Thread(target=self.sendRequests, args=())
        t.setDaemon(True)
        t.start()

        self.taskID = 0
        self.f = open(savFile, 'w', encoding='utf-8')

    def send(self, task):
        taskString = task + ';' + str(self.taskID)
        taskString += (MAX_BYTES - len(taskString)) * ' '
        startTime = time.time()
        self.sent[self.taskID] = (startTime, taskString)
        self.queue.put((startTime, taskString))
        self.taskID += 1

    def gatherResponses(self):
        print('start gather response')

        while True:
            result = ''
            while len(result) < 112:
                result += self.sock.recv(112-len(result)).decode('ascii')

            print(result)

            taskID = int(result.split(':')[0])
            endTime = time.time()

            taskStartTime, taskString = self.sent[taskID]
            del self.sent[taskID]
            latencyMS = (endTime-taskStartTime) * 1000
            self.f.write(result + ': '+str(latencyMS) + '\n')

    def sendRequests(self):
        print('begin send requests')

        while True:
            timeTask = self.queue.get()
            sendTime, task = timeTask
            startTime = time.time()
            while len(task) > 0:
                sent = self.sock.send(task.encode('ascii'))
                if sent <= 0:
                    raise RuntimeError('failed to send task ' + str(task))
                task = task[sent:]


if __name__ == "__main__":
    st = SendTasks('127.0.0.1', 7777, 100, './test.csv')

    iteration = 1

    taskStrings = []

    with open('tasks/wiki.1M.nostopwords.term.tasks', 'r') as f:
        for line in f:
            taskStrings.append(line.split(' #')[0])

    r = random.Random(0)
    if True:
        r.shuffle(taskStrings)

    iters = 0
    while True:
        iters += 1
        for task in taskStrings:
            st.send(task)

        if iters == iteration:
            break

    print('Sent all tasks ' + str(iters) + ' times')

    time.sleep(10)
