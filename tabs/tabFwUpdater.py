from os.path import normpath
from pathlib import Path
from timeit import default_timer as timer

from PySide6 import QtWidgets
from PySide6.QtWidgets import (
    QFileDialog,
    QMessageBox,
)

from source.multiFwUpdater import *
from source.loggerBox import LoggerBoxer
from source.sensorSelector import SensorSelector
from source.recentXmlWriter import RecentXMLWriter


class FwUpdaterTab(QtWidgets.QTabWidget):
    def __init__(self, window, recent_xml_file):
        super().__init__()
        self.ui = window
        self.recent_xml_file = recent_xml_file

        # Log box, sensor tree widget and path textbox
        self.logListWidget = self.ui.logListWidget_2
        self.sensorTreeWidget = self.ui.sensorTreeWidget_2
        self.pathLine = self.ui.pathLineEdit_2

        # Init classes
        self.logger_box = LoggerBoxer(self.logListWidget)
        self.recent_xml_writer = RecentXMLWriter(self)
        self.sensor_selector = SensorSelector(self)

        # Run methods from xml writer
        self.recent_xml_writer.check_or_make_recent_xml_file_path()
        self.recent_xml_writer.init_sensors_from_existing_recent_xml()
        self.recent_xml_writer.init_path_from_existing_recent_xml()

        # Buttons
        self.add_button = self.ui.addButton_2  # Add button
        self.del_button = self.ui.deleteButton_2  # Delete button
        self.dir_button = self.ui.selectFileButton  # Select directory button
        self.syn_button = self.ui.syncButton_2  # Sync button
        self.upt_button = self.ui.updateButton  # Extract button
        self.udp_button = self.ui.discoveryButton_2  # Discovery button
        self.apd_button = self.ui.openAppdataButton_2  # open Appdata button

        self.upt_button.clicked.connect(self.start)
        self.add_button.clicked.connect(self.sensor_selector.add)
        self.del_button.clicked.connect(self.sensor_selector.delete)
        self.syn_button.clicked.connect(self.sensor_selector.sync)
        self.dir_button.clicked.connect(self.swu_file_path)
        self.udp_button.clicked.connect(self.discovery)
        self.apd_button.clicked.connect(self.open_appdata_folder)

        # Checkboxes
        self.log_checkbox = self.ui.logCheckBox_2
        self.bck_checkbox = self.ui.backupCheckBox
        self.rst_checkbox = self.ui.restoreCheckBox

        self.log_checkbox.clicked.connect(self.checkbox_log_clicked)
        self.bck_checkbox.clicked.connect(self.checkbox_backup_clicked)
        self.rst_checkbox.clicked.connect(self.checkbox_restore_clicked)

        self.sync_flag = False

    def checkbox_log_clicked(self):
        if self.log_checkbox.isChecked():
            self.log_checkbox.setChecked(True)
            self.logger_box.add_log_entry("Activated log process of this output into APPDATA folder.")
        else:
            self.log_checkbox.setChecked(False)
            self.logger_box.add_log_entry("WARNING: Deactivated log process of this output into APPDATA folder.")

    def checkbox_backup_clicked(self):
        if self.bck_checkbox.isChecked():
            self.bck_checkbox.setChecked(True)
            self.logger_box.add_log_entry("Activated backup process of device config. If you want to restore your "
                                          "device config on the sensor, please activate the restore process.")
        else:
            self.bck_checkbox.setChecked(False)
            self.rst_checkbox.setChecked(False)
            self.logger_box.add_log_entry("WARNING: Deactivated backup process of device config. "
                                          "Auto-deactivated restore process.")

    def checkbox_restore_clicked(self):
        if not self.bck_checkbox.isChecked():
            self.rst_checkbox.setChecked(False)
            self.logger_box.add_log_entry("ERROR: Unable to activated restore process. "
                                          "Please first activate the backup process.")
        else:
            if self.rst_checkbox.isChecked():
                self.logger_box.add_log_entry("Activated restore process of device config.")
            else:
                self.logger_box.add_log_entry("WARNING: Deactivated restore process of device config.")

    @property
    def updater_appdata_folder(self):
        appdata_path = os.getenv('APPDATA')
        if appdata_path:
            appdata_path = os.path.join(appdata_path, "ifm electronic", "ifmVisionServiceTool", "updater")
            return appdata_path
        else:
            self.logger_box.add_log_entry("APPDATA path not found.")

    def open_appdata_folder(self):
        if self.updater_appdata_folder:
            os.system(f'explorer "{self.updater_appdata_folder}"')
        else:
            self.logger_box.add_log_entry("Folder for extractor in APPDATA not found.")

    def start(self):
        # Message box for asking user if he wants to stop the sensors while extracting the data
        choice = QMessageBox.question(self, 'Firmware Update Warning!',
                                      "For the update process, the sensor is taken out of run mode for a "
                                      "longer time (approx. 3-5 minutes) and does not provide any results.\n\n"
                                      "We do not check whether the selected firmware matches the sensors in the list. "
                                      "Please note that some sensors will be put into recovery mode "
                                      "if the wrong selection is made!\n\n"
                                      "Are you sure?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if choice == QMessageBox.StandardButton.Yes:
            threading.Thread(target=self._update_sensors, daemon=True).start()
        else:
            pass

    def swu_file_path(self):
        QFileDialog().setDirectory(self.pathLine.text())
        swu_file, _ = QFileDialog().getOpenFileName(None, "Select update file", "", "*.swu")
        swu_file_path = str(Path(normpath(str(swu_file))))
        is_swu_file = validate_swu_files(swu_file_path, self.logger_box)
        # Write valid swu file to recent.xml
        if is_swu_file:
            self.pathLine.setText(swu_file_path)
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
        self.upt_button.setEnabled(False)
        self.udp_button.setEnabled(False)
        self.apd_button.setEnabled(False)

    def enable_buttons(self):
        """Enables all buttons on GUI"""
        self.add_button.setEnabled(True)
        self.del_button.setEnabled(True)
        self.syn_button.setEnabled(True)
        self.dir_button.setEnabled(True)
        self.upt_button.setEnabled(True)
        self.udp_button.setEnabled(True)
        self.apd_button.setEnabled(True)

    @staticmethod
    def check_or_make_dir(path):
        if not os.path.exists(path):
            # directory does not exist
            os.makedirs(path)

    def _update_sensors(self):
        start = datetime.now()
        # Check first if sensors are synced than run extraction function again
        if not self.sync_flag:
            self.sensor_selector.sync_sensors()

        # Init and reset values in LoggerBox
        self.logger_box.timer_start = timer()
        self.logger_box.total_bar_steps = len(self.sensor_selector.available_sensors) * 9

        # ### INIT DEVICE UPDATER PROCESS ###
        firmware_updater = []
        for i, sensor in enumerate(self.sensor_selector.available_sensors):
            sensor_ip = sensor[1]

            updater = FirmwareUpdater(address=sensor_ip, update_files=[self.pathLine.text()],
                                      logger_box=self.logger_box)
            firmware_updater.append(updater)

        # Skip update process if no device is ready or reachable
        if not firmware_updater:
            self.logger_box.add_log_entry("No firmware updater detected. "
                                          "Check your device IPs. Stopping update process here.")

        # Disable all buttons if everything is fine
        self.disable_buttons()

        # Clear log textbox and write first line
        self.logger_box.clear_all_entries()

        # ### BACKUP DEVICE CONFIG PROCESS ###
        backup_start_datetime_for_threads = datetime.now()
        backup_start_datetime = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        self.logger_box.add_log_entry("Backup process started at time: {dt}"
                                      .format(dt=datetime.today().strftime('%Y-%m-%d %H:%M:%S')))
        # Check or make backup folder
        backup_path = os.path.join(self.updater_appdata_folder, "backup", "{}".format(backup_start_datetime))
        self.check_or_make_dir(path=backup_path)

        # Thread config backup process for each device
        for u in firmware_updater:
            self.logger_box.add_log_entry("{} : Config backup thread started. Config backup stored here:\n{}"
                                          .format(u.address, backup_path))
            thread = threading.Thread(target=threaded_backup_device_config, daemon=True,
                                      kwargs={"_updater": u, "backup_path": backup_path})
            thread.name = 'ifm_config_backup_IP_{}'.format(u.address)
            thread.start()

        backup_threads = [t for t in threading.enumerate() if "ifm_config_backup_IP_" in t.name]
        trace_threads(backup_threads, backup_start_datetime_for_threads, thread_type="backup",
                      logger_box=self.logger_box)

        self.logger_box.add_log_entry("Backup process finished at time: {dt}"
                                      .format(dt=datetime.today().strftime('%Y-%m-%d %H:%M:%S')))

        # ## UPDATE DEVICE FIRMWARE PROCESS ###
        updater_start_datetime_for_threads = datetime.now()
        self.logger_box.add_log_entry("Firmware update process started at time: {dt}"
                                      .format(dt=datetime.today().strftime('%Y-%m-%d %H:%M:%S')))

        # Thread updater process for each device
        for u in firmware_updater:
            self.logger_box.add_log_entry("{} : swu update started ...".format(u.address))
            thread = threading.Thread(target=threaded_install_swu, daemon=True, kwargs={"_updater": u})
            thread.name = 'ifm_FW_updater_IP_{}'.format(u.address)
            thread.start()

        updater_threads = [t for t in threading.enumerate() if "ifm_FW_updater_IP_" in t.name]
        trace_threads(updater_threads, updater_start_datetime_for_threads, thread_type="update",
                      logger_box=self.logger_box)

        self.logger_box.add_log_entry("Firmware update process finished at time: {dt}"
                                      .format(dt=datetime.today().strftime('%Y-%m-%d %H:%M:%S')))

        # ## RESTORE DEVICE CONFIG PROCESS ###
        if self.bck_checkbox.isChecked():
            import_start_datetime_for_threads = datetime.now()
            self.logger_box.add_log_entry("Firmware update process started at time: {dt}"
                                          .format(dt=datetime.today().strftime('%Y-%m-%d %H:%M:%S')))

            # Thread config import process for each device
            for u in firmware_updater:
                self.logger_box.add_log_entry("{} : Config import thread started ...".format(u.address))
                thread = threading.Thread(target=threaded_import_device_config, daemon=True, kwargs={"_updater": u})
                thread.name = 'ifm_config_import_IP_{}'.format(u.address)
                thread.start()

            import_threads = [t for t in threading.enumerate() if "ifm_config_import_IP_" in t.name]
            trace_threads(import_threads, import_start_datetime_for_threads, thread_type="import",
                          logger_box=self.logger_box)

        # ## SAVE LOG INTO APPDATA FOLDER ###
        log_time = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        if self.log_checkbox.isChecked():
            log_file = os.path.join(self.updater_appdata_folder, "logs", "{}_extract_log.txt".format(log_time))
            self.logger_box.save_log(log_file_path=log_file)

        # Enable all buttons after finished extraction
        self.enable_buttons()

        self.logger_box.add_log_entry("Total update process runtime: {}".format(datetime.now() - start))
        self.logger_box.add_log_entry("Finished update process!")
