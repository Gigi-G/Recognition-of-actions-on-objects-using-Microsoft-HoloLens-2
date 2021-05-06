from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtWidgets import QMessageBox
from modules.GraphWindow import GraphWindow

class VideoWindow(QtWidgets.QMainWindow):
    def __init__(self, graph:GraphWindow, parent = None):

        super(VideoWindow, self).__init__(parent)

        self.setWindowTitle("PyQt Video Player Widget")

        self.graph:GraphWindow = graph
        self.graph.show()

        self.mediaPlayer = QtMultimedia.QMediaPlayer(self, QtMultimedia.QMediaPlayer.VideoSurface)

        videoWidget = QtMultimediaWidgets.QVideoWidget()

        self.playButton = QtWidgets.QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QtWidgets.QLabel()
        self.errorLabel.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)

        # Create new action
        openActionMovie = QtWidgets.QAction(QtGui.QIcon('open.png'), '&Open_Movie', self)
        openActionMovie.setShortcut('Ctrl+O')
        openActionMovie.setStatusTip('Open movie')
        openActionMovie.triggered.connect(self.openFile)

        # Create new action
        openActionHandPose = QtWidgets.QAction(QtGui.QIcon('open.png'), '&Open_Hand_Pose', self)
        openActionHandPose.setShortcut('Ctrl+P')
        openActionHandPose.setStatusTip('Open Hand Pose')
        openActionHandPose.triggered.connect(self.graph.openFile)

        # Create exit action
        exitAction = QtWidgets.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openActionMovie)
        fileMenu.addAction(openActionHandPose)
        fileMenu.addAction(exitAction)

        # Create a widget for window contents
        wid = QtWidgets.QWidget()
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QtWidgets.QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)
        # Set widget to contain window contents

        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)


    def openFile(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Movie", QtCore.QDir.homePath())

        if fileName:
            media = QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(fileName))
            self.mediaPlayer.setMedia(media)
            self.playButton.setEnabled(True)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            self.graph.exitCall()
        else:
            event.ignore()

    def exitCall(self):
        QtWidgets.QApplication.quit()

    def play(self):
        if self.mediaPlayer.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        print(position)
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        pass
        #self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())
