Smart Home Automation Project Using AWS, Sumologic and Raspberry Pi. For CICO03 Module.
Create a Github (https://github.com/) repository and upload the following:
(1)	SBC - Raspberry Pi & GrovePi Shield + Pi Cobbler Breakout 
a.	Sensors Used - Grove Analog Temperature Sensor - Connected to A1 
b.	Grove Analog Light Sensor - Connected to A0 
c.	Grove Touch Sensor - Connected to D3 
d.	PIR (Passive Infra-red) Sensor - Connected to GPIO 4 
e.	Opto-isolated Relay - Connected to GPIO 23 & 24 
f.	4W LED Strip DC12V 
g.	0.3W Motor Fan DC12 V 
(2) Relays are to be +5V rail powered and Input of 12V to Motor Fan and LED strip (3)Include an image of the hardware components/ schematics
1.	Current Code - Python 3.51 - gp_1a1.py * Used to upload sensor data to AWS IOT for analysis via cert-based SSL in MQTT json strings. * Also required to recieve data for actuation commmand.
(2) External Libraries required include 
a) SSL 
b) Json 
c) paho mqtt client 
d) grovepi 
e) pigpio
