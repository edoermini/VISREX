import time
import psutil
import re
from time import time
from typing import Any
import pickle
import threading

from .workflow import Workflow

class Analysis:
	def __init__(self, malware_sample:str=""):
		self.workflow = Workflow(malware_sample)
		self.activities : dict[str, str] = {}
		self.active_tools : set[str] = set([])
		
		self.activity_log : list[dict[str, Any]] = []
		self.executables : dict[str, dict[str, Any]] = {}

		# locks both self.activity_log and self.executables resources
		self.activity_log_lock = threading.Lock()
	
	def _update_active_tools(self):
		current_time = time()

		new_active_tools = set()

		pids = psutil.pids()

		for pid in pids:
			try:
				process = psutil.Process(pid)
				process_name = process.name()
			except psutil.NoSuchProcess:
				continue
				
			try:
				executable = process.exe()
				arguments = process.cmdline()[1:]
			except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
				executable = ""
				arguments = []

			for tool_name, tool in self.workflow['tools'].items():
				if re.match(tool['regex'], process_name):
					new_active_tools.add(tool_name)

					with self.activity_log_lock:
						self.executables[tool_name] = {
							'executable': executable,
							'arguments': arguments
						}

		closed_tools = self.active_tools - new_active_tools
		opened_tools = new_active_tools - self.active_tools

		log_entries = [
			{
				"time": current_time,
				"tool": tool,
				"activity": "Close tool",
				**self.executables[tool],

			} for tool in closed_tools
		] + [
			{
				"time": current_time,
				"tool": tool,
				"activity": "Open tool",
				**self.executables[tool]
			} for tool in opened_tools
		]

		with self.activity_log_lock:
			self.activity_log.extend(log_entries)

		self.active_tools = new_active_tools

	def update_activities(self):
		self._update_active_tools()

		current_time = time()

		updated_activities = set()

		for node_id, node in self.workflow['workflow']['nodes'].items():
			if any(tool in self.active_tools for tool in node['tools']):
				updated_activities.add(node_id)

				if node_id not in self.activities:
					self.activities[node_id] = {
						'start_time': current_time,
						'active': True,
						**node  # Copy other attributes from the node
					}

		for node_id, activity in list(self.activities.items()):
			if activity['active'] and node_id not in updated_activities:
				activity.update({
					'active': False,
					'stop_time': current_time - activity['start_time']
				})

	def export_analysis(self, file_path:str):
		with open(file_path, "wb") as file:
			pickle.dump(self, file)

	def update_activity_log(self, data:list[dict[str, Any]]):
		with self.activity_log_lock:
			self.activity_log.extend(data)