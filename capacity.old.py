#!/usr/bin/python3

import serial
import re
import RPi.GPIO as GPIO
import os,sys
import time

class UPS2:
    def __init__(self,port):
        self.ser  = serial.Serial(port,9600)        
        
    def get_data(self,nums):
        while True:
            self.count = self.ser.inWaiting()
            
            if self.count !=0:
                self.recv = self.ser.read(nums)
                return self.recv
    
    def decode_uart(self):
        self.uart_string = self.get_data(100)

        self.data = self.uart_string.decode('ascii','ignore')
        self.pattern = r'BATCAP (.*?),'
        self.batcap = re.findall(self.pattern,self.data)
        return self.batcap[0]
    

if __name__ == "__main__":
    print("This is UPS v2 class file")
    test = UPS2("/dev/ttyAMA0")
    i = 1
    while True:       
        batcap = test.decode_uart()
        print("Battery Capacity: "+batcap+"%")
        print("-----------")
        time.sleep(5)
        
        i = i+1
        
        if i == 1000:
            i = 1
    
   
        
        
    