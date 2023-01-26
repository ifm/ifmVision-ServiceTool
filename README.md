# ifmVisionLogTracesTool


## Description

The ifmVisionLogTracesTool is a small stand-alone application for extracting
log traces, service report, application and device backup setting for the
ifm sensor portfolio O2D, O3D and O2I.

## Python Version

For the build process the Python version 3.8.10 was used.

## Pre-Requirements

For this project you first have to install all required packages.
Therefore, navigate to the project folder and enter following command:

```
pip install -r requirements.txt
```

## Build stand-alone application

You can build a stand-alone application with the package PyInstaller.
Install this package with following command from your command shell:

```
pip install pyinstaller
```

Navigate to the project folder and build the application with following command:

```
python -m PyInstaller --onefile --windowed --clean --name LogTracesExtractor.exe main.py
```

You will find the stand-alone application LogTracesExtractor.exe in the dist folder.