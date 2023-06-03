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
Tamb = 26 #当前环境温度/水冷温度
Loops = 50000
Loopnow = 1
Mode = 0 # 0恒定温度，1循环测试
Systemstate = 0 # 0 空置 ，1冷却，2加热
Achieve =2 # 循环模式触及边界剩余次数，一轮2次

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
    #U2 TC1
    spi_max31855_tec = SoftSPI(baudrate=800000, polarity=1, sck=Pin(13), miso=Pin(12), mosi=Pin(14)) # Create SoftSPI at frequency of 800kHz
    cs_max31855_tec = Pin(33, mode=Pin.OUT, value=1) # Create chip-select on pin 33, when cs(0),chip works.
    #U3 TC2
    spi_max31855_samp = SoftSPI(baudrate=800000, polarity=1, sck=Pin(13), miso=Pin(12), mosi=Pin(14)) # Create SoftSPI at frequency of 800kHz
    cs_max31855_samp = Pin(25, mode=Pin.OUT, value=1) # Create chip-select on pin 33, when cs(0),chip works.
    ##########################
    ##### SPI of OLED ########
    ##########################
    spi_oled = SoftSPI(baudrate=800000, polarity=1, sck=Pin(13), miso=Pin(12), mosi=Pin(14))
    cs_oled = Pin(32, mode=Pin.OUT)
    dc_oled = Pin(27, mode=Pin.OUT)
    res_oled = Pin(26, mode=Pin.OUT)
    return led, spi_max31855_tec, cs_max31855_tec, spi_max31855_samp, cs_max31855_samp, spi_oled, cs_oled, dc_oled, res_oled

def relay_init():
    relay_1 = Pin(23, mode=Pin.OUT, value=0)
    relay_2 = Pin(22, mode=Pin.OUT, value=0)
    relay_3 = Pin(21, mode=Pin.OUT, value=0)
    relay_4 = Pin(19, mode=Pin.OUT, value=0)
    return relay_1, relay_2, relay_3, relay_4

def relay_state(relay):
    state=relay()
    if state == 1:
        return "On"
    else:
        return "Off"
        
def get_time():
    mytime = time.localtime()
    #mytime = "%d-%d-%d %d:%d:%d"%(mytime[0],mytime[1],mytime[2],mytime[3]+8,mytime[4],mytime[5])
    mytime = "%d-%d-%d %02d:%02d:%02d"%(mytime[0],mytime[1],mytime[2],mytime[3]+8,mytime[4],mytime[5])
    return mytime

def sensor_init(spi_tec, cs_tec, spi_samp, cs_samp):
    tc_tec = MAX31855(spi_tec, cs_tec)
    tc_samp = MAX31855(spi_samp, cs_samp)
    return tc_tec, tc_samp

def temprature_init():
    temperature_history_tec=[0, 0, 0, 0]
    temperature_history_tec[0] = tc_tec.read()
    temperature_history_tec[1] = tc_tec.read()
    temperature_history_tec[2] = tc_tec.read()
    temperature_history_tec[3] = tc_tec.read()
    temperature_history_samp=[0, 0, 0, 0]
    temperature_history_samp[0] = tc_tec.read()
    temperature_history_samp[1] = tc_tec.read()
    temperature_history_samp[2] = tc_tec.read()
    temperature_history_samp[3] = tc_tec.read()
    return temperature_history_tec, temperature_history_samp

def mean_filtering_max31855(temperature_history,tc):
    temperature_history[0:3] = temperature_history[1:4]
    temperature_history[3] = tc.read()
    temperature_now = (sum(temperature_history)-max(temperature_history)-min(temperature_history))/2
    return temperature_history, temperature_now
    
def holding_control():
    if temperature_now_samp < Ttarget:
        if temperature_now_samp > (Tamb-5): #环境无法提供大幅升温
            relay_1.off() # TEC
            relay_2.on() # Heater
            Systemstate = 2 # Heating
        else:
            relay_1.off()
            relay_2.off()
            Systemstate = 0 #Idle
    else:
        if temperature_now_samp < (Tamb+15): #环境无法提供大幅降温
            relay_1.on() #TEC
            relay_2.off() #Heater
            Systemstate = 1 # Cooling
        else: #室温温差足够大
            relay_1.off() #TEC
            relay_2.off() #Heater
            Systemstate = 0 #Idle
    return Systemstate

def loop_control():
    a=1
    '''待定'''
    

def pc_print():
    print(get_time(), " TEC温度：", temperature_now_tec, "℃", " Samp温度：", temperature_now_samp, "℃",
          " 继电器1:", relay_state(relay_1), " 继电器2:", relay_state(relay_2),
          " 继电器3：", relay_state(relay_3), " 继电器4：", relay_state(relay_4))

def oled_print():
    oled.fill(0)
    nowtime=time.localtime()
    oled.text("%02d:%02d:%02d"%(nowtime[3],nowtime[4],nowtime[5]),0,2,1)
    oled.text(" T_samp:%.2fC"%temperature_now_samp,0,54,1) #变量要改为Samp
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
    if Systemstate == 0:
        oled.text("  Status:Idle",0,28,1)
    elif Systemstate == 1:
        oled.text(" Status:Cooling",0,28,1)
    else:
        oled.text(" Status:Heating",0,28,1)
    oled.show()
    

##########################
##### Main Program #######
##########################

'''
#network and time
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('D241', 'dd241241')
ntptime.NTP_DELTA = 3155644800
ntptime.host = 'ntp1.aliyun.com'
ntptime.settime()
'''

#time_init()
led, spi_tec, cs_tec, spi_samp, cs_samp, spi_oled, cs_oled, dc_oled, res_oled = peripheral_init()
#relay_1, relay_2, relay_3, relay_4, relay_5, relay_6, relay_7, relay_8 = relay_init()
relay_1, relay_2, relay_3, relay_4 = relay_init()
tc_tec, tc_samp = sensor_init(spi_tec,cs_tec,spi_samp,cs_samp)
oled = SSD1306_SPI(128,64,spi_oled,dc_oled,res_oled,cs_oled)
oled.poweron()

temperature_history_tec, temperature_history_samp = temprature_init()

while(1):
    time.sleep_ms(500)
    led(not led())
    temperature_history_tec, temperature_now_tec = mean_filtering_max31855(temperature_history_tec,tc_tec)
    temperature_history_samp, temperature_now_samp = mean_filtering_max31855(temperature_history_samp,tc_samp)
    ###################
    ## Control Part ###
    ###################
    if Mode == 0:
        Systemstate=holding_control()
    elif Mode ==1:
        Loops, Systemstate = loop_control()
    #显示输出    
    pc_print()
    oled_print()
        
        