import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from modules.HandPose import HandPose
from modules.target import Target

class Plot3DWindow(QtWidgets.QWidget):
    
    _time_keys:list = [] 
    _hand_pose:dict = {}

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Joints Viewer")
        self._graph_init()

    def _graph_init(self) -> None:
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111, projection='3d')
        self._create_real_label()
        self._create_predict_label()
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.canvas)
        layout.addWidget(self.realLabel)
        layout.addWidget(self.predictLabel)
        self.axes.set_xlabel('X')
        self.axes.set_ylabel('Y')
        self.axes.set_zlabel('Z')

    def _create_real_label(self) -> None:
        self.realLabel = QtWidgets.QLabel()
        self.realLabel.setText("REAL TARGET: None")

    def _create_predict_label(self) -> None:
        self.predictLabel = QtWidgets.QLabel()
        self.predictLabel.setText("PREDICT TARGET: None")

    def draw(self, time:int) -> None:
        time = min(self._time_keys, key=lambda x:abs(x-time))
        if time == 0: return
        coordinates:dict = self._hand_pose[str(time)]
        self.axes.clear()
        count:int = 0
        for _, val in coordinates.items():
            if count == 0:
                try:
                    x:float = float(val)
                except:
                    self.realLabel.setText("REAL TARGET: " + str(val))
            elif count == 1:
                y:float = val
            elif count == 2:
                z:float = val
                self.axes.scatter(x, y, z, marker='o', c="limegreen")
                self.axes.set_xlim3d(left=-0.2, right=0.2) 
                self.axes.set_ylim3d(bottom=-0.2, top=0.2) 
                self.axes.set_zlim3d(bottom=-0.4, top=1)
                count = -1
            count += 1

    def hand_pose_length(self) -> int:
        return len(self._hand_pose)

    def add_target(self, target:dict) -> None:
        for key in self._hand_pose:
            start_tim:int = int(key)
            self._hand_pose[key]["action"] = "No_action"
            for _, val in target.items():
                if val["time"][0] <= start_tim <= val["time"][1]:
                    self._hand_pose[key]["action"] = val["action"]

    def openFile(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Hand Pose", QtCore.QDir.homePath())
        if fileName:
            self._hand_pose = HandPose(fileName).get_hand_pose_dict()
            self.add_target(Target.get(fileName[:-15] + "_action.json", 0))
            for key in self._hand_pose:
                self._time_keys.append(int(key))

    def exitCall(self) -> None:
        QtWidgets.QApplication.quit()
    
    def closeEvent(self, event) -> None:
        event.ignore()