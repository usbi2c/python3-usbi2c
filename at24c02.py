# -*- coding: utf-8 -*-

'''
This code is experimental: always check if writing was successful.
'''

import serial
import time
from usbi2c.usbi2c import *

class AT24C02:

	def __init__(self, adapter):
		self.address = 0x50
		self.adapter = adapter

	def ACK_polling(self):
		'''
		Keep sending address and wait until 
		'''
		elapsedTime = 0
		while elapsedTime < 1:
			nack = 0
			try:
				self.adapter.ReadLength(1)
				self.adapter.Start()
				self.adapter.WaitForCompletion()
			except Exception as e:
				if e.char and e.char == b'a':
					nack = 1
			if nack == 0:
				break;
			time.sleep(0.1)
			elapsedTime += 0.1

	def Read(self, length, offset = 0):
		buf = b''
		if length < 0:
			raise Exception("Length must be positive")

		self.adapter.Reset()
		self.adapter.Address(self.address)

		while length:
			l = 64 if length > 64 else length
			self.adapter.Write(bytes([offset]))
			self.adapter.ReadLength(l)
			self.adapter.Start()
			self.adapter.WaitForCompletion()
			buf += self.adapter.Read(l)
			length -= l
			offset += l

		return buf

	def Write(self, data, offset = 0):
		k = 0
		self.adapter.Reset()
		self.adapter.Address(self.address)

		length = len(data)
		while length:
			l = 8 if length > 8 else length
			self.adapter.Write(bytes([offset]) + data[k:k+l])
			self.adapter.Start()
			self.adapter.WaitForCompletion()
			length -= l
			offset += l
			k += l
			self.ACK_polling()


try:
	print("24C02 I2C EEPROM demo application")
	uart = serial.Serial('/dev/ttyACM0', timeout = 1);

	adapter = USBI2C(uart)
	at24c02 = AT24C02(adapter)

	w = "Hello World ! 24C02 I2C EEPROM demo application"
	length = len(w)
	print("Writting: %s" % (w))
	at24c02.Write(w.encode('utf-8'), offset = 0)

	r = at24c02.Read(length).decode()
	print("Reading: %s" % (r))

except Exception as e:
	print(e)