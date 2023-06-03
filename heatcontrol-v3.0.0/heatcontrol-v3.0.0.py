from machine import Pin, SoftSPI
import time

def system_init():
    ##########################
    ##### Pin of LED #########
    ##########################
    led = Pin(2, mode=Pin.OUT, value=0) # Defining Work Status Lights
    ##########################
    #### SPI of MAX6675 ######
    ##########################
    spi_max6675 = SoftSPI(baudrate=1000000, polarity=1, sck=Pin(14), miso=Pin(12), mosi=Pin(27)) # Create SPI peripheral 1 at frequency of 1MHz
    cs_max6675 = Pin(13, mode=Pin.OUT, value=1) # Create chip-select on pin 13, when cs(0),chip works.
    ##########################
    ##### SPI of OLED ########
    ##########################
    #留空
    return led, spi_max6675, cs_max6675

def get_time():
    mytime = time.localtime()
    mytime = "%d-%d-%d %d:%d:%d"%(mytime[0],mytime[1],mytime[2],mytime[3]+8,mytime[4],mytime[5])
    return mytime

def get_temperature():
    cs_max6675(0)
    data = spi_max6675.read(2)
    cs_max6675(1)
    TC_state=bin(data[1])[-3]  # get state of thermocouple
    t_output = data[0]*32+int(data[1]/8)
    temperature = t_output/4
    #temperature = t_output*1023.75/4096
    return TC_state, temperature

def mean_filtering():
    aaa=1
    

    

##########################
##### Main Program #######
##########################
led,spi_max6675,cs_max6675=system_init()

while(1):
    time.sleep_ms(1000)
    TC_state, temperature=get_temperature()
    #print(data)
    if TC_state == "1":
        print(get_time()," Error：热电偶断线……")
    else:
        print(get_time(), " 探头温度：", temperature, "℃")
    