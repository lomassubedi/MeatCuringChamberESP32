# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\prefence.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Preferences(object):
    def setupUi(self, Preferences):
        Preferences.setObjectName("Preferences")
        Preferences.resize(361, 193)
        self.labelBrokerIP = QtWidgets.QLabel(Preferences)
        self.labelBrokerIP.setGeometry(QtCore.QRect(20, 20, 91, 16))
        self.labelBrokerIP.setObjectName("labelBrokerIP")
        self.lineEditBrokerIP = QtWidgets.QLineEdit(Preferences)
        self.lineEditBrokerIP.setGeometry(QtCore.QRect(120, 20, 113, 20))
        self.lineEditBrokerIP.setText("")
        self.lineEditBrokerIP.setObjectName("lineEditBrokerIP")
        self.lineEditLogFilePath = QtWidgets.QLineEdit(Preferences)
        self.lineEditLogFilePath.setGeometry(QtCore.QRect(120, 110, 191, 20))
        self.lineEditLogFilePath.setText("")
        self.lineEditLogFilePath.setObjectName("lineEditLogFilePath")
        self.labelLogFilePath = QtWidgets.QLabel(Preferences)
        self.labelLogFilePath.setGeometry(QtCore.QRect(20, 110, 91, 16))
        self.labelLogFilePath.setObjectName("labelLogFilePath")
        self.labelLogFileName = QtWidgets.QLabel(Preferences)
        self.labelLogFileName.setGeometry(QtCore.QRect(20, 80, 91, 16))
        self.labelLogFileName.setObjectName("labelLogFileName")
        self.lineEditLogFileName = QtWidgets.QLineEdit(Preferences)
        self.lineEditLogFileName.setGeometry(QtCore.QRect(120, 80, 191, 20))
        self.lineEditLogFileName.setText("")
        self.lineEditLogFileName.setObjectName("lineEditLogFileName")
        self.labelDataLoggingRad = QtWidgets.QLabel(Preferences)
        self.labelDataLoggingRad.setGeometry(QtCore.QRect(20, 47, 71, 16))
        self.labelDataLoggingRad.setObjectName("labelDataLoggingRad")
        self.radioButtonDataLogEnable = QtWidgets.QRadioButton(Preferences)
        self.radioButtonDataLogEnable.setGeometry(QtCore.QRect(120, 50, 82, 17))
        self.radioButtonDataLogEnable.setObjectName("radioButtonDataLogEnable")
        self.radioButtonDataLogDisable = QtWidgets.QRadioButton(Preferences)
        self.radioButtonDataLogDisable.setGeometry(QtCore.QRect(210, 50, 82, 17))
        self.radioButtonDataLogDisable.setChecked(True)
        self.radioButtonDataLogDisable.setObjectName("radioButtonDataLogDisable")
        self.toolButtonBrowseLogFilePath = QtWidgets.QToolButton(Preferences)
        self.toolButtonBrowseLogFilePath.setGeometry(QtCore.QRect(318, 110, 25, 19))
        self.toolButtonBrowseLogFilePath.setObjectName("toolButtonBrowseLogFilePath")
        self.lineEditBrokerPort = QtWidgets.QLineEdit(Preferences)
        self.lineEditBrokerPort.setGeometry(QtCore.QRect(290, 20, 51, 20))
        self.lineEditBrokerPort.setText("")
        self.lineEditBrokerPort.setObjectName("lineEditBrokerPort")
        self.labelBrokerPort = QtWidgets.QLabel(Preferences)
        self.labelBrokerPort.setGeometry(QtCore.QRect(260, 20, 21, 16))
        self.labelBrokerPort.setObjectName("labelBrokerPort")
        self.pushButtonSavePref = QtWidgets.QPushButton(Preferences)
        self.pushButtonSavePref.setGeometry(QtCore.QRect(180, 160, 75, 23))
        self.pushButtonSavePref.setObjectName("pushButtonSavePref")
        self.pushButtonExitPref = QtWidgets.QPushButton(Preferences)
        self.pushButtonExitPref.setGeometry(QtCore.QRect(270, 160, 75, 23))
        self.pushButtonExitPref.setObjectName("pushButtonExitPref")

        self.retranslateUi(Preferences)
        QtCore.QMetaObject.connectSlotsByName(Preferences)

    def retranslateUi(self, Preferences):
        _translate = QtCore.QCoreApplication.translate
        Preferences.setWindowTitle(_translate("Preferences", "Dialog"))
        self.labelBrokerIP.setText(_translate("Preferences", "MQTT Broker IP"))
        self.lineEditLogFilePath.setStatusTip(_translate("Preferences", "Log file name without extenshion"))
        self.labelLogFilePath.setText(_translate("Preferences", "Log File Path"))
        self.labelLogFileName.setText(_translate("Preferences", "Log File Name"))
        self.lineEditLogFileName.setStatusTip(_translate("Preferences", "Log file name without extenshion"))
        self.labelDataLoggingRad.setText(_translate("Preferences", "Data Logging"))
        self.radioButtonDataLogEnable.setText(_translate("Preferences", "Enable"))
        self.radioButtonDataLogDisable.setText(_translate("Preferences", "Disable"))
        self.toolButtonBrowseLogFilePath.setText(_translate("Preferences", "..."))
        self.labelBrokerPort.setText(_translate("Preferences", "Port"))
        self.pushButtonSavePref.setText(_translate("Preferences", "Save"))
        self.pushButtonExitPref.setText(_translate("Preferences", "Exit"))

