import os
import re


class Point:
    def updatePagerank(self):
        self.pagerank = self.newpagerank

    def newPagerank(self, val):
        self.newpagerank = val

    def connectTo(self, point):
        self.linkTo.add(point)
        point.connectFrom(self)

    def connectFrom(self, point):
        self.linkFrom.add(point)

    def __init__(self, identification, auth=1, hub=1, pagerank=1):
        self.identification = identification
        self.linkTo = set()
        self.linkFrom = set()
        self.auth = auth
        self.hub = hub
        self.pagerank = pagerank

    def __repr__(self):
        return "<utility.Point object (id: {}, auth: {}, hub: {})>".format(self.identification, self.auth, self.hub)

    def __str__(self):
        return self.identification

    def __hash__(self):
        return hash(self.identification)

    def __eq__(self, other):
        return self.identification == other.identification


class Graph:
    Pattern = re.compile(r"(\d+),(\d+)")

    def print_pagerank(self):
        print("PageRank")
        for p in self.iterpoints():
            print("ID: {} --> {}".format(p, float(p.pagerank)))

    def initPagerank(self):
        for p in self.iterpoints():
            p.newPagerank(1 / self.__len__())
        self.updateAllPagerank()

    def updateAllPagerank(self):
        for p in self.iterpoints():
            p.updatePagerank()

    def print_hit(self):
        print("HITS")
        for p in self.iterpoints():
            print("ID: {} --> (Auth: {}, Hub: {})".format(p, float(p.auth), float(p.hub)))

    def iterpoints(self):
        return self.points

    def index(self, idx):
        return self.points[idx]

    def indexOf(self, point):
        for i in range(len(self.points)):
            if self.points[i] == point:
                return i
        return -1

    def get_or_create(self, identification):
        created = False
        try:
            obj = self.__getitem__(identification)
        except KeyError:
            obj = Point(identification)
            created = True
            self.points.append(obj)
        return obj, created

    def __init__(self, file):
        pwd = os.getcwd()
        self.points = list()
        with open(os.path.join(pwd, file), "r") as f:
            for data in re.finditer(self.Pattern, f.read()):
                point1, _ = self.get_or_create(data[1])
                point2, _ = self.get_or_create(data[2])
                point1.connectTo(point2)

    def __getitem__(self, identification):
        for idx in range(len(self.points)):
            if self.points[idx].identification == identification:
                return self.points[idx]
        raise KeyError

    def __len__(self):
        return len(self.points)
