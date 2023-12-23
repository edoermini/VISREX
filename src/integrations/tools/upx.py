from integrations.generics import CLITool

class Tool(CLITool):
    def __init__(self, path: str):
        super().__init__(path)
    
    def execute(self, *args, **kwargs):
        _, _, returncode = self._run(['-d', kwargs['malware'], '-o', kwargs['output']])
        
        if returncode == 0:
            return f"Successfully unpacked to {kwargs['output']}"

        return "Unpacking Failed"