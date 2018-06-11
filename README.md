# USB–I2C (USB to I²C) interface (adapter module)

This repository provides a Python 3 interface between user application and [KEL USB-I2C interface](http://kel.si/) protocol. See files inside `usbi2c` directory.

Additionally this repository provides the following examples:
* I2C search algorithm
* ADS1115 16-bit ADC, address 0x48 (includes 10k pull-ups, ADDR = GND and VDD = 5V)
* AT24C02 EEPROM, address 0x50 (YL-90 includes 10k pull-ups and VCC = 5V)
* BH1750 ambient light sensor, address 0x23 (GY-302 includes 10k pull-ups, floating ADDR and VCC = 5V)
* BMP180 temperature and pressure sensor, address 0x77 (GY-68 includes 4k7 pull-ups and VIN = 5V)
* PCF8574 (I2C LCD version 1), address 0x27 (black PCB no text, includes 4k7 pull-ups and VCC = 5V)
* SHT21 temperature and humidity sensor, address 0x40 (GY-21 includes 10k pull-ups)

### Windows

A `pyserial` package is needed for Python 3 on Windows. The package could be installed by executing `pip install pyserial` on Windows command line.

In examples, string `/dev/ttyACM0` must be changed to reflect COM port where USB-I2C interface is attached to. Look at Device Manager.

### Debian, Ubuntu

On Debian based operating system a `python3-serial` package is needed.
