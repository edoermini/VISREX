import pygetwindow as gw
import pyautogui
import pyperclip
import time 

def listen_for_selection(max_active_selection_time:int=2):
    active_selection_time = 0
    last_selected_text = ""

    while True:
        focused_window = gw.getActiveWindow()
        if focused_window:
            focused_window.activate()
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'c')
            selected_text = pyperclip.paste()

            if last_selected_text == selected_text:
                active_selection_time += 1
            
            if active_selection_time == max_active_selection_time:
                return active_selection_time

        time.sleep(1)