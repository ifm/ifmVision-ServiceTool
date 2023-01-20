# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_form_with_textnOXKox.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
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
from PySide6.QtWidgets import (QApplication, QDialog, QHeaderView, QLineEdit,
    QListWidget, QListWidgetItem, QProgressBar, QPushButton,
    QSizePolicy, QToolButton, QTreeWidget, QTreeWidgetItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(685, 484)
        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(560, 100, 101, 31))
        self.listWidget = QListWidget(Dialog)
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.NoBrush)
        brush1 = QBrush(QColor(0, 0, 0, 255))
        brush1.setStyle(Qt.NoBrush)
        __qlistwidgetitem = QListWidgetItem(self.listWidget)
        __qlistwidgetitem.setBackground(brush1);
        __qlistwidgetitem.setForeground(brush);
        brush2 = QBrush(QColor(0, 85, 0, 255))
        brush2.setStyle(Qt.NoBrush)
        __qlistwidgetitem1 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem1.setForeground(brush2);
        brush3 = QBrush(QColor(0, 85, 0, 255))
        brush3.setStyle(Qt.NoBrush)
        __qlistwidgetitem2 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem2.setForeground(brush3);
        brush4 = QBrush(QColor(0, 85, 0, 255))
        brush4.setStyle(Qt.NoBrush)
        __qlistwidgetitem3 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem3.setForeground(brush4);
        brush5 = QBrush(QColor(0, 85, 0, 255))
        brush5.setStyle(Qt.NoBrush)
        __qlistwidgetitem4 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem4.setForeground(brush5);
        brush6 = QBrush(QColor(0, 85, 0, 255))
        brush6.setStyle(Qt.NoBrush)
        __qlistwidgetitem5 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem5.setForeground(brush6);
        brush7 = QBrush(QColor(170, 0, 0, 255))
        brush7.setStyle(Qt.NoBrush)
        __qlistwidgetitem6 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem6.setForeground(brush7);
        brush8 = QBrush(QColor(0, 0, 255, 255))
        brush8.setStyle(Qt.NoBrush)
        __qlistwidgetitem7 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem7.setForeground(brush8);
        brush9 = QBrush(QColor(0, 85, 0, 255))
        brush9.setStyle(Qt.NoBrush)
        __qlistwidgetitem8 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem8.setForeground(brush9);
        QListWidgetItem(self.listWidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setEnabled(True)
        self.listWidget.setGeometry(QRect(20, 180, 641, 241))
        self.progressBar = QProgressBar(Dialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(20, 430, 641, 31))
        self.progressBar.setAutoFillBackground(False)
        self.progressBar.setValue(24)
        self.progressBar.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.treeWidget = QTreeWidget(Dialog)
        QTreeWidgetItem(self.treeWidget)
        QTreeWidgetItem(self.treeWidget)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setGeometry(QRect(20, 20, 521, 111))
        self.pushButton_2 = QPushButton(Dialog)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(560, 20, 101, 31))
        self.pushButton_3 = QPushButton(Dialog)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(560, 60, 101, 31))
        self.toolButton = QToolButton(Dialog)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setGeometry(QRect(560, 140, 101, 31))
        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setEnabled(False)
        self.lineEdit.setGeometry(QRect(20, 140, 521, 31))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"TraceExtractor - O2D5xx - O3D3xx", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Extract", None))

        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Dialog", u"Starting extraction for Sensor \"Sensor 1\" with IP 192.168.0.69 ...", None));
        ___qlistwidgetitem1 = self.listWidget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("Dialog", u"Extracting getAllParameters() was successful ...", None));
        ___qlistwidgetitem2 = self.listWidget.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("Dialog", u"Extracting getSWVersion() was successful ...", None));
        ___qlistwidgetitem3 = self.listWidget.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("Dialog", u"Extracting getHWInfo() was successful ...", None));
        ___qlistwidgetitem4 = self.listWidget.item(4)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("Dialog", u"Extracting getApplicationList() was successful ...", None));
        ___qlistwidgetitem5 = self.listWidget.item(5)
        ___qlistwidgetitem5.setText(QCoreApplication.translate("Dialog", u"Extracting getTraceLogs() was successful ...", None));
        ___qlistwidgetitem6 = self.listWidget.item(6)
        ___qlistwidgetitem6.setText(QCoreApplication.translate("Dialog", u"Extracting ServiceReport failed ...", None));
        ___qlistwidgetitem7 = self.listWidget.item(7)
        ___qlistwidgetitem7.setText(QCoreApplication.translate("Dialog", u"Extracting logs for ifmVisionAssistant skipped ... (0 files found)", None));
        ___qlistwidgetitem8 = self.listWidget.item(8)
        ___qlistwidgetitem8.setText(QCoreApplication.translate("Dialog", u"Extracting crashDumps for ifmVisionAssistant successful ... (6 files found)", None));
        ___qlistwidgetitem9 = self.listWidget.item(9)
        ___qlistwidgetitem9.setText(QCoreApplication.translate("Dialog", u"Starting extraction for Sensor \"Sensor 2\" with IP 192.168.0.70 ...", None));
        self.listWidget.setSortingEnabled(__sortingEnabled)

        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("Dialog", u"name", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"available", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"ip address", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"id", None));

        __sortingEnabled1 = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.treeWidget.topLevelItem(0)
        ___qtreewidgetitem1.setText(3, QCoreApplication.translate("Dialog", u"Sensor 1", None));
        ___qtreewidgetitem1.setText(2, QCoreApplication.translate("Dialog", u"up", None));
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("Dialog", u"192.168.0.69", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Dialog", u"1", None));
        ___qtreewidgetitem2 = self.treeWidget.topLevelItem(1)
        ___qtreewidgetitem2.setText(3, QCoreApplication.translate("Dialog", u"Sensor 2", None));
        ___qtreewidgetitem2.setText(2, QCoreApplication.translate("Dialog", u"up", None));
        ___qtreewidgetitem2.setText(1, QCoreApplication.translate("Dialog", u"192.168.0.70", None));
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("Dialog", u"2", None));
        self.treeWidget.setSortingEnabled(__sortingEnabled1)

        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"Add", None))
        self.pushButton_3.setText(QCoreApplication.translate("Dialog", u"Delete", None))
        self.toolButton.setText(QCoreApplication.translate("Dialog", u"Save as", None))
        self.lineEdit.setText(QCoreApplication.translate("Dialog", u"C:\\git\\O2D5xx_TraceLogs", None))
    # retranslateUi

