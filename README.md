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
    │   │   ├── read_process_memory_dialog.py
    │   │   ├── text_box_dialog.py
    │   │   └── tools_coverage_dialog.py
    │   ├── flowcharts
    │   │   ├── graphviz_flowchart_items.py
    │   │   ├── graphviz_flowchart.py
    │   │   ├── __init__.py
    │   │   └── signals.py
    │   ├── __init__.py
    │   ├── shared
    │   │   ├── __init__.py
    │   │   └── status_message_queue.py
    │   ├── tables
    │   │   ├── __init__.py
    │   │   └── responsive_table.py
    │   ├── updaters
    │   │   ├── activity_updater.py
    │   │   ├── dialog_form_updater.py
    │   │   ├── executables_updater.py
    │   │   ├── __init__.py
    │   ├── utils
    │   │   ├── colors.py
    │   │   ├── __init__.py
    │   │   ├── listeners.py
    │   ├── widgets
    │   │   ├── __init__.py
    │   │   ├── markdown_edit.py
    │   └── windows
    │       ├── __init__.py
    │       └── main_window.py
    ├── integrations
    │   ├── generics
    │   │   ├── __init__.py
    │   │   └── tool.py
    │   ├── importer.py
    │   ├── __init__.py
    │   ├── modules
    │   │   ├── __init__.py
    │   │   └── processes.py
    │   ├── scripts
    │   │   └── debug.py
    │   └── tools
    │       ├── bintext.py
    │       ├── __init__.py
    │       ├── peid.py
    │       ├── pestudio.py
    │       ├── scylla.py
    │       └── upx.py
    ├── main.py
    ├── main.spec
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
