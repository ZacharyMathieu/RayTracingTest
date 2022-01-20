import random

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from Point import Point
import math

N_POINTS = 6
G = -0.25


class Model:
    liste = [Point(0, 0, 0)] * N_POINTS

    def __init__(self):
        for i in range(N_POINTS):
            # self.liste[i] = Point(random.randrange(25, 30), random.randrange(-15, 15), random.randrange(5, 10),
            #                       random.randrange(4, 8))
            self.liste[i] = Point(random.randrange(10, 15), random.randrange(-10, 10), random.randrange(5, 15),
                                  4)
            self.liste[i].color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            # self.liste[i].r = random.randint(1, 10)

    def distance_closest_point(self, p: Point, ignored: list) -> list[float, Point]:
        min_dist = float("inf")
        min_point = None
        for point in self.liste:
            # d = p.dist(point) + point.r
            # d = p.dist(point)
            d = p.dist_squared(point)
            if d < min_dist:
                if (len(ignored) is 0) or (not ignored.__contains__(point)):
                    min_dist = d
                    min_point = point
        return [math.sqrt(min_dist), min_point]

    def loop(self, speed: float):
        for p in self.liste:
            # p.x = random.randrange(0, 100, 1)
            p.vz += G * speed
            p.z += p.vz * speed
            if p.z <= p.r:
                p.z = (p.r - p.z) + p.r
                p.vz = -p.vz
