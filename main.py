import time                   # Allows use of time.sleep() for delays 
from machine import Pin       # Pin object to configure pins
from machine import ADC   # ADC object to configure reading values
from dht import DHT    
from lib.mqtt import MQTTClient
import ujson
import constants as CONST

th = DHT(Pin('P23', mode=Pin.OPEN_DRAIN), 0)


# function to read values from the DHT11 sensor

LightSensorPin = 'P20'
lightPin = Pin(LightSensorPin, mode=Pin.IN)
adc = ADC(bits=10) 
apin = adc.channel(attn=ADC.ATTN_11DB, pin=LightSensorPin)

def sub_cb(topic, msg): #callback
   print(msg)


# MQTT Setup
client = MQTTClient(client_id,
                    CONST.UBIDOTS_MQTT_URL,
                    user=CONST.UBIDOTS_TOKEN,
                    password='',
                    port=CONST.UBIDOTS_MQTT_PORT)

client.set_callback(sub_cb)
client.connect() 
print('connected')


my_topic = CONST.UBIDOTS_MQTT_TOPIC + "My_Device" 

payload = {}

while True:
    time.sleep(2)
    result = th.read()
    while not result.is_valid():
        time.sleep(.5)
        result = th.read()
    val = apin() # read an analog value
    print("Value", val ,result.temperature, result.humidity )

    payload['temperature'] = result.temperature
    payload['humidity'] = result.humidity
    payload['light'] = val

    json_payload = ujson.dumps(payload)
    print(json_payload)

    client.publish(topic=my_topic, msg=json_payload)
    client.check_msg()
