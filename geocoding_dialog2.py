from PyQt5 import uic
from PyQt5 import QtWidgets
from multiprocessing import Process
from PyQt5 import QtCore, QtWidgets,uic
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QMenu,QAction
from PyQt5.QtWidgets import QPushButton,QFileDialog,QProgressDialog,QProgressBar,QApplication,QMainWindow
from PyQt5.QtWidgets import QMessageBox,QDialog
from PyQt5.QtCore import QSize,QTimer,QThread, pyqtSignal
from PyQt5.QtGui import *  
from PyQt5.QtCore import *  
from qgis.utils import iface
from PyQt5 import QtCore,QtGui,QtWidgets
from qgis.core import *
from qgis.gui import *
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
import  os,time,datetime,subprocess,datetime,csv,sys

FORM_CLASS, _ = uic.loadUiType(os.path.join(
	os.path.dirname(__file__), 'geocoding_dialog_base2.ui'))

class geo_coding_dialog_base2(QtWidgets.QDialog, FORM_CLASS):
	def __init__(self,myiface,parent=None):
		super(geo_coding_dialog_base2, self).__init__(parent)
		self.myiface=myiface
		self.setupUi(self)
		self.clasifiercomboBoxfillcomboBox(self.clasifiercomboBox)
		self.feature_extractionbtn.clicked.connect(self.feature_extractionbtn_clicked)
		self.choose_train_data_btn.clicked.connect(self.choose_train_data_btnclicked)
		self.experiment_path_btn.clicked.connect(self.experiment_path_btnclicked)
		self.algorithm_selectionbtn.clicked.connect(self.algorithm_selectionbtn_clicked)
		self.model_selectionbtn.clicked.connect(self.model_selectionbtn_clicked)
		self.model_trainingbtn.clicked.connect(self.model_trainingbtn_clicked)
	##################################
	#   MODEL    TRAINING    SECTION 
	##################################
	def experiment_path_btnclicked(self):     
		exp_file_dir = QFileDialog()
		exp_file_str = exp_file_dir.getExistingDirectory(self,"Select experiment folder path",os.getcwd(),QFileDialog.ShowDirsOnly)
		self.experiment_path_file.setText(exp_file_str)
		while exp_file_str=='':
			no_exp_path_msg = 'Experiment path not selected. Please choose an experiment path file to proceed '
			QMessageBox.warning(self,"CAUTION",no_exp_path_msg)
			break	
	def choose_train_data_btnclicked(self):
		try:
			QMessageBox.information(self,"INFO","Please select train data file (.csv)")
			train_file_dir = QFileDialog()
			mfullstr=str(train_file_dir.getOpenFileName(self,"Select CSV File ",os.getcwd())) 
			fname=mfullstr[2:mfullstr.index("'", 4, 1000)]
			self.train_data_chosenfile.setText(fname)
		except FileNotFoundError:
			QMessageBox.warning(self,"CAUTION","No train data specified")
			self.train_data_chosenfile.clear()
	def feature_extractionbtn_clicked(self):
		progress = QProgressBar()
		progress.setGeometry(200, 80, 250, 20)
		progress.move(600,600)
		progress.setWindowTitle('Processing..')
		progress.setAlignment(QtCore.Qt.AlignCenter)
		progress.show()
		fpath = self.train_data_chosenfile.text()
		fpath = fpath.replace("//","\\")
		pythonexepath= os.environ['PYTHONHOME'] + '\\python.exe'
		os.chdir('.\\LGM-Geocoding-master')
		command = f'python features_extraction.py -fpath {fpath}'
		try:
			output = subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT)
		except subprocess.CalledProcessError:
			print(stderr)
			QMessageBox.warning(self,"WARNING",str(stderr))		
		QMessageBox.information(self,"INFO",str(output))
	def algorithm_selectionbtn_clicked(self):
		progress = QProgressBar()
		progress.setGeometry(200, 80, 250, 20)
		progress.move(600,600)
		progress.setWindowTitle('Processing..')
		progress.setAlignment(QtCore.Qt.AlignCenter)
		progress.show()
		time.sleep(1)
		exp_path = self.experiment_path_file.text() + "\\"
		if "LGM-Geocoding-master" in str(os.getcwd()):
			pass
		else:
			os.chdir('.\\LGM-Geocoding-master')
		command = f'python algorithm_selection.py -experiment_path {exp_path}'
		print(command)
		try:
			output = subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT)
		except subprocess.CalledProcessError:
			print(stderr)
			QMessageBox.warning(self,"WARNING",str(output))
		QMessageBox.information(self,"OUTPUT",str(output))
	def model_selectionbtn_clicked(self):
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
		exp_path = self.experiment_path_file.text() + "\\"
		theclassifierstr=self.clasifiercomboBox.itemText(self.clasifiercomboBox.currentIndex())
		command = f'python model_selection.py -classifier {theclassifierstr} -experiment_path {exp_path}'
		try:
			output = subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT)
		except subprocess.CalledProcessError:
			print(stderr)
			QMessageBox.warning(self,"WARNING",str(output))		
		QMessageBox.information(self,"INFO",str(output))
		
	def clasifiercomboBoxfillcomboBox(self,componame):
		componame.addItem ("\"Baseline\"")
		componame.addItem ("\"NaiveBayes\"")
		componame.addItem ("NearestNeighbors")	
		componame.addItem ("\"LogisticRegression\"") 	
		componame.addItem ("SVM") 
		componame.addItem ("MLP") 	
		componame.addItem ("\"DecisionTree\"") 	
		componame.addItem ("\"RandomForest")	
		componame.addItem ("\"ExtraTrees\"")			
		
	def model_trainingbtn_clicked(self):
		progress = QProgressBar()
		progress.setGeometry(200, 80, 250, 20)
		progress.move(600,600)
		progress.setWindowTitle('Processing..')
		progress.setAlignment(QtCore.Qt.AlignCenter)
		progress.show()
		exp_path = self.experiment_path_file.text() + "\\"
		command = f'python model_training.py  -experiment_path {exp_path}'
		if "LGM-Geocoding-master" in str(os.getcwd()):
			pass
		else:
			os.chdir('.\\LGM-Geocoding-master')		
		try:
			output = subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT)
		except subprocess.CalledProcessError:
			QMessageBox.warning(self,"WARNING",str(output))
		QMessageBox.information(self,"INFO",str(output))



