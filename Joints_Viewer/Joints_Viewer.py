import queue
import sys
from PyQt5 import QtWidgets
from modules.VideoWindow import VideoWindow
from modules.GraphWindow import GraphWindow
from threading import Semaphore, Thread
from queue import Queue

queue_data:Queue = Queue(1)
full:Semaphore = Semaphore(0)
empty:Semaphore = Semaphore(1)
access:Semaphore = Semaphore(1)

def video_window():
    player.show()

def graph_view():
    graph.show()

if __name__ == '__main__':
    app:QtWidgets.QApplication = QtWidgets.QApplication(sys.argv)
    player:VideoWindow = VideoWindow(GraphWindow())
    player.resize(640, 480)
    graph:GraphWindow = GraphWindow()
    graph.resize(640, 480)
    #thread_video = Thread(target=video_window)
    thread_graph = Thread(target=graph_view)
    #thread_video.start()
    thread_graph.start()
    sys.exit(app.exec_())