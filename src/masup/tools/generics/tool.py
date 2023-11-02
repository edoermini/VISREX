from abc import ABC, abstractmethod
import subprocess
from RPA.Windows import Windows
import pyperclip

class DesktopTool(ABC):
    
    @abstractmethod
    def __init__(self, path):
        self.window_locator = r''
        self.load_file_button_locator = r''
        self.open_file_pop_up_window_locator = r''
        self.clipboard = ""

        self.path = path
        self.library = Windows()
    
    def update_clipboard(self):
        self.clipboard = ""

    def run(self):
        """Opens the application"""
        
        self.library.windows_run(self.path)
        self._control_window()

    def _control_window(self):
        self.library.control_window(
            locator=self.window_locator,
            foreground=False,
            main=True
        )
    
    def load_sample_from_gui(self, sample_path):
        self.library.click(self.load_file_button_locator)
        self.library.send_keys(self.open_file_pop_up_window_locator,sample_path+'{ENTER}')
    
    def click(self, locator):
        self.library.click(locator)
    
    def copy_to_clipboard(self):
        pyperclip.copy(self.clipboard)

    def close(self):
        """Closes the application"""
        self.library.close_window(self.window_locator)


class CLITool(ABC):

    @abstractmethod
    def __init__(self, path:str):
        self.path = path
        self.process = None
        self.stdout = str()
        self.stderr = str()

    def _run(self, args):
        self.process = subprocess.Popen([self.path] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = self.process.communicate()

        self.stdout = stdout.decode('utf-8')
        self.stderr = stderr.decode('utf-8')
    
    def get_output(self) -> str:
        return self.stdout

    def get_error(self) -> str:
        return self.stderr

    def close(self):
        self.process.kill()