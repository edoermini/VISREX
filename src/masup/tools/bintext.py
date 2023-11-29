from masup.tools.generics import DesktopTool
import tempfile
import re
from pathlib import Path
import os
import random
import string
import time

class Tool(DesktopTool):
    def __init__(self, path: str):
        super().__init__(path)

        self.window_locator = r'regex:BinText.*'
        self.load_file_locator = r'name:"Browse"'
        self.open_file_pop_up_window_locator = r'name:"Open file for scanning"'
        self.save_file_pop_up_window_locator = r'name:"Save text to file"'
    
    def execute(self, *args, **kwargs):
        self.run()
        self.load_sample_from_gui(kwargs['malware'])
        self.scan()

    def scan(self, *args, **kwargs):
        self.library.click('name:Go')

    def save(self, file_path):
        self.library.click('name:Save')
        self.library.send_keys(self.save_file_pop_up_window_locator, file_path+"{ENTER}")