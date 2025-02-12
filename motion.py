import paho.mqtt.client as mqtt 
import time
import random
import global_state



with open("config.txt", "r") as f:
    BROKER = f.readline().strip()
    PORT = f.readline().strip()

client = mqtt.Client()
client.connect(BROKER, int(PORT), 60)

def on_connect(client, userdata, flags, rc):
    print(f"Conectado con resultado {rc}")
    if rc == 0:
        print("Conexión exitosa")
        client.subscribe("humidity")

def on_message(client, userdata, msg):
    print(f"Mensaje recibido: {msg.topic} {msg.payload}")
    if msg.topic == "humidity":
        global humidity_value_received
        humidity_value_received = int(msg.payload)

client.on_connect = on_connect
client.on_message = on_message
client.loop_start()

def activate_motion(client, topic, motion):
    client.publish(topic, str(motion))
    print("Motion activated")
    time.sleep(1)

aux = 0

while True:
    try:
        if aux > humidity_value_received:
            motion = True
            activate_motion(client, "motion", motion)
        else:
            motion = False
        aux = humidity_value_received
    except:
        pass
    time.sleep(5)
