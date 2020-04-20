[In English](https://github.com/danalvarez/gr-quetzal1)

# Especificaciones UHF

## **¡Ayúdanos a escuchar a Quetzal-1!**

Quetzal-1 será liberado desde la Estación Espacial Internacional el 28 de abril de 2020 a las 09:20 hrs (GMT-6). Aproximadamente 30 minutos luego de la liberación, deberá desplegar sus antenas y empezar la transmisión de datos. Para la descarga, Quetzal-1 utiliza el transmisor AX100 de GOMSpace, que transmite datos en modulación GMSK a 4800 bits/segundo sobre la frecuencia 437.200 MHz ([coordinada por IARU](http://www.amsatuk.me.uk/iaru/finished_detail.php?serialnum=653)).

Los paquetes de datos estarán codificados en el formato AX.25 + HDLC, como lo muestra la imagen a continuación:

![Beacon Structure](misc/beacon_structure.png)

Los datos se enviarán periódicamente cada 10 segundos. La hoja de cálculo en `docs/Beacon_Package_Data.xlsx` describe la estructura a más detalle.

---
:warning: **NOTA**

Aunque siempre se envía, no usamos la porción AX.25 del paquete de datos. Sin embargo, con el fin de ser explícitos, los datos contenidos en esta sección del paquete son siempre los siguientes (en hexadecimal):

`40 40 40 40 40 40 60 40 40 40 40 40 40 61 03 F0`

---

