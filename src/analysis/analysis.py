import psutil
import re
from time import time
from typing import Any
import json
from threading import Lock
from datetime import datetime
from time import time
from collections import OrderedDict
import copy
import os
import pathlib

from .workflow import Workflow
from .analysis_log_entry import AnalysisLogEntry

class Analysis:
	def __init__(self, malware_sample):
		self.malware_sample = str(pathlib.Path(malware_sample))

		self.workflow = Workflow(os.path.basename(malware_sample))

		# a structure logging the activities at level of workflow actions
		self.activities : dict[str, Any] = {}

		# stores the current active tools, used to determine closed and opened tools
		self.active_tools : set[str] = set([])
		
		# the entire activity log at level of tools
		self.activity_log : list[AnalysisLogEntry] = []

		# stores all the executables found for a tool
		self.executables : dict[str, list[str]] = {}
		
		# stores for each running tool the executable and the arguments
		self.running_tools_info : dict[str, OrderedDict[str, Any]] = {}

		# locks self.activities, self.activity_log and self.executables resources
		self.activities_lock = Lock()
		self.activity_log_lock = Lock()
		self.executables_lock = Lock()
	
	def _update_active_tools(self):

		old_active_tools = self.active_tools.copy()
		self.active_tools = set()

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
					self.active_tools.add(tool_name)
					
					if tool_name not in self.running_tools_info:
							self.running_tools_info[tool_name] = {
								'executable':'',
								'arguments':[]
							}

					if executable:
						self.update_executable(tool_name, executable)

						if not self.running_tools_info[tool_name]['executable']:
							self.running_tools_info[tool_name]['executable'] = executable

					if arguments:
						if not self.running_tools_info[tool_name]['arguments']:
							self.running_tools_info[tool_name]['arguments'] = arguments
		
		return old_active_tools

	def _update_activity_log(self, current_time:int, old_active_tools:set, new_active_tools:set):

		closed_tools = list(old_active_tools - new_active_tools)
		opened_tools = list(new_active_tools - old_active_tools)
		
		log_entries = []

		for i, tool in enumerate(closed_tools + opened_tools):
			activity = "Close tool"

			running_tool_info = self.running_tools_info.pop(tool)

			if len(closed_tools) == 0 or i > len(closed_tools):
				activity = "Open tool"
				self.running_tools_info[tool] = running_tool_info
			
			log_entries.append(AnalysisLogEntry(
				tool,
				activity,
				os.path.basename(running_tool_info['executable']),
				running_tool_info['arguments'],
				"",
				current_time,
			))

		self.update_activity_log(log_entries)

	def _update_activities(self, current_time:int):
		updated_activities = set()

		for node_id, node in self.workflow['workflow']['nodes'].items():
			if any(tool in self.active_tools for tool in node['tools']):
				updated_activities.add(node_id)

				with self.activities_lock:
					if node_id not in self.activities:
						self.activities[node_id] = {
							'start_time': current_time,
							'active': True,
						}

		with self.activities_lock:
			for node_id, activity in list(self.activities.items()):
				if activity['active'] and node_id not in updated_activities:
					activity.update({
						'active': False,
						'stop_time': current_time
					})

	def update(self):
		current_time = time()

		old_active_tools = self._update_active_tools()
		self._update_activity_log(current_time, old_active_tools, self.active_tools)
		self._update_activities(current_time)

	def export_analysis(self, file_path:str):
		
		json_analysis = {
			'malware_sample': self.malware_sample,
			'workflow': self.workflow.__dict__,
			'activities': self.activities,
			'activity_log': [log.__dict__ for log in self.activity_log]
		}

		with open(file_path, "w") as file:
			json.dump(json_analysis, file)
	
	@staticmethod
	def import_analysis(file_path:str):

		json_analysis = {}

		with open(file_path, "r") as file:
			json_analysis = json.load(file)

		analysis = Analysis(json_analysis['malware_sample'])
		analysis.workflow = Workflow.from_dict(json_analysis['workflow'])
		analysis.activities = json_analysis['activities']

		analysis.activity_log = [AnalysisLogEntry(**log_entry) for log_entry in json_analysis['activity_log']]

		return analysis

	def update_activity_log(self, data:list[AnalysisLogEntry] | AnalysisLogEntry):
		with self.activity_log_lock:

			if isinstance(data, list):
				self.activity_log.extend(data)
			elif isinstance(data, AnalysisLogEntry):
				self.activity_log.append(data)
	
	def update_executable(self, tool_name:str, executable:str):
		with self.executables_lock:
			if tool_name not in self.executables:
				self.executables[tool_name] = []
			
			if executable not in self.executables[tool_name]:
				self.executables[tool_name].append(executable)
	
	def get_executables(self):
		executables = {}

		with self.executables_lock:
			for tool_name, tool_exec in self.executables.items():
				executables[tool_name] = tool_exec.copy()
		
		return executables

	def get_activity_log(self, from_index:int = 0) -> AnalysisLogEntry:
		log = []

		with self.activity_log_lock:
			for log_entry in self.activity_log[from_index:]:
				log.append(copy.copy(log_entry))
		
		return log

	def get_activity_log_entry(self, index:int) -> AnalysisLogEntry:

		with self.activity_log_lock:
			return copy.copy(self.activity_log[index])
	
	def get_activity_log_len(self):
		with self.activity_log_lock:
			return len(self.activity_log)

	def get_installed_tools(self, node_id:str):
		executables = self.get_executables()
		installed_tools = set(executables.keys())
		node_tools = set(self.workflow['workflow']['nodes'][node_id]['tools'])

		return list(installed_tools.intersection(node_tools))

	def get_tools(self, node_id:str):
		return self.workflow['workflow']['nodes'][node_id]['tools']
	
	def get_executable(self, tool:str):
		with self.executables_lock:
			if tool in self.executables:
				return self.executables[tool].copy()
		
		return []
	
	def update_log_entry_notes(self, index:int, notes:str):
		with self.activity_log_lock:
			self.activity_log[index].notes = notes
	
	def change_malware_sample(self, malware_sample:str):
		self.malware_sample = str(pathlib.Path(malware_sample))
		self.workflow = Workflow(os.path.basename(malware_sample))
	
	def update_log_entry(self, index:int, log_etry:AnalysisLogEntry):
		with self.activity_log_lock:
			self.activity_log[index] = log_etry
	
	def delete_log_entry(self, index:int):
		with self.activity_log_lock:
			self.activity_log.pop(index)
	
	def update_activity(self, node_id:str, active:bool):
		
		with self.activities_lock:
			if active:
				# activity started
				if node_id not in self.activities:
					self.activities[node_id] = {
						'start_time': time(),
						'active': True,
					}
			
				else:
					if not self.activities[node_id]['active']:
						self.activities[node_id].update({
							'active': True,
							'start_time': time()
						})
			else:
				# activity stopped
				if self.activities[node_id]['active']:
					self.activities[node_id].update({
						'active': False,
						'stop_time': time()
					})
