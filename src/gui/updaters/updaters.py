import threading

class ProgressTableUpdater(threading.Thread):
    def __init__(self, gui):
        super(ProgressTableUpdater, self).__init__()
        self.gui = gui

        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            self.gui.update_progress()

            # Sleep for some time before the next update
            self.stop_event.wait(1)  # Sleep for 5 seconds

    def stop(self):
        self.stop_event.set()