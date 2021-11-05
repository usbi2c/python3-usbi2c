# -*- coding: utf-8 -*-

import serial
import struct
from usbi2c.usbi2c import *

def TransformTemperature(r):
	val = struct.unpack('>H', r[0:2])[0]
	k = (1.0 * val) / 2**16
	return -46.85 + 175.72 * k

def TransformHumidity(r):
	val = struct.unpack('>H', r[0:2])[0]
	k = (1.0 * val) / 2**16
	return -5 + 125 * k

class SHT21:

	def __init__(self, adapter):
		self.address = 0x40
		self.adapter = adapter

	def Read(self, command):
		self.adapter.Reset()
		self.adapter.Address(self.address)

		# This will write a command (one byte) to SHT21 with clock stretching.
		self.adapter.Write(command)
		self.adapter.Start()
		self.adapter.WaitForCompletion()

		# This will request 3 bytes from SHT21.
		self.adapter.ReadLength(3)
		self.adapter.Start()
		# Any bytes less will result in NACK.
		self.adapter.WaitForCompletion()

		# Read received bytes from interface.
		return self.adapter.Read(3)

	def Temperature(self):
		r = self.Read(b'\xe3')
		return TransformTemperature(r)

	def Humidity(self):
		r = self.Read(b'\xe5')
		return TransformHumidity(r)

print("SHT21 demo application")
try:
	uart = serial.Serial('/dev/ttyACM0', timeout = 1)

	adapter = USBI2C(uart)
	sht21 = SHT21(adapter)

	t = sht21.Temperature()
	h = sht21.Humidity()
	print("T = %.3f °C\nH = %.2f %%" % (t, h))

	uart.close()

except Exception as e:
	print(e)