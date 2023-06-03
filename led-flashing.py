from machine import Pin
from machine import Timer

p2 = Pin(2,Pin.OUT)
print(p2.value())

tim0 = Timer(0)
tim0.init(period=20, mode=Timer.PERIODIC, callback=lambda t:p2.value(not p2.value()))

