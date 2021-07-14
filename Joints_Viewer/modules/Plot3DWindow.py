from typing import Any
import matplotlib
from torch.functional import Tensor
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from modules.HandPose import HandPose
from modules.target import Target
import torch
import numpy as np
from modules.LSTM import LSTM
import json

class Plot3DWindow(QtWidgets.QWidget):
    
    _time_keys:list = [] 
    _hand_pose:dict = {}
    _model:Any = None
    _colnames:list = []
    _data:list = []
    _window:int = 8
    _count:int = 0

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Joints Viewer")
        self._graph_init()
        self._model_init()

    def _graph_init(self) -> None:
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111, projection='3d')
        #self._create_real_label()
        self._create_predict_label()
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.canvas)
        #layout.addWidget(self.realLabel)
        layout.addWidget(self.predictLabel)
        self.axes.set_xlabel('X')
        self.axes.set_ylabel('Y')
        self.axes.set_zlabel('Z')
        self.axes.set_xlim3d(left=-0.4, right=0.4) 
        self.axes.set_ylim3d(bottom=-0.4, top=0.4)
        self.axes.set_zlim3d(bottom=0.4, top=1)

    def _model_init(self) -> None:
        self._model = LSTM(156, 4, 78, 1)
        self._model.load_state_dict(torch.load("../data/modelli_overlap/0007_mymodel.pt"))
        self._model.to(
            torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        )

    def _create_real_label(self) -> None:
        self.realLabel = QtWidgets.QLabel()
        self.realLabel.setText("REAL TARGET: None")

    def _create_predict_label(self) -> None:
        self.predictLabel = QtWidgets.QLabel()
        self.predictLabel.setText("PREDICT TARGET: None")

    def idx2class(self, key:int) -> str:
        names = {
            0: "No_action",
            1: "Action",
            2: "Action",
            3: "Action"
        }
        return names[key]

    def class2pseudo(self, key:str) -> str:
        names = {
            "No_action": "No_action",
            "Prendi": "Action",
            "Rilascia": "Action",
            "Premi": "Action"
        }
        return names[key]

    def get_action(self, joints_video:list, val:str) -> None:
        if self._count == 0:
            self._data = [np.array(joints_video).astype(float)] * self._window
            self._count += 1
        else:
            self._data.pop(0)
            self._data.append(np.array(joints_video).astype(float))
        self._model.eval()
        with torch.no_grad():
            batch:Tensor = torch.from_numpy(np.array([self._data]).astype(float)).float().to(
                torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            )
            y_pred, _ = self._model(batch)
            print(y_pred)
            _, top_i = y_pred.topk(1)
            y_tags = top_i[0].item()
            #print(self._data)
            #print(self.idx2class(y_tags))
        #self.realLabel.setText("REAL TARGET: " + str(val))
        self.predictLabel.setText("PREDICT TARGET: " + self.idx2class(y_tags))

    def draw(self, time:int) -> None:
        #time = min(self._time_keys, key=lambda x: abs(x-time))
        t:list = []
        for key in self._time_keys:
           if abs(time - key) < 500:
               t.append(key)
        time = max(t) if len(t) > 0 else 0
        self.axes.clear()
        if time == 0:
           joints_video = [0.0] * 156
           self.get_action(joints_video, "No_action")
           joints_video = []
        else:
            coordinates = self._hand_pose[str(time)]
            joints_video = [0.0] * 156
            for key, val in coordinates.items():
                if key == "action":
                    self.get_action(joints_video, val)
                    joints_video = []
                else:
                    x, y, z = val
                    joints_video[self._colnames.index(key + "_x")] = x
                    joints_video[self._colnames.index(key + "_y")] = y
                    joints_video[self._colnames.index(key + "_z")] = z
                    self.axes.scatter(x, y, z, marker='o', c="limegreen")
        self.axes.set_xlim3d(left=-0.4, right=0.4) 
        self.axes.set_ylim3d(bottom=-0.4, top=0.4)
        self.axes.set_zlim3d(bottom=0.4, top=1)
        self.canvas.draw()

    def hand_pose_length(self) -> int:
        return len(self._hand_pose)

    def add_target(self, target:dict) -> None:
        for key in self._hand_pose:
            start_tim:int = int(key)
            self._hand_pose[key]["action"] = "No_action"
            for _, val in target.items():
                if val["time"][0] <= start_tim <= val["time"][1]:
                    self._hand_pose[key]["action"] = val["action"]

    def load_hand_joints(self) -> None:
        with open("./hand_joints.json") as f:
            joints:dict = json.load(f)
            self._colnames = [(joint) for joint in joints]
            f.close()

    def openFile(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Hand Pose", QtCore.QDir.homePath())
        if fileName:
            self._hand_pose = HandPose(fileName).get_hand_pose_dict()
            self.add_target(Target.get(fileName[:-15] + "_action.json", 0))
            self._time_keys = [(int(key)) for key in self._hand_pose]
            self.load_hand_joints()
            self._data = [[0.0] * 156] * self._window
                

    def exitCall(self) -> None:
        QtWidgets.QApplication.quit()
    
    def closeEvent(self, event) -> None:
        event.ignore()