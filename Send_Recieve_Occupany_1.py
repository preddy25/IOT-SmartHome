
#!/usr/bin/env python3

# Send Grove sensor data periodically to AWS IoT and process actuation commands received.

import time
import datetime
import ssl
import json
import paho.mqtt.client as mqtt
import grovepi
# Added
# import pigpio

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
# Set the pin numbering to the BCM (same as GPIO) numbering format.
GPIO.setmode(GPIO.BCM)
# GPIO.setmode(GPIO.BOARD)
relay_1 = 23
relay_2 = 24
GPIO.setup(relay_1, GPIO.OUT)
GPIO.setup(relay_2, GPIO.OUT)
GPIO.output(relay_1, 1)
GPIO.output(relay_2, 1)

# read status of pin/port and assign to variable i
# i = GPIO.input(port_or_pin)


# TODO: Change this to the name of our Raspberry Pi, also known as our "Thing Name"
deviceName = "g41pi"

# Public certificate of our Raspberry Pi, as provided by AWS IoT.
deviceCertificate = "tp-iot-certificate.pem.crt"
# Private key of our Raspberry Pi, as provided by AWS IoT.
devicePrivateKey = "tp-iot-private.pem.key"
# Root certificate to authenticate AWS IoT when we connect to their server.
awsCert = "aws-iot-rootCA.crt"

isConnected = True

# Define Grove ports -
# Assume we connected the Grove Light Sensor to analog port A0,
# Digital Humidity/Temperature Sensor (DHT11) to digital port D2,
# Sound Sensor to A2, Grove LED to digital port D4.
# If you are using the Grove Analog Temperature Sensor, connect it to analog port A1.

#light_sensor = 0
#sound_sensor = 2
dht_sensor = 4
pir_sensor = 5
timecounter = 0
motioncount = 0

#led = 4
#temp_sensor = 1

# Configure vairous Grove Ports for In or Output

#grovepi.pinMode(led, "OUTPUT")
#grovepi.pinMode(light_sensor, "INPUT")
grovepi.pinMode(pir_sensor, "INPUT")
#grovepi.pinMode(sound_sensor, "INPUT")
#grovepi.pinMode(light_switch, "INPUT")



# This is the main logic of the program.  We connect to AWS IoT via MQTT, send sensor data periodically to AWS IoT,
# and handle any actuation commands received from AWS IoT.
def main():
    global isConnected
    # Create an MQTT client for connecting to AWS IoT via MQTT.
    client = mqtt.Client(deviceName + "_sr")  # Client ID must be unique because AWS will disconnect any duplicates.
    client.on_connect = on_connect  # When connected, call on_connect.
    client.on_message = on_message  # When message received, call on_message.
    client.on_log = on_log  # When logging debug messages, call on_log.

    # Set the certificates and private key for connecting to AWS IoT.  TLS 1.2 is mandatory for AWS IoT and is supported
    # only in Python 3.4 and later, compiled with OpenSSL 1.0.1 and later.
    client.tls_set(awsCert, deviceCertificate, devicePrivateKey, ssl.CERT_REQUIRED, ssl.PROTOCOL_TLSv1_2)

    # Connect to AWS IoT server.  Use AWS command line "aws iot describe-endpoint" to get the address.
    print("Connecting to AWS IoT...")
    client.connect("A1P01IYM2DOZA0.iot.us-west-2.amazonaws.com", 8883, 60)

    # Start a background thread to process the MQTT network commands concurrently, including auto-reconnection.
    client.loop_start()

   # Loop forever.
    while True:
        try:
            # If we are not connected yet to AWS IoT, wait 1 second and try again.
            if not isConnected:
                time.sleep(1)
                continue

            # Read Grove sensor values. Prepare our sensor data in JSON format.
            payload = {
                "state": {
                    "reported": {
                        # Uncomment the next line if you're using the Grove Analog Temperature Sensor.
                        # "temperature": round(grovepi.temp(temp_sensor, '1.1'), 1),
                        # Comment out the next 2 lines if you're using the Grove Analog Temperature Sensor.
                        "temperature": grovepi.dht(dht_sensor, 0)[0],  # The first 0 means that the DHT module is DHT11.
                        "humidity": grovepi.dht(dht_sensor, 0)[1],
#                        "light_level": grovepi.analogRead(light_sensor),
#                       "sound_level": grovepi.analogRead(sound_sensor),
#                        "pir_status": grovepi.digitalRead(pir_sensor),

			            "pir_status": 'Occupied' if motioncount >= 10 else 'Unoccupied',
                        while (1):
                            try:
                                presence = grovepi.digitalRead(pir_sensor):
                                #if (presence):
                                # print ("People count %s , counter %d")%(peoplecount, counter)
                                motioncount += 1
                                print(motioncount, timecounter)
                                presence = 0
                                time.sleep(1.5)
                                time.sleep(1)
                                timecounter += 1
                                if (timecounter == 60) and (motioncount <= 10):  #minimum interval (in sec.) (here 1min)
                                    print("No one Deteched.Resetting count :%d. %d seconds ." % (motioncount, timecounter))
                                # print("Setting " + attribute + " to " + value + "...")
                                # people.save_value({'value': peoplecount})
                                timecounter = 0
                                motioncount = 0,

                        "timestamp": datetime.datetime.now().isoformat()
                    }
                }
            }
            print("Sending sensor data to AWS IoT...\n" +
                  json.dumps(payload, indent=4, separators=(',', ': ')))

            # Publish our sensor data to AWS IoT via the MQTT topic, also known as updating our "Thing Shadow".
            client.publish("$aws/things/" + deviceName + "/shadow/update", json.dumps(payload))
            print("Sent to AWS IoT")

            # Wait 30 seconds before sending the next set of sensor data.
            time.sleep(10)

        except KeyboardInterrupt:
            break
        except IOError:
            print("Error")


# This is called when we are connected to AWS IoT via MQTT.
# We subscribe for notifications of desired state updates.
def on_connect(client, userdata, flags, rc):
    global isConnected
    isConnected = True
    print("Connected to AWS IoT")
    # Subscribe to our MQTT topic so that we will receive notifications of updates.
    topic = "$aws/things/" + deviceName + "/shadow/update/accepted"
    print("Subscribing to MQTT topic " + topic)
    client.subscribe(topic)


# This is called when we receive a subscription notification from AWS IoT.
# If this is an actuation command, we execute it.
def on_message(client, userdata, msg):
    # Convert the JSON payload to a Python dictionary.
    # The payload is in binary format so we need to decode as UTF-8.
    payload2 = json.loads(msg.payload.decode("utf-8"))
    print("Received message, topic: " + msg.topic + ", payload:\n" +
          json.dumps(payload2, indent=4, separators=(',', ': ')))

    # If there is a desired state in this message, then we actuate, e.g. if we see "led=on", we switch on the LED.
    if payload2.get("state") is not None and payload2["state"].get("desired") is not None:
        # Get the desired state and loop through all attributes inside.
        desired_state = payload2["state"]["desired"]
        for attribute in desired_state:
            # We handle the attribute and desired value by actuating.
            value = desired_state.get(attribute)
            actuate(client, attribute, value)


# Control my actuators based on the specified attribute and value, e.g. "led=on" will switch on my LED.
def actuate(client, attribute, value):
    if attribute == "timestamp":
        # Ignore the timestamp attribute, it's only for info.
        return
    print("Setting " + attribute + " to " + value + "...")
    if attribute == "led":
        # We actuate the LED for "on", "off" or "flash1".
        if value == "on":
            # Switch on LED.
            grovepi.digitalWrite(led, 1)
            send_reported_state(client, "led", "on")
            return
        elif value == "off":
            # Switch off LED.
            grovepi.digitalWrite(led, 0)
            send_reported_state(client, "led", "off")
            return
        elif value == "flash1":
            # Switch on LED, wait 1 second, switch it off.
            grovepi.digitalWrite(led, 1)
            send_reported_state(client, "led", "on")
            time.sleep(1)

            grovepi.digitalWrite(led, 0)
            send_reported_state(client, "led", "off")
            time.sleep(1)
            return

            # added
    if attribute == "relay_1":
        # We actuate the Relays for "on", "off"
        if value == "on":
            # Switch on relay_1
            # 0 or False to On a N.O relay
            GPIO.output(relay_1, 0)
            send_reported_state(client, "relay_1", "on")
            return
        elif value == "off":
            # Switch off relay.
            GPIO.output(relay_1, 1)
            send_reported_state(client, "relay_1", "off")
            return

    if attribute == "relay_2":
            # We actuate the LED for "on", "off"
        if value == "on":
            # Switch on relay_2
            GPIO.output(relay_2, 0)
            send_reported_state(client, "relay_2", "on")
            return
        elif value == "off":
            # Switch off relay_2.
            GPIO.output(relay_2, 1)
            send_reported_state(client, "relay_2", "off")
            return


            # Show an error if attribute or value are incorrect.
    print("Error: Don't know how to set " + attribute + " to " + value)


# Send the reported state of our actuator tp AWS IoT after it has been triggered, e.g. "led": "on".
def send_reported_state(client, attribute, value):
    # Prepare our sensor data in JSON format.
    payload = {
        "state": {
            "reported": {
                attribute: value,
                "timestamp": datetime.datetime.now().isoformat()
            }
        }
    }
    print("Sending sensor data to AWS IoT...\n" +
          json.dumps(payload, indent=4, separators=(',', ': ')))

    # Publish our sensor data to AWS IoT via the MQTT topic, also known as updating our "Thing Shadow".
    client.publish("$aws/things/" + deviceName + "/shadow/update", json.dumps(payload))
    print("Sent to AWS IoT")


# Print out log messages for tracing.
def on_log(client, userdata, level, buf):
    print("Log: " + buf)


# Start the main program.
main()

GPIO.cleanup()

