from umqtt.simple import MQTTClient
import time, network
import ntptime

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('D241', 'dd241241')
ntptime.NTP_DELTA = 3155644800
ntptime.host = 'ntp1.aliyun.com'
ntptime.settime()

# MQTT配置信息
mqtt_client_id = ''
mqtt_server_ip = ''
mqtt_server_port = ''
mqtt_topic = ''


# MQTT建立链接
def mqtt_init():
    mqtt_client = MQTTClient(mqtt_client_id, mqtt_server_ip, mqtt_server_port)
    mqtt_client.connect()
    return mqtt_client
 
# MQTT回调函数，收到服务器消息后会调用这个函数
def mqtt_sub(topic, msg): 
    print('收到服务器信息')
    print(topic, msg)

