# ifmVisionLogTracesTool


## Description

The ifmVisionLogTracesTool is a small stand-alone application for extracting
log traces, service report, application and device backup setting for the
ifm sensor portfolio O2D, O3D and O2I.

## Instruction

1. You can add a new item in the sensor list with the default ip 192.168.0.1 with a single-click on the button.
2. You can delete the last item in the sensor list with a single-click on the button.
3. You can sync and check for the availability of the sensors in the list.
4. You can change the ip address of any sensor by double-clicking in the ip address itself.
5. You can select or create an empty directory in the explorer window, which opens after a single-click on the button.
6. You can extract all log traces, the service report, the application and device settings a single-click on the button.

![alt text](ui_legend.png?raw=true)

## Python Version

For the build process the Python version 3.8.10 was used.

## Pre-Requirements

For this project you first have to install all required packages.
Therefore, navigate to the project folder and enter following command:

```
pip install -r requirements.txt
```

## Build stand-alone application

Navigate to the project folder and build the application with following command:

```
python -m PyInstaller --onefile --windowed --name LogTracesExtractor main.py
```

You will find the stand-alone application LogTracesExtractor.exe in the dist folder.