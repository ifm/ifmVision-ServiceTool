import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    'name-%s%' % 'LogTracesExtractor',
    '--onefile',
    '--windowed',
    '--clean',
    os.path.join('/path/to/your/script/', 'main.py'), """your script and path to the script"""
])