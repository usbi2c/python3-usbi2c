import time

class PCF8574:

	def __init__(self, adapter):
		self.address = 0x27
		self.adapter = adapter

		'''
		This example works for I2C LCD version 1, black PCB, with words: POWER, A0, A1 and A2.

		PCF8574T connections:
		addr, en,rw,rs,d4,d5,d6,d7,bl,blpol
		0x27,  2, 1, 0, 4, 5, 6, 7, 3, POSITIVE
		'''
		self.rs = 0x01
		self.rw = 0x02
		self.enable = 0x04
		self.bg = 0x08

		self.background = 0
		self.opts = 0

	def _send_byte(self, data):
		self.adapter.Write(bytes([data | self.enable | self.opts, data | self.opts]))
		self.adapter.Start()
		self.adapter.WaitForCompletion()

	def _send_bytes(self, data):
		buf = []
		for byte in data:
			buf += [byte | self.enable | self.opts]
			buf += [byte | self.opts]
		k = 0
		length = len(buf)
		while length:
			l = 64 if length > 64 else length
			self.adapter.Write(bytes(buf[k:k+l]))
			self.adapter.Start()
			self.adapter.WaitForCompletion()
			length -= l
			k += l

	def SendCommand(self, data):
		self._send_bytes([data & 0xF0, (data << 4) & 0xF0])

	def SendChar(self, data):
		self._send_bytes([(data & 0xF0) | self.rs, ((data << 4) & 0xF0) | self.rs])

	def Clear(self):
		self.SendCommand(0x01)
		time.sleep(0.001)

	def Configure(self):
		# LCD 2LINE
		self.SendCommand(0x28)

		# LCD ENTRY
		self.SendCommand(0x06)

	def SetCursor(self, config = 0):
		'''
		0 - nothing
		1 - blinking box
		2 - underline
		'''
		self.SendCommand(0x0C | (config & 0x03))

	def InitLCD(self):
		self.adapter.Reset()
		self.adapter.Address(self.address)

		# LCD RESET
		self._send_byte(0x30)
		time.sleep(0.01)
		self._send_byte(0x30)
		self._send_byte(0x30)

		# LCD 4-lines
		self._send_byte(0x20)

		self.Configure()
		self.Clear()
		self.SetCursor()

	def SendText(self, text):
		buf = []
		for i in text:
			buf += [(ord(i) & 0xF0) | self.rs]
			buf += [((ord(i) << 4) & 0xF0) | self.rs]
		self._send_bytes(buf)

	def Background(self, state):
		self.background = state
		self.opts = self.bg if self.background else 0
		self._send_byte(self.enable)

	def gotoXY(self, x, y):
		self.SendCommand(x + (0x80 | (0x40 if y == 1 else 0)))