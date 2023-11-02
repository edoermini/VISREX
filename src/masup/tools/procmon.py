from masup.tools.generics import DesktopTool
from procmon_parser import ProcmonLogsReader

import tempfile

class ProcMonTool(DesktopTool):
    def __init__(self, path: str):
        super().__init__(path)

        self.window_locator = r'regex:".*Process Monitor.*"'
        self.load_file_button_locator = r'name:...'
        self.open_file_pop_up_window_locator = r'name:"Choose the file to open..."'
        self.save_file_pop_up_window_locator = r'name:"Save To File"'
        self.paused = False
        self.log_file = tempfile.NamedTemporaryFile()
    
    def pause(self):
        if not self.paused:
            self.library.send_keys(self.window_locator, '{CONTROL}E')
            self.paused = True
    
    def resume(self):
        if self.paused:
            self.library.send_keys(self.window_locator, '{CONTROL}E')
            self.paused = False
    
    def save_log(self, log_format='pml'):
        self.library.send_keys(self.window_locator, '{CONTROL}S')

        self.library.set_anchor(self.save_file_pop_up_window_locator)

        if log_format == 'pml':
            self.library.click(self.save_file_pop_up_window_locator, 'name:"Native Process Monitor Format (PML)"')
        elif log_format == 'csv':
            self.library.click(self.save_file_pop_up_window_locator, 'name:"Comma-Separated Values (CSV)"')
        elif log_format == 'xml':
            self.library.click(self.save_file_pop_up_window_locator, 'name"Extensible Markup Language (XML)"')
        else:
            raise ValueError(f'{log_format} is not a valid log format. Allowed log format are: pml, csv or xml')
        
        self.library.send_keys('name:"Path:" type:"Edit"', self.log_file.name)
        self.library.click('name:"Ok" type:"Button"')
        self.library.clear_anchor()
    
    def get_log(self, log_format='pml'):
        log = None

        if log_format == 'pml':
            with open(self.log_file.name, "rb") as f:
                log = ProcmonLogsReader(f)
        
        return log