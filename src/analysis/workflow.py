import json
from typing import TextIO
from io import IOBase
from graphviz import Digraph

class Workflow:
	def __init__(self, workflow:dict[str,str]|TextIO = None):
		
		self.__dict__ = {
		  "workflow": {
			"nodes": {
			  "start": {
				"type": "activity",
				"name": "Malware sample",
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
				  "IceSword"
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
				  "pe_explorer",
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
				  "reverse_engineering_compiler",
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
				  "import_reconstruction",
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
				"tools": []
			  },
			  "bhvr_1": {
				"type": "activity",
				"name": "Run malware for 10 minutes",
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
				"tools": []
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
				  "process_monitor",
				  "process_explorer",
				  "memoryze",
				  "systracer",
				  "process_hacker",
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
				  "malcode_analyst_pack",
				  "netcat",
				  "honeyd",
				  "capturebot",
				  "process_explorer",
				  "systracer",
				  "process_monitor",
				  "apatedns",
				  "sniff_hit",
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
			  "regex": "[Ii]\\s{0,1}[Cc]\\s{0,1}[Ee]\\s{0,1}[Ss]\\s{0,1}[Ww]\\s{0,1}[Oo]\\s{0,1}[Rr]\\s{0,1}[Dd]\\s{0,1}"
			},
			"pestudio": {
			  "regex": "[Pp]\\s{0,1}[Ee]\\s{0,1}[Ss]\\s{0,1}[Tt]\\s{0,1}[Uu]\\s{0,1}[Dd]\\s{0,1}[Ii]\\s{0,1}[Oo]\\s{0,1}"
			},
			"ssdeep": {
			  "regex": "[Ss]\\s{0,1}[Ss]\\s{0,1}[Dd]\\s{0,1}[Ee]\\s{0,1}[Ee]\\s{0,1}[Pp]\\s{0,1}"
			},
			"idapro": {
			  "regex": "[Ii]\\s{0,1}[Dd]\\s{0,1}[Aa]"
			},
			"bintext": {
			  "regex": "[Bb]\\s{0,1}[Ii]\\s{0,1}[Nn]\\s{0,1}[Tt]\\s{0,1}[Ee]\\s{0,1}[Xx]\\s{0,1}[Tt]\\s{0,1}"
			},
			"pebrowse": {
			  "regex": "[Pp]\\s{0,1}[Ee]\\s{0,1}[Bb]\\s{0,1}[Rr]\\s{0,1}[Oo]\\s{0,1}[Ww]\\s{0,1}[Ss]\\s{0,1}[Ee]\\s{0,1}"
			},
			"fileinsight": {
			  "regex": "[Ff]\\s{0,1}[Ii]\\s{0,1}[Ll]\\s{0,1}[Ee]\\s{0,1}[Ii]\\s{0,1}[Nn]\\s{0,1}[Ss]\\s{0,1}[Ii]\\s{0,1}[Gg]\\s{0,1}[Hh]\\s{0,1}[Tt]\\s{0,1}"
			},
			"peid": {
			  "regex": "[Pp]\\s{0,1}[Ee]\\s{0,1}[Ii]\\s{0,1}[Dd]\\s{0,1}"
			},
			"die": {
			  "regex": "[Dd]\\s{0,1}[Ii]\\s{0,1}[Ee]\\s{0,1}"
			},
			"binwalk": {
			  "regex": "[Bb]\\s{0,1}[Ii]\\s{0,1}[Nn]\\s{0,1}[Ww]\\s{0,1}[Aa]\\s{0,1}[Ll]\\s{0,1}[Kk]\\s{0,1}"
			},
			"yara": {
			  "regex": "[Yy]\\s{0,1}[Aa]\\s{0,1}[Rr]\\s{0,1}[Aa]\\s{0,1}"
			},
			"winhex": {
			  "regex": "[Ww]\\s{0,1}[Ii]\\s{0,1}[Nn]\\s{0,1}[Hh]\\s{0,1}[Ee]\\s{0,1}[Xx]\\s{0,1}"
			},
			"pe_explorer": {
			  "regex": "[Pp]\\s{0,1}[Ee]\\s{0,1}[__]\\s{0,1}[Ee]\\s{0,1}[Xx]\\s{0,1}[Pp]\\s{0,1}[Ll]\\s{0,1}[Oo]\\s{0,1}[Rr]\\s{0,1}[Ee]\\s{0,1}[Rr]\\s{0,1}"
			},
			"procdump32": {
			  "regex": "[Pp]\\s{0,1}[Rr]\\s{0,1}[Oo]\\s{0,1}[Cc]\\s{0,1}[Dd]\\s{0,1}[Uu]\\s{0,1}[Mm]\\s{0,1}[Pp]\\s{0,1}[33]\\s{0,1}[22]\\s{0,1}"
			},
			"scylla": {
			  "regex": "[Ss]\\s{0,1}[Cc]\\s{0,1}[Yy]\\s{0,1}[Ll]\\s{0,1}[Ll]\\s{0,1}[Aa]\\s{0,1}"
			},
			"ghidra": {
			  "regex": "[Gg]\\s{0,1}[Hh]\\s{0,1}[Ii]\\s{0,1}[Dd]\\s{0,1}[Rr]\\s{0,1}[Aa]\\s{0,1}"
			},
			"reverse_engineering_compiler": {
			  "regex": "[Rr]\\s{0,1}[Ee]\\s{0,1}[Vv]\\s{0,1}[Ee]\\s{0,1}[Rr]\\s{0,1}[Ss]\\s{0,1}[Ee]\\s{0,1}[__]\\s{0,1}[Ee]\\s{0,1}[Nn]\\s{0,1}[Gg]\\s{0,1}[Ii]\\s{0,1}[Nn]\\s{0,1}[Ee]\\s{0,1}[Ee]\\s{0,1}[Rr]\\s{0,1}[Ii]\\s{0,1}[Nn]\\s{0,1}[Gg]\\s{0,1}[__]\\s{0,1}[Cc]\\s{0,1}[Oo]\\s{0,1}[Mm]\\s{0,1}[Pp]\\s{0,1}[Ii]\\s{0,1}[Ll]\\s{0,1}[Ee]\\s{0,1}[Rr]\\s{0,1}"
			},
			"ollydbg": {
			  "regex": "[Oo]\\s{0,1}[Ll]\\s{0,1}[Ll]\\s{0,1}[Yy]\\s{0,1}[Dd]\\s{0,1}[Bb]\\s{0,1}[Gg]\\s{0,1}"
			},
			"import_reconstruction": {
			  "regex": "[Ii]\\s{0,1}[Mm]\\s{0,1}[Pp]\\s{0,1}[Oo]\\s{0,1}[Rr]\\s{0,1}[Tt]\\s{0,1}[__]\\s{0,1}[Rr]\\s{0,1}[Ee]\\s{0,1}[Cc]\\s{0,1}[Oo]\\s{0,1}[Nn]\\s{0,1}[Ss]\\s{0,1}[Tt]\\s{0,1}[Rr]\\s{0,1}[Uu]\\s{0,1}[Cc]\\s{0,1}[Tt]\\s{0,1}[Ii]\\s{0,1}[Oo]\\s{0,1}[Nn]\\s{0,1}"
			},
			"floatnotmyfault": {
			  "regex": "[Ff]\\s{0,1}[Ll]\\s{0,1}[Oo]\\s{0,1}[Aa]\\s{0,1}[Tt]\\s{0,1}[Nn]\\s{0,1}[Oo]\\s{0,1}[Tt]\\s{0,1}[Mm]\\s{0,1}[Yy]\\s{0,1}[Ff]\\s{0,1}[Aa]\\s{0,1}[Uu]\\s{0,1}[Ll]\\s{0,1}[Tt]\\s{0,1}"
			},
			"process_monitor": {
			  "regex": "[Pp]\\s{0,1}[Rr]\\s{0,1}[Oo]\\s{0,1}[Cc]\\s{0,1}[Ee]\\s{0,1}[Ss]\\s{0,1}[Ss]\\s{0,1}[__]\\s{0,1}[Mm]\\s{0,1}[Oo]\\s{0,1}[Nn]\\s{0,1}[Ii]\\s{0,1}[Tt]\\s{0,1}[Oo]\\s{0,1}[Rr]\\s{0,1}"
			},
			"process_explorer": {
			  "regex": "[Pp]\\s{0,1}[Rr]\\s{0,1}[Oo]\\s{0,1}[Cc]\\s{0,1}[Ee]\\s{0,1}[Ss]\\s{0,1}[Ss]\\s{0,1}[__]\\s{0,1}[Ee]\\s{0,1}[Xx]\\s{0,1}[Pp]\\s{0,1}[Ll]\\s{0,1}[Oo]\\s{0,1}[Rr]\\s{0,1}[Ee]\\s{0,1}[Rr]\\s{0,1}"
			},
			"memoryze": {
			  "regex": "[Mm]\\s{0,1}[Ee]\\s{0,1}[Mm]\\s{0,1}[Oo]\\s{0,1}[Rr]\\s{0,1}[Yy]\\s{0,1}[Zz]\\s{0,1}[Ee]\\s{0,1}"
			},
			"systracer": {
			  "regex": "[Ss]\\s{0,1}[Yy]\\s{0,1}[Ss]\\s{0,1}[Tt]\\s{0,1}[Rr]\\s{0,1}[Aa]\\s{0,1}[Cc]\\s{0,1}[Ee]\\s{0,1}[Rr]\\s{0,1}"
			},
			"process_hacker": {
			  "regex": "[Pp]\\s{0,1}[Rr]\\s{0,1}[Oo]\\s{0,1}[Cc]\\s{0,1}[Ee]\\s{0,1}[Ss]\\s{0,1}[Ss]\\s{0,1}[__]\\s{0,1}[Hh]\\s{0,1}[Aa]\\s{0,1}[Cc]\\s{0,1}[Kk]\\s{0,1}[Ee]\\s{0,1}[Rr]\\s{0,1}"
			},
			"autoruns": {
			  "regex": "[Aa]\\s{0,1}[Uu]\\s{0,1}[Tt]\\s{0,1}[Oo]\\s{0,1}[Rr]\\s{0,1}[Uu]\\s{0,1}[Nn]\\s{0,1}[Ss]\\s{0,1}"
			},
			"spymetool": {
			  "regex": "[Ss]\\s{0,1}[Pp]\\s{0,1}[Yy]\\s{0,1}[Mm]\\s{0,1}[Ee]\\s{0,1}[Tt]\\s{0,1}[Oo]\\s{0,1}[Oo]\\s{0,1}[Ll]\\s{0,1}"
			},
			"regshot": {
			  "regex": "[Rr]\\s{0,1}[Ee]\\s{0,1}[Gg]\\s{0,1}[Ss]\\s{0,1}[Hh]\\s{0,1}[Oo]\\s{0,1}[Tt]\\s{0,1}"
			},
			"psfile": {
			  "regex": "[Pp]\\s{0,1}[Ss]\\s{0,1}[Ff]\\s{0,1}[Ii]\\s{0,1}[Ll]\\s{0,1}[Ee]\\s{0,1}"
			},
			"wireshark": {
			  "regex": "[Ww]\\s{0,1}[Ii]\\s{0,1}[Rr]\\s{0,1}[Ee]\\s{0,1}[Ss]\\s{0,1}[Hh]\\s{0,1}[Aa]\\s{0,1}[Rr]\\s{0,1}[Kk]\\s{0,1}"
			},
			"snort": {
			  "regex": "[Ss]\\s{0,1}[Nn]\\s{0,1}[Oo]\\s{0,1}[Rr]\\s{0,1}[Tt]\\s{0,1}"
			},
			"dirwatch": {
			  "regex": "[Dd]\\s{0,1}[Ii]\\s{0,1}[Rr]\\s{0,1}[Ww]\\s{0,1}[Aa]\\s{0,1}[Tt]\\s{0,1}[Cc]\\s{0,1}[Hh]\\s{0,1}"
			},
			"fakedns": {
			  "regex": "[Ff]\\s{0,1}[Aa]\\s{0,1}[Kk]\\s{0,1}[Ee]\\s{0,1}[Dd]\\s{0,1}[Nn]\\s{0,1}[Ss]\\s{0,1}"
			},
			"finddll": {
			  "regex": "[Ff]\\s{0,1}[Ii]\\s{0,1}[Nn]\\s{0,1}[Dd]\\s{0,1}[Dd]\\s{0,1}[Ll]\\s{0,1}[Ll]\\s{0,1}"
			},
			"mailpot": {
			  "regex": "[Mm]\\s{0,1}[Aa]\\s{0,1}[Ii]\\s{0,1}[Ll]\\s{0,1}[Pp]\\s{0,1}[Oo]\\s{0,1}[Tt]\\s{0,1}"
			},
			"sniff_hit": {
			  "regex": "[Ss]\\s{0,1}[Nn]\\s{0,1}[Ii]\\s{0,1}[Ff]\\s{0,1}[Ff]\\s{0,1}[__]\\s{0,1}[Hh]\\s{0,1}[Ii]\\s{0,1}[Tt]\\s{0,1}"
			},
			"icddumpfix": {
			  "regex": "[Ii]\\s{0,1}[Cc]\\s{0,1}[Dd]\\s{0,1}[Dd]\\s{0,1}[Uu]\\s{0,1}[Mm]\\s{0,1}[Pp]\\s{0,1}[Ff]\\s{0,1}[Ii]\\s{0,1}[Xx]\\s{0,1}"
			},
			"gdiproc": {
			  "regex": "[Gg]\\s{0,1}[Dd]\\s{0,1}[Ii]\\s{0,1}[Pp]\\s{0,1}[Rr]\\s{0,1}[Oo]\\s{0,1}[Cc]\\s{0,1}"
			},
			"loadlib": {
			  "regex": "[Ll]\\s{0,1}[Oo]\\s{0,1}[Aa]\\s{0,1}[Dd]\\s{0,1}[Ll]\\s{0,1}[Ii]\\s{0,1}[Bb]\\s{0,1}"
			},
			"netcat": {
			  "regex": "[Nn]\\s{0,1}[Ee]\\s{0,1}[Tt]\\s{0,1}[Cc]\\s{0,1}[Aa]\\s{0,1}[Tt]\\s{0,1}"
			},
			"honeyd": {
			  "regex": "[Hh]\\s{0,1}[Oo]\\s{0,1}[Nn]\\s{0,1}[Ee]\\s{0,1}[Yy]\\s{0,1}[Dd]\\s{0,1}"
			},
			"capturebot": {
			  "regex": "[Cc]\\s{0,1}[Aa]\\s{0,1}[Pp]\\s{0,1}[Tt]\\s{0,1}[Uu]\\s{0,1}[Rr]\\s{0,1}[Ee]\\s{0,1}[Bb]\\s{0,1}[Oo]\\s{0,1}[Tt]\\s{0,1}"
			},
			"apatedns": {
			  "regex": "[Aa]\\s{0,1}[Pp]\\s{0,1}[Aa]\\s{0,1}[Tt]\\s{0,1}[Ee]\\s{0,1}[Dd]\\s{0,1}[Nn]\\s{0,1}[Ss]\\s{0,1}"
			}
		  }
		}

		if isinstance(workflow, IOBase):
			with open(workflow, 'r') as wf:
				self.__dict__ = json.load(wf)
		elif isinstance(workflow, dict):
			self.__dict__ = workflow.copy()
		
		self._check_structure()
	
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
	  