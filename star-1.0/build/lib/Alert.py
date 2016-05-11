# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Alert.ui'
#
# Created: Tue Dec 23 05:45:23 2008
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Alert(object):
    def setupUi(self, Alert):
        Alert.setObjectName("Alert")
        Alert.resize(400, 93)
        self.verticalLayout = QtGui.QVBoxLayout(Alert)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.label = QtGui.QLabel(Alert)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtGui.QDialogButtonBox(Alert)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Alert)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Alert.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Alert.reject)
        QtCore.QMetaObject.connectSlotsByName(Alert)

    def retranslateUi(self, Alert):
        Alert.setWindowTitle(QtGui.QApplication.translate("Alert", "Alert", None, QtGui.QApplication.UnicodeUTF8))

