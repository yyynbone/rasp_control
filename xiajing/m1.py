import paho.mqtt.client as mqtt
import time 
def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
#client.connect('47.100.92.173', 11883, 600)
client.connect('192.18.50.89', 1883, 600)
order= "down"
client.publish('prawnmonitor/pi02',order, qos=1)
print(order)
time.sleep(10)

client.disconnect()