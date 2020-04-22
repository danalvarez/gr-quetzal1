# ----------------------------------------------------------------------
# Titulo: Pantalla_RAM.py
# Autor: Aldo Aguilar Nadalini
# Fecha: 19 de abril de 2020
# Descripcion: Pantalla que despliega datos guardados en memoria RAM de
#              Quetzal-1
# ----------------------------------------------------------------------

# Librerias ------------------------------------------------------------

# Local libraries
from PyQt5 import QtCore, QtGui, QtWidgets

# Own libraries
from Qt_RAM import Ui_Dialog

# **********************************************************************
#               CLASE DE PANTALLA DE PARAMETROS RAM
# **********************************************************************

# Pantalla de parametros RAM hereda de QDialog y Ui_Dialog (Qt
# Designer)
class Pantalla_RAM(QtWidgets.QDialog, Ui_Dialog):
	"""
	Clase que engloba las funcionalidades de la pantalla de parametros
	guardados en memoria RAM de satelite Quetzal-1

	Atributos
	----------
	None

	Métodos
	-------
	update_LCD(beacon_data)
		Funcion para actualizar datos de pantalla de parametros RAM
	"""

	def __init__(self, *args, parent=None):
		"""
		Constructor

		Parametros
		----------
		args : varios
			Parametros varios
		parent : None
			Parent class de ventana
		"""

		QtWidgets.QDialog.__init__(self, parent)

		# Configuracion estetica de Dialog
		self.setupUi(self)
		self.setStyleSheet("#Dialog { border-image: url(./resources/background.jpg) 0 0 0 0 stretch stretch; }")
		self.setWindowIcon(QtGui.QIcon('./resources/emblema_Quetzal-1.png'))       # Configurar imagen de fondo e icono de aplicacion
		self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)    		   # Deshabilitar opcion de maximizado de ventana

		# Resize de ventana (47.5% de ancho de pantalla, 60% de alto de
		# pantalla)
		screen = QtWidgets.QDesktopWidget().screenGeometry(-1)
		if (screen.width() > 1500):
			width_factor = 0.4
			height_factor = 0.475
		else:
			width_factor = 0.475
			height_factor = 0.6
		#self.setFixedSize(QtCore.QSize(screen.width() * width_factor, screen.height() * height_factor))
		self.resize(QtCore.QSize(parent.frameGeometry().width() * width_factor, parent.frameGeometry().height() * height_factor))

		# Centrado de ventana en pantalla
		qr = self.frameGeometry()
		cp = QtWidgets.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def update_LCD(self, beacon_data):
		"""
		Funcion para actualizar datos de pantalla de parametros RAM

		ACTIVADO POR: Llamada externa de funcion

		Parametros
		----------
		beacon_data : list
			Listado de datos de beacon de Quetzal-1
		"""

		self.lcdNumber.display(beacon_data[61])
		self.lcdNumber_2.display(beacon_data[62])
		self.lcdNumber_3.display(beacon_data[63])
		self.lcdNumber_4.display(beacon_data[64])
		self.lcdNumber_5.display(beacon_data[65])
		self.lcdNumber_6.display(beacon_data[66])
		self.lcdNumber_7.display(beacon_data[67])
		self.lcdNumber_8.display(beacon_data[68])
		self.lcdNumber_9.display(beacon_data[69])
		self.lcdNumber_10.display(beacon_data[70])
		self.lcdNumber_11.display(beacon_data[71])
		self.lcdNumber_12.display(beacon_data[72])
		self.lcdNumber_13.display(beacon_data[73])
		self.lcdNumber_14.display(beacon_data[74])
		self.lcdNumber_15.display(beacon_data[75])
		self.lcdNumber_16.display(beacon_data[76])
		self.lcdNumber_17.display(beacon_data[77])
		self.lcdNumber_18.display(beacon_data[78])
		self.lcdNumber_19.display(beacon_data[79])
		self.lcdNumber_20.display(beacon_data[80])
		self.lcdNumber_21.display(beacon_data[81])
		self.lcdNumber_22.display(beacon_data[82])

# ----------------------------------------------------------------------
