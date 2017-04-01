from PyQt5 import QtCore, QtGui, QtWidgets


class ImageLabel(QtWidgets.QLabel):

    def __init__(self, parent):
        super().__init__(parent)
        self.points = []
        self.twin = None
        self.locked = True

    def paintEvent(self, a0: QtGui.QPaintEvent):
        super().paintEvent(a0)
        qp = QtGui.QPainter()
        qp.begin(self)
        pen = QtGui.QPen(QtCore.Qt.black, 4, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        for point in self.points:
            qp.drawPoint(point)
        qp.end()

    def mousePressEvent(self, ev: QtGui.QMouseEvent):
        if not self.locked:
            self.points.append(ev.pos())
            self.lock()
            self.twin.release()
            self.update()

    def delete(self):
        if len(self.points) == 0:
            return
        del self.points[-1]
        self.update()

    def delete_all(self):
        self.points = []
        self.update()

    def set_twin(self, twin):
        self.twin = twin

    def lock(self):
        self.locked = True

    def release(self):
        self.locked = False

    def is_locked(self) -> bool:
        return self.locked

    def get_points(self) -> list:
        return self.points

