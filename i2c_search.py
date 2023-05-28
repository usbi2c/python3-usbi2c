# -*- coding: utf-8 -*-

import serial
from argparse import ArgumentParser
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

def serial_port():
	if platform == "linux":
		return "/dev/ttyACM0"
	else:
		return "COM4"

def search(uart):
	adapter = USBI2C(uart)
	adapter.Reset()

	serial_number = adapter.Serial()
	print("Connected to adapter with serial number: %s" % serial_number)
	print("Scanning for I2C devices ...")

	for address in range(1, 128):
		detected = probe(adapter, address)
		result = "found" if detected else "not found"
		if verbose:
			print("Probing address %x ... %s" % (address, result))
		elif detected:
			print ("%s on 0x%x (%d)" %
				(result.capitalize(), address, address))

parser = ArgumentParser(description="")
parser.add_argument('--port',
	help="serial port name",
)

args = parser.parse_args()
port = serial_port() if args.port is None else args.port

try:
	if verbose:
		print("Using serial port: %s" % port)
	uart = serial.Serial(port, timeout = 1)
	if uart:
		search(uart)
		uart.close()

except Exception as e:
	print(e)

finally:
	print("Finished scanning")