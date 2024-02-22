import os
import sys

from PySide6 import QtWidgets
from form.form import Ui_ServiceTool
from tabs.tabFwUpdater import FwUpdaterTab
from tabs.tabLogExtractor import LogExtractorTab

UPDATER_XML_FILE = os.path.join(os.getenv('APPDATA'), "ifm electronic", "ifmVisionServiceTool", "updater", "recent.xml")
EXTRACTOR_XML_FILE = os.path.join(os.getenv('APPDATA'), "ifm electronic", "ifmVisionServiceTool", "extractor",
                                  "recent.xml")


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.ui = Ui_ServiceTool()
        self.ui.setupUi(self)

        self.logExtractorTab = LogExtractorTab(window=self.ui, recent_xml_file=EXTRACTOR_XML_FILE)
        self.FwUpdaterTab = FwUpdaterTab(window=self.ui, recent_xml_file=UPDATER_XML_FILE)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    widget = Window()
    widget.show()
    sys.exit(app.exec())
