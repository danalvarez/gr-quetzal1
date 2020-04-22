1. The desktop GUI's entry point is `main.py`
2. The `resources` folder contains all the images used by the Quetzal-1 Desktop GUI
3. The `templates` folder contains all the .ui files generated with Qt_Designer
4. `Pantalla_Interfaz_V2.py` is the script for the Main Window of the GUI
5. `Pantalla_CDHS.py` is the script for the Dialog that displays Quetzal-1's CDHS Telemetry
6. `Pantalla_RAM.py`  is the script for the Dialog that displays all parameters stored in Quetzal-1's RAM Memory
7. `Qt_Interfaz.py`, `Qt_CDHS.py` and `Qt_RAM.py` are the python files generated from the .ui templates
8. `Modulo_HEX.py` is a module that contains the necessary functions to parse Quetzal-1's beacon telemetry
9. Quetzal-1 Desktop GUI can be used to analyze post-mortem telemetry stored in a `.dat` file or it can also be connected via TCP port to the GNURadio decoder to view telemetry in real time.
