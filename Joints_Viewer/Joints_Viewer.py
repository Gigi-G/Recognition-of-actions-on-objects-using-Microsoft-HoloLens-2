import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtWidgets import QMessageBox

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation
import numpy as np

class GraphWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        np.random.seed(19680801)
        self.setWindowTitle("Joints Viewer")
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111, projection='3d')

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.canvas)

        self.axes.set_xlabel('X')
        self.axes.set_ylabel('Y')
        self.axes.set_zlabel('Z')
        self.anim = animation.FuncAnimation(self.fig, self.animate, 25, interval=50, blit=False)

    def animate(self, i):
        n = 100

        # For each set of style and range settings, plot n random points in the box
        # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
        for m, zlow, zhigh in [('o', -50, -25), ('^', -30, -5)]:
            xs = self.randrange(n, 23, 32)
            ys = self.randrange(n, 0, 100)
            zs = self.randrange(n, zlow, zhigh)
            self.line = self.axes.scatter(xs, ys, zs, marker=m)
        return self.line

    def randrange(self, n, vmin, vmax):
        return (vmax - vmin)*np.random.rand(n) + vmin

    def exitCall(self):
        QtWidgets.QApplication.quit()
    
    def closeEvent(self, event):
        event.ignore()


class VideoWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):

        super(VideoWindow, self).__init__(parent)

        self.setWindowTitle("PyQt Video Player Widget Example - pythonprogramminglanguage.com")

        self.graph = GraphWindow()
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

        self.errorLabel =QtWidgets.QLabel()
        self.errorLabel.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)

        # Create new action
        openAction = QtWidgets.QAction(QtGui.QIcon('open.png'), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.openFile)

        # Create exit action
        exitAction = QtWidgets.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        #fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
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
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        pass
        #self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    player = VideoWindow()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec_())