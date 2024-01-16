from integrations.generics import DesktopTool

class Tool(DesktopTool):
    def __init__(self, path: str):
        super().__init__(path)

        self.window_locator = r'regex:pestudio.*'
        self.load_file_locator = r'name:"open file" type:Button'
        self.open_file_pop_up_window_locator = r'name:"Select file to open"'
    
    def execute(self, *args, **kwargs):
        self.run()
        self.load_sample_from_gui(kwargs['malware'])