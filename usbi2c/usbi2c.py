import time

USBI2C_error_messages = {
	'a': "NACK received",
	'A': "Invalid address",
	'L': "Invalid length",
	'C': "Unknown command",
	'U': "Unknown escape sequence",
	'T': "Timer expired"
	}

class AdapterResponseException(Exception):

	def __init__(self, char):
		self.char = char

	def __str__(self):
		if self.char in USBI2C_error_messages:
			return USBI2C_error_messages[self.char]
		return "Unknown response"

class USBI2C:

	def __init__(self, uart):
		self.waitInterval = 0.02
		self.wait = 1.5
		self.uart = uart

	def _send(self, data):
		buf = b''
		for byte in data:
			if byte == 27:
				buf += b'\x5c\xb1'
			elif byte == 92:
				buf += b'\x5c\xc5'
			else:
				buf += bytes([byte])
		self.uart.write(buf)

	def _recv(self, len):
		buf = b''
		escaped = 0
		while len:
			byte = self.uart.read(1)
			if byte == b'\x5c':
				escaped = 1
			else:
				len = len - 1
				if escaped:
					if byte == b'\xb1':
						byte = b'\x1b'
					elif byte == b'\xc5':
						byte = b'\x5c'
					escaped = 0
				buf += byte
		return buf

	def Reset(self):
		self.uart.write(b'\x1b');
		if not self.StatusOK():
			raise Exception("Adapter not ready")

	def Timing(self, speed):
		if speed == 10:
			timing = b'\xc7\xc3\x42\xb0';
		elif speed == 100:
			timing = b'\x13\x0f\x42\xb0'
		elif speed == 400:
			timing = b'\x09\x03\x33\x50'
		elif speed == 1000:
			timing = b'\x03\x01\x11\x50'
		else:
			raise Exception("Unsuppored timing")
		self.uart.write(b't')
		self.uart.write(timing)
		self.uart.write(b'i')

	def Serial(self):
		self.uart.write(b'n')
		return self._recv(8).decode()

	def Address(self, address):
		if isinstance(address, int):
			if address < 0 or address > 128:
				raise Exception('Address out of range')
			address = bytes([address])
		elif isinstance(address, str) and len(address) > 0:
			address = address[0].encode('ascii')
		elif not isinstance(address, bytes):
			raise Exception('Address is not an integer')
		self.uart.write(b'A')
		self._send(address)

	def Write(self, data):
		l = len(data)
		if l < 1 or l > 64:
			raise Exception('Data length out of range')
		self.uart.write(b'W')
		self._send(bytes([l]));
		self.uart.write(b'w')
		self._send(data)

	def ReadLength(self, l):
		if l < 1 or l > 64:
			raise Exception('Data length out of range')
		self.uart.write(b'R')
		self._send(bytes([l]))

	def Read(self, l):
		self.uart.write(b'r')
		r = self._recv(l)
		if (len(r) != l):
			raise Exception('Insufficient data received')
		return r

	def Start(self):
		self.uart.write(b'S');

	def Busy(self):
		self.uart.write(b's');
		r = self.uart.read(1)
		return len(r) == 0 or r == b'\xff'

	def StatusOK(self):
		self.uart.write(b'E');
		r = self.uart.read(1)
		if len(r) == 0:
			raise Exception("Communication error")
		if r == b'N':
			return True
		raise AdapterResponseException(r)
		return False

	def WaitForCompletion(self):
		elapsedTime = 0
		while self.Busy():
			elapsedTime += self.waitInterval
			time.sleep(self.waitInterval)
			if elapsedTime > self.wait:
				raise Exception("Communication timeout")
		self.StatusOK()