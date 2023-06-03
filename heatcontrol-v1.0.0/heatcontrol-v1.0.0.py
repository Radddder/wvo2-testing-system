from machine import Pin, SPI
import time

led = Pin(2, mode=Pin.OUT, value=0) # Defining Work Status Lights
hspi = SPI(1, baudrate=100, sck=Pin(14), miso=Pin(12), mosi=None,firstbit=SPI.MSB) # Create SPI peripheral 1 at frequency of 100Hz
cs = Pin(13, mode=Pin.OUT, value=1) # Create chip-select on pin 13, when cs(0),chip works.
buf = bytearray(2) # 2byte,16位

cs(0)
while(1):
    #cs(0)
    hspi.readinto(buf) 
    #cs(1)
    #print(buf)
    #mvoltage=buf[0]*2^5+buf[1]%4
    #print(mvoltage)
    time.sleep_ms(500)
    
