import os
import threading
from datetime import datetime
from os.path import normpath
from pathlib import Path
from timeit import default_timer as timer

from PySide6 import QtWidgets
from PySide6.QtWidgets import (
    QFileDialog,
    QMessageBox
)

from source.rpc import RPC
from source.loggerBox import LoggerBoxer
from source.sensorSelector import SensorSelector
from source.recentXmlWriter import RecentXMLWriter


class LogExtractorTab(QtWidgets.QTabWidget):
    def __init__(self, window, recent_xml_file):
        super().__init__()
        self.ui = window
        self.recent_xml_file = recent_xml_file

        # Log box, sensor tree widget and path textbox
        self.logListWidget = self.ui.logListWidget
        self.sensorTreeWidget = self.ui.sensorTreeWidget
        self.pathLine = self.ui.pathLineEdit

        # Init classes
        self.logger_box = LoggerBoxer(self.logListWidget)
        self.recent_xml_writer = RecentXMLWriter(self)
        self.sensor_selector = SensorSelector(self)

        # Run methods from xml writer
        self.recent_xml_writer.check_or_make_recent_xml_file_path()
        self.recent_xml_writer.init_sensors_from_existing_recent_xml()
        self.recent_xml_writer.init_path_from_existing_recent_xml()

        # Buttons
        self.add_button = self.ui.addButton  # Add button
        self.del_button = self.ui.deleteButton  # Delete button
        self.dir_button = self.ui.selectDirButton  # Select directory button
        self.syn_button = self.ui.syncButton  # Sync button
        self.ext_button = self.ui.extractButton  # Extract button
        self.udp_button = self.ui.discoveryButton  # Discovery button
        self.apd_button = self.ui.openAppdataButton  # open Appdata button

        self.ext_button.clicked.connect(self.start)
        self.add_button.clicked.connect(self.sensor_selector.add)
        self.del_button.clicked.connect(self.sensor_selector.delete)
        self.syn_button.clicked.connect(self.sensor_selector.sync)
        self.dir_button.clicked.connect(self.directory)
        self.udp_button.clicked.connect(self.discovery)
        self.apd_button.clicked.connect(self.open_appdata_folder)

        # Checkboxes
        self.log_checkbox = self.ui.logCheckBox

        self.log_checkbox.clicked.connect(self.checkbox_log_clicked)

        self.sync_flag = False

    def checkbox_log_clicked(self):
        if self.log_checkbox.isChecked():
            self.log_checkbox.setChecked(True)
            self.logger_box.add_log_entry("Activated log process of this output into APPDATA folder.")
        else:
            self.log_checkbox.setChecked(False)
            self.logger_box.add_log_entry("WARNING: Deactivated log process of this output into APPDATA folder.")

    @property
    def extractor_appdata_folder(self):
        appdata_path = os.getenv('APPDATA')
        if appdata_path:
            appdata_path = os.path.join(appdata_path, "ifm electronic", "ifmVisionServiceTool", "extractor")
            return appdata_path
        else:
            self.logger_box.add_log_entry("APPDATA path not found.")

    def open_appdata_folder(self):
        if self.extractor_appdata_folder:
            os.system(f'explorer "{self.extractor_appdata_folder}"')
        else:
            self.logger_box.add_log_entry("Folder for extractor in APPDATA not found.")

    def start(self):
        # Message box for asking user if he wants to stop the sensors while extracting the data
        choice = QMessageBox.question(self, 'Extraction Warning!',
                                      "For the extraction purpose, the sensor is taken out of run mode for a "
                                      "short time (approx. 20-60 seconds) and does not provide any results. "
                                      "Are you sure?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if choice == QMessageBox.StandardButton.Yes:
            threading.Thread(target=self._extract_trace_logs, daemon=True).start()
        else:
            pass

    def directory(self):
        QFileDialog().setDirectory(self.pathLine.text())
        folder = str(QFileDialog().getExistingDirectory(None, "Select directory"))
        folder = str(Path(normpath(str(folder))))
        if os.path.isdir(folder):
            self.pathLine.setText(folder)
            self.recent_xml_writer.save_new_recent_xml_content(self.sensor_selector.sensor_entries)

    def discovery(self):
        # Message box for asking user if he wants to send a UDP broadcast
        choice = QMessageBox.question(self, 'UDP Broadcast Warning!',
                                      "For the device discovery purpose, a UDP broadcast is triggered "
                                      "over all of your network interfaces."
                                      "This process will take a short time (approx. 20 seconds) "
                                      "Are you sure?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if choice == QMessageBox.StandardButton.Yes:
            threading.Thread(target=self.sensor_selector.discover_sensors, daemon=True).start()
        else:
            pass

    def disable_buttons(self):
        """Disables all buttons on GUI"""
        self.add_button.setEnabled(False)
        self.del_button.setEnabled(False)
        self.syn_button.setEnabled(False)
        self.dir_button.setEnabled(False)
        self.ext_button.setEnabled(False)
        self.udp_button.setEnabled(False)
        self.apd_button.setEnabled(False)

    def enable_buttons(self):
        """Enables all buttons on GUI"""
        self.add_button.setEnabled(True)
        self.del_button.setEnabled(True)
        self.syn_button.setEnabled(True)
        self.dir_button.setEnabled(True)
        self.ext_button.setEnabled(True)
        self.udp_button.setEnabled(True)
        self.apd_button.setEnabled(True)

    def _extract_trace_logs(self):
        # Check first if sensors are synced than run extraction function again
        if not self.sync_flag:
            self.sensor_selector.sync_sensors()

        # Init and reset values in LoggerBox
        self.logger_box.timer_start = timer()
        self.logger_box.total_bar_steps = len(self.sensor_selector.available_sensors) * 9

        # Disable all buttons
        self.disable_buttons()

        # Clear log textbox and write first line
        self.logger_box.clear_all_entries()

        # Iterate over all available sensors and extract data
        for i, sensor in enumerate(self.sensor_selector.available_sensors):
            sensor_ip = sensor[1]

            rpc_session = RPC(address=sensor_ip, save_folder=self.pathLine.text())
            sensor_name = rpc_session.call_getParameter_function(param="Name")
            sensor_model = rpc_session.call_getParameter_function(param="ArticleNumber")

            if rpc_session.call_doPing_function() == "up":
                self.logger_box.add_log_entry("Extraction process started at time: {dt}"
                                              .format(dt=datetime.today().strftime('%Y-%m-%d %H:%M:%S')))

                self.logger_box.add_log_entry("Starting extraction for sensor {model} - \"{name}\" with IP {ip}."
                                              .format(model=sensor_model, name=sensor_name, ip=sensor_ip))

                self.logger_box.add_log_entry(rpc_session.start_getAllParameters_download(), .5 * (i + 1))
                self.logger_box.add_log_entry(rpc_session.start_getSWVersion_download(), 1 * (i + 1))
                self.logger_box.add_log_entry(rpc_session.start_getHWInfo_download(), 1.5 * (i + 1))
                self.logger_box.add_log_entry(rpc_session.start_getApplicationList_download(), 2 * (i + 1))
                self.logger_box.add_log_entry(rpc_session.start_getActiveDataConnections_download(), 2.5 * (i + 1))
                self.logger_box.add_log_entry(rpc_session.start_getTraceLogs_download(lines=1000), 3 * (i + 1))
                self.logger_box.add_log_entry(rpc_session.start_getDmesgData_download(), 3.5 * (i + 1))
                self.logger_box.add_log_entry(rpc_session.start_serviceReport_download(), 7 * (i + 1))
                self.logger_box.add_log_entry(rpc_session.start_deviceAndApplicationSettings_download(), 8 * (i + 1))
                self.logger_box.add_log_entry(rpc_session.start_ifmVisionAssistantCrashDumps_download(), 8.5 * (i + 1))
                self.logger_box.add_log_entry(rpc_session.start_ifmVisionAssistantExtendedLogs_download(), 9 * (i + 1))

                self.logger_box.add_log_entry("Finished extraction for sensor {model} - \"{name}\" with IP {ip}."
                                              .format(model=sensor_model, name=sensor_name, ip=sensor_ip))

                self.logger_box.add_log_entry("Extraction process finished at time: {dt}"
                                              .format(dt=datetime.today().strftime('%Y-%m-%d %H:%M:%S')))

        # ## SAVE LOG INTO EXTRACTION FOLDER ###
        log_time = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        log_file = os.path.join(self.pathLine.text(), "{}_extract_log.txt".format(log_time))
        self.logger_box.save_log(log_file_path=log_file)

        # ## SAVE LOG INTO APPDATA FOLDER ###
        if self.log_checkbox.isChecked():
            log_file = os.path.join(self.extractor_appdata_folder, "logs", "{}_extract_log.txt".format(log_time))
            self.logger_box.save_log(log_file_path=log_file)

        # Enable all buttons after finished extraction
        self.enable_buttons()
