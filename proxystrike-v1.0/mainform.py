#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainform.ui'
#
# Created: Tue Aug 29 19:57:46 2006
#      by: PyQt4 UI code generator 4.0.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui
from Proxynet import *
from string import *
import cPickle as pickl
from mainGUI import *
import logging
import attacker
import urllib
from crllr import *

logging.basicConfig(level=logging.INFO,format='%(message)s')


class Ui_MainWindow(mainGUI):
	def __init__(self):

		self.targetSelect="All"
		self.pathSelect="All"
		self.variableSelect="All"
		self.timer = QtCore.QTimer()
		QtCore.QObject.connect(self.timer,QtCore.SIGNAL("timeout()"),self.timerFunc)
		self.timer.start(500)

		self.controller=Controller()


	def setupUi(self, MainWindow):
		mainGUI.setupUi(self,MainWindow)

		self.retranslateUi(MainWindow)
		
#		QtCore.QObject.connect(self.actionOpen_2, QtCore.SIGNAL("triggered()"), self.funcion_Open)
#		QtCore.QObject.connect(self.actionSave_session, QtCore.SIGNAL("triggered()"), self.funcion_Save)
		QtCore.QObject.connect(self.actionExit_2, QtCore.SIGNAL("triggered()"), self.salir)
		QtCore.QObject.connect(self.radioButton, QtCore.SIGNAL("clicked(bool)"), self.updateTable)
		QtCore.QObject.connect(self.radioButton_2, QtCore.SIGNAL("clicked(bool)"), self.updateTable)
		QtCore.QObject.connect(self.radioButton_3, QtCore.SIGNAL("clicked(bool)"), self.updateTable)
		QtCore.QObject.connect(self.comboBox, QtCore.SIGNAL("activated(QString)"), self.targetSelected)
		QtCore.QObject.connect(self.comboBox_2, QtCore.SIGNAL("activated(QString)"), self.pathSelected)
		QtCore.QObject.connect(self.comboBox_3, QtCore.SIGNAL("activated(QString)"), self.variableSelected)
		QtCore.QObject.connect(self.tableWidget, QtCore.SIGNAL("currentCellChanged(int,int,int,int)"), self.cambiaPeticion)
		QtCore.QObject.connect(self.varStatsTreeWidget, QtCore.SIGNAL("itemDoubleClicked(QTreeWidgetItem *,int)"), self.slotTree)
		QtCore.QObject.connect(self.updateVarStatsButton, QtCore.SIGNAL("clicked()"), self.updateVarStatsTree)
		QtCore.QObject.connect(self.updateReqStatsButton, QtCore.SIGNAL("clicked()"), self.updateReqStatsTree)
		QtCore.QObject.connect(self.deleteInViewButton, QtCore.SIGNAL("clicked()"), self.deleteInView)
		QtCore.QObject.connect(self.deleteSelectedButton, QtCore.SIGNAL("clicked()"), self.deleteSelected)
		QtCore.QObject.connect(self.editRequestsButton, QtCore.SIGNAL("clicked()"), self.toogleEditor)
		QtCore.QObject.connect(self.doneButton, QtCore.SIGNAL("clicked()"), self.toogleEditor)
		QtCore.QObject.connect(self.setCookieButton, QtCore.SIGNAL("clicked()"), self.setNewCookie)
		QtCore.QObject.connect(self.substButton, QtCore.SIGNAL("clicked()"), self.applyRegex)
		QtCore.QObject.connect(self.enableXSSCheck, QtCore.SIGNAL("stateChanged(int)"), self.xssToogled)
		QtCore.QObject.connect(self.enableSQLCheck, QtCore.SIGNAL("stateChanged(int)"), self.sqlToogled)
		QtCore.QObject.connect(self.sqlToXMLButton, QtCore.SIGNAL("clicked()"), self.exportSqlToXML)
		QtCore.QObject.connect(self.xssToXMLButton, QtCore.SIGNAL("clicked()"), self.exportXssToXML)
		QtCore.QObject.connect(self.sqlToHTMLButton, QtCore.SIGNAL("clicked()"), self.exportSqlToHTML)
		QtCore.QObject.connect(self.xssToHTMLButton, QtCore.SIGNAL("clicked()"), self.exportXssToHTML)
		QtCore.QObject.connect(self.resetAttackButton, QtCore.SIGNAL("clicked()"), self.controller.clearAttackerCache)
		QtCore.QObject.connect(self.attackRequestThreadsSpin, QtCore.SIGNAL("valueChanged(int)"), self.changeReqThreads)
		QtCore.QObject.connect(self.configApplyButton, QtCore.SIGNAL("clicked()"), self.applyConfig)
		QtCore.QObject.connect(self.actionAbout, QtCore.SIGNAL("triggered()"), self.funcion_About)
		
		QtCore.QMetaObject.connectSlotsByName(MainWindow)


####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################


	def funcion_Save(self):
		fileName = QtGui.QFileDialog.getSaveFileName()
		if len(fileName)>0:
			self.timer.stop()
			f = file(fileName, 'w')
			pickl.dump(self.requests, f)
			f.close()
			self.timer.start(500)
      
	def funcion_Open(self):
		fileName = QtGui.QFileDialog.getOpenFileName()
		if len(fileName)>0:
			self.timer.stop()
			self.variableStats={}
			self.reqStats={}
			self.limpiatablas()
			self.comboBox.clear()
			self.comboBox.addItem("All")
			self.comboBox_2.clear()
			self.comboBox_2.addItem("All")
			self.comboBox_3.clear()
			self.comboBox_3.addItem("All")
	
			Proxynet.clearRequests()

			f = file(fileName)
			Proxynet.addRequests(pickl.load(f))
			f.close()
			self.numRequests=0
			self.timerFunc()
	
			self.timer.start(500)


	def __getattr__(self,value):
		if value=="numRequests":
			return len(self.controller.getRequests())
		else:
			raise AttributeError

	def updateVarStatsTree(self):
		self.varStatsTreeWidget.clear()
		self.varStatsTreeWidget.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Variable", None, QtGui.QApplication.UnicodeUTF8))
		self.varStatsTreeWidget.headerItem().setText(1,QtGui.QApplication.translate("MainWindow", "Values", None, QtGui.QApplication.UnicodeUTF8))

		variableStats=self.controller.getVariableStats()
		sort1=variableStats.keys()
		sort1.sort()
		for tg in sort1:
			target=QtCore.QStringList()
			target.append(tg)
			targetTree=QtGui.QTreeWidgetItem(target)
			self.varStatsTreeWidget.addTopLevelItem(targetTree)
			sort2=variableStats[tg].keys()
			sort2.sort()
			for pt in sort2:
				path=QtCore.QStringList()
				path.append(pt)
				pathTree=QtGui.QTreeWidgetItem(path)
				pathTree.setTextColor(0,QtGui.QColor(0,0,200))
				font=pathTree.font(0)
				font.setBold(True)
				pathTree.setFont(0,font)
				targetTree.addChild(pathTree)
				sort3=variableStats[tg][pt].keys()
				sort3.sort()
				for vr in sort3:
					variable=QtCore.QStringList()
					variable.append(vr)
					values=""					
					for vls in variableStats[tg][pt][vr].keys():
						values+=urllib.unquote(vls)+"\n"
					variable.append(values)
					variableTree=QtGui.QTreeWidgetItem(variable)
					pathTree.addChild(variableTree)
		

	def updateReqStatsTree(self):
		self.reqStatsTreeWidget.clear()
		self.reqStatsTreeWidget.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Request", None, QtGui.QApplication.UnicodeUTF8))
		self.reqStatsTreeWidget.headerItem().setText(1,QtGui.QApplication.translate("MainWindow", "Variable set", None, QtGui.QApplication.UnicodeUTF8))
	
		reqStats=self.controller.getReqStats()
		sort1=reqStats.keys()
		sort1.sort()
		for tg in sort1:
			target=QtCore.QStringList()
			target.append(tg)
			targetTree=QtGui.QTreeWidgetItem(target)
			self.reqStatsTreeWidget.addTopLevelItem(targetTree)
			sort2=reqStats[tg].items()
			sort2.sort()
			for k,l in sort2:
				path=QtCore.QStringList()
				path.append(k)
				sets=""
				for set in l:
					sets+=join(set[0],',')+'\n'
				path.append(sets)
				pathTree=QtGui.QTreeWidgetItem(path)
				pathTree.setTextColor(0,QtGui.QColor(0,0,200))
				font=pathTree.font(0)
				font.setBold(True)
				pathTree.setFont(0,font)
				targetTree.addChild(pathTree)

	

	def limpiatablas(self):
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

		self.tableWidget_2.clear()
		self.tableWidget_2.setColumnCount(2)
		self.tableWidget_2.setRowCount(0)
		
		headerItem4 = QtGui.QTableWidgetItem()
		headerItem4.setText(QtGui.QApplication.translate("MainWindow", "Variable", None, QtGui.QApplication.UnicodeUTF8))
		self.tableWidget_2.setHorizontalHeaderItem(0,headerItem4)
		
		headerItem5 = QtGui.QTableWidgetItem()
		headerItem5.setText(QtGui.QApplication.translate("MainWindow", "Value", None, QtGui.QApplication.UnicodeUTF8))
		self.tableWidget_2.setHorizontalHeaderItem(1,headerItem5)

	def updateTable(self):
		requests=self.controller.getRequests()

		if self.radioButton.isChecked()==True:
			method="GET"
		elif self.radioButton_2.isChecked()==True:
			method="POST"	
		else:
			method="BOTH"
			
		a=0
		for i in requests:
			if method=="BOTH":
				self.tableWidget.showRow(a)
			elif method==i.method:
				self.tableWidget.showRow(a)
			else:
				self.tableWidget.hideRow(a)

			
			if self.targetSelect!="All":
				if i.urlWithoutPath!=self.targetSelect:
					self.tableWidget.hideRow(a)
				elif self.pathSelect!="All":
					if i.path!=self.pathSelect:
						self.tableWidget.hideRow(a)
					elif self.variableSelect!="All":
						if not ( i.getVariableGET(self.variableSelect) or i.getVariablePOST(self.variableSelect) ):
							self.tableWidget.hideRow(a)

			a+=1

		self.tableWidget.resizeColumnsToContents()
		self.tableWidget.resizeRowsToContents()
		#Al actualizar pueden visualizarse rows cuyas anchuras no han sido ajstadas, por eso lo de aqui arriba )
					

		
	def targetSelected(self,qstring):

		variableStats=self.controller.getVariableStats()

		self.targetSelect=str(qstring)
		self.comboBox_2.clear()
		self.comboBox_3.clear()
		self.comboBox_2.addItem("All")
		self.comboBox_3.addItem("All")

		if self.targetSelect!="All" and self.targetSelect!='':
			list=variableStats[self.targetSelect].keys()
			list.sort()
			for i in list:
				self.comboBox_2.addItem(i)

		self.variableSelect="All"
		self.pathSelect="All"

		self.updateTable()
		
	def pathSelected(self,qstring):
		variableStats=self.controller.getVariableStats()
		self.pathSelect=str(qstring)
		self.comboBox_3.clear()
		self.comboBox_3.addItem("All")
		
		if self.pathSelect!="All" and len(self.pathSelect)>0:
			list=variableStats[self.targetSelect][self.pathSelect].keys()
			list.sort()
			for i in list:
				self.comboBox_3.addItem(i)

		self.variableSelect="All"
		self.updateTable()
		
	def variableSelected(self,qstring):
		self.variableSelect=str(qstring)
		self.updateTable()

	def cambiaPeticion(self,row,col,row2,col2):
		"Cada vez que se aprieta una peticion de la tabla. row2 y col 2 no se utilizan"
		requests=self.controller.getRequests()

		if self.numRequests:	
			self.requestEdit.clear()
			self.requestEdit.append(requests[row].getAll())
			self.responseEdit.clear()
			self.responseEdit.setPlainText(requests[row].response.getAll())
			
			self.tableWidget_2.clear()
			self.tableWidget_2.setColumnCount(2)
			self.tableWidget_2.setRowCount(0)
			
			headerItem4 = QtGui.QTableWidgetItem()
			headerItem4.setText(QtGui.QApplication.translate("MainWindow", "Variable", None, QtGui.QApplication.UnicodeUTF8))
			self.tableWidget_2.setHorizontalHeaderItem(0,headerItem4)
			
			headerItem5 = QtGui.QTableWidgetItem()
			headerItem5.setText(QtGui.QApplication.translate("MainWindow", "Value", None, QtGui.QApplication.UnicodeUTF8))
			self.tableWidget_2.setHorizontalHeaderItem(1,headerItem5)
		
			a=0
			for i in requests[row].variablesGET():
				self.tableWidget_2.insertRow(a)
				self.tableWidget_2.setItem(a,0,QtGui.QTableWidgetItem(i))
				self.tableWidget_2.setItem(a,1,QtGui.QTableWidgetItem(requests[row].getVariableGET(i)))
				a+=1
	
			for i in requests[row].variablesPOST():
				self.tableWidget_2.insertRow(a)
				self.tableWidget_2.setItem(a,0,QtGui.QTableWidgetItem(i))
				self.tableWidget_2.setItem(a,1,QtGui.QTableWidgetItem(requests[row].getVariablePOST(i)))
				a+=1
	
			self.tableWidget_2.resizeColumnToContents(0)
			self.tableWidget_2.resizeColumnToContents(1)
			self.tableWidget_2.resizeRowsToContents()
			

	def slotTree (self,item,a):
		if item.parent()!=None and item.parent().parent()!=None:

			self.targetSelected(item.parent().parent().text(0))
			self.pathSelected(item.parent().text(0))
			self.variableSelected(item.text(0))
			
			indexvar=self.comboBox_3.findText(item.text(0))
			indexpath=self.comboBox_2.findText(item.parent().text(0))
			indextarget=self.comboBox.findText(item.parent().parent().text(0))

			self.comboBox.setCurrentIndex(indextarget)
			self.comboBox_2.setCurrentIndex(indexpath)
			self.comboBox_3.setCurrentIndex(indexvar)


	def salir(self):
		sys.exit(0)
	

	def timerFunc(self):
		x,y=self.controller.getNumAttacks()
		self.statusbar.showMessage("Status: %d Sql Injection Attacks\t-\t%d XSS Attacks" % (y,x))
		if not x and not y:
			self.attackRequestThreadsSpin.setEnabled(True)
		else:
			self.attackRequestThreadsSpin.setEnabled(False)


		self.controller.timer()
		self.updateSQLResults(self.controller.getSqlResults())
		self.updateXSS(self.controller.getXssResults())

		reqs=self.controller.getNewRequests()
		if reqs:
			a=self.tableWidget.rowCount()
			for i in reqs:

				self.tableWidget.insertRow(a)
				self.tableWidget.setItem(a,0,QtGui.QTableWidgetItem(i.method))
				self.tableWidget.setItem(a,1,QtGui.QTableWidgetItem(i.urlWithoutPath))
				self.tableWidget.setItem(a,2,QtGui.QTableWidgetItem(i.pathWithVariables))
				if i["Cookie"]:
					self.tableWidget.setItem(a,3,QtGui.QTableWidgetItem(i["Cookie"]))
				
				self.updateCombos(i)
				a+=1

			self.updateTable()
			self.tableWidget.setRowCount(self.numRequests)  
	
			a=self.comboBox.currentText()
			b=self.comboBox_2.currentText()
			c=self.comboBox_3.currentText()
	
			self.targetSelected(a)
			self.pathSelected(b)
			self.variableSelected(c)
			
			indexvar=self.comboBox_3.findText(c)
			indexpath=self.comboBox_2.findText(b)
			indextarget=self.comboBox.findText(a)

			self.comboBox.setCurrentIndex(indextarget)
			self.comboBox_2.setCurrentIndex(indexpath)
			self.comboBox_3.setCurrentIndex(indexvar)


	

		
	def updateCombos (self,req):
		if self.comboBox.findText(req.urlWithoutPath)==-1:
			self.comboBox.addItem(req.urlWithoutPath)

	def deleteSelected(self):
		a=[]
		for i in self.tableWidget.selectedRanges():
			a+=range (i.topRow(),i.bottomRow()+1)
		a.sort(reverse=True)
	
		self.deleteRequests(a)


	def deleteInView(self):
		indexes=[]

		n=self.tableWidget.rowCount()
		for i in range(n):
			if not self.tableWidget.isRowHidden(i):
				indexes.append(i)

		indexes.reverse()
		self.deleteRequests(indexes)


	def deleteRequests(self,indexes):
		requests=self.controller.getRequests()
		mb = QtGui.QMessageBox ("Deleting Requests","Are you sure you want to delete selected requests ?",QtGui.QMessageBox.Warning,QtGui.QMessageBox.Cancel,QtGui.QMessageBox.Ok,0)
		if mb.exec_()==QtGui.QMessageBox.Ok:
			for i in indexes:
				del requests[i]
				self.tableWidget.removeRow(i)

			self.updateAllStats()
	
	def updateAllStats(self):
		self.controller.updateAllStats()
		requests=self.controller.getRequests()

		self.comboBox.clear()
		self.comboBox.addItem("All")
		
		for i in requests:
			self.updateCombos(i)

		self.targetSelected("All")


	def setNewCookie(self):
		requests=self.controller.getRequests()
		indexes=[]

		n=self.tableWidget.rowCount()
		for i in range(n):
			if not self.tableWidget.isRowHidden(i):
				indexes.append(i)

		for i in indexes:
			requests[i].addHeader("Cookie",str(self.cookieEdit.text()))
			self.tableWidget.setItem(i,3,QtGui.QTableWidgetItem(str(self.cookieEdit.text())))


		
	
	def toogleEditor(self):	
		number= self.stackedWidget.currentIndex()
		if number:
			number= self.stackedWidget.setCurrentIndex(0)
		else:
			number= self.stackedWidget.setCurrentIndex(1)

	def applyRegex (self):
		requests=self.controller.getRequests()
		if str(self.substSrcEdit.text()):
			indexes=[]
	
			n=self.tableWidget.rowCount()
			for i in range(n):
				if not self.tableWidget.isRowHidden(i):
					indexes.append(i)
	
			for i in indexes:
				try:
					requests[i].Substitute(str(self.substSrcEdit.text()),str(self.substDstEdit.text()))
					self.tableWidget.setItem(i,1,QtGui.QTableWidgetItem(requests[i].urlWithoutPath))
					self.tableWidget.setItem(i,2,QtGui.QTableWidgetItem(requests[i].pathWithVariables))
					if requests[i]["Cookie"]:
						self.tableWidget.setItem(i,3,QtGui.QTableWidgetItem(requests[i]["Cookie"]))
				except Exception,a:
					mb = QtGui.QMessageBox ("Error in substitution","ERROR !",QtGui.QMessageBox.Warning,QtGui.QMessageBox.Ok,0,0)
					mb.exec_()
					return

			self.updateAllStats()
					

	def applyConfig (self):
		getsign=str(self.getsignEdit.text())
		headersign=str(self.headersignEdit.text())
		valuesign=str(self.valuesignEdit.text())
		limitpath=str(self.pathlimitEdit.text())
		proxy=str(self.proxyEdit.text())
		proxyport=self.portSpin.value()

		try:
			Proxynet.changePort(proxyport)
		except Exception,a:
			Proxynet.changePort(8008)
			Proxynet.init()
			self.portSpin.setValue(8008)
			mb = QtGui.QMessageBox ("Error",str(a),QtGui.QMessageBox.Critical,QtGui.QMessageBox.Ok,0,0)
			mb.exec_()
			
			
			
		Proxynet.signGET(getsign)
		Proxynet.signHeaders(headersign, valuesign)
		Proxynet.limitPath(limitpath)
		if proxy:
			Proxynet.setProxy(proxy)
			Attacker.setProxy(proxy)
		else:
			Proxynet.setProxy(None)
			Attacker.setProxy(None)
		
########################################################################################################################################
########################################################################################################################################
########################################################################################################################################
#########################################                Attacker                    ###################################################
########################################################################################################################################
########################################################################################################################################

	def updateXSS(self,list):
		if not list:
			return
		for i in list:
			target=QtCore.QStringList()
			target.append(i[0])
			targetTree=QtGui.QTreeWidgetItem(target)
			self.treeXss.addTopLevelItem(targetTree)
			for j in i[1]:
				target2=QtCore.QStringList()
				target2.append("")
				target2.append(j[2])
				target2.append(j[1])
				str=""
				for l in j[3]:
					str+=l+"\r\n"
				target2.append(str)

				targetTree2=QtGui.QTreeWidgetItem(target2)
				targetTree.addChild(targetTree2)




	def updateSQLResults(self,list):
		if not list:
			return
		for i in list:
			target=QtCore.QStringList()
			target.append(i[0])
			targetTree=QtGui.QTreeWidgetItem(target)
			self.treeSql.addTopLevelItem(targetTree)
			for j in i[1]:
				target2=QtCore.QStringList()
				target2.append("")
				for k in j:
					if k:
						target2.append(k)
					else:
						target2.append("")
				targetTree2=QtGui.QTreeWidgetItem(target2)
				targetTree.addChild(targetTree2)
			pass


	def sqlToogled(self,int):
		self.controller.sqlToogled(int)

	def xssToogled(self,int):
		self.controller.xssToogled(int)

	def exportXssToHTML(self):
		fileName = QtGui.QFileDialog.getSaveFileName()
		if len(fileName)>0:
			try:
				self.controller.saveHTMLXss(fileName)
			except:
				print "Error Writing File"

	def exportSqlToHTML(self):
		fileName = QtGui.QFileDialog.getSaveFileName()
		if len(fileName)>0:
			try:
				self.controller.saveHTMLSql(fileName)
			except:
				print "Error Writing File"

	def exportSqlToXML(self):
		fileName = QtGui.QFileDialog.getSaveFileName()
		if len(fileName)>0:
			try:
				self.controller.saveXMLSql(fileName)
			except:
				print "Error Writing File"

	def exportXssToXML(self):
		fileName = QtGui.QFileDialog.getSaveFileName()
		if len(fileName)>0:
			try:
				self.controller.saveXMLXss(fileName)
			except:
				print "Error Writing File"

	def changeReqThreads(self,n):
		self.controller.changeReqThreads(n)

	def funcion_About(self):
		mb = QtGui.QMessageBox ("About","About ProxyStrike\n\nAUTHOR\n\nCarlos del Ojo Elias (deepbit)\ncdelojo@edge-security.com\n\nEDGE-SECURITY 2008",QtGui.QMessageBox.Information,QtGui.QMessageBox.Ok,0,0)
		mb.exec_()
	#	mb=about.Ui_Form()	
	#	mb.show()

	def close(self):
		print "Closing..."
