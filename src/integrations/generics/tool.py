from abc import ABC, abstractmethod
import subprocess
import platform

if platform.system() == 'Windows':
    from RPA.Windows import Windows as Library
elif platform.system() == 'Linux':
    from RPA.Desktop import Desktop as Library

class DesktopTool(ABC):
    
    @abstractmethod
    def __init__(self, path):
        self.window_locator = r''
        self.load_file_locator = r''
        self.open_file_pop_up_window_locator = r''

        self.path = path
        self.library = Library()
    
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    def attach(self):
        self._control_window()

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
        self.library.click(self.load_file_locator)
        #self.library.set_anchor(self.open_file_pop_up_window_locator)
        self.library.send_keys(self.open_file_pop_up_window_locator,sample_path+'{ENTER}')
        #self.library.
    
    def click(self, locator:str):
        self.library.click(locator)

    def close(self):
        """Closes the application"""
        self.library.close_window(self.window_locator)


class CLITool(ABC):

    @abstractmethod
    def __init__(self, path:str):
        self.path = path

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
    
    def _run(self, args):
        process = subprocess.Popen([self.path] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        return stdout.decode('utf-8'), stderr.decode('utf-8'), process.returncode