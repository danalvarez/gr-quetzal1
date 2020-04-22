# ----------------------------------------------------------------------
# Titulo: Pantalla_CDHS.py
# Autor: Aldo Aguilar Nadalini
# Fecha: 19 de abril de 2020
# Descripcion: Pantalla de telemetria CDHS de Quetzal-1
# ----------------------------------------------------------------------

# Librerias ------------------------------------------------------------

# Local libraries
from PyQt5 import QtCore, QtGui, QtWidgets

# Own libraries
from Qt_CDHS import Ui_Dialog

# **********************************************************************
#               CLASE DE PANTALLA DE TELEMETRIA CDHS
# **********************************************************************

# Pantalla de CDHS hereda de QDialog y Ui_Dialog (Qt Designer)
class Pantalla_CDHS(QtWidgets.QDialog, Ui_Dialog):
	"""
	Clase que engloba las funcionalidades de la pantalla de telemetria
	de modulo CDHS de Quetzal-1

	Atributos
	----------
	None

	Métodos
	-------
	update_LCD(beacon_data)
		Funcion para actualizar datos de telemetria desplegados en
		ventana de CDHS
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

		# Resize de ventana (97.5% de ancho de pantalla, 90% de alto de
		# pantalla)
		screen = QtWidgets.QDesktopWidget().screenGeometry(-1)
		if (screen.width() > 1500):
			width_factor = 0.375
			height_factor = 0.3
		else:
			width_factor = 0.45
			height_factor = 0.375
		#self.setFixedSize(QtCore.QSize(screen.width() * width_factor, screen.height() * height_factor))
		self.resize(QtCore.QSize(parent.frameGeometry().width() * width_factor, parent.frameGeometry().height() * height_factor))

		# Centrado de ventana en pantalla
		qr = self.frameGeometry()
		cp = QtWidgets.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def update_LCD(self, beacon_data):
		"""
		Funcion para actualizar datos de telemetria desplegados en
		ventana de CDHS

		ACTIVADO POR: Llamado externo de funcion

		Parametros
		----------
		beacon_data : list
			Listado de datos de beacon de Quetzal-1
		"""

		self.lcdNumber.display(beacon_data[11])
		self.lcdNumber_2.display(beacon_data[12])
		self.lcdNumber_3.display(beacon_data[13])
		self.lcdNumber_4.display(beacon_data[14])
		self.lcdNumber_5.display(beacon_data[15])
		self.lcdNumber_6.display(beacon_data[16])

# ----------------------------------------------------------------------
