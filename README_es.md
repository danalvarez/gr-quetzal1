[In English](https://github.com/danalvarez/gr-quetzal1)

# **Un mensaje del equipo de Quetzal-1**

Gracias al soporte de la comunidad internacional de radioaficionados, y [SatNOGS](https://satnogs.org/), más de 75,000 paquetes de telemetría se recibieron en los 211 días de operación exitosa de nuestro satélite, entre abril y noviembre del 2020. Hemos publicado estos datos (¡así como todas las fotos :framed_picture: enviadas por el primer satélite guatemalteco!) en el repositorio [quetzal1-telemetry](https://github.com/Quetzal-1-CubeSat-Team/quetzal1-telemetry).

Mantendremos este repositorio como estaba durante el período en que Quetzal-1 estuvo operacional, para referencia futura de los equipos o individuos que estén interesados. Más información del fin de operaciones del satélite está disponible [acá](https://twitter.com/quetzal1_uvg/status/1354169636275826688).

Les debemos una deuda de gratitud a todos ustedes: la comunidad.

 - *Con :heart:, el equipo del satélite Quetzal-1*

 # **Repositorios disponibles**

| Repositorio               | Descripción                                                                                                             |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------|
| [quetzal1-hardware](https://github.com/Quetzal-1-CubeSat-Team/quetzal1-hardware)        | Contiene los archivos de *hardware* para Quetzal-1 y sus subsistemas.                                                    |
| [quetzal1-flight-software](https://github.com/Quetzal-1-CubeSat-Team/quetzal1-flight-software) | Contiene el *software* para Quetzal-1 y sus subsistemas.                                                                 |
| [quetzal1-telemetry](https://github.com/Quetzal-1-CubeSat-Team/quetzal1-telemetry)              | Contiene toda la telemetría y fotografías enviadas por Quetzal-1 mientras estuvo en órbita. |
| gr-quetzal1              | Este repositorio. |

# **¡Ayúdanos a escuchar a Quetzal-1!**

## TLE

Gracias a SatNOGS, Space-Track y Celestrak, además de un grupo de radioaficionados alrededor del mundo, Quetzal-1 ha sido identificado con el NORAD ID #45598. El post de SatNOGS explicando esto está [acá](https://community.libre.space/t/iss-cubesat-deployment-2020-04-28-quetzal-1/6046/6?u=danalvarez). El TLE puede encontrarse [acá](https://celestrak.com/norad/elements/tle-new.txt).

## Especificaciones UHF

Quetzal-1 fue liberado desde la Estación Espacial Internacional el 28 de abril de 2020 a las 15:20 UTC. Aproximadamente 30 minutos luego de la liberación, empezó a desplegar sus antenas y a transmitir datos. Para la descarga, Quetzal-1 utiliza el transmisor AX100 de GOMSpace, que transmite datos en modulación GMSK a 4800 bits/segundo sobre la frecuencia 437.200 MHz ([coordinada por IARU](http://www.amsatuk.me.uk/iaru/finished_detail.php?serialnum=653)).

Los paquetes de datos están codificados en el formato AX.25 + HDLC, con *scrambling* G3RUH y codificación NRZI. La siguiente imagen muestra el formato general de los paquetes:

![Beacon Structure](media/beacon_structure.png)

Los datos se envían periódicamente cada 10 segundos. La hoja de cálculo en `docs/Beacon_Package_Data.xlsx` describe la estructura a más detalle.

---
:warning: **NOTA**

Aunque siempre se envía, no usamos la porción AX.25 del paquete de datos. Sin embargo, con el fin de ser explícitos, los datos contenidos en esta sección del paquete son siempre los siguientes (en hexadecimal):

`40 40 40 40 40 40 60 40 40 40 40 40 40 61 03 F0`

---

