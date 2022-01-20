import math

from Point import Point
from Line import Line

TURN_AMOUNT = 0.25
TURN_ANGLE = 0.1


class Observer(Line):
    generated_directions = []

    def __init__(self, direction: Line):
        super().__init__(direction.p1, direction.p2)
        self.normalize()

    def turn_right(self):
        sin = math.sin(TURN_ANGLE)
        cos = math.cos(TURN_ANGLE)
        old = self.p2.copy()
        self.p2.x = (old.x * cos) + (old.y * (-sin))
        self.p2.y = (old.x * sin) + (old.y * cos)
        self.normalize()

    def turn_left(self):
        sin = math.sin(-TURN_ANGLE)
        cos = math.cos(-TURN_ANGLE)
        old = self.p2.copy()
        self.p2.x = (old.x * cos) + (old.y * (-sin))
        self.p2.y = (old.x * sin) + (old.y * cos)
        self.normalize()

    def turn_up(self):
        sin = math.sin(-TURN_ANGLE)
        cos = math.cos(-TURN_ANGLE)
        old = self.p2.copy()
        self.p2.x = (old.x * cos) + (old.z * sin)
        self.p2.z = (old.x * (-sin)) + (old.z * cos)
        self.normalize()

    def turn_down(self):
        sin = math.sin(TURN_ANGLE)
        cos = math.cos(TURN_ANGLE)
        old = self.p2.copy()
        self.p2.x = (old.x * cos) + (old.z * sin)
        self.p2.z = (old.x * (-sin)) + (old.z * cos)
        self.normalize()

    def generate_directions(self, n_width: int, n_height: int, step: float):
        self.generated_directions = [Line(Point(0, 0, 0, 0), Point(0, 0, 0, 0))] * (n_width * n_height)
        for z in range(n_height):
            for y in range(n_width):
                newLine = Line(self.p1.copy(), Point(self.p2.x,
                                                     self.p2.y + ((y - (n_width / 2)) * step),
                                                     self.p2.z + ((z - (n_height / 2)) * step)))
                # newLine = Line(self.p1.copy(),
                #                Point(self.p2.x, y * step, z * step, 0))
                newLine.normalize()
                self.generated_directions[(z * n_width) + y] = newLine
