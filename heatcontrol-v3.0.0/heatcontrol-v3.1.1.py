from machine import Pin, SoftSPI
from max31855 import MAX31855
from ssd1306 import SSD1306_SPI
import time, ntptime

def time_init():
    ntptime.NTP_DELTA = 3155644800
    ntptime.host = 'ntp1.aliyun.com'
    ntptime.settime()

def peripheral_init():
    ##########################
    ##### Pin of LED #########
    ##########################
    led = Pin(2, mode=Pin.OUT, value=0) # Defining Work Status Lights
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
    return led, spi_max31855, cs_max31855, spi_oled, cs_oled, dc_oled, res_oled

def relay_init():
    relay_1 = Pin(23, mode=Pin.OUT, value=1)
    relay_2 = Pin(22, mode=Pin.OUT, value=1)
    relay_7 = Pin(18, mode=Pin.OUT, value=1)
    relay_8 = Pin(5, mode=Pin.OUT, value=1)
    return relay_1, relay_2, relay_7, relay_8

def relay_state(relay):
    state=relay()
    if state == 1:
        return "开"
    else:
        return "关"
        

def get_time():
    mytime = time.localtime()
    #mytime = "%d-%d-%d %d:%d:%d"%(mytime[0],mytime[1],mytime[2],mytime[3]+8,mytime[4],mytime[5])
    mytime = "%d-%d-%d %d:%d:%d"%(mytime[0],mytime[1],mytime[2],mytime[3]+8,mytime[4],mytime[5])
    return mytime

def sensor_init(spi,cs):
    tc = MAX31855(spi_max31855, cs_max31855)
    return tc

def temprature_init():
    temperature_history=[0, 0, 0, 0]
    temperature_history[0] = tc.read()
    temperature_history[1] = tc.read()
    temperature_history[2] = tc.read()
    temperature_history[3] = tc.read()
    return temperature_history

def mean_filtering_max31855(temperature_history):
    temperature_history[0:3] = temperature_history[1:4]
    temperature_history[3] = tc.read()
    temperature_now = (sum(temperature_history)-max(temperature_history)-min(temperature_history))/2
    return temperature_history, temperature_now
    

##########################
##### Main Program #######
##########################
Tmax = 50
Tmin = -10
Loops = 1000

led, spi_max31855, cs_max31855, spi_oled, cs_oled, dc_oled, res_oled = peripheral_init()
#relay_1, relay_2, relay_3, relay_4, relay_5, relay_6, relay_7, relay_8 = relay_init()
relay_1, relay_2, relay_7, relay_8 = relay_init()
tc = sensor_init(spi_max31855,cs_max31855)
temperature_history = temprature_init()

while(1):
    time.sleep_ms(1000)
    #relay_1(not relay_1())
    temperature_history, temperature_now = mean_filtering_max31855(temperature_history)
    print(get_time(), " 探头温度：", temperature_now, "℃", " 继电器1:", relay_state(relay_1),
          " 继电器2:", relay_state(relay_2), " 继电器7：", relay_state(relay_7), " 继电器8：", relay_state(relay_8))