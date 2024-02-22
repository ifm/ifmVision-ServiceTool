import os
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QObject
from PySide6.QtUiTools import QUiLoader

from tabs.tabLogExtractor import LogExtractorTab
from tabs.tabFwUpdater import FwUpdaterTab

UPDATER_XML_FILE = os.path.join(os.getenv('APPDATA'), "ifm electronic", "ifmVisionServiceTool", "updater", "recent.xml")
EXTRACTOR_XML_FILE = os.path.join(os.getenv('APPDATA'), "ifm electronic", "ifmVisionServiceTool", "extractor", "recent.xml")


class Window(QObject):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        ui_file_name = "form/form.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QFile.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)

        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        self.logExtractorTab = LogExtractorTab(window=self.window, recent_xml_file=EXTRACTOR_XML_FILE)
        self.FwUpdaterTab = FwUpdaterTab(window=self.window, recent_xml_file=UPDATER_XML_FILE)

        if not self.window:
            print(loader.errorString())
            sys.exit(-1)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    widget = Window()
    widget.window.show()
    sys.exit(app.exec())
