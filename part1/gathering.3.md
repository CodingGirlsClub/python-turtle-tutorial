### 第三次聚会任务

小组成员相互协作，按要求思考并完成：
+ 设计`Theseus`类，继承`turtle.Turtle`类，有方法`up`，`down`，`left`，`right`分别表示上下左右移动一格。
+ 设计`Labyrinth`类，用`list`对象存储迷宫格子之间的连通情况。
+ 设计`Labyrinth`类的`is_valid_move`方法，判断从某个格子向某方向走一格是否会撞墙。
+ 设计`Labyrinth`类的`draw`方法，将迷宫画出来。
+ 一个“合格”的迷宫是指，迷宫中的每个格子相互之间连通，并且再建任何一道墙都会让迷宫变得不连通。
设计`Labyrinth`类的`is_connected`方法，判断迷宫是否连通。
+ 设计`Labyrinth`类的`get_next_wall`方法，判断迷宫是否还有可以加上的墙，如果有，返回其中任意一道，否则返回`None`。
+ 设计`Labyrinth`类的`__init__`方法，从头开始生成一个迷宫。
+ 分析你生成迷宫这个过程的时间复杂度。
+ 利用`turtle`模块的`onkey`方法，实现按一下方向键，小海龟就走一步。

提示：
+ 注意根据需要添加合适的方法、属性。
