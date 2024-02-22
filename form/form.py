# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QHeaderView,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QTabWidget, QToolButton, QTreeWidget,
    QTreeWidgetItem, QWidget)

class Ui_ServiceTool(object):
    def setupUi(self, ServiceTool):
        if not ServiceTool.objectName():
            ServiceTool.setObjectName(u"ServiceTool")
        ServiceTool.resize(862, 529)
        icon = QIcon()
        icon.addFile(u"../doc/ifm_logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        ServiceTool.setWindowIcon(icon)
        ServiceTool.setStyleSheet(u"")
        self.tabWidget = QTabWidget(ServiceTool)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 10, 841, 501))
        font = QFont()
        font.setFamilies([u"Roboto"])
        font.setBold(True)
        self.tabWidget.setFont(font)
        self.tabWidget.setStyleSheet(u"")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.syncButton = QPushButton(self.tab)
        self.syncButton.setObjectName(u"syncButton")
        self.syncButton.setGeometry(QRect(700, 90, 121, 31))
        self.syncButton.setFont(font)
        self.syncButton.setStyleSheet(u"")
        self.addButton = QPushButton(self.tab)
        self.addButton.setObjectName(u"addButton")
        self.addButton.setGeometry(QRect(700, 10, 121, 31))
        self.addButton.setFont(font)
        self.addButton.setStyleSheet(u"")
        self.extractButton = QPushButton(self.tab)
        self.extractButton.setObjectName(u"extractButton")
        self.extractButton.setGeometry(QRect(700, 430, 121, 31))
        self.extractButton.setFont(font)
        self.extractButton.setStyleSheet(u"")
        self.pathLineEdit = QLineEdit(self.tab)
        self.pathLineEdit.setObjectName(u"pathLineEdit")
        self.pathLineEdit.setEnabled(False)
        self.pathLineEdit.setGeometry(QRect(10, 430, 531, 31))
        self.pathLineEdit.setFont(font)
        self.pathLineEdit.setAutoFillBackground(False)
        self.pathLineEdit.setStyleSheet(u"")
        self.selectDirButton = QToolButton(self.tab)
        self.selectDirButton.setObjectName(u"selectDirButton")
        self.selectDirButton.setGeometry(QRect(560, 430, 121, 31))
        self.selectDirButton.setFont(font)
        self.selectDirButton.setStyleSheet(u"")
        self.deleteButton = QPushButton(self.tab)
        self.deleteButton.setObjectName(u"deleteButton")
        self.deleteButton.setGeometry(QRect(700, 50, 121, 31))
        self.deleteButton.setFont(font)
        self.deleteButton.setStyleSheet(u"")
        self.sensorTreeWidget = QTreeWidget(self.tab)
        QTreeWidgetItem(self.sensorTreeWidget)
        QTreeWidgetItem(self.sensorTreeWidget)
        self.sensorTreeWidget.setObjectName(u"sensorTreeWidget")
        self.sensorTreeWidget.setGeometry(QRect(10, 10, 671, 111))
        self.sensorTreeWidget.setFont(font)
        self.sensorTreeWidget.setStyleSheet(u"")
        self.logListWidget = QListWidget(self.tab)
        QListWidgetItem(self.logListWidget)
        QListWidgetItem(self.logListWidget)
        QListWidgetItem(self.logListWidget)
        self.logListWidget.setObjectName(u"logListWidget")
        self.logListWidget.setEnabled(True)
        self.logListWidget.setGeometry(QRect(10, 170, 811, 251))
        self.logListWidget.setFont(font)
        self.logListWidget.setStyleSheet(u"")
        self.discoveryButton = QPushButton(self.tab)
        self.discoveryButton.setObjectName(u"discoveryButton")
        self.discoveryButton.setGeometry(QRect(700, 130, 121, 31))
        self.discoveryButton.setFont(font)
        self.discoveryButton.setStyleSheet(u"")
        self.logCheckBox = QCheckBox(self.tab)
        self.logCheckBox.setObjectName(u"logCheckBox")
        self.logCheckBox.setGeometry(QRect(20, 140, 121, 17))
        self.logCheckBox.setFont(font)
        self.logCheckBox.setStyleSheet(u"")
        self.logCheckBox.setChecked(True)
        self.openAppdataButton = QPushButton(self.tab)
        self.openAppdataButton.setObjectName(u"openAppdataButton")
        self.openAppdataButton.setGeometry(QRect(560, 130, 121, 31))
        self.openAppdataButton.setFont(font)
        self.openAppdataButton.setStyleSheet(u"")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.lineEdit_2 = QLineEdit(self.tab_2)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_2.setGeometry(QRect(10, 430, 521, 31))
        self.lineEdit_2.setFont(font)
        self.backupCheckBox = QCheckBox(self.tab_2)
        self.backupCheckBox.setObjectName(u"backupCheckBox")
        self.backupCheckBox.setGeometry(QRect(170, 140, 151, 17))
        self.backupCheckBox.setFont(font)
        self.backupCheckBox.setStyleSheet(u"")
        self.backupCheckBox.setChecked(True)
        self.deleteButton_2 = QPushButton(self.tab_2)
        self.deleteButton_2.setObjectName(u"deleteButton_2")
        self.deleteButton_2.setGeometry(QRect(700, 50, 121, 31))
        self.deleteButton_2.setFont(font)
        self.deleteButton_2.setStyleSheet(u"")
        self.discoveryButton_2 = QPushButton(self.tab_2)
        self.discoveryButton_2.setObjectName(u"discoveryButton_2")
        self.discoveryButton_2.setGeometry(QRect(700, 130, 121, 31))
        self.discoveryButton_2.setFont(font)
        self.discoveryButton_2.setStyleSheet(u"")
        self.addButton_2 = QPushButton(self.tab_2)
        self.addButton_2.setObjectName(u"addButton_2")
        self.addButton_2.setGeometry(QRect(700, 10, 121, 31))
        self.addButton_2.setFont(font)
        self.addButton_2.setStyleSheet(u"")
        self.syncButton_2 = QPushButton(self.tab_2)
        self.syncButton_2.setObjectName(u"syncButton_2")
        self.syncButton_2.setGeometry(QRect(700, 90, 121, 31))
        self.syncButton_2.setFont(font)
        self.syncButton_2.setStyleSheet(u"")
        self.logListWidget_2 = QListWidget(self.tab_2)
        QListWidgetItem(self.logListWidget_2)
        QListWidgetItem(self.logListWidget_2)
        QListWidgetItem(self.logListWidget_2)
        self.logListWidget_2.setObjectName(u"logListWidget_2")
        self.logListWidget_2.setEnabled(True)
        self.logListWidget_2.setGeometry(QRect(10, 170, 811, 251))
        self.logListWidget_2.setFont(font)
        self.logCheckBox_2 = QCheckBox(self.tab_2)
        self.logCheckBox_2.setObjectName(u"logCheckBox_2")
        self.logCheckBox_2.setGeometry(QRect(20, 140, 121, 17))
        self.logCheckBox_2.setFont(font)
        self.logCheckBox_2.setStyleSheet(u"")
        self.logCheckBox_2.setChecked(True)
        self.pathLineEdit_2 = QLineEdit(self.tab_2)
        self.pathLineEdit_2.setObjectName(u"pathLineEdit_2")
        self.pathLineEdit_2.setEnabled(False)
        self.pathLineEdit_2.setGeometry(QRect(10, 430, 531, 31))
        self.pathLineEdit_2.setFont(font)
        self.selectFileButton = QToolButton(self.tab_2)
        self.selectFileButton.setObjectName(u"selectFileButton")
        self.selectFileButton.setGeometry(QRect(560, 430, 121, 31))
        self.selectFileButton.setFont(font)
        self.selectFileButton.setStyleSheet(u"")
        self.updateButton = QPushButton(self.tab_2)
        self.updateButton.setObjectName(u"updateButton")
        self.updateButton.setGeometry(QRect(700, 430, 121, 31))
        self.updateButton.setFont(font)
        self.updateButton.setStyleSheet(u"")
        self.sensorTreeWidget_2 = QTreeWidget(self.tab_2)
        QTreeWidgetItem(self.sensorTreeWidget_2)
        QTreeWidgetItem(self.sensorTreeWidget_2)
        self.sensorTreeWidget_2.setObjectName(u"sensorTreeWidget_2")
        self.sensorTreeWidget_2.setGeometry(QRect(10, 10, 671, 111))
        self.sensorTreeWidget_2.setFont(font)
        self.openAppdataButton_2 = QPushButton(self.tab_2)
        self.openAppdataButton_2.setObjectName(u"openAppdataButton_2")
        self.openAppdataButton_2.setGeometry(QRect(560, 130, 121, 31))
        self.openAppdataButton_2.setFont(font)
        self.openAppdataButton_2.setStyleSheet(u"")
        self.restoreCheckBox = QCheckBox(self.tab_2)
        self.restoreCheckBox.setObjectName(u"restoreCheckBox")
        self.restoreCheckBox.setGeometry(QRect(350, 140, 151, 17))
        self.restoreCheckBox.setFont(font)
        self.restoreCheckBox.setStyleSheet(u"")
        self.restoreCheckBox.setChecked(True)
        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(ServiceTool)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ServiceTool)
    # setupUi

    def retranslateUi(self, ServiceTool):
        ServiceTool.setWindowTitle(QCoreApplication.translate("ServiceTool", u"ifmVision - ServiceTool (O2D5, O3D3, O2I5, O2U5)", None))
        self.syncButton.setText(QCoreApplication.translate("ServiceTool", u"Sync", None))
        self.addButton.setText(QCoreApplication.translate("ServiceTool", u"Add", None))
        self.extractButton.setText(QCoreApplication.translate("ServiceTool", u"Extract", None))
        self.pathLineEdit.setText(QCoreApplication.translate("ServiceTool", u"<Select directory>", None))
        self.selectDirButton.setText(QCoreApplication.translate("ServiceTool", u"Select directory", None))
        self.deleteButton.setText(QCoreApplication.translate("ServiceTool", u"Delete", None))
        ___qtreewidgetitem = self.sensorTreeWidget.headerItem()
        ___qtreewidgetitem.setText(5, QCoreApplication.translate("ServiceTool", u"FW Version", None));
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("ServiceTool", u"Model", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("ServiceTool", u"Name", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("ServiceTool", u"Available", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("ServiceTool", u"IP Address", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("ServiceTool", u"ID", None));

        __sortingEnabled = self.sensorTreeWidget.isSortingEnabled()
        self.sensorTreeWidget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.sensorTreeWidget.topLevelItem(0)
        ___qtreewidgetitem1.setText(5, QCoreApplication.translate("ServiceTool", u"n.a.", None));
        ___qtreewidgetitem1.setText(4, QCoreApplication.translate("ServiceTool", u"n.a.", None));
        ___qtreewidgetitem1.setText(3, QCoreApplication.translate("ServiceTool", u"n.a.", None));
        ___qtreewidgetitem1.setText(2, QCoreApplication.translate("ServiceTool", u"n.a.", None));
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("ServiceTool", u"192.168.0.69", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("ServiceTool", u"1", None));
        ___qtreewidgetitem2 = self.sensorTreeWidget.topLevelItem(1)
        ___qtreewidgetitem2.setText(5, QCoreApplication.translate("ServiceTool", u"n.a.", None));
        ___qtreewidgetitem2.setText(4, QCoreApplication.translate("ServiceTool", u"n.a.", None));
        ___qtreewidgetitem2.setText(3, QCoreApplication.translate("ServiceTool", u"n.a.", None));
        ___qtreewidgetitem2.setText(2, QCoreApplication.translate("ServiceTool", u"n.a.", None));
        ___qtreewidgetitem2.setText(1, QCoreApplication.translate("ServiceTool", u"192.168.0.70", None));
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("ServiceTool", u"2", None));
        self.sensorTreeWidget.setSortingEnabled(__sortingEnabled)


        __sortingEnabled1 = self.logListWidget.isSortingEnabled()
        self.logListWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.logListWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("ServiceTool", u"Welcome to our ifm Vision Service Tool.", None));
        ___qlistwidgetitem1 = self.logListWidget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("ServiceTool", u"Feel free to use our Log and Trace Extractor or the Multi Firmware Updater feature.", None));
        ___qlistwidgetitem2 = self.logListWidget.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("ServiceTool", u"Both are compatible for the sensor types O2D5xx, O2I5xx, O2U5xx and O3D3xx.", None));
        self.logListWidget.setSortingEnabled(__sortingEnabled1)

        self.discoveryButton.setText(QCoreApplication.translate("ServiceTool", u"Discovery", None))
        self.logCheckBox.setText(QCoreApplication.translate("ServiceTool", u"Log into APPDATA", None))
        self.openAppdataButton.setText(QCoreApplication.translate("ServiceTool", u"Open APPDATA", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("ServiceTool", u"Log Extractor", None))
        self.lineEdit_2.setStyleSheet("")
        self.lineEdit_2.setText(QCoreApplication.translate("ServiceTool", u"<Select file>", None))
        self.backupCheckBox.setText(QCoreApplication.translate("ServiceTool", u"Backup device(s) config", None))
        self.deleteButton_2.setText(QCoreApplication.translate("ServiceTool", u"Delete", None))
        self.discoveryButton_2.setText(QCoreApplication.translate("ServiceTool", u"Discovery", None))
        self.addButton_2.setText(QCoreApplication.translate("ServiceTool", u"Add", None))
        self.syncButton_2.setText(QCoreApplication.translate("ServiceTool", u"Sync", None))

        __sortingEnabled2 = self.logListWidget_2.isSortingEnabled()
        self.logListWidget_2.setSortingEnabled(False)
        ___qlistwidgetitem3 = self.logListWidget_2.item(0)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("ServiceTool", u"Welcome to our ifm Vision Service Tool.", None));
        ___qlistwidgetitem4 = self.logListWidget_2.item(1)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("ServiceTool", u"Feel free to use our Log and Trace Extractor or the Multi Firmware Updater feature.", None));
        ___qlistwidgetitem5 = self.logListWidget_2.item(2)
        ___qlistwidgetitem5.setText(QCoreApplication.translate("ServiceTool", u"Both are compatible for the sensor types O2D5xx, O2I5xx, O2U5xx and O3D3xx.", None));
        self.logListWidget_2.setSortingEnabled(__sortingEnabled2)

        self.logListWidget_2.setStyleSheet("")
        self.logCheckBox_2.setText(QCoreApplication.translate("ServiceTool", u"Log into APPDATA", None))
        self.pathLineEdit_2.setStyleSheet("")
        self.pathLineEdit_2.setText(QCoreApplication.translate("ServiceTool", u"<Select file>", None))
        self.selectFileButton.setText(QCoreApplication.translate("ServiceTool", u"Select file", None))
        self.updateButton.setText(QCoreApplication.translate("ServiceTool", u"Update", None))
        ___qtreewidgetitem3 = self.sensorTreeWidget_2.headerItem()
        ___qtreewidgetitem3.setText(5, QCoreApplication.translate("ServiceTool", u"FW Version", None));
        ___qtreewidgetitem3.setText(4, QCoreApplication.translate("ServiceTool", u"Model", None));
        ___qtreewidgetitem3.setText(3, QCoreApplication.translate("ServiceTool", u"Name", None));
        ___qtreewidgetitem3.setText(2, QCoreApplication.translate("ServiceTool", u"Available", None));
        ___qtreewidgetitem3.setText(1, QCoreApplication.translate("ServiceTool", u"IP Address", None));
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("ServiceTool", u"ID", None));

        __sortingEnabled3 = self.sensorTreeWidget_2.isSortingEnabled()
        self.sensorTreeWidget_2.setSortingEnabled(False)
        ___qtreewidgetitem4 = self.sensorTreeWidget_2.topLevelItem(0)
        ___qtreewidgetitem4.setText(5, QCoreApplication.translate("ServiceTool", u"n.a.", None));
        ___qtreewidgetitem4.setText(4, QCoreApplication.translate("ServiceTool", u"n.a.", None));
        ___qtreewidgetitem4.setText(3, QCoreApplication.translate("ServiceTool", u"n.a.", None));
        ___qtreewidgetitem4.setText(2, QCoreApplication.translate("ServiceTool", u"n.a.", None));
        ___qtreewidgetitem4.setText(1, QCoreApplication.translate("ServiceTool", u"192.168.0.69", None));
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("ServiceTool", u"1", None));
        ___qtreewidgetitem5 = self.sensorTreeWidget_2.topLevelItem(1)
        ___qtreewidgetitem5.setText(5, QCoreApplication.translate("ServiceTool", u"n.a.", None));
        ___qtreewidgetitem5.setText(4, QCoreApplication.translate("ServiceTool", u"n.a.", None));
        ___qtreewidgetitem5.setText(3, QCoreApplication.translate("ServiceTool", u"n.a.", None));
        ___qtreewidgetitem5.setText(2, QCoreApplication.translate("ServiceTool", u"n.a.", None));
        ___qtreewidgetitem5.setText(1, QCoreApplication.translate("ServiceTool", u"192.168.0.70", None));
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("ServiceTool", u"2", None));
        self.sensorTreeWidget_2.setSortingEnabled(__sortingEnabled3)

        self.sensorTreeWidget_2.setStyleSheet("")
        self.openAppdataButton_2.setText(QCoreApplication.translate("ServiceTool", u"Open APPDATA", None))
        self.restoreCheckBox.setText(QCoreApplication.translate("ServiceTool", u"Restore device(s) config", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("ServiceTool", u"Firmware Updater", None))
    # retranslateUi

