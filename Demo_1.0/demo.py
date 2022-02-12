import sys
from PyQt5 import QtWidgets
from modules.VideoWindow import VideoWindow
from modules.Plot3DWindow import Plot3DWindow

if __name__ == '__main__':
    app:QtWidgets.QApplication = QtWidgets.QApplication(sys.argv)
    player:VideoWindow = VideoWindow(Plot3DWindow())
    player.resize(840, 580)
    player.show()
    sys.exit(app.exec_())