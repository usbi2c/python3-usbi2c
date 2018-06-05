# USB–I2C (USB to I²C) interface (adapter module)

This repository provides a Python 3 interface between user application and [KEL USB-I2C interface](http://kel.si/) protocol. See files inside `usbi2c` directory.

Additionally this repository provides the following examples:
* I2C search algorithm
* SHT21 temperature and humidity sensor

### Windows

A `pyserial` package is needed for Python 3 on Windows. The package could be installed by executing `pip install pyserial` on Windows command line.

### Debian, Ubuntu

On Debian based operating system a `python3-serial` package is needed.
