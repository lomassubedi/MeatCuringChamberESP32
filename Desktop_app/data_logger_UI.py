# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data_logger_dialogue.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DataLoggerSetting(object):
    def setupUi(self, DataLoggerSetting):
        DataLoggerSetting.setObjectName("DataLoggerSetting")
        DataLoggerSetting.resize(388, 128)
        self.lineEditBrowsePath = QtWidgets.QLineEdit(DataLoggerSetting)
        self.lineEditBrowsePath.setGeometry(QtCore.QRect(20, 40, 271, 20))
        self.lineEditBrowsePath.setObjectName("lineEditBrowsePath")
        self.labelBrowseFile = QtWidgets.QLabel(DataLoggerSetting)
        self.labelBrowseFile.setGeometry(QtCore.QRect(20, 20, 111, 16))
        self.labelBrowseFile.setObjectName("labelBrowseFile")
        self.pushButtonBrowse = QtWidgets.QPushButton(DataLoggerSetting)
        self.pushButtonBrowse.setGeometry(QtCore.QRect(300, 40, 75, 23))
        self.pushButtonBrowse.setObjectName("pushButtonBrowse")
        self.pushButtonApply = QtWidgets.QPushButton(DataLoggerSetting)
        self.pushButtonApply.setGeometry(QtCore.QRect(200, 90, 75, 23))
        self.pushButtonApply.setObjectName("pushButtonApply")
        self.pushButtonExit = QtWidgets.QPushButton(DataLoggerSetting)
        self.pushButtonExit.setGeometry(QtCore.QRect(290, 90, 75, 23))
        self.pushButtonExit.setObjectName("pushButtonExit")

        self.retranslateUi(DataLoggerSetting)
        QtCore.QMetaObject.connectSlotsByName(DataLoggerSetting)

    def retranslateUi(self, DataLoggerSetting):
        _translate = QtCore.QCoreApplication.translate
        DataLoggerSetting.setWindowTitle(_translate("DataLoggerSetting", "Data Logger Setting"))
        self.labelBrowseFile.setText(_translate("DataLoggerSetting", "Browse for the log file."))
        self.pushButtonBrowse.setText(_translate("DataLoggerSetting", "Browse"))
        self.pushButtonApply.setText(_translate("DataLoggerSetting", "Apply"))
        self.pushButtonExit.setText(_translate("DataLoggerSetting", "Exit"))
