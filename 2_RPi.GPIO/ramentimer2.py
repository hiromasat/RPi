#coding: utf-8

import sys
import RPi.GPIO as GPIO
import time

"""
K04_Smart IoT System Business
Author:Hiromasa Tabuchi
Date:2019/4/8
Ver.1.1
"""

# GPIO setting
SW_PIN = 18       #SWITCH
LED_G_PIN = 23    #LED GREEN
BUZZER_PIN = 24   #BUZZER

# Parameter
timeToCount = 180    # 3min timer

countStatus = False    # False(OFF) True(ON)

def callBack(channel):
    # countStatus inversement
    global countStatus
    countStatus = not countStatus
    
    print("callBack")

# Initialize--GPIO setting
GPIO.setmode(GPIO.BCM)

# PIN Initial Setting
GPIO.setup(LED_G_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(SW_PIN, GPIO.FALLING, callback=callBack, bouncetime=300)

# Alert with LED and Buzzer
def alert():
    GPIO.output(LED_G_PIN, True)
    GPIO.output(BUZZER_PIN, True)
    time.sleep(0.5)
    GPIO.output(LED_G_PIN, False)
    GPIO.output(BUZZER_PIN, False)
    time.sleep(0.5)

# main
try:
    while True:
        countTime = 0

        # Default setting
        GPIO.output(LED_G_PIN, False)
        GPIO.output(BUZZER_PIN, False)
          
        while (countStatus == True):    #Wait for Button ON
            if countTime == 0:
                print("Start to count by ", timeToCount, "sec")

            print(countTime, "SW PIN State:", GPIO.input(SW_PIN), "countStatus:", countStatus)
            countTime  += 1

            if countTime > timeToCount:
                alert()
            else:
                time.sleep(1) # 1 sec wait
            
# Ctrl + C 
except KeyboardInterrupt:
    GPIO.OUTPUT(LED_G_PIN, False)
    GPIO.OUTPUT(BUZZER_PIN, False)
    GPIO.cleanup()
    sys.exit(0)