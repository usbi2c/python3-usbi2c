# -*- coding: utf-8 -*-

import serial
from sys import platform
from usbi2c.usbi2c import *

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
	uart = serial.Serial(serial_name(), timeout = 1);

	adapter = USBI2C(uart)
	adapter.Reset()

	serial = adapter.Serial()
	print("Connected to adapter with serial number: %s" % serial)
	print("Searching I2C devices ...")

	for address in range(1, 128):
		if probe(adapter, address):
			print("0x%x (%d)" % (address, address))

except Exception as e:
	print(e)

finally:
	print("Finished")