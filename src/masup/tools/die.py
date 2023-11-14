from masup.tools.generics import DesktopTool

class DiE(DesktopTool):
    def __init__(self, path: str):
        super().__init__(path)

        self.load_file_button_locator = r'name:...'
        self.open_file_pop_up_window_locator = r'name:"Open file..."'

    def load_sample(self, sample_path):
        self.library.click(self.load_file_button_locator)
        self.library.send_keys('name:"Open file..."',sample_path + "{ENTER}")