import threading
from PyQt5.QtCore import QObject, pyqtSignal, QThreadPool, QRunnable, QTimer, Qt
import time

from analysis import Analysis

class ActivityUpdateTaskSignals(QObject):
    result = pyqtSignal()

class ActivityUpdater(QObject):
    dataUpdated = pyqtSignal()

    def __init__(self, analysis:Analysis, timeout:int=1000):
        super().__init__()
        self.analysis = analysis
        self.thread_pool = QThreadPool.globalInstance()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateData)
        self.timer.start(timeout)

    def updateData(self):
        # Simulate updating data asynchronously
        task = ActivityUpdateTask(self.analysis)
        task.signals.result.connect(self.dataUpdated.emit)
        self.thread_pool.start(task)

class ActivityUpdateTask(QRunnable):

    def __init__(self, analysis:Analysis):
        super().__init__()
        self.signals = ActivityUpdateTaskSignals()
        self.analysis = analysis

    def run(self):

        self.analysis.update_activities()
        self.signals.result.emit()