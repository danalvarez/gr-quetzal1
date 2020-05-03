[In English](https://github.com/danalvarez/gr-quetzal1)

# **¡Ayúdanos a escuchar a Quetzal-1!**

## TLE

Gracias a SatNOGS, Space-Track y Celestrak, además de un grupo de radioaficionados alrededor del mundo, Quetzal-1 ha sido identificado con el NORAD ID #45598. El post de SatNOGS explicando esto está [acá](https://community.libre.space/t/iss-cubesat-deployment-2020-04-28-quetzal-1/6046/6?u=danalvarez). El TLE puede encontrarse [acá](https://celestrak.com/norad/elements/tle-new.txt).

## Especificaciones UHF

Quetzal-1 fue liberado desde la Estación Espacial Internacional el 28 de abril de 2020 a las 15:20 UTC. Aproximadamente 30 minutos luego de la liberación, empezó a desplegar sus antenas y a transmitir datos. Para la descarga, Quetzal-1 utiliza el transmisor AX100 de GOMSpace, que transmite datos en modulación GMSK a 4800 bits/segundo sobre la frecuencia 437.200 MHz ([coordinada por IARU](http://www.amsatuk.me.uk/iaru/finished_detail.php?serialnum=653)).

Los paquetes de datos están codificados en el formato AX.25 + HDLC, con *scrambling* G3RUH y codificación NRZI. La siguiente imagen muestra el formato general de los paquetes:

![Beacon Structure](misc/beacon_structure.png)

Los datos se envían periódicamente cada 10 segundos. La hoja de cálculo en `docs/Beacon_Package_Data.xlsx` describe la estructura a más detalle.

---
:warning: **NOTA**

Aunque siempre se envía, no usamos la porción AX.25 del paquete de datos. Sin embargo, con el fin de ser explícitos, los datos contenidos en esta sección del paquete son siempre los siguientes (en hexadecimal):

`40 40 40 40 40 40 60 40 40 40 40 40 40 61 03 F0`

---

