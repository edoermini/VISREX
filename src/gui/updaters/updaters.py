import threading
from PyQt5.QtCore import QObject, pyqtSignal, QThreadPool, QRunnable, QTimer, Qt
import time

from analysis import Analysis


class ActivityUpdater(QObject):
    dataUpdated = pyqtSignal()

    def __init__(self, analysis:Analysis, timeout=1000):
        super().__init__()
        self.analysis = analysis
        self.thread_pool = QThreadPool.globalInstance()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateData)
        self.timer.start(timeout)
        self.running = True  # Flag to track the state

    def updateData(self):
        if not self.running:
            return  # Do not start a new task if the updater is stopped

        # Simulate updating data asynchronously
        task = ActivityUpdateTask(self.analysis, self.dataUpdated)
        self.thread_pool.start(task)

    def stop(self):
        # Stop the timer and set the running flag to False
        self.timer.stop()
        self.running = False

class ActivityUpdateTask(QRunnable):
    def __init__(self, analysis:Analysis, result_callback):
        super().__init__()
        self.analysis = analysis
        self.result_callback = result_callback

    def run(self):
        self.analysis.update_activities()
        self.result_callback.emit()