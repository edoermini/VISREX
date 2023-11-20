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
        self.load_file_button_locator = r'name:Browse'
        self.open_file_pop_up_window_locator = r'name:"Open file for scanning"'
        self.save_file_pop_up_window_locator = r'name:"Save text to file"'

        self.strings:list[dict[str:any]] = []
    
    def execute(self):
        self.library.click('name:Go')

        tmp_file = os.path.join(Path.home(),f"{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}.txt")

        self.save(tmp_file)

        with open(tmp_file, 'r') as bintext_output:
            for line in bintext_output.readlines():
                print(line)

                if line.startswith("File") or line.startswith("=") or not line:
                    continue

                splitted_line = re.split(' {2,}', line)

                if len(splitted_line) < 3:
                    continue
                    
                self.strings.append({
                    'file_pos': splitted_line[0],
                    'mem_pos': splitted_line[1],
                    'str_id': splitted_line[2],
                    'string': splitted_line[3] if len(splitted_line) == 4 else ""
                })
        
        os.remove(tmp_file)
    
    def update_clipboard(self):
        super().update_clipboard()

        for bintext_string in self.strings:
            self.clipboard += f"{bintext_string['string']}"

    def save(self, file_path):
        self.library.click('name:Save')
        self.library.send_keys(self.save_file_pop_up_window_locator, file_path+"{ENTER}")