from utility import Graph
import numpy as np
import math


class simrank:
    def __init__(self, graph, c=0.9):
        self.table = dict()
        self.graph = graph
        self.c = c

    def similarity(self, point1, point2):
        hash_val = hash(str(point1) + str(point2))
        if hash_val in self.table.keys():
            return self.table[hash_val][2]
        if len(point1.linkFrom) == 0 or len(point2.linkFrom) == 0:
            self.table[hash_val] = (point1, point2, 0)
            return self.table[hash_val][2]
        _sum = 0
        for p1 in point1.linkFrom:
            for p2 in point2.linkFrom:
                _sum += self.similarity(p1, p2)
        self.table[hash_val] = (point1, point2, self.c * _sum / len(point1.linkFrom) / len(point2.linkFrom))
        return self.table[hash_val][2]

    def calculate(self):
        self.table = dict()
        for i in range(len(self.graph)):
            for j in range(i, len(self.graph)):
                p1 = self.graph.index(i)
                p2 = self.graph.index(j)
                hash_val = hash(str(p1) + str(p2))
                if hash_val not in self.table.keys():
                    self.table[hash_val] = (p1, p2, self.similarity(p1, p2))

    def print_result(self):
        print("SimRank")
        for val in self.table.values():
            print("S({}, {}) --> {}".format(val[0], val[1], val[2]))


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
        if sum(pagerank_old[i] - pagerank_current[i] for i in range(len(pagerank_current))) < epsilon:
            break


def simrank_(graph, c=0.8, epsilon=0.1, show=False):
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
        if np.linalg.det(np.subtract(sim_old, sim)) < epsilon:
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
    simrank_(graph, show=True)
