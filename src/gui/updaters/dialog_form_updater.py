from PyQt6.QtCore import QThread, pyqtSignal
import time
#import pygetwindow as gw
#import pyautogui
#import pyperclip
import time 

class DialogFormUpdater(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self, max_active_selection_times:int=2):
        super().__init__()

        self.max_active_selection_times = max_active_selection_times
        self.stopped = False

    def run(self):
        last_selected_text = ""
        active_selection_times = 0
        # while True and not self.stopped:
        #     focused_window = gw.getActiveWindow()
        #     if focused_window:
        #         focused_window.activate()
        #         time.sleep(1)
        #         pyautogui.hotkey('ctrl', 'c')
        #         selected_text = pyperclip.paste()

        #     if last_selected_text == selected_text:
        #         active_selection_times += 1
            
        #     if active_selection_times == self.max_active_selection_times:
        #         self.update_signal.emit(last_selected_text)
    
    def stop(self):
        self.stopped = True
        self.quit()