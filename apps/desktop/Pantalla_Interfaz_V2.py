# ----------------------------------------------------------------------
# Titulo: Pantalla_Interfaz_V2.py
# Autor: Aldo Aguilar Nadalini
# Fecha: 20 de abril de 2020
# Descripcion: Interfaz grafica para procesar datos HEX de beacons
#              recolectados de nanosatelite Quetzal-1 (Primer satelite
#              guatemalteco)
# ----------------------------------------------------------------------

# Librerias ------------------------------------------------------------

# Local libraries
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QLineEdit, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from datetime import datetime
from collections import deque

# Thrird-party libraries
import pyqtgraph as pg
import zmq

# Own libraries
import Modulo_HEX as mh
from Pantalla_CDHS import Pantalla_CDHS
from Pantalla_RAM import Pantalla_RAM
from Qt_Interfaz import Ui_MainWindow

# **********************************************************************
#               CLASE DE PANTALLA DE INTERFAZ QUETZAL-1
# **********************************************************************

# Pantalla de interfaz hereda de QMainWindow y Ui_MainWindow (Qt
# Designer)
class Pantalla_Interfaz(QtWidgets.QMainWindow, Ui_MainWindow):
	"""
	Clase que engloba las funcionalidades de la pantalla de la interfaz
	grafica para procesar la telemetria recibida del nanosatelite 1U
	Quetzal-1 (primer satelite guatemalteco)

	Atributos
	----------
	current_time : str
		Tiempo actual 'hh-mm-ss'
	current_date : str
		Fecha actual 'yyyy-MM-dd'
	selected_port : bool
		Bandera de puerto TCP seleccionado
	hexSelected : bool
		Bandera de HEX File seleccionado
	playHex : bool
		Bandera de Comenzar en estado PLAY GUI
	steppingBackwards : bool
		Bandera de Estado RETROCEDER GUI
	pen : pyqtgraph.pen
		Marcador para pintar graficas en interfaz
	beacon_counter : int
		Contador No.1 de beacon (cuenta individualmente cada dato de
		beacon)
	num_beacon : int
		Contador No.2 de beacon (cuenta cada paquete de beacon leido)
	beacon_data : list
		Variable que almacena los datos de beacon procesados de linea de
		archivo o linea recibida por puerto TCP

	Métodos
	-------
	connect_slots()
		Realizar conexion de seniales de modificacion de campos en
		ventana con slots de diferentes funciones de clase
	configurar_graficas()
		Funcion para ejecutar la configuracion de las GraphicsView para
		que desplieguen correctamente las graficas de los datos de
		telemetria del satelite
	step_backwards()
		Funcion que permite regresar a linea anterior de datos de
		telemetria leidos desde archivo .dat. Esto es posible cuando la
		interfaz se encuentra en Modo Manual (Boton de pausa presionado)
	toggle_play_pausa()
		Funcion para cambiar entre Modo Manual (pausa) y Modo Automatico
		(play) de interpretacion de los datos procesados del archivo
		.dat. Si se encuentra en Modo Manual, se puede regresar o
		avanzar en los datos del archivo utilizando el boton Step
		Backwards y Step Forwards. En Modo Automatico, se va iterando
		a travez de todos los datos del archivo utilizando el timer (1s)
	step_forward()
		Funcion que permite avanzar a linea siguiente de datos de
		telemetria leidos desde archivo .dat. Esto es posible cuando la
		interfaz se encuentra en Modo Manual (Boton de pausa presionado)
	select_HEX()
		Funcion para realizar la seleccion del archivo .dat del cual se
		extraen los datos HEX de telemetria del satelite para su
		despliegue en la interfaz grafica
	abrir_parametros_RAM()
		Funcion para desplegar ventana en donde se muestran los
		parametros guardados en memoria RAM del satelite
	abrir_telemetria_CDHS()
		Funcion para desplegar ventana en donde se muestran los
		datos de telemetria del modulo CDHS (On-board computer)
	reset_HEX()
		Funcion para comenzar a desplegar datos de telemetria del
		satelite nuevamente desde el principio del documento .dat
		procesado
	conectar_puerto()
		Funcion para realizar la conexion a un puerto TCP para la
		recepcion de datos de telemetria de Quetzal-1 ya decodificados
		por AX25 Decode
	update_incoming_beacon(beacon)
		Funcion para cargar datos recibidos por puerto TCP a funcion
		de parsing de los datos para su consecuente despliegue en GUI
	updatedata()
		Funcion para lectura automatica de cada linea en archivo .dat
		y su procesamiento antes de desplegar la telemetria en interfaz
	update_GUI()
		Funcion para actualizar los datos desplegados en widgets de
		interfaz grafica. Se cargan los datos procesados en updatedata()
		si interfaz se encuentra en Modo Automatico. De lo contrario,
		se cargan los datos procesados en step_backwards() o
		step_forward() en Modo Manual
	"""

	def __init__(self, args, parent=None):
		"""
		Constructor

		Parametros
		----------
		args : varios
			Parametros varios
		parent : None
			Parent class de ventana
		"""

		QtWidgets.QMainWindow.__init__(self, parent)

		# Configuracion estetica de MainWindow
		self.setupUi(self)
		self.setStyleSheet("#MainWindow { border-image: url(./resources/background.jpg) 0 0 0 0 stretch stretch; }")
		self.setWindowIcon(QtGui.QIcon('./resources/emblema_Quetzal-1.png'))       # Configurar imagen de fondo e icono de aplicacion
		self.windows_icon = QtGui.QIcon('./resources/emblema_Quetzal-1.png')

		_maximizado = False
		if (_maximizado == False):
			# Resize de ventana (97.5% de ancho de pantalla, 90% de alto
			# de pantalla)
			screen = QtWidgets.QDesktopWidget().screenGeometry(-1)
			if (screen.width() > 1500):
				width_factor = 0.90
				height_factor = 0.85
			else:
				width_factor = 0.975
				height_factor = 0.90
			#self.setFixedSize(QtCore.QSize(screen.width() * width_factor, screen.height() * height_factor))
			self.resize(QtCore.QSize(screen.width() * width_factor, screen.height() * height_factor))
			self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)

			# Centrado de ventana en pantalla
			qr = self.frameGeometry()
			cp = QtWidgets.QDesktopWidget().availableGeometry().center()
			qr.moveCenter(cp)
			self.move(qr.topLeft())
		else:
			self.showMaximized()
			self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)    		# Deshabilitar opcion de maximizado de ventana

		# Inicializacion de variables de clase
		now = datetime.now()
		self.current_time = now.strftime("%H:%M:%S")                    # Obtener tiempo actual
		self.current_date = now.strftime("%Y-%m-%d")                    # Obtener fecha actual
		self.selected_port = False									    # Puerto aun no seleccionado
		self.hexSelected = False           								# HEX File aun no seleccionado
		self.playHex = True                								# Comenzar en estado PLAY GUI
		self.steppingBackwards = False     								# Estado RETROCEDER GUI desactivado
		C = pg.hsvColor(0.3,1.0,1.0)
		self.pen = pg.mkPen(color = C,width = 2.5)						# Marcador para pintar graficas en interfaz
		self.beacon_counter = 0                                         # Contador No.1 de beacon (cuenta individualmente cada dato de beacon)
		self.num_beacon = 0                                             # Contador No.2 de beacon (cuenta cada paquete de beacon leido)
		self.beacon_data = 0											# Variable que almacena los datos de beacon procesados de linea de archivo o linea recibida por puerto TCP

		# CDHS Dialog
		self.pantalla_CDHS = Pantalla_CDHS(parent=self)

		# RAM Dialog
		self.pantalla_RAM = Pantalla_RAM(parent=self)

		# Configuracion de timer que actualiza data
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.updatedata)
		self.timer.start(args.interval)

		# Comenzar con todos los botones desactivados (excepto Select
		# HEX y Conectar a puerto)
		self.pushButton.setEnabled(False)
		self.pushButton_2.setEnabled(False)
		self.pushButton_3.setEnabled(False)
		self.pushButton_5.setEnabled(False)
		self.pushButton_6.setEnabled(False)
		self.pushButton_7.setEnabled(False)

		# Ejecutar conexion de seniales
		self.connect_slots()

		# Configuracion de graficas
		self.configurar_graficas()
		print('Starting QUETZAL-1 UHF Desktop')

	def connect_slots(self):
		"""
		Funcion para conectar seniales a botones de ventana

		ACTIVADO POR: Constructor
		"""

		self.pushButton.clicked.connect(self.step_backwards)
		self.pushButton_2.clicked.connect(self.toggle_play_pausa)
		self.pushButton_3.clicked.connect(self.step_forward)
		self.pushButton_4.clicked.connect(self.select_HEX)
		self.pushButton_5.clicked.connect(self.abrir_parametros_RAM)
		self.pushButton_6.clicked.connect(self.abrir_telemetria_CDHS)
		self.pushButton_7.clicked.connect(self.reset_HEX)
		self.pushButton_8.clicked.connect(self.conectar_puerto)

	def configurar_graficas(self):
		"""
		Funcion para ejecutar la configuracion de las GraphicsView para
		que desplieguen correctamente las graficas de los datos de
		telemetria del satelite

		ACTIVADO POR: Constructor
		"""

		# Inicializar fondo negro y graficas verde claro
		pg.setConfigOption('background', 'k')
		pg.setConfigOption('foreground', 'g')

		# Configuracion de Grafica No.1 (Voltaje de Solar Channel)
		self.graphicsView = pg.PlotWidget(self.centralwidget)
		self.gridLayout_4.addWidget(self.graphicsView, 1, 0, 1, 1)
		self.graphicsView.setObjectName("graphicsView")
		self.graphicsView.showGrid(x = True, y = True)
		self.graphicsView.setYRange(3,5)
		ax = self.graphicsView.getAxis('left')
		ax.setTicks([[(3, '3.0'), (3.5, '3.5'), (4, '4.0'), (4.5, '4.5'), (5.0, '5.0')]])
		self.curve = self.graphicsView.plot()
		self.L = deque([0], maxlen = 50)
		self.t = deque([0], maxlen = 50)
		self.graphicsView.setLabel('bottom','- V')

		# Configuracion de Grafica No.2 (Corriente de Solar Channel)
		self.graphicsView_2 = pg.PlotWidget(self.centralwidget)
		self.gridLayout_4.addWidget(self.graphicsView_2, 1, 1, 1, 1)
		self.graphicsView_2.setObjectName("graphicsView_2")
		self.graphicsView_2.showGrid(x = True, y = True)
		self.graphicsView_2.setYRange(0,1500)
		ax_2 = self.graphicsView_2.getAxis('left')
		ax_2.setTicks([[(0, '0'), (250, '250'), (500, '500'), (750, '750'), (1000, '1000'), (1250, '1250'), (1500, '1500'), (1750, '1750')]])
		self.curve_2 = self.graphicsView_2.plot()
		self.L_2 = deque([0], maxlen = 50)
		self.t_2 = deque([0], maxlen = 50)
		self.graphicsView_2.setLabel('bottom','- mA')

		# Configuracion de Grafica No.3 (Voltaje de 3V3 Channel)
		self.graphicsView_3 = pg.PlotWidget(self.centralwidget)
		self.gridLayout_4.addWidget(self.graphicsView_3, 1, 2, 1, 1)
		self.graphicsView_3.setObjectName("graphicsView_3")
		self.graphicsView_3.showGrid(x = True, y = True)
		self.graphicsView_3.setYRange(3,5)
		ax_3 = self.graphicsView_3.getAxis('left')
		ax_3.setTicks([[(3, '3.0'), (3.5, '3.5'), (4, '4.0'), (4.5, '4.5'), (5.0, '5.0')]])
		self.curve_3 = self.graphicsView_3.plot()
		self.L_3 = deque([0], maxlen = 50)
		self.t_3 = deque([0], maxlen = 50)
		self.graphicsView_3.setLabel('bottom','- V')

		# Configuracion de Grafica No.4 (Corriente de 3V3 Channel)
		self.graphicsView_4 = pg.PlotWidget(self.centralwidget)
		self.gridLayout_4.addWidget(self.graphicsView_4, 1, 3, 1, 1)
		self.graphicsView_4.setObjectName("graphicsView_4")
		self.graphicsView_4.showGrid(x = True, y = True)
		self.graphicsView_4.setYRange(0,1500)
		ax_4 = self.graphicsView_4.getAxis('left')
		ax_4.setTicks([[(0, '0'), (250, '250'), (500, '500'), (750, '750'), (1000, '1000'), (1250, '1250'), (1500, '1500'), (1750, '1750')]])
		self.curve_4 = self.graphicsView_4.plot()
		self.L_4 = deque([0], maxlen = 50)
		self.t_4 = deque([0], maxlen = 50)
		self.graphicsView_4.setLabel('bottom','- mA')

	# ---------------------- FUNCIONES DE BOTONES ----------------------

	def step_backwards(self):
		"""
		Funcion que permite regresar a linea anterior de datos de
		telemetria leidos desde archivo .dat. Esto es posible cuando la
		interfaz se encuentra en Modo Manual (Boton de pausa presionado)

		ACTIVADO POR: Click en Step Backwards |<
		"""

		# Ejecutar accion si modo manual esta activado
		if (self.hexSelected == True and self.playHex == False):

			# Reactivar boton de step-forward
			self.pushButton_3.setEnabled(True)

			# FakeBeacon para capturar datos desechados de las graficas
			# y lograr que se vuelvan a agregar al inicio de la misma
			# simulando efecto de retroceso
			fakebeacon_counter = self.beacon_counter - (51 * self.beacon_length)
			num_fakebeacon = self.num_beacon - 51

			# Si ya no hay datos para retroceder, no actualizar
			# FakeBeacon
			self.stopAddingFakebeacon = False
			if (num_fakebeacon < 0):
				self.stopAddingFakebeacon = True

			# Movimiento de lectura en retroceso de beacon a travez de
			# HEX
			self.beacon_counter = self.beacon_counter - (2 * self.beacon_length)
			self.num_beacon = self.num_beacon - 2

			# Si aun quedan beacons para retroceder
			if (self.num_beacon >= 0):
				# Lectura de HEX
				self.beacon_data = mh.beacon_decode(self.hex_list, self.beacon_counter, self.num_beacon, False)
				self.fakebeacon_data = 0
				if (self.stopAddingFakebeacon == False):
					self.fakebeacon_data = mh.beacon_decode(self.hex_list, fakebeacon_counter, num_fakebeacon, False)

				# Actualizar interfaz grafica en modo retroceso
				self.steppingBackwards = True
				self.update_GUI()
				self.steppingBackwards = False
				self.pantalla_CDHS.update_LCD(self.beacon_data)
				self.pantalla_RAM.update_LCD(self.beacon_data)
			else:
				# Si ya no se puede retroceder, deshabilitar boton de
				# step backward hasta que se habilite modo PLAY GUI o se
				# ejecute un step forward
				self.pushButton.setEnabled(False)
				self.beacon_counter = 0
				self.num_beacon = 0

			# Movimiento de lectura de beacon a travez de HEX
			self.beacon_counter = self.beacon_counter + self.beacon_length
			self.num_beacon += 1

	def toggle_play_pausa(self):
		"""
		Funcion para cambiar entre Modo Manual (pausa) y Modo Automatico
		(play) de interpretacion de los datos procesados del archivo
		.dat. Si se encuentra en Modo Manual, se puede regresar o
		avanzar en los datos del archivo utilizando el boton Step
		Backwards y Step Forwards. En Modo Automatico, se va iterando
		a travez de todos los datos del archivo utilizando el timer (1s)

		ACTIVADO POR: Click en Boton Pausa/Play
		"""

		if (self.playHex == True):
			# Estado de Pausa de analisis automatico
			self.playHex = False
			# Cambiar icono de boton a simbolo de Play
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("./resources/Play2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.pushButton_2.setIcon(icon)								# Cambiar icono de Boton Play/Pausa a simbolo de Play
			self.pushButton.setEnabled(True)      					    # Habilitar boton de Step Backward
			self.pushButton_3.setEnabled(True)      					# Habilitar boton de Step Forward
			self.pushButton_7.setEnabled(False)     					# Deshabilitar boton de Reset Hex
		else:
			# Estado de Play de analisis automatico
			self.playHex = True
			# Cambiar icono de boton a simbolo de Pausa
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("./resources/Pause.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.pushButton_2.setIcon(icon)								# Cambiar icono de Boton Play/Pausa a simbolo de Pausa
			self.pushButton.setEnabled(False)     						# Deshabilitar boton de Step Backward
			self.pushButton_3.setEnabled(False)     					# Deshabilitar boton de Step Forward
			self.pushButton_7.setEnabled(True)      					# Habilitar boton de Reset Hex

	def step_forward(self):
		"""
		Funcion que permite avanzar a linea siguiente de datos de
		telemetria leidos desde archivo .dat. Esto es posible cuando la
		interfaz se encuentra en Modo Manual (Boton de pausa presionado)

		ACTIVADO POR: Click en Step Forwards >|
		"""

		# Ejecutar accion si modo manual esta activado
		if (self.hexSelected == True and self.playHex == False):

			# Reactivar boton de step-backward
			self.pushButton.setEnabled(True)

			# Mientras aun hayan beacons por leer
			if (self.num_beacon < self.beacon_amount):

			  # Lectura de HEX
			  self.beacon_data = mh.beacon_decode(self.hex_list, self.beacon_counter, self.num_beacon, False)

			  # Movimiento de lectura de beacon a travez de HEX
			  self.beacon_counter = self.beacon_counter + self.beacon_length
			  self.num_beacon += 1

			  # Actualizar interfaz grafica
			  self.update_GUI()
			  self.pantalla_CDHS.update_LCD(self.beacon_data)
			  self.pantalla_RAM.update_LCD(self.beacon_data)
			else:
			  # Si ya no hay beacons nuevos, deshabilitar boton de step
			  # forward hasta que se ejecute un step backward
			  self.pushButton_3.setEnabled(False)

	def select_HEX(self):
		"""
		Funcion para realizar la seleccion del archivo .dat del cual se
		extraen los datos HEX de telemetria del satelite para su
		despliegue en la interfaz grafica

		ACTIVADO POR: Click en Select HEX
		"""

		if (self.hexSelected == False):
			# Seleccionar archivo en buscador de files
			filedialog = QtWidgets.QFileDialog()
			fname = QFileDialog.getOpenFileName(filedialog, 'Open file', '/home')
			# Procesar archivo para generar listado HEX
			self.hex_list = mh.HEX_select(fname[0])
			self.beacon_length = 137
			self.beacon_amount = len(self.hex_list)/self.beacon_length
			self.beacon_counter = 0
			self.num_beacon = 0
			self.beacon_data = 0
			# HEX File seleccionado
			self.hexSelected = True
			# Habilitar botones de GUI para analizar datos
			self.pushButton.setEnabled(False)
			self.pushButton_2.setEnabled(True)
			self.pushButton_3.setEnabled(False)
			self.pushButton_4.setEnabled(False)
			self.pushButton_5.setEnabled(True)
			self.pushButton_6.setEnabled(True)
			self.pushButton_7.setEnabled(True)
			self.pushButton_8.setEnabled(False)

	def abrir_parametros_RAM(self):
		"""
		Funcion para desplegar ventana en donde se muestran los
		parametros guardados en memoria RAM del satelite

		ACTIVADO POR: Click en RAM Params
		"""

		if (self.hexSelected or (self.selected_port and self.beacon_data != 0)):
			self.pantalla_RAM.update_LCD(self.beacon_data)
			self.pantalla_RAM.show()

	def abrir_telemetria_CDHS(self):
		"""
		Funcion para desplegar ventana en donde se muestran los
		datos de telemetria del modulo CDHS (On-board computer)

		ACTIVADO POR: Click en CDHS Telemetry
		"""

		if (self.hexSelected or (self.selected_port and self.beacon_data != 0)):
			self.pantalla_CDHS.update_LCD(self.beacon_data)
			self.pantalla_CDHS.show()

	def reset_HEX(self):
		"""
		Funcion para comenzar a desplegar datos de telemetria del
		satelite nuevamente desde el principio del documento .dat
		procesado

		ACTIVADO POR: Click en Reset HEX
		"""

		# Reiniciar contadores de beacons
		self.beacon_counter = 0
		self.num_beacon = 0

		# Resetear datos desplegados en Grafica No.1 (Voltaje de Solar
		# Channel)
		self.L = deque([0], maxlen = 50)
		self.t = deque([0], maxlen = 50)
		self.curve.setData(self.t, self.L, pen = self.pen)

		# Resetear datos desplegados en Grafica No.2 (Corriente de Solar
		# Channel)
		self.L_2 = deque([0], maxlen = 50)
		self.t_2 = deque([0], maxlen = 50)
		self.curve_2.setData(self.t_2, self.L_2, pen = self.pen)

		# Resetear datos desplegados en Grafica No.3 (Voltaje de 3V3
		# Channel)
		self.L_3 = deque([0], maxlen = 50)
		self.t_3 = deque([0], maxlen = 50)
		self.curve_3.setData(self.t_3, self.L_3, pen = self.pen)

		# Resetear datos desplegados en Grafica No.4 (Corriente de 3V3
		# Channel)
		self.L_4 = deque([0], maxlen = 50)
		self.t_4 = deque([0], maxlen = 50)
		self.curve_4.setData(self.t_4, self.L_4, pen = self.pen)

	# ----------------- FUNCIONES DE CONEXION A PUERTO -----------------

	def conectar_puerto(self):
		"""
		Funcion para realizar la conexion a un puerto TCP para la
		recepcion de datos de telemetria de Quetzal-1 ya decodificados
		por AX25 Decode

		ACTIVADO POR: Click en Conectar a puerto
		"""

		# Inicializar variables
		ip = ''
		port = 0
		_selected_port = False

		# Obtener IP y No. de puerto al que se desea conectar
		idialog = QInputDialog()
		idialog.setWindowIcon(self.windows_icon)
		text, okPressed = QInputDialog.getText(idialog, "Enter IP","Enter IP address of port:", QLineEdit.Normal, "")
		if (okPressed and text != ''):
			ip = text
			if (ip.lower() == 'localhost' or ip.lower() == 'local'):   	# Permitir ingreso de palabra localhost
				ip = '127.0.0.1'
			if (ip.count('.') != 3):								    # Verificacion de formato IPv4
				return None
			idialog = QInputDialog()
			idialog.setWindowIcon(self.windows_icon)
			text, okPressed = QInputDialog.getText(idialog, "Select port","Enter port number:", QLineEdit.Normal, "")
			if (okPressed and text != ''):
				try:
					port = int(text)
					_selected_port = True
				except:
					pass

		# Si se selecciono puerto
		if (_selected_port):

			# Inicializar thread que se encarga de escuchar en puerto
			# seleccionado y emitir senial cuando se recibe un beacon
			self.adapter = TMadapter(self, ip, port)
			self.adapter.link.connect(self.updateLink)
			self.adapter.packet.connect(self.update_incoming_beacon)
			self.adapter.packet_count.connect(self.updatePacketCounter)
			self.adapter.start()

			print('QUETZAL-1 GUI-TCP Thread started')

			# Puerto TCP seleccionado
			self.selected_port = True

			# Habilitar botones de GUI para analizar datos
			self.pushButton.setEnabled(False)
			self.pushButton_2.setEnabled(False)
			self.pushButton_3.setEnabled(False)
			self.pushButton_4.setEnabled(False)
			self.pushButton_5.setEnabled(True)
			self.pushButton_6.setEnabled(True)
			self.pushButton_7.setEnabled(False)
			self.pushButton_8.setEnabled(False)

			qms = QMessageBox()
			qms.setWindowIcon(self.windows_icon)
			QMessageBox.information(qms, 'Successful connection','Successfully connected to:\n- IP: '+ip+'\n- Port: '+str(port), QMessageBox.Ok)
		else:
			return None

	def updatePacketCounter(self, count):
		print('Received packets: ' + str(count))

	def updateLink(self, up):
		if (up):
			print("Connected")
		else:
			print("Not connected")

	def update_incoming_beacon(self, beacon):
		"""
		Funcion para cargar datos recibidos por puerto TCP a funcion
		de parsing de los datos para su consecuente despliegue en GUI

		ACTIVADO POR: Senial packet de TMadapter (recepcion de nuevo
		beacon)

		Parametros
		----------
		beacon : bytearray
			Byte array que corresponde a una linea de datos de beacon
			(137 bytes)
		"""

		try:
			if (len(beacon) == 141):									# Determinar si data recibida corresponde a beacon de Quetzal-1
				# Extraer datos de beacon como linea de HEX bytes
				self.received_HEX = ['{:02x}'.format(b) for b in beacon]
				self.received_HEX = self.received_HEX[4:]				# Eliminar headers de CSP

				# Lectura de HEX recibido por TCP
				self.beacon_data = mh.beacon_decode(self.received_HEX, 0, self.adapter.recvd_packets, False)

				# Actualizar interfaz grafica
				self.update_GUI()
				self.pantalla_CDHS.update_LCD(self.beacon_data)
				self.pantalla_RAM.update_LCD(self.beacon_data)
			else:
				print('Received incorrect beacon of length {LEN} bytes over TCP port '.format(LEN=len(beacon)))
		except Exception as e:
			print('Error occured: {ERR}'.format(ERR=e))

	# ---------------------- FUNCIONES GENERALES -----------------------

	def updatedata(self):
		"""
		Funcion para lectura automatica de cada linea en archivo .dat
		y su procesamiento antes de desplegar la telemetria en interfaz

		ACTIVADO POR: Timer (1000ms)
		"""

		# Ejecutar si modo PLAY GUI automatico esta activado
		if (self.hexSelected == True and self.playHex == True):
			# Mientras aun hayan beacons por leer
			if (self.num_beacon < self.beacon_amount):

			  # Lectura de HEX
			  self.beacon_data = mh.beacon_decode(self.hex_list, self.beacon_counter, self.num_beacon, False)

			  # Movimiento de lectura de beacon a travez de HEX
			  self.beacon_counter = self.beacon_counter + self.beacon_length
			  self.num_beacon += 1

			  # Actualizar interfaz grafica
			  self.update_GUI()
			  self.pantalla_CDHS.update_LCD(self.beacon_data)
			  self.pantalla_RAM.update_LCD(self.beacon_data)

	def update_GUI(self):
		"""
		Funcion para actualizar los datos desplegados en widgets de
		interfaz grafica. Se cargan los datos procesados en updatedata()
		si interfaz se encuentra en Modo Automatico. De lo contrario,
		se cargan los datos procesados en step_backwards() o
		step_forward() en Modo Manual

		ACTIVADO POR: Funciones step_backwards(), step_forward() y
					  updatedata()
		"""

		# Inicializar blinkers
		green_blink = QtGui.QPixmap("./resources/green_blinker.png")
		red_blink = QtGui.QPixmap("./resources/red_blinker.png")

		# Datos de RTC (Real-time clock) -------------------------------
		self.lcdNumber.display(self.beacon_data[0])
		self.lcdNumber_2.display(self.beacon_data[1])
		self.lcdNumber_3.display(self.beacon_data[2])
		self.lcdNumber_4.display(self.beacon_data[3])
		self.lcdNumber_5.display(self.beacon_data[4])
		self.lcdNumber_6.display(self.beacon_data[5])

		# Datos de STATUS ----------------------------------------------

		# ADM Status
		ADM_deployed = int(self.beacon_data[6])
		ADM_deployed = '{0:08b}'.format(ADM_deployed)
		if ((int(ADM_deployed[7]) + int(ADM_deployed[6]) + int(ADM_deployed[5]) + int(ADM_deployed[4])) == 0):
			self.label_15.setPixmap(red_blink)
		elif ((int(ADM_deployed[7]) + int(ADM_deployed[6]) + int(ADM_deployed[5]) + int(ADM_deployed[4])) == 1):
			self.label_15.setPixmap(QtGui.QPixmap("./resources/green_blinker_antenna1.png"))
		elif ((int(ADM_deployed[7]) + int(ADM_deployed[6]) + int(ADM_deployed[5]) + int(ADM_deployed[4])) == 2):
			self.label_15.setPixmap(QtGui.QPixmap("./resources/green_blinker_antenna2.png"))
		elif ((int(ADM_deployed[7]) + int(ADM_deployed[6]) + int(ADM_deployed[5]) + int(ADM_deployed[4])) == 3):
			self.label_15.setPixmap(QtGui.QPixmap("./resources/green_blinker_antenna3.png"))
		elif ((int(ADM_deployed[7]) + int(ADM_deployed[6]) + int(ADM_deployed[5]) + int(ADM_deployed[4])) == 4):
			self.label_15.setPixmap(QtGui.QPixmap("./resources/green_blinker_antenna4.png"))

		# EPS Status
		if (self.beacon_data[7] == 83):
			self.label_16.setPixmap(green_blink)
		elif (self.beacon_data[7] == 69):
			self.label_16.setPixmap(red_blink)

		# HEATER Status
		if (self.beacon_data[8] == 102):
			self.label_17.setPixmap(QtGui.QPixmap("./resources/red_blinker3.png"))
		elif (self.beacon_data[8] == 105):
			self.label_17.setPixmap(QtGui.QPixmap("./resources/green_blinker3.png"))
		elif (self.beacon_data[8] == 150):
			self.label_17.setPixmap(QtGui.QPixmap("./resources/red_blinker2.png"))
		elif (self.beacon_data[8] == 153):
			self.label_17.setPixmap(QtGui.QPixmap("./resources/green_blinker2.png"))

		# ADCS Status
		if (self.beacon_data[9] == 83):
			self.label_18.setPixmap(green_blink)
		elif (self.beacon_data[9] == 69):
			self.label_18.setPixmap(red_blink)

		# PAYLOAD Status
		if (self.beacon_data[10] == 83):
			self.label_19.setPixmap(green_blink)
		elif (self.beacon_data[10] == 69):
			self.label_19.setPixmap(red_blink)

		# Datos Numericos de Telemetria EPS ----------------------------
		self.lcdNumber_15.display(self.beacon_data[17])					# Temperatura EPS
		self.lcdNumber_7.display(self.beacon_data[18])					# State of Charge
		self.progressBar.setValue(self.beacon_data[18])
		self.lcdNumber_8.display(self.beacon_data[19])					# Battery Voltage
		self.lcdNumber_9.display(self.beacon_data[20])					# Average Current
		self.lcdNumber_10.display(self.beacon_data[21])					# Remaining Capacity
		self.lcdNumber_11.display(self.beacon_data[22])					# Average Power
		self.lcdNumber_12.display(self.beacon_data[23])					# State of Health
		self.lcdNumber_13.display(self.beacon_data[28])					# V/I Monitor No.3 (5V0 Channel) Voltage
		self.lcdNumber_14.display(self.beacon_data[29])					# V/I Monitor No.3 (5V0 Channel) Current

		# Modo de actualizacion Forward
		if (self.steppingBackwards == False):

			# Datos Graficos para plotters
			# NOTA: Indexar [-1] en array apunta a ultimo valor de
			# lista. Ayuda al tener arrays de longitudes desconocidas.
			# En este caso, al ultimo elemento de tiempo se le suma 1
			# para siguiente step.

			# V/I Monitor No.1 (Solar Channel) Voltage
			val = self.beacon_data[24]
			self.L.append(val)
			self.t.append(self.t[-1]+1)
			self.curve.setData(self.t, self.L, pen = self.pen)
			self.graphicsView.setLabel('bottom',str(val) + ' V')

			# V/I Monitor No.1 (Solar Channel) Current
			val_2 = self.beacon_data[25]
			self.L_2.append(val_2)
			self.t_2.append(self.t_2[-1]+1)
			self.curve_2.setData(self.t_2, self.L_2,pen = self.pen)
			self.graphicsView_2.setLabel('bottom',str(val_2) + ' mA')

			# V/I Monitor No.2 (3V3 Channel) Voltage
			val_3 = self.beacon_data[26]
			self.L_3.append(val_3)
			self.t_3.append(self.t_3[-1]+1)
			self.curve_3.setData(self.t_3, self.L_3,pen = self.pen)
			self.graphicsView_3.setLabel('bottom',str(val_3) + ' V')

			# V/I Monitor No.2 (3V3 Channel) Current
			val_4 = self.beacon_data[27]
			self.L_4.append(val_4)
			self.t_4.append(self.t_4[-1]+1)
			self.curve_4.setData(self.t_4, self.L_4,pen = self.pen)
			self.graphicsView_4.setLabel('bottom',str(val_4) + ' mA')

		# Modo de actualizacion Backward
		elif (self.steppingBackwards == True):

			# Borrar ultimo dato de listas para retroceder grafica
			self.L.pop()
			self.L_2.pop()
			self.L_3.pop()
			self.L_4.pop()
			self.t.pop()
			self.t_2.pop()
			self.t_3.pop()
			self.t_4.pop()

			self.graphicsView.setLabel('bottom',str(self.L[-1]) + ' V')
			self.graphicsView_2.setLabel('bottom',str(self.L_2[-1]) + ' mA')
			self.graphicsView_3.setLabel('bottom',str(self.L_3[-1]) + ' V')
			self.graphicsView_4.setLabel('bottom',str(self.L_4[-1]) + ' mA')

			# Si aun hay nuevo FakeBeacon al cual retroceder las
			# graficas
			if (self.stopAddingFakebeacon == False):

				# Agregar primer dato de listas para retroceder grafica

				# V/I Monitor No.1 (Solar Channel) Voltage
				val = self.fakebeacon_data[24]
				self.L.appendleft(val)
				self.t.appendleft(self.t[0]-1)

				# V/I Monitor No.1 (Solar Channel) Current
				val_2 = self.fakebeacon_data[25]
				self.L_2.appendleft(val_2)
				self.t_2.appendleft(self.t_2[0]-1)

				# V/I Monitor No.2 (3V3 Channel) Voltage
				val_3 = self.fakebeacon_data[26]
				self.L_3.appendleft(val_3)
				self.t_3.appendleft(self.t_3[0]-1)

				# V/I Monitor No.2 (3V3 Channel) Current
				val_4 = self.fakebeacon_data[27]
				self.L_4.appendleft(val_4)
				self.t_4.appendleft(self.t_4[0]-1)

			self.curve.setData(self.t, self.L, pen = self.pen)
			self.curve_2.setData(self.t_2, self.L_2,pen = self.pen)
			self.curve_3.setData(self.t_3, self.L_3,pen = self.pen)
			self.curve_4.setData(self.t_4, self.L_4,pen = self.pen)

		# Datos Numericos de Telemetria FPB
		self.lcdNumber_39.display(self.beacon_data[30])					# ADCS Current
		self.lcdNumber_40.display(self.beacon_data[31])					# COMMS Current
		self.lcdNumber_41.display(self.beacon_data[32])					# PAYLOAD Current
		self.lcdNumber_42.display(self.beacon_data[33])					# HEATER Current

		# Datos Binarios para blinkers de Communication Flags
		comm_flags = int(self.beacon_data[35])
		comm_flags = '{0:08b}'.format(comm_flags)
		if (int(comm_flags[7]) == 1):
			self.label_102.setPixmap(green_blink)
		else:
			self.label_102.setPixmap(red_blink)
		if (int(comm_flags[6]) == 1):
			self.label_105.setPixmap(green_blink)
		else:
			self.label_105.setPixmap(red_blink)
		if (int(comm_flags[5]) == 1):
			self.label_108.setPixmap(green_blink)
		else:
			self.label_108.setPixmap(red_blink)
		if (int(comm_flags[4]) == 1):
			self.label_111.setPixmap(green_blink)
		else:
			self.label_111.setPixmap(red_blink)
		if (int(comm_flags[3]) == 1):
			self.label_114.setPixmap(green_blink)
		else:
			self.label_114.setPixmap(red_blink)

		# Datos Binarios para blinkers de Transmission Flags
		trans_flags = int(self.beacon_data[36])
		trans_flags = '{0:08b}'.format(trans_flags)
		if (int(trans_flags[7]) == 1):
			self.label_103.setPixmap(green_blink)
		else:
			self.label_103.setPixmap(red_blink)
		if (int(trans_flags[6]) == 1):
			self.label_106.setPixmap(green_blink)
		else:
			self.label_106.setPixmap(red_blink)
		if (int(trans_flags[5]) == 1):
			self.label_109.setPixmap(green_blink)
		else:
			self.label_109.setPixmap(red_blink)
		if (int(trans_flags[4]) == 1):
			self.label_112.setPixmap(green_blink)
		else:
			self.label_112.setPixmap(red_blink)
		if (int(trans_flags[3]) == 1):
			self.label_115.setPixmap(green_blink)
		else:
			self.label_115.setPixmap(red_blink)

		# Datos Binarios para blinkers de FPB Flags
		FPB_flags = int(self.beacon_data[34])
		FPB_flags = '{0:08b}'.format(FPB_flags)
		if (int(FPB_flags[7]) == 1):
			self.label_117.setPixmap(green_blink)
		else:
			self.label_117.setPixmap(red_blink)
		if (int(FPB_flags[6]) == 1):
			self.label_121.setPixmap(green_blink)
		else:
			self.label_121.setPixmap(red_blink)
		if (int(FPB_flags[5]) == 1):
			self.label_125.setPixmap(green_blink)
		else:
			self.label_125.setPixmap(red_blink)
		if (int(FPB_flags[4]) == 1):
			self.label_129.setPixmap(green_blink)
		else:
			self.label_129.setPixmap(red_blink)
		if (int(FPB_flags[3]) == 1):
			self.label_119.setPixmap(green_blink)
		else:
			self.label_119.setPixmap(red_blink)
		if (int(FPB_flags[2]) == 1):
			self.label_123.setPixmap(green_blink)
		else:
			self.label_123.setPixmap(red_blink)
		if (int(FPB_flags[1]) == 1):
			self.label_127.setPixmap(green_blink)
		else:
			self.label_127.setPixmap(red_blink)
		if (int(FPB_flags[0]) == 1):
			self.label_131.setPixmap(green_blink)
		else:
			self.label_131.setPixmap(red_blink)

		# Datos Numericos de Telemetria ADCS ---------------------------

		# Gyroscopes
		self.lcdNumber_19.display(self.beacon_data[37])					# Gyro X
		self.lcdNumber_20.display(self.beacon_data[38])					# Gyro Y
		self.lcdNumber_21.display(self.beacon_data[39])					# Gyro Z

		# Magnetometers
		self.lcdNumber_22.display(self.beacon_data[40])					# Mag X
		self.lcdNumber_23.display(self.beacon_data[41])					# Mag X
		self.lcdNumber_24.display(self.beacon_data[42])					# Mag X

		# ADC No.1
		self.lcdNumber_25.display(self.beacon_data[43])					# Channel No.1
		self.lcdNumber_27.display(self.beacon_data[44])					# Channel No.2
		self.lcdNumber_29.display(self.beacon_data[45])					# Channel No.3
		self.lcdNumber_31.display(self.beacon_data[46])					# Channel No.4
		self.lcdNumber_33.display(self.beacon_data[47])					# Channel No.5
		self.lcdNumber_35.display(self.beacon_data[48])					# Channel No.6

		# ADC No.2
		self.lcdNumber_26.display(self.beacon_data[49])					# Channel No.1
		self.lcdNumber_28.display(self.beacon_data[50])					# Channel No.2
		self.lcdNumber_30.display(self.beacon_data[51])					# Channel No.3
		self.lcdNumber_32.display(self.beacon_data[52])					# Channel No.4
		self.lcdNumber_34.display(self.beacon_data[53])					# Channel No.5
		self.lcdNumber_36.display(self.beacon_data[54])					# Channel No.6

		# Temperaturas
		self.lcdNumber_37.display(self.beacon_data[55])					# BNO055 Temperature
		self.lcdNumber_38.display(self.beacon_data[56])					# TMP100 Temperature

		# Datos Binarios para blinkers de FPB Flags
		trans_flags_A = int(self.beacon_data[57])
		trans_flags_A = '{0:08b}'.format(trans_flags_A)
		if (int(trans_flags_A[7]) == 1):
			self.label_81.setPixmap(green_blink)
		else:
			self.label_81.setPixmap(red_blink)
		if (int(trans_flags_A[6]) == 1):
			self.label_85.setPixmap(green_blink)
		else:
			self.label_85.setPixmap(red_blink)
		if (int(trans_flags_A[5]) == 1):
			self.label_83.setPixmap(green_blink)
		else:
			self.label_83.setPixmap(red_blink)
		if (int(trans_flags_A[4]) == 1):
			self.label_88.setPixmap(green_blink)
		else:
			self.label_88.setPixmap(red_blink)

		# Beacon Data --------------------------------------------------
		self.lcdNumber_16.display(self.beacon_data[58])
		self.lcdNumber_17.display(self.beacon_data[59])
		self.lcdNumber_18.display(self.beacon_data[60])

# **********************************************************************

# **********************************************************************
#                   CLASE DE THREAD DE CONEXION TCP
# **********************************************************************

# Clase TMadapter que hereda de clase QThread
class TMadapter(QThread):
	"""
	Clase de thread que se encarga de ejecutar las conexiones necesarias
	a un socket especifico para la recepcion de datos provenientes de un
	puerto TCP. Recepcion de paquetes con el formato de beacon de
	Quetzal-1 empacado con Cubesat Space Protocol (CSP). Hereda de
	QThread

	Atributos
	---------
	packet : pyqtSignal
		Senial que transporta paquete de beacon recibido por TCP
	link : pyqtSignal
		Senial que transporta bandera de estado de conexion TCP
	packet_count : pyqtSignal
		Senial que transporta cantidad de beacons recibidos por TCP

	Metodos
	-------
	run():
		Ejecucion principal de QThread. Se mantiene escuchando a puerto
		TCP para recepcion de datos, y si no recibe beacon en 15s
		genera excepcion
	"""

	# Seniales de thread
	packet = pyqtSignal(object)											# Senial emitida que contiene paquete de beacon recibido
	link = pyqtSignal(bool)												# Senial emitida que contiene flag de recepcion de datos
	packet_count = pyqtSignal(int)										# Senial emitida que contiene numero de paquetes recibidos

	# Inicializacion de variables globales
	recvd_packets = 0													# Contador de paquetes recibidos
	active = False														# Bandera de thread inicializado
	host = None															# Direccion de puerto a conectarse

	def __init__(self, parent, ip, port):
		"""
		Constructor

		Parametros
		----------
		parent : QMainWindow
			Parent de QThread
		ip : str
			Direccion ip de puerto (usualmente localhost -> 127.0.0.1)
		port : int
			No. de puerto a conectar socket
		"""

		QtCore.QThread.__init__(self, parent)
		self.parent = parent											# Guardado de parent (QMainWindow de interfaz grafica)
		self.active = True												# Thread inicializado
		self.context = zmq.Context()									# ZeroMQ high-performance asynchronous messaging initialization
		self.socket = self.context.socket(zmq.SUB)						# Inicializar socket
		self.host = 'tcp://' + ip + ':' + str(port)						# Inicializar host (direccion de puerto) [Linea original decia tcp://]
		self.socket.connect(self.host)									# Conectar socket a puerto
		self.socket.setsockopt_string(zmq.SUBSCRIBE, "")
		self.socket.setsockopt(zmq.RCVTIMEO, 15000) 					#Timeout de 15s (beacons transmitidos cada 10s)
		print('Started listening on {HOST} for incoming packets from AX25 Decode'.format(HOST=self.host))

	def run(self):
		"""
		Funcion de ejecucion de QThread

		ACTIVADO POR: Llamada de funcion externa
		"""

		while (self.active):											# Si QThread ya se inicializo
			try:
				data = self.socket.recv()								# Extraccion de datos del socket (thread monitorea puerto)
				self.packet.emit(data)									# Enviar paquete en senial que causa actualizacion de GUI
				self.recvd_packets = self.recvd_packets + 1				# Aumentar conteo de paquetes recibidos en socket
				self.packet_count.emit(self.recvd_packets)				# Enviar cantidad de paquetes recibidos
				self.link.emit(True)									# Enviar bandera de conexion exitosa
			except Exception as e:
				print('No packets received in the last 15 seconds...{ERR}'.format(ERR=e))
				self.link.emit(False)									# Enviar bandera de conexion fallida

# ----------------------------------------------------------------------
