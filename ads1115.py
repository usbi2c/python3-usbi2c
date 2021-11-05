# -*- coding: utf-8 -*-

'''
This code is experimental.
'''

import serial
import struct
import time
from usbi2c.usbi2c import *

class ADS1115:

	def __init__(self, adapter):
		self.address = 0x48
		self.pollTime = 0.01
		self.range = [6.144, 4.094, 2.048, 1.024, 0.512, 0.256]
		self.adapter = adapter

		self.adapter.Reset()
		self.adapter.Address(self.address)

	def _register(self, register = 0, endiness = '>h'):
		self.adapter.Write(bytes([register]))
		self.adapter.ReadLength(2)
		self.adapter.Start()

		self.adapter.WaitForCompletion()

		r = adapter.Read(2)
		return struct.unpack(endiness, r)[0]

	def _pga(self, config):
		return (config >> 9 & 0x7)

	def Value(self):
		return self._register(0)

	def Voltage(self):
		return self.range[self._pga(self.config)] * self.Value() / (2 ** 15)

	def Config(self):
		self.config = self._register(1, endiness = '>H')
		return self.config

	def LoThresh(self):
		return self._register(2)

	def HiThresh(self):
		return self._register(3)

	def StartOneShot(self, mux = 4, pga = 0, dr = 4):
		config = 1 << 15 | mux << 12 | pga << 9 | 1 << 8 | dr << 5
		w = struct.pack('>H', config)
		adapter.Write(b'\x01' + w)
		adapter.Start()
		adapter.WaitForCompletion()

	def WaitForCompletion(self):
		elapsedTime = 0
		while elapsedTime < 1:
			self.config = self.Config()
			if self.config & (1 << 15):
				break
			elapsedTime += self.pollTime
			time.sleep(self.pollTime)

try:
	print("ADS1115 demo application")
	uart = serial.Serial('/dev/ttyACM0', timeout = 1)

	adapter = USBI2C(uart)
	ads1115 = ADS1115(adapter)

	# Measure voltages on A1
	for i in range(4):
		ads1115.StartOneShot(mux = 4 + i)
		ads1115.WaitForCompletion()
		print("U%d = %.3f V" % (i, ads1115.Voltage()))

	uart.close()

except Exception as e:
	print(e)