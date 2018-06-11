import time

USBI2C_error_messages = {
	b'a': "NACK received",
	b'A': "Invalid address",
	b'L': "Invalid length",
	b'C': "Unknown command",
	b'U': "Unknown escape sequence",
	b'T': "Timer expired"
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
			if byte == b'':
				raise Exception("Read timeout")
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
		'''
		This command resets the adapter into defined (reset) state.
		'''
		self.uart.flushInput()
		self.uart.flushOutput()
		self.uart.write(b'\x1b')
		if not self.StatusOK():
			raise Exception("Adapter not ready")

	def Timing(self, speed):
		'''
		This command sets the I2C bus frequency and resets into defined state.
		'''
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
		'''
		This command retrieves 96-bit serial number from the adapter.
		'''
		self.uart.write(b'n')
		return self._recv(24).decode()

	def Address(self, address):
		'''
		This command sets address of target I2C device.
		'''
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
		'''
		This command writes data into adapter transmit buffer.
		'''
		l = len(data)
		if l < 1 or l > 64:
			raise Exception('Data length out of range')
		self.uart.write(b'W')
		self._send(bytes([l]));
		self.uart.write(b'w')
		self._send(data)

	def ReadLength(self, l):
		'''
		This commands sets the number of expected bytes from target I2C device.
		'''
		if l < 1 or l > 64:
			raise Exception('Data length out of range')
		self.uart.write(b'R')
		self._send(bytes([l]))

	def Read(self, l):
		'''
		This commands reads the data from adapter receive buffer.
		'''
		self.uart.write(b'r')
		r = self._recv(l)
		if (len(r) != l):
			raise Exception('Insufficient data received')
		return r

	def Start(self):
		'''
		This command starts the transmission with target I2C device.
		'''
		self.uart.write(b'S');

	def Busy(self):
		'''
		This command checks if the adapter is busy (transmission takes place).
		'''
		self.uart.write(b's');
		r = self.uart.read(1)
		return len(r) == 0 or r == b'\xff'

	def StatusOK(self):
		'''
		This command checks if an error has occured.
		'''
		self.uart.write(b'E');
		r = self.uart.read(1)
		if len(r) == 0:
			raise Exception("Communication error")
		if r == b'N':
			return True
		raise AdapterResponseException(r)
		return False

	def WaitForCompletion(self):
		'''
		Busy-wait loop while transmission takes place.
		'''
		elapsedTime = 0
		while self.Busy():
			elapsedTime += self.waitInterval
			time.sleep(self.waitInterval)
			if elapsedTime > self.wait:
				raise Exception("Communication timeout")
		self.StatusOK()