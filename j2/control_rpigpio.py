# -*-coding:utf-8-*-
#鱼镜J4控制程序，引脚11控制灯，10，13控制上下限位开关，15,16控制电机正反转
import time
import paho.mqtt.client as mqtt

def init_gpio():
    
    #初始化设置
    GPIO.setmode(GPIO.BOARD)

    #设置引脚模式,11灯，15,16电机
    channel=[11,15,16]
    GPIO.setup(channel,GPIO.OUT,initial=0)

    #11、12限位
    GPIO.setup([10, 13], GPIO.IN)
 
    GPIO.add_event_detect(13, GPIO.RISING, callback = up_close_callback)
    GPIO.add_event_detect(10, GPIO.RISING, callback = down_close_callback)

def message(client, userdata, msg):
    global state
    state = str(msg.payload.decode("utf-8"))
    print(state)
    # #开关灯
    if state=="light_on":
        # pass
        GPIO.output(11,1)
    elif state=="light_off":
        GPIO.output(11, 0)
    #电机正转，摄像头上移
    elif state=="up":
        GPIO.output(15, 0)
        GPIO.output(16,1)
    # 电机反转，摄像头下移
    elif state=="down":
        GPIO.output(15, 1)
        GPIO.output(16, 0)
    elif state=="stop":
        GPIO.output([15,16], 0)
    
def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_disconnect(client, userdata, flags, rc):
    print("disConnected with result code: " + str(rc))

#上限位回调
def up_close_callback(channel):
    global state 
    time.sleep(0.001)
    if GPIO.input(channel):
        GPIO.output([15, 16], 0)
        if (state == "up"):
            print("up end")


# 下限位回调
def down_close_callback(channel):
    global state 
    time.sleep(0.001)
    if GPIO.input(channel):
        GPIO.output([15, 16], 0)
        if (state == "down"):
            print("down end")

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

            client.subscribe('E21103157', qos=0)
            
            client.loop_forever()  # keeplive
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



