# 面包板版本

from machine import Pin, SoftSPI
from max31855 import MAX31855
from ssd1306 import SSD1306_SPI
import time, ntptime

#############################
#############################
###### Key Parameters #######
#############################
Tmax = 50
Tmin = -10
Ttarget = 30
Loops = 50000
Loopnow = 1
Mode = 0 # 0恒定温度，1循环测试
Systemstate = 1 # 1加热 ，0冷却

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
    spi_max31855_tec = SoftSPI(baudrate=800000, polarity=1, sck=Pin(26), miso=Pin(25), mosi=Pin(23)) # Create SoftSPI at frequency of 100kHz
    cs_max31855_tec = Pin(33, mode=Pin.OUT, value=1) # Create chip-select on pin 33, when cs(0),chip works.
    ##########################
    ##### SPI of OLED ########
    ##########################
    spi_oled = SoftSPI(baudrate=800000, polarity=1, sck=Pin(26), miso=Pin(25), mosi=Pin(12))
    cs_oled = Pin(32, mode=Pin.OUT)
    dc_oled = Pin(14, mode=Pin.OUT)
    res_oled = Pin(27, mode=Pin.OUT)
    return led, spi_max31855_tec, cs_max31855_tec, spi_oled, cs_oled, dc_oled, res_oled

def relay_init():
    relay_1 = Pin(13, mode=Pin.OUT, value=1)
    relay_2 = Pin(22, mode=Pin.OUT, value=1)
    relay_7 = Pin(18, mode=Pin.OUT, value=1)
    relay_8 = Pin(5, mode=Pin.OUT, value=1)
    return relay_1, relay_2, relay_7, relay_8

def relay_state(relay):
    state=relay()
    if state == 1:
        return "On"
    else:
        return "Off"
        
def get_time():
    mytime = time.localtime()
    #mytime = "%d-%d-%d %d:%d:%d"%(mytime[0],mytime[1],mytime[2],mytime[3]+8,mytime[4],mytime[5])
    mytime = "%d-%d-%d %02d:%02d:%02d"%(mytime[0],mytime[1],mytime[2],mytime[3],mytime[4],mytime[5])
    return mytime

def sensor_init(spi,cs):
    tc = MAX31855(spi, cs)
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

def operation(state):
    a=1
    '''待定'''
    
def holding_control():
    a=1
    '''待定'''

def loop_control():
    a=1
    '''待定'''
    

def pc_print():
    print(get_time(), " 探头温度：", temperature_now_tec, "℃", " 继电器1:", relay_state(relay_1),
          " 继电器2:", relay_state(relay_2), " 继电器7：", relay_state(relay_7), " 继电器8：", relay_state(relay_8))

def oled_print():
    oled.fill(0)
    nowtime=time.localtime()
    oled.text("%02d:%02d:%02d"%(nowtime[3],nowtime[4],nowtime[5]),0,2,1)
    oled.text(" T_samp:%.2fC"%temperature_now_tec,0,54,1) #变量要改为Samp
    #Mode print
    if Mode == 0: #恒定温度
        oled.text("Holding",72,2,1)
        oled.text("  Target:%dC"%(Ttarget),0,15,1)
        oled.text("  T_TEC:%.2fC"%temperature_now_tec,0,41,1) #变量要改为Samp
    elif Mode == 1: #循环
        oled.text("Cycle",75,2,1)
        oled.text("Target:%d to %d"%(Tmin,Tmax),0,15,1)
        oled.text("  Loops:%05d"%Loopnow,0,41,1)
    #Status print
    if Systemstate == 1:
        oled.text(" Status:Heating",0,28,1)
    else:
        oled.text(" Status:Cooling",0,28,1)
    oled.show()
    

##########################
##### Main Program #######
##########################

#time_init()
led, spi_max31855_tec, cs_max31855_tec, spi_oled, cs_oled, dc_oled, res_oled = peripheral_init()
#relay_1, relay_2, relay_3, relay_4, relay_5, relay_6, relay_7, relay_8 = relay_init()
relay_1, relay_2, relay_7, relay_8 = relay_init()
tc = sensor_init(spi_max31855_tec,cs_max31855_tec)
oled = SSD1306_SPI(128,64,spi_oled,dc_oled,res_oled,cs_oled)
oled.poweron()

temperature_history_tec = temprature_init()

while(1):
    time.sleep_ms(1000)
    led(not led())
    temperature_history_tec, temperature_now_tec = mean_filtering_max31855(temperature_history_tec)
    pc_print()
    oled_print()