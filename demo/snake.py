# coding: utf-8

import turtle
import random
from collections import deque

DIST = 4
BORDER = 4
N, M = 24, 24
START_X, START_Y = N / 2, M / 2
DOT_SIZE = 5
SCREEN_SIZE = (M * (DOT_SIZE * 2 + DIST) + BORDER * 2 - DIST, N * (DOT_SIZE * 2 + DIST) + BORDER * 2 - DIST)
INIT_VELOCITY = 300
DECAY = 0.03
SCREEN = turtle.getscreen()


class DotShape(turtle.Shape):

    SIZE = DOT_SIZE
    SHAPE = [(SIZE, SIZE), (-SIZE, SIZE), (-SIZE, -SIZE), (SIZE, -SIZE)]
    COLOR = 'black'

    def __init__(self):
        super(DotShape, self).__init__("compound")
        self.addcomponent(self.SHAPE, self.COLOR, self.COLOR)


class EventMixin(object):

    def register(self, **kwargs):
        for arg, func in kwargs.iteritems():
            if arg.startswith('on_'):
                setattr(self, arg, func)


class Dot(turtle.Turtle, EventMixin):

    def __init__(self, i, j, **kwargs):
        super(Dot, self).__init__()
        self.register(**kwargs)
        self.shape('dot')
        self.speed(0)
        self.pu()
        self.ht()
        self.i = i
        self.j = j
        self.x = j * (DotShape.SIZE * 2 + DIST) + BORDER + DotShape.SIZE
        self.y = (N - i - 1) * (DotShape.SIZE * 2 + DIST) + BORDER + DotShape.SIZE
        self.setpos(self.x, self.y)
        self.neighbor = {}
        self.body = False
        self.food = False

    def eaten(self):
        assert(self.food and not self.body)
        self.food = False
        self.ht()

    def become_food(self):
        assert(not self.food and not self.body)
        self.food = True
        self.st()

    def in_body(self):
        assert(not self.body)
        on_eaten = False
        if self.food:
            on_eaten = True
            self.eaten()
        self.body = True
        if on_eaten:
            self.on_eaten()
        self.st()

    def out_body(self):
        assert(self.body and not self.food)
        self.body = False
        self.ht()


class Dots(object):

    def __init__(self, N, M):
        self.N = N
        self.M = M
        self.dots = [[None for j in range(M)] for i in range(N)]
        for i in range(N):
            for j in range(M):
                self.dots[i][j] = Dot(i, j, on_eaten=self.find_food)
                if random.randint(1, 2) == 1:
                    self.dots[i][j].st()
        self.ht()
        for i in range(N):
            for j in range(M):
                if 0 < i:
                    self.dots[i][j].neighbor[(-1, 0)] = self.dots[i-1][j]
                if i < N - 1:
                    self.dots[i][j].neighbor[(1, 0)] = self.dots[i+1][j]
                if 0 < j:
                    self.dots[i][j].neighbor[(0, -1)] = self.dots[i][j-1]
                if j < M - 1:
                    self.dots[i][j].neighbor[(0, 1)] = self.dots[i][j+1]

    def __getitem__(self, x):
        assert(isinstance(x, tuple) and len(x) == 2)
        x = (int(x[0]), int(x[1]))
        return self.dots[x[0]][x[1]]

    def find_food(self):
        while True:
            i, j = random.randint(0, self.N - 1), random.randint(0, self.M - 1)
            try:
                self[i, j].become_food()
            except:
                continue
            break

    def ht(self):
        for i in range(self.N):
            for j in range(self.M):
                self.dots[i][j].ht()


class Snake(deque, EventMixin):

    def __init__(self, body, **kwargs):
        super(Snake, self).__init__()
        self.register(**kwargs)
        for b in body:
            self.append(b)
        self.head = body[-1]
        self.direction = (0, 0)
        self.init_velocity = INIT_VELOCITY
        self.decay_rate = DECAY ** (1 / float(N * M))

    def change_direction(self, direction):
        self.direction = direction

    def append(self, x):
        super(Snake, self).append(x)
        x.in_body()

    def popleft(self):
        x = super(Snake, self).popleft()
        x.out_body()

    def start(self):
        self.move()

    def move(self):
        if self.__len__() == N * M - 1:
            self.on_game_over()
        elif not self._move():
            self.on_game_over()

    def _move(self):
        if self.direction != (0, 0):
            next_pos = self.head.neighbor.get(self.direction)
            if not next_pos: # 撞墙
                return False
            if next_pos.body: # 撞自己
                return False
            if not next_pos.food:
                self.popleft()
            self.append(next_pos)
            self.head = next_pos
        turtle.ontimer(self.move, int(self.init_velocity * (self.decay_rate ** (self.__len__() - 1))))
        return True


class Board(object):

    def __init__(self, auto=False):
        auto = auto and N % 2 == 0 and M % 2 == 0
        self.dots = Dots(N, M)
        self.snake = Snake([self.dots[START_X, START_Y]], on_game_over=self.game_over)
        self.dots.find_food()
        if not auto:
            turtle.onkey(lambda: self.snake.change_direction((0, -1)), "Left")
            turtle.onkey(lambda: self.snake.change_direction((0, 1)), "Right")
            turtle.onkey(lambda: self.snake.change_direction((-1, 0)), "Up")
            turtle.onkey(lambda: self.snake.change_direction((1, 0)), "Down")
        self.over = False
        self.snake.start()
        if auto:
            turtle.ontimer(self.auto, 1500)

    def auto(self):
        if not self.over:
            i, j = self.snake.head.i, self.snake.head.j
            if 0 < j < M - 2 or (j == M - 2 and i in (0, N - 1)):
                direction = [(0, -1), (0, 1)][i % 2]
            if j == M - 1 and i not in (0, N - 1):
                direction = (-1, 0)
            if j == 0:
                direction = ([(1, 0), (0, 1)][i % 2])
            if j == M - 2 and 0 < i < N - 1:
                direction = ([(0, -1), (1, 0)][i % 2])
            if j == M - 1 and i in (0, N - 1):
                if i == 0:
                    direction = ((0, -1))
                else:
                    direction = ((-1, 0))
            if direction != self.snake.direction:
                self.snake.change_direction(direction)
            turtle.ontimer(self.auto, 5)

    def game_over(self):
        scribe = turtle.Turtle()
        scribe.setpos(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2 - M)
        self.dots.ht()
        scribe.write("GAME OVER!\nSCORE: %s" % (len(self.snake) - 1), align="center", font=("Courier", 2 * M, "bold"))
        self.over = True
        return


def main():
    turtle.mode("logo")
    turtle.register_shape('dot', DotShape())
    turtle.pu()
    turtle.setup(SCREEN_SIZE[0], SCREEN_SIZE[1], 0, 0)
    turtle.setworldcoordinates(0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1])
    turtle.setpos(0, 0)
    turtle.pd()
    turtle.setpos(0, SCREEN_SIZE[1])
    turtle.setpos(SCREEN_SIZE[0], SCREEN_SIZE[1])
    turtle.setpos(SCREEN_SIZE[0], 0)
    turtle.setpos(0, 0)
    turtle.ht()
    turtle.pu()
    turtle.setpos(-20, -20)
    Board(auto=False)
    turtle.listen()
    turtle.mainloop()


if __name__ == "__main__":
    main()
