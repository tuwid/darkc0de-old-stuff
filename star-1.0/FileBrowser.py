# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FileBrowser.ui'
#
# Created: Sun Dec 21 00:08:35 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FileBrowser(object):
    def setupUi(self, FileBrowser):
        FileBrowser.setObjectName("FileBrowser")
        FileBrowser.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(FileBrowser)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtGui.QSplitter(FileBrowser)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.treeView = QtGui.QTreeView(self.splitter)
        self.treeView.setObjectName("treeView")
        self.buttonBox = QtGui.QDialogButtonBox(self.splitter)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(FileBrowser)
        QtCore.QMetaObject.connectSlotsByName(FileBrowser)

    def retranslateUi(self, FileBrowser):
        FileBrowser.setWindowTitle(QtGui.QApplication.translate("FileBrowser", "Select a File", None, QtGui.QApplication.UnicodeUTF8))

