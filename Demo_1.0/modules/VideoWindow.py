import json
from typing import Any
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtWidgets import QMessageBox
import numpy as np
from torch import tensor
from modules.Plot3DWindow import Plot3DWindow
import torch
from modules.LSTM import LSTM
from modules.HandPose import HandPose
from modules.target import Target

class VideoWindow(QtWidgets.QMainWindow):

    _time_keys:list = [] 
    _hand_pose:dict = {}
    _model:Any = None
    _data:list = []
    _window:int = 8
    _count:int = 0
    
    def __init__(self, graph:Plot3DWindow, parent = None):
        super(VideoWindow, self).__init__(parent)
        self._video_init(graph)

    def _video_init(self, graph:Plot3DWindow) -> None:
        self.setWindowTitle("PyQt Video Player Widget")
        self.setMinimumSize(640, 580)
        self.mediaPlayer = QtMultimedia.QMediaPlayer(self, QtMultimedia.QMediaPlayer.VideoSurface)
        self.videoWidget = QtMultimediaWidgets.QVideoWidget()
        self.videoWidget.setMinimumSize(self.videoWidget.width(), self.videoWidget.height())
        self._create_play_button()
        self._create_position_slider()
        self._create_error_label()
        self._create_graph_window(graph)
        self._create_actions()
        self._create_menu_bar()
        self._create_widget()
        self._create_layouts()
        self._create_media_player()
        self._model_init()

    def idx2class(self, key:int) -> str:
        names = {
            0: "No_action",
            1: "Action",
            2: "Action",
            3: "Action"
        }
        return names[key]

    def idx2class2(self, key:int) -> str:
        names = {
            0: "No_action",
            1: "Prendi",
            2: "Rilascia",
            3: "Premi"
        }
        return names[key]
    
    def idx2class3(self, key:int) -> str:
        names = {
            0: "No_action",
            1: "P/R",
            2: "P/R",
            3: "Premi"
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
    
    def class2pseudo2(self, key:str) -> str:
        names = {
            "No_action": "No_action",
            "Prendi": "P/R",
            "Rilascia": "P/R",
            "Premi": "Premi"
        }
        return names[key]

    def _model_init(self) -> None:
        self._model = LSTM(156, 4, 78, 1)
        self._model.load_state_dict(torch.load("../data/modelli_overlap/0007_mymodel.pt"))
        self._model.to(
            torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        )

    def _create_real_label(self) -> None:
        self.realLabel = QtWidgets.QLabel()
        self.realLabel.setStyleSheet("background-color: limegreen")
        font = QtGui.QFont('Arial', 20)
        font.setBold(True)
        self.realLabel.setFont(font)
        self.realLabel.setText("GROUND TRUTH: None")

    def _create_predict_label(self) -> None:
        self.predictLabel = QtWidgets.QLabel()
        self.predictLabel.setStyleSheet("background-color: limegreen")
        font = QtGui.QFont('Arial', 20)
        font.setBold(True)
        self.predictLabel.setFont(font)
        self.predictLabel.setText("PREDICTION: None")

    def resizeEvent(self, event):
        QtWidgets.QMainWindow.resizeEvent(self, event)

    def _create_play_button(self) -> None:
        self.playButton = QtWidgets.QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

    def _create_position_slider(self) -> None:
        self.positionSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

    def _create_error_label(self) -> None:
        self.errorLabel = QtWidgets.QLabel()
        self.errorLabel.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)

    def _create_graph_window(self, graph:Plot3DWindow) -> None:
        self.graph:Plot3DWindow = graph
        self.graph.resize(840, 580)
        self.graph.show()

    def _create_actions(self) -> None:
        # Create open hand poses file action
        self.openActionHandPose = QtWidgets.QAction(QtGui.QIcon('open.png'), '&Open_Hand_Pose', self)
        self.openActionHandPose.setShortcut('Ctrl+P')
        self.openActionHandPose.setStatusTip('Open hand poses')
        self.openActionHandPose.triggered.connect(self.openFile)

        # Create exit action
        self.exitAction = QtWidgets.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(self.exitCall)

    def _create_menu_bar(self) -> None:
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(self.openActionHandPose)
        fileMenu.addAction(self.exitAction)

    def _create_widget(self) -> None:
        self.wid = QtWidgets.QWidget()
        self.setCentralWidget(self.wid)

    def _create_layouts(self) -> None:
        # Create a layout for label
        layoutLabel = QtWidgets.QHBoxLayout()
        layoutLabel.setContentsMargins(0, 0, 0, 0)
        self._create_real_label()
        self._create_predict_label()
        layoutLabel.addWidget(self.realLabel)
        layoutLabel.addWidget(self.predictLabel)

        #Create control video layout
        controlLayout = QtWidgets.QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        # Create a vertical layout for label and control
        layoutCL = QtWidgets.QVBoxLayout()
        layoutCL.addLayout(layoutLabel)
        layoutCL.addLayout(controlLayout)
        layoutCL.addStretch()

        # Create a vertical layout with video widget and CL layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.videoWidget)
        layout.addLayout(layoutCL)
        layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        self.wid.setLayout(layout)

    def _create_media_player(self) -> None:
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

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

            #Video option
            fileName = fileName[:-15] + "_Video.mp4"
            media = QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(fileName))
            self.mediaPlayer.setMedia(media)
            self.mediaPlayer.setPlaybackRate(0.75)
            self.mediaPlayer.setNotifyInterval(0.5)
            self.playButton.setEnabled(True)

    def closeEvent(self, event) -> None:
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            self.graph.exitCall()
        else:
            event.ignore()

    def exitCall(self) -> None:
        QtWidgets.QApplication.quit()

    def play(self) -> None:
        if self.mediaPlayer.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state) -> None:
        if self.mediaPlayer.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))

    def get_action(self, joints_video:list, val:str) -> None:
        if self._count == 0:
            self._data = [np.array(joints_video).astype(float)] * self._window
            self._count += 1
        else:
            self._data.pop(0)
            self._data.append(np.array(joints_video).astype(float))
        self._model.eval()
        with torch.no_grad():
            batch:tensor = torch.from_numpy(np.array([self._data]).astype(float)).float().to(
                torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            )
            y_pred, _ = self._model(batch)
            #print(y_pred)
            _, top_i = y_pred.topk(1)
            y_tags = top_i[0].item()
            #print(self._data)
            #print(self.idx2class(y_tags))
        self.realLabel.setText("GROUND TRUTH: " + self.class2pseudo(val))
        #self.realLabel.setText("GROUND TRUTH: " + str(val))
        self.predictLabel.setText("PREDICTION: " + self.idx2class(y_tags))
        if self.class2pseudo(val) == self.idx2class(y_tags):
        #if val == self.idx2class2(y_tags):
            self.realLabel.setStyleSheet("background-color: limegreen")
            self.predictLabel.setStyleSheet("background-color: limegreen")
        else:
            self.realLabel.setStyleSheet("background-color: red")
            self.predictLabel.setStyleSheet("background-color: red")

    def draw(self, time:int) -> None:
        t:list = []
        for key in self._time_keys:
           if abs(time - key) < 500:
               t.append(key)
        time = max(t) if len(t) > 0 else 0
        self.graph.axes.clear()
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
                    self.graph.axes.scatter(x, y, z, marker='o', c="limegreen")
        self.graph.axes.set_xlim3d(left=-0.4, right=0.4) 
        self.graph.axes.set_ylim3d(bottom=-0.4, top=0.4)
        self.graph.axes.set_zlim3d(bottom=0.4, top=1)
        self.graph.canvas.draw()

    def positionChanged(self, position) -> None:
        self.positionSlider.setValue(position)
        self.draw(position+550)

    def durationChanged(self, duration) -> None:
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position) -> None:
        self.mediaPlayer.setPosition(position)

    def handleError(self) -> None:
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())