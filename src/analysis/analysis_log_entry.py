from datetime import datetime
from time import time

class AnalysisLogEntry:
    def __init__(self, tool:str, activity:str, executable:str, arguments:list, notes:str="", log_time:int = None):
        self.tool = tool
        self.activity = activity
        self.executable = executable
        self.arguments = arguments
        self.time = int(time())

        if log_time:
            self.time = log_time

        self.notes : str = notes

    def to_json(self, string_values:bool = False):
        return {
            'time':datetime.fromtimestamp(self.time).isoformat() if string_values else self.time,
            'tool':self.tool,
            'activity':self.activity,
            'executable':self.executable,
            'arguments':','.join(self.arguments) if string_values else self.arguments,
            'notes': self.notes
        }

    def to_list(self, string_values:bool = False):
        return [
            datetime.fromtimestamp(self.time).isoformat() if string_values else self.time,
            self.tool,
            self.activity,
            self.executable,
            ','.join(self.arguments) if string_values else self.arguments,
            self.notes
        ]
    
    def __copy__(self):
        return AnalysisLogEntry(
            self.tool,
            self.activity,
            self.executable,
            self.arguments,
            self.notes,
            self.time
        )