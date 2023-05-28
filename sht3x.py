# -*- coding: utf-8 -*-

import serial
import struct
from argparse import ArgumentParser
from usbi2c import USBI2C

def TransformTemperature(r):
	val = struct.unpack('>H', r)[0]
	return -45 + 175.0 * val / 2**16

def TransformHumidity(r):
	val = struct.unpack('>H', r)[0]
	return 100.0 * val / 2**16

def CRC8(data):
	crc = 0xff
	for byte in iter(data):
		crc ^= byte
		for i in range(8):
			mix = crc & 0x80
			crc <<= 1
			if mix:
				crc ^= 0x31
			crc &= 0xff
	return crc


class SHT3X:

	def __init__(self, adapter):
		self.address = 0x44
		self.adapter = adapter

	def Read(self, command):
		self.adapter.Reset()
		self.adapter.Address(self.address)

		# Write a command to SHT3X
		self.adapter.Write(command)
		self.adapter.Start()
		self.adapter.WaitForCompletion()

		# Request 6 bytes from SHT3X
		self.adapter.ReadLength(6)
		self.adapter.Start()
		# Any bytes less will result in NACK
		self.adapter.WaitForCompletion()

		# Read received bytes from interface
		return self.adapter.Read(6)

	def CRC(self, data):
		return CRC8(data)


def measure(uart):
	adapter = USBI2C(uart)
	sht3x = SHT3X(adapter)

	resp = sht3x.Read(b"\x2c\x06")

	t = (
		None if sht3x.CRC(resp[0:3]) else
		TransformTemperature(resp[0:2])
	)
	h = (
		None if sht3x.CRC(resp[3:6]) else
		TransformHumidity(resp[3:5])
	)

	if h and t:
		print("T = %.3f °C\nH = %.2f %%" % (t, h))

print("SHT3X demo application")

parser = ArgumentParser(description="")
parser.add_argument('--port',
	help="serial port name",
)

args = parser.parse_args()
port = "/dev/ttyACM0" if args.port is None else args.port

try:
	uart = serial.Serial(port, timeout = 1)
	measure(uart)
	uart.close()

except Exception as e:
	print(e)