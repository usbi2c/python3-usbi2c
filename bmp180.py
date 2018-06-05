# -*- coding: utf-8 -*-

import time
import serial
import struct
from usbi2c.usbi2c import *

class BMP180:

	def __init__(self, adapter):
		self.address = 0x77
		self.adapter = adapter

	def getCalibrationData(self):
		self.adapter.Reset()

		self.adapter.Address(self.address)
		self.adapter.Write(b'\xAA')
		self.adapter.ReadLength(22)
		self.adapter.Start()

		self.adapter.WaitForCompletion()

		r = self.adapter.Read(22)
		(self.ac1, self.ac2, self.ac3, self.ac4, self.ac5, self.ac6, self.b1, self.b2, self.mb, self.mc, self.md) = struct.unpack('>hhhHHHhhhhh', r)

	def getTemperature(self):
		self.adapter.Write(b'\xF4\x2E')
		self.adapter.Start()

		time.sleep(0.01)

		self.adapter.Write(b'\xF6')
		self.adapter.ReadLength(2)
		self.adapter.Start()

		self.adapter.WaitForCompletion()

		r = self.adapter.Read(2)
		return struct.unpack('>h', r)[0]

	def calculateTemperature(self, ut):
		x1 = (ut - self.ac6) * self.ac5 / 2**15
		x2 = self.mc * 2**11 / (x1 + self.md)
		self.b5 = x1 + x2
		t = (self.b5 + 8) / 2**4
		return t / 10

	def preprarePressure(self):
		# OSS = 0
		self.adapter.Write(b'\xF4\x34')
		self.adapter.Start()

		time.sleep(0.1)

		self.adapter.Write(b'\xF6')
		self.adapter.ReadLength(3)
		self.adapter.Start()

		self.adapter.WaitForCompletion()

		r = self.adapter.Read(3)
		return struct.unpack('>H', r[0:2])[0]

	def getPressure(self, up):
		b6 = self.b5 - 4000
		x1 = (self.b2 * (b6 * b6 / 2**12)) / 2**11
		x2 = self.ac2 * b6 / 2**11
		x3 = x1 + x2
		b3 = ((self.ac1 * 4 + x3) + 2) / 4
		x1 = self.ac3 * b6 / 2**13
		x2 = (self.b1 * (b6 * b6 / 2**12)) / 2**16
		x3 = ((x1 + x2) + 2) / 4
		b4 = self.ac4 * (x3 + 32768) / 2**15
		b7 = (up - b3) * 50000
		if b7 < 0x80000000:
			p = (b7 * 2) / b4
		else:
			p = (b7 * b4) / 2
		x1 = (p / 2**8) * (p / 2**8)
		x1 = (x1 * 3038) / 2**16
		x2 = (-7357 * p) / 2**16
		p = p + (x1 + x2 + 3791) / 2**4
		return p

	def getAltitude(self, pressure):
		A = P / 101325
		n = 1 / 5.25588
		e = A**n
		e = 1 - e
		return e / 0.0000225577

try:
	print("BMP180 demo application")
	uart = serial.Serial('/dev/ttyACM0', timeout = 1);

	adapter = USBI2C(uart)
	bmp180 = BMP180(adapter)

	print("Reading calibration data ...")
	bmp180.getCalibrationData()
	#print("AC1 = %d AC2 = %d AC3 = %d" % (bmp180.ac1, bmp180.ac2, bmp180.ac3))

	print("Obtaining temperature ...")
	print("T = %.3f °C" % (bmp180.calculateTemperature(bmp180.getTemperature())))

	print("Obtaining pressure ...")
	P = bmp180.getPressure(bmp180.preprarePressure())
	print("P = %.4f mBar" % (P / 10**5))
	print("A = %d m" % (bmp180.getAltitude(P)));

except Exception as e:
	print(e)