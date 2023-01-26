# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'formLkZAWK.ui'
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
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QToolButton, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(678, 448)
        icon = QIcon()
        icon.addFile(u"ifm_logo.ico", QSize(), QIcon.Normal, QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(560, 400, 101, 31))
        font = QFont()
        font.setBold(True)
        self.pushButton.setFont(font)
        self.listWidget = QListWidget(Dialog)
        QListWidgetItem(self.listWidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setEnabled(True)
        self.listWidget.setGeometry(QRect(20, 140, 641, 251))
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
        self.toolButton.setGeometry(QRect(450, 400, 101, 31))
        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setEnabled(False)
        self.lineEdit.setGeometry(QRect(20, 400, 421, 31))
        self.pushButton_4 = QPushButton(Dialog)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(560, 100, 101, 31))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"ifmVision - LogTracesExtractor (O2D5, O3D3, O2I5)", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Extract", None))

        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Dialog", u"Welcome to our new Log and Trace Extractor for the sensor types O2D5xx, O2I5xx and O3D3xx.", None));
        self.listWidget.setSortingEnabled(__sortingEnabled)

        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("Dialog", u"model", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("Dialog", u"name", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"available", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"ip address", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"id", None));

        __sortingEnabled1 = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.treeWidget.topLevelItem(0)
        ___qtreewidgetitem1.setText(4, QCoreApplication.translate("Dialog", u"O2D524", None));
        ___qtreewidgetitem1.setText(3, QCoreApplication.translate("Dialog", u"Sensor 2D", None));
        ___qtreewidgetitem1.setText(2, QCoreApplication.translate("Dialog", u"n.a.", None));
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("Dialog", u"192.168.0.69", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Dialog", u"1", None));
        ___qtreewidgetitem2 = self.treeWidget.topLevelItem(1)
        ___qtreewidgetitem2.setText(4, QCoreApplication.translate("Dialog", u"O3D354", None));
        ___qtreewidgetitem2.setText(3, QCoreApplication.translate("Dialog", u"Sensor 3D", None));
        ___qtreewidgetitem2.setText(2, QCoreApplication.translate("Dialog", u"n.a.", None));
        ___qtreewidgetitem2.setText(1, QCoreApplication.translate("Dialog", u"192.168.0.70", None));
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("Dialog", u"2", None));
        self.treeWidget.setSortingEnabled(__sortingEnabled1)

        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"Add", None))
        self.pushButton_3.setText(QCoreApplication.translate("Dialog", u"Delete", None))
        self.toolButton.setText(QCoreApplication.translate("Dialog", u"Select directory", None))
        self.lineEdit.setText(QCoreApplication.translate("Dialog", u"<Select directory>", None))
        self.pushButton_4.setText(QCoreApplication.translate("Dialog", u"Sync", None))
    # retranslateUi

