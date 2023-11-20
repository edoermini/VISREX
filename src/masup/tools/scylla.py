from masup.tools.generics import DesktopTool
import tempfile
import os

class Tool(DesktopTool):
    def __init__(self, path: str):
        super().__init__(path)

        self.window_locator = r'regex:"^Scylla.*"'
        self.load_file_button_locator = r'name:...'
        self.open_file_pop_up_window_locator = r'name:"Open file..."'

    def attach_to_process(self, executable_name):
        self.library.click(r'name:"Attach to an active process" type:ComboBox')
        self.library.click(f'regex:".*{executable_name}.*" type:ListItem')
        
    def set_oep(self, oep:str):
        self.library.send_keys(r'name:OEP type:Edit', "{CONTROL}A")
        self.library.send_keys(r'name:OEP type:Edit', oep)
    
    def iat_autosearch(self):
        self.library.click(r'name:"IAT Autosearch"')

        if self.library.get_element('name:Information'):
            self.library.click('name:Yes type:Button')

        self.library.set_anchor(r'name:"IAT found"')
        self.library.click(r'name:OK type:Button')
        self.library.clear_anchor()

    def get_imports(self):
        self.library.click(r'name:"Get Imports" type:Button')
    
    def dump(self, filename):
        self.library.click(r'name:Dump')

        with tempfile.TemporaryDirectory() as tmp_dir:
            self.library.send_keys('name:"Save As"', os.path.join(tmp_dir.name(), "dump"))
    
    def fix_dump(self):
        self.library.click(r'name:"Fix Dump"')