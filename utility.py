import os
import re


class Point:
    def connectTo(self, point):
        self.linkTo.add(point)
        point.connectFrom(self)

    def connectFrom(self, point):
        self.linkFrom.add(point)

    def __init__(self, identification, auth=1, hub=1):
        self.identification = identification
        self.linkTo = set()
        self.linkFrom = set()
        self.auth = auth
        self.hub = hub

    def __repr__(self):
        return "<utility.Point object (id: {}, auth: {}, hub: {})>".format(self.identification, self.auth, self.hub)

    def __hash__(self):
        return hash(self.identification)

    def __eq__(self, other):
        return self.identification == other.identification


class Graph:
    Pattern = re.compile(r"(\d+),(\d+)")

    def print(self):
        for p in self.iterpoints():
            print("ID: {} --> (Auth: {}, Hub: {})".format(p.identification, p.auth, p.hub))

    def iterpoints(self):
        return self.points

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
