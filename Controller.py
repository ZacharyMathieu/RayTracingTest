from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt5.QtCore import Qt, QRect, QSize
from Model import Model
from Observer import Observer
from Point import Point
from Line import Line
import math


def average_color(color_list: list) -> QColor:
    red = 0
    green = 0
    blue = 0
    alpha = 0
    if len(color_list) == 0:
        return Qt.white
    else:
        # more strength = less color (because bounced later)
        strength = 1
        for c in color_list:
            color = QColor(c)
            red += color.red() / strength
            green += color.green() / strength
            blue += color.blue() / strength
            alpha += color.alpha() / strength
            strength += 1
        return QColor(red / len(color_list), green / len(color_list), blue / len(color_list), min(alpha, 255))
        # return color_list[0]


def adjust_color(index, color: QColor) -> QColor:
    # return QColor(color.red() / index, color.green() / index, color.blue() / index, color.alpha() / index)
    return QColor(color.red(), color.green(), color.blue(), color.alpha() / index)


class Controller:
    model = Model()
    observer = Observer(Line(Point(-1, 0, 0), Point(1, 0, 0.2)))
    display_mode = 2
    SCALE_2D = 50
    N_RAYS_H = 100
    STEP = 1 / N_RAYS_H
    RENDER_DISTANCE = 50

    def __init__(self):
        pass

    # self.observer.z = -0.25

    def up(self):
        # TODO Normaliser vecteur de direction de obs
        print("UP")
        self.observer.turn_up()

    def down(self):
        print("DOWN")
        self.observer.turn_down()

    def right(self):
        print("RIGHT")
        self.observer.turn_right()

    def left(self):
        print("LEFT")
        self.observer.turn_left()

    def w_key(self):
        print("W")
        self.observer.move_forward(1)

    def s_key(self):
        print("S")
        self.observer.move_forward(-1)

    def d_key(self):
        print("D")
        self.observer.move_sideways(1)

    def a_key(self):
        print("A")
        self.observer.move_sideways(-1)

    def plus_key(self):
        print("PLUS")
        if self.display_mode < 2:
            self.display_mode += 1

    def minus_key(self):
        print("MINUS")
        if self.display_mode > 0:
            self.display_mode -= 1

    def add_rays(self):
        print("More rays!")
        self.N_RAYS_H += 1
        self.STEP = 1 / self.N_RAYS_H

    def remove_rays(self):
        print("Less rays!")
        if self.N_RAYS_H > 0:
            self.N_RAYS_H -= 1
            self.STEP = 1 / self.N_RAYS_H

    def clear_display(self, painter: QPainter, size: QSize):
        painter.fillRect(0, 0, size.width(), size.height(), Qt.white)

    def display(self, painter: QPainter, size: QSize):
        if self.display_mode == 0:
            self.display2D(painter, size)
        elif self.display_mode == 1:
            self.displayRayTracingM1(painter, size)
        elif self.display_mode == 2:
            self.displayRayTracingM2(painter, size)

    def display2D(self, painter: QPainter, size: QSize):
        # print("DISPLAY DE CONTROLLER")
        # painter.setPen(QPen(Qt.white, 5, Qt.SolidLine))
        # self.clear_display(painter, size)
        painter.setPen(Qt.black)
        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        for p in self.model.liste:
            # painter.drawPoint(p.y * SCALE_2D, p.z * SCALE_2D)
            painter.drawEllipse(((p.y - p.r - self.observer.p1.y) * self.SCALE_2D) + (size.width() / 2),
                                size.height() - ((p.z + p.r - self.observer.p1.z) * self.SCALE_2D),
                                (p.r * 2) * self.SCALE_2D,
                                (p.r * 2) * self.SCALE_2D)

    def displayRayTracingM1(self, painter: QPainter, size: QSize):
        # print("DISPLAY RAY TRACING")
        # self.clear_display(painter, size)
        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))

        pixel_width = size.width() / self.N_RAYS_H
        N_RAYS_V = int(size.height() / pixel_width)
        # pixel_height = size.height() / N_RAYS_V
        # self.observer.generateDirections(Point2D(0, 0, 0), N_RAYS_H, N_RAYS_V, 1)
        for z in range(N_RAYS_V):
            for y in range(self.N_RAYS_H):
                # for l in self.observer.directions:
                line = Line(self.observer.p1, Point(self.observer.p2.x,
                                                    self.observer.p2.y + ((y - (self.N_RAYS_H / 2)) * self.STEP),
                                                    self.observer.p2.z + ((z - (N_RAYS_V / 2)) * self.STEP)))
                for p in self.model.liste:
                    dist = line.distPoint(p)
                    if dist <= p.r:
                        # print("AT: " + line.p2.__str__())
                        # color_val = int(255 * (1 - (dist / p.r)))
                        # painter.setBrush(QBrush(QColor(255, color_val, color_val), Qt.SolidPattern))
                        color_val = int(255 * (dist / p.r))
                        color = QColor(p.color)
                        color.setAlpha(color_val)
                        painter.setBrush(color)
                        painter.drawRect(y * pixel_width, size.height() - (z * pixel_width), pixel_width + 0.5,
                                         pixel_width + 0.5)
                        break

    def displayRayTracingM2(self, painter: QPainter, size: QSize):
        # print("DISPLAY RAY TRACING 2")
        # self.clear_display(painter, size)
        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(Qt.black)

        pixel_width = (size.width() / self.N_RAYS_H)
        N_RAYS_V = int(size.height() / pixel_width) + 1
        self.observer.generate_directions(self.N_RAYS_H, N_RAYS_V, self.STEP)
        for z in range(N_RAYS_V):
            for y in range(self.N_RAYS_H):
                line = self.observer.generated_directions[(z * self.N_RAYS_H) + y]
                color = self.get_ray_color(line)
                painter.setBrush(color)
                painter.drawRect(y * pixel_width, size.height() - (z * pixel_width), pixel_width + 1,
                                 pixel_width + 1)

    def get_ray_color(self, line: Line) -> QColor:
        total_distance = 0
        # bounced = []
        # index_bounced = 0
        # colors = []
        color = Qt.white
        loop_count = 0
        collision = False
        final_dist_data = 0
        # while total_distance < self.RENDER_DISTANCE:
        #     new_distance = self.distance_closest_point(line.p1, bounced)
        #     if new_distance[1] is not None:
        #         total_distance += new_distance[0]
        #         if new_distance[0] < new_distance[1].r:
        #             color_val = int(255 * (new_distance[0] / new_distance[1].r))
        #             color = QColor(new_distance[1].color)
        #             color.setAlpha(color_val)
        #             bounced.append(new_distance[1])
        #             colors.append(color)
        #             # TODO B O U N C E dat boi
        #             break
        #             # line.p2.mult(-1)
        #         else:
        #             line.move_forward(new_distance[0])
        #     else:
        #         break
        new_distance = self.distance_closest_point(line.p1, [])
        while new_distance[0] < self.RENDER_DISTANCE:
            final_dist_data += new_distance[0] / 15
            if new_distance[1] is not None:
                if new_distance[0] < new_distance[1].r:
                    color = new_distance[1].color
                    # final_dist_data = max(new_distance[0], 1)
                    # final_dist_data = 1
                    collision = True
                    break
            line.move_forward(new_distance[0])
            loop_count += 1
            new_distance = self.distance_closest_point(line.p1, [])

        # return adjust_color(final_dist_data, color) if collision else Qt.white
        return color if collision else Qt.white

    def distance_closest_point(self, p: Point, ignored: list) -> list:
        return self.model.distance_closest_point(p, ignored)

    def loop(self, speed: float):
        self.model.loop(speed)
