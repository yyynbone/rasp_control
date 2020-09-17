# -*-coding:utf-8-*-
#鱼镜J4控制程序，引脚10控制灯，11，12控制上下限位开关，13、15控制电机正反转，16上下舵机，18左右舵机
import time
import paho.mqtt.client as mqtt

def init_gpio():
    global pwm_up_down,pwm_left_right,fPWM
    #初始化设置
    GPIO.setmode(GPIO.BOARD)

    #设置引脚模式,10灯，13、15电机
    channel=[10,13,15,16,18]
    GPIO.setup(channel,GPIO.OUT,initial=0)

    #11、12限位
    GPIO.setup([11, 12], GPIO.IN)
'''
    #16、18PWM,16上下舵机，18左右舵机
    fPWM = 50
    
    pwm_up_down = GPIO.PWM(16,fPWM)
    pwm_up_down.start(50/20.0)

    pwm_left_right = GPIO.PWM(18,fPWM)
    pwm_left_right.start(50/20.0)
''' 
    GPIO.add_event_detect(12, GPIO.RISING, callback = up_close_callback)
    GPIO.add_event_detect(11, GPIO.RISING, callback = down_close_callback)
'''    
#16、18PWM,16上下舵机，18左右舵机
def steering_engine_control(pwm,max_duty,per_angle):

    duty  = 2.5 + (10.0 / 360.0) * per_angle #2.5 12.5
    
    if (duty >= 2.5)&(duty <= max_duty) :
        pwm.ChangeDutyCycle(duty)
        print( " duty =", duty)
    time.sleep(0.1)
    
'''
def message(client, userdata, msg):
    global state,i,j
    state = str(msg.payload.decode("utf-8"))
    duty_up_down = 2.5 + 10/3.0
    duty_left_right = 12.5
    print(state)
    # #开关灯
    if state=="light_on":
        # pass
        GPIO.output(10,1)
    elif state=="light_off":
        GPIO.output(10, 0)
    #电机正转，摄像头上移
    elif state=="up":
        GPIO.output(15, 0)
        GPIO.output(13,1)
    # 电机反转，摄像头下移
    elif state=="down":
        # print("I get it")
        GPIO.output(13, 0)
        GPIO.output(15, 1)
    elif state=="stop":
        GPIO.output([13,15], 0)
    '''
    elif state=="up_engine":
    	i+=1
    	if i>=0 and i<=9:
        	steering_engine_control(pwm_up_down,duty_up_down,40/3.0*i)
        else:
        	i=9
        	print("duty is too big,you should down_engine")

    elif state=="down_engine":
    	i-=1
    	if i>=0 and i<=9:
        	steering_engine_control(pwm_up_down,duty_up_down,40/3.0*i)
        else:
        	i=0
        	print("duty is too small,you should up_engine")

    elif state=="left_engine":
    	j-=1
    	if j>=0 and j<=9:
        	steering_engine_control(pwm_left_right,duty_left_right,38*j)
        else:
        	j=0
        	print("duty is too small,you should right_engine")

    elif state=="right_engine":
    	j+=1
    	if j>=0 and j<=9:
        	steering_engine_control(pwm_left_right,duty_left_right,38*j)
        else:
        	j=9
        	print("duty is too big,you should left_engine")


    #print(GPIO.input([10,11,12,13,15]))
'''
def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_disconnect(client, userdata, flags, rc):
    print("disConnected with result code: " + str(rc))

#上限位回调
def up_close_callback(channel):
    global state 
    time.sleep(0.001)
    if GPIO.input(channel):
        GPIO.output([13, 15], 0)
        if (state == "up"):
            print("up end")


# 下限位回调
def down_close_callback(channel):
    global state 
    time.sleep(0.001)
    if GPIO.input(channel):
        GPIO.output([13, 15], 0)
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
            client.connect('192.168.50.89', 1883, 600)  #600 keepalive

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
    i=0
    j=0
    client_connected()
    GPIO.cleanup()



