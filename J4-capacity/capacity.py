#!/usr/bin/python3
#coding=utf-8

import serial
import re
import time

class UPS2:
    def __init__(self,port):
        self.ser  = serial.Serial(port,9600,timeout =1)
        if self.ser.isOpen():
            print("open success")
        else:
            print("open failed")
        #self.ser.read(1)        
    
    def get_data(self,nums):
        try:
            while True:
                self.count = self.ser.inWaiting()
                #time.sleep(0.1) #延时读取
                #print(self.count)
                if self.count >0:
                    self.ser.flushInput()
                    time.sleep(1)
                    self.recv = self.ser.read(nums)
                    return self.recv
                else:
                    print("error")
                    # self.ser.flushInput()

                    # self.ser.close()
                    
                    # time.sleep(1)
                    # self.ser.open()
                    #self.ser.write('error'.encode("ascii"))
                    #time.sleep(0.5)
                    print(self.ser.read(1))
                    #print("ok")
                # self.ser.inWaiting()
                # time.sleep(0.1) #延时读取
                # #先读取一下，保证下次可以读取数据
                # #self.ser.read(nums)
                # self.recv = self.ser.read(nums)
                # print(self.recv)
                # print(len(self.recv))
                # print("---------------")
                # if len(self.recv)>=46:
                #     return self.recv

                           
                    
                #time.sleep(0.1)
        # 消除因 ctrl+c 程序中断后，下次无法读取的错误
        except KeyboardInterrupt:
            if serial != None:
                self.ser.close()
    

    def decode_uart(self,nums):
        self.uart_string = self.get_data(nums)
        self.data = self.uart_string.decode('ascii','ignore')
        print(self.data)
        self.pattern = r'BATCAP (.*?),' #以，结尾
        self.batcap = re.findall(self.pattern,self.data)
        self.pattern = r'Vout (.*?) '   #以空格结尾
        self.vout = re.findall(self.pattern,self.data)
        #print(self.batcap,self.vout)
        return self.batcap[0],self.vout[0]
    


'''
    def decode_uart(self,nums):
        self.uart_string = self.get_data(nums)
        if self.uart_string:
            self.data = self.uart_string.decode('ascii','ignore')
            #print(self.data)
            self.pattern = r'BATCAP (.*?),' #以，结尾
            self.batcap = re.findall(self.pattern,self.data)
            self.pattern = r'Vout (.*?) '   #以空格结尾
            self.vout = re.findall(self.pattern,self.data)
            #print(self.batcap,self.vout)
            return self.batcap[0],self.vout[0]
        else:
            print("null")
            return 0,0
'''

if __name__ == "__main__":
    print("This is UPS v2 class file")
    test = UPS2("/dev/ttyAMA0")
    # 每字段为46
    nums = 60
    #test.get_data(nums+1)
    '''
    i = 0
    while True:
        batcap,vout = test.decode_uart(nums)
        if i%10==0:
            #print("Battery Capacity: %d %%, out voltage: %d mV"%(batcap,vout))
            print("capacity: {0}%, out voltage: {1} mV".format(batcap,vout))
            print("-----------")
            with open("./log.txt","w+") as f:    #a为追加，不删除原来
                f.write("capacity: {0}%, out voltage: {1} mV".format(batcap,vout))
        i+=1
        #time.sleep(1)
    '''
    while True:
        batcap,vout = test.decode_uart(nums)
        #print("Battery Capacity: %d %%, out voltage: %d mV"%(batcap,vout))
        print("capacity: {0}%, out voltage: {1} mV".format(batcap,vout))
        print("-----------")
        with open("./log.txt","w+") as f:    #a为追加，不删除原来
            f.write("capacity: {0}%, out voltage: {1} mV".format(batcap,vout))
        time.sleep(300)
