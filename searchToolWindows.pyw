#!usr/bin/python3.4

import sys, xlrd, datetime
from PyQt4 import QtGui, QtCore

class SearchGUI(QtGui.QWidget):
	""" Graphical interface for the patient incident search tool """

	def __init__(self):
		super(SearchGUI, self).__init__()
		self.dataFile = self.findDatefile()
		#self.dataFile = sys.argv[1]
		self.informationDict = self.inputData()
		self.initUI()
		self.setWindowTitle('Incident Zoekmachine')
		self.keywords = []
		#self.oldSetting = True
		if self.horLabels[20].startswith('zz'):
			self.index = 20
		else:
			self.index = 14		
		
	def initUI(self):
		""" Initializes the user interface """
		self.grid = QtGui.QGridLayout()
		self.grid.setSpacing(1)

		self.searchInput1 = QtGui.QLineEdit()
		self.searchInput1.returnPressed.connect(self.searchButtonPressed)
		self.searchInput2 = QtGui.QLineEdit()
		self.searchInput2.returnPressed.connect(self.searchButtonPressed)
		self.searchInput3 = QtGui.QLineEdit()
		self.searchInput3.returnPressed.connect(self.searchButtonPressed)
		self.searchInput4 = QtGui.QLineEdit()
		self.BooleanButton1 = QtGui.QComboBox()
		self.BooleanButton1.addItems(['', 'AND', 'OR', 'NOT'])
		self.BooleanButton2 = QtGui.QComboBox()
		self.BooleanButton2.addItems(['', 'AND', 'OR', 'NOT'])
		self.BooleanButton3 = QtGui.QComboBox()
		self.BooleanButton3.addItems(['', 'AND', 'OR', 'NOT'])
		self.BooleanButton4 = QtGui.QComboBox()
		self.BooleanButton4.addItems(['', 'AND', 'OR', 'NOT'])
		self.searchLabel = QtGui.QLabel("Toegevoegde zoektermen:")
		self.showKeywords = QtGui.QLineEdit()
		self.showKeywords.setReadOnly(True)
		self.SearchButton = QtGui.QPushButton("Zoek")
		self.SearchButton.clicked.connect(self.searchButtonPressed)
		self.ClearButton = QtGui.QPushButton("Tabel opschonen")
		self.ClearButton.clicked.connect(self.clearTable)
		self.ExplainLabel = QtGui.QLabel("Typ de gewenste zoektermen met Boolean waarden in de velden hieronder. U kunt maximaal 3 zoektermen toevoegen.\nU begint automatisch opnieuw als u met nieuwe zoektermen op <Zoek> drukt, de tabel wordt dan ververst op basis van de nieuwe zoektermen.")

		self.dataTable = QtGui.QTableWidget(self.rowLength, self.columnLength)
		self.dataTable.isSortingEnabled()
		self.dataTable.setHorizontalHeaderLabels(self.horLabels)
		#self.dataTable.cellDoubleClicked.connect(self.showFullText)
			
		self.grid.addWidget(self.ExplainLabel, 0, 0, 1, 6)
		#self.grid.addWidget(self.BooleanButton1, 1, 0, 1, 1)
		self.grid.addWidget(self.searchInput1, 1, 0, 1, 1)
		self.grid.addWidget(self.BooleanButton2, 1, 1, 1, 1)
		self.grid.addWidget(self.searchInput2, 1, 2, 1, 1)
		self.grid.addWidget(self.BooleanButton3, 1, 3, 1, 1)
		self.grid.addWidget(self.searchInput3, 1, 4, 1, 1)
		#self.grid.addWidget(self.BooleanButton4, 1, 5, 1, 1)
		#self.grid.addWidget(self.searchInput4, 1, 6, 1, 1)
		#self.grid.addWidget(self.searchLabel, 2, 0, 1, 1)
		#self.grid.addWidget(self.showKeywords, 3, 0, 1, 6)
		self.grid.addWidget(self.SearchButton, 4, 0, 1, 1)
		self.grid.addWidget(self.ClearButton, 4, 1, 1, 1)
		self.grid.addWidget(self.dataTable, 5, 0, 1, 6)

		self.setWindowIcon(QtGui.QIcon('icon.png'))
		self.setLayout(self.grid)
		self.hasMouseTracking = True
		#self.showMaximized()
		self.show()

	def clearTable(self):
		""" Clears the table and sets the headers """
		self.dataTable.clear()
		self.dataTable.setHorizontalHeaderLabels(self.horLabels)

	def searchButtonPressed(self):
		""" Handles the pressing of the search button """
		#print(self.searchInput1.text(), self.BooleanButton2.currentText(), self.searchInput2.text(), self.BooleanButton3.currentText(), self.searchInput3.text(), self.BooleanButton4.currentText(), self.searchInput4.text())
		self.clearTable()
		self.keywords = []
		self.search1 = self.searchInput1.text()
		self.search2 = self.searchInput2.text()
		self.search3 = self.searchInput3.text()
		self.search4 = self.searchInput4.text()
		self.bool2 = self.BooleanButton2.currentText()
		self.bool3 = self.BooleanButton3.currentText()
		self.bool4 = self.BooleanButton4.currentText()
		self.keywords.append(('', self.search1))
		if self.search2 != '' and self.bool2 != '':
			self.keywords.append((self.bool2, self.search2))
		if self.search3 != '' and self.bool3 != '':
			self.keywords.append((self.bool3, self.search3))
		self.checkData()
		self.setData()
		self.clearFields()

	def clearFields(self):
		""" Clear the input fields """
		self.searchInput1.setText('')
		self.searchInput2.setText('')
		self.searchInput3.setText('')
		self.searchInput4.setText('')
		self.BooleanButton1.setCurrentIndex(0)
		self.BooleanButton2.setCurrentIndex(0)
		self.BooleanButton3.setCurrentIndex(0)
		self.BooleanButton4.setCurrentIndex(0)
		self.keywords = []

	def checkData(self):
		""" Matches the keywords with incident descriptions """
		self.referenceNums = []
		if len(self.keywords) == 1:
			#print("Using single keyword")
			for values in self.informationDict.values():
				count = 0
				#concatValues = ' '.join(values) # For searching all fields
				concatValues = values[self.index] # For searching only description field
				if self.keywords[0][1] in concatValues:
					while count == 0:
						self.referenceNums.append(self.informationDict[values[0]])
						count += 1
		
		elif len(self.keywords) == 2:
			for values in self.informationDict.values():
				#concatValues = ' '.join(values) # For searching all fields
				concatValues = values[self.index] # For searching only description field
				count = 0
				firstCondition = False
				secondCondition = False
				if self.keywords[0][1] in concatValues:
					firstCondition = True

				if self.keywords[1][0] == 'AND':
					if self.keywords[1][1] in concatValues:
						secondCondition = True
						if firstCondition == True and secondCondition == True:
							while count == 0:
								self.referenceNums.append(self.informationDict[values[0]])
								count += 1
				
				elif self.keywords[1][0] == 'OR':
					if self.keywords[1][1] in concatValues:
						secondCondition = True
					if firstCondition == True or secondCondition == True:
						while count == 0:
							self.referenceNums.append(self.informationDict[values[0]])
							count += 1
				
				elif self.keywords[1][0] == 'NOT':
					if self.keywords[1][1] in concatValues:
						secondCondition = True
					if firstCondition == True and secondCondition == False:
						while count == 0:
							self.referenceNums.append(self.informationDict[values[0]])
							count += 1
				
				else:
					pass

		elif len(self.keywords) == 3:
			for values in self.informationDict.values():
				#concatValues = ' '.join(values) # For searching all fields
				concatValues = values[self.index] # For searching only description field
				count = 0
				firstCondition = False
				secondCondition = False
				thirdCondition = False

				if self.keywords[0][1] in concatValues:
					firstCondition = True

				if self.keywords[1][1] in concatValues:
					secondCondition = True

				if self.keywords[2][1] in concatValues:
					thirdCondition = True

				if self.keywords[1][0] == 'AND' and self.keywords[2][0] == 'AND':
					if firstCondition == True and secondCondition == True and thirdCondition == True:
						while count == 0:
							self.referenceNums.append(self.informationDict[values[0]])
							count += 1
					
				elif self.keywords[1][0] == 'AND' and self.keywords[2][0] == 'OR':
					if (firstCondition == True and secondCondition == True) or thirdCondition == True:
						while count == 0:
							self.referenceNums.append(self.informationDict[values[0]])
							count += 1

				elif self.keywords[1][0] == 'AND' and self.keywords[2][0] == 'NOT':
					if firstCondition == True and secondCondition == True and thirdCondition == False:
						while count == 0:
							self.referenceNums.append(self.informationDict[values[0]])
							count += 1
				
				elif self.keywords[1][0] == 'NOT' and self.keywords[2][0] == 'AND':
					if firstCondition == True and secondCondition == False and thirdCondition == True:
						while count == 0:
							self.referenceNums.append(self.informationDict[values[0]])
							count += 1

				elif self.keywords[1][0] == 'NOT' and self.keywords[2][0] == 'OR':
					if (firstCondition == True or thirdCondition == True) and secondCondition == False:
						while count == 0:
							self.referenceNums.append(self.informationDict[values[0]])
							count += 1
				
				elif self.keywords[1][0] == 'NOT' and self.keywords[2][0] == 'NOT':
					if firstCondition == True and secondCondition == False and thirdCondition == False:
						while count == 0:
							self.referenceNums.append(self.informationDict[values[0]])
							count += 1

				elif self.keywords[1][0] == 'OR' and self.keywords[2][0] == 'AND':
					if (firstCondition == True or secondCondition == True) and thirdCondition == True:
						while count == 0:
							self.referenceNums.append(self.informationDict[values[0]])
							count += 1

				elif self.keywords[1][0] == 'OR' and self.keywords[2][0] == 'OR':
					if firstCondition == True or secondCondition == True or thirdCondition == True:
						while count == 0:
							self.referenceNums.append(self.informationDict[values[0]])
							count += 1

				elif self.keywords[1][0] == 'OR' and self.keywords[2][0] == 'NOT':
					if (firstCondition == True or secondCondition == True) and thirdCondition == False:
						while count == 0:
							self.referenceNums.append(self.informationDict[values[0]])
							count += 1
				else:
					pass
						
		else:
			pass
		

	def inputData(self):
		""" Searches the datafile based on the queries """
		try:
			self.workbook = xlrd.open_workbook(self.dataFile)
		except FileNotFoundError:
			exit(-1)

		self.sheet = self.workbook.sheet_by_index(0)
		informationDict = {}
		self.rowLength = self.sheet.nrows
		self.columnLength = self.sheet.ncols

		for i, row in enumerate(range(self.sheet.nrows)):
			if i == 0:
				self.horLabels = self.sheet.row_values(row)
			#elif i == 1:
			#	for waarden in self.sheet.row_values(row):
			#		print(type(waarden))
			else:
				rowInformation = self.sheet.row_values(row)
				for index, value in enumerate(rowInformation):
					if type(value) == float:
						if index == 1 or index == 2 or index == 3 or index == 5 or index == 6:
							newValue = str(datetime.datetime(*xlrd.xldate_as_tuple(value, 0))).split()[0]
							rowInformation[index] = newValue
						else:
							newValue = str(value)
							rowInformation[index] = newValue
				informationDict[self.sheet.row_values(row)[0]] = tuple(rowInformation)
		return informationDict

	def setData(self):
		""" Sets the relevant data in the Table-view """
		for r, values in enumerate(self.referenceNums):
			for c, item in enumerate(values):
				newitem = QtGui.QTableWidgetItem(item)
				self.dataTable.setItem(r, c, newitem)
		self.dataTable.sortByColumn(0, 0)
		self.dataTable.resizeColumnsToContents()
		self.dataTable.resizeRowsToContents()

	def findDatefile(self):
		""" Dialog that prompts the user to open a data file """
		self.dialog = QtGui.QFileDialog(self)
		self.dialog.setNameFilter("Excel files (*.xls, *.xlsx)")
		self.dialog.setLabelText(1, "Selecteer een data bestand in Excel-formaat")
		return self.dialog.getOpenFileName()



if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	s = SearchGUI()
	s.show()
	app.exec_()