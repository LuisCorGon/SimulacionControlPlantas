import paho.mqtt.client as mqtt 
import time
import random

with open("config.txt", "r") as f:
    BROKER = f.readline().strip()
    PORT = f.readline().strip()

client = mqtt.Client()
client.connect(BROKER, int(PORT), 60)

def publish_color(client, topic, color):
    client.publish(topic, str(color))
    print("Color published")
    time.sleep(1)

while True:
    colors = ["Verde", "Verde Intenso", "Naranja", "Amarillo", "Blnaco", "Negro"]
    color = random.choice(colors)
    publish_color(client, "color", color )
    time.sleep(30)
