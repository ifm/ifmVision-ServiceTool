from ui_form import Ui_Dialog
from rpc import RPC
from PySide6 import QtWidgets
from PySide6.QtWidgets import QTreeWidgetItem, QFileDialog
from pathlib import Path
from os.path import normpath
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from xml.dom import minidom
from timeit import default_timer as timer
from datetime import timedelta, datetime
import argparse
import sys
import time
import threading
import re
import os

RECENT_XML_FILE = os.path.join(os.getenv('APPDATA'), "ifm electronic", "ifmVisionLogTracesExtractor", "recent.xml")


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.add_button = self.ui.pushButton_2  # Add button
        self.del_button = self.ui.pushButton_3  # Delete button
        self.dir_button = self.ui.toolButton  # Select directory button
        self.syn_button = self.ui.pushButton_4  # Sync button
        self.ext_button = self.ui.pushButton  # Extract button

        self.ext_button.clicked.connect(self.start)
        self.add_button.clicked.connect(self.add)
        self.del_button.clicked.connect(self.delete)
        self.syn_button.clicked.connect(self.sync)
        self.dir_button.clicked.connect(self.directory)

        self.ui.treeWidget.itemDoubleClicked.connect(self.modify)
        self.ui.treeWidget.clicked.connect(self.finish_modify)

        self.ui.lineEdit.setText(str(Path.home() / "Downloads"))
        self._check_or_make_roaming_folder()
        self._init_sensors_from_xml()

        self._sync_flag = False
        self._total_bar_steps = 0
        self._timer_start = None

    def closeEvent(self, event):
        root = minidom.Document()

        xml = root.createElement('root')
        root.appendChild(xml)

        for i in range(len(self.sensor_entries)):
            productChild = root.createElement('sensor')
            productChild.setAttribute('id', self.sensor_entries[i].text(0))
            productChild.setAttribute('ip_address', self.sensor_entries[i].text(1))
            productChild.setAttribute('available', self.sensor_entries[i].text(2))
            productChild.setAttribute('name', self.sensor_entries[i].text(3))
            productChild.setAttribute('model', self.sensor_entries[i].text(4))
            xml.appendChild(productChild)

        xml_str = root.toprettyxml(indent="\t")

        with open(RECENT_XML_FILE, "w") as f:
            f.write(xml_str)
        f.close()

        can_exit = True
        if can_exit:
            event.accept()  # let the window close
        else:
            event.ignore()

    def _check_or_make_roaming_folder(self):
        try:
            f = open(RECENT_XML_FILE)
            f.close()
        except (FileNotFoundError, IOError):
            self._add_log_entry(msg="File or directory missing for path: " + RECENT_XML_FILE)
            dir_path = os.path.dirname(os.path.realpath(RECENT_XML_FILE))
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                self._add_log_entry(msg="Created directory " + str(dir_path))

    def _init_sensors_from_xml(self):
        try:
            doc = minidom.parse(RECENT_XML_FILE)
            sensors = doc.getElementsByTagName('sensor')

            # Clear all items in tree widget
            self.ui.treeWidget.clear()

            for s in sensors:
                item = QTreeWidgetItem(self.ui.treeWidget)
                item.setText(0, s.attributes['id'].value)
                item.setText(1, s.attributes['ip_address'].value)
                item.setText(2, s.attributes['available'].value)
                item.setText(3, s.attributes['name'].value)
                item.setText(4, s.attributes['model'].value)
                self.ui.treeWidget.addTopLevelItem(item)
        except IOError:
            self._add_log_entry(msg="Unable to read file: " + RECENT_XML_FILE)

    def finish_modify(self):
        threading.Thread(target=self._finish_modify_tree_widget_item, daemon=True).start()

    def modify(self):
        threading.Thread(target=self._modify_tree_widget_item, daemon=True).start()

    def start(self):
        threading.Thread(target=self._extract_trace_logs, daemon=True).start()

    def add(self):
        threading.Thread(target=self._add_sensor, daemon=True).start()

    def delete(self):
        threading.Thread(target=self._delete_sensor, daemon=True).start()

    def sync(self):
        threading.Thread(target=self._sync_sensors, daemon=True).start()

    def _finish_modify_tree_widget_item(self):

        def verifyEdit(old_item, new_item):
            ip_valid_flag = [0 <= int(x) < 256 for x in
                             re.split('\.', re.match(r'^\d+\.\d+\.\d+\.\d+$',
                                                     new_item.text(1)).group(0))].count(True) == 4
            new_item.setText(0, old_item.text(0))
            if not ip_valid_flag:
                new_item.setText(1, old_item.text(1))
            new_item.setText(2, old_item.text(2))
            new_item.setText(3, old_item.text(3))
            new_item.setText(4, old_item.text(4))

        verifyEdit(old_item=self.ui.treeWidget.selectedItems()[0].clone(),
                   new_item=self.ui.treeWidget.selectedItems()[0])

        self._sync_flag = False

    def _modify_tree_widget_item(self):

        def checkEdit(item, column):
            tmp = item.flags()
            if column == 1:
                item.setFlags(tmp | Qt.ItemIsEditable)
            elif tmp & Qt.ItemIsEditable:
                item.setFlags(tmp ^ Qt.ItemIsEditable)

        checkEdit(item=self.ui.treeWidget.selectedItems()[0], column=1)

    def _add_sensor(self):
        item = QTreeWidgetItem(self.ui.treeWidget)
        item.setText(0, str(len(self.sensor_entries)))
        item.setText(1, '192.168.0.1')
        item.setText(2, 'n.a.')
        item.setText(3, 'n.a.')
        item.setText(4, 'n.a.')
        self.ui.treeWidget.addTopLevelItem(item)
        self._sync_flag = False

    def _delete_sensor(self):
        root = self.ui.treeWidget.invisibleRootItem()
        for item in self.ui.treeWidget.selectedItems():
            (item.parent() or root).removeChild(item)
            self._resync_sensors_ids()

    def _resync_sensors_ids(self):
        _sensor_entries = self.sensor_entries
        for i in range(len(_sensor_entries)):
            _sensor_entries[i].setText(0, str(i + 1))

    def _sync_sensors(self):
        # Disable all buttons
        self.disable_buttons()
        # Clear log textbox and write first line
        self.ui.listWidget.clear()
        _sensor_entries = self.sensor_entries
        # Clear colors for sensors availability
        for i in range(len(_sensor_entries)):
            _sensor_entries[i].setBackground(2, QColor("white"))
        # Start sync process for each sensor
        for i in range(len(_sensor_entries)):
            sensor_ip = _sensor_entries[i].text(1)
            self.ui.listWidget.addItem("Checking availability for sensor with IP {ip} ...".format(ip=sensor_ip))
            rpc_session = RPC(address=sensor_ip)
            _sensor_entries[i].setText(0, str(i + 1))
            ping_response = rpc_session.call_doPing_function()
            if ping_response == "up":
                _sensor_entries[i].setBackground(2, QColor("green"))
                _sensor_entries[i].setText(2, ping_response)
                _sensor_entries[i].setText(3, rpc_session.call_getParameter_function(param="Name"))
                _sensor_entries[i].setText(4, rpc_session.call_getParameter_function(param="ArticleNumber"))
                self.ui.listWidget.addItem("Sensor with IP {ip} is alive.".format(ip=sensor_ip))
            else:
                _sensor_entries[i].setBackground(2, QColor("red"))
                _sensor_entries[i].setText(2, ping_response)
                _sensor_entries[i].setText(3, "n.a.")
                _sensor_entries[i].setText(4, "n.a.")
                self.ui.listWidget.addItem("Sensor with IP {ip} is not reachable.".format(ip=sensor_ip))
        self.enable_buttons()
        self._sync_flag = True

    def directory(self):
        QFileDialog().setDirectory(self.ui.lineEdit.text())
        folder = str(QFileDialog().getExistingDirectory(None, "Select directory"))
        folder = str(Path(normpath(str(folder))))
        self.ui.lineEdit.setText(folder)

    def disable_buttons(self):
        """Disables all buttons on GUI"""
        self.add_button.setEnabled(False)
        self.del_button.setEnabled(False)
        self.syn_button.setEnabled(False)
        self.dir_button.setEnabled(False)
        self.ext_button.setEnabled(False)

    def enable_buttons(self):
        """Enables all buttons on GUI"""
        self.add_button.setEnabled(True)
        self.del_button.setEnabled(True)
        self.syn_button.setEnabled(True)
        self.dir_button.setEnabled(True)
        self.ext_button.setEnabled(True)

    @property
    def available_sensors(self) -> list:
        """Returns all available sensors with content as a list."""
        _sensor_entries = self.sensor_entries
        result = []
        for i in range(len(_sensor_entries)):
            if _sensor_entries[i].text(2) == "up":
                result.append([_sensor_entries[i].text(0), _sensor_entries[i].text(1),
                               _sensor_entries[i].text(2), _sensor_entries[i].text(3),
                               _sensor_entries[i].text(4)])
        return result

    @property
    def sensor_entries(self):
        """Returns all QTreeWidgetItems in the given QTreeWidget."""
        return self.get_tree_nodes(self.ui.treeWidget)

    def available_sensors_in_list(self):
        _widget = QTreeWidgetItem(self.ui.treeWidget)
        cnt = _widget.childCount()
        for i in range(cnt):
            item = _widget.child(i)
            text = item.text(0)
            print(text)
        return 0

    def get_subtree_nodes(self, tree_widget_item):
        """Returns all QTreeWidgetItems in the subtree rooted at the given node."""
        nodes = []
        nodes.append(tree_widget_item)
        for i in range(tree_widget_item.childCount()):
            nodes.extend(self.get_subtree_nodes(tree_widget_item.child(i)))
        return nodes

    def get_tree_nodes(self, tree_widget):
        """Returns all QTreeWidgetItems in the given QTreeWidget."""
        all_items = []
        for i in range(tree_widget.topLevelItemCount()):
            top_item = tree_widget.topLevelItem(i)
            all_items.extend(self.get_subtree_nodes(top_item))
        return all_items

    @staticmethod
    def progress_bar(count, total, suffix=''):
        """Returns a progress bar as string."""
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '#' * filled_len + ' ' * (bar_len - filled_len)
        if suffix:
            return '[%s] %s%s ... %s\r' % (bar, percents, '%', suffix)
        return '[%s] %s%s' % (bar, percents, '%')

    def save_log_to_folder_after_extraction_process(self, save_path):
        itemsTextList = [str(self.ui.listWidget.item(i).text()) for i in range(self.ui.listWidget.count())]

        json_file = os.path.join(save_path, "extract_log.txt")
        with open(json_file, "w") as f:
            f.writelines([f"{line}\n" for line in itemsTextList])
        f.close()

    def _add_log_entry(self, msg, cnt=-1.0):
        if cnt > 1:
            last_item_index = self.ui.listWidget.count()
            self.ui.listWidget.takeItem(last_item_index-1)

        self.ui.listWidget.addItem(str(msg))
        if cnt >= 1:
            _time_elapsed = str(timedelta(seconds=timer() - self._timer_start))
            _bar = self.progress_bar(count=cnt, total=self._total_bar_steps, suffix=_time_elapsed)
            self.ui.listWidget.addItem(_bar)
        time.sleep(0.2)
        self.ui.listWidget.scrollToBottom()
        time.sleep(0.2)

    def _extract_trace_logs(self):
        # Reset timer
        self._timer_start = timer()

        # Check first if sensors are synced than run extraction function again
        if not self._sync_flag:
            self._sync_sensors()

        # Disable all buttons
        self.disable_buttons()

        # Clear log textbox and write first line
        self.ui.listWidget.clear()

        # Number of steps for progress bar
        self._total_bar_steps = len(self.available_sensors) * 9

        # Iterate over all available sensors and extract data
        for i, sensor in enumerate(self.available_sensors):
            sensor_ip = sensor[1]
            rpc_session = RPC(address=sensor_ip, save_folder=self.ui.lineEdit.text())
            sensor_name = rpc_session.call_getParameter_function(param="Name")
            sensor_model = rpc_session.call_getParameter_function(param="ArticleNumber")

            if rpc_session.call_doPing_function() == "up":
                self._add_log_entry("Extraction process started at time: {dt}"
                                    .format(dt=datetime.today().strftime('%Y-%m-%d %H:%M:%S')))

                self._add_log_entry("Starting extraction for sensor {model} - \"{name}\" with IP {ip}."
                                    .format(model=sensor_model, name=sensor_name, ip=sensor_ip))

                self._add_log_entry(rpc_session.start_getAllParameters_download(), 1*(i+1))
                self._add_log_entry(rpc_session.start_getSWVersion_download(), 2*(i+1))
                self._add_log_entry(rpc_session.start_getHWInfo_download(), 3*(i+1))
                self._add_log_entry(rpc_session.start_getApplicationList_download(), 4*(i+1))
                self._add_log_entry(rpc_session.start_getActiveDataConnections_download(), 5*(i+1))
                self._add_log_entry(rpc_session.start_getTraceLogs_download(lines=1000), 6*(i+1))
                self._add_log_entry(rpc_session.start_getDmesgData_download(), 7*(i+1))
                self._add_log_entry(rpc_session.start_serviceReport_download(), 8*(i+1))
                self._add_log_entry(rpc_session.start_deviceAndApplicationSettings_download(), 9*(i+1))

                self._add_log_entry("Finished extraction for sensor {model} - \"{name}\" with IP {ip}."
                                    .format(model=sensor_model, name=sensor_name, ip=sensor_ip))

                self._add_log_entry("Extraction process finished at time: {dt}"
                                    .format(dt=datetime.today().strftime('%Y-%m-%d %H:%M:%S')))

        # Save log in extract folder
        self.save_log_to_folder_after_extraction_process(save_path=self.ui.lineEdit.text())

        # Enable all buttons after finished extraction
        self.enable_buttons()


if __name__ == '__main__':
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Optional app description')

    # Required positional argument
    # '+' == 1 or more.
    # '*' == 0 or more.
    # '?' == 0 or 1.
    parser.add_argument('-i', '--ip', required=True, type=str, nargs='+',
                        help='The IPs of the sensor you want to extract the log traces from.')

    # Optional positional argument
    parser.add_argument('-d', '--destination', required=True, type=str, nargs=1,
                        help='The folder path where you want to store the log traces.')
    try:
        args = vars(parser.parse_args())

        if args['ip'] and args['destination']:
            print(args['ip'])
            print(args['destination'])
    except Exception as e:
        app = QtWidgets.QApplication(sys.argv)
        widget = MyWidget()
        widget.show()
        sys.exit(app.exec())
