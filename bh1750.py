# -*- coding: utf-8 -*-

import time
import serial
import struct
from usbi2c.usbi2c import *

class BH1750:

	def __init__(self, adapter):
		self.address = 0x23
		self.adapter = adapter

	def getLuminosity(self):
		# Measurement at 1 lux. Measurement time is approx. 120 ms.
		resolution = 0x20

		self.adapter.Reset()

		self.adapter.Address(self.address)
		self.adapter.Write(bytes([resolution]))
		self.adapter.Start()

		time.sleep(0.2)

		self.adapter.ReadLength(2)
		self.adapter.Start()
		self.adapter.WaitForCompletion()
		r = self.adapter.Read(2)

		return struct.unpack('>h', r)[0] / 1.2

try:
	print("BH1750 demo application")
	uart = serial.Serial('/dev/ttyACM0', timeout = 1)

	adapter = USBI2C(uart)
	bh1750 = BH1750(adapter)

	print("L = %d lx" % (bh1750.getLuminosity()))

	uart.close()

except Exception as e:
	print(e)