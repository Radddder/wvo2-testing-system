'''
import esp
print(esp.flash_size())
#ESP32本地实际4MB大小
'''

from machine import Pin, SoftSPI
import time,os
from sdcard import SDCard

cs = Pin(33, mode=Pin.OUT, value=1)
spi = SoftSPI(baudrate=800000, polarity=1, sck=Pin(13), miso=Pin(12), mosi=Pin(14)) 

sd = SDCard(spi,cs)

def write_png(buf, width, height):
    # buf - bytearray
    

def main():
    
    os.Vfsfat(sd) #文件系统初始化
    os.mount(sd,"/sd") #挂载路径
    
    fb = os.statvfs("/sd")
    print("Capacity = %d MB"%(fb[0]*fb[2]/1024/1024)) #总容量
    print("Remaining = %d MB"%(fb[0]*fb[3]/1024/1024)) #剩余容量
    
    '''
    os.mkdir("/sd/IRphoto") #创建dir
    #os.rmdir("/sd/IRphoto")
    print(os.listdir("/sd"))
    '''
    
    w = open("/sd/IRphoto/test.txt",'w',encoding="utf-8")
    w.write("testdata")
    w.close() 
    
    print(os.listdir("/sd/IRphoto"))
    
    while True:
        pass
    
if __main__ == "__main__":
    main()
