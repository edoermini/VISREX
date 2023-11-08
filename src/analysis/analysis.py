import time
import psutil
import re
import time
from datetime import datetime
from typing import Any
import os

from .workflow import Workflow

class Analysis:
    def __init__(self, workflow:Workflow):
        self.workflow = workflow
        self.activities : dict[str, str] = {}
        self.active_tools : set[str] = set([])
        self.activity_log : list[dict[str, Any]] = []
        self.executables : dict[str, str] = {}
    
    def _update_active_tools(self):
        new_active_tools = set([])

        pids = psutil.pids()

        for pid in pids:
            try:
                process = psutil.Process(pid)
            except psutil.NoSuchProcess:
                continue

            for tool_name, tool in self.workflow['tools'].items():
                active = re.match(tool['regex'], process.name())

                if active:
                    new_active_tools.add(tool_name)
                    self.executables[tool_name] = process.exe()
            
        already_opened_tools = new_active_tools.intersection(self.active_tools)

        closed_tools = self.active_tools - already_opened_tools
        opened_tools = new_active_tools - already_opened_tools
        
        for tool in closed_tools:
            # tool was active and now is not anymore
            
            self.activity_log.append({
                "time":time.time(),
                "tool":tool,
                "opened":False,
                "executable": self.executables[tool]
            })
            
        for tool in opened_tools:
            # opended a tool that was closed
 
            self.activity_log.append({
                "time":time.time(),
                "tool":tool,
                "opened":True,
                "executable": self.executables[tool]
            })
        
        self.active_tools = new_active_tools

    def update_activities(self):
        self._update_active_tools()
        
        updated_activities = []

        for node_id, node in self.workflow['workflow']['nodes'].items():
            if any([tool in self.active_tools for tool in node['tools']]):

                updated_activities.append(node_id)

                if not node_id in self.activities:
                    start_time = int(time.time())

                    self.activities[node_id] = node
                    self.activities[node_id]['start_time'] = start_time
                    self.activities[node_id]['active'] = True
        
        for node_id, activity in self.activities.items():
            if activity['active'] and node_id not in updated_activities:
                self.activities[node_id]['active'] = False
                self.activities[node_id]['stop_time'] = time.time() - activity['start_time']

    