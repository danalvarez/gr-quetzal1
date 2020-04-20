# Titulo: Quetzal_1_HEX.py
# Autor: Aldo Aguilar Nadalini 15170
# Fecha: 04 de agosto de 2019
# Descripcion: Interfaz grafica para procesar datos HEX de beacons recolectados
#              de nanosatelite Quetzal-1 (Primer satelite guatemalteco)
# -----------------------------------------------------------------------------

# Librerias
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDesktopWidget, QFileDialog
from collections import deque
import pyqtgraph as pg
import Modulo_HEX as mh
import CMD_Dialog_PyQT5 as cd
import RAM_Dialog_PyQT5 as rm

    # Constructor
    def __init__(self):
        # HEX PROCESSING ------------------------------------------------------
        self.hexSelected = False           # HEX File aun no seleccionado
        self.playHex = True                # Comenzar en estado PLAY GUI
        self.steppingBackwards = False     # Estado RETROCEDER GUI desactivado
        # PYQTGRAPHICS --------------------------------------------------------
        C = pg.hsvColor(0.3,1.0,1.0)
        self.pen = pg.mkPen(color = C,width = 2.5)
        # CDHS DIALOG ---------------------------------------------------------
        self.Dialog = QtGui.QDialog()
        self.uid = cd.Ui_Dialog()
        self.uid.setupUi(self.Dialog)
        # RAM DIALOG ----------------------------------------------------------
        self.Dialog2 = QtGui.QDialog()
        self.uir = rm.Ui_Dialog()
        self.uir.setupUi(self.Dialog2)
        # ---------------------------------------------------------------------
        
        # Centrado de GUI
        qr = MainWindow.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        MainWindow.move(qr.topLeft())

        # Timer Configuration
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updatedata)
        self.timer.start(1000)

        # Graficas
        pg.setConfigOption('background', 'k')
        pg.setConfigOption('foreground', 'g')
        
        self.graphicsView = PlotWidget(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(20, 460, 261, 221))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.showGrid(x = True, y = True)
        self.graphicsView.setYRange(3,5)
        ax = self.graphicsView.getAxis('left') 
        ax.setTicks([[(3, '3.0'), (3.5, '3.5'), (4, '4.0'), (4.5, '4.5'), (5.0, '5.0')]])
        self.curve = self.graphicsView.plot()
        self.L = deque([0], maxlen = 50)
        self.t = deque([0], maxlen = 50)
        
        self.graphicsView_2 = PlotWidget(self.centralwidget)
        self.graphicsView_2.setGeometry(QtCore.QRect(290, 460, 261, 221))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.graphicsView_2.showGrid(x = True, y = True)
        self.graphicsView_2.setYRange(0,1500)
        ax_2 = self.graphicsView_2.getAxis('left') 
        ax_2.setTicks([[(0, '0'), (250, '250'), (500, '500'), (750, '750'), (1000, '1000'), (1250, '1250'), (1500, '1500'), (1750, '1750')]])
        self.curve_2 = self.graphicsView_2.plot()
        self.L_2 = deque([0], maxlen = 50)
        self.t_2 = deque([0], maxlen = 50)
        
        self.graphicsView_3 = PlotWidget(self.centralwidget)
        self.graphicsView_3.setGeometry(QtCore.QRect(570, 460, 261, 221))
        self.graphicsView_3.setObjectName("graphicsView_3")
        self.graphicsView_3.showGrid(x = True, y = True)
        self.graphicsView_3.setYRange(3,5)
        ax_3 = self.graphicsView_3.getAxis('left') 
        ax_3.setTicks([[(3, '3.0'), (3.5, '3.5'), (4, '4.0'), (4.5, '4.5'), (5.0, '5.0')]])
        self.curve_3 = self.graphicsView_3.plot()
        self.L_3 = deque([0], maxlen = 50)
        self.t_3 = deque([0], maxlen = 50)
        
        self.graphicsView_4 = PlotWidget(self.centralwidget)
        self.graphicsView_4.setGeometry(QtCore.QRect(840, 460, 261, 221))
        self.graphicsView_4.setObjectName("graphicsView_4")
        self.graphicsView_4.showGrid(x = True, y = True)
        self.graphicsView_4.setYRange(0,1500)
        ax_4 = self.graphicsView_4.getAxis('left') 
        ax_4.setTicks([[(0, '0'), (250, '250'), (500, '500'), (750, '750'), (1000, '1000'), (1250, '1250'), (1500, '1500'), (1750, '1750')]])
        self.curve_4 = self.graphicsView_4.plot()
        self.L_4 = deque([0], maxlen = 50)
        self.t_4 = deque([0], maxlen = 50)

        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1290, 10, 131, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.on_RAM_Button_clicked)

        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(1290, 50, 131, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.on_CDHS_Button_clicked)

        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(1290, 90, 131, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.on_HEXR_Button_clicked)

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(910, 70, 131, 28))        
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.on_SHEX_Button_clicked)

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(960, 410, 41, 41))
        self.pushButton_5.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("StepBackward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.on_StepBackward_clicked)
        
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(1010, 410, 41, 41))
        self.pushButton_6.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Pause.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_6.setIcon(icon1)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.on_PlayPause_clicked)
        
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(1060, 410, 41, 41))
        self.pushButton_7.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("StepForward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_7.setIcon(icon2)
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.clicked.connect(self.on_StepForward_clicked)
        
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        self.pushButton_7.setEnabled(False)

    # Desplegar parametros de RAM de satelite
    def on_RAM_Button_clicked(self):
        if (self.hexSelected == True):
            self.uir.update_LCD(self.beacon_data)
            self.Dialog2.show()

    # Desplegar telemetria de CDHS
    def on_CDHS_Button_clicked(self):
        if (self.hexSelected == True):
            self.uid.update_LCD(self.beacon_data)
            self.Dialog.show()

    # Resettear lectura de HEX file
    def on_HEXR_Button_clicked(self):
        # Reiniciar contadores de beacons
        self.beacon_counter = 0
        self.num_beacon = 0
        # Resettear graficas de simulacion
        self.L = deque([0], maxlen = 50)
        self.t = deque([0], maxlen = 50)
        self.curve.setData(self.t, self.L, pen = self.pen)
        self.L_2 = deque([0], maxlen = 50)
        self.t_2 = deque([0], maxlen = 50)
        self.curve_2.setData(self.t_2, self.L_2, pen = self.pen)
        self.L_3 = deque([0], maxlen = 50)
        self.t_3 = deque([0], maxlen = 50)
        self.curve_3.setData(self.t_3, self.L_3, pen = self.pen)
        self.L_4 = deque([0], maxlen = 50)
        self.t_4 = deque([0], maxlen = 50)
        self.curve_4.setData(self.t_4, self.L_4, pen = self.pen)

    # Seleccionar HEX file a analizar
    def on_SHEX_Button_clicked(self):
        if (self.hexSelected == False):
            # Seleccionar archivo en buscador de files
            filedialog = QtWidgets.QFileDialog()
            fname = QFileDialog.getOpenFileName(filedialog, 'Open file', '/home')
            # Procesar archivo para generar listado HEX
            self.hex_list = mh.HEX_select2(fname[0])
            self.beacon_length = 137
            self.beacon_amount = len(self.hex_list)/self.beacon_length
            self.beacon_counter = 0
            self.num_beacon = 0
            self.beacon_data = 0
            # HEX File seleccionado
            self.hexSelected = True                 
            # Habilitar botones de GUI para analizar datos
            self.pushButton.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(False)
            self.pushButton_6.setEnabled(True)
            
    # Play/Pausar analisis automatico de HEX file
    def on_PlayPause_clicked(self):
        if (self.playHex == True):
            # Estado de Pausa de analisis automatico
            self.playHex = False
            # Cambiar icono de boton a simbolo de Play
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("Play2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pushButton_6.setIcon(icon)
            self.pushButton_3.setEnabled(False)     # Deshabilitar boton de RESET Hex
            self.pushButton_5.setEnabled(True)      # Habilitar boton de StepBackward 
            self.pushButton_7.setEnabled(True)      # Habilitar boton de StepForward
        else:
            # Estado de Play de analisis automatico
            self.playHex = True
            # Cambiar icono de boton a simbolo de Pausa
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("Pause.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pushButton_6.setIcon(icon)
            self.pushButton_3.setEnabled(True)      # Habilitar boton de RESET Hex
            self.pushButton_5.setEnabled(False)     # Deshabilitar boton de StepBackward 
            self.pushButton_7.setEnabled(False)     # Deshabilitar boton de StepForward 
            
    # Retroceder un step en analisis manual de HEX file
    def on_StepBackward_clicked(self):
        # Ejecutar accion si modo manual esta activado
        if (self.hexSelected == True and self.playHex == False):
            
            # Reactivar boton de step-forward
            self.pushButton_7.setEnabled(True)
            
            # FakeBeacon para capturar datos desechados de las graficas y lograr
            # que se vuelvan a agregar al inicio de la misma simulando efecto de retroceso
            fakebeacon_counter = self.beacon_counter - 51*self.beacon_length
            num_fakebeacon = self.num_beacon - 51
            
            self.stopAddingFakebeacon = False
            # Si ya no hay datos para retroceder, no actualizar FakeBeacon
            if (num_fakebeacon < 0):
                self.stopAddingFakebeacon = True
            
            # Movimiento de lectura en retroceso de beacon a travez de HEX
            self.beacon_counter = self.beacon_counter - 2*self.beacon_length
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
                self.uid.update_LCD(self.beacon_data)
                self.uir.update_LCD(self.beacon_data)
            else:
                # Si ya no se puede retroceder, deshabilitar boton de step backward
                # hasta que se habilite modo PLAY GUI o se ejecute un step forward
                self.pushButton_5.setEnabled(False)
                self.beacon_counter = 0
                self.num_beacon = 0
                
            # Movimiento de lectura de beacon a travez de HEX
            self.beacon_counter = self.beacon_counter + self.beacon_length
            self.num_beacon += 1
            
    # Avanzar un step en analisis manual de HEX file
    def on_StepForward_clicked(self):
        # Ejecutar accion si modo manual esta activado
        if (self.hexSelected == True and self.playHex == False):
            
            # Reactivar boton de step-backward
            self.pushButton_5.setEnabled(True)
            
            # Mientras aun hayan beacons por leer
            if (self.num_beacon < self.beacon_amount):
                
              # Lectura de HEX
              self.beacon_data = mh.beacon_decode(self.hex_list, self.beacon_counter, self.num_beacon, False)
        
              # Movimiento de lectura de beacon a travez de HEX
              self.beacon_counter = self.beacon_counter + self.beacon_length
              self.num_beacon += 1
        
              # Actualizar interfaz grafica
              self.update_GUI()
              self.uid.update_LCD(self.beacon_data)
              self.uir.update_LCD(self.beacon_data)
            else:
              # Si ya no hay beacons nuevos, deshabilitar boton de step forward 
              # hasta que se ejecute un step backward
              self.pushButton_7.setEnabled(False)
                       
    # Actualizacion automatica de GUI cada un segundo
    def updatedata(self):
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
              self.uid.update_LCD(self.beacon_data)
              self.uir.update_LCD(self.beacon_data)

    # Actualizacion grafica de GUI (Automatica, step forward/backward)
    def update_GUI(self):

        # Datos de RTC (Real-time clock)
        self.lcdNumber.display(self.beacon_data[0])
        self.lcdNumber_2.display(self.beacon_data[1])
        self.lcdNumber_3.display(self.beacon_data[2])
        self.lcdNumber_4.display(self.beacon_data[3])
        self.lcdNumber_5.display(self.beacon_data[4])
        self.lcdNumber_6.display(self.beacon_data[5])

        # Datos de STATUS
        if (self.beacon_data[6] == 83):
            self.label_9.setPixmap(QtGui.QPixmap("green_blinker.png"))
        elif (self.beacon_data[6] == 69):
            self.label_9.setPixmap(QtGui.QPixmap("red_blinker.png"))
        if (self.beacon_data[7] == 83):
            self.label_16.setPixmap(QtGui.QPixmap("green_blinker.png"))
        elif (self.beacon_data[7] == 69):
            self.label_16.setPixmap(QtGui.QPixmap("red_blinker.png"))
        if (self.beacon_data[8] == 83):
            self.label_11.setPixmap(QtGui.QPixmap("green_blinker.png"))
        elif (self.beacon_data[8] == 69):
            self.label_11.setPixmap(QtGui.QPixmap("red_blinker.png"))
        if (self.beacon_data[9] == 83):
            self.label_17.setPixmap(QtGui.QPixmap("green_blinker.png"))
        elif (self.beacon_data[9] == 69):
            self.label_17.setPixmap(QtGui.QPixmap("red_blinker.png"))
        if (self.beacon_data[10] == 83):
            self.label_18.setPixmap(QtGui.QPixmap("green_blinker.png"))
        elif (self.beacon_data[10] == 69):
            self.label_18.setPixmap(QtGui.QPixmap("red_blinker.png"))

        # Datos Numericos de Telemetria EPS
        self.lcdNumber_15.display(self.beacon_data[17])
        self.lcdNumber_19.display(self.beacon_data[18])
        self.progressBar.setValue(self.beacon_data[18])
        self.lcdNumber_17.display(self.beacon_data[19])
        self.lcdNumber_18.display(self.beacon_data[20])
        self.lcdNumber_21.display(self.beacon_data[21])
        self.lcdNumber_20.display(self.beacon_data[22])
        self.lcdNumber_22.display(self.beacon_data[23])
        self.lcdNumber_23.display(self.beacon_data[18])
        self.lcdNumber_28.display(self.beacon_data[28])
        self.lcdNumber_29.display(self.beacon_data[29])
        
        # Modo de actualizacion Forward
        if (self.steppingBackwards == False):
            
            # Datos Graficos para plotters
            # NOTA: Indexar [-1] en array apunta a ultimo valor de lista. Ayuda
            # al tener arrays de longitudes desconocidas. En este caso, al ultimo
            # elemento de tiempo se le suma 1 para siguiente step.
            val = self.beacon_data[24]
            self.L.append(val)
            self.t.append(self.t[-1]+1)                 
            self.curve.setData(self.t, self.L, pen = self.pen)
            
            val_2 = self.beacon_data[25]
            self.L_2.append(val_2)
            self.t_2.append(self.t_2[-1]+1)
            self.curve_2.setData(self.t_2, self.L_2,pen = self.pen)
    
            val_3 = self.beacon_data[26]
            self.L_3.append(val_3)
            self.t_3.append(self.t_3[-1]+1)
            self.curve_3.setData(self.t_3, self.L_3,pen = self.pen)
    
            val_4 = self.beacon_data[27]
            self.L_4.append(val_4)
            self.t_4.append(self.t_4[-1]+1)
            self.curve_4.setData(self.t_4, self.L_4,pen = self.pen)
            
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
            
            # Si aun hay nuevo FakeBeacon al cual retroceder las graficas
            if (self.stopAddingFakebeacon == False):
            
                # Agregar primer dato de listas para retroceder grafica
                val = self.fakebeacon_data[24]
                self.L.appendleft(val)
                self.t.appendleft(self.t[0]-1)                 
                
                val_2 = self.fakebeacon_data[25]
                self.L_2.appendleft(val_2)
                self.t_2.appendleft(self.t_2[0]-1)  
        
                val_3 = self.fakebeacon_data[26]
                self.L_3.appendleft(val_3)
                self.t_3.appendleft(self.t_3[0]-1)
        
                val_4 = self.fakebeacon_data[27]
                self.L_4.appendleft(val_4)
                self.t_4.appendleft(self.t_4[0]-1)
                
            self.curve.setData(self.t, self.L, pen = self.pen)
            self.curve_2.setData(self.t_2, self.L_2,pen = self.pen)
            self.curve_3.setData(self.t_3, self.L_3,pen = self.pen)
            self.curve_4.setData(self.t_4, self.L_4,pen = self.pen)
            
        # Datos Numericos de Telemetria FPB
        self.lcdNumber_24.display(self.beacon_data[30])
        self.lcdNumber_25.display(self.beacon_data[31])
        self.lcdNumber_26.display(self.beacon_data[32])
        self.lcdNumber_27.display(self.beacon_data[33])

        # Datos Binarios para blinkers de Communication Flags
        comm_flags = int(self.beacon_data[35])
        comm_flags = '{0:08b}'.format(comm_flags)
        if (int(comm_flags[7]) == 1):
            self.label_54.setPixmap(QtGui.QPixmap("green_blinker.png"))
        else:
            self.label_54.setPixmap(QtGui.QPixmap("red_blinker.png"))
        if (int(comm_flags[6]) == 1):
            self.label_55.setPixmap(QtGui.QPixmap("green_blinker.png"))
        else:
            self.label_55.setPixmap(QtGui.QPixmap("red_blinker.png"))
        if (int(comm_flags[5]) == 1):
            self.label_56.setPixmap(QtGui.QPixmap("green_blinker.png"))
        else:
            self.label_56.setPixmap(QtGui.QPixmap("red_blinker.png"))
        if (int(comm_flags[4]) == 1):
            self.label_57.setPixmap(QtGui.QPixmap("green_blinker.png"))
        else:
            self.label_57.setPixmap(QtGui.QPixmap("red_blinker.png"))
        if (int(comm_flags[3]) == 1):
            self.label_58.setPixmap(QtGui.QPixmap("green_blinker.png"))
        else:
            self.label_58.setPixmap(QtGui.QPixmap("red_blinker.png"))

        # Datos Binarios para blinkers de Transmission Flags
        trans_flags = int(self.beacon_data[36])
        trans_flags = '{0:08b}'.format(trans_flags)
        if (int(trans_flags[7]) == 1):
            self.label_67.setPixmap(QtGui.QPixmap("green_blinker.png"))
        else:
            self.label_67.setPixmap(QtGui.QPixmap("red_blinker.png"))
        if (int(trans_flags[6]) == 1):
            self.label_68.setPixmap(QtGui.QPixmap("green_blinker.png"))
        else:
            self.label_68.setPixmap(QtGui.QPixmap("red_blinker.png"))
        if (int(trans_flags[5]) == 1):
            self.label_73.setPixmap(QtGui.QPixmap("green_blinker.png"))
        else:
            self.label_73.setPixmap(QtGui.QPixmap("red_blinker.png"))
        if (int(trans_flags[4]) == 1):
            self.label_64.setPixmap(QtGui.QPixmap("green_blinker.png"))
        else:
            self.label_64.setPixmap(QtGui.QPixmap("red_blinker.png"))
        if (int(trans_flags[3]) == 1):
            self.label_74.setPixmap(QtGui.QPixmap("green_blinker.png"))
        else:
            self.label_74.setPixmap(QtGui.QPixmap("red_blinker.png"))
        
        # Datos Binarios para blinkers de FPB Flags
        FPB_flags = int(self.beacon_data[34])
        FPB_flags = '{0:08b}'.format(FPB_flags)
        if (int(FPB_flags[7]) == 1):
            self.label_75.setPixmap(QtGui.QPixmap("green_blinker.png"))
        else:
            self.label_75.setPixmap(QtGui.QPixmap("red_blinker.png"))
        if (int(FPB_flags[6]) == 1):
            self.label_83.setPixmap(QtGui.QPixmap("green_blinker.png"))
        else:
            self.label_83.setPixmap(QtGui.QPixmap("red_blinker.png"))
        if (int(FPB_flags[5]) == 1):
            self.label_82.setPixmap(QtGui.QPixmap("green_blinker.png"))
        else:
            self.label_82.setPixmap(QtGui.QPixmap("red_blinker.png"))
        if (int(FPB_flags[4]) == 1):
            self.label_76.setPixmap(QtGui.QPixmap("green_blinker.png"))
        else:
            self.label_76.setPixmap(QtGui.QPixmap("red_blinker.png"))
        if (int(FPB_flags[3]) == 1):
            self.label_88.setPixmap(QtGui.QPixmap("green_blinker.png"))
        else:
            self.label_88.setPixmap(QtGui.QPixmap("red_blinker.png"))
        if (int(FPB_flags[2]) == 1):
            self.label_90.setPixmap(QtGui.QPixmap("green_blinker.png"))
        else:
            self.label_90.setPixmap(QtGui.QPixmap("red_blinker.png"))
        if (int(FPB_flags[1]) == 1):
            self.label_87.setPixmap(QtGui.QPixmap("green_blinker.png"))
        else:
            self.label_87.setPixmap(QtGui.QPixmap("red_blinker.png"))
        if (int(FPB_flags[0]) == 1):
            self.label_89.setPixmap(QtGui.QPixmap("green_blinker.png"))
        else:
            self.label_89.setPixmap(QtGui.QPixmap("red_blinker.png"))

        # Datos Numericos de Telemetria ADCS
        self.lcdNumber_30.display(self.beacon_data[37])
        self.lcdNumber_31.display(self.beacon_data[38])
        self.lcdNumber_32.display(self.beacon_data[39])
        self.lcdNumber_35.display(self.beacon_data[40])
        self.lcdNumber_34.display(self.beacon_data[41])
        self.lcdNumber_33.display(self.beacon_data[42])
        self.lcdNumber_36.display(self.beacon_data[43])
        self.lcdNumber_37.display(self.beacon_data[44])
        self.lcdNumber_38.display(self.beacon_data[45])
        self.lcdNumber_39.display(self.beacon_data[46])
        self.lcdNumber_40.display(self.beacon_data[47])
        self.lcdNumber_41.display(self.beacon_data[48])
        self.lcdNumber_44.display(self.beacon_data[49])
        self.lcdNumber_45.display(self.beacon_data[50])
        self.lcdNumber_46.display(self.beacon_data[51])
        self.lcdNumber_42.display(self.beacon_data[52])
        self.lcdNumber_47.display(self.beacon_data[53])
        self.lcdNumber_43.display(self.beacon_data[54])
        self.lcdNumber_16.display(self.beacon_data[55])
        self.lcdNumber_48.display(self.beacon_data[56])

        # Datos Binarios para blinkers de FPB Flags
        trans_flags_A = int(self.beacon_data[57])
        trans_flags_A = '{0:08b}'.format(trans_flags_A)
        if (int(trans_flags_A[7]) == 1):
            self.label_132.setPixmap(QtGui.QPixmap("green_blinker.png"))
        else:
            self.label_132.setPixmap(QtGui.QPixmap("red_blinker.png"))
        if (int(trans_flags_A[6]) == 1):
            self.label_134.setPixmap(QtGui.QPixmap("green_blinker.png"))
        else:
            self.label_134.setPixmap(QtGui.QPixmap("red_blinker.png"))
        if (int(trans_flags_A[5]) == 1):
            self.label_127.setPixmap(QtGui.QPixmap("green_blinker.png"))
        else:
            self.label_127.setPixmap(QtGui.QPixmap("red_blinker.png"))
        if (int(trans_flags_A[4]) == 1):
            self.label_129.setPixmap(QtGui.QPixmap("green_blinker.png"))
        else:
            self.label_129.setPixmap(QtGui.QPixmap("red_blinker.png"))

        self.lcdNumber_49.display(self.beacon_data[58])
        self.lcdNumber_50.display(self.beacon_data[59])
        self.lcdNumber_51.display(self.beacon_data[60])
        