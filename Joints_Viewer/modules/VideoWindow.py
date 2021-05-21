from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtWidgets import QMessageBox
from modules.Plot3DWindow import Plot3DWindow

class VideoWindow(QtWidgets.QMainWindow):
    
    def __init__(self, graph:Plot3DWindow, parent = None):
        super(VideoWindow, self).__init__(parent)
        self._video_init(graph)

    def _video_init(self, graph:Plot3DWindow) -> None:
        self.setWindowTitle("PyQt Video Player Widget")
        self.mediaPlayer = QtMultimedia.QMediaPlayer(self, QtMultimedia.QMediaPlayer.VideoSurface)
        self.videoWidget = QtMultimediaWidgets.QVideoWidget()
        self._create_play_button()
        self._create_position_slider()
        self._create_error_label()
        self._create_graph_window(graph)
        self._create_actions()
        self._create_menu_bar()
        self._create_widget()
        self._create_layouts()
        self._create_media_player()

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
        self.graph.show()

    def _create_actions(self) -> None:
        # Create open hand poses file action
        self.openActionHandPose = QtWidgets.QAction(QtGui.QIcon('open.png'), '&Open_Hand_Pose', self)
        self.openActionHandPose.setShortcut('Ctrl+P')
        self.openActionHandPose.setStatusTip('Open hand poses')
        self.openActionHandPose.triggered.connect(self.graph.openFile)

        # Create open video file action
        self.openActionMovie = QtWidgets.QAction(QtGui.QIcon('open.png'), '&Open_Video', self)
        self.openActionMovie.setShortcut('Ctrl+O')
        self.openActionMovie.setStatusTip('Open video')
        self.openActionMovie.triggered.connect(self.openFile)

        # Create exit action
        self.exitAction = QtWidgets.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(self.exitCall)

    def _create_menu_bar(self) -> None:
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(self.openActionHandPose)
        fileMenu.addAction(self.openActionMovie)
        fileMenu.addAction(self.exitAction)

    def _create_widget(self) -> None:
        self.wid = QtWidgets.QWidget()
        self.setCentralWidget(self.wid)

    def _create_layouts(self) -> None:
        controlLayout = QtWidgets.QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)
        # Set widget to contain window contents
        self.wid.setLayout(layout)

    def _create_media_player(self) -> None:
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

    def openFile(self) -> None:
        if self.graph.hand_pose_length() <= 0:
            QMessageBox.information(self, 'Information', 'First of all you must select hand poses file.', QMessageBox.Ok, QMessageBox.Ok)
            return
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Video", QtCore.QDir.homePath())

        if fileName:
            media = QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(fileName))
            self.mediaPlayer.setMedia(media)
            self.mediaPlayer.setPlaybackRate(0.5)
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

    def positionChanged(self, position) -> None:
        self.positionSlider.setValue(position)
        self.graph.draw(position+900)
        self.graph.canvas.draw()

    def durationChanged(self, duration) -> None:
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position) -> None:
        self.mediaPlayer.setPosition(position)

    def handleError(self) -> None:
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())