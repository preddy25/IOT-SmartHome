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
counter = 0
peoplecount = 0

while (1):
    presence = grovepi.digitalRead(pir_sensor)
    if (presence):
        #print ("People count %s , counter %d")%(peoplecount, counter)
        peoplecount += 1
        print(peoplecount, counter)
        presence = 0
        time.sleep(1.5)
    time.sleep(1)
    counter += 1
    if (counter == 60) and (peoplecount <= 10): # minimum interval (in sec.) before each sending to Ubidots server (here 5min)
        print("Resetted count :%d. %d seconds ." % (peoplecount, counter))
        #print("Setting " + attribute + " to " + value + "...")
        #people.save_value({'value': peoplecount})
        counter = 0
        peoplecount = 0

