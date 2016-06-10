import RPi.GPIO as GPIO
import time
import grovepi

#from ubidots import ApiClient

GPIO.setmode(GPIO.BCM)  # use BCM GPIO references
GPIO_PIR = 4  # define GPIO to use on rpi
print ( "Capture is running (CTRL-C to exit)")
# GPIO.setup(GPIO_PIR, GPIO.IN)  # set pin as input

# try:
#     api = ApiClient("9d7a13d955497b9c3a5c2670eeed73979aXXXXXX")  # put your own apikey (unique key)
#     people = api.get_variable("54a7f0357625426a0f13XXXX")  # pur your own variable's id (one per device)
# except:
#     print
#     "cant connect. please verify your GPIO connector"

pir_sensor = 5
timecounter = 0
motioncounter = 0

while (1):
    presence = grovepi.digitalRead(pir_sensor)
    if (presence):
        #print ("People count %s , counter %d")%(motioncount, counter)
        motioncount += 1
        print(motioncount, timecounter)
        presence = 0
        time.sleep(1.5)
    time.sleep(1)
    timecounter += 1
    if (timecounter == 60) and (motioncount <= 10): # minimum interval (in sec.) before each sending to Ubidots server (here 5min)
        print("Resetted: count :%d. %d seconds ." % (motioncount, timecounter))
        #print("Setting " + attribute + " to " + value + "...")
        #people.save_value({'value': motioncount})
        counter = 0
        motioncount = 0
