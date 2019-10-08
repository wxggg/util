import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns


markers = ['o', '.', '*', 'x', '^']
i = 0


def randomMarker():
    global i
    i = (i+1) % len(markers)
    return markers[i]


def plotLabels(log, labels, x=None, xw=None):
    if x == None:
        x = list(range(len(log)))

    if xw == None:
        xw = x

    for label in labels:
        plt.plot(xw, log[label][x], label=label, marker=randomMarker())

    plt.xticks(xw)
    plt.title(labels)
    plt.legend()
    plt.show()


def plotLabelsTwo(log1, log2, labels, legend1, legend2, x=None, xw=None):
    if x == None:
        x = list(range(len(log1)))

    if xw == None:
        xw = x

    for label in labels:
        plt.plot(xw, log1[label][x], label=legend1 +
                 label, marker=randomMarker())
        plt.plot(xw, log2[label][x], label=legend2 +
                 label, marker=randomMarker())

    plt.xticks(xw)
    plt.title(labels)
    plt.legend()
    plt.show()


def plotLabelsSub(log, labels1, labels2, x=None, xw=None):
    if x == None:
        x = list(range(len(log)))

    if xw == None:
        xw = x

    plt.subplot(211)
    for label in labels1:
        plt.plot(xw, log[label][x], label=label, marker=randomMarker())
    plt.xticks(xw)
    plt.title(labels1)
    plt.legend

    plt.subplot(212)
    for label in labels2:
        plt.plot(xw, log[label][x], label=label, marker=randomMarker())
    plt.xticks(xw)
    plt.title(labels2)
    plt.legend()

    plt.show()


def plotBars(log, labels, x=None, xw=None):
    if x == None:
        x = list(range(len(log)))

    if xw == None:
        xw = x

    width = 0.3

    y = log[labels[0]][x]
    p1 = plt.bar(xw, y, width)
    bottom = y
    pxs = [p1]
    for label in labels[1:]:
        y = log[label][x]
        px = plt.bar(xw, y, width, bottom=bottom)
        bottom += y
        pxs.append(px)

    plt.xticks(xw)
    plt.title(labels)
    plt.legend(pxs, labels)

    plt.show()


def plotDist(log, label, x=None):
    if x == None:
        x = list(range(len(log)))
    y = log[label][x]

    sns.distplot(y, kde=True)
    plt.show()
