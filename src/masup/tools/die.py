from masup.tools.generics import DesktopTool

class Tool(DesktopTool):
    def __init__(self, path: str):
        super().__init__(path)

        self.load_file_button_locator = r'name:...'
        self.open_file_pop_up_window_locator = r'name:"Open file..."'