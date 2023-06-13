from machine import Pin, SoftSPI, SoftI2C
from mlx90640_v4 import I2C, MLX90640, RefreshRate, __memory_manage
from sdcard import SDCard
import os, time, gc

#### Main Program ####
print("Beginning main ...")
gc.threshold(5000) # Seriously push the memory managing to the limit! Manages every <n> bytes allocated
 
ixc = I2C(pins=(5, 18), frequency=100000)
mlx = MLX90640(ixc)
mlx.refresh_rate = RefreshRate.REFRESH_0_5_HZ
frame = [0]*768

cs = Pin(33, mode=Pin.OUT, value=1)
spi = SoftSPI(baudrate=800000, polarity=1, sck=Pin(13), miso=Pin(12), mosi=Pin(14))

sd = SDCard(spi,cs)
os.VfsFat(sd) #文件系统初始化
os.mount(sd,"/sd") #挂载路径

while(1):
    print("Querying camera ...\n")
    mytime = time.localtime()
    #mytime = "%d-%d-%d %d:%d:%d"%(mytime[0],mytime[1],mytime[2],mytime[3]+8,mytime[4],mytime[5])
    mytime = "%d-%d-%d-%02d-%02d-%02d"%(mytime[0],mytime[1],mytime[2],mytime[3]+8,mytime[4],mytime[5])
    
    mlx.getFrame(frame)
    content = " ".join([str(x) for x in frame]) # s is "1 2 3"
    #print(content)
    w = open("/sd/IRphoto/"+mytime+".txt",'w')
    w.write(content)
    w.close() 
    __memory_manage()
    time.sleep_ms(100)