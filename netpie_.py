from machine import Pin
import network
from simple import MQTTClient
from machine import Pin
import dht
import time
import json
from neopixel import NeoPixel

d = dht.DHT11(Pin(13))

pin = Pin(23, Pin.OUT)   
np = NeoPixel(pin, 8)

Relay1 = Pin(14,Pin.OUT)
Relay2 = Pin(27,Pin.OUT)

Button1 = Pin(15,Pin.IN,Pin.PULL_UP)
Button2 = Pin(2,Pin.IN,Pin.PULL_UP)
Button3 = Pin(0,Pin.IN,Pin.PULL_UP)
Button4 = Pin(4,Pin.IN,Pin.PULL_UP)

# Network interface Mode = Station
wlan = network.WLAN(network.STA_IF)
wlan.active(True) # Activate station mode

print('WiFi Connecting...')
wlan.connect(' ', ' ')
while not wlan.isconnected(): # if wlan.isconnected() == False:
    pass # pass loop until wlan.isconnected is True

print('WiFi Connected!')
print(wlan.ifconfig())

MQTT_Client_ID = ' '
MQTT_Token = ' '
MQTT_Secret = ' '
MQTT_Broker = ' '

# Create Netpie profile
client = MQTTClient(MQTT_Client_ID, MQTT_Broker, user = MQTT_Token, password = MQTT_Secret)

# Connect to Netpie
client.connect()

while True:
    d.measure()
    temp = d.temperature() # eg. 23 (°C)
    hum = d.humidity()
    Btn1_state = Button1.value()
    Btn2_state = Button2.value()
    Btn3_state = Button3.value()
    Btn4_state = Button4.value()
    time.sleep(0.5)
    
    if Btn1_state == 0:
        np[0] = (25, 0, 0)     
        np.write()
        Relay1.value(1)
        client.publish('@shadow/data/update'
                  ,json.dumps({
                      'data':{
                          'Relay1' : 'ON',
                          }
                      }))
        
    elif Btn2_state == 0:
        np[1] = (25, 0, 0)     
        np.write()
        Relay2.value(1)
        client.publish('@shadow/data/update'
                  ,json.dumps({
                      'data':{
                          'Relay2' : 'ON',
                          }
                      }))
        
    elif Btn3_state == 0:
        np[0] = (0, 0, 0)     
        np.write()
        Relay1.value(0)
        client.publish('@shadow/data/update'
                  ,json.dumps({
                      'data':{
                          'Relay1' : 'OFF',
                          }
                      }))
        
    elif Btn4_state == 0:
        np[1] = (0, 0, 0)     
        np.write()
        Relay2.value(0)
        client.publish('@shadow/data/update'
                  ,json.dumps({
                      'data':{
                          'Relay2' : 'OFF',
                          }
                      }))
    
    print('Temp :',temp,'Humidity :',hum)
    
    client.publish('@shadow/data/update'
                  ,json.dumps({
                      'data':{
                          'temperature' : temp,
                          'humidity' : hum
                          }
                      }))
    
