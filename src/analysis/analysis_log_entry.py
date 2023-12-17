from datetime import datetime
from time import time

class AnalysisLogEntry:
    def __init__(self, tool:str, activity:str, executable:str, arguments:list, notes:str="", log_time:int = None):
        self.tool = tool
        self.activity = activity
        self.executable = executable
        self.arguments = arguments
        self.log_time = int(time())

        if log_time:
            self.log_time = log_time

        self.notes : str = notes
    
    @staticmethod
    def get_keys():
        return ['log_time', 'tool', 'activity', 'executable', 'arguments', 'notes']

    def to_json(self, string_values:bool = False):
        return {
            'log_time':datetime.fromtimestamp(self.log_time).isoformat() if string_values else self.log_time,
            'tool':self.tool,
            'activity':self.activity,
            'executable':self.executable,
            'arguments':','.join(self.arguments) if string_values else self.arguments,
            'notes': self.notes
        }

    def to_list(self, string_values:bool = False):
        return [
            datetime.fromtimestamp(self.log_time).isoformat() if string_values else self.log_time,
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
            self.log_time
        )