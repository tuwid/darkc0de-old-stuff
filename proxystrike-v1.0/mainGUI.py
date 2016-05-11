# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainform.ui'
#
# Created: Tue Mar 25 18:22:06 2008
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class mainGUI(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,856,786).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.hboxlayout = QtGui.QHBoxLayout(self.centralwidget)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(9)
        self.hboxlayout.setObjectName("hboxlayout")

        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.tab)
        self.hboxlayout1.setMargin(1)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.stackedWidget = QtGui.QStackedWidget(self.tab)
        self.stackedWidget.setObjectName("stackedWidget")

        self.page = QtGui.QWidget()
        self.page.setObjectName("page")

        self.vboxlayout = QtGui.QVBoxLayout(self.page)
        self.vboxlayout.setMargin(1)
        self.vboxlayout.setObjectName("vboxlayout")

        self.splitter = QtGui.QSplitter(self.page)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")

        self.tableWidget = QtGui.QTableWidget(self.splitter)
        self.tableWidget.setAutoScroll(False)
        self.tableWidget.setTabKeyNavigation(True)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setObjectName("tableWidget")

        self.groupBox = QtGui.QGroupBox(self.splitter)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215,160))
        self.groupBox.setObjectName("groupBox")

        self.hboxlayout2 = QtGui.QHBoxLayout(self.groupBox)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setMargin(9)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setSpacing(6)
        self.hboxlayout3.setMargin(0)
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.radioButton = QtGui.QRadioButton(self.groupBox)
        self.radioButton.setObjectName("radioButton")
        self.hboxlayout3.addWidget(self.radioButton)

        self.radioButton_2 = QtGui.QRadioButton(self.groupBox)
        self.radioButton_2.setObjectName("radioButton_2")
        self.hboxlayout3.addWidget(self.radioButton_2)

        self.radioButton_3 = QtGui.QRadioButton(self.groupBox)
        self.radioButton_3.setChecked(True)
        self.radioButton_3.setObjectName("radioButton_3")
        self.hboxlayout3.addWidget(self.radioButton_3)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout3.addItem(spacerItem)
        self.vboxlayout1.addLayout(self.hboxlayout3)

        self.hboxlayout4 = QtGui.QHBoxLayout()
        self.hboxlayout4.setSpacing(6)
        self.hboxlayout4.setMargin(0)
        self.hboxlayout4.setObjectName("hboxlayout4")

        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.hboxlayout4.addWidget(self.label)

        self.comboBox = QtGui.QComboBox(self.groupBox)
        self.comboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.comboBox.setObjectName("comboBox")
        self.hboxlayout4.addWidget(self.comboBox)

        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout4.addItem(spacerItem1)
        self.vboxlayout1.addLayout(self.hboxlayout4)

        self.hboxlayout5 = QtGui.QHBoxLayout()
        self.hboxlayout5.setSpacing(6)
        self.hboxlayout5.setMargin(0)
        self.hboxlayout5.setObjectName("hboxlayout5")

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.hboxlayout5.addWidget(self.label_2)

        self.comboBox_2 = QtGui.QComboBox(self.groupBox)
        self.comboBox_2.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.comboBox_2.setObjectName("comboBox_2")
        self.hboxlayout5.addWidget(self.comboBox_2)

        spacerItem2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout5.addItem(spacerItem2)
        self.vboxlayout1.addLayout(self.hboxlayout5)

        self.hboxlayout6 = QtGui.QHBoxLayout()
        self.hboxlayout6.setSpacing(6)
        self.hboxlayout6.setMargin(0)
        self.hboxlayout6.setObjectName("hboxlayout6")

        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.hboxlayout6.addWidget(self.label_3)

        self.comboBox_3 = QtGui.QComboBox(self.groupBox)
        self.comboBox_3.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.comboBox_3.setObjectName("comboBox_3")
        self.hboxlayout6.addWidget(self.comboBox_3)

        spacerItem3 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout6.addItem(spacerItem3)
        self.vboxlayout1.addLayout(self.hboxlayout6)
        self.hboxlayout2.addLayout(self.vboxlayout1)

        self.line = QtGui.QFrame(self.groupBox)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.hboxlayout2.addWidget(self.line)

        spacerItem4 = QtGui.QSpacerItem(71,22,QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem4)

        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setMargin(0)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.deleteSelectedButton = QtGui.QPushButton(self.groupBox)
        self.deleteSelectedButton.setObjectName("deleteSelectedButton")
        self.vboxlayout2.addWidget(self.deleteSelectedButton)

        self.deleteInViewButton = QtGui.QPushButton(self.groupBox)
        self.deleteInViewButton.setObjectName("deleteInViewButton")
        self.vboxlayout2.addWidget(self.deleteInViewButton)

        self.editRequestsButton = QtGui.QPushButton(self.groupBox)
        self.editRequestsButton.setObjectName("editRequestsButton")
        self.vboxlayout2.addWidget(self.editRequestsButton)

        spacerItem5 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout2.addItem(spacerItem5)
        self.hboxlayout2.addLayout(self.vboxlayout2)

        self.tabResponse = QtGui.QTabWidget(self.splitter)
        self.tabResponse.setTabPosition(QtGui.QTabWidget.West)
        self.tabResponse.setObjectName("tabResponse")

        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.gridlayout = QtGui.QGridLayout(self.tab_3)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.requestEdit = QtGui.QTextEdit(self.tab_3)
        self.requestEdit.setReadOnly(True)
        self.requestEdit.setObjectName("requestEdit")
        self.gridlayout.addWidget(self.requestEdit,0,0,1,1)
        self.tabResponse.addTab(self.tab_3,"")

        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")

        self.gridlayout1 = QtGui.QGridLayout(self.tab_4)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.responseEdit = QtGui.QTextEdit(self.tab_4)
        self.responseEdit.setReadOnly(True)
        self.responseEdit.setObjectName("responseEdit")
        self.gridlayout1.addWidget(self.responseEdit,0,0,1,1)
        self.tabResponse.addTab(self.tab_4,"")

        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName("tab_5")

        self.hboxlayout7 = QtGui.QHBoxLayout(self.tab_5)
        self.hboxlayout7.setSpacing(6)
        self.hboxlayout7.setMargin(9)
        self.hboxlayout7.setObjectName("hboxlayout7")

        self.tableWidget_2 = QtGui.QTableWidget(self.tab_5)
        self.tableWidget_2.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.tableWidget_2.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.hboxlayout7.addWidget(self.tableWidget_2)

        spacerItem6 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout7.addItem(spacerItem6)
        self.tabResponse.addTab(self.tab_5,"")
        self.vboxlayout.addWidget(self.splitter)
        self.stackedWidget.addWidget(self.page)

        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName("page_2")

        self.vboxlayout3 = QtGui.QVBoxLayout(self.page_2)
        self.vboxlayout3.setSpacing(6)
        self.vboxlayout3.setMargin(9)
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.groupBox_2 = QtGui.QGroupBox(self.page_2)
        self.groupBox_2.setObjectName("groupBox_2")

        self.hboxlayout8 = QtGui.QHBoxLayout(self.groupBox_2)
        self.hboxlayout8.setSpacing(6)
        self.hboxlayout8.setMargin(9)
        self.hboxlayout8.setObjectName("hboxlayout8")

        self.cookieEdit = QtGui.QLineEdit(self.groupBox_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cookieEdit.sizePolicy().hasHeightForWidth())
        self.cookieEdit.setSizePolicy(sizePolicy)
        self.cookieEdit.setObjectName("cookieEdit")
        self.hboxlayout8.addWidget(self.cookieEdit)

        self.setCookieButton = QtGui.QPushButton(self.groupBox_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setCookieButton.sizePolicy().hasHeightForWidth())
        self.setCookieButton.setSizePolicy(sizePolicy)
        self.setCookieButton.setObjectName("setCookieButton")
        self.hboxlayout8.addWidget(self.setCookieButton)
        self.vboxlayout3.addWidget(self.groupBox_2)

        self.groupBox_3 = QtGui.QGroupBox(self.page_2)
        self.groupBox_3.setObjectName("groupBox_3")

        self.vboxlayout4 = QtGui.QVBoxLayout(self.groupBox_3)
        self.vboxlayout4.setSpacing(6)
        self.vboxlayout4.setMargin(9)
        self.vboxlayout4.setObjectName("vboxlayout4")

        self.hboxlayout9 = QtGui.QHBoxLayout()
        self.hboxlayout9.setSpacing(6)
        self.hboxlayout9.setMargin(0)
        self.hboxlayout9.setObjectName("hboxlayout9")

        self.label_4 = QtGui.QLabel(self.groupBox_3)
        self.label_4.setObjectName("label_4")
        self.hboxlayout9.addWidget(self.label_4)

        self.substSrcEdit = QtGui.QLineEdit(self.groupBox_3)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.substSrcEdit.sizePolicy().hasHeightForWidth())
        self.substSrcEdit.setSizePolicy(sizePolicy)
        self.substSrcEdit.setObjectName("substSrcEdit")
        self.hboxlayout9.addWidget(self.substSrcEdit)
        self.vboxlayout4.addLayout(self.hboxlayout9)

        self.hboxlayout10 = QtGui.QHBoxLayout()
        self.hboxlayout10.setSpacing(6)
        self.hboxlayout10.setMargin(0)
        self.hboxlayout10.setObjectName("hboxlayout10")

        self.label_5 = QtGui.QLabel(self.groupBox_3)
        self.label_5.setObjectName("label_5")
        self.hboxlayout10.addWidget(self.label_5)

        self.substDstEdit = QtGui.QLineEdit(self.groupBox_3)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.substDstEdit.sizePolicy().hasHeightForWidth())
        self.substDstEdit.setSizePolicy(sizePolicy)
        self.substDstEdit.setObjectName("substDstEdit")
        self.hboxlayout10.addWidget(self.substDstEdit)
        self.vboxlayout4.addLayout(self.hboxlayout10)

        self.hboxlayout11 = QtGui.QHBoxLayout()
        self.hboxlayout11.setSpacing(6)
        self.hboxlayout11.setMargin(0)
        self.hboxlayout11.setObjectName("hboxlayout11")

        spacerItem7 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout11.addItem(spacerItem7)

        self.substButton = QtGui.QPushButton(self.groupBox_3)
        self.substButton.setObjectName("substButton")
        self.hboxlayout11.addWidget(self.substButton)
        self.vboxlayout4.addLayout(self.hboxlayout11)
        self.vboxlayout3.addWidget(self.groupBox_3)

        spacerItem8 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout3.addItem(spacerItem8)

        self.hboxlayout12 = QtGui.QHBoxLayout()
        self.hboxlayout12.setSpacing(6)
        self.hboxlayout12.setMargin(0)
        self.hboxlayout12.setObjectName("hboxlayout12")

        spacerItem9 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout12.addItem(spacerItem9)

        self.doneButton = QtGui.QPushButton(self.page_2)
        self.doneButton.setObjectName("doneButton")
        self.hboxlayout12.addWidget(self.doneButton)
        self.vboxlayout3.addLayout(self.hboxlayout12)
        self.stackedWidget.addWidget(self.page_2)
        self.hboxlayout1.addWidget(self.stackedWidget)
        self.tabWidget.addTab(self.tab,"")

        self.tab_6 = QtGui.QWidget()
        self.tab_6.setObjectName("tab_6")

        self.vboxlayout5 = QtGui.QVBoxLayout(self.tab_6)
        self.vboxlayout5.setSpacing(6)
        self.vboxlayout5.setMargin(9)
        self.vboxlayout5.setObjectName("vboxlayout5")

        self.reqStatsTreeWidget = QtGui.QTreeWidget(self.tab_6)
        self.reqStatsTreeWidget.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.reqStatsTreeWidget.setObjectName("reqStatsTreeWidget")
        self.vboxlayout5.addWidget(self.reqStatsTreeWidget)

        self.hboxlayout13 = QtGui.QHBoxLayout()
        self.hboxlayout13.setSpacing(6)
        self.hboxlayout13.setMargin(0)
        self.hboxlayout13.setObjectName("hboxlayout13")

        self.updateReqStatsButton = QtGui.QPushButton(self.tab_6)
        self.updateReqStatsButton.setObjectName("updateReqStatsButton")
        self.hboxlayout13.addWidget(self.updateReqStatsButton)

        spacerItem10 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout13.addItem(spacerItem10)
        self.vboxlayout5.addLayout(self.hboxlayout13)
        self.tabWidget.addTab(self.tab_6,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.vboxlayout6 = QtGui.QVBoxLayout(self.tab_2)
        self.vboxlayout6.setSpacing(6)
        self.vboxlayout6.setMargin(9)
        self.vboxlayout6.setObjectName("vboxlayout6")

        self.varStatsTreeWidget = QtGui.QTreeWidget(self.tab_2)
        self.varStatsTreeWidget.setAlternatingRowColors(True)
        self.varStatsTreeWidget.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.varStatsTreeWidget.setIndentation(30)
        self.varStatsTreeWidget.setObjectName("varStatsTreeWidget")
        self.vboxlayout6.addWidget(self.varStatsTreeWidget)

        self.hboxlayout14 = QtGui.QHBoxLayout()
        self.hboxlayout14.setSpacing(6)
        self.hboxlayout14.setMargin(0)
        self.hboxlayout14.setObjectName("hboxlayout14")

        self.updateVarStatsButton = QtGui.QPushButton(self.tab_2)
        self.updateVarStatsButton.setObjectName("updateVarStatsButton")
        self.hboxlayout14.addWidget(self.updateVarStatsButton)

        spacerItem11 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout14.addItem(spacerItem11)
        self.vboxlayout6.addLayout(self.hboxlayout14)
        self.tabWidget.addTab(self.tab_2,"")

        self.tab_7 = QtGui.QWidget()
        self.tab_7.setObjectName("tab_7")

        self.vboxlayout7 = QtGui.QVBoxLayout(self.tab_7)
        self.vboxlayout7.setObjectName("vboxlayout7")

        self.groupBox_4 = QtGui.QGroupBox(self.tab_7)
        self.groupBox_4.setObjectName("groupBox_4")

        self.vboxlayout8 = QtGui.QVBoxLayout(self.groupBox_4)
        self.vboxlayout8.setObjectName("vboxlayout8")

        self.label_16 = QtGui.QLabel(self.groupBox_4)
        self.label_16.setObjectName("label_16")
        self.vboxlayout8.addWidget(self.label_16)

        self.hboxlayout15 = QtGui.QHBoxLayout()
        self.hboxlayout15.setObjectName("hboxlayout15")

        self.label_6 = QtGui.QLabel(self.groupBox_4)
        self.label_6.setObjectName("label_6")
        self.hboxlayout15.addWidget(self.label_6)

        self.getsignEdit = QtGui.QLineEdit(self.groupBox_4)
        self.getsignEdit.setObjectName("getsignEdit")
        self.hboxlayout15.addWidget(self.getsignEdit)
        self.vboxlayout8.addLayout(self.hboxlayout15)

        self.label_17 = QtGui.QLabel(self.groupBox_4)
        self.label_17.setObjectName("label_17")
        self.vboxlayout8.addWidget(self.label_17)

        self.hboxlayout16 = QtGui.QHBoxLayout()
        self.hboxlayout16.setObjectName("hboxlayout16")

        self.label_8 = QtGui.QLabel(self.groupBox_4)
        self.label_8.setObjectName("label_8")
        self.hboxlayout16.addWidget(self.label_8)

        self.headersignEdit = QtGui.QLineEdit(self.groupBox_4)
        self.headersignEdit.setObjectName("headersignEdit")
        self.hboxlayout16.addWidget(self.headersignEdit)

        self.label_7 = QtGui.QLabel(self.groupBox_4)
        self.label_7.setObjectName("label_7")
        self.hboxlayout16.addWidget(self.label_7)

        self.valuesignEdit = QtGui.QLineEdit(self.groupBox_4)
        self.valuesignEdit.setObjectName("valuesignEdit")
        self.hboxlayout16.addWidget(self.valuesignEdit)
        self.vboxlayout8.addLayout(self.hboxlayout16)
        self.vboxlayout7.addWidget(self.groupBox_4)

        self.groupBox_5 = QtGui.QGroupBox(self.tab_7)
        self.groupBox_5.setObjectName("groupBox_5")

        self.vboxlayout9 = QtGui.QVBoxLayout(self.groupBox_5)
        self.vboxlayout9.setObjectName("vboxlayout9")

        self.label_9 = QtGui.QLabel(self.groupBox_5)
        self.label_9.setObjectName("label_9")
        self.vboxlayout9.addWidget(self.label_9)

        self.label_15 = QtGui.QLabel(self.groupBox_5)
        self.label_15.setObjectName("label_15")
        self.vboxlayout9.addWidget(self.label_15)

        self.pathlimitEdit = QtGui.QLineEdit(self.groupBox_5)
        self.pathlimitEdit.setObjectName("pathlimitEdit")
        self.vboxlayout9.addWidget(self.pathlimitEdit)
        self.vboxlayout7.addWidget(self.groupBox_5)

        self.groupBox_6 = QtGui.QGroupBox(self.tab_7)
        self.groupBox_6.setObjectName("groupBox_6")

        self.vboxlayout10 = QtGui.QVBoxLayout(self.groupBox_6)
        self.vboxlayout10.setObjectName("vboxlayout10")

        self.label_10 = QtGui.QLabel(self.groupBox_6)
        self.label_10.setObjectName("label_10")
        self.vboxlayout10.addWidget(self.label_10)

        self.proxyEdit = QtGui.QLineEdit(self.groupBox_6)
        self.proxyEdit.setObjectName("proxyEdit")
        self.vboxlayout10.addWidget(self.proxyEdit)
        self.vboxlayout7.addWidget(self.groupBox_6)

        self.groupBox_7 = QtGui.QGroupBox(self.tab_7)
        self.groupBox_7.setObjectName("groupBox_7")

        self.hboxlayout17 = QtGui.QHBoxLayout(self.groupBox_7)
        self.hboxlayout17.setObjectName("hboxlayout17")

        self.label_18 = QtGui.QLabel(self.groupBox_7)
        self.label_18.setObjectName("label_18")
        self.hboxlayout17.addWidget(self.label_18)

        self.portSpin = QtGui.QSpinBox(self.groupBox_7)
        self.portSpin.setMinimum(1)
        self.portSpin.setMaximum(65535)
        self.portSpin.setProperty("value",QtCore.QVariant(8008))
        self.portSpin.setObjectName("portSpin")
        self.hboxlayout17.addWidget(self.portSpin)

        spacerItem12 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout17.addItem(spacerItem12)
        self.vboxlayout7.addWidget(self.groupBox_7)

        spacerItem13 = QtGui.QSpacerItem(816,131,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout7.addItem(spacerItem13)

        self.hboxlayout18 = QtGui.QHBoxLayout()
        self.hboxlayout18.setObjectName("hboxlayout18")

        spacerItem14 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout18.addItem(spacerItem14)

        self.configApplyButton = QtGui.QPushButton(self.tab_7)
        self.configApplyButton.setObjectName("configApplyButton")
        self.hboxlayout18.addWidget(self.configApplyButton)
        self.vboxlayout7.addLayout(self.hboxlayout18)
        self.tabWidget.addTab(self.tab_7,"")

        self.tab_8 = QtGui.QWidget()
        self.tab_8.setObjectName("tab_8")

        self.vboxlayout11 = QtGui.QVBoxLayout(self.tab_8)
        self.vboxlayout11.setSpacing(0)
        self.vboxlayout11.setMargin(0)
        self.vboxlayout11.setObjectName("vboxlayout11")

        self.hboxlayout19 = QtGui.QHBoxLayout()
        self.hboxlayout19.setSpacing(-1)
        self.hboxlayout19.setObjectName("hboxlayout19")

        self.label_11 = QtGui.QLabel(self.tab_8)
        self.label_11.setObjectName("label_11")
        self.hboxlayout19.addWidget(self.label_11)

        self.attackRequestThreadsSpin = QtGui.QSpinBox(self.tab_8)
        self.attackRequestThreadsSpin.setMinimum(1)
        self.attackRequestThreadsSpin.setMaximum(20)
        self.attackRequestThreadsSpin.setObjectName("attackRequestThreadsSpin")
        self.hboxlayout19.addWidget(self.attackRequestThreadsSpin)

        self.label_12 = QtGui.QLabel(self.tab_8)
        self.label_12.setObjectName("label_12")
        self.hboxlayout19.addWidget(self.label_12)

        self.attackParamThreadsSpin = QtGui.QSpinBox(self.tab_8)
        self.attackParamThreadsSpin.setEnabled(False)
        self.attackParamThreadsSpin.setMinimum(1)
        self.attackParamThreadsSpin.setMaximum(20)
        self.attackParamThreadsSpin.setObjectName("attackParamThreadsSpin")
        self.hboxlayout19.addWidget(self.attackParamThreadsSpin)

        spacerItem15 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout19.addItem(spacerItem15)

        self.resetAttackButton = QtGui.QPushButton(self.tab_8)
        self.resetAttackButton.setObjectName("resetAttackButton")
        self.hboxlayout19.addWidget(self.resetAttackButton)
        self.vboxlayout11.addLayout(self.hboxlayout19)

        self.splitter_2 = QtGui.QSplitter(self.tab_8)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setHandleWidth(7)
        self.splitter_2.setObjectName("splitter_2")

        self.layoutWidget = QtGui.QWidget(self.splitter_2)
        self.layoutWidget.setObjectName("layoutWidget")

        self.vboxlayout12 = QtGui.QVBoxLayout(self.layoutWidget)
        self.vboxlayout12.setObjectName("vboxlayout12")

        self.hboxlayout20 = QtGui.QHBoxLayout()
        self.hboxlayout20.setObjectName("hboxlayout20")

        self.label_13 = QtGui.QLabel(self.layoutWidget)
        self.label_13.setObjectName("label_13")
        self.hboxlayout20.addWidget(self.label_13)

        self.enableXSSCheck = QtGui.QCheckBox(self.layoutWidget)
        self.enableXSSCheck.setObjectName("enableXSSCheck")
        self.hboxlayout20.addWidget(self.enableXSSCheck)

        spacerItem16 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout20.addItem(spacerItem16)

        self.xssToHTMLButton = QtGui.QPushButton(self.layoutWidget)
        self.xssToHTMLButton.setObjectName("xssToHTMLButton")
        self.hboxlayout20.addWidget(self.xssToHTMLButton)

        self.xssToXMLButton = QtGui.QPushButton(self.layoutWidget)
        self.xssToXMLButton.setObjectName("xssToXMLButton")
        self.hboxlayout20.addWidget(self.xssToXMLButton)
        self.vboxlayout12.addLayout(self.hboxlayout20)

        self.treeXss = QtGui.QTreeWidget(self.layoutWidget)
        self.treeXss.setAlternatingRowColors(True)
        self.treeXss.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.treeXss.setObjectName("treeXss")
        self.vboxlayout12.addWidget(self.treeXss)

        self.layoutWidget1 = QtGui.QWidget(self.splitter_2)
        self.layoutWidget1.setObjectName("layoutWidget1")

        self.vboxlayout13 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.vboxlayout13.setObjectName("vboxlayout13")

        self.hboxlayout21 = QtGui.QHBoxLayout()
        self.hboxlayout21.setObjectName("hboxlayout21")

        self.label_14 = QtGui.QLabel(self.layoutWidget1)
        self.label_14.setObjectName("label_14")
        self.hboxlayout21.addWidget(self.label_14)

        self.enableSQLCheck = QtGui.QCheckBox(self.layoutWidget1)
        self.enableSQLCheck.setObjectName("enableSQLCheck")
        self.hboxlayout21.addWidget(self.enableSQLCheck)

        spacerItem17 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout21.addItem(spacerItem17)

        self.sqlToHTMLButton = QtGui.QPushButton(self.layoutWidget1)
        self.sqlToHTMLButton.setObjectName("sqlToHTMLButton")
        self.hboxlayout21.addWidget(self.sqlToHTMLButton)

        self.sqlToXMLButton = QtGui.QPushButton(self.layoutWidget1)
        self.sqlToXMLButton.setObjectName("sqlToXMLButton")
        self.hboxlayout21.addWidget(self.sqlToXMLButton)
        self.vboxlayout13.addLayout(self.hboxlayout21)

        self.treeSql = QtGui.QTreeWidget(self.layoutWidget1)
        self.treeSql.setAlternatingRowColors(True)
        self.treeSql.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.treeSql.setObjectName("treeSql")
        self.vboxlayout13.addWidget(self.treeSql)
        self.vboxlayout11.addWidget(self.splitter_2)
        self.tabWidget.addTab(self.tab_8,"")
        self.hboxlayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,856,29))
        self.menubar.setObjectName("menubar")

        self.menuHjlk = QtGui.QMenu(self.menubar)
        self.menuHjlk.setObjectName("menuHjlk")

        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")

        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")

        self.actionOpen_2 = QtGui.QAction(MainWindow)
        self.actionOpen_2.setObjectName("actionOpen_2")

        self.actionExit_2 = QtGui.QAction(MainWindow)
        self.actionExit_2.setObjectName("actionExit_2")

        self.actionSave_session = QtGui.QAction(MainWindow)
        self.actionSave_session.setObjectName("actionSave_session")

        self.actionHelp = QtGui.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")

        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuHjlk.addSeparator()
#        self.menuHjlk.addAction(self.actionOpen_2)
#        self.menuHjlk.addAction(self.actionSave_session)
        self.menuHjlk.addAction(self.actionExit_2)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuHjlk.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "ProxyStrike v1.0", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)

        headerItem = QtGui.QTableWidgetItem()
        headerItem.setText(QtGui.QApplication.translate("MainWindow", "Method", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(0,headerItem)

        headerItem1 = QtGui.QTableWidgetItem()
        headerItem1.setText(QtGui.QApplication.translate("MainWindow", "Target", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(1,headerItem1)

        headerItem2 = QtGui.QTableWidgetItem()
        headerItem2.setText(QtGui.QApplication.translate("MainWindow", "Url", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(2,headerItem2)

        headerItem3 = QtGui.QTableWidgetItem()
        headerItem3.setText(QtGui.QApplication.translate("MainWindow", "Cookies", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(3,headerItem3)
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Select", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton.setText(QtGui.QApplication.translate("MainWindow", "Get", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_2.setText(QtGui.QApplication.translate("MainWindow", "Post", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_3.setText(QtGui.QApplication.translate("MainWindow", "All", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Target :", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(QtGui.QApplication.translate("MainWindow", "All", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Path :", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.addItem(QtGui.QApplication.translate("MainWindow", "All", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Variable: ", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_3.addItem(QtGui.QApplication.translate("MainWindow", "All", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteSelectedButton.setText(QtGui.QApplication.translate("MainWindow", "Delete selected requests", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteInViewButton.setText(QtGui.QApplication.translate("MainWindow", "Delete requests in view", None, QtGui.QApplication.UnicodeUTF8))
        self.editRequestsButton.setText(QtGui.QApplication.translate("MainWindow", "Edit requests in view", None, QtGui.QApplication.UnicodeUTF8))
        self.tabResponse.setTabText(self.tabResponse.indexOf(self.tab_3), QtGui.QApplication.translate("MainWindow", "Requests", None, QtGui.QApplication.UnicodeUTF8))
        self.tabResponse.setTabText(self.tabResponse.indexOf(self.tab_4), QtGui.QApplication.translate("MainWindow", "Responses", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget_2.clear()
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setRowCount(0)

        headerItem4 = QtGui.QTableWidgetItem()
        headerItem4.setText(QtGui.QApplication.translate("MainWindow", "Variable", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget_2.setHorizontalHeaderItem(0,headerItem4)

        headerItem5 = QtGui.QTableWidgetItem()
        headerItem5.setText(QtGui.QApplication.translate("MainWindow", "Value", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget_2.setHorizontalHeaderItem(1,headerItem5)
        self.tabResponse.setTabText(self.tabResponse.indexOf(self.tab_5), QtGui.QApplication.translate("MainWindow", "Variables", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This action, sets a new cookie for the </p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">visible requests in the requests table.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("MainWindow", "Set Cookie", None, QtGui.QApplication.UnicodeUTF8))
        self.setCookieButton.setText(QtGui.QApplication.translate("MainWindow", "Set cookie", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("MainWindow", "Regex request substitution", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Substitute:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "by:", None, QtGui.QApplication.UnicodeUTF8))
        self.substButton.setText(QtGui.QApplication.translate("MainWindow", "Substitute", None, QtGui.QApplication.UnicodeUTF8))
        self.doneButton.setText(QtGui.QApplication.translate("MainWindow", "Done", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Comms", None, QtGui.QApplication.UnicodeUTF8))
        self.reqStatsTreeWidget.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Request", None, QtGui.QApplication.UnicodeUTF8))
        self.reqStatsTreeWidget.headerItem().setText(1,QtGui.QApplication.translate("MainWindow", "Variable set", None, QtGui.QApplication.UnicodeUTF8))
        self.updateReqStatsButton.setText(QtGui.QApplication.translate("MainWindow", "Update stats", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), QtGui.QApplication.translate("MainWindow", "Request Stats", None, QtGui.QApplication.UnicodeUTF8))
        self.varStatsTreeWidget.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Variable", None, QtGui.QApplication.UnicodeUTF8))
        self.varStatsTreeWidget.headerItem().setText(1,QtGui.QApplication.translate("MainWindow", "Values", None, QtGui.QApplication.UnicodeUTF8))
        self.updateVarStatsButton.setText(QtGui.QApplication.translate("MainWindow", "Update stats", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "Variable Stats", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("MainWindow", "GET and HEADERS Sign", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("MainWindow", "Proxy Strike can append values to the url while you are browsing web pages.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Get (ex: &myvar=myval)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("MainWindow", "You can add or modify existing headers while browsing. Eg: User-agent: FakeBrowser", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "Header", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Value", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_5.setTitle(QtGui.QApplication.translate("MainWindow", "Path limit", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("MainWindow", "Proxy will allow acces only to paths matching the following pattern (regex):", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("MainWindow", "eg: /pages/page[0-9]{2}.html            (will only allow access to urls containing /pages/pageXX.html where XX are numbers)", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_6.setTitle(QtGui.QApplication.translate("MainWindow", "Use proxy", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("MainWindow", "Set proxy server (eg. localhost:8080)", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_7.setTitle(QtGui.QApplication.translate("MainWindow", "ProxyStrike listen port", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setText(QtGui.QApplication.translate("MainWindow", "Listen port", None, QtGui.QApplication.UnicodeUTF8))
        self.configApplyButton.setText(QtGui.QApplication.translate("MainWindow", "Apply", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), QtGui.QApplication.translate("MainWindow", "Config", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("MainWindow", "Request threads", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("MainWindow", "Parameter threads", None, QtGui.QApplication.UnicodeUTF8))
        self.resetAttackButton.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You will be able to attack the same url more than once.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.resetAttackButton.setText(QtGui.QApplication.translate("MainWindow", "Reset attacker cache", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("MainWindow", "Cross site scripting:", None, QtGui.QApplication.UnicodeUTF8))
        self.enableXSSCheck.setText(QtGui.QApplication.translate("MainWindow", "enable", None, QtGui.QApplication.UnicodeUTF8))
        self.xssToHTMLButton.setText(QtGui.QApplication.translate("MainWindow", "Export HTML", None, QtGui.QApplication.UnicodeUTF8))
        self.xssToXMLButton.setText(QtGui.QApplication.translate("MainWindow", "Export XML", None, QtGui.QApplication.UnicodeUTF8))
        self.treeXss.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Url", None, QtGui.QApplication.UnicodeUTF8))
        self.treeXss.headerItem().setText(1,QtGui.QApplication.translate("MainWindow", "Variable", None, QtGui.QApplication.UnicodeUTF8))
        self.treeXss.headerItem().setText(2,QtGui.QApplication.translate("MainWindow", "Method", None, QtGui.QApplication.UnicodeUTF8))
        self.treeXss.headerItem().setText(3,QtGui.QApplication.translate("MainWindow", "Injections Available", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("MainWindow", "Sql Injection:", None, QtGui.QApplication.UnicodeUTF8))
        self.enableSQLCheck.setText(QtGui.QApplication.translate("MainWindow", "enable", None, QtGui.QApplication.UnicodeUTF8))
        self.sqlToHTMLButton.setText(QtGui.QApplication.translate("MainWindow", "Export HTML", None, QtGui.QApplication.UnicodeUTF8))
        self.sqlToXMLButton.setText(QtGui.QApplication.translate("MainWindow", "Export XML", None, QtGui.QApplication.UnicodeUTF8))
        self.treeSql.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Url", None, QtGui.QApplication.UnicodeUTF8))
        self.treeSql.headerItem().setText(1,QtGui.QApplication.translate("MainWindow", "Variable", None, QtGui.QApplication.UnicodeUTF8))
        self.treeSql.headerItem().setText(2,QtGui.QApplication.translate("MainWindow", "Method", None, QtGui.QApplication.UnicodeUTF8))
        self.treeSql.headerItem().setText(3,QtGui.QApplication.translate("MainWindow", "Injection Type", None, QtGui.QApplication.UnicodeUTF8))
        self.treeSql.headerItem().setText(4,QtGui.QApplication.translate("MainWindow", "DB Fingerprint", None, QtGui.QApplication.UnicodeUTF8))
        self.treeSql.headerItem().setText(5,QtGui.QApplication.translate("MainWindow", "DB Error", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_8), QtGui.QApplication.translate("MainWindow", "Attacks", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHjlk.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_2.setText(QtGui.QApplication.translate("MainWindow", "Open session", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit_2.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_session.setText(QtGui.QApplication.translate("MainWindow", "Save session", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp.setText(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))

