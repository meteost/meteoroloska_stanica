import time
from w1thermsensor import *

sensor = W1ThermSensor()

while True:
	temperature = sensor.get_temperature()
	print("Temp: %.1f\xb0C" % temperature)
	time.sleep(1)
