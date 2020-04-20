# Titulo: Modulo_Quetzal_1.py
# Autor: Aldo Stefano Aguilar Nadalini 15170
# Fecha: 01 de agosto de 2019
# Descripcion: Modulo de funciones a ejecutar en Quetzal_1.py (GUI de satelite)

# Librerias
import serial
import serial.tools.list_ports as sp
import struct
import sys

## Funcion para configuracion de puerto serial --------------------------------
def init_serial(PORT_NUMBER):
    try:
        #PORT_NUMBER = 9                     ## Numero de puerto
        BAUD_RATE = 9600                    ## Baud Rate de puerto
    
        # Inicializar puerto serial
        data = serial.Serial()
        
        data.baudrate = BAUD_RATE
        data.port = "COM" + str(int(PORT_NUMBER))
        data.timeout = 1
        data.open()
    except:
        print ("ERROR: SERIAL PORT 'COM" + str(int(PORT_NUMBER)) + "' NOT OPEN")
        sys.exit(0)
    return data

## Funcion para verificar ingreso de digito -----------------------------------
def IntVerification(num):
    state = False
    try:
        num = int(num)
        state = True
    except:
        print ("Ingreso no valido, intente de nuevo!")
        state = False
    return state

def update_data(data):
    datos = str(data.readline(), 'utf-8')
    datos = datos.replace("\n", "")
    datos = datos.replace("\r", "")
    return str(datos)

def open_serial(data):
    data.open()

def close_serial(data):
    data.close()
