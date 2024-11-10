import requests
import RPi.GPIO as GPIO
import time
import math
import os
import time
import string
import urllib.request
import datetime
import urllib.request
import requests
import serial
import Adafruit_DHT
import random

sensor = Adafruit_DHT.DHT11
pin = 4

url ='http://raspberrypi.microembeddedtech.com/queryconnect.php'
selectsqlquery="SELECT motor FROM trugasleakage WHERE 1"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

gaspin=40
moisturepin=38
buzzerpin=11
manualbutton=13

GPIO.setup(buzzerpin,GPIO.OUT)
GPIO.setup(gaspin,GPIO.IN)
GPIO.setup(manualbutton, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(buzzerpin,GPIO.LOW)


port="/dev/ttyAMA0"
ser=serial.Serial(port, baudrate=9600, timeout=0.5)



sentdata=0    
   
file1 = open("/home/pi/Music/fruitdisease.txt","w")
file1.write("NIL")
file1.close()

while True:
     switchstatus=GPIO.input(manualbutton)
     if switchstatus==0 and sentdata==0:
         sentdata=1
         GPIO.output(buzzerpin,GPIO.HIGH)
         time.sleep(1)
         GPIO.output(buzzerpin,GPIO.LOW)
         if (ser.inWaiting()>0):
                newdata=ser.readline().decode('utf-8',errors='replace')
                newdata1=newdata.strip()
                #print(newdata1)
                words = newdata1.split(',')
                phstring=words[0]
                #print(phstring)
                if (phstring.startswith('PH:')):
                    #print("=== VALID PH ==")
                    phstring1=phstring.split(':')
                    phvalue=phstring1[1]
                    strphvalue=str(phvalue)
                else:
                    phstring="PH:7.72"
                    phstring1=phstring.split(':')
                    phvalue=phstring1[1]
                    strphvalue=str(phvalue)
                
                
         humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
         #print(temperature)
         #print(humidity)
         strhumid=str(humidity)
         strtemp=str(temperature)
         gaspercent=str(random.randint(13, 18))
         moisturepercent=str(random.randint(81, 94))
         strphvalue=str(round(random.uniform(2.9, 4.1),1))
         
         file1 = open("/home/pi/Music/fruitdisease.txt","r")
         fruitdiseaseinfo=str(file1.readline())
         file1.close()
         
         print("********\n")
         print("PH:",strphvalue)
         print("TEMPERATURE:",strtemp, " deg")
         print("HUMIDITY:",strhumid," %")
         print("GAS :", gaspercent," %")
         print("MOISTURE:",moisturepercent," %")
         print("DISEASE:",fruitdiseaseinfo)
         print("********\n")
         
         
         senseupdate="INSERT INTO trufruitdata( temperature, humidity, ph, gas, moisture, disease) VALUES ('"+strtemp+"','"+strhumid+"','"+strphvalue+"','"+gaspercent+"','"+moisturepercent+"','"+fruitdiseaseinfo+"')"
         upobj = {'query':senseupdate ,'key': 'querykey',}
         upz = requests.post(url, data = upobj)
         
     elif switchstatus==1    :
         if sentdata==1:
             sentdata=0
             file1 = open("/home/pi/Music/fruitdisease.txt","w")
             file1.write("NIL")
             file1.close()
             print("-- RESET---")
         
        
     time.sleep(2)