# coding: utf-8
# http://www.matrix67.com/blog/archives/6231

import turtle
import math


def dragon_curve(x, n):
    if not n:
        turtle.fd(x)
        return
    turtle.rt(45)
    dragon_curve(x/math.sqrt(2), n-1)
    turtle.lt(90)
    turtle.pu()
    turtle.fd(x/math.sqrt(2))
    turtle.pd()
    turtle.rt(180)
    dragon_curve(x/math.sqrt(2), n-1)
    turtle.rt(180)
    turtle.pu()
    turtle.fd(x/math.sqrt(2))
    turtle.pd()
    turtle.rt(45)


def h_fractal(x, n):
    for i in range(2):
        turtle.lt(90)
        turtle.fd(x/2)
        if n:
            h_fractal(x*0.7, n-1)
        turtle.bk(x/2)
        turtle.lt(90)


def koch_curve(x, n):
    if not n:
        turtle.fd(x)
        return
    koch_curve(x/3, n-1)
    turtle.lt(60)
    koch_curve(x/3, n-1)
    turtle.rt(120)
    koch_curve(x/3, n-1)
    turtle.lt(60)
    koch_curve(x/3, n-1)
