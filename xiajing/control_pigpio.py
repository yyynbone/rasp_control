# -*-coding:utf-8-*-
#虾镜控制程序，引脚10控制灯，11控制上下限位开关，13、15控制电机正反转，15上下电调，18左右电调，50Hz时，电调范围1-2ms,占空比5-10（%）

def init_gpio():

    #设置引脚模式,10灯，13、15电机
    # 10  11  #12  13  15  16  18
    # 15  17  #18  27  22  23  24   BCM
    pi.set_mode(15,pigpio.OUTPUT)
    pi.write(15,0)
    pi.set_mode(27,pigpio.OUTPUT)
    pi.write(27,0)
    pi.set_mode(22,pigpio.OUTPUT)
    pi.write(22,0)
    pi.set_mode(23,pigpio.OUTPUT)
    pi.write(23,0)
    pi.set_mode(24,pigpio.OUTPUT)
    pi.write(24,0)
    

    #11、12限位
    pi.set_mode(17, pigpio.INPUT)
    # pi.set_mode(18, pigpio.INPUT)

    #16、18PWM,16上下舵机，18左右舵机
    fPWM = 50
    
    pi.set_PWM_frequency(23,fPWM)
    pi.set_PWM_range(23,2000)
    pi.set_PWM_dutycycle(23,150)
    time.sleep(0.5)
    pi.set_PWM_frequency(24,fPWM)
    pi.set_PWM_range(24,2000)
    pi.set_PWM_dutycycle(24,150)
    
    pi.callback(17, pigpio.RISING_EDGE, up_close_callback)


    
#16、18PWM,16上下舵机，18左右舵机，duty 为频宽范围time
def steering_engine_control(channel,per_angle):

    duty  = 150 + 10 * per_angle 
    
    if (duty >= 100)&(duty <= 200) :
        pi.set_PWM_dutycycle(channel,duty)
        print( " duty =", duty)

    time.sleep(0.1)
    

def message(client, userdata, msg):
    global state,i,j
    state = str(msg.payload.decode("utf-8"))
    
    print(state)
    # #开关灯
    if state=="light_on":
        # pass
        pi.write(15,1)
        #print(pi.read(15))
    elif state=="light_off":
        pi.write(15, 0)
    #电机正转，摄像头上移
    elif state=="up":
        pi.write(22, 0)
        pi.write(27,1)
        
    # 电机反转，摄像头下移
    elif state=="down":
        pi.write(27, 0)
        pi.write(22, 1)
    elif state=="stop":
        pi.write(27, 0)
        pi.write(22, 0)
    elif state=="forward":
        while i<=1:
            i+=1
            steering_engine_control(23,i)
            time.sleep(0.05)
        print("max forword")

    elif state=="back":
        while i>=-4:
            i-=1
            steering_engine_control(23,i)
            time.sleep(0.05)
        print("max back")

    elif state=="left":
        while j>=-4:
            j-=1
            steering_engine_control(24,j)
            time.sleep(0.05)
        print("max left")

    elif state=="right":
        while j<=1:
    	    j+=1
            steering_engine_control(24,j)
            time.sleep(0.05)
        print("max right")
    elif state=="stop_all":
        i=0
        j=0
        steering_engine_control(23,i)
        steering_engine_control(24,j)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_disconnect(client, userdata, flags, rc):
    print("disConnected with result code: " + str(rc))

#上限位回调,level 0-2  
#0: change to low
#1: change to high
#2: no level change

def up_close_callback(channel,level,tick):
    global state
    time.sleep(0.001)
    if level==1:
        if pi.read(channel)>=0.5:
            pi.write(27, 0)
            pi.write(22, 0)
            print("the camera should fall down")



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
            client.subscribe('D87938874',qos=1)
            client.loop_forever()  # keeplive
            print("success connected")
            exit()
        except Exception:
            print("timeout,try again...")


if __name__=="__main__":
    import time
    import paho.mqtt.client as mqtt
    import os
    
    server = os.system("ps -e | grep pigpiod |awk '{print $1}'|xargs echo")
    if server:
        print("pigpiod exited")
	pass
    else:
        os.system('sudo pigpiod')
        time.sleep(0.1)
        
    try:
        import pigpio
    except ImportError:
    	print("error import pigpio")

    state = "stop"
    pi = pigpio.pi()
    init_gpio()
    i=0
    j=0
    client_connected()
    pi.stop()



