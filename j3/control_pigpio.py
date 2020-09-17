# -*-coding:utf-8-*-
#鱼镜J3控制程序，引脚10控制灯，11，12控制上下限位开关，13、15控制电机正反转，16上下舵机，18左右舵机

def init_gpio():

    #设置引脚模式,10灯，13、15电机
    # 10  11  12  13  15  16  18
    # 15  17  18  27  22  23  24   BCM
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
    pi.set_mode(18, pigpio.INPUT)

    #16、18PWM,16上下舵机，18左右舵机
    fPWM = 50
    
    #0.5---2.5ms ，中间为1.5
    pi.set_PWM_frequency(23,fPWM)
    pi.set_PWM_range(23,2000)
    for cycle in range(50,251,50):
    	pi.set_PWM_dutycycle(23,cycle)
    	time.sleep(0.01)
    for cycle in range(250,151,-50):
    	pi.set_PWM_dutycycle(23,cycle)
    	time.sleep(0.01)

    #0.5 --- 0.5+2/3= 7/6, 中间为0.5+1/3=5/6
    pi.set_PWM_frequency(24,fPWM)
    pi.set_PWM_range(24,2000)
    for cycle in range(50,701/6.0,50/3.0):
    	pi.set_PWM_dutycycle(23,cycle)
    	time.sleep(0.01)
    for cycle in range(700/6.0,501/6.0,-50/3.0):
    	pi.set_PWM_dutycycle(23,cycle)
    	time.sleep(0.01)
    #pi.set_PWM_dutycycle(24,500/6.0)
  
    pi.callback(18, pigpio.RISING_EDGE, up_close_callback)
    pi.callback(17, pigpio.RISING_EDGE, down_close_callback)
  
#16、18PWM,16上下舵机，18左右舵机
def steering_engine_control(channel,max_duty,per_angle):

    duty  = (50+max_duty)/2 + per_angle
    
    if (duty >= 50)&(duty <= max_duty) :
        pi.set_PWM_dutycycle(channel,duty)
        print( " duty =", duty)

    time.sleep(0.1)
    

def message(client, userdata, msg):
    global state,i,j
    state = str(msg.payload.decode("utf-8"))
    duty_up_down = 700/6.0
    duty_left_right = 250
    print(state)
    # #开关灯
    if state=="light_on":
        # pass
        pi.write(15,1)
        
    elif state=="light_off":
        pi.write(15, 0)
    #电机正转，摄像头上移
    elif state=="up":
        for c in range(5):
            pi.write(22, 0)
            pi.write(27,1)
            time.sleep(0.01)
        
    # 电机反转，摄像头下移
    elif state=="down":
        # print("I get it")
        for c in range(5):
            pi.write(27, 0)
            pi.write(22, 1)
            time.sleep(0.01)   
    elif state=="stop":
        pi.write(27, 0)
        pi.write(22, 0)
    elif state=="up_engine":
    	i+=1
    	if i>=-10 and i<=10:
            steering_engine_control(23,duty_up_down,9.9/3.0*i)
        else:
            i=10
            print("duty is too big,you should down_engine")

    elif state=="down_engine":
    	i-=1
    	if i>=-10 and i<=10:
            steering_engine_control(23,duty_up_down,9.9/3.0*i)
        else:
            i=-10
            print("duty is too small,you should up_engine")

    elif state=="left_engine":
    	j-=1
    	if j>=-15 and j<=15:
            steering_engine_control(24,duty_left_right,19.8/3.0*j)
        else:
            j=-15
            print("duty is too small,you should right_engine")

    elif state=="right_engine":
    	j+=1
    	if j>=-15 and j<=15:
            steering_engine_control(24,duty_left_right,19.8/3.0*j)
        else:
            j=15
            print("duty is too big,you should left_engine")


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
            if (state == "up"):
                print("up end")
                state = "stop"


# 下限位回调
def down_close_callback(channel,level,tick):
    global state
    time.sleep(0.001)
    if level==1:
        if pi.read(channel)>=0.5:
            pi.write(27, 0)
            pi.write(22, 0)
            
            if (state == "down"):
                print("down end")
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
            client.connect('192.168.50.89', 1883, 600)  #600 keepalive

            client.subscribe('fishmonitor/pi01', qos=1) #topic为test
            
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



