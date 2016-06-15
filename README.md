# IOT-SmartHome
Smart Home Automation Project Using AWS, Sumologic and Raspberry Pi. For CICO03 Module.

Create a Github (https://github.com/) repository and upload the following:

1.Hardware Platform
  (1) SBC - Raspberry Pi  & GrovePi Shield + Pi Cobbler Breakout
      Sensors Used - Grove Analog Temperature Sensor - Connected to A1
                     Grove Analog Light Sensor - Connected to A0
                     Grove Touch Sensor    - Connected to D3
                     PIR (Passive Infra-red) Sensor - Connected to GPIO 4
                     Opto-isolated Relay  - Connected to GPIO 23 & 24
                     4W LED Strip DC12V
                     0.3W Motor Fan  DC12 V 

  (2) Relays are to be +5V rail powered and Input of 12V to Motor Fan and LED strip 
  (3)Include an image of the hardware components/ schematics

2. Current Code - Python 3.51 - gp_1a1.py 
        * Used to upload sensor data to AWS IOT for analysis via cert-based SSL in MQTT json strings.
        * Also required to recieve data for actuation commmand.
        

(2) External Libraries required include a) SSL
                                        b) Json
                                        c) paho mqtt client
                                        d) grovepi
                                        e) pigpio


