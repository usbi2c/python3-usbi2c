# USB–I2C (USB to I²C) interface (adapter module)

This repository provides a Python 3 interface between user application and [KEL USB-I2C interface](http://kel.si/) protocol. See files inside `usbi2c` directory.

Additionally this repository provides the following examples:
* I2C search algorithm
* SHT21 temperature and humidity sensor (GY-21 includes pull-ups)
* BMP180 temperature and pressure sensor (GY-68 includes pull-ups and VIN = 5V)
* BH1750 ambient light sensor (GY-302 includes pull-ups, floating ADDR, and VCC = 5V)
* AT24C02 eeprom (YL-90 includes pull-ups and VCC = 5V)
* I2C LCD version 1, address 0x27 (black PCB no text, includes pull-ups and VCC = 5V)

### Windows

A `pyserial` package is needed for Python 3 on Windows. The package could be installed by executing `pip install pyserial` on Windows command line.

### Debian, Ubuntu

On Debian based operating system a `python3-serial` package is needed.
