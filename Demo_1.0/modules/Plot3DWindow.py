from typing import Any
import matplotlib
from torch.functional import Tensor
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Plot3DWindow(QtWidgets.QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Joints Viewer")
        self.setMinimumSize(640, 480)
        self._graph_init()

    def _graph_init(self) -> None:
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111, projection='3d')
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.canvas)
        self.axes.set_xlabel('X')
        self.axes.set_ylabel('Y')
        self.axes.set_zlabel('Z')
        self.axes.set_xlim3d(left=-0.4, right=0.4) 
        self.axes.set_ylim3d(bottom=-0.4, top=0.4)
        self.axes.set_zlim3d(bottom=0.4, top=1)

    def exitCall(self) -> None:
        QtWidgets.QApplication.quit()
    
    def closeEvent(self, event) -> None:
        event.ignore()