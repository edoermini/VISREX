from integrations.generics import DesktopTool

class Tool(DesktopTool):
    def __init__(self, path: str):
        super().__init__(path)

        self.window_locator = r'regex:PEiD.*'
        self.load_file_locator = r'name:...'
        self.open_file_pop_up_window_locator = r'name:"Choose the file to open..."'
    
    def execute(self, *args, **kwargs):
        self.run()
        self.load_sample_from_gui(kwargs['malware'])
        return self.get_packer()

    def get_packer(self):
        packer_box = self.library.get_elements('type:Edit name:"File:"')[1]
        return self.library.get_value(packer_box)