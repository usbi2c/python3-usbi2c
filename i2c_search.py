# -*- coding: utf-8 -*-

import serial
from sys import platform
from usbi2c.usbi2c import *

verbose = False

def probe(adapter, address):
	try:
		adapter.Address(address)
		adapter.Start()
		adapter.WaitForCompletion()
		return True

	except Exception as e:
		if e.char and e.char == b'T' and address == 1:
			raise Exception("Pull-up resistors missing")
		return False

def serial_name():
	if platform == "linux":
		return "/dev/ttyACM0"
	else:
		return "COM4"

try:
	name = serial_name()
	if verbose:
		print ("Using serial port: %s" % name)
	uart = serial.Serial(name, timeout = 1)

	adapter = USBI2C(uart)
	adapter.Reset()

	serial = adapter.Serial()
	print("Connected to adapter with serial number: %s" % serial)
	print("Scanning for I2C devices ...")

	for address in range(1, 128):
		detected = probe(adapter, address)
		result = "found" if detected else "not found"
		if verbose:
			print("Probing address %x ... %s" % (address, result))
		elif detected:
			print ("%s on 0x%x (%d)" %
				(result.capitalize(), address, address))

	uart.close()

except Exception as e:
	print(e)

finally:
	print("Finished scanning")