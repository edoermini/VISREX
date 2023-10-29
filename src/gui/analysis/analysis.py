import json
import psutil
import re
import time

class Analysis:
    def __init__(self, file=None):
        
        self.workflow = {}
        
        with open('/home/edoardo/Documents/cybersec/thesis/MASup-GUI/src/gui/analysis/workflow.json', 'r') as workflow_file:
            self.workflow = json.load(workflow_file)
        
        self.activities = {}
        self.active_tools = []
    
    def _update_active_tools(self):
        self.active_tools = []

        pids = psutil.pids()

        for pid in pids:
            process = psutil.Process(pid)

            for tool_name, tool in self.workflow['tools'].items():
                active = re.match(tool['regex'], process.name())

                if active:
                    self.active_tools.append(tool_name)

    def update_activities(self):
        self._update_active_tools()
        
        updated_activities = []

        for node_id, node in self.workflow['workflow']['nodes'].items():
            if any([tool in self.active_tools for tool in node['tools']]):

                updated_activities.append(node_id)

                if not node_id in self.activities:
                    self.activities[node_id] = node
                    self.activities[node_id]['start_time'] = time.time()
                    self.activities[node_id]['active'] = True
        
        for node_id, activity in self.activities.items():
            if activity['active'] and node_id not in updated_activities:
                self.activities[node_id]['active'] = False
                self.activities[node_id]['stop_time'] = time.time() - activity['start_time']

    