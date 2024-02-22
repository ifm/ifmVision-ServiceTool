# ifmVision - ServiceTool


## Description

The ifmVision - ServiceTool is a small stand-alone application for extracting
log traces, service report, application and device backup setting for the
ifm sensor portfolio O2D, O3D and O2I.

It has also been extended to include an updater, which can be used to update the firmware 
of several ifm Vision sensors at the same time.

## Instruction - Log Extractor

1. You can add a new item in the sensor list with the default ip 192.168.0.1 with a single-click on the button.
2. You can delete the last item in the sensor list with a single-click on the button.
3. You can sync and check for the availability of the sensors in the list.
4. You can use the discovery client to detect ifm vision sensors in you network interfaces.
5. You can open the local APPDATA roaming folder where the recent.xml file and other files are stored.
6. You can change the ip address of any sensor by double-clicking on the ip address itself.
7. You can select or create an empty directory in the explorer window, which opens after a single-click on the button.
8. You can extract all log traces, the service report, the application and device settings a single-click on the button.
9. Decide whether to store the logs from the below text field into the APPDATA folder.

![alt text](doc/ui_legend_log_extractor.png?raw=true)

## Instruction - Firmware Updater

1. You can add a new item in the sensor list with the default ip 192.168.0.1 with a single-click on the button.
2. You can delete the last item in the sensor list with a single-click on the button.
3. You can sync and check for the availability of the sensors in the list.
4. You can use the discovery client to detect ifm vision sensors in you network interfaces.
5. You can open the local APPDATA roaming folder where the recent.xml file and other files are stored.
6. You can change the ip address of any sensor by double-clicking on the ip address itself.
7. You can select a firmware file (*.swu) in the explorer window, which opens after a single-click on the button.
8. You can start the update process with a single-click on the button.
9. Decide whether to store the logs from the below text field into the APPDATA folder.
10. Decide whether to backup all device configurations into the APPDATA folder.
11. Decide whether to restore all device configurations from the backups.

![alt text](doc/ui_legend_fw_updater.png?raw=true)

## Python Version

For the build process the Python version 3.8.10 was used.

## Virtual Environment (recommended)

```
python -m venv
```

### In cmd.exe

```
venv\Scripts\activate.bat
```

### In PowerShell

```
venv\Scripts\Activate.ps1
```

## Pre-Requirements (packages)

For this project you first have to install all required packages.
Therefore, navigate to the project folder and enter following command:

```
pip install -r requirements.txt
```

## Debug or develop application

If you want to load the GUI during runtime for debugging or development purpose,
you should use the main_develop.py script or following argument:

```
python main_develop.py
```

## Build stand-alone application (in venv recommended!)

Navigate to the project folder and build the application with following commands:

```
pyside6-uic .\form\form.ui -o .\form\form.py
```

```
python -m PyInstaller --onefile --windowed --name IfmVisionServiceTool main_pyinstaller.py
```

You will find the stand-alone application IfmVisionServiceTool.exe in the dist folder.