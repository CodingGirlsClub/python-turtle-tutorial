# coding: utf-8

import sympy
import random
import turtle
import networkx
from sympy import geometry
from collections import deque


class UnionFind(object):

    def __init__(self, nodes):
        self.__uf = {node: node for node in nodes}

    def is_same(self, x, y):
        return self.__root(x) == self.__root(y)

    def __root(self, x):
        if self.__uf[x] == x:
            return x
        root = self.__root(self.__uf[x])
        self.__uf[x] = root
        return root

    def union(self, x, y):
        root_x = self.__root(x)
        root_y = self.__root(y)
        self.__uf[root_x] = root_y


class Maze(object):

    def __init__(self, base_polygons, transforms, bounds):
        # base_polygons = map(geometry.Polygon, base_polygons)
        self.connection = networkx.Graph()
        self.xmin, self.ymin, self.xmax, self.ymax = bounds.bounds
        self.lines = {}
        bfs_polygons = deque()
        for p in filter(self.polygon_in_maze, base_polygons):
            self.add_polygon(p)
            bfs_polygons.append(p)
        while bfs_polygons:
            p = bfs_polygons.popleft()
            print(p)
            for transform in transforms:
                p_transformed = transform(p)
                if self.polygon_in_maze(p_transformed):
                    if self.add_polygon(p_transformed):
                        bfs_polygons.append(p_transformed)
        self.break_walls()
        # self.draw()

    def polygon_in_maze(self, polygon):
        xmin, ymin, xmax, ymax = polygon.bounds
        return self.xmin <= xmin <= xmax <= self.xmax and self.ymin <= ymin <= ymax <= self.ymax

    def add_polygon(self, polygon):
        if self.connection.has_node(polygon):
            return False
        for line in polygon.sides:
            if line in self.lines:
                self.connection.add_edge(polygon, self.lines[line], weight=line)
            else:
                self.lines[line] = polygon
        return True

    def break_walls(self):
        s = UnionFind(self.connection.nodes)
        self.walls = set()
        shuffle = list(self.connection.edges)
        random.shuffle(shuffle)
        for edge in shuffle:
            line = self.connection.edges[edge]['weight']
            if not s.is_same(edge[0], edge[1]):
                s.union(edge[0], edge[1])
                self.walls.add(line)

    def draw(self):
        for p in self.connection.nodes:
            for line in p.sides:
                if line not in self.walls:
                    self.draw_line(line)

    def draw_line(self, line):
        turtle.pu()
        u, v = line.points
        turtle.goto(u.x.evalf(), u.y.evalf())
        turtle.pd()
        turtle.goto(v.x.evalf(), v.y.evalf())


def main():
    SCREEN_SIZE = [400, 400]
    # PADDING = [50, 50]
    # turtle.mode("logo")
    # turtle.setup(SCREEN_SIZE[0] + PADDING[0], SCREEN_SIZE[1] + PADDING[0], 0, 0)
    # turtle.setworldcoordinates(-PADDING[0]/2, -PADDING[1]/2, SCREEN_SIZE[0]+PADDING[0]/2, SCREEN_SIZE[1]+PADDING[0]/2)
    SCALE = 5
    Maze(
        [
            geometry.Polygon(
                (-1, sympy.sqrt(3)),
                (1, sympy.sqrt(3)),
                (2, 0),
                (1, -sympy.sqrt(3)),
                (-1, -sympy.sqrt(3)),
                (-2, 0),
            ).translate(2, 2).scale(SCALE, SCALE),
        ],
        [
            lambda p: p.translate(0, sympy.sqrt(3) * 2 * SCALE),
            lambda p: p.translate(0, -sympy.sqrt(3) * 2 * SCALE),
            lambda p: p.translate(1.5 * 2 * SCALE, sympy.sqrt(3) / 2 * 2 * SCALE),
            lambda p: p.translate(-1.5 * 2 * SCALE, -sympy.sqrt(3) / 2 * 2 * SCALE),
        ],
        geometry.Polygon((0, 0), (SCREEN_SIZE[0], SCREEN_SIZE[1]))
    )
    # turtle.mainloop()

if __name__ == "__main__":
    main()