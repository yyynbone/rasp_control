# -*-coding:utf-8-*-
#步进电机控制程序，引脚22pul，21drive，16ena
import paho.mqtt.client as mqtt
import time
import multiprocessing as mp

def init_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    #设置引脚模式
    channel=[21,22]
    GPIO.setup(channel,GPIO.OUT,initial=0)
    

def message(client, userdata, msg):
    global queue
    state = str(msg.payload.decode("utf-8"))
    print(state)
    flag = 0
    #  first drive then pul
    if state=="forward":
    	GPIO.output(21,1)
    	time.sleep(0.1)
        flag = 1
    	

    elif state=="reverse":
        GPIO.output(21, 0)
        time.sleep(0.1)
        flag = 1 
        
    #电机正转，摄像头上移
    elif state=="stop":
        GPIO.output(22, 1)
        flag = 0
    queue.put(flag)

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

def reader(queue):
    flag = queue.get()
    while True:
        while flag:
            # GPIO.output(22,0)
            # time.sleep(0.01)
            # GPIO.output(22,1)
            print("not stop")



if __name__=="__main__":
    try:
        import RPi.GPIO as GPIO
    except ImportError:
        print("error import RPi.GPIO")

    init_gpio()
    queue = mp.Queue()
    pulse = mp.Process(target=reader,args=((queue),))
    pulse.daemon = True
    pulse.start()
    client_connected()
    pulse.join()






