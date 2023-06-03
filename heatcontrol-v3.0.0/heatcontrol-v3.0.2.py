from machine import Pin, SoftSPI
from ssd1306 import SSD1306_SPI
import time

def peripheral_init():
    ##########################
    ##### Pin of LED #########
    ##########################
    led = Pin(2, mode=Pin.OUT, value=0) # Defining Work Status Lights
    ##########################
    #### SPI of MAX6675 ######
    ##########################
    spi_max6675 = SoftSPI(baudrate=1000000, polarity=1, sck=Pin(14), miso=Pin(12), mosi=Pin(27)) # Create SoftSPI at frequency of 1MHz
    #Here, D27 is unused
    cs_max6675 = Pin(13, mode=Pin.OUT, value=1) # Create chip-select on pin 13, when cs(0),chip works.
    ##########################
    #### SPI of MAX31855 #####
    ##########################
    spi_max31855 = SoftSPI(baudrate=1000000, polarity=1, sck=Pin(26), miso=Pin(25), mosi=Pin(32)) # Create SoftSPI at frequency of 1MHz
    cs_max31855 = Pin(33, mode=Pin.OUT, value=1) # Create chip-select on pin 33, when cs(0),chip works.
    ##########################
    ##### SPI of OLED ########
    ##########################
    spi_oled = SoftSPI(baudrate=1000000, polarity=1, sck=Pin(35), miso=Pin(17), mosi=Pin(34))
    cs_oled = Pin(15, mode=Pin.OUT, value=1)
    dc_oled = Pin(16, mode=Pin.OUT)
    res_oled = Pin(4, mode=Pin.OUT)
    return led, spi_max6675, cs_max6675, spi_max31855, cs_max31855, spi_oled, cs_oled, dc_oled, res_oled

def relay_init():
    relay_1 = Pin(23, mode=Pin.OUT, value=1)
    relay_2 = Pin(22, mode=Pin.OUT, value=1)
    #relay_3 = Pin(1, mode=Pin.OUT, value=1)
    #relay_4 = Pin(3, mode=Pin.OUT, value=1)
    relay_5 = Pin(21, mode=Pin.OUT, value=1)
    relay_6 = Pin(19, mode=Pin.OUT, value=1)
    relay_7 = Pin(18, mode=Pin.OUT, value=1)
    relay_8 = Pin(5, mode=Pin.OUT, value=1)
    #return relay_1, relay_2, relay_3, relay_4, relay_5, relay_6, relay_7, relay_8
    return relay_1, relay_2, relay_5, relay_6, relay_7, relay_8

def get_time():
    mytime = time.localtime()
    mytime = "%d-%d-%d %d:%d:%d"%(mytime[0],mytime[1],mytime[2],mytime[3]+8,mytime[4],mytime[5])
    return mytime

def get_temperature_max6675():
    cs_max6675(0)
    data = spi_max6675.read(2)
    cs_max6675(1)
    TC_state=bin(data[1])[-3]  # get state of thermocouple
    t_output = data[0]*32+int(data[1]/8)
    temperature = t_output/4
    #temperature = t_output*1023.75/4096
    return TC_state, temperature

def get_temperature_max31855():
    print(1)

def temprature_init():
    temperature_history=[0, 0, 0, 0]
    TC_state, temperature_history[0] = get_temperature_max6675()
    TC_state, temperature_history[1] = get_temperature_max6675()
    TC_state, temperature_history[2] = get_temperature_max6675()
    TC_state, temperature_history[3] = get_temperature_max6675()
    return temperature_history

def mean_filtering_max6675(temperature_history):
    temperature_history[0:3] = temperature_history[1:4]
    TC_state, temperature_history[3] = get_temperature_max6675()
    temperature_now = (sum(temperature_history)-max(temperature_history)-min(temperature_history))/2
    return TC_state, temperature_history, temperature_now
    

##########################
##### Main Program #######
##########################
led, spi_max6675, cs_max6675, spi_max31855, cs_max31855, spi_oled, cs_oled, dc_oled, res_oled = peripheral_init()
#relay_1, relay_2, relay_3, relay_4, relay_5, relay_6, relay_7, relay_8 = relay_init()
relay_1, relay_2, relay_5, relay_6, relay_7, relay_8 = relay_init()
temperature_history = temprature_init()

while(1):
    time.sleep_ms(1000)
    TC_state, temperature_history, temperature_now = mean_filtering_max6675(temperature_history)
    #print(data)
    if TC_state == "1":
        print(get_time()," Error：热电偶断线……")
    else:
        print(get_time(), " 探头温度：", temperature_now, "℃")
        print("继电器1 %d 继电器2 %d 继电器5 %d 继电器6 %d"%(relay_1(),relay_2(),relay_5(),relay_6()))