from utility import Graph
import numpy as np
import math


def hits(graph, epsilon=0.1):
    auth_current = 1
    hub_current = 1
    while True:
        auth_old = auth_current
        hub_old = hub_current
        for point in graph.iterpoints():
            point.auth = sum(p.hub for p in point.linkFrom)
            point.hub = sum(p.auth for p in point.linkTo)
        norm_auth = math.sqrt(sum(math.pow(p.auth, 2) for p in graph.iterpoints()))
        norm_hub = math.sqrt(sum(math.pow(p.hub, 2) for p in graph.iterpoints()))
        for point in graph.iterpoints():
            point.auth /= norm_auth
            point.hub /= norm_hub
        auth_current = sum(p.auth for p in graph.iterpoints()) / len(graph.points)
        hub_current = sum(p.hub for p in graph.iterpoints()) / len(graph.points)
        if auth_current - auth_old + hub_current - hub_old < epsilon:
            break


def pagerank(graph, epsilon=0.1):
    graph.initPagerank()
    while True:
        pagerank_old = [p.pagerank for p in graph.iterpoints()]
        for point in graph.iterpoints():
            point.newPagerank(sum(p.pagerank / len(p.linkTo) for p in point.linkFrom))
        graph.updateAllPagerank()
        pagerank_current = [p.pagerank for p in graph.iterpoints()]
        if sum(abs(pagerank_old[i] - pagerank_current[i]) for i in range(len(pagerank_current))) < epsilon:
            break


def simrank(graph, c=0.8, epsilon=0.1, show=False):
    sim = np.identity(len(graph))
    while True:
        sim_old = np.copy(sim)
        for i in range(len(graph)):
            for j in range(len(graph)):
                p1 = graph.index(i)
                p2 = graph.index(j)
                if p1 is not p2 and len(p1.linkFrom) > 0 and len(p2.linkFrom) > 0:
                    sum_ = 0
                    for pp1 in p1.linkFrom:
                        for pp2 in p2.linkFrom:
                            k = graph.indexOf(pp1)
                            l = graph.indexOf(pp2)
                            sum_ += sim_old[k][l]
                    sim[i][j] = sum_ * c / len(p1.linkFrom) / len(p2.linkFrom)
        if sum(abs(n) for n in np.subtract(sim_old, sim).flatten()) / 2 < epsilon:
            break

    if show:
        print("SimRank")
        for i in range(len(graph)):
            for j in range(len(graph)):
                if sim[i][j] == 1:
                    break
                else:
                    print("S({}, {}) --> {}".format(graph.index(j), graph.index(i), sim[j][i]))
    return sim


if __name__ == '__main__':
    graph = Graph("dataset/graph_3.txt")
    hits(graph)
    graph.print_hit()
    print("---")
    pagerank(graph)
    graph.print_pagerank()
    print("---")
    simrank(graph, show=True)
