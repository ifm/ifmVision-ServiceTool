import multiprocessing
import os
import platform
import re
import socket
import threading

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QTreeWidgetItem,
)

from source.discovery import DiscoveryClient
from source.rpc import RPC


class SensorSelector(object):

    def __init__(self, tab):
        self.tab = tab

        self.tab.sensorTreeWidget.itemDoubleClicked.connect(self.modify)
        self.tab.sensorTreeWidget.clicked.connect(self.finish_modify)

    def add(self):
        threading.Thread(target=self._add_sensor, daemon=True).start()

    def delete(self):
        threading.Thread(target=self._delete_sensor, daemon=True).start()

    def sync(self):
        threading.Thread(target=self.sync_sensors, daemon=True).start()

    def discovery(self):
        threading.Thread(target=self.discover_sensors, daemon=True).start()

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

    def finish_modify(self):
        threading.Thread(target=self._finish_modify_tree_widget_item, daemon=True).start()

    def modify(self):
        threading.Thread(target=self._modify_tree_widget_item, daemon=True).start()

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
            new_item.setText(5, old_item.text(5))

        _new_item = self.tab.sensorTreeWidget.selectedItems()[0]
        _old_item = self.tab.sensorTreeWidget.selectedItems()[0].clone()
        verifyEdit(old_item=_old_item, new_item=_new_item)

        self._sync_flag = False

    def _modify_tree_widget_item(self):

        def checkEdit(item, column):
            tmp = item.flags()
            if column == 1:
                item.setFlags(tmp | Qt.ItemIsEditable)
            elif tmp & Qt.ItemIsEditable:
                item.setFlags(tmp ^ Qt.ItemIsEditable)

        checkEdit(item=self.tab.sensorTreeWidget.selectedItems()[0], column=1)

    def _add_sensor(self, ip_address="192.168.0.1"):
        item = QTreeWidgetItem(self.tab.sensorTreeWidget)
        item.setText(0, str(len(self.sensor_entries)))
        item.setText(1, ip_address)
        item.setText(2, 'n.a.')
        item.setText(3, 'n.a.')
        item.setText(4, 'n.a.')
        item.setText(5, 'n.a.')
        self.tab.sensorTreeWidget.addTopLevelItem(item)
        self._sync_flag = False

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

    def available_sensors_in_list(self):
        _widget = QTreeWidgetItem(self.tab.sensorTreeWidget)
        cnt = _widget.childCount()
        for i in range(cnt):
            item = _widget.child(i)
            text = item.text(0)
            print(text)
        return 0

    @property
    def sensor_entries(self):
        """Returns all QTreeWidgetItems in the given QTreeWidget."""
        return self.get_tree_nodes(self.tab.sensorTreeWidget)

    def _delete_sensor(self):
        root = self.tab.sensorTreeWidget.invisibleRootItem()
        for item in self.tab.sensorTreeWidget.selectedItems():
            (item.parent() or root).removeChild(item)
            self._resync_sensors_ids()

    def _resync_sensors_ids(self):
        _sensor_entries = self.sensor_entries
        for i in range(len(_sensor_entries)):
            _sensor_entries[i].setText(0, str(i + 1))

    @staticmethod
    def get_os() -> str:
        """
        Get the current operating system

        :return: (str) operating system
        """
        print("platform.system() = %s" % (platform.system()))
        return platform.system()

    def get_local_network_interfaces(self) -> list:
        """
        Get all local network interfaces as a list

        :return: (list) local network interfaces
        """
        local_os = self.get_os()
        if local_os == "Linux":
            interfaces = os.listdir('/sys/class/net/')
            interfaces = [str.encode(inf) for inf in interfaces]
        elif local_os == "Windows":
            interfaces = socket.getaddrinfo(host=socket.gethostname(),
                                            port=None,
                                            family=socket.AF_INET)
            interfaces = [ip[-1][0] for ip in interfaces]
        else:
            raise EnvironmentError("IFM device discovery not implemented and tested yet for OS {}".format(local_os))

        print("Following interfaces found for OS {}:\n{}".format(local_os, interfaces))
        return interfaces

    def discover_sensors(self):
        # Disable all buttons
        self.tab.disable_buttons()

        # detect local network adapters
        my_network_interfaces = self.get_local_network_interfaces()

        interface_devices = {}
        if my_network_interfaces:
            # iterate over all available network adapters and detect IFM devices
            for inf_id, my_inf in enumerate(my_network_interfaces):
                discovery_client = DiscoveryClient(interface=my_inf, loggerBox=self.tab.logger_box)
                devices = discovery_client.detect_devices()
                interface_devices[inf_id] = devices

        ifm_device_ips = []
        for _, interface_item in interface_devices.items():
            if interface_item["devices"]:
                for _, device in interface_item["devices"].items():
                    ifm_device_ips.append(device["device_ip"])

        if ifm_device_ips:
            self.tab.sensorTreeWidget.clear()

            for ip in ifm_device_ips:
                self._add_sensor(ip_address=ip)

        self.sync_sensors(clearLog=False)

        self.tab.enable_buttons()
        # self.save_new_recent_xml_content()
        self.tab.sync_flag = True

        self.tab.logger_box.add_log_entry("Finished discovery!")

        self.tab.recent_xml_writer.save_new_recent_xml_content(self.sensor_entries)

    def sync_sensors(self, clearLog=True):
        # Disable all buttons
        self.tab.disable_buttons()
        # Clear log textbox and write first line
        if clearLog:
            self.tab.logger_box.clear_all_entries()
        _sensor_entries = self.sensor_entries
        # Clear colors for sensors availability
        for i in range(len(_sensor_entries)):
            _sensor_entries[i].setBackground(2, QColor("white"))
        # Start sync process for each sensor
        for i in range(len(_sensor_entries)):
            sensor_ip = _sensor_entries[i].text(1)
            self.tab.logger_box.add_log_entry("Checking availability for sensor with IP {ip} ...".format(ip=sensor_ip))
            try:
                rpc_session = RPC(address=sensor_ip)
                ping_response = rpc_session.call_doPing_function()
                if ping_response == "up":
                    _sensor_entries[i].setBackground(2, QColor("green"))
                    _sensor_entries[i].setText(2, ping_response)
                    _sensor_entries[i].setText(3, rpc_session.call_getParameter_function(param="Name"))
                    _sensor_entries[i].setText(4, rpc_session.call_getParameter_function(param="ArticleNumber"))
                    _sensor_entries[i].setText(5, rpc_session.call_getFWVersion_function())
                    self.tab.logger_box.add_log_entry("Sensor with IP {ip} is alive.".format(ip=sensor_ip))
                else:
                    _sensor_entries[i].setBackground(2, QColor("red"))
                    _sensor_entries[i].setText(2, ping_response)
                    _sensor_entries[i].setText(3, "n.a.")
                    _sensor_entries[i].setText(4, "n.a.")
                    _sensor_entries[i].setText(5, "n.a.")
                    self.tab.logger_box.add_log_entry("Sensor with IP {ip} is not reachable.".format(ip=sensor_ip))
            except ConnectionAbortedError:
                self.tab.logger_box.add_log_entry("Sensor with IP {ip} not in Operating Mode 0. "
                                                  "Reboot sensor or close ifm Vision Assistant."
                                                  .format(ip=sensor_ip))
                _sensor_entries[i].setBackground(2, QColor("yellow"))
                _sensor_entries[i].setText(2, "wrong mode")
                _sensor_entries[i].setText(3, "n.a.")
                _sensor_entries[i].setText(4, "n.a.")
                _sensor_entries[i].setText(5, "n.a.")
                self.tab.enable_buttons()
            except multiprocessing.context.TimeoutError:
                self.tab.logger_box.add_log_entry("Timeout for sensor with IP {ip}. "
                                                  "Please check the network connection or IP address."
                                                  .format(ip=sensor_ip))
                _sensor_entries[i].setBackground(2, QColor("red"))
                _sensor_entries[i].setText(2, "timeout")
                _sensor_entries[i].setText(3, "n.a.")
                _sensor_entries[i].setText(4, "n.a.")
                _sensor_entries[i].setText(5, "n.a.")
                self.tab.enable_buttons()
            except ConnectionRefusedError:
                _sensor_entries[i].setBackground(2, QColor("red"))
                _sensor_entries[i].setText(2, "error (socket)")
                _sensor_entries[i].setText(3, "n.a.")
                _sensor_entries[i].setText(4, "n.a.")
                _sensor_entries[i].setText(5, "n.a.")
                self.tab.logger_box.add_log_entry(
                    "Sensor with IP {ip} is not reachable. Check if a socket connection is already "
                    "active and try reaching the sensor with the ifmVisionAssistant."
                    .format(ip=sensor_ip))

            _sensor_entries[i].setText(0, str(i + 1))

        self.tab.enable_buttons()
        self.tab.sync_flag = True

        self.tab.logger_box.add_log_entry("Finished sync process of sensors in list!")

        self.tab.recent_xml_writer.save_new_recent_xml_content(self.sensor_entries)
