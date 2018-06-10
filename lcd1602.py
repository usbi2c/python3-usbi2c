# -*- coding: utf-8 -*-

import serial
from usbi2c.usbi2c import *
from lcd.pcf8574 import PCF8574

try:
	print("LCD1602 demo application")
	uart = serial.Serial('/dev/ttyACM0', timeout = 1);

	adapter = USBI2C(uart)
	lcd = PCF8574(adapter)

	lcd.InitLCD()

	lcd.SendText("LCD1602 demo app")
	lcd.Background(1);

	lcd.gotoXY(2, 1)
	lcd.SendText("USB-I2C")

	lcd.SetCursor(1)

except Exception as e:
	print(e)