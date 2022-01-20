import math
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class Point:
    x = 0
    vx = 0
    y = 0
    vy = 0
    z = 0
    vz = 0
    r = 1
    color: QColor = Qt.red

    def xyz_constructor(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def xyz_r_constructor(self, x: float, y: float, z: float, r: float):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def xyz_velocity_constructor(self, x: float, vx: float, y: float, vy: float, z: float, vz: float):
        self.x = x
        self.vx = vx
        self.y = y
        self.vy = vy
        self.z = z
        self.vz = vz

    def xyz_r_velocity_constructor(self, x: float, vx: float, y: float, vy: float, z: float, vz: float, r: float):
        self.x = x
        self.vx = vx
        self.y = y
        self.vy = vy
        self.z = z
        self.vz = vz
        self.r = r

    def __init__(self, *args: float):
        if len(args) == 3:
            self.xyz_constructor(args[0], args[1], args[2])
        elif len(args) == 4:
            self.xyz_r_constructor(args[0], args[1], args[2], args[3])
        elif len(args) == 6:
            self.xyz_velocity_constructor(args[0], args[1], args[2], args[3], args[4], args[5])
        elif len(args) == 7:
            self.xyz_r_velocity_constructor(args[0], args[1], args[2], args[3], args[4], args[5], args[6])
        else:
            print("INVALID CONSTRUCTOR")

    def __str__(self):
        return "(" + self.x + ", " + self.y + ", " + self.z + ")"

    def copy(self):
        return Point(self.x, self.y, self.z)

    def dist(self, p):
        return math.sqrt(((self.x - p.x) ** 2) + ((self.y - p.y) ** 2) + ((self.z - p.z) ** 2))

    def dist_squared(self, p):
        return ((self.x - p.x) ** 2) + ((self.y - p.y) ** 2) + ((self.z - p.z) ** 2)

    def vector_length(self):
        return math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

    def dot(self, p):
        return (self.x * p.x) + (self.y * p.y) + (self.z * p.z)

    def cross(self, p):
        return Point((self.y * p.z) - (self.z * p.y),
                     -((self.x * p.z) - (self.z * p.x)),
                     (self.x * p.y) - (self.y * p.x))

    def add(self, p):
        self.x += p.x
        self.y += p.y
        self.z += p.z

    def substract(self, p):
        self.x -= p.x
        self.y -= p.y
        self.z -= p.z

    def mult(self, m: float):
        self.x *= m
        self.y *= m
        self.z *= m

    def normalize(self):
        len = self.vector_length()
        if len == 1:
            return
        if len > 0:
            self.mult(1 / self.vector_length())
        else:
            print("VECTOR ZERO LENGTH")
