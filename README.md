Smart Home Automation Project Using AWS, Sumologic and Raspberry Pi. For CICO03 Module.

Hardware Used;

SBC - Raspberry Pi 3 & GrovePi Shield + Pi Cobbler Breakout 

Sensors Used ;

a.  Grove Analog Temperature Sensor - Connected to A1 

b. 	Grove Analog Light Sensor - Connected to A0 
 
c.	PIR (Passive Infra-red) Sensor - Connected to GPIO 4 

d.	2N1 Opto-isolated Relay - Connected to GPIO 23 & 24 

e.	4W LED Strip DC9V 

f.	0.3W Motor Fan DC9V 



(2) Relays are to be +5V rail powered and Input of DC9V to Motor Fan and LED strip 

(3) Hardware components & schematic -IOT_CIC03_SmartHome_bb.jpg

https://github.com/preddy25/IOT-SmartHome/blob/master/IOT_CIC03_SmartHome_bb.jpg

Software & Code
1.	Current Code - Python 3.51 - gp_1a1.py 

 - Used to upload sensor data to AWS IOT for analysis via cert-based SSL in MQTT json strings. 
 - Also required to recieve data for actuation commmand.

(2) External Libraries required include  
a) SSL 

b) Json 

c) paho mqtt client 

d) grovepi 
