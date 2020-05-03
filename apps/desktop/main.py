# ----------------------------------------------------------------------
# Titulo: main.py
# Autor: Aldo Aguilar Nadalini
# Fecha: 19 de abril de 2020
# Descripcion: Punto de entrada general de Quetzal-1 Interface
# ----------------------------------------------------------------------

# Librerias ------------------------------------------------------------

# Local libraries
from PyQt5 import QtCore, QtGui, QtWidgets
import argparse
import sys

# Own libraries
from Pantalla_Interfaz_V2 import Pantalla_Interfaz


# Parse arguments
def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--interval', '-i', help='Beacon frame loading interval (ms)', type=int, default=1000)
	return parser.parse_args()


# Ejecucion principal de intefaz ---------------------------------------
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	pantalla_interfaz = Pantalla_Interfaz(parse_args())
	pantalla_interfaz.show()
	sys.exit(app.exec_())
# ----------------------------------------------------------------------
