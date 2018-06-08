# -*- coding: utf-8 -*-

import time
import serial
from usbi2c.usbi2c import *

class LCD1602:

	def __init__(self, adapter):
		self.address = 0x27
		self.adapter = adapter

		self.rs = 0x01
		self.rw = 0x02
		self.enable = 0x04
		self.bg = 0x08

		self.background = 0
		self.opts = 0

	def _send(self, data): 
		self.adapter.Write(bytes([data | self.enable | self.opts, data | self.opts]))
		self.adapter.Start()
		self.adapter.WaitForCompletion()

	def SendCommand(self, data):
		self._send((data & 0xF0))
		self._send(((data << 4) & 0xF0))

	def SendChar(self, data):
		self._send((data & 0xF0) | self.rs)
		self._send(((data << 4) & 0xF0) | self.rs)

	def InitLCD(self):
		self.adapter.Reset()
		self.adapter.Address(self.address)
		self._send(0x30)
		time.sleep(0.01)
		self._send(0x30)
		self._send(0x30)
		self._send(0x20)

		# 2LINE
		self.SendCommand(0x28)

		# CLEAN
		self.SendCommand(0x01)
		time.sleep(0.001)

		# ENTRY
		self.SendCommand(0x06)

		# CURSOR
		self.SendCommand(0x0F)

	def SendText(self, text):
		for i in text:
			self.SendChar(ord(i))

	def Background(self, state):
		self.background = state
		self.opts = self.bg if self.background else 0
		self._send(self.enable)

	def gotoXY(self, x, y):
		self.SendCommand(x + (0x80 | (0x40 if y == 1 else 0)))

try:
	print("LCD1602 demo application")
	uart = serial.Serial('/dev/ttyACM0', timeout = 1);

	adapter = USBI2C(uart)
	lcd = LCD1602(adapter)
	lcd.InitLCD()

	lcd.SendText("LCD1602 demo app")
	lcd.Background(1);

	lcd.gotoXY(2, 1)
	lcd.SendText("USB-I2C")

except Exception as e:
	print(e)