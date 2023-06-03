from machine import Pin, SoftSPI
import time
import math

led = Pin(2, mode=Pin.OUT, value=0) # Defining Work Status Lights
spi = SoftSPI(baudrate=1000, polarity=1, sck=Pin(14), miso=Pin(12), mosi=Pin(27)) # Create SPI peripheral 1 at frequency of 1kHz
cs = Pin(13, mode=Pin.OUT, value=1) # Create chip-select on pin 13, when cs(0),chip works.

while(1):
    time.sleep_ms(500)
    cs(0)
    data=spi.read(2)
    cs(1)
    print(data)
    #bin(data[1])[3:5]
    t_output=data[0]*32+int(data[1]/4)
    print(t_output)
    temperature=t_output/4
    print(str(temperature)+"℃")
    