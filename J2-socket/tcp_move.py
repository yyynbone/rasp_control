import socket
import threading
import RPi.GPIO as GPIO
import time
import logging
from logging import handlers
import os
import datetime

state = "stop"
flag_tcp = 0

def send_log_tcp(command):
    global flag_tcp, socket_tcp
    if(flag_tcp == 1):
        try:
            print(1)
            time_now = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
            command = time_now + ' ' + command
            print(command)
            socket_tcp.send(command.encode())
            #print(command)
        except Exception:
            flag_tcp = 0

def mkdir(path):
	folder = os.path.exists(path)
	if not folder:
		os.makedirs(path)

class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }

    def __init__(self,filename,level='info',when='D',backCount=1,fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(self.level_relations.get(level))
        sh = logging.StreamHandler()
        sh.setFormatter(format_str)
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')
        th.setFormatter(format_str)
        self.logger.addHandler(sh)
        self.logger.addHandler(th)
        
def turn_on_light():
    global log
    #print("li_on")
    log.logger.info('li_on')
    send_log_tcp('info li_on')
    GPIO.output(11, True)
    GPIO.output(12, True)

def turn_off_light():
    global log
    #print("li_off")
    log.logger.info('li_off')
    send_log_tcp('info li_off')
    GPIO.output(11, False)
    GPIO.output(12, False)

def up_too_close():
    return GPIO.input(10)

def down_too_close():
    return GPIO.input(13)

def move_up():
    global state,log
    #print("up")
    if up_too_close():
        stop_move()
        state = "stop"
        log.logger.warning('up_too_close')
        send_log_tcp('warning up_too_close')
        return
    else:
        GPIO.output(15,False)
        GPIO.output(16,True)
        state = "up"
        log.logger.info('up')
        send_log_tcp('info up')

def move_down():
    global state,log
    #print("down")
    if down_too_close():
        stop_move()
        state = "stop"
        log.logger.warning('down_too_close')
        send_log_tcp('warning down_too_close')
        return
    else:
        GPIO.output(15,True)
        GPIO.output(16,False)
        state = "down"
        log.logger.info('down')
        send_log_tcp('info down')

def stop_move():
    global state,log
    GPIO.output(15 , False)
    GPIO.output(16 , False)
    state = "stop"
    log.logger.info('stop')
    send_log_tcp('info stop')

def up_close_callback(self):
    global state,log
    #print("up_stop")
    log.logger.warning('up_close')
    send_log_tcp('warning up_close')

    time.sleep(0.001)
    if up_too_close():
        if(state == "up"):
            stop_move()
    
def down_close_callback(self):
    global state,log
    #print("down_stop")
    log.logger.warning('down_close')
    send_log_tcp('warning down_close')
    time.sleep(0.001)
    if down_too_close():
        if(state == "down"):
            stop_move()

def init_GPIO():
    # GPIO setting
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    ## light control   ture,true ->on false ,false -> off
    GPIO.setup(11, GPIO.OUT)#,initial=GPIO.LOW)
    GPIO.output(11, False)
    GPIO.setup(12, GPIO.OUT)#,initial=GPIO.LOW)
    GPIO.output(12, False)
    ## up and down : true,true -> up  false,false -> down  true ,false ->stop
    GPIO.setup(15, GPIO.OUT)#,initial=GPIO.HIGH)
    GPIO.output(15, False)
    GPIO.setup(16, GPIO.OUT)#,initial=GPIO.LOW)
    GPIO.output(16, False)
    
    GPIO.setup(10,GPIO.IN)#,pull_up_down=GPIO.PUD_DOWN)#,initial=GPIO.LOW)  # up_too_close
    GPIO.setup(13,GPIO.IN)#,pull_up_down=GPIO.PUD_DOWN)#,initial=GPIO.LOW)  # down_too_close
    GPIO.add_event_detect(10, GPIO.RISING, callback=up_close_callback)
    GPIO.add_event_detect(13, GPIO.RISING, callback=down_close_callback)

def deal_client(newSocket, addr):
    global flag_tcp, socket_tcp
    socket_tcp = newSocket
    flag_tcp = 1
    while True:
        data = newSocket.recv(2)
        print("%s %s" % (str(addr), data))
        if data == b"up":
            move_up()
            print("up")
        elif data == b'dn':
            move_down()
            print("down")
        elif data == b'sp':
            stop_move()
            print("stop")
        elif data == b'on':
            turn_on_light()
            print("on")
        elif data == b'of':
            turn_off_light()
            print("off")
        else:
            print("client [%s] exit" % str(addr))
            newSocket.close()
            break

if __name__ == '__main__':
    init_GPIO()
    mkdir("log")
    log = Logger('log/all.log',level='debug')
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
        client = threading.Thread(target=deal_client, args=(newSocket, addr))
        client.start()

