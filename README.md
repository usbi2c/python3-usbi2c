# USB–I2C (USB to I²C) interface (adapter module)

This repository provides a Python 3 interface between user application and [KEL USB-I2C interface](http://kel.si/) protocol. See files inside `usbi2c` directory.

Additionally this repository provides the following examples:
* I2C search algorithm
* SHT21 temperature and humidity sensor (GY-21 includes 10k pull-ups)
* BMP180 temperature and pressure sensor (GY-68 includes 4k7 pull-ups and VIN = 5V)
* BH1750 ambient light sensor (GY-302 includes 10k pull-ups, floating ADDR, and VCC = 5V)
* AT24C02 EEPROM (YL-90 includes 10k pull-ups and VCC = 5V)
* PCF8574 (I2C LCD version 1), address 0x27 (black PCB no text, includes 4k7 pull-ups and VCC = 5V)
* ADS1115 16-bit ADC, address 0x48 (includes 10k pull-ups, ADDR = GND, VDD = 5V)

### Windows

A `pyserial` package is needed for Python 3 on Windows. The package could be installed by executing `pip install pyserial` on Windows command line.

In examples string `/dev/ttyACM0` must be changed to reflect COM port where USB-I2C interface is attached to. Look at Device Manager.

### Debian, Ubuntu

On Debian based operating system a `python3-serial` package is needed.
