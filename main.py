import network

def connect_wlan(ssid,key):    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to network 'D241'...")
        wlan.connect(ssid,key)
        while not wlan.isconnected():
            pass
    print("network config:",wlan.ifconfig())
    
connect_wlan("D241","dd241241")