# -*-coding:utf-8-*-
#鱼镜J4控制程序，引脚11控制灯，10，13控制上下限位开关，15,16控制电机正反转
import time
import threading
import socket
import os

def init_gpio():
    
    #初始化设置
    GPIO.setmode(GPIO.BOARD)

    #设置引脚模式,11灯，15,16电机
    channel=[11,15,16]
    GPIO.setup(channel,GPIO.OUT,initial=0)

    #11、12限位
    GPIO.setup([10, 13], GPIO.IN)
 
    GPIO.add_event_detect(10, GPIO.RISING, callback = up_close_callback)
    GPIO.add_event_detect(13, GPIO.RISING, callback = down_close_callback)

def message(newSocket,addr):
    global flag_tcp, socket_tcp,state
    socket_tcp = newSocket
    flag_tcp = 1
    while True:
        data =  newSocket.recv(2)
        state = str(data.decode("utf-8"))
        print(state)
        # #开关灯
        if state=="on":
            # pass
            GPIO.output(11,1)
        elif state=="of":
            GPIO.output(11, 0)
        #电机正转，摄像头上移
        elif state=="up":
            GPIO.output(15, 0)
            GPIO.output(16,1)
        # 电机反转，摄像头下移
        elif state=="dn":
            GPIO.output(15, 1)
            GPIO.output(16, 0)
        elif state=="sp":
            GPIO.output([15,16], 0)
        else:
            print("client [%s] exit" % str(addr))
            newSocket.close()
            break

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
def socket_connected():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind(("", 7000))
    server.listen(10)
    print("server is running!")
    while True:
        newSocket, addr = server.accept()
        str_h = 'hello'
        newSocket.send(str_h.encode())
        print("client [%s] is connected!" % str(addr))
        client = threading.Thread(target=message, args=(newSocket, addr))
        client.start()


if __name__=="__main__":
    try:
        import RPi.GPIO as GPIO
    except ImportError:
        print("error import RPi.GPIO")
    state = "stop"
    init_gpio()
    socket_connected()
    GPIO.cleanup()



