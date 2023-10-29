import threading
import psutil
import re
import time

from .analysis import Analysis

class ProcessTableUpdater(threading.Thread):
    def __init__(self, gui, analysis:Analysis):
        super(ProcessTableUpdater, self).__init__()
        self.gui = gui
        self.analysis = analysis

        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            # Your periodic update logic here
            self.analysis.update_activities()
            
            # Update the GUI
            self.gui.update_progress_table()

            # Sleep for some time before the next update
            self.stop_event.wait(1)  # Sleep for 5 seconds

    def stop(self):
        self.stop_event.set()