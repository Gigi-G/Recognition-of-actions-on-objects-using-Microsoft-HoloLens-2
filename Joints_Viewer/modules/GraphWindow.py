import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation
import numpy as np
from modules.HandPose import HandPose

class GraphWindow(QtWidgets.QWidget):
    
    _hand_pose_dict:dict = {}

    def __init__(self):
        super().__init__()
        np.random.seed(19680801)
        self.setWindowTitle("Joints Viewer")
        self.graph_init()

    def graph_init(self):
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111, projection='3d')

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.canvas)

        self.axes.set_xlabel('X')
        self.axes.set_ylabel('Y')
        self.axes.set_zlabel('Z')
        #self.anim = animation.FuncAnimation(self.fig, self.animate, 25, interval=50, blit=False)

    def animate(self, i):
        n = 100
        # For each set of style and range settings, plot n random points in the box
        # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
        for m, zlow, zhigh in [('o', -50, -25), ('^', -30, -5)]:
            xs = self.randrange(n, 23, 32)
            ys = self.randrange(n, 0, 100)
            zs = self.randrange(n, zlow, zhigh)
            self.line = self.axes.scatter(xs, ys, zs, marker=m)
        self.axes.clear()

    def openFile(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Hand Pose", QtCore.QDir.homePath())
        if fileName:
            self._hand_pose_dict = HandPose(fileName).get_hand_pose_dict()

    def randrange(self, n, vmin, vmax):
        return (vmax - vmin)*np.random.rand(n) + vmin

    def exitCall(self):
        QtWidgets.QApplication.quit()
    
    def closeEvent(self, event):
        #event.ignore()
        event.accept()