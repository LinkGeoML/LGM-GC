# -*- coding: UTF-8 -*-
"""
/***************************************************************************
 GeoCodingDialog
                                 A QGIS plugin
 geocoding
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-02-27
        git sha              : $Format:%H$
        copyright            : (C) 2020 by eratosthenis
        email                : iliasvrk@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os,glob,time,subprocess,datetime,re,csv,sys,threading,shutil,tempfile,numpy
from PyQt5 import uic,QtWidgets,QtCore
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QMenu,QAction,QPushButton,QFileDialog,QInputDialog,QLineEdit,QMessageBox,QDialog,QProgressBar,QTableWidget,QTableWidgetItem,QTableView,QHBoxLayout,QCheckBox,QVBoxLayout,QDockWidget 
from PyQt5.QtCore import QSize
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qgis.PyQt.QtWidgets import QWidget
from qgis.core import *
from qgis.core import QgsFeature
from qgis.gui import *
import qgis.utils
from functools import partial
from qgis.PyQt import QtWidgets
from .geocoding_dialog2 import geo_coding_dialog_base2

default_path=QgsApplication.qgisSettingsDirPath() + "\python\plugins"  #OS independent default  path for qgis plugins
os.chdir(default_path)
        
temp1=os.getcwd()
temp2=os.listdir(path=str(temp1))               

if 'geocoding' in temp2:
	os.chdir('.\geocoding')  
	
if not sys.path==(os.getcwd() + '\\LGM-Geocoding-master'):
    sys.path.append(os.getcwd() + '\\LGM-Geocoding-master')
# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'geocoding2_dialog_base.ui'))

	
	
class GeoCodingDialog(QtWidgets.QDialog, FORM_CLASS):
	def __init__(self,myiface, parent=None):
		"""Constructor."""
		super(GeoCodingDialog, self).__init__(parent)
		self.myiface = myiface
        self.setupUi(self)
		self.TrainingSectionbtn.clicked.connect(self.TrainingSectionbtncliked)          
		self.choosepoifilefilebtn.clicked.connect(self.choosepoifilefilebtncliked)
		self.model_deploymentbtn.clicked.connect(self.model_deploymentbtn_clicked)
		self.showresultsbtn.clicked.connect(self.showresultsbtncliked)
		self.load_layer_btn.clicked.connect(self.load_layerbtn_clicked)
		self.myupdatebtn.clicked.connect(self.myupdatebtncliked)
		self.load_user_btn.clicked.connect(self.load_user_btn_clicked)
		self.auto_selectbtn.clicked.connect(self.auto_selectbtn_clicked)
		self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
		self.tableWidget.customContextMenuRequested.connect(self.tableWidgetpopup2)
	
	###################################
	#    MODEL     RUNNING     SECTION #
	###################################

	def TrainingSectionbtncliked(self):  
		self.dlg = geo_coding_dialog_base2(self.myiface)
		self.dlg.show()
    def choosepoifilefilebtncliked(self):   
		QMessageBox.information(self,"INFO","Choose input file")
		try:
			fd=QFileDialog()
			test_file = ".\\LGM-Geocoding-master\\geocoding-dataset"
			mfullstr=str(fd.getOpenFileName(self,"Open POI File to Classify ",test_file))
			fname=mfullstr[2:mfullstr.index("'", 4, 1000)] # fname has the full path of the desired poi file
			self.choosepoifilefilechoosenfile.setText(fname) # set the fname to choosepoifilefilechoosenfile
			with open(fname, newline='', encoding=' utf-8') as csv_file:   # utf-8 
				csv_data = csv.reader(csv_file, delimiter=',')
				rownum = 0          
				for row in csv_data:
					rownum=rownum+1
			csv_file.close()
			
		except FileNotFoundError:  # check if cancel or x is pressed
			QMessageBox.information(self,"CAUTION","File Selection Canceled")
			self.choosepoifilefilechoosenfile.clear() #clears line
			
			
	def load_layerbtn_clicked(self):
		fname=self.choosepoifilefilechoosenfile.text() #fname is the input file to be classified
		predictions_csv = self.last_exp_file() + "\\model_deployment_results\\predictionsrplconverted.csv"
		
		file_original = self.last_exp_file() + "\\model_deployment_results\\original.csv" #file containing 'original' category
		file_arcgis = self.last_exp_file() + "\\model_deployment_results\\arcgis.csv"     # file containing 'arcgis' category
		file_nominatim = self.last_exp_file() + "\\model_deployment_results\\nominatim.csv" # file containing 'nominatim' category
		with open(predictions_csv,'r',newline='', encoding=' utf-8') as userfile , open(fname,'r',newline='', encoding=' utf-8')as inputfile:
			with open(file_original,'w',newline='') as original , open(file_arcgis,'w',newline='') as arcgis , open(file_nominatim,'w',newline='') as nominatim:   
				csv_test_input=csv.reader(inputfile,quoting=csv.QUOTE_MINIMAL,skipinitialspace='True')
				csv_results=csv.reader(userfile,quoting=csv.QUOTE_MINIMAL,skipinitialspace='True')
				next(csv_test_input) #ignore csv headers
				wr_original = csv.writer(original,delimiter=",")
				wr_arcgis = csv.writer(arcgis,delimiter=",")
				wr_nominatim = csv.writer(nominatim,delimiter=",")
        
				wr_original.writerow(['address','score','x_original','y_original'])
				wr_arcgis.writerow(['address','score','x_arcgis','y_arcgis'])
				wr_nominatim.writerow(['address','score','x_nominatim','y_nominatim'])
				counter=0
				for i in csv_results:
					temp1 = ((i[2].split(' ',2))[:2])
					temp2 = ((i[2].split(' ',4))[2:4])
					temp3 = ((i[2].split(' ',6))[4:6])
           
					for j in csv_test_input:
						if ("'original'") in temp1:
							temp1= str(temp1).replace("[","").replace("]","").replace('"','').replace(",","").replace("'","")
							wr_original.writerow([j[0],temp1,j[1],j[2]])
							counter+=1
						if ("'arcgis'") in temp1:
							temp1=str(temp1).replace("[","").replace("]","").replace('"','').replace(",","").replace("'","")
							wr_arcgis.writerow([j[0],temp1,j[3],j[4]])
							counter+=1
						if("'nominatim") in temp1:
							temp1= str(temp1).replace("[","").replace("]","").replace('"','').replace(",","").replace("'","")
							wr_nominatim.writerow([j[0],temp1,j[5],j[6]])
							counter+=1  
                
						if ("'original'") in temp2:
							temp2=str(temp2).replace("[","").replace("]","").replace('"','').replace(",","").replace("'","")
							wr_original.writerow([j[0],temp2,j[1],j[2]])
							counter+=1      
						if ("'arcgis'") in temp2:
							temp2=str(temp2).replace("[","").replace("]","").replace('"','').replace(",","").replace("'","")
							wr_arcgis.writerow([j[0],temp2,j[3],j[4]])
							counter+=1      
						if ("'nominatim'") in temp2:
							temp2=str(temp2).replace("[","").replace("]","").replace('"','').replace(",","").replace("'","")
							wr_nominatim.writerow([j[0],temp2,j[5],j[6]])
							counter+=1      
                      
						if ("'original'") in temp3:
							temp3=str(temp3).replace("[","").replace("]","").replace('"','').replace(",","").replace("'","")
							wr_original.writerow([j[0],temp3,j[1],j[2]])
							counter+=1      
						if ("'arcgis'") in temp3:
							temp3=str(temp3).replace("[","").replace("]","").replace('"','').replace(",","").replace("'","")
							wr_arcgis.writerow([j[0],temp3,j[3],j[4]])
							counter+=1      
						if ("'nominatim'") in temp3:
							temp3=str(temp3).replace("[","").replace("]","").replace('"','').replace(",","").replace("'","")
							wr_nominatim.writerow([j[0],temp3,j[5],j[6]])
							counter+=1
						break

		QMessageBox.information(self,"INFO","Load ORIGINAL Category")
		
		####  Load 1st layer category - ORIGINAL -  #########
		uri_original = "file:///" + file_original + "?delimiter={}&xField={}&yField={}".format(",", "x_original", "y_original")	# Need to have that type of file structure
		layer_csv = QgsVectorLayer(uri_original, "Roads Classified (original)", 'delimitedtext') # layer constructor
		#Check if the (uri) file has the appropriate format to load as a layer
		if not layer_csv.isValid():
			QMessageBox.warning(self,"CAUTION","Layer failed to load")
		properties = {'style': 'no','width_border': '1.1','color_border': 'red','style_border' : 'solid'}
		symbol = QgsFillSymbol.createSimple(properties)
		symbol = QgsMarkerSymbol.createSimple({'name': 'square', 'color': 'purple','size':'2.5'})
		layer_csv.setRenderer(QgsSingleSymbolRenderer(symbol))
		
		layer_settings  = QgsPalLayerSettings()
		layer_settings.fieldName = "name"
		layer_settings.placement = 3
		layer_settings = QgsVectorLayerSimpleLabeling(layer_settings)
		layer_csv.setLabelsEnabled(True)
		layer_csv.setLabeling(layer_settings)
		
		config = layer_csv.editFormConfig()
		config.setInitCodeSource(1)
		
		default_path=QgsApplication.qgisSettingsDirPath() + "\\python\\plugins\\geocoding"  #OS independent default  path for qgis plugins
		os.chdir(default_path)
		uiform = default_path + '.\\tableWidget-for-pois-original.ui'
		config.setUiForm(uiform) #layout form of the individual pois
		
		layer_csv.setEditFormConfig(config)
		QgsProject.instance().addMapLayer(layer_csv)
		### Load 2nd  layer Category - ARCGIS - ####
		QMessageBox.information(self,"INFO","Load ARCGIS Category")
		uri_arcgis = "file:///" + file_arcgis + "?delimiter={}&xField={}&yField={}".format(",", "x_arcgis", "y_arcgis")
		layer_arcgis = QgsVectorLayer(uri_arcgis, "Roads Classified (arcgis)", 'delimitedtext') # layer constructor
		if not layer_arcgis.isValid():
			QMessageBox.warning(self,"CAUTION","Layer failed to load")
		properties_arcgis = {'style': 'no','width_border': '1.1','color_border': 'purple','style_border' : 'solid'}
		symbol_arcgis = QgsFillSymbol.createSimple(properties_arcgis)
		symbol_arcgis = QgsMarkerSymbol.createSimple({'name': 'circle', 'color': 'blue','size':'2.5'})
		layer_arcgis.setRenderer(QgsSingleSymbolRenderer(symbol_arcgis))
		default_path=QgsApplication.qgisSettingsDirPath() + "\\python\\plugins\\geocoding"  #OS independent default  path for qgis plugins
		os.chdir(default_path)
		config_form_arcgis=layer_arcgis.editFormConfig()
		uiform_arcgis = default_path + '.\\tableWidget-for-pois-arcgis.ui'
		config_form_arcgis.setUiForm(uiform_arcgis) #layout form of the individual pois
		layer_arcgis.setEditFormConfig(config_form_arcgis)
		layer_settings_arcgis  = QgsPalLayerSettings()
		layer_settings_arcgis.fieldName = "name"
		layer_settings_arcgis.placement = 4
		layer_settings_arcgis = QgsVectorLayerSimpleLabeling(layer_settings_arcgis)
		layer_arcgis.setLabelsEnabled(True)
		layer_arcgis.setLabeling(layer_settings_arcgis)
		QgsProject.instance().addMapLayer(layer_arcgis)
		########### Load 3rd layer Category - NOMINATIM - ##################
		QMessageBox.information(self,"INFO","Load NOMINATIM Category")
		uri_nominatim = "file:///" + file_nominatim +"?delimiter={}&xField={}&yField={}".format(",","x_nominatim","y_nominatim")
		layer_nominatim = QgsVectorLayer(uri_nominatim, "Roads Classified (nominatim)", 'delimitedtext') # layer constructor
		if not layer_nominatim.isValid():
			QMessageBox.warning(self,"CAUTION","Layer failed to load")
		properties_nominatim = {'style': 'no','width_border': '2.2','color_border': 'green','style_border' : 'solid'}
		symbol_nominatim = QgsFillSymbol.createSimple(properties_nominatim)
		symbol_nominatim = QgsMarkerSymbol.createSimple({'name': 'star', 'color': 'red','size':'5.0'})
		layer_nominatim.setRenderer(QgsSingleSymbolRenderer(symbol_nominatim))
		config_form_nominatim = layer_nominatim.editFormConfig()
		path_nominatim = QgsApplication.qgisSettingsDirPath() + "\\python\\plugins\\geocoding" 
		uiform_nominatim = path_nominatim + ".\\tableWidget-for-pois-nominatim.ui"
		config_form_nominatim.setUiForm(uiform_nominatim)
		layer_nominatim.setEditFormConfig(config_form_nominatim)
		layer_settings_nominatim = QgsPalLayerSettings()
		layer_settings_nominatim.fieldName = "name"
		layer_settings_nominatim.placement = 5
		layer_settings_nominatim = QgsVectorLayerSimpleLabeling(layer_settings_nominatim)
		layer_nominatim.setLabelsEnabled(True)
		layer_nominatim.setLabeling(layer_settings_nominatim)
		QgsProject.instance().addMapLayer(layer_nominatim)
		
	def model_deploymentbtn_clicked(self):
		global count
		experiment_path=QFileDialog()
		exp_path = (experiment_path.getExistingDirectory(self,"Please choose experiment path file",str(os.getcwd()),QFileDialog.ShowDirsOnly)) + "\\\\"
		while exp_path=='':
			QMessageBox.warning(self,"CAUTION","No experiment path selected")
			break
		fpath = self.choosepoifilefilechoosenfile.text()
		
		progress = QProgressBar()
		progress.setGeometry(200, 80, 250, 20)
		progress.move(600,600)
		progress.setWindowTitle('Processing..')
		progress.setAlignment(QtCore.Qt.AlignCenter)
		progress.show()
				
		if "LGM-Geocoding-master" in str(os.getcwd()):
			pass
		else:
			os.chdir('.\\LGM-Geocoding-master')		
		
		command = f'python model_deployment.py -experiment_path {exp_path} -fpath {fpath}'
		
		try:
			output = subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT)
		except subprocess.CalledProcessError:
			QMessageBox.warning(self,"WARNING","Execution of command failed")
		out_put = str(output)
		
		
		QMessageBox.information(self,'INFO',out_put)
		csv_filepath = exp_path + "model_deployment_results\\predictions.csv"
		
		csvmyfile = exp_path + "model_deployment_results" +"\\predictionsrplconverted.csv"
		
		with open(csv_filepath, newline='', encoding=' utf-8') as csv_file:
			with open(csvmyfile,"w",newline='') as myfile: 
				csv_data = csv.reader(csv_file,quoting=csv.QUOTE_MINIMAL,skipinitialspace='True') ###
				count = 0
				wr=csv.writer(myfile)
				for row in csv_data:
					if count < 1: #skip csv header
						count=1
						continue
					if len(str(row))>2:
						a=count # id
						count+=1
						b=row[0] # address
						c=row[1] # predictions
						c=c.replace('"',"").replace("[","").replace("]","").replace("(","").replace(")","").replace(",","")
						if any(row): #remove empty lines in csv file
							wr.writerow([a,b,c])
		count=count-1  # remove header from csv
		
			
#-------------------------------------------------------------	
	def last_exp_file(self):    
		if "LGM-Geocoding-master" in os.getcwd():
			temp1=os.getcwd()
		else:
			temp1=os.getcwd() + "\\LGM-Geocoding-master"
		temp2=os.listdir(path=str(temp1))
		latest_file = ""
		if 'experiments' in temp2:
			list_of_files = glob.glob(str(temp1) + '\\experiments\\*')  
			
			latest_file = max(list_of_files,key=os.path.getctime)
			
		else:
			latest_file = ("")
		return latest_file    
#----------------------------------------------------------------
	def showresultsbtncliked(self):
		csv_filepath = self.last_exp_file() + "\\model_deployment_results\\predictionsrplconverted.csv"
		with open(csv_filepath, newline='', encoding=' utf-8') as csv_file:
			csv_data = csv.reader(csv_file)
			count=0
			for row in csv_data:
				count+=1
		self.createTable(count)
	def createTable(self,count):    
        self.tableWidget.setRowCount(count) 
		self.tableWidget.setColumnCount(5)  
		rownum=0
        csv_filepath = self.last_exp_file() + "\\model_deployment_results\\predictionsrplconverted.csv"
		progress = QProgressBar()
		progress.setGeometry(200, 80, 250, 20)
		progress.move(600,600)
		progress.setWindowTitle('Loading Result Table')
		progress.setAlignment(QtCore.Qt.AlignCenter)
		progress.show()
		with open(csv_filepath, newline='', encoding=' UTF-8') as csv_file:  
			csv_data = csv.reader(csv_file)
			rownum = 0
			for row in csv_data:
				j=row[2] #row[2] -> category
				k=row[2]
				l=row[2]
				j=str(str(j).split(' ',2)[:2]).replace("'","").replace('"','').replace("[","").replace("]","").replace(",","") 
				k=str(str(k).split(' ',4)[2:4]).replace("'","").replace('"','').replace("[","").replace("]","").replace(",","") 
				l=str(str(l).split(' ',6)[4:6]).replace("'","").replace('"','').replace("[","").replace("]","").replace(",","") 
				if len(str(row))>2:     
					item1=QTableWidgetItem(str(row[1])) #address doesn't need checkbox
					item2=QTableWidgetItem(str(row[0])) #id doesn't need checkbox
					checkbox3=QCheckBox(str(j))
					checkbox4=QCheckBox(str(k))	
					checkbox5=QCheckBox(str(l))
					
					checkbox3.setCheckState(Qt.Unchecked)
					checkbox4.setCheckState(Qt.Unchecked)
					checkbox5.setCheckState(Qt.Unchecked)
					
					self.tableWidget.setHorizontalHeaderLabels("poi_id address Category1 Category2 Category3".split())
					self.tableWidget.setItem(rownum,0, item2)
					self.tableWidget.setItem(rownum,1, item1) 
					self.tableWidget.setCellWidget(rownum,2,checkbox3)
					self.tableWidget.setCellWidget(rownum,3,checkbox4)
					self.tableWidget.setCellWidget(rownum,4,checkbox5)
					
				self.tableWidget.resizeColumnsToContents()
					
				rownum=rownum+1	
					
			self.tableWidget.setRowCount(rownum)
		self.tableWidget.cellClicked.connect(self.cell_was_clicked)
			
			
	
	def myupdatebtncliked(self):
		global user_path
		QMessageBox.information(self,"INFO","Select where to save your choices in a csv file")
		user_path=str(QFileDialog.getSaveFileName(self,"Select where to save your CSV choices",("*.csv")))
		user_path=user_path[2:user_path.index("'",4,1000)]
		input_csv = self.choosepoifilefilechoosenfile.text()
		
		with open(user_path ,'w+',newline='', encoding=' utf-8') as myfile ,open(input_csv,'r',newline='', encoding=' utf-8')as inputfile:        
			csv_test_input=csv.reader(inputfile,quoting=csv.QUOTE_MINIMAL,skipinitialspace='True')
			wr=csv.writer(myfile,quoting=csv.QUOTE_MINIMAL,escapechar='\n')
			next(csv_test_input) #ignore csv headers
			wr.writerow(['address','results','x','y'])
			for i in range(self.tableWidget.rowCount()):
				for j in csv_test_input:
					if self.tableWidget.cellWidget(i,2).isChecked(): # i,2 --> category1
						temp=self.tableWidget.cellWidget(i,2).text()
						if("original") in temp:
							temp = str(temp).replace("[","").replace("]","").replace('"','').replace(",","").replace("'","")
							wr.writerow([self.tableWidget.item(i,1).text(),temp,j[1],j[2]])	
						if("arcgis") in temp:
							temp = str(temp).replace("[","").replace("]","").replace('"','').replace(",","").replace("'","")
							wr.writerow([self.tableWidget.item(i,1).text(),temp,j[3],j[4]])	
						if("nominatim") in temp:
							temp = str(temp).replace("[","").replace("]","").replace('"','').replace(",","").replace("'","")
							wr.writerow([self.tableWidget.item(i,1).text(),temp,j[5],j[6]])	
					if self.tableWidget.cellWidget(i,3).isChecked():  #i,3 --> category2
						temp=self.tableWidget.cellWidget(i,3).text()
						if("original") in temp:
							temp = str(temp).replace("[","").replace("]","").replace('"','').replace(",","").replace("'","")
							wr.writerow([self.tableWidget.item(i,1).text(),temp,j[1],j[2]])	
						if ("arcgis") in temp:
							temp = str(temp).replace("[","").replace("]","").replace('"','').replace(",","").replace("'","")
							wr.writerow([self.tableWidget.item(i,1).text() ,temp,j[3],j[4]])
						if("nominatim") in temp:
							temp = str(temp).replace("[","").replace("]","").replace('"','').replace(",","").replace("'","")
							wr.writerow([self.tableWidget.item(i,1).text(),temp,j[5],j[6]])	
					if self.tableWidget.cellWidget(i,4).isChecked(): # i,4 --> category3
						temp=self.tableWidget.cellWidget(i,4).text()
						if("original") in temp:
							temp = str(temp).replace("[","").replace("]","").replace('"','').replace(",","").replace("'","")
							wr.writerow([self.tableWidget.item(i,1).text(),temp,j[1],j[2]])	
						if ("arcgis") in temp:
							temp = str(temp).replace("[","").replace("]","").replace('"','').replace(",","").replace("'","")
							wr.writerow([self.tableWidget.item(i,1).text() ,temp,j[3],j[4]])
						if("nominatim") in temp:
							temp = str(temp).replace("[","").replace("]","").replace('"','').replace(",","").replace("'","")
							wr.writerow([self.tableWidget.item(i,1).text() ,temp,j[5],j[6]])
					break
		myfile.close()
		return user_path		

	def auto_selectbtn_clicked(self): # That button selects the category that has the maximum result and checks the appropriate checkbox in the table 
		csv_predictions = self.last_exp_file() + "\\model_deployment_results\\predictionsrplconverted.csv"
		with open(csv_predictions,'r',newline='',encoding=' utf-8') as csv_results:
			csv_reader = csv.reader(csv_results,quoting=csv.QUOTE_MINIMAL,skipinitialspace='True')
			count=0
			for row in csv_reader:
				a=row[2]
				temp=max(((str(a.split(' ',2)[1:2]).replace("[","").replace("'","").replace("]",""))),((str(a.split(' ',4)[3:4]).replace("[","").replace("'","").replace("]",""))),((str(a.split(' ',6)[5:6]).replace("[","").replace("'","").replace("]",""))))
				print(temp)
				if temp ==((str(a.split(' ',2)[1:2]).replace("[","").replace("'","").replace("]",""))):
					self.tableWidget.cellWidget(count,2).setCheckState(Qt.Checked)
				if temp == ((str(a.split(' ',4)[3:4]).replace("[","").replace("'","").replace("]",""))):	
					self.tableWidget.cellWidget(count,3).setCheckState(Qt.Checked)
				if temp == ((str(a.split(' ',6)[5:6]).replace("[","").replace("'","").replace("]",""))):
					self.tableWidget.cellWidget(count,4).setCheckState(Qt.Checked)
				count+=1	
	def load_user_btn_clicked(self):
		try:	
			QMessageBox.information(self,"INFO","Load User Choices")
			uri_user_choices = "file:///" + user_path + "?delimiter={}&xField={}&yField={}".format(",", "x", "y")
			layer_user_choices = QgsVectorLayer(uri_user_choices, "Roads Classified User Choices", 'delimitedtext') # layer constructor
			if not layer_user_choices.isValid():
				QMessageBox.warning(self,"CAUTION","Layer failed to load")
		
			properties_arcgis = {'style': 'no','width_border': '2.0','color_border': 'purple','style_border' : 'solid'}
			symbol_arcgis = QgsFillSymbol.createSimple(properties_arcgis)
			symbol_arcgis = QgsMarkerSymbol.createSimple({'name': 'triangle', 'color': 'orange'})
			layer_user_choices.setRenderer(QgsSingleSymbolRenderer(symbol_arcgis))
		
			layer_settings_user_choices  = QgsPalLayerSettings()
			layer_settings_user_choices.fieldName = "name"
			layer_settings_user_choices.placement = 1
			layer_settings_user_choices = QgsVectorLayerSimpleLabeling(layer_settings_user_choices)
			layer_user_choices.setLabelsEnabled(True)
			layer_user_choices.setLabeling(layer_settings_user_choices)
		
			config_form_user_choices = layer_user_choices.editFormConfig()
			path_user_choices = QgsApplication.qgisSettingsDirPath() + "\\python\\plugins\\geocoding" 
			uiform_user_choices = path_user_choices + ".\\tableWidget-for-pois-user-choices.ui"
			config_form_user_choices.setUiForm(uiform_user_choices)
			layer_user_choices.setEditFormConfig(config_form_user_choices)
		
			QgsProject.instance().addMapLayer(layer_user_choices)
		except NameError:
			QMessageBox.warning(self,"WARNING","Check pois from results table and press select.Then your choices may be loaded.")
	
	#########################################################################
	#                  Connection table results - Pois in layer             #
	#########################################################################	
	
	def tableWidgetpopup2(self,event):
		self.popupMenu2 = QMenu(self)
		subMenu = QMenu(self.popupMenu2)
		Action2 = QAction("Show current address categories in map",self)
		self.popupMenu2.addAction(Action2)
		
		Action3 = QAction("Go to User's Choice Road",self)
		self.popupMenu2.addAction(Action3)
		
		Action4 = QAction("Go to maximum probability point",self)
		self.popupMenu2.addAction(Action4)
		
		self.popupMenu2.popup(QCursor.pos()) 
		Action2.triggered.connect(self.show_address_categories)
		Action3.triggered.connect(self.goto_user_pois_feature)
		Action4.triggered.connect(self.max_prob_point)
	########################################################
	def max_prob_point(self):
		r=self.tableWidget.selectionModel().currentIndex().row()
		c=self.tableWidget.selectionModel().currentIndex().column()
		
		poi_max = []
		poi_max.append((self.tableWidget.cellWidget(r,2)).text())
		poi_max.append((self.tableWidget.cellWidget(r,3)).text())
		poi_max.append((self.tableWidget.cellWidget(r,4)).text())
		for i in poi_max:
			result = list(map(lambda i: float(i.replace("arcgis ","").replace("nominatim ","").replace("original ","").replace(" ","").replace("'","")), poi_max))
			
		# result has only the float results (numbers)
		# poi_max has all categories
		if str(max((result))) in str((self.tableWidget.cellWidget(r,2).text())):
			temp111=(self.tableWidget.cellWidget(r,2).text())
			temp111=str(temp111.replace(",",""))
			QMessageBox.information(self,"INFO","Max is: %s"%temp111,QMessageBox.Close)
			self.tableWidget.cellWidget(r,2).setCheckState(Qt.Checked)
			answer_msg = QMessageBox.question(self,"REDIRECTION","Redirect to max poi in map?",QMessageBox.Yes | QMessageBox.No)
			user_click = self.select_from_tableWidget()
			if answer_msg== QMessageBox.Yes:
				alllayers = self.myiface.mapCanvas().layers()
				for layer in alllayers:
					temp112= str(temp111.split()[:1]).replace("'","").replace("[","").replace("]","")
					QMessageBox.information(self,"INFO","HERE")
					if  "OpenStreetMap" in str(layer.name()):
						continue					
					elif "Roads Classified (nominatim)" in str(layer.name()):
						QMessageBox.information(self,"INFO","nominatim")
						if (temp112) in str(layer.name()):											
							current_Layer=layer																		
							current_Layer.removeSelection()																	
							current_Layer.selectByExpression("\"address\" = '{}'".format(user_click),QgsVectorLayer.SetSelection)	
							box = current_Layer.boundingBoxOfSelected()																	
							self.myiface.mapCanvas().setExtent(box)																	
							canvas = qgis.utils.iface.mapCanvas()
							canvas.zoomToSelected(current_Layer) 
							print("Categ 1 zoom nominatim")
					elif "Roads Classified (arcgis)" in str(layer.name()):
						QMessageBox.information(self,"INFO","arcgis")
						if (temp112) in str(layer.name()):
							current_Layer=layer
							current_Layer.removeSelection()
							current_Layer.selectByExpression("\"address\" = '{}'".format(user_click),QgsVectorLayer.SetSelection)
							box = current_Layer.boundingBoxOfSelected()
							self.myiface.mapCanvas().setExtent(box)
							canvas = qgis.utils.iface.mapCanvas()
							canvas.zoomToSelected(current_Layer)
					elif "Roads Classified (original)" in str(layer.name()):
						QMessageBox.information(self,"INFO","original")
						if (temp112) in str(layer.name()):
							QMessageBox.information(self,"INFO","-----")
							current_Layer=layer
							current_Layer.removeSelection()
							current_Layer.selectByExpression("\"address\" = '{}'".format(user_click),QgsVectorLayer.SetSelection)
							box = current_Layer.boundingBoxOfSelected()
							self.myiface.mapCanvas().setExtent(box)
							canvas = qgis.utils.iface.mapCanvas()
							canvas.zoomToSelected(current_Layer)
							print("Categ 1 zoom original")
					else:
						QMessageBox.warning(self,"Loaded Layers","Redirection to poi in layer failed.Please load the layer.",QMessageBox.Yes)
						break
			else:
				pass
		if str(max((result))) in str((self.tableWidget.cellWidget(r,3).text())):
			temp111=(self.tableWidget.cellWidget(r,3).text())
			QMessageBox.information(self,"INFO","Max is: %s"%temp111)
			self.tableWidget.cellWidget(r,3).setCheckState(Qt.Checked)
			answer_msg = QMessageBox.question(self,"REDIRECTION","Redirect to max poi in map?",QMessageBox.Yes | QMessageBox.No)
			user_click = self.select_from_tableWidget()
			if answer_msg== QMessageBox.Yes:
				alllayers = self.myiface.mapCanvas().layers()
				for layer in alllayers:
					temp112= str(temp111.split()[:1])
					if "OpenStreetMap" in str(layer.name()):
						continue
					if "Roads Classified (nominatim)" in str(layer.name()):
						if (temp112) in str(layer.name()):											
							current_Layer=layer																		
							current_Layer.removeSelection()																	
							current_Layer.selectByExpression("\"address\" = '{}'".format(user_click),QgsVectorLayer.SetSelection)	
							box = current_Layer.boundingBoxOfSelected()																	
							self.myiface.mapCanvas().setExtent(box)																	
							canvas = qgis.utils.iface.mapCanvas()
							canvas.zoomToSelected(current_Layer) 
							print("Categ 2 zoom nominatim")
					if "Roads Classified (arcgis)" in str(layer.name()):
						if (temp112) in str(layer.name()):
							current_Layer=layer
							current_Layer.removeSelection()
							current_Layer.selectByExpression("\"address\" = '{}'".format(user_click),QgsVectorLayer.SetSelection)
							box = current_Layer.boundingBoxOfSelected()
							self.myiface.mapCanvas().setExtent(box)
							canvas = qgis.utils.iface.mapCanvas()
							canvas.zoomToSelected(current_Layer)
							print("Categ 2 zoom arcgis")
					if "Roads Classified (original)" in str(layer.name()):
						if (temp112) in str(layer.name()):
							current_Layer=layer
							current_Layer.removeSelection()
							current_Layer.selectByExpression("\"address\" = '{}'".format(user_click),QgsVectorLayer.SetSelection)
							box = current_Layer.boundingBoxOfSelected()
							self.myiface.mapCanvas().setExtent(box)
							canvas = qgis.utils.iface.mapCanvas()
							canvas.zoomToSelected(current_Layer)
							print("Categ 2 zoom original")
					else:
						QMessageBox.warning(self,"Loaded Layers","Redirection to poi in layer failed.Please load the layer.",QMessageBox.Yes)
						break
			else:
				pass
		if str(max((result))) in str((self.tableWidget.cellWidget(r,4).text())):
			temp111=(self.tableWidget.cellWidget(r,4).text())
			QMessageBox.information(self,"INFO","Max is: %s"%temp111)
			self.tableWidget.cellWidget(r,4).setCheckState(Qt.Checked)
			answer_msg = QMessageBox.question(self,"REDIRECTION","Redirect to max poi in map?",QMessageBox.Yes | QMessageBox.No)
			user_click = self.select_from_tableWidget()
			if answer_msg== QMessageBox.Yes:
				alllayers = self.myiface.mapCanvas().layers()
				for layer in alllayers:
					temp112= str(temp111.split()[:1])
					if "OpenStreetMap" in str(layer.name()):
						continue					
					if "Roads Classified (nominatim)" in str(layer.name()):
						if (temp112) in str(layer.name()):											
							current_Layer=layer																		
							current_Layer.removeSelection()																	
							current_Layer.selectByExpression("\"address\" = '{}'".format(user_click),QgsVectorLayer.SetSelection)	
							box = current_Layer.boundingBoxOfSelected()																	
							self.myiface.mapCanvas().setExtent(box)																	
							canvas = qgis.utils.iface.mapCanvas()
							canvas.zoomToSelected(current_Layer) 
							print("Categ 3 zoom nominatim")
					if "Roads Classified (arcgis)" in str(layer.name()):
						if (temp112) in str(layer.name()):
							current_Layer=layer
							current_Layer.removeSelection()
							current_Layer.selectByExpression("\"address\" = '{}'".format(user_click),QgsVectorLayer.SetSelection)
							box = current_Layer.boundingBoxOfSelected()
							self.myiface.mapCanvas().setExtent(box)
							canvas = qgis.utils.iface.mapCanvas()
							canvas.zoomToSelected(current_Layer)
							print("Categ 3 zoom arcgis")
					if "Roads Classified (original)" in str(layer.name()):
						if (temp112) in str(layer.name()):
							current_Layer=layer
							current_Layer.removeSelection()
							current_Layer.selectByExpression("\"address\" = '{}'".format(user_click),QgsVectorLayer.SetSelection)
							box = current_Layer.boundingBoxOfSelected()
							self.myiface.mapCanvas().setExtent(box)
							canvas = qgis.utils.iface.mapCanvas()
							canvas.zoomToSelected(current_Layer)
							print("Categ 3 zoom original")
					else:
						QMessageBox.warning(self,"Loaded Layers","Redirection to poi in layer failed.Please load the layer.",QMessageBox.Yes)
						break
			else:
				pass
		QWidget.update(self)
	
	def select_from_tableWidget(self):
		r=self.tableWidget.selectionModel().currentIndex().row()
		c=self.tableWidget.selectionModel().currentIndex().column()
		return self.tableWidget.item(r,1).text() # .item(r,1).text --> refers to address(r,1)
	def goto_user_pois_feature(self):
		address = self.select_from_tableWidget()
		alllayers = self.myiface.mapCanvas().layers()
		layer_names=[]
		for layer in alllayers:
			layer_names.append(layer.name())
			if ((layer.name()) == "Roads Classified User Choices"):
				current_Layer=layer
				current_Layer.removeSelection()
				current_Layer.selectByExpression("\"address\" = '{}'".format(address),QgsVectorLayer.SetSelection)
				box = current_Layer.boundingBoxOfSelected()
				self.myiface.mapCanvas().setExtent(box)
				canvas = qgis.utils.iface.mapCanvas()
				canvas.zoomToSelected(current_Layer) 
				self.myiface.mapCanvas().refresh()
		if ("Roads Classified User Choices" not in layer_names):
			QMessageBox.warning(self,"CAUTION","User choices should be loaded first")
	def show_address_categories(self):
		user_click = self.select_from_tableWidget()		
		loaded_layers = self.myiface.mapCanvas().layers() #all current loaded layers		
		for layer in loaded_layers:												   
			if ((layer.name()) == "Roads Classified (nominatim)"):			#if nominatim is loaded zoom to nominatim										
				current_Layer=layer																		
				current_Layer.removeSelection()																	
				current_Layer.selectByExpression("\"address\" = '{}'".format(user_click),QgsVectorLayer.SetSelection)	
				box = current_Layer.boundingBoxOfSelected()																	
				self.myiface.mapCanvas().setExtent(box)																	
				canvas = qgis.utils.iface.mapCanvas()
				canvas.zoomToSelected(current_Layer) 
			if ((layer.name()) == "Roads Classified (arcgis)"):			#if arcgis is loaded zoom to arcgis
				current_Layer=layer
				current_Layer.removeSelection()
				current_Layer.selectByExpression("\"address\" = '{}'".format(user_click),QgsVectorLayer.SetSelection)
				box = current_Layer.boundingBoxOfSelected()
				self.myiface.mapCanvas().setExtent(box)
				canvas = qgis.utils.iface.mapCanvas()	
				canvas.zoomToSelected(current_Layer)
			if ((layer.name()) == "Roads Classified (original)"):		#if original is loaded zoom to original
				current_Layer=layer											
				current_Layer.removeSelection()											
				current_Layer.selectByExpression("\"address\" = '{}'".format(user_click),QgsVectorLayer.SetSelection)
				box = current_Layer.boundingBoxOfSelected()
				self.myiface.mapCanvas().setExtent(box)
				canvas = qgis.utils.iface.mapCanvas()
				canvas.zoomToSelected(current_Layer)
		self.myiface.mapCanvas().refresh()		
		if (("Roads Classified (nominatim)" not in loaded_layers) and ("Roads Classified (arcgis)" not in loaded_layers) and ("Roads Classified (original)" not in loaded_layers)):
			QMessageBox.information(self,"INFO","Please load classification results first.")


			
