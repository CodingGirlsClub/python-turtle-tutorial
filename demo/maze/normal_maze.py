# coding: utf-8

import random
import turtle

SIDE_LENGTH = 5


class Theseus(turtle.Turtle):

    def up(self):
        self.seth(90)
        self.fd(self.SIDE_LENGTH)

    def down(self):
        self.seth(270)
        self.fd(self.SIDE_LENGTH)

    def left(self):
        self.seth(180)
        self.fd(self.SIDE_LENGTH)

    def right(self):
        self.seth(0)
        self.fd(self.SIDE_LENGTH)


class Labyrinth(object):
    
    DIRECTIONS = [[0, -1], [-1, 0], [0, 1], [1, 0]]

    def __init__(self, nrow, ncol):
        self.connection = [[[1, 1, 1, 1] for i in range(ncol)] for i in range(nrow)]
        self.theseus = Theseus()
        self.theseus.speed(0)
        self.theseus.lt(90)
        self.nrow = nrow
        self.ncol = ncol
        self.break_walls()

    def draw(self):
        for row in range(self.nrow):
            for col in range(self.ncol):
                for i in range(4):
                    if self.connection[row][col][i] == 0:
                        self.theseus.pu()
                        self.theseus.fd(SIDE_LENGTH)
                        self.theseus.pd()
                    else:
                        self.theseus.fd(SIDE_LENGTH)
                    self.theseus.rt(90)
                self.theseus.rt(90)
                self.theseus.pu()
                self.theseus.fd(SIDE_LENGTH)
                self.theseus.pd()
                self.theseus.lt(90)
            self.theseus.pu()
            self.theseus.lt(90)
            self.theseus.fd(SIDE_LENGTH*self.ncol)
            self.theseus.rt(90)
            self.theseus.bk(SIDE_LENGTH)
            self.theseus.pd()

    def is_valid_move(self, row, col, direction):
        if self.connection[row][col][direction] == 1:
            return False
        return True
    
    def break_walls(self):
        connected_cells = set()
        possible_walls = set()
        start_cell = (random.randint(0, self.nrow-1), random.randint(0, self.ncol-1))
        connected_cells.add(start_cell)
        
        def add_possible_walls(x, y):
            for i, (dx, dy) in enumerate(self.DIRECTIONS):
                if 0 <= x + dx < self.nrow and 0 <= y + dy < self.ncol:
                    possible_walls.add(((x, y), i, (x+dx, y+dy)))
        add_possible_walls(*start_cell)
        while possible_walls:
            from_cell, direction, to_cell = possible_walls.pop()
            if to_cell not in connected_cells:
                connected_cells.add(to_cell)
                add_possible_walls(*to_cell)
                self.connection[from_cell[0]][from_cell[1]][direction] = 0
                self.connection[to_cell[0]][to_cell[1]][(direction+2)%4] = 0

SCREEN_SIZE = [400, 400]
PADDING = [80, 80]
turtle.mode("logo")
turtle.setup(SCREEN_SIZE[0] + PADDING[0], SCREEN_SIZE[1] + PADDING[0], 0, 0)
turtle.setworldcoordinates(-PADDING[0]/2, PADDING[1]/2, SCREEN_SIZE[0]+PADDING[0]/2, -SCREEN_SIZE[1]-PADDING[0]/2)
turtle.ht()
Labyrinth(80, 80).draw()
turtle.mainloop()