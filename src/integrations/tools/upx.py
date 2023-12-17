from integrations.generics import CLITool

class Tool(CLITool):
    def __init__(self, path: str):
        super().__init__(path)