from machine import Pin, SoftSPI
import time

##########################
##### Pin of LED #########
##########################
led = Pin(2, mode=Pin.OUT, value=0) # Defining Work Status Lights
##########################
#### SPI of MAX6675 ######
##########################
spi = SoftSPI(baudrate=1000000, polarity=1, sck=Pin(14), miso=Pin(12), mosi=Pin(27)) # Create SPI peripheral 1 at frequency of 1MHz
cs = Pin(13, mode=Pin.OUT, value=1) # Create chip-select on pin 13, when cs(0),chip works.
##########################
##### SPI of OLED ########
##########################
#留空

def get_time():
    mytime = time.localtime()
    mytime = "%d-%d-%d %d:%d:%d"%(mytime[0],mytime[1],mytime[2],mytime[3]+8,mytime[4],mytime[5])
    return mytime

while(1):
    time.sleep_ms(1000)
    cs(0)
    data = spi.read(2)
    cs(1)
    #print(data)
    TC_state=bin(data[1])[-3]  # get state of thermocouple
    if TC_state == "1":
        print(get_time()," Error：热电偶断线……")
    else:
        t_output = data[0]*32+int(data[1]/4)
        temperature = t_output/4
        print(get_time(), t_output," ", temperature,"℃")
    