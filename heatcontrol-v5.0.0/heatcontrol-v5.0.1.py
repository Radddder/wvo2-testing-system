'''
Todolist
1、保存数据到SD卡
2、MLX90640红外成像
3、半球积分控制集成
'''


from machine import Pin, SoftSPI
from max31855v2 import MAX31855
from ssd1306 import SSD1306_SPI
from font import Font
import time, ntptime

#############################
#############################
###### Key Parameters #######
#############################
Tmax = 40
Tmin = -5
Ttarget = 30
Tamb = 30 #当前环境温度/水冷温度
Loops = 50000
Loopnow = 0 #已完成循环次数
Mode = 1 # 0恒定温度，1循环测试
Systemstate = 0 # 0 空置 ，1冷却，2加热
Achieve = 2 # 循环模式触及边界剩余次数，一轮2次

def peripheral_init():
    ##########################
    ##### Pin of LED #########
    ##########################
    led = Pin(2, mode=Pin.OUT, value=0) # Defining Work Status Lights
    ##########################
    #### SPI of MAX31855 #####
    ##########################
    #U2 TC1
    '''
    Empyt
    '''
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
    return led, spi_max31855_samp, cs_max31855_samp, spi_oled, cs_oled, dc_oled, res_oled

def relay_init():
    relay_1 = Pin(23, mode=Pin.OUT, value=0)   #TEC
    relay_2 = Pin(22, mode=Pin.OUT, value=0)   #Heater
    relay_3 = Pin(21, mode=Pin.OUT, value=0)   #D610
    relay_4 = Pin(19, mode=Pin.OUT, value=0)   #T630C
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

#def sensor_init(spi_tec, cs_tec, spi_samp, cs_samp):
def sensor_init(spi_samp, cs_samp):
    tc_samp = MAX31855(spi_samp, cs_samp)
    return tc_samp

def temprature_init():
    temperature_history_samp=[0, 0, 0, 0]
    temperature_history_samp[0] = tc_samp.read()
    temperature_history_samp[1] = tc_samp.read()
    temperature_history_samp[2] = tc_samp.read()
    temperature_history_samp[3] = tc_samp.read()
    return temperature_history_samp

def mean_filtering_max31855(temperature_history,tc):
    temperature_history[0:3] = temperature_history[1:4] #左闭右开，1-3位移到0-2
    t_temp = tc.read()
    while t_temp == "error":
        time.sleep_ms(1000)
        t_temp = tc.read()
    temperature_history[3] = t_temp
    temperature_now = (sum(temperature_history)-max(temperature_history)-min(temperature_history))/2
    return temperature_history, temperature_now
    
def holding_control():
    if temperature_now_samp < Ttarget:
        if temperature_now_samp > (Tamb-10): #环境无法提供大幅升温
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

def loop_control(Achieve,Loopnow,Systemstate):
    if Loopnow <= Loops:      
        # 先升后降
        if Achieve == 2: #上升段
            if temperature_now_samp < Tmax:
                relay_1.off() #TEC
                relay_2.on() #Heater
                Systemstate = 2 # Heating
            else:
                Achieve = Achieve - 1
                relay_1.on() #TEC
                relay_2.off() #Heater
                relay_3.on()
                relay_3.off() # take a photo
                relay_4.on()
                relay_4.off()
                Systemstate = 1 # Cooling
        elif Achieve == 1: #下降段
            if temperature_now_samp < Tmin:
                Achieve = Achieve - 1 
                relay_1.off() #TEC
                relay_2.on() #Heater
                relay_3.on()
                relay_3.off() # take a photo
                relay_4.on()
                relay_4.off()
                Systemstate = 2 # Heating
            else:
                relay_1.on() #TEC
                relay_2.off() #Heater
                Systemstate = 1 # Cooling
    else:
        Systemstate = 0 #Idle
    if Achieve == 0:
        Achieve = 2 #reset
        Loopnow = Loopnow + 1
    return Loopnow, Achieve, Systemstate
    

def pc_print():
    #print(get_time(), " TEC温度：", temperature_now_tec, "℃", " Samp温度：", temperature_now_samp, "℃",
    print(get_time(), " Samp温度：", temperature_now_samp, "℃",
          " TEC:", relay_state(relay_1), " Heater:", relay_state(relay_2))

def oled_print():
    nowtime=time.localtime()
    oled.text("Time: %02d:%02d:%02d"%(nowtime[3],nowtime[4],nowtime[5]),0,2,16)
    oled.text("T:%.1fC"%temperature_now_samp,0,24,32) #Samp温度
    oled.show()
    
def take_photo():
    relay_3.on()
    time.sleep_ms(250)
    relay_3.off()
    

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

led, spi_samp, cs_samp, spi_oled, cs_oled, dc_oled, res_oled = peripheral_init()
relay_1, relay_2, relay_3, relay_4 = relay_init()
tc_samp = sensor_init(spi_samp,cs_samp)
oled_spi = SSD1306_SPI(128,64,spi_oled,dc_oled,res_oled,cs_oled)
oled = Font(oled_spi)

temperature_history_samp = temprature_init()

while(1):
    time.sleep_ms(750)
    led(not led())
    temperature_history_samp, temperature_now_samp = mean_filtering_max31855(temperature_history_samp,tc_samp)
    ###################
    ## Control Part ###
    ###################
    if Mode == 0:
        Systemstate = holding_control()
    elif Mode ==1:
        Loopnow, Achieve, Systemstate = loop_control(Achieve,Loopnow,Systemstate)
    #显示输出    
    pc_print()
    oled_print()
    if led():
        take_photo()
    else:
        time.sleep_ms(250)        
        