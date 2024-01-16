# Introduction

<img src="src/gui/assets/app_icon.png" width=200></img>

VISREX unifies the malware anlaysis methodology making it clearer, shareable and reproducible.

## :ledger: Index

- [About](#beginner-about)
- [Usage](#zap-usage)
  - [Installation](#electric_plug-installation)
  - [Commands](#package-commands)
- [Development](#wrench-development)
  - [Developmen Environment](#nut_and_bolt-development-environment)
  - [File Structure](#file_folder-file-structure)
  - [Build](#hammer-build)  
- [License](#lock-license)

##  :beginner: About
The projects is born from my MSc thesis in Cybersecurity and it is developed as a proof of concept and not as a complete tool, with the objective to be further improved.

## :zap: Usage
The tool has two main views the framework view and the activity log view in which the analyst actions are recorded.
The usage is very simple, the tool aims to unify the process, so just open the tool and perform your analysis maintaining it opened and see what happens.

# :wrench: Development

###  :nut_and_bolt: Development Environment
Clone the project with:
```
git@github.com:edoermini/VISREX.git
```
Open a python virtual environment within the root project directory:
```
virtualenv .venv
```
Activate the environment:

-   In windows
    ```
    .venv\Scripts\activate
    ```

- In Linux
    ```
    source .venv/bin/activate
    ```

Install requirements:
```
pip instasll -r requirements.txt
```

Run the project
```
cd src
python main.py
```


###  :file_folder: File Structure
Add a file structure here with the basic details about files, below is an example.

```
.
├── examples
│   └── mydoom.json
├── LICENSE
├── README.md
├── requirements.txt
└── src
    ├── analysis
    │   ├── analysis_log_entry.py
    │   ├── analysis.py
    │   ├── __init__.py
    │   ├── __pycache__
    │   │   ├── analysis.cpython-311.pyc
    │   │   ├── analysis_log_entry.cpython-311.pyc
    │   │   ├── __init__.cpython-311.pyc
    │   │   └── workflow.cpython-311.pyc
    │   └── workflow.py
    ├── constants.py
    ├── gui
    │   ├── assets
    │   │   ├── app_icon.ico
    │   │   ├── app_icon.png
    │   │   └── loading.gif
    │   ├── dialogs
    │   │   ├── change_paths_dialog.py
    │   │   ├── chose_file_dialog.py
    │   │   ├── combo_box_dialog.py
    │   │   ├── hex_viewer_dialog.py
    │   │   ├── iat_reconstruction_dialog.py
    │   │   ├── __init__.py
    │   │   ├── loading_dialog.py
    │   │   ├── main_dialog.py
    │   │   ├── packer_detection_result_dialog.py
    │   │   ├── __pycache__
    │   │   │   ├── change_paths_dialog.cpython-311.pyc
    │   │   │   ├── chose_file.cpython-311.pyc
    │   │   │   ├── chose_file_dialog.cpython-311.pyc
    │   │   │   ├── combo_box_dialog.cpython-311.pyc
    │   │   │   ├── extract_injected_dialog.cpython-311.pyc
    │   │   │   ├── find_executable_task.cpython-311.pyc
    │   │   │   ├── hex_viewer.cpython-311.pyc
    │   │   │   ├── hex_viewer_dialog.cpython-311.pyc
    │   │   │   ├── iat_reconstruction_dialog.cpython-311.pyc
    │   │   │   ├── __init__.cpython-311.pyc
    │   │   │   ├── loading_dialog.cpython-311.pyc
    │   │   │   ├── main.cpython-311.pyc
    │   │   │   ├── main_dialog.cpython-311.pyc
    │   │   │   ├── new_analysis.cpython-311.pyc
    │   │   │   ├── open.cpython-311.pyc
    │   │   │   ├── open_dialog.cpython-311.pyc
    │   │   │   ├── open_tool.cpython-311.pyc
    │   │   │   ├── open_tool_dialog.cpython-311.pyc
    │   │   │   ├── packer_detection_result_dialog.cpython-311.pyc
    │   │   │   ├── read_process_memory.cpython-311.pyc
    │   │   │   ├── read_process_memory_dialog.cpython-311.pyc
    │   │   │   ├── text_box_dialog.cpython-311.pyc
    │   │   │   └── tools_coverage_dialog.cpython-311.pyc
    │   │   ├── read_process_memory_dialog.py
    │   │   ├── text_box_dialog.py
    │   │   └── tools_coverage_dialog.py
    │   ├── flowcharts
    │   │   ├── graphviz_flowchart_items.py
    │   │   ├── graphviz_flowchart.py
    │   │   ├── __init__.py
    │   │   ├── __pycache__
    │   │   │   ├── flowchart_items.cpython-311.pyc
    │   │   │   ├── graphviz_flowchart.cpython-311.pyc
    │   │   │   ├── graphviz_flowchart_items.cpython-311.pyc
    │   │   │   ├── graphviz_zoomable_flowchart.cpython-311.pyc
    │   │   │   ├── __init__.cpython-311.pyc
    │   │   │   ├── signals.cpython-311.pyc
    │   │   │   └── zoomable_flowchart.cpython-311.pyc
    │   │   └── signals.py
    │   ├── __init__.py
    │   ├── __pycache__
    │   │   └── __init__.cpython-311.pyc
    │   ├── shared
    │   │   ├── __init__.py
    │   │   ├── __pycache__
    │   │   │   ├── __init__.cpython-311.pyc
    │   │   │   └── status_message_queue.cpython-311.pyc
    │   │   └── status_message_queue.py
    │   ├── tables
    │   │   ├── __init__.py
    │   │   ├── __pycache__
    │   │   │   ├── __init__.cpython-311.pyc
    │   │   │   ├── responsive_table.cpython-311.pyc
    │   │   │   └── responsive_table_widget.cpython-311.pyc
    │   │   └── responsive_table.py
    │   ├── updaters
    │   │   ├── activity_updater.py
    │   │   ├── dialog_form_updater.py
    │   │   ├── executables_updater.py
    │   │   ├── __init__.py
    │   │   └── __pycache__
    │   │       ├── activity_updater.cpython-311.pyc
    │   │       ├── dialog_form_updater.cpython-311.pyc
    │   │       ├── executables_updater.cpython-311.pyc
    │   │       ├── __init__.cpython-311.pyc
    │   │       └── updaters.cpython-311.pyc
    │   ├── utils
    │   │   ├── colors.py
    │   │   ├── __init__.py
    │   │   ├── listeners.py
    │   │   └── __pycache__
    │   │       ├── colors.cpython-311.pyc
    │   │       ├── dark_theme.cpython-311.pyc
    │   │       └── __init__.cpython-311.pyc
    │   ├── widgets
    │   │   ├── __init__.py
    │   │   ├── markdown_edit.py
    │   │   └── __pycache__
    │   │       ├── __init__.cpython-311.pyc
    │   │       └── markdown_edit.cpython-311.pyc
    │   └── windows
    │       ├── __init__.py
    │       ├── main_window.py
    │       └── __pycache__
    │           ├── __init__.cpython-311.pyc
    │           ├── main.cpython-311.pyc
    │           ├── main_window.cpython-311.pyc
    │           └── new_analysis.cpython-311.pyc
    ├── integrations
    │   ├── generics
    │   │   ├── __init__.py
    │   │   ├── __pycache__
    │   │   │   ├── __init__.cpython-311.pyc
    │   │   │   └── tool.cpython-311.pyc
    │   │   └── tool.py
    │   ├── importer.py
    │   ├── __init__.py
    │   ├── modules
    │   │   ├── __init__.py
    │   │   ├── processes.py
    │   │   └── __pycache__
    │   │       ├── __init__.cpython-311.pyc
    │   │       └── processes.cpython-311.pyc
    │   ├── __pycache__
    │   │   ├── importer.cpython-311.pyc
    │   │   └── __init__.cpython-311.pyc
    │   ├── scripts
    │   │   └── debug.py
    │   └── tools
    │       ├── bintext.py
    │       ├── __init__.py
    │       ├── peid.py
    │       ├── pestudio.py
    │       ├── __pycache__
    │       │   ├── die.cpython-311.pyc
    │       │   ├── __init__.cpython-311.pyc
    │       │   ├── peid.cpython-311.pyc
    │       │   ├── procmon.cpython-311.pyc
    │       │   └── upx.cpython-311.pyc
    │       ├── scylla.py
    │       └── upx.py
    ├── main.py
    ├── main.spec
    ├── __pycache__
    │   └── constants.cpython-311.pyc
    ├── resources.qrc
    └── resources_rc.py

```

| No | Directory Name | Details 
|----|------------|-------|
| 1  | examples   | contains the analysis of mydoom sample
| 2  | src        | contains the source code of the tool
| 3  | src/gui    | contains the GUI source code
| 4  | src/analysis | contains the source code for handling the analysis
| 5  | src/integrations | contains the source code for automatizing malware analysis tools

###  :hammer: Build
To build the project use:
```
cd src
pyinstaller main.spec
```

##  :lock: License
GNU General Public Licence version 3