# Titulo: Modulo_HEX.py
# Autor: Aldo Stefano Aguilar Nadalini 15170
# Fecha: 10 de julio de 2019
# Descripcion: Programa para procesar archivo .dat que contiene Beacon
#              codificado en HEX. Este modulo devuelve los datos procesados
# -----------------------------------------------------------------------------

# Librerias
import sys

# -------------------------------- FUNCIONES -----------------------------------

# Funcion para abrir archivo seleccionado y volverlo array de HEX values
def HEX_select(name):
  try:
      with open(name,'rb') as fp:
        buff = fp.read()
      hex_list = ['{:02x}'.format(b) for b in buff]
      return hex_list
  except:
      print ("Archivo cargado incorrecto")
      sys.exit(0)
      return 0

# Funcion para decodificar bytes de beacon segun QUETZAL-1 :: Beacon & Package Data v3
def map_values(raw, lowLim, highLim, mapLow, mapHigh):
  m = (mapHigh - mapLow)/(highLim - lowLim)
  b = mapHigh - m*highLim
  y = m*raw + b
  return y

# Ejecucion continua para lectura de todo beacon en el HEX file
def beacon_decode(hex_list, beacon_counter, num_beacon, display_beacon):

  # ----------------------- SEGMENTACION DE BEACON ----------------------
  cubesat_identifier = hex_list[beacon_counter:beacon_counter + 8]      # 8 bytes
  CDHS_beacon = hex_list[beacon_counter + 8:beacon_counter + 26]        # 18 bytes
  EPS_beacon = hex_list[beacon_counter + 26:beacon_counter + 56]        # 30 bytes
  ADCS_beacon = hex_list[beacon_counter + 56:beacon_counter + 81]       # 25 bytes
  COMMS_beacon = hex_list[beacon_counter + 81:beacon_counter + 85]      # 4 bytes
  PAYLOAD_beacon = hex_list[beacon_counter + 85:beacon_counter + 88]    # 3 bytes
  RAM_parameters = hex_list[beacon_counter + 88:beacon_counter + 110]   # 22 bytes
  cubesat_message = hex_list[beacon_counter + 110:beacon_counter + 137] # 137 bytes (Total: 137 bytes)

  # ------------------------ CUBESAT IDENTIFIER -------------------------

  # Procesar identificador de satelite (Bytes 0-7)
  i = 0
  for letter in cubesat_identifier:
      cubesat_identifier[i] = chr(int(letter,16))
      i += 1
  cubesat_identifier = ''.join(cubesat_identifier)

  # ---------------------------- CDHS BEACON ----------------------------

  # Procesar valores de Real-time Clock (RTC)
  hora = int(CDHS_beacon[0],16)
  minuto = int(CDHS_beacon[1],16)
  segundo = int(CDHS_beacon[2],16)
  dia = int(CDHS_beacon[3],16)
  mes = int(CDHS_beacon[4],16)
  year = int(CDHS_beacon[5],16)

  # Estado de sub-modulos
  ADM_status = int(CDHS_beacon[6],16)
  EPS_status = int(CDHS_beacon[7],16)
  HEATER_status = int(CDHS_beacon[8],16)       # HEATER Status missing in HEX
  ADCS_status = int(CDHS_beacon[9],16)
  PAYLOAD_status = int(CDHS_beacon[10],16)

  # Contadores de RESET de sub-modulos
  ADM_resetS = int(CDHS_beacon[11],16)
  EPS_resetS = int(CDHS_beacon[12],16)
  ADCS_resetS = int(CDHS_beacon[13],16)
  ADCS_resetH = int(CDHS_beacon[14],16)
  COMMS_resetH = int(CDHS_beacon[15],16)
  CDHS_reset = int(CDHS_beacon[16] + CDHS_beacon[17],16)

  # ---------------------------- EPS BEACON -----------------------------

  # ---------- Temperature Sensor (TMP100) ----------
  # Battery Temperature (C)
  EPS_temperature = int(EPS_beacon[0],16)
  if (EPS_temperature < 253):
      EPS_temperature = round(map_values(EPS_temperature, 0, 252, -25.0, 70.0),2)

  # ------------ Battery Gauge (BQ27551) ------------
  # Battery State of Charge (%)
  state_charge = int(EPS_beacon[1],16)

  # Battery Voltage (V)
  battery_voltage = int(EPS_beacon[2],16)
  if (battery_voltage < 253):
      battery_voltage = round(map_values(battery_voltage, 0, 252, 2.5, 4.5),2)

  # Battery Average Current (mA)
  average_current = int(EPS_beacon[3] + EPS_beacon[4],16)
  if (average_current < 4093):
      average_current = round(map_values(average_current, 0, 4092, -2500.0, 2500.0),2)

  # Battery Remaining Capacity (mAh)
  remaining_capacity = int(EPS_beacon[5] + EPS_beacon[6],16)
  if (remaining_capacity < 4093):
      remaining_capacity = round(map_values(remaining_capacity, 0, 4092, 0.0, 4000.0),2)

  # Battery Average Power (mW)
  average_power = int(EPS_beacon[7] + EPS_beacon[8],16)
  if (average_power < 4093):
      average_power = round(map_values(average_power, 0, 4092, -8500.0, 8500.0),2)/1000.0

  # Battery State of Health (%)
  state_health = int(EPS_beacon[9],16)

  # ------------- V/I Monitors (INA260) -------------
  # Channel No.1 (Solar Bus) Voltage (V)
  CH1_voltage = int(EPS_beacon[10],16)
  if (CH1_voltage < 253):
      CH1_voltage = round(map_values(CH1_voltage, 0, 252, 0.0, 4.5),2)

  # Channel No.1 (Solar Bus) Current (mA)
  CH1_current = int(EPS_beacon[11] + EPS_beacon[12],16)
  if (CH1_current < 4093):
      CH1_current = round(map_values(CH1_current, 0, 4092, 0.0, 2500.0),2)

  # Channel No.2 (To 3V3 Bus) Voltage (V)
  CH2_voltage = int(EPS_beacon[13],16)
  if (CH2_voltage < 253):
      CH2_voltage = round(map_values(CH2_voltage, 0, 252, 0.0, 4.5),2)

  # Channel No.2 (To 3V3 Bus) Current (mA)
  CH2_current = int(EPS_beacon[14] + EPS_beacon[15],16)
  if (CH2_current < 4093):
      CH2_current = round(map_values(CH2_current, 0, 4092, 0.0, 2500.0),2)

  # Channel No.3 (To 5V0 Bus) Voltage (V)
  CH3_voltage = int(EPS_beacon[16],16)
  if (CH3_voltage < 253):
      CH3_voltage = round(map_values(CH3_voltage, 0, 252, 0.0, 4.5),2)

  # Channel No.3 (To 5V0 Bus) Current (mA)
  CH3_current = int(EPS_beacon[17] + EPS_beacon[18],16)
  if (CH3_current < 4093):
      CH3_current = round(map_values(CH3_current, 0, 4092, 0.0, 2500.0),2)

  # ------------- FPB Monitors (INA169) -------------
  # ADCS Current
  ADCS_current = int(EPS_beacon[19] + EPS_beacon[20],16)

  # COMMS Current
  COMMS_current = int(EPS_beacon[21] + EPS_beacon[22],16)

  # PAYLOAD Current
  PAYLOAD_current = int(EPS_beacon[23] + EPS_beacon[24],16)

  # HEATER Current
  HEATER_current = int(EPS_beacon[25] + EPS_beacon[26],16)
  
  # --------------- EPS Control Flags ---------------
  fault_flags = int(EPS_beacon[27],16)
  FPB_flags = '{0:08b}'.format(fault_flags)
  communication_flags = int(EPS_beacon[28],16)
  comm_flags = '{0:08b}'.format(communication_flags)
  transmission_flags_EPS = int(EPS_beacon[29],16)
  trans_flags_EPS = '{0:08b}'.format(transmission_flags_EPS)

  # ---------------------------- ADCS BEACON ----------------------------
                                  
  # ------------------ Gyroscopes -------------------
  # Gyroscope X
  gyro_X = int(ADCS_beacon[0],16)
  gyro_X = round(map_values(gyro_X, 0, 255, -100.0, 100.0),4)

  # Gyroscope Y
  gyro_Y = int(ADCS_beacon[1],16)
  gyro_Y = round(map_values(gyro_Y, 0, 255, -100.0, 100.0),4)

  # Gyroscope Z
  gyro_Z = int(ADCS_beacon[2],16)
  gyro_Z = round(map_values(gyro_Z, 0, 255, -100.0, 100.0),4)

  # ----------------- Magnetometers -----------------
  # Magnetometer X
  mag_X = int(ADCS_beacon[3] + ADCS_beacon[4],16)
  mag_X = round(map_values(mag_X, 0, 65535, -1300.0, 1300.0),4)

  # Magnetometer Y
  mag_Y = int(ADCS_beacon[5] + ADCS_beacon[6],16)
  mag_Y = round(map_values(mag_Y, 0, 65535, -1300.0, 1300.0),4)

  # Magnetometer Z
  mag_Z = int(ADCS_beacon[7] + ADCS_beacon[8],16)
  mag_Z = round(map_values(mag_Z, 0, 65535, -2500.0, 2500.0),4)

  # --------------------- ADCs ----------------------
  # ADC1 Channel No.1
  ADC1_CH1 = int(ADCS_beacon[9],16)
  ADC1_CH1 = round(map_values(ADC1_CH1, 0, 255, 0.0, 3.3),2)

  # ADC1 Channel No.2
  ADC1_CH2 = int(ADCS_beacon[10],16)
  ADC1_CH2 = round(map_values(ADC1_CH2, 0, 255, 0.0, 3.3),2)

  # ADC1 Channel No.3
  ADC1_CH3 = int(ADCS_beacon[11],16)
  ADC1_CH3 = round(map_values(ADC1_CH3, 0, 255, 0.0, 3.3),2)

  # ADC1 Channel No.4
  ADC1_CH4 = int(ADCS_beacon[12],16)
  ADC1_CH4 = round(map_values(ADC1_CH4, 0, 255, 0.0, 3.3),2)

  # ADC1 Channel No.5
  ADC1_CH5 = int(ADCS_beacon[13],16)
  ADC1_CH5 = round(map_values(ADC1_CH5, 0, 255, 0.0, 3.3),2)

  # ADC1 Channel No.6
  ADC1_CH6 = int(ADCS_beacon[14],16)
  ADC1_CH6 = round(map_values(ADC1_CH6, 0, 255, 0.0, 3.3),2)

  # ADC2 Channel No.1
  ADC2_CH1 = int(ADCS_beacon[15],16)
  ADC2_CH1 = round(map_values(ADC2_CH1, 0, 255, 0.0, 3.3),2)

  # ADC2 Channel No.2
  ADC2_CH2 = int(ADCS_beacon[16],16)
  ADC2_CH2 = round(map_values(ADC2_CH2, 0, 255, 0.0, 3.3),2)

  # ADC2 Channel No.3
  ADC2_CH3 = int(ADCS_beacon[17],16)
  ADC2_CH3 = round(map_values(ADC2_CH3, 0, 255, 0.0, 3.3),2)

  # ADC2 Channel No.4
  ADC2_CH4 = int(ADCS_beacon[18],16)
  ADC2_CH4 = round(map_values(ADC2_CH4, 0, 255, 0.0, 3.3),2)

  # ADC2 Channel No.5
  ADC2_CH5 = int(ADCS_beacon[19],16)
  ADC2_CH5 = round(map_values(ADC2_CH5, 0, 255, 0.0, 3.3),2)

  # ADC2 Channel No.6
  ADC2_CH6 = int(ADCS_beacon[20],16)
  ADC2_CH6 = round(map_values(ADC2_CH6, 0, 255, 0.0, 3.3),2)

  # ----------- IMU Temperature (BNO055) ------------
  # Imu Temperature Sensor (C)
  BNO055_temperature = int(ADCS_beacon[21],16)
  BNO055_temperature = -(BNO055_temperature & 0x8000) | (BNO055_temperature & 0x7fff)
  
  # ---------- Temperature Sensor (TMP100) ----------
  # ADCS Temperature No.1 (C)
  ADCS_temperature1 = int(ADCS_beacon[22] + ADCS_beacon[23],16)
  ADCS_temperature1 = -(ADCS_temperature1 & 0x8000) | (ADCS_temperature1 & 0x7fff)

  # -------------- ADCS Control Flags ---------------
  transmission_flags_ADCS = int(ADCS_beacon[24],16)
  trans_flags_ADCS = '{0:08b}'.format(transmission_flags_ADCS)

  # --------------------------- COMMS BEACON ----------------------------

  # -------------- Transciever (AX100) --------------
  # Package Counter
  package_counter = int(COMMS_beacon[0] + COMMS_beacon[1] + COMMS_beacon[2] + COMMS_beacon[3],16)

  # -------------------------- PAYLOAD BEACON ---------------------------

  # --------------- Camera (ArduCAM) ----------------
  # Camera Mode of operation
  camera_mode = int(PAYLOAD_beacon[0],16)

  # Picture Counter
  picture_counter = int(PAYLOAD_beacon[1] + PAYLOAD_beacon[2],16)
  
  # -------------------------- RAM PARAMETER ----------------------------
  CDHS_CYCLE_TIME = int(RAM_parameters[0],16)*1000
  CDHS_WDT = int(RAM_parameters[1],16)*3600
  ADM_SOC_LIMIT = int(RAM_parameters[2],16)
  ADCS_SOC_LIMIT = int(RAM_parameters[3],16)
  COMMS_SOC_LIMIT = int(RAM_parameters[4],16)
  PLD_SOC_LIMIT = int(RAM_parameters[5],16)
  HEATER_CYCLE_TIME = int(RAM_parameters[6],16)*1000
  HEATER_EMON_TIME = int(RAM_parameters[7],16)
  HEATER_EMOFF_TIME = int(RAM_parameters[8],16)
  ADM_CYCLE_TIME = int(RAM_parameters[9],16)*1000
  ADM_BURN_TIME = int(RAM_parameters[10],16)
  ADM_MAX_CYCLES = int(RAM_parameters[11],16)
  ADM_WAIT_TIME1 = int(RAM_parameters[12],16)*1000
  ADM_WAIT_TIME2 = int(RAM_parameters[13],16)*60000
  ADM_ENABLE = int(RAM_parameters[14],16)
  COMMS_CYCLE_TIME = int(RAM_parameters[15],16)*1000
  PLD_CYCLE_TIME = int(RAM_parameters[16],16)*1000
  PLD_OP_MODE = int(RAM_parameters[17],16)
  CAM_RESOLUTION = int(RAM_parameters[18],16)
  CAM_EXPOSURE = int(RAM_parameters[19],16)
  CAM_SAVE_TIME = int(RAM_parameters[20],16)*1000
  PLD_ENABLE = int(RAM_parameters[21],16)

  # ------------------------- CUBESAT MESSAGE ---------------------------

  # Procesar mensaje de satelite (Bytes 89-115)
  i = 0
  for letter in cubesat_message:
      cubesat_message[i] = chr(int(letter,16))
      i += 1
  cubesat_message = ''.join(cubesat_message)

  # -------------------------- BEACON STORAGE ---------------------------
  identifier = cubesat_identifier
  beacon_data = [hora, minuto, segundo, dia, mes, year, ADM_status, EPS_status, \
               HEATER_status, ADCS_status, PAYLOAD_status, ADM_resetS, \
               EPS_resetS, ADCS_resetS, ADCS_resetH, COMMS_resetH, CDHS_reset,\
               EPS_temperature, state_charge, battery_voltage, average_current,\
               remaining_capacity, average_power, state_health, CH1_voltage, \
               CH1_current, CH2_voltage, CH2_current, CH3_voltage, CH3_current,\
               ADCS_current, COMMS_current, PAYLOAD_current, HEATER_current,\
               fault_flags, communication_flags, transmission_flags_EPS,\
               gyro_X, gyro_Y, gyro_Z, mag_X, mag_Y, mag_Z, ADC1_CH1, ADC1_CH2,\
               ADC1_CH3, ADC1_CH4, ADC1_CH5, ADC1_CH6, ADC2_CH1, ADC2_CH2,\
               ADC2_CH3, ADC2_CH4, ADC2_CH5, ADC2_CH6, BNO055_temperature,\
               ADCS_temperature1, transmission_flags_ADCS,\
               package_counter, camera_mode, picture_counter, CDHS_CYCLE_TIME,\
               CDHS_WDT, ADM_SOC_LIMIT, ADCS_SOC_LIMIT, COMMS_SOC_LIMIT, \
               PLD_SOC_LIMIT, HEATER_CYCLE_TIME, HEATER_EMON_TIME, HEATER_EMOFF_TIME, \
               ADM_CYCLE_TIME, ADM_BURN_TIME, ADM_MAX_CYCLES, ADM_WAIT_TIME1,\
               ADM_WAIT_TIME2, ADM_ENABLE, COMMS_CYCLE_TIME, PLD_CYCLE_TIME,\
               PLD_OP_MODE, CAM_RESOLUTION, CAM_EXPOSURE, CAM_SAVE_TIME, PLD_ENABLE]
  messages = cubesat_message

  # -------------------------- BEACON DISPLAY ---------------------------
  if (display_beacon):
    print ("------------------ BEACON No." + str(num_beacon + 1) + " ------------------")
    print ("Identifier: "),
    print (cubesat_identifier)
    print ("----------------- CDHS -----------------")
    print ("RTC Time: " + str(hora) + ":" + str(minuto) + ":" + str(segundo))
    print ("RTC Date: " + str(dia) + "/" + str(mes) + "/" + str(year))
    print ("ADM Status: " + str(ADM_status))
    print ("EPS Status: " + str(EPS_status))
    print ("HEATER Status: " + str(HEATER_status))
    print ("ADCS Status: " + str(ADCS_status))
    print ("PAYLOAD Status: " + str(PAYLOAD_status))
    print ("ADM Software Reset Counter: " + str(ADM_resetS))
    print ("EPS Software Reset Counter: " + str(EPS_resetS))
    print ("ADCS Software Reset Counter: " + str(ADCS_resetS))
    print ("ADCS Hardware Reset Counter: " + str(ADCS_resetH))
    print ("COMMS Hardware Reset Counter: " + str(COMMS_resetH))
    print ("CDHS Reset Counter: " + str(CDHS_reset))
    print ("----------------- EPS ------------------")
    print ("Temperature No.1: " + str(EPS_temperature) + " degC")
    print ("State of Charge: " + str(state_charge) + "%")
    print ("Battery Voltage: " + str(battery_voltage) + " V")
    print ("Average Current: " + str(average_current) + " mA")
    print ("Remaining Capacity: " + str(remaining_capacity) + " mAh")
    print ("Average Power: " + str(average_power) + " mW")
    print ("State of Health: " + str(state_health) + "%")
    print ("CH1 Voltage: " + str(CH1_voltage) + " V")
    print ("CH1 Current: " + str(CH1_current) + " mA")
    print ("CH2 Voltage: " + str(CH2_voltage) + " V")
    print ("CH2 Current: " + str(CH2_current) + " mA")
    print ("CH3 Voltage: " + str(CH3_voltage) + " V")
    print ("CH3 Current: " + str(CH3_current) + " mA")
    print ("ADCS Current: " + str(ADCS_current) + " mA")
    print ("COMMS Current: " + str(COMMS_current) + " mA")
    print ("PAYLOAD Current: " + str(PAYLOAD_current) + " mA")
    print ("HEATER Current: " + str(HEATER_current) + " mA")
    print ("FPB Flags: " + FPB_flags)
    print ("Communication Flags: " + comm_flags)
    print ("Transmission Flags: " + trans_flags_EPS)
    print ("---------------- ADCS ------------------")
    print ("Gyro X: " + str(gyro_X) + " degC/s")
    print ("Gyro Y: " + str(gyro_Y) + " degC/s")
    print ("Gyro Z: " + str(gyro_Z) + " degC/s")
    print ("Magnetometer X: " + str(mag_X) + " uT")
    print ("Magnetometer Y: " + str(mag_Y) + " uT")
    print ("Magnetometer Z: " + str(mag_Z) + " uT")
    print ("ADC1:")
    print ("CH1: " + str(ADC1_CH1) + " V")
    print ("CH2: " + str(ADC1_CH2) + " V")
    print ("CH3: " + str(ADC1_CH3) + " V")
    print ("CH4: " + str(ADC1_CH4) + " V")
    print ("CH5: " + str(ADC1_CH5) + " V")
    print ("CH6: " + str(ADC1_CH6) + " V")
    print ("ADC2:")
    print ("CH1: " + str(ADC2_CH1) + " V")
    print ("CH2: " + str(ADC2_CH2) + " V")
    print ("CH3: " + str(ADC2_CH3) + " V")
    print ("CH4: " + str(ADC2_CH4) + " V")
    print ("CH5: " + str(ADC2_CH5) + " V")
    print ("CH6: " + str(ADC2_CH6) + " V")
    print ("BNO005 Temperature: " + str(BNO055_temperature) + " degC")
    print ("Temperature No.1: " + str(ADCS_temperature1) + " degC")
    print ("Transmission Flags: " + trans_flags_ADCS)
    print ("---------------- COMMS -----------------")
    print ("Package Counter: " + str(package_counter))
    print ("--------------- PAYLOAD ----------------")
    print ("Camera Mode: " + str(camera_mode))
    print ("Picture Counter: " + str(picture_counter))
    print ("------------ RAM PARAMETERS ------------")
    print ("CDHS Cycle Time: " + str(CDHS_CYCLE_TIME))
    print ("CDHS Watchdog: " + str(CDHS_WDT))
    print ("ADM SOC Limit: " + str(ADM_SOC_LIMIT))
    print ("ADCS SOC Limit: " + str(ADCS_SOC_LIMIT))
    print ("COMMS SOC Limit: " + str(COMMS_SOC_LIMIT))
    print ("PLD SOC Limit: " + str(PLD_SOC_LIMIT))
    print ("HEATER Cycle Time: " + str(HEATER_CYCLE_TIME))
    print ("HEATER Emergency On Time: " + str(HEATER_EMON_TIME))
    print ("HEATER Emergency Off Time: " + str(HEATER_EMOFF_TIME))
    print ("ADM Cycle Time: " + str(ADM_CYCLE_TIME))
    print ("ADM Burn Time: " + str(ADM_BURN_TIME))
    print ("ADM Max Cycles: " + str(ADM_MAX_CYCLES))
    print ("ADM Wait Time 1: " + str(ADM_WAIT_TIME1))
    print ("ADM Wait Time 2: " + str(ADM_WAIT_TIME2))
    print ("ADM Enable: " + str(ADM_ENABLE))
    print ("COMMS Cycle Time: " + str(COMMS_CYCLE_TIME))
    print ("PLD Cycle Time: " + str(PLD_CYCLE_TIME))
    print ("PLD Operation Mode: " + str(PLD_OP_MODE))
    print ("CAM Resolution: " + str(CAM_RESOLUTION))
    print ("CAM Exposure: " + str(CAM_EXPOSURE))
    print ("CAM Save Time: " + str(CAM_SAVE_TIME))
    print ("PLD Enable: " + str(PLD_ENABLE))
    print ("----------------------------------------")
    print ("Message: "),
    print (cubesat_message)

  return beacon_data

# -------------------------------- EJECUCION -----------------------------------

##hex_list = HEX_select('B_HEX2.dat')
##beacon_length = 115
##beacon_amount = len(hex_list)/beacon_length
##print ("No. of Beacons to read: " + str(beacon_amount))
##beacon_counter = 0
##num_beacon = 0
##
### Ejecucion continua para lectura de todo beacon en el HEX file
##while (num_beacon < beacon_amount):
##
##  beacon_data = beacon_decode(hex_list, beacon_counter, num_beacon, True)
##  #print (beacon_data)
##
##  # Movimiento de lectura de beacon a travez de HEX
##  beacon_counter = beacon_counter + beacon_length
##  num_beacon += 1
  
