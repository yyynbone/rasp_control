# -*-coding:utf-8-*-
#鱼镜J3控制程序，引脚15，16控制上下限位开关，11,12控制电机正反转
import time
import paho.mqtt.client as mqtt

def init_gpio():
    #初始化设置
    GPIO.setmode(GPIO.BOARD)

    #设置引脚模式,11、12电机
    channel=[11,12]
    GPIO.setup(channel,GPIO.OUT,initial=0)

    #15、16限位
    GPIO.setup([15, 16], GPIO.IN) 
    GPIO.add_event_detect(15, GPIO.RISING, callback = callback)
    GPIO.add_event_detect(16, GPIO.RISING, callback = callback)

def message(client, userdata, msg):
    global state 
    state = str(msg.payload.decode("utf-8"))
    #duty_up_down = 2.5 + 10/3.0
    #duty_left_right = 12.5
    print(state)
    电机正转，摄像头上移
    if state=="up":
        for i in range(3):
            GPIO.output(11, 0)
            GPIO.output(12,1)
            time.sleep(0.01)
    # 电机反转，摄像头下移
    elif state=="down":
        # print("I get it")
        for i in range(3):
            GPIO.output(12, 0)
            GPIO.output(11, 1)
            time.sleep(0.01)
    elif state=="stop":
        GPIO.output([11,12], 0)
def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_disconnect(client, userdata, flags, rc):
    print("disConnected with result code: " + str(rc))

#限位回调
def callback(channel):
    global state 
    time.sleep(0.001)
    if GPIO.input(channel):
        GPIO.output([11, 12], 0)
        print("end")
        state = "stop"

#连接mqtt,订阅消息
def client_connected():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = message
    client.on_disconnect = on_disconnect
    while True:
        time.sleep(1)
        try:
            client.connect('192.168.50.248', 1883, 600)  #600 keepalive

            client.subscribe('fishmonitor/pi01', qos=1) #topic为test
            
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

    state = "stop"
    init_gpio()
    client_connected()
    GPIO.cleanup()



