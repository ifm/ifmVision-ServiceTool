from xml.dom import minidom
from pathlib import Path
import os

from PySide6.QtWidgets import (
    QTreeWidgetItem,
)


class RecentXMLWriter(object):

    def __init__(self, tab):
        self.tab = tab

        self.init_sensors_from_existing_recent_xml()
        self.check_or_make_recent_xml_file_path()

    def init_sensors_from_existing_recent_xml(self):
        if os.path.isfile(self.tab.recent_xml_file):
            try:
                doc = minidom.parse(self.tab.recent_xml_file)
                sensors = doc.getElementsByTagName('sensor')

                # Clear all items in tree widget
                self.tab.sensorTreeWidget.clear()

                for s in sensors:
                    item = QTreeWidgetItem(self.tab.sensorTreeWidget)
                    item.setText(0, s.attributes['id'].value)
                    item.setText(1, s.attributes['ip_address'].value)
                    item.setText(2, s.attributes['available'].value)
                    item.setText(3, s.attributes['name'].value)
                    item.setText(4, s.attributes['model'].value)
                    item.setText(5, s.attributes['fw_version'].value)
                    self.tab.sensorTreeWidget.addTopLevelItem(item)
            except IOError:
                self.tab.loggerBox.add_log_entry(msg="Unable to read file: " + self.tab.recent_xml_file)
        else:
            self.tab.loggerBox.add_log_entry(msg="File: " + self.tab.recent_xml_file + " does not exist.")

    def init_path_from_existing_recent_xml(self):
        if os.path.isfile(self.tab.recent_xml_file):
            try:
                doc = minidom.parse(self.tab.recent_xml_file)
                path = doc.getElementsByTagName('path')

                if path:
                    self.tab.pathLine.setText(path[0].attributes['path_line'].value)
                else:
                    self.tab.pathLine.setText(str(Path.home() / "Downloads"))
                    _msg = "Path element does not exist in recent.xml file. Setting path to user's download folder."
                    self.tab.logger_box.add_log_entry(msg=_msg)
            except IOError:
                self.tab.logger_box.add_log_entry(msg="Unable to read file: " + self.tab.recent_xml_file)
        else:
            self.tab.pathLine.setText(str(Path.home() / "Downloads"))
            _msg = "File: " + self.tab.recent_xml_file + " does not exist. Setting path to user's download folder."
            self.tab.logger_box.add_log_entry(msg=_msg)
            
    def check_or_make_recent_xml_file_path(self):
        dir_path = os.path.dirname(os.path.realpath(self.tab.recent_xml_file))
        if not os.path.exists(dir_path):
            # directory does not exist
            os.makedirs(dir_path)
            self.tab.logger_box.add_log_entry(msg="Roaming path missing. Created path: " + str(dir_path))

    # def closeEvent(self, event):
    def save_new_recent_xml_content(self, sensor_entries):
        root = minidom.Document()

        xml = root.createElement('root')
        root.appendChild(xml)

        # sensors
        for i in range(len(sensor_entries)):
            productChild = root.createElement('sensor')
            productChild.setAttribute('id', sensor_entries[i].text(0))
            productChild.setAttribute('ip_address', sensor_entries[i].text(1))
            productChild.setAttribute('available', sensor_entries[i].text(2))
            productChild.setAttribute('name', sensor_entries[i].text(3))
            productChild.setAttribute('model', sensor_entries[i].text(4))
            productChild.setAttribute('fw_version', sensor_entries[i].text(5))
            xml.appendChild(productChild)

        # path line
        productChild = root.createElement('path')
        productChild.setAttribute('path_line', self.tab.pathLine.displayText())
        xml.appendChild(productChild)

        xml_str = root.toprettyxml(indent="\t")

        with open(self.tab.recent_xml_file, "w") as f:
            f.write(xml_str)
        f.close()

        return True
