#coding: utf-8
import sys
import wiringpi as pi
import time

"""
K04_Smart IoT System Business
Author:Hiromasa Tabuchi
Date:2019/4/8
Ver.0.9
"""

# GPIO setting
SW_PIN = 18       #SWITCH
LED_G_PIN = 23    #LED GREEN
BUZZER_PIN = 24   #BUZZER

# Parameter
timeToCount = 180 # 180sec timer
pi.wiringPiSetupGpio() # Intialize

# PIN Initial Setting
pi.pinMode(LED_G_PIN, pi.OUTPUT)
pi.pinMode(BUZZER_PIN, pi.OUTPUT)
pi.pinMode(SW_PIN, pi.INPUT)
pi.pullUpDnControl(SW_PIN, pi.PUD_UP)

# Alert with LED and Buzzer
def alert():
    pi.digitalWrite(LED_G_PIN, pi.HIGH)    # LED ON
    pi.digitalWrite(BUZZER_PIN, pi.LOW)   # BUZZER OFF(LOW) for test 
    time.sleep(0.5)
    pi.digitalWrite(LED_G_PIN, pi.LOW)    # LED ON
    pi.digitalWrite(BUZZER_PIN, pi.LOW)
    time.sleep(0.5)

def ramenTimer():
    try:
        while True:
            # Default setting
            pi.digitalWrite(BUZZER_PIN, pi.LOW)
            pi.digitalWrite(LED_G_PIN, pi.LOW)
            countTime = 0
            countStatus = 0    #(0:wait, 1:counting, 2:finished)
            
            if (pi.digitalRead(SW_PIN) == pi.LOW and countStatus == 0):    #Wait for Button ON
                print("Start to count by ", timeToCount, "sec")
                countStatus += 1 # 0->1 (wait->counting)
                
                while (countStatus == 1):
                    countTime  += 1
                    print(countTime, "SW PIN State:", pi.digitalRead(SW_PIN), "countStatus:", countStatus)
            
                    if countTime > timeToCount:
                        alert()
                        
                        if (pi.digitalRead(SW_PIN) == pi.LOW):
                            countStatus += 1 # 1->2 (alerting and break)
                            print("reset")
                            time.sleep(1)
                        
                    else:
                        time.sleep(1) # 1 sec wait 
    # Ctrl + C 
    except KeyboardInterrupt:
        pi.digitalWrite(LED_G_PIN, pi.LOW)
        pi.digitalWrite(BUZZER_PIN, pi.LOW)
        sys.exit(0)
    
if __name__ == '__main__':
    ramenTimer()