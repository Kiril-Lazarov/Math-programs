from abc import ABC, abstractmethod
import turtle


class Ball(ABC, turtle.Turtle):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_coordinates(self):
        pass


class CircleBall(Ball):
    def __init__(self):
        super().__init__()
        self.shape('circle')
        self.color('black')
        self.penup()


    def get_coordinates(self):
        return 1


class SquareBall(Ball):
    def __init__(self):
        super().__init__()

        self.shape('square')
        self.color('orange')
        self.penup()


    def get_coordinates(self):
        return 1


class TriangleBall(Ball):
    def __init__(self):
        super().__init__()

        self.shape('triangle')
        self.color('orange')
        self.shapetransform()
        self.penup()


    def get_coordinates(self):
        return 1
