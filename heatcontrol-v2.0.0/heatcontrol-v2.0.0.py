from machine import Pin, SPI
from max6675 import MAX6675
import time

so = Pin(12, Pin.IN)
sck = Pin(14, Pin.OUT)
cs = Pin(13, Pin.OUT)

temperature = MAX6675(sck, cs, so)

for _ in range(10):
    cs(0)
    time.sleep(1)
    print(temperature.read())
    cs(1)