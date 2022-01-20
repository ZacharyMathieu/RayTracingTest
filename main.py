from Controller import Controller
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPainter, QPaintEvent, QPen
from PyQt5.QtCore import QThread, QObject, Qt, QSize, QTimer
import sys

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080


class MainWindow(QMainWindow):
    controller = Controller()
    painter = None
    timer = None

    FPS = 16
    MSPF = int(1000 / FPS)

    # thread = QThread()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ray Tracing Experiment")

        # self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # self.painter = QPainter(self)

        # self.worker = Worker(self.next_frame)
        # self.thread = QThread()
        # # thread = QThread()
        # self.worker.moveToThread(self.thread)
        # self.thread.started.connect(self.worker.start)
        # self.thread.finished.connect(self.worker.stop)
        # self.thread.start()
        self.start()

        self.show()

    def start(self):
        if self.timer is not None:
            self.timer.deleteLater()
        # else:
        self.timer = QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.setInterval(self.MSPF)  # in milliseconds, so 5000 = 5 seconds
        self.timer.timeout.connect(self.next_frame)
        self.timer.start()

    def paintEvent(self, event):
        if self.painter is None:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.NoPen))
        # try:
        # self.controller.displayRayTracing(painter,
        #                                   QSize(WINDOW_WIDTH, WINDOW_HEIGHT))
        # self.controller.displayRayTracingMethod2(painter,
        #                                          QSize(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.controller.display(painter, self.size())

        # except Exception:
        # pass
        painter.end()

    def next_frame(self):
        self.controller.loop(1 / self.FPS)
        # self.paintEvent(None)
        self.repaint()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.controller.up()
        elif event.key() == Qt.Key_Down:
            self.controller.down()
        elif event.key() == Qt.Key_Left:
            self.controller.left()
        elif event.key() == Qt.Key_Right:
            self.controller.right()
        elif event.key() == Qt.Key_W:
            self.controller.w_key()
        elif event.key() == Qt.Key_S:
            self.controller.s_key()
        elif event.key() == Qt.Key_D:
            self.controller.d_key()
        elif event.key() == Qt.Key_A:
            self.controller.a_key()
        elif event.key() == Qt.Key_Plus:
            self.controller.plus_key()
        elif event.key() == Qt.Key_Minus:
            self.controller.minus_key()
        elif event.key() == Qt.Key_Asterisk:
            print("MULTIPLY")
            self.FPS = self.FPS * 2
            self.MSPF = int(1000 / self.FPS)
            self.start()
        elif event.key() == Qt.Key_Slash:
            print("DIVIDE")
            self.FPS = self.FPS / 2
            self.MSPF = int(1000 / self.FPS)
            self.start()
        elif event.key() == Qt.Key_Period:
            self.controller.add_rays()
        elif event.key() == Qt.Key_Comma:
            self.controller.remove_rays()
        elif event.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication([])

    window = MainWindow()
    # window.show()

    app.exec()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
