from PyQt6.QtCore import QThread, pyqtSignal

import platform
import os
import re
import subprocess

from analysis import Analysis

class ExecutablesUpdater(QThread):
	finished = pyqtSignal()
	executableFound = pyqtSignal()

	def __init__(self, analysis:Analysis):
		super().__init__()

		self.analysis = analysis
		self.extensions = {'', '.bin', '.elf', '.exe', '.com', '.sh', '.bat'}
	
	def run(self):
		# Your worker thread logic goes here
		self.find_executables()
		self.finished.emit()

	def find_executables(self):
		system_name = platform.system()

		self._find_exec_in_path(os.path.expanduser('~'))

		if system_name == "Windows":
			self._find_exec_in_path(r'C:\Program Files')
		elif system_name == "Linux":
			self._find_exec_in_path('/usr/bin')
			self._find_exec_in_path('/usr/sbin')
			self._find_exec_in_path('/usr/local/bin')
		elif system_name == "Darwin":
			self._find_exec_in_path('/Applications')
			self._find_exec_in_path('/usr/local/bin')
		
	def _is_valid_executable(self, file_path):
		valid = False
		process = None

		try:
			# Attempt to execute the file with a harmless command
			process = subprocess.Popen([file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			valid=True
		except subprocess.CalledProcessError:
			valid=False
		except Exception:
			valid=False
		finally:
			if process is not None:
				process.kill()
		
		return valid

	def _find_exec_in_path(self, path:str):
		for tool_name, tool in self.analysis.workflow['tools'].items():
			pattern = re.compile(tool['regex'])
			
			for root, dirs, files in os.walk(path):
				for file in files:
					if pattern.search(file):
						# Check for common executable file extensions
						_, extension = os.path.splitext(file)
						
						if extension.lower() in self.extensions:
							
							executable = os.path.join(root, file)
							self.executableFound.emit()
							self.analysis.update_executable(tool_name, executable)