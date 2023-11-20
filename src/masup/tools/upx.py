from masup.tools.generics import CLITool

class Tool(CLITool):
    def __init__(self, path: str):
        super().__init__(path)

        self.output = str()
    
    def set_output(self, file:str):
        self.output = file

    def execute(self, packed_file:str):
        args = ['-d',]

        if self.output:
            args += ['-o', self.output]
        
        args.append(packed_file)

        self._run(args)