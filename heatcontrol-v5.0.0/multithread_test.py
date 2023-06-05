from machine import Pin
import time
import _thread

def second_thread():
    while True:
        print("Second Now : %d"%time.localtime()[5])
        time.sleep(1)

def led_thread():
    while True:
        led(not led())
        time.sleep(0.5)
    
led = Pin(2, mode=Pin.OUT, value=0)

_thread.start_new_thread(second_thread,())
_thread.start_new_thread(led_thread,())


while True:
    print("主线程")
    time.sleep(2)