import paho.mqtt.client as mqtt 
import time
import random

with open("config.txt", "r") as f:
    BROKER = f.readline().strip()
    PORT = f.readline().strip()

client = mqtt.Client()
client.connect(BROKER, int(PORT), 60)

def publish_temperature(client, topic, temp):
    client.publish(topic, str(temp))
    print("Temperature published")
    time.sleep(1)


while True:
    temperature = random.randint(15, 35)
    publish_temperature(client, "temperature", temperature)
    time.sleep(30)
