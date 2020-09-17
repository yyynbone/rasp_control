# -*-coding:utf-8-*-
#步进电机控制程序，引脚22pul，21drive，16ena
import paho.mqtt.client as mqtt
import time
import threading

def init_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    #设置引脚模式
    channel=[21,22]
    GPIO.setup(channel,GPIO.OUT,initial=0)
    

def message(client, userdata, msg):
    state = str(msg.payload.decode("utf-8"))
    state = state.split("/")
    print(state)
    dire = state[0]
    try:
        count = int(state[1])
    except:
        count = 10
    print(count)
    #  first drive then pul
    if dire=="stop":
        pass
    else:
        if dire=="forward":
            GPIO.output(21,1)
            time.sleep(0.1)
        elif dire=="reverse":
            GPIO.output(21, 0)
            time.sleep(0.1)
        for i in range(count):
            GPIO.output(22,0)
            time.sleep(0.001)
            GPIO.output(22,1)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_disconnect(client, userdata, flags, rc):
    print("disConnected with result code: " + str(rc))

#连接mqtt,订阅消息
def client_connected():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = message
    client.on_disconnect = on_disconnect
    while True:
        time.sleep(1)
        try:
            client.connect('47.100.92.173', 11883, 600)  #600 keepalive

            client.subscribe('bujing/pi05', qos=1) #topic为test

            client.loop_forever()  # keeplive
            print("success connected")
            exit()
        except Exception:
            print("timeout,try again...")


if __name__=="__main__":
    try:
        import RPi.GPIO as GPIO
    except ImportError:
        print("error import RPi.GPIO")

    init_gpio()
    client_connected()
    GPIO.cleanup()



