# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'meat_curing_UI.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MeatCuringChamberMW(object):
    def setupUi(self, MeatCuringChamberMW):
        MeatCuringChamberMW.setObjectName("MeatCuringChamberMW")
        MeatCuringChamberMW.setEnabled(True)
        MeatCuringChamberMW.resize(780, 406)
        MeatCuringChamberMW.setAutoFillBackground(False)
        MeatCuringChamberMW.setInputMethodHints(QtCore.Qt.ImhNone)
        MeatCuringChamberMW.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MeatCuringChamberMW.setAnimated(False)
        self.centralwidget = QtWidgets.QWidget(MeatCuringChamberMW)
        self.centralwidget.setObjectName("centralwidget")
        self.lcdNumberSetTmpVal = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumberSetTmpVal.setGeometry(QtCore.QRect(210, 190, 121, 41))
        self.lcdNumberSetTmpVal.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lcdNumberSetTmpVal.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumberSetTmpVal.setObjectName("lcdNumberSetTmpVal")
        self.lcdNumberSetHumVal = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumberSetHumVal.setGeometry(QtCore.QRect(370, 190, 121, 41))
        self.lcdNumberSetHumVal.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lcdNumberSetHumVal.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumberSetHumVal.setObjectName("lcdNumberSetHumVal")
        self.lcdNumberCurTmp = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumberCurTmp.setEnabled(True)
        self.lcdNumberCurTmp.setGeometry(QtCore.QRect(210, 100, 121, 41))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.lcdNumberCurTmp.setPalette(palette)
        self.lcdNumberCurTmp.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.lcdNumberCurTmp.setAutoFillBackground(False)
        self.lcdNumberCurTmp.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lcdNumberCurTmp.setSmallDecimalPoint(False)
        self.lcdNumberCurTmp.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumberCurTmp.setProperty("value", 0.0)
        self.lcdNumberCurTmp.setProperty("intValue", 0)
        self.lcdNumberCurTmp.setObjectName("lcdNumberCurTmp")
        self.lcdNumberCurHum = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumberCurHum.setGeometry(QtCore.QRect(370, 100, 121, 41))
        self.lcdNumberCurHum.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lcdNumberCurHum.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumberCurHum.setObjectName("lcdNumberCurHum")
        self.labelTmpNow = QtWidgets.QLabel(self.centralwidget)
        self.labelTmpNow.setGeometry(QtCore.QRect(210, 150, 121, 21))
        self.labelTmpNow.setObjectName("labelTmpNow")
        self.labelHumNow = QtWidgets.QLabel(self.centralwidget)
        self.labelHumNow.setGeometry(QtCore.QRect(370, 150, 121, 21))
        self.labelHumNow.setObjectName("labelHumNow")
        self.labelTmpSetVal = QtWidgets.QLabel(self.centralwidget)
        self.labelTmpSetVal.setGeometry(QtCore.QRect(210, 240, 121, 21))
        self.labelTmpSetVal.setObjectName("labelTmpSetVal")
        self.labelHumSetVal = QtWidgets.QLabel(self.centralwidget)
        self.labelHumSetVal.setGeometry(QtCore.QRect(370, 240, 121, 21))
        self.labelHumSetVal.setObjectName("labelHumSetVal")
        self.groupBoxTmpHumMonitor = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxTmpHumMonitor.setGeometry(QtCore.QRect(190, 80, 311, 201))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.LinkVisited, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.LinkVisited, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.LinkVisited, brush)
        self.groupBoxTmpHumMonitor.setPalette(palette)
        self.groupBoxTmpHumMonitor.setObjectName("groupBoxTmpHumMonitor")
        self.checkBoxFreezer = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxFreezer.setGeometry(QtCore.QRect(40, 100, 70, 17))
        self.checkBoxFreezer.setObjectName("checkBoxFreezer")
        self.checkBoxHumidifier = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxHumidifier.setGeometry(QtCore.QRect(40, 120, 70, 17))
        self.checkBoxHumidifier.setObjectName("checkBoxHumidifier")
        self.checkBoxHeater = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxHeater.setGeometry(QtCore.QRect(40, 160, 81, 17))
        self.checkBoxHeater.setObjectName("checkBoxHeater")
        self.checkBoxInternalFan = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxInternalFan.setGeometry(QtCore.QRect(40, 180, 91, 21))
        self.checkBoxInternalFan.setObjectName("checkBoxInternalFan")
        self.checkBoxDevice7 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxDevice7.setGeometry(QtCore.QRect(40, 220, 70, 17))
        self.checkBoxDevice7.setObjectName("checkBoxDevice7")
        self.checkBoxFreshAirFan = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxFreshAirFan.setGeometry(QtCore.QRect(40, 200, 81, 17))
        self.checkBoxFreshAirFan.setObjectName("checkBoxFreshAirFan")
        self.checkBoxDevice8 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxDevice8.setGeometry(QtCore.QRect(40, 240, 70, 17))
        self.checkBoxDevice8.setObjectName("checkBoxDevice8")
        self.groupBoxDeviceControl = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxDeviceControl.setGeometry(QtCore.QRect(20, 80, 151, 201))
        self.groupBoxDeviceControl.setCheckable(False)
        self.groupBoxDeviceControl.setObjectName("groupBoxDeviceControl")
        self.checkBoxDehumidifier = QtWidgets.QCheckBox(self.groupBoxDeviceControl)
        self.checkBoxDehumidifier.setGeometry(QtCore.QRect(20, 60, 91, 17))
        self.checkBoxDehumidifier.setObjectName("checkBoxDehumidifier")
        self.labelSetSetPointTmp = QtWidgets.QLabel(self.centralwidget)
        self.labelSetSetPointTmp.setGeometry(QtCore.QRect(20, 310, 81, 16))
        self.labelSetSetPointTmp.setObjectName("labelSetSetPointTmp")
        self.labelSetSetPointHum = QtWidgets.QLabel(self.centralwidget)
        self.labelSetSetPointHum.setGeometry(QtCore.QRect(180, 310, 61, 16))
        self.labelSetSetPointHum.setObjectName("labelSetSetPointHum")
        self.pushButtonSetSetpointApply = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSetSetpointApply.setGeometry(QtCore.QRect(340, 310, 61, 23))
        self.pushButtonSetSetpointApply.setObjectName("pushButtonSetSetpointApply")
        self.doubleSpinBoxSetSetPointTmp = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBoxSetSetPointTmp.setGeometry(QtCore.QRect(110, 310, 62, 22))
        self.doubleSpinBoxSetSetPointTmp.setMaximum(1000.0)
        self.doubleSpinBoxSetSetPointTmp.setObjectName("doubleSpinBoxSetSetPointTmp")
        self.doubleSpinBoxSetSetPointHum = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBoxSetSetPointHum.setGeometry(QtCore.QRect(250, 310, 62, 22))
        self.doubleSpinBoxSetSetPointHum.setObjectName("doubleSpinBoxSetSetPointHum")
        self.pushButtonExit = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonExit.setGeometry(QtCore.QRect(420, 310, 61, 23))
        self.pushButtonExit.setObjectName("pushButtonExit")
        self.lineEditBrokerPort = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditBrokerPort.setGeometry(QtCore.QRect(310, 29, 61, 20))
        self.lineEditBrokerPort.setText("")
        self.lineEditBrokerPort.setObjectName("lineEditBrokerPort")
        self.labelBrokerPort = QtWidgets.QLabel(self.centralwidget)
        self.labelBrokerPort.setGeometry(QtCore.QRect(277, 29, 21, 16))
        self.labelBrokerPort.setObjectName("labelBrokerPort")
        self.labelBrokerIP = QtWidgets.QLabel(self.centralwidget)
        self.labelBrokerIP.setGeometry(QtCore.QRect(33, 29, 81, 16))
        self.labelBrokerIP.setObjectName("labelBrokerIP")
        self.lineEditBrokerIP = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditBrokerIP.setGeometry(QtCore.QRect(123, 28, 131, 20))
        self.lineEditBrokerIP.setText("")
        self.lineEditBrokerIP.setObjectName("lineEditBrokerIP")
        self.pushButtonConnectBroker = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonConnectBroker.setGeometry(QtCore.QRect(391, 28, 81, 23))
        self.pushButtonConnectBroker.setObjectName("pushButtonConnectBroker")
        self.groupBoxDeviceStatus = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxDeviceStatus.setGeometry(QtCore.QRect(510, 10, 241, 161))
        self.groupBoxDeviceStatus.setCheckable(False)
        self.groupBoxDeviceStatus.setObjectName("groupBoxDeviceStatus")
        self.labelFreezerStatus = QtWidgets.QLabel(self.groupBoxDeviceStatus)
        self.labelFreezerStatus.setGeometry(QtCore.QRect(10, 20, 47, 13))
        self.labelFreezerStatus.setObjectName("labelFreezerStatus")
        self.labelHumidifierStatus = QtWidgets.QLabel(self.groupBoxDeviceStatus)
        self.labelHumidifierStatus.setGeometry(QtCore.QRect(10, 35, 51, 16))
        self.labelHumidifierStatus.setObjectName("labelHumidifierStatus")
        self.labelDehumidifierStatus = QtWidgets.QLabel(self.groupBoxDeviceStatus)
        self.labelDehumidifierStatus.setGeometry(QtCore.QRect(11, 52, 61, 16))
        self.labelDehumidifierStatus.setObjectName("labelDehumidifierStatus")
        self.labelInternalFanStatus = QtWidgets.QLabel(self.groupBoxDeviceStatus)
        self.labelInternalFanStatus.setGeometry(QtCore.QRect(11, 83, 71, 16))
        self.labelInternalFanStatus.setObjectName("labelInternalFanStatus")
        self.labelFreshAirFanStatus = QtWidgets.QLabel(self.groupBoxDeviceStatus)
        self.labelFreshAirFanStatus.setGeometry(QtCore.QRect(11, 101, 71, 16))
        self.labelFreshAirFanStatus.setObjectName("labelFreshAirFanStatus")
        self.labelHeaterSatus = QtWidgets.QLabel(self.groupBoxDeviceStatus)
        self.labelHeaterSatus.setGeometry(QtCore.QRect(11, 70, 47, 13))
        self.labelHeaterSatus.setObjectName("labelHeaterSatus")
        self.labelDevice7Status = QtWidgets.QLabel(self.groupBoxDeviceStatus)
        self.labelDevice7Status.setGeometry(QtCore.QRect(10, 118, 71, 16))
        self.labelDevice7Status.setObjectName("labelDevice7Status")
        self.labelDevice8Status = QtWidgets.QLabel(self.groupBoxDeviceStatus)
        self.labelDevice8Status.setGeometry(QtCore.QRect(10, 133, 71, 16))
        self.labelDevice8Status.setObjectName("labelDevice8Status")
        self.labellabelFreezerStatusValue = QtWidgets.QLabel(self.groupBoxDeviceStatus)
        self.labellabelFreezerStatusValue.setGeometry(QtCore.QRect(140, 20, 47, 13))
        self.labellabelFreezerStatusValue.setObjectName("labellabelFreezerStatusValue")
        self.labelHumidifierStatusValue = QtWidgets.QLabel(self.groupBoxDeviceStatus)
        self.labelHumidifierStatusValue.setGeometry(QtCore.QRect(140, 37, 47, 13))
        self.labelHumidifierStatusValue.setObjectName("labelHumidifierStatusValue")
        self.labelDehumidifierStatusValue = QtWidgets.QLabel(self.groupBoxDeviceStatus)
        self.labelDehumidifierStatusValue.setGeometry(QtCore.QRect(140, 54, 47, 13))
        self.labelDehumidifierStatusValue.setObjectName("labelDehumidifierStatusValue")
        self.labelHeaterSatusValue = QtWidgets.QLabel(self.groupBoxDeviceStatus)
        self.labelHeaterSatusValue.setGeometry(QtCore.QRect(140, 71, 47, 13))
        self.labelHeaterSatusValue.setObjectName("labelHeaterSatusValue")
        self.labelFreshAirFanStatusValue = QtWidgets.QLabel(self.groupBoxDeviceStatus)
        self.labelFreshAirFanStatusValue.setGeometry(QtCore.QRect(140, 104, 47, 13))
        self.labelFreshAirFanStatusValue.setObjectName("labelFreshAirFanStatusValue")
        self.labelDevice7StatusValue = QtWidgets.QLabel(self.groupBoxDeviceStatus)
        self.labelDevice7StatusValue.setGeometry(QtCore.QRect(140, 120, 47, 13))
        self.labelDevice7StatusValue.setObjectName("labelDevice7StatusValue")
        self.labelDevice8StatusValue = QtWidgets.QLabel(self.groupBoxDeviceStatus)
        self.labelDevice8StatusValue.setGeometry(QtCore.QRect(140, 135, 47, 13))
        self.labelDevice8StatusValue.setObjectName("labelDevice8StatusValue")
        self.labelInternalFanStatusValue = QtWidgets.QLabel(self.groupBoxDeviceStatus)
        self.labelInternalFanStatusValue.setGeometry(QtCore.QRect(140, 87, 47, 13))
        self.labelInternalFanStatusValue.setObjectName("labelInternalFanStatusValue")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 9, 481, 61))
        self.groupBox.setObjectName("groupBox")
        self.textBrowserDeviceStatus = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowserDeviceStatus.setGeometry(QtCore.QRect(510, 180, 241, 161))
        self.textBrowserDeviceStatus.setObjectName("textBrowserDeviceStatus")
        self.groupBox.raise_()
        self.groupBoxDeviceControl.raise_()
        self.groupBoxTmpHumMonitor.raise_()
        self.lcdNumberSetTmpVal.raise_()
        self.lcdNumberSetHumVal.raise_()
        self.lcdNumberCurTmp.raise_()
        self.lcdNumberCurHum.raise_()
        self.labelTmpNow.raise_()
        self.labelHumNow.raise_()
        self.labelTmpSetVal.raise_()
        self.labelHumSetVal.raise_()
        self.checkBoxFreezer.raise_()
        self.checkBoxHumidifier.raise_()
        self.checkBoxHeater.raise_()
        self.checkBoxInternalFan.raise_()
        self.checkBoxDevice7.raise_()
        self.checkBoxFreshAirFan.raise_()
        self.checkBoxDevice8.raise_()
        self.labelSetSetPointTmp.raise_()
        self.labelSetSetPointHum.raise_()
        self.pushButtonSetSetpointApply.raise_()
        self.doubleSpinBoxSetSetPointTmp.raise_()
        self.doubleSpinBoxSetSetPointHum.raise_()
        self.pushButtonExit.raise_()
        self.lineEditBrokerPort.raise_()
        self.labelBrokerPort.raise_()
        self.labelBrokerIP.raise_()
        self.lineEditBrokerIP.raise_()
        self.pushButtonConnectBroker.raise_()
        self.groupBoxDeviceStatus.raise_()
        self.textBrowserDeviceStatus.raise_()
        MeatCuringChamberMW.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MeatCuringChamberMW)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 780, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MeatCuringChamberMW.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MeatCuringChamberMW)
        self.statusbar.setObjectName("statusbar")
        MeatCuringChamberMW.setStatusBar(self.statusbar)
        self.actionPref = QtWidgets.QAction(MeatCuringChamberMW)
        self.actionPref.setObjectName("actionPref")
        self.actionAbout = QtWidgets.QAction(MeatCuringChamberMW)
        self.actionAbout.setObjectName("actionAbout")
        self.actionQuit = QtWidgets.QAction(MeatCuringChamberMW)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MeatCuringChamberMW)
        QtCore.QMetaObject.connectSlotsByName(MeatCuringChamberMW)

    def retranslateUi(self, MeatCuringChamberMW):
        _translate = QtCore.QCoreApplication.translate
        MeatCuringChamberMW.setWindowTitle(_translate("MeatCuringChamberMW", "MeatCuringChamber"))
        self.labelTmpNow.setText(_translate("MeatCuringChamberMW", "Current Temperature (C)"))
        self.labelHumNow.setText(_translate("MeatCuringChamberMW", "Current Humidity (RH)"))
        self.labelTmpSetVal.setText(_translate("MeatCuringChamberMW", "Temperature Set Point"))
        self.labelHumSetVal.setText(_translate("MeatCuringChamberMW", "Humidity Set Point"))
        self.groupBoxTmpHumMonitor.setTitle(_translate("MeatCuringChamberMW", "Temperature and Humidity monitor"))
        self.checkBoxFreezer.setText(_translate("MeatCuringChamberMW", "Freezer"))
        self.checkBoxHumidifier.setText(_translate("MeatCuringChamberMW", "Humidifier"))
        self.checkBoxHeater.setText(_translate("MeatCuringChamberMW", "Heater"))
        self.checkBoxInternalFan.setText(_translate("MeatCuringChamberMW", "Internal fan"))
        self.checkBoxDevice7.setText(_translate("MeatCuringChamberMW", "Device 7"))
        self.checkBoxFreshAirFan.setText(_translate("MeatCuringChamberMW", "Fresh air fan"))
        self.checkBoxDevice8.setText(_translate("MeatCuringChamberMW", "Device 8"))
        self.groupBoxDeviceControl.setTitle(_translate("MeatCuringChamberMW", "Device Control"))
        self.checkBoxDehumidifier.setText(_translate("MeatCuringChamberMW", "Dehumidifier"))
        self.labelSetSetPointTmp.setText(_translate("MeatCuringChamberMW", "Set Temperature"))
        self.labelSetSetPointHum.setText(_translate("MeatCuringChamberMW", "Set Humidity"))
        self.pushButtonSetSetpointApply.setText(_translate("MeatCuringChamberMW", "Apply"))
        self.pushButtonExit.setText(_translate("MeatCuringChamberMW", "Exit"))
        self.labelBrokerPort.setText(_translate("MeatCuringChamberMW", "Port"))
        self.labelBrokerIP.setText(_translate("MeatCuringChamberMW", "MQTT Broker IP"))
        self.pushButtonConnectBroker.setText(_translate("MeatCuringChamberMW", "Connect"))
        self.groupBoxDeviceStatus.setTitle(_translate("MeatCuringChamberMW", "Device Status"))
        self.labelFreezerStatus.setText(_translate("MeatCuringChamberMW", "Freezer"))
        self.labelHumidifierStatus.setText(_translate("MeatCuringChamberMW", "Humidifier"))
        self.labelDehumidifierStatus.setText(_translate("MeatCuringChamberMW", "Dehumidifier"))
        self.labelInternalFanStatus.setText(_translate("MeatCuringChamberMW", "Internal fan"))
        self.labelFreshAirFanStatus.setText(_translate("MeatCuringChamberMW", "Fresh air fan"))
        self.labelHeaterSatus.setText(_translate("MeatCuringChamberMW", "Heater"))
        self.labelDevice7Status.setText(_translate("MeatCuringChamberMW", "Device 7"))
        self.labelDevice8Status.setText(_translate("MeatCuringChamberMW", "Device 8"))
        self.labellabelFreezerStatusValue.setText(_translate("MeatCuringChamberMW", "OFF"))
        self.labelHumidifierStatusValue.setText(_translate("MeatCuringChamberMW", "OFF"))
        self.labelDehumidifierStatusValue.setText(_translate("MeatCuringChamberMW", "OFF"))
        self.labelHeaterSatusValue.setText(_translate("MeatCuringChamberMW", "OFF"))
        self.labelFreshAirFanStatusValue.setText(_translate("MeatCuringChamberMW", "OFF"))
        self.labelDevice7StatusValue.setText(_translate("MeatCuringChamberMW", "OFF"))
        self.labelDevice8StatusValue.setText(_translate("MeatCuringChamberMW", "OFF"))
        self.labelInternalFanStatusValue.setText(_translate("MeatCuringChamberMW", "OFF"))
        self.groupBox.setTitle(_translate("MeatCuringChamberMW", "MQTT Setup"))
        self.textBrowserDeviceStatus.setHtml(_translate("MeatCuringChamberMW", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.menuFile.setTitle(_translate("MeatCuringChamberMW", "File"))
        self.menuHelp.setTitle(_translate("MeatCuringChamberMW", "Help"))
        self.actionPref.setText(_translate("MeatCuringChamberMW", "Preference"))
        self.actionAbout.setText(_translate("MeatCuringChamberMW", "About"))
        self.actionQuit.setText(_translate("MeatCuringChamberMW", "Quit"))
