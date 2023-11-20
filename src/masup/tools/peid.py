from masup.tools.generics import DesktopTool

class PEiD(DesktopTool):
    def __init__(self, path: str):
        super().__init__(path)

        self.window_locator = r'regex:PEiD.*'
        self.load_file_button_locator = r'name:...'
        self.open_file_pop_up_window_locator = r'name:"Choose the file to open..."'
    
    def execute(self):

        packer_box = self.library.get_elements('type:Edit name:"File:"')[1]
        return self.library.get_value(packer_box)