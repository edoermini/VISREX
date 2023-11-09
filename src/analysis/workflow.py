import json
from typing import TextIO
from io import IOBase
from graphviz import Digraph

class Workflow:
	def __init__(self, malware_executable:str = ""):
		
		self.__dict__ = {
		  "workflow": {
			"nodes": {
			  "start": {
				"type": "activity",
				"name": "Malware sample" if not malware_executable else malware_executable,
				"description": "",
				"phase": "",
				"color": "#4051B5",
				"results": [],
				"tools": []
			  },
			  "extr_0": {
				"type": "decision",
				"name": "Hidden from WinAPI",
				"description": "",
				"phase": "extraction",
				"color": "#4051B5",
				"results": [],
				"tools": []
			  },
			  "extr_1": {
				"type": "activity",
				"name": "Automatic Extraction",
				"description": "",
				"phase": "extraction",
				"color": "#4051B5",
				"results": [],
				"tools": [
				  "icesword"
				]
			  },
			  "extr_2": {
				"type": "activity",
				"name": "Manual Extraction",
				"description": "",
				"phase": "extraction",
				"color": "#4051B5",
				"results": [],
				"tools": []
			  },
			  "extr_3": {
				"type": "activity",
				"name": "Extract from archive",
				"description": "",
				"phase": "extraction",
				"color": "#4051B5",
				"results": [],
				"tools": []
			  },
			  "pran_0": {
				"type": "activity",
				"name": "Identify the hash",
				"description": "",
				"phase": "Preliminary analysis",
				"color": "#EA8ABA",
				"results": [],
				"tools": [
				  "pestudio"
				]
			  },
			  "pran_1": {
				"type": "activity",
				"name": "Check for malware",
				"description": "",
				"phase": "Preliminary analysis",
				"color": "#EA8ABA",
				"results": [],
				"tools": [
				  "ssdeep",
				  "pestudio"
				]
			  },
			  "pran_2": {
				"type": "activity",
				"name": "Data in open sources",
				"description": "",
				"phase": "Preliminary analysis",
				"color": "#EA8ABA",
				"results": [],
				"tools": []
			  },
			  "pran_3": {
				"type": "activity",
				"name": "Text strings",
				"description": "",
				"phase": "Preliminary analysis",
				"color": "#EA8ABA",
				"results": [],
				"tools": [
				  "pestudio",
				  "idapro",
				  "bintext"
				]
			  },
			  "unpk_0": {
				"type": "activity",
				"name": "Detection of packers or chiphers",
				"description": "",
				"phase": "Unpacking",
				"color":"#2CD551",
				"results": [],
				"tools": [
				  "pestudio",
				  "bintext",
				  "pebrowse",
				  "fileinsight",
				  "peid",
				  "die",
				  "binwalk",
				  "yara"
				]
			  },
			  "unpk_1": {
				"type": "decision",
				"name": "Obfuscated/Compressed or encrypted?",
				"description": "",
				"phase": "Unpacking",
				"color":"#2CD551",
				"results": [],
				"tools": []
			  },
			  "unpk_2": {
				"type": "activity",
				"name": "Automatic decryption or unpacking",
				"description": "",
				"phase": "Unpacking",
				"color":"#2CD551",
				"results": [],
				"tools": [
				  "pebrowse",
				  "winhex",
				  "peexplorer",
				  "procdump32"
				]
			  },
			  "unpk_3": {
				"type": "decision",
				"name": "Has it been decrypted or unpacked?",
				"description": "",
				"phase": "Unpacking",
				"color":"#2CD551",
				"results": [],
				"tools": []
			  },
			  "unpk_4": {
				"type": "activity",
				"name": "Manual decryption or unpacking",
				"description": "",
				"phase": "Unpacking",
				"color":"#2CD551",
				"results": [],
				"tools": [
				  "scylla",
				  "idapro"
				]
			  },
			  "unpk_5": {
				"type": "decision",
				"name": "Has it been decrypted or unpacked?",
				"description": "",
				"phase": "Unpacking",
				"color":"#2CD551",
				"results": [],
				"tools": []
			  },
			  "imgc_0": {
				"type": "activity",
				"name": "Digital material",
				"description": "",
				"phase": "Image creation",
				"color": "#05A8F4",
				"results": [],
				"tools": []
			  },
			  "imgc_1": {
				"type": "activity",
				"name": "Build a virtual machine",
				"description": "",
				"phase": "Image creation",
				"color": "#05A8F4",
				"results": [],
				"tools": []
			  },
			  "imgc_2": {
				"type": "activity",
				"name": "Image animation",
				"description": "",
				"phase": "Image creation",
				"color": "#05A8F4",
				"results": [],
				"tools": []
			  },
			  "stic_0": {
				"type": "activity",
				"name": "Static code analysis",
				"description": "",
				"phase": "Static analysis",
				"color":"#FFC009",
				"results": [],
				"tools": [
				  "idapro",
				  "ghidra",
				  "reverseengineeringcompiler",
				  "loadlib"
				]
			  },
			  "stic_1": {
				"type": "decision",
				"name": "Problem?",
				"description": "",
				"phase": "Static analysis",
				"color":"#FFC009",
				"results": [],
				"tools": []
			  },
			  "stic_2": {
				"type": "activity",
				"name": "IDA Pro plugin",
				"description": "",
				"phase": "Static analysis",
				"color":"#FFC009",
				"results": [],
				"tools": []
			  },
			  "stic_3": {
				"type": "decision",
				"name": "Need dynamic analysis?",
				"description": "",
				"phase": "Static analysis",
				"color":"#FFC009",
				"results": [],
				"tools": []
			  },
			  "dnmc_0": {
				"type": "activity",
				"name": "Dynamic code analysis",
				"description": "",
				"phase": "Dynamic analysis",
				"color": "#FF5252",
				"results": [],
				"tools": [
				  "idapro",
				  "ollydbg",
				  "loadlib"
				]
			  },
			  "dnmc_1": {
				"type": "decision",
				"name": "Problem?",
				"description": "",
				"phase": "Dynamic analysis",
				"color": "#FF5252",
				"results": [],
				"tools": []
			  },
			  "dnmc_2": {
				"type": "activity",
				"name": "OllyDBG Plugin",
				"description": "",
				"phase": "Dynamic analysis",
				"color": "#FF5252",
				"results": [],
				"tools": []
			  },
			  "dnmc_3": {
				"type": "decision",
				"name": "Need more static analysis?",
				"description": "",
				"phase": "Dynamic analysis",
				"color": "#FF5252",
				"results": [],
				"tools": []
			  },
			  "impt_0": {
				"type": "decision",
				"name": "Import table corrupted",
				"description": "",
				"phase": "Import table reconstruction",
				"color":"#9C27B0",
				"results": [],
				"tools": []
			  },
			  "impt_1": {
				"type": "activity",
				"name": "Reconstruct import table",
				"description": "",
				"phase": "Import table reconstruction",
				"color":"#9C27B0",
				"results": [],
				"tools": [
				  "importreconstruction",
				  "icddumpfix"
				]
			  },
			  "bhvr_0": {
				"type": "activity",
				"name": "Pre execution tasks",
				"description": "",
				"phase": "Behavioral analysis",
				"color": "#00A99D",
				"results": [],
				"tools": [
				  	"gdiproc",
					"memoryze",
					"systracer",
					"autoruns",
					"floatnotmyfault",
					"regshot",
					"dirwatch",
					"processhacker",
					"snort",
					"apatedns",
					"spymetool",
					"malcodeanalystpack",
					"netcat",
					"capturebot",
					"psfile",
					"processexplorer",
					"wireshark",
					"mailpot",
					"sniffhit",
					"honeyd",
					"processmonitor"
				]
			  },
			  "bhvr_1": {
				"type": "activity",
				"name": "Run malware",
				"description": "",
				"phase": "Behavioral analysis",
				"color": "#00A99D",
				"results": [],
				"tools": []
			  },
			  "bhvr_2": {
				"type": "activity",
				"name": "Post execution tasks",
				"description": "",
				"phase": "Behavioral analysis",
				"color": "#00A99D",
				"results": [],
				"tools": [
				  	"gdiproc",
					"memoryze",
					"systracer",
					"autoruns",
					"floatnotmyfault",
					"regshot",
					"dirwatch",
					"processhacker",
					"snort",
					"apatedns",
					"spymetool",
					"malcodeanalystpack",
					"netcat",
					"capturebot",
					"psfile",
					"processexplorer",
					"wireshark",
					"mailpot",
					"sniffhit",
					"honeyd",
					"processmonitor"
				]
			  },
			  "bhvr_3": {
				"type": "activity",
				"name": "Dump and RAM analysis",
				"description": "",
				"phase": "Behavioral analysis",
				"color": "#00A99D",
				"phase_id": 6,
				"activity_id": 3,
				"results": [],
				"tools": [
				  "floatnotmyfault",
				  "processmonitor",
				  "processexplorer",
				  "memoryze",
				  "systracer",
				  "processhacker",
				  "autoruns",
				  "gdiproc"
				]
			  },
			  "bhvr_4": {
				"type": "activity",
				"name": "HD analysis",
				"description": "",
				"phase": "Behavioral analysis",
				"color": "#00A99D",
				"results": [],
				"tools": [
				  "spymetool",
				  "regshot",
				  "systracer",
				  "process_monitor",
				  "psfile",
				  "dirwatch"
				]
			  },
			  "bhvr_5": {
				"type": "activity",
				"name": "Network analysis",
				"description": "",
				"phase": "Behavioral analysis",
				"color": "#00A99D",
				"results": [],
				"tools": [
				  "wireshark",
				  "snort",
				  "malcodeanalystpack",
				  "netcat",
				  "honeyd",
				  "capturebot",
				  "processexplorer",
				  "systracer",
				  "processmonitor",
				  "apatedns",
				  "sniffhit",
				  "mailpot"
				]
			  }
			},
			"edges": [
			  {
				"source": "start",
				"destination": "extr_0",
				"value": ""
			  },
			  {
				"source": "extr_0",
				"destination": "extr_1",
				"value": "Yes"
			  },
			  {
				"source": "extr_0",
				"destination": "extr_2",
				"value": "No"
			  },
			  {
				"source": "extr_1",
				"destination": "extr_3",
				"value": ""
			  },
			  {
				"source": "extr_2",
				"destination": "extr_3",
				"value": ""
			  },
			  {
				"source": "extr_3",
				"destination": "pran_0",
				"value": ""
			  },
			  {
				"source": "pran_0",
				"destination": "pran_1",
				"value": ""
			  },
			  {
				"source": "pran_1",
				"destination": "pran_2",
				"value": ""
			  },
			  {
				"source": "pran_2",
				"destination": "pran_3",
				"value": ""
			  },
			  {
				"source": "pran_3",
				"destination": "unpk_0",
				"value": ""
			  },
			  {
				"source": "unpk_0",
				"destination": "unpk_1",
				"value": ""
			  },
			  {
				"source": "unpk_1",
				"destination": "unpk_2",
				"value": "Yes"
			  },
			  {
				"source": "unpk_1",
				"destination": "imgc_0",
				"value": "No"
			  },
			  {
				"source": "unpk_2",
				"destination": "unpk_3",
				"value": ""
			  },
			  {
				"source": "unpk_3",
				"destination": "pran_3",
				"value": "Yes"
			  },
			  {
				"source": "unpk_3",
				"destination": "unpk_4",
				"value": "No"
			  },
			  {
				"source": "unpk_4",
				"destination": "unpk_5",
				"value": ""
			  },
			  {
				"source": "unpk_5",
				"destination": "pran_3",
				"value": "Yes"
			  },
			  {
				"source": "unpk_5",
				"destination": "imgc_0",
				"value": "No"
			  },
			  {
				"source": "imgc_0",
				"destination": "imgc_1",
				"value": ""
			  },
			  {
				"source": "imgc_1",
				"destination": "imgc_2",
				"value": ""
			  },
			  {
				"source": "imgc_2",
				"destination": "stic_0",
				"value": ""
			  },
			  {
				"source": "stic_0",
				"destination": "stic_1",
				"value": ""
			  },
			  {
				"source": "stic_1",
				"destination": "stic_2",
				"value": "Yes"
			  },
			  {
				"source": "stic_1",
				"destination": "stic_3",
				"value": "No"
			  },
			  {
				"source": "stic_2",
				"destination": "stic_0",
				"value": ""
			  },
			  {
				"source": "stic_3",
				"destination": "dnmc_0",
				"value": "Yes"
			  },
			  {
				"source": "stic_3",
				"destination": "impt_0",
				"value": "No"
			  },
			  {
				"source": "dnmc_0",
				"destination": "dnmc_1",
				"value": ""
			  },
			  {
				"source": "dnmc_1",
				"destination": "dnmc_2",
				"value": "Yes"
			  },
			  {
				"source": "dnmc_1",
				"destination": "dnmc_3",
				"value": "No"
			  },
			  {
				"source": "dnmc_2",
				"destination": "dnmc_0",
				"value": ""
			  },
			  {
				"source": "dnmc_3",
				"destination": "stic_0",
				"value": "Yes"
			  },
			  {
				"source": "dnmc_3",
				"destination": "impt_0",
				"value": "No"
			  },
			  {
				"source": "impt_0",
				"destination": "impt_1",
				"value": "Yes"
			  },
			  {
				"source": "impt_0",
				"destination": "bhvr_0",
				"value": "Yes"
			  },
			  {
				"source": "impt_1",
				"destination": "unpk_1",
				"value": ""
			  },
			  {
				"source": "bhvr_0",
				"destination": "bhvr_1",
				"value": ""
			  },
			  {
				"source": "bhvr_1",
				"destination": "bhvr_2",
				"value": ""
			  },
			  {
				"source": "bhvr_2",
				"destination": "bhvr_3",
				"value": ""
			  },
			  {
				"source": "bhvr_3",
				"destination": "bhvr_4",
				"value": ""
			  },
			  {
				"source": "bhvr_4",
				"destination": "bhvr_5",
				"value": ""
			  }
			]
		  },
			"tools": {
				"icesword": {
					"regex": "(?i)^icesword(?:\\.exe)?"
				},
				"pestudio": {
					"regex": "(?i)^pestudio(?:\\.exe)?"
				},
				"ssdeep": {
					"regex": "(?i)^ssdeep(?:\\.exe)?"
				},
				"idapro": {
					"regex": "(?i)^ida(?:pro)?(?:64)?(?:\\.exe)?"
				},
				"bintext": {
					"regex": "(?i)^bintext(?:\\.exe)?"
				},
				"pebrowse": {
					"regex": "(?i)^pebrowse(?:\\.exe)?"
				},
				"fileinsight": {
					"regex": "(?i)^fileinsight(?:\\.exe)?"
				},
				"peid": {
					"regex": "(?i)^peid(?:\\.exe)?"
				},
				"die": {
					"regex": "(?i)^die(?:\\.exe)?"
				},
				"binwalk": {
					"regex": "(?i)^binwalk(?:\\.exe)?"
				},
				"yara": {
					"regex": "(?i)^yara(?:\\.exe)?"
				},
				"winhex": {
					"regex": "(?i)^winhex(?:\\.exe)?"
				},
				"peexplorer": {
					"regex": "(?i)^peexplorer(?:\\.exe)?"
				},
				"procdump32": {
					"regex": "(?i)^procdump32(?:\\.exe)?"
				},
				"scylla": {
					"regex": "(?i)^scylla(?:\\.exe)?"
				},
				"ghidra": {
					"regex": "(?i)^ghidra(?:\\.exe)?"
				},
				"reverseengineeringcompiler": {
					"regex": "(?i)^reverseengineeringcompiler(?:\\.exe)?"
				},
				"ollydbg": {
					"regex": "(?i)^ollydbg(?:\\.exe)?"
				},
				"importreconstruction": {
					"regex": "(?i)^importreconstruction(?:\\.exe)?"
				},
				"floatnotmyfault": {
					"regex": "(?i)^floatnotmyfault(?:\\.exe)?"
				},
				"processmonitor": {
					"regex": "(?i)^proc(?:ess)?mon(?:itor)?(?:32|64)?(?:\\.exe)?"
				},
				"processexplorer": {
					"regex": "(?i)^processexplorer(?:\\.exe)?"
				},
				"memoryze": {
					"regex": "(?i)^memoryze(?:\\.exe)?"
				},
				"systracer": {
					"regex": "(?i)^systracer(?:\\.exe)?"
				},
				"processhacker": {
					"regex": "(?i)^processhacker(?:\\.exe)?"
				},
				"autoruns": {
					"regex": "(?i)^autoruns(?:\\.exe)?"
				},
				"spymetool": {
					"regex": "(?i)^spymetool(?:\\.exe)?"
				},
				"regshot": {
					"regex": "(?i)^regshot(?:\\.exe)?"
				},
				"psfile": {
					"regex": "(?i)^psfile(?:\\.exe)?"
				},
				"wireshark": {
					"regex": "(?i)^wireshark(?:\\.exe)?"
				},
				"snort": {
					"regex": "(?i)^snort(?:\\.exe)?"
				},
				"dirwatch": {
					"regex": "(?i)^dirwatch(?:\\.exe)?"
				},
				"fakedns": {
					"regex": "(?i)^fakedns(?:\\.exe)?"
				},
				"finddll": {
					"regex": "(?i)^finddll(?:\\.exe)?"
				},
				"mailpot": {
					"regex": "(?i)^mailpot(?:\\.exe)?"
				},
				"sniffhit": {
					"regex": "(?i)^sniffhit(?:\\.exe)?"
				},
				"icddumpfix": {
					"regex": "(?i)^icddumpfix(?:\\.exe)?"
				},
				"gdiproc": {
					"regex": "(?i)^gdiproc(?:\\.exe)?"
				},
				"loadlib": {
					"regex": "(?i)^loadlib(?:\\.exe)?"
				},
				"netcat": {
					"regex": "(?i)^netcat(?:\\.exe)?"
				},
				"honeyd": {
					"regex": "(?i)^honeyd(?:\\.exe)?"
				},
				"capturebot": {
					"regex": "(?i)^capturebot(?:\\.exe)?"
				},
				"apatedns": {
					"regex": "(?i)^apatedns(?:\\.exe)?"
				}
			}

		}
		
		self._check_structure()

		if malware_executable:
			self.__dict__['workflow']['nodes']['bhvr_1']['tools'].append(malware_executable)
			self.__dict__['tools'][malware_executable] = {}
			self.__dict__['tools'][malware_executable]['regex'] = malware_executable
	
	def _check_structure(self):
		
		if 'workflow' not in self.__dict__:
			raise ValueError("workflow must contain 2 main keys 'workflow' and 'tools'")
		
		if 'nodes' not in self.__dict__['workflow'] or 'edges' not in self.__dict__['workflow']:
			raise ValueError("'workflow' key must contain the sub keys 'nodes' and 'edges'")

		if not isinstance(self.__dict__['workflow']['nodes'], dict):
			raise ValueError("'nodes' must have a dictionary as value")
		
		if not isinstance(self.__dict__['workflow']['edges'], list):
			raise ValueError("'edges' must have a list as value")

		if not all(['type' in node for _,node in self.__dict__['workflow']['nodes'].items()]):
			raise ValueError("'type' key is missing in one or more nodes")
		
		if not all(['name' in node for _,node in self.__dict__['workflow']['nodes'].items()]):
			raise ValueError("'name' key is missing in one or more nodes")

		if not all(['phase' in node for _,node in self.__dict__['workflow']['nodes'].items()]):
			raise ValueError("'phase' key is missing in one or more nodes")

		if not all(['tools' in node for _,node in self.__dict__['workflow']['nodes'].items()]):
			raise ValueError("'tools' key is missing in one or more nodes")
		

		if not all(['source' in edge for edge in self.__dict__['workflow']['edges']]):
			raise ValueError("'source' key is missing in one or more edges")

		if not all(['destination' in edge for edge in self.__dict__['workflow']['edges']]):
			raise ValueError("'destination' key is missing in one or more edges")

		if not all(['value' in edge for edge in self.__dict__['workflow']['edges']]):
			raise ValueError("'value' key is missing in one or more edges")
		
	def __getitem__(self, key):
		return self.__dict__[key]

	def __contains__(self, key):
		return key in self.__dict__

	def __len__(self):
		return len(self.__dict__)

	def __repr__(self):
		return repr(self.__dict__)
	
	def dot_code(self):
		dot = Digraph(comment="Malware Analysis Flowchart")
		dot.attr('node', style="rounded,filled", shape="box", fillcolor="lightblue", fontname="Arial")
		dot.attr('edge', fontname="Arial")

		for node_id, node in self.__dict__['workflow']['nodes'].items():
			dot.node(node_id, node["name"], shape="ellipse" if node["type"] == "activity" else "diamond", style="filled", fillcolor=node["color"])
	  
		for edge in self.__dict__['workflow']['edges']:
			dot.edge(edge["source"],edge["destination"], label=edge["value"])
		
		return dot
	  