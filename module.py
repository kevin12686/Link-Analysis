from utility import Graph
import math


def hits(graph, epsilon=0.15):
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


if __name__ == '__main__':
    graph = Graph("dataset/graph_4.txt")
    hits(graph)
    graph.print()