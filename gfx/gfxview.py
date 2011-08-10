import math
import random

from PySide import QtCore, QtGui

class GfxView(QtGui.QGraphicsView):

    def __init__(self, parent=None):
        super(GfxView, self).__init__(parent)
        self.scene = QtGui.QGraphicsScene(self)
        self.setScene(self.scene)
        gradient = QtGui.QRadialGradient(0, 0, 250)
        gradient.setColorAt(1, QtCore.Qt.black)
        gradient.setColorAt(0, QtCore.Qt.lightGray)
        self.scene.setBackgroundBrush(gradient)
        self.setSceneRect(-200, -200, 400, 400)

        self.populate()

        box = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(':/laptop.png'))
        self.scene.addItem(box)
        self.scale(.5, .5)
        box.setOffset(-64, -64)

    def animate(self):
        random.shuffle(self.in_items)
        random.shuffle(self.out_items)
        for i in range(self.n / 3):
            self.in_items[i].animate()
            self.out_items[i].animate()

    def populate(self):
        n = 10
        self.n = n
        r = 400
        dt = 2 * math.pi / n
        offset = 15
        self.in_items, self.out_items = [], []
        ingradient = QtGui.QRadialGradient(0, 0, offset)
        ingradient.setColorAt(0, QtCore.Qt.red)
        ingradient.setColorAt(1, QtCore.Qt.lightGray)
        for i in range(n):
            radian = i * dt
            x = r * math.cos(radian)
            y = r * math.sin(radian)

            item = ArrowItem(x, y, radian)
            self.scene.addItem(item)
            self.in_items.append(item)

            item = ArrowItem(x, y, radian, False)
            self.scene.addItem(item)
            self.out_items.append(item)

class ArrowItem(QtGui.QGraphicsPixmapItem):

    def __init__(self, x, y, angle, is_in=True):
        super(ArrowItem, self).__init__()
        pixmap = QtGui.QPixmap(':/green_arrow.png' if is_in else ':/red_arrow.png')
        transform = QtGui.QTransform()
        if is_in:
            transform.rotateRadians(angle - math.pi / 2)
            self.setOffset(x-24, y-24)
        else:
            transform.rotateRadians(angle + math.pi / 2)
            self.setOffset(-24, -24)
        self.arrow = pixmap.transformed(transform)
        self.setPixmap(self.arrow)
        self.hide()
        self.animation = QtGui.QGraphicsItemAnimation()
        self.timeline = QtCore.QTimeLine(1000)
        self.timeline.setFrameRange(0, 100)
        self.animation.setScaleAt(.8, 0, 0)
        self.animation.setScaleAt(0, 1, 1)
        if not is_in:
            self.animation.setPosAt(0, QtCore.QPointF(0, 0))
            self.animation.setPosAt(.8, QtCore.QPointF(-x, -y))
        self.animation.setItem(self)
        self.animation.setTimeLine(self.timeline)
        self.timeline.finished.connect(self.finished_animation)

    def animate(self):
        self.show()
        if self.timeline.state() == QtCore.QTimeLine.NotRunning:
            self.timeline.start()

    def finished_animation(self):
        self.hide()

class ByteItem(QtGui.QGraphicsEllipseItem):

    def __init__(self, x, y, radius, is_in=True):
        if is_in:
            super(ByteItem, self).__init__(x - radius, y - radius, radius, radius)
        else:
            super(ByteItem, self).__init__(-radius, -radius, radius, radius)
        self.setBrush(QtGui.QBrush(QtCore.Qt.red if is_in else QtCore.Qt.green))
        self.setPen(QtCore.Qt.NoPen)
        self.x, self.y = x, y
        self.hide()
        self.animation = QtGui.QGraphicsItemAnimation()
        self.timeline = QtCore.QTimeLine(1000)
        self.timeline.setFrameRange(0, 100)
        self.animation.setPosAt(1., QtCore.QPointF(-self.x, -self.y))
        self.animation.setPosAt(0., QtCore.QPointF(0, 0))
        self.animation.setItem(self)
        self.animation.setTimeLine(self.timeline)
        self.timeline.finished.connect(self.finished_animation)

    def animate(self):
        self.show()
        if self.timeline.state() == QtCore.QTimeLine.NotRunning:
            self.timeline.start()

    def finished_animation(self):
        self.hide()

if __name__ == '__main__':
    import resources
    app = QtGui.QApplication([])
    view = GfxView()
    view.show()
    raise SystemExit(app.exec_())

