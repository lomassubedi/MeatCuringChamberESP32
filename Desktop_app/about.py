# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about_dialogue.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_About(object):
    def setupUi(self, About):
        About.setObjectName("About")
        About.resize(252, 166)
        self.label = QtWidgets.QLabel(About)
        self.label.setGeometry(QtCore.QRect(10, 10, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(About)
        self.label_2.setGeometry(QtCore.QRect(80, 50, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(About)
        self.label_3.setGeometry(QtCore.QRect(50, 100, 141, 51))
        self.label_3.setObjectName("label_3")

        self.retranslateUi(About)
        QtCore.QMetaObject.connectSlotsByName(About)

    def retranslateUi(self, About):
        _translate = QtCore.QCoreApplication.translate
        About.setWindowTitle(_translate("About", "About"))
        self.label.setText(_translate("About", "Meat Curing Chamber Controller"))
        self.label_2.setText(_translate("About", "V 1.0.0"))
        self.label_3.setText(_translate("About", "Copyright: Kyle Schaub\n"
" Developed by Lomas"))
