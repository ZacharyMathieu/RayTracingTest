from Point import Point


class Line:
    p1 = Point(0, 0, 0)
    p2 = Point(0, 0, 0)

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def pointOnLine2D(self, p: Point):
        newLinePoint = Point(self.p2.x - self.p1.x, self.p2.y - self.p1.y, self.p2.z - self.p1.z)
        newCirclePoint = Point(p.x - self.p1.x, p.y - self.p1.y, p.z - self.p1.z)
        newLinePoint.mult((newLinePoint.dot(newCirclePoint)) / newLinePoint.dot(newLinePoint))
        newLinePoint.add(self.p1)
        return newLinePoint

    def pointOnLine(self, p: Point):
        dist = self.p1.dist(self.p2)
        newLinePoint = Point((self.p2.x - self.p1.x) / dist,
                             (self.p2.y - self.p1.y) / dist,
                             (self.p2.z - self.p1.z) / dist)
        newCirclePoint = Point(p.x - self.p1.x, p.y - self.p1.y, p.z - self.p1.z)
        newLinePoint.mult(newLinePoint.dot(newCirclePoint))
        return newLinePoint

    def distPoint2D(self, p: Point):
        return (abs(((self.p2.x - self.p1.x) * (self.p1.y - p.y)) - ((self.p2.y - self.p1.y) * (self.p1.x - p.x)))) / \
               (self.p1.dist(self.p2))

    # def distPoint(self, p: Point2D):
    #     dist = self.p1.dist(self.p2)
    #     newLinePoint = Point2D((self.p2.x - self.p1.x) / dist,
    #                            (self.p2.y - self.p1.y) / dist,
    #                            (self.p2.z - self.p1.z) / dist)
    #     newCirclePoint = Point2D(p.x - self.p1.x, p.y - self.p1.y, p.z - self.p1.z)
    #     # newLinePoint.mult((newLinePoint.cross(newCirclePoint)) / newLinePoint.dot(newLinePoint))
    #     return ((newCirclePoint.cross(newLinePoint)).vector_length()) / (newLinePoint.vector_length())

    def distPoint(self, p: Point):
        return p.dist(self.pointOnLine(p))

    def move_forward(self, factor: float):
        added_value = self.p2.copy()
        added_value.mult(factor)
        self.p1.add(added_value)

    # Positive values = move right
    def move_sideways(self, factor: float):
        self.normalize()
        # added_value = Point(-self.p2.y, self.p2.x, self.p2.z)
        added_value = Point(0, 1, 0)
        added_value.mult(factor)
        self.p1.add(added_value)

    def normalize(self):
        # self.p2.substract(self.p1)
        self.p2.normalize()
        # self.p2.add(self.p1)

    # def distPoint(self, p: Point2D):
    #     return self.p1.dist(self.pointOnLine(p))
