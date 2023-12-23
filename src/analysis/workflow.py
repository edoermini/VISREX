from graphviz import Digraph

class Workflow:
	def __init__(self, malware_executable:str = ""):
		
		self.__dict__ = {
		  "workflow": {
			"nodes": {
			  "start": {
				"type": "activity",
				"name": "Start",
				"description": "",
				"phase": "",
				"color": "",
				"results": [],
				"tools": []
			  },
			  "extr_0": {
				"type": "decision",
				"name": "Malware Specimen Hidden?",
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
				"tools": []
			  },
			  "extr_2": {
				"type": "decision",
				"name": "Has it Been Extracted?",
				"description": "",
				"phase": "extraction",
				"color": "#4051B5",
				"results": [],
				"tools": []
			  },
			  "extr_3": {
				"type": "activity",
				"name": "Manual Extraction",
				"description": "",
				"phase": "extraction",
				"color": "#4051B5",
				"results": [],
				"tools": []
			  },
			  "extr_4": {
				"type": "activity",
				"name": "Extract from archive",
				"description": "",
				"phase": "extraction",
				"color": "#4051B5",
				"results": [],
				"tools": []
			  },
			  "exan_0": {
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
			  "exan_1": {
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
			  "exan_2": {
				"type": "activity",
				"name": "Data in open sources",
				"description": "",
				"phase": "Preliminary analysis",
				"color": "#EA8ABA",
				"results": [],
				"tools": []
			  },
			  "exan_3": {
				"type": "activity",
				"name": "Text strings",
				"description": "",
				"phase": "Preliminary analysis",
				"color": "#EA8ABA",
				"results": [],
				"tools": [
				  "pestudio",
				  "idapro",
				  "bintext",
				  "winhex",
				  "peview"
				]
			  },
			  "exan_4": {
				"type": "activity",
				"name": "File Format",
				"description": "",
				"phase": "Preliminary analysis",
				"color": "#EA8ABA",
				"results": [],
				"tools": [
				  "pestudio",
				  "idapro",
				  "binwalk",
				  "pebrowse",
				  "dependencywalker",
				  "lordpe",
				  "peview"
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
				  "peview",
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
				"type": "decision",
				"name": "Packer identified?",
				"description": "",
				"phase": "Unpacking",
				"color":"#2CD551",
				"results": [],
				"tools": []
			  },
			  "unpk_3": {
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
				  "procdump32",
				  "upx"
				]
			  },
			  "unpk_4": {
				"type": "decision",
				"name": "Has it been automatically decrypted or unpacked?",
				"description": "",
				"phase": "Unpacking",
				"color":"#2CD551",
				"results": [],
				"tools": []
			  },
			  "unpk_5": {
				"type": "activity",
				"name": "Manual decryption or unpacking",
				"description": "",
				"phase": "Unpacking",
				"color":"#2CD551",
				"results": [],
				"tools": [
				  "idapro",
				  "ollydbg",
				]
			  },
			  "unpk_6": {
				"type": "decision",
				"name": "Has it been manually decrypted or unpacked?",
				"description": "",
				"phase": "Unpacking",
				"color":"#2CD551",
				"results": [],
				"tools": []
			  },
			#   "imgc_0": {
			# 	"type": "activity",
			# 	"name": "Digital material",
			# 	"description": "",
			# 	"phase": "Image creation",
			# 	"color": "#05A8F4",
			# 	"results": [],
			# 	"tools": []
			#   },
			#   "imgc_1": {
			# 	"type": "activity",
			# 	"name": "Build a virtual machine",
			# 	"description": "",
			# 	"phase": "Image creation",
			# 	"color": "#05A8F4",
			# 	"results": [],
			# 	"tools": []
			#   },
			#   "imgc_2": {
			# 	"type": "activity",
			# 	"name": "Image animation",
			# 	"description": "",
			# 	"phase": "Image creation",
			# 	"color": "#05A8F4",
			# 	"results": [],
			# 	"tools": []
			#   },
			  "stic_0": {
				"type": "activity",
				"name": "Static code analysis",
				"description": "",
				"phase": "Static analysis",
				"color":"#FFC009",
				"results": [],
				"tools": [
				  "pebrowse",
				  "idapro",
				  "ghidra",
				  "loadlib"
				]
			  },
			#   "stic_1": {
			# 	"type": "decision",
			# 	"name": "Problem?",
			# 	"description": "",
			# 	"phase": "Static analysis",
			# 	"color":"#FFC009",
			# 	"results": [],
			# 	"tools": []
			#   },
			#   "stic_2": {
			# 	"type": "activity",
			# 	"name": "IDA Pro plugin",
			# 	"description": "",
			# 	"phase": "Static analysis",
			# 	"color":"#FFC009",
			# 	"results": [],
			# 	"tools": []
			#   },
			#   "stic_3": {
			# 	"type": "decision",
			# 	"name": "Need dynamic analysis?",
			# 	"description": "",
			# 	"phase": "Static analysis",
			# 	"color":"#FFC009",
			# 	"results": [],
			# 	"tools": []
			#   },
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
			#   "dnmc_1": {
			# 	"type": "decision",
			# 	"name": "Problem?",
			# 	"description": "",
			# 	"phase": "Dynamic analysis",
			# 	"color": "#FF5252",
			# 	"results": [],
			# 	"tools": []
			#   },
			#   "dnmc_2": {
			# 	"type": "activity",
			# 	"name": "OllyDBG Plugin",
			# 	"description": "",
			# 	"phase": "Dynamic analysis",
			# 	"color": "#FF5252",
			# 	"results": [],
			# 	"tools": []
			#   },
			  "dnmc_3": {
				"type": "decision",
				"name": "Need Static Analysis?",
				"description": "",
				"phase": "Dynamic analysis",
				"color": "#FF5252",
				"results": [],
				"tools": []
			  },
			  "dnmc_4": {
				"type": "decision",
				"name": "Need More Dynamic Analysis?",
				"description": "",
				"phase": "Dynamic analysis",
				"color": "#FF5252",
				"results": [],
				"tools": []
			  },
			  "impt_0": {
				"type": "activity",
				"name": "Check Import Table",
				"description": "",
				"phase": "Import table reconstruction",
				"color":"#9C27B0",
				"results": [],
				"tools": [
					"pestudio",
					"pebrowse",
					"idapro",
					"scylla",
					"lordpe"
				]
			  },
			  "impt_1": {
				"type": "decision",
				"name": "Import table corrupted",
				"description": "",
				"phase": "Import table reconstruction",
				"color":"#9C27B0",
				"results": [],
				"tools": []
			  },
			  "impt_2": {
				"type": "activity",
				"name": "Reconstruct import table",
				"description": "",
				"phase": "Import table reconstruction",
				"color":"#9C27B0",
				"results": [],
				"tools": [
				  "importreconstructor",
				  "icddumpfix",
				  "scylla"
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
					"systracer",
					"autoruns",
					"regshot",
					"dirwatch",
					"processhacker",
					"apatedns",
					"spymetool",
					"malcodeanalystpack",
					"netcat",
					"psfile",
					"processexplorer",
					"wireshark",
					"mailpot",
					"sniffhit",
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
					"systracer",
					"autoruns",
					"regshot",
					"dirwatch",
					"processhacker",
					"apatedns",
					"spymetool",
					"malcodeanalystpack",
					"netcat",
					"psfile",
					"processexplorer",
					"wireshark",
					"mailpot",
					"sniffhit",
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
				  "processmonitor",
				  "processexplorer",
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
				  "malcodeanalystpack",
				  "netcat",
				  "processexplorer",
				  "systracer",
				  "processmonitor",
				  "apatedns",
				  "sniffhit",
				  "mailpot"
				]
			  },
			  "stop": {
				  "type": "activity",
				  "name": "End",
				  "description": "",
				  "phase": "",
				  "color": "",
				  "results": [],
				  "tools": []
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
				"destination": "bhvr_0",
				"value": "No"
			  },
			  {
				"source": "extr_1",
				"destination": "extr_2",
				"value": ""
			  },
			  {
				"source": "extr_2",
				"destination": "extr_3",
				"value": "No"
			  },
			  {
				"source": "extr_2",
				"destination": "extr_4",
				"value": "Yes"
			  },
			  {
				"source": "extr_3",
				"destination": "extr_4",
				"value": ""
			  },
			  {
				"source": "extr_4",
				"destination": "bhvr_0",
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
			  },
			  {
				"source": "bhvr_5",
				"destination": "exan_0",
				"value": ""
			  },
			  {
				"source": "exan_0",
				"destination": "exan_1",
				"value": ""
			  },
			  {
				"source": "exan_1",
				"destination": "exan_2",
				"value": ""
			  },
			  {
				"source": "exan_2",
				"destination": "exan_3",
				"value": ""
			  },
			  {
				"source": "exan_3",
				"destination": "exan_4",
				"value": ""
			  },
			  {
				"source": "exan_4",
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
				"destination": "stic_0",
				"value": "No"
			  },
			#   {
			# 	"source": "unpk_1",
			# 	"destination": "imgc_0",
			# 	"value": "No"
			#   },
			  {
				"source": "unpk_2",
				"destination": "unpk_3",
				"value": "Yes"
			  },
              {
				"source": "unpk_2",
				"destination": "unpk_5",
				"value": "No"
			  },
			  {
				"source": "unpk_3",
				"destination": "unpk_4",
				"value": ""
			  },
			  {
				"source": "unpk_4",
				"destination": "exan_3",
				"value": "Yes"
			  },
			  {
				"source": "unpk_4",
				"destination": "unpk_5",
				"value": "No"
			  },
			  {
				"source": "unpk_5",
				"destination": "unpk_6",
				"value": ""
			  },
			  {
				"source": "unpk_6",
				"destination": "impt_0",
				"value": "Yes"
			  },
			  {
				"source": "unpk_6",
				"destination": "dnmc_0",
				"value": "No"
			  },
			#   {
			# 	"source": "unpk_5",
			# 	"destination": "imgc_0",
			# 	"value": "No"
			#   },
			#   {
			# 	"source": "imgc_0",
			# 	"destination": "imgc_1",
			# 	"value": ""
			#   },
			#   {
			# 	"source": "imgc_1",
			# 	"destination": "imgc_2",
			# 	"value": ""
			#   },
			#   {
			# 	"source": "imgc_2",
			# 	"destination": "stic_0",
			# 	"value": ""
			#   },
			  {
				"source": "impt_0",
				"destination": "impt_1",
				"value": ""
			  },
			  {
				"source": "impt_1",
				"destination": "impt_2",
				"value": "Yes"
			  },
			  {
				"source": "impt_1",
				"destination": "stic_0",
				"value": "No"
			  },
			  {
				"source": "impt_2",
				"destination": "exan_3",
				"value": ""
			  },
			  {
				"source": "stic_0",
				"destination": "dnmc_0",
				"value": ""
			  },
			#   {
			# 	"source": "stic_0",
			# 	"destination": "stic_1",
			# 	"value": ""
			#   },
			#   {
			# 	"source": "stic_1",
			# 	"destination": "stic_2",
			# 	"value": "Yes"
			#   },
			#   {
			# 	"source": "stic_1",
			# 	"destination": "stic_3",
			# 	"value": "No"
			#   },
			#   {
			# 	"source": "stic_2",
			# 	"destination": "stic_0",
			# 	"value": ""
			#   },
			#   {
			# 	"source": "stic_3",
			# 	"destination": "dnmc_0",
			# 	"value": "Yes"
			#   },
			#   {
			# 	"source": "stic_3",
			# 	"destination": "stop",
			# 	"value": "No"
			#   },
			  {
				"source": "dnmc_0",
				"destination": "dnmc_3",
				"value": ""
			  },
			#   {
			# 	"source": "dnmc_0",
			# 	"destination": "dnmc_1",
			# 	"value": ""
			#   },
			#   {
			# 	"source": "dnmc_1",
			# 	"destination": "dnmc_2",
			# 	"value": "Yes"
			#   },
			#   {
			# 	"source": "dnmc_1",
			# 	"destination": "dnmc_3",
			# 	"value": "No"
			#   },
			#   {
			# 	"source": "dnmc_2",
			# 	"destination": "dnmc_0",
			# 	"value": ""
			#   },
			  {
				"source": "dnmc_3",
				"destination": "stic_0",
				"value": "Yes"
			  },
			  {
				"source": "dnmc_3",
				"destination": "dnmc_4",
				"value": "No"
			  },
			  {
				"source": "dnmc_4",
				"destination": "dnmc_0",
				"value": "Yes"
			  },
			  {
				"source": "dnmc_4",
				"destination": "stop",
				"value": "No"
			  },
			]
		  },
			"tools": {
				"pestudio": {
					"regex": r"(?i)^pestudio(?:\.exe)?",
					"nature": "GUI"
				},
				"ssdeep": {
					"regex": r"(?i)^ssdeep(?:\.exe)?",
					"nature": "CLI"
				},
				"idapro": {
					"regex": r"(?i)^ida(?:pro)?(?:64)?(?:\.exe)?",
					"nature": "GUI"
				},
				"bintext": {
					"regex": r"(?i)^bintext(?:\.exe)?",
					"nature": "GUI"
				},
				"pebrowse": {
					"regex": r"(?i)^pebrowse(?:.*)(?:\.exe)?",
					"nature": "GUI"
				},
				"fileinsight": {
					"regex": r"(?i)^fileinsight(?:\.exe)?",
					"nature": "GUI"
				},
				"peid": {
					"regex": r"(?i)^peid(?:\.exe)?",
					"nature": "GUI"
				},
				"die": {
					"regex": r"(?i)^die(?:\.exe)?",
					"nature": "GUI"
				},
				"binwalk": {
					"regex": r"(?i)^binwalk(?:\.exe)?",
					"nature": "CLI"
				},
				"yara": {
					"regex": r"(?i)^yara(?:\.exe)?",
					"nature": "CLI"
				},
				"winhex": {
					"regex": r"(?i)^winhex(?:\.exe)?",
					"nature": "GUI"
				},
				"peexplorer": {
					"regex": r"(?i)^pe(?:\\s)?explorer(?:\.exe)?",
					"nature": "GUI"
				},
				"procdump32": {
					"regex": r"(?i)^procdump32(?:\.exe)?",
					"nature": "CLI"
				},
				"scylla": {
					"regex": r"(?i)^scylla(?:\.exe)?",
					"nature": "GUI"
				},
				"upx": {
					"regex": r"(?i)^upx(?:\.exe)?",
					"nature": "CLI"
				},
				"ghidra": {
					"regex": r"(?i)^ghidra(?:\.exe)?",
					"nature": "GUI"
				},
				"ollydbg": {
					"regex": r"(?i)^ollydbg(?:\.exe)?",
					"nature": "GUI"
				},
				"importreconstructor": {
					"regex": r"(?i)^imp(?:ort)?rec(?:onstructor)?(?:\.exe)?",
					"nature": "GUI"
				},
				"processmonitor": {
					"regex": r"(?i)^proc(?:ess)?mon(?:itor)?(?:32|64)?(?:\.exe)?",
					"nature": "GUI"
				},
				"processexplorer": {
					"regex": r"(?i)^process(?:\s)?explorer(?:\.exe)?",
					"nature": "GUI"
				},
				"systracer": {
					"regex": r"(?i)^systracer(?:\.exe)?",
					"nature": "GUI"
				},
				"processhacker": {
					"regex": r"(?i)^processhacker(?:\.exe)?",
					"nature": "GUI"
				},
				"autoruns": {
					"regex": r"(?i)^autoruns(?:\.exe)?",
					"nature": "GUI"
				},
				"spymetool": {
					"regex": r"(?i)^spymetool(?:\.exe)?",
					"nature": "GUI"
				},
				"regshot": {
					"regex": r"(?i)^regshot(?:\.exe)?",
					"nature": "GUI"
				},
				"psfile": {
					"regex": r"(?i)^psfile(?:\.exe)?",
					"nature": "CLI"
				},
				"wireshark": {
					"regex": r"(?i)^wireshark(?:\.exe)?",
					"nature": "GUI"
				},
				"dirwatch": {
					"regex": r"(?i)^dirwatch(?:\.exe)?",
					"nature": "GUI"
				},
				"fakedns": {
					"regex": r"(?i)^fakedns(?:\.exe)?",
					"nature": "CLI-GUI"
				},
				"finddll": {
					"regex": r"(?i)^finddll(?:\.exe)?",
					"nature": "CLI"
				},
				"mailpot": {
					"regex": r"(?i)^mailpot(?:\.exe)?",
					"nature": "GUI"
				},
				"sniffhit": {
					"regex": r"(?i)^sniffhit(?:\.exe)?",
					"nature": "GUI"
				},
				"icddumpfix": {
					"regex": r"(?i)^icddumpfix(?:\.exe)?",
					"nature": "GUI"
				},
				"gdiproc": {
					"regex": r"(?i)^gdiproc(?:\.exe)?",
					"nature": "CLI"
				},
				"loadlib": {
					"regex": r"(?i)^loadlib(?:\.exe)?",
					"nature": "CLI"
				},
				"netcat": {
					"regex": r"(?i)^netcat(?:\.exe)?",
					"nature": "CLI"
				},
				"apatedns": {
					"regex": r"(?i)^apatedns(?:\.exe)?",
					"nature": "GUI"
				},
				"dependencywalker": {
					"regex": r"(?i)^dependency(?:\s*)walker(?:\.exe)?",
					"nature": "GUI"
				},
				"lordpe": {
					"regex": r"(?i)^lordpe(?:\.exe)?",
					"nature": "GUI"
				},
				"peview": {
					"regex": r"(?i)^peview(?:\.exe)?",
					"nature": "GUI"
				}
			}

		}
		Workflow.check_structure(self.__dict__)

		if malware_executable:
			self.__dict__['workflow']['nodes']['bhvr_1']['tools'].append(malware_executable)
			self.__dict__['tools'][malware_executable] = {}
			self.__dict__['tools'][malware_executable]['regex'] = malware_executable
	
	@staticmethod
	def check_structure(workflow:dict):
		
		if 'workflow' not in workflow:
			raise ValueError("workflow must contain 2 main keys 'workflow' and 'tools'")
		
		if 'nodes' not in workflow['workflow'] or 'edges' not in workflow['workflow']:
			raise ValueError("'workflow' key must contain the sub keys 'nodes' and 'edges'")

		if not isinstance(workflow['workflow']['nodes'], dict):
			raise ValueError("'nodes' must have a dictionary as value")
		
		if not isinstance(workflow['workflow']['edges'], list):
			raise ValueError("'edges' must have a list as value")

		if not all(['type' in node for _,node in workflow['workflow']['nodes'].items()]):
			raise ValueError("'type' key is missing in one or more nodes")
		
		if not all(['name' in node for _,node in workflow['workflow']['nodes'].items()]):
			raise ValueError("'name' key is missing in one or more nodes")

		if not all(['phase' in node for _,node in workflow['workflow']['nodes'].items()]):
			raise ValueError("'phase' key is missing in one or more nodes")

		if not all(['tools' in node for _,node in workflow['workflow']['nodes'].items()]):
			raise ValueError("'tools' key is missing in one or more nodes")
		

		if not all(['source' in edge for edge in workflow['workflow']['edges']]):
			raise ValueError("'source' key is missing in one or more edges")

		if not all(['destination' in edge for edge in workflow['workflow']['edges']]):
			raise ValueError("'destination' key is missing in one or more edges")

		if not all(['value' in edge for edge in workflow['workflow']['edges']]):
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

	def get_nodes_ids(self):
		return self.__dict__['workflow']['nodes'].keys()

	@staticmethod
	def from_dict(obj):
		Workflow.check_structure(obj)

		workflow = Workflow()
		workflow.__dict__ = obj

		return workflow
	  