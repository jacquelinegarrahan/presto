from qtpy import QtCore, QtWidgets, QtGui
import pyqtgraph.opengl as gl
import sys
import time


class Screen:
    """Core application


    Attributes
    ----------
    """

    def __init__(self, animation, data_queue):
        self._app = QtWidgets.QApplication(sys.argv)
        self._window = gl.GLViewWidget()
        self._window.setWindowTitle("Presto")
        self._window.setGeometry(0, 110, 1920, 1080)
        self._window.setCameraPosition(distance=50, elevation=12)
        self._window.show()
        self._animation = animation
        self._data_queue = data_queue
        self._window.addItem(animation.view)

    def set_camera_position(self, distance, elevation):
        self._window.setCameraPosition(distance=distance, elevation=elevation)

    def update(self):
        data = self._data_queue.get()
        self._animation.update(data)

    def start(self, frametime=0.1):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(frametime)

        if (sys.flags.interactive != 1) or not hasattr(QtCore, "PYQT_VERSION"):
            QtWidgets.QApplication.instance().exec_()


if __name__ == "__main__":
    screen = Screen()
    while True:
        time.sleep(1)
