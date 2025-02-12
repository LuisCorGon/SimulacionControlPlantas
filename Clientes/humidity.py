import paho.mqtt.client as mqtt 
import time
import random

with open("config.txt", "r") as f:
    BROKER = f.readline().strip()
    PORT = f.readline().strip()

client = mqtt.Client()
client.connect(BROKER, int(PORT), 60)

def publish_humidity(client, topic, humidity):
    result = client.publish(topic, str(humidity))
    if result.rc != mqtt.MQTT_ERR_SUCCESS:
        print(f"Error al publicar el mensaje: {result.rc}")
    else:
        print(f"Humedad {humidity} publicada correctamente.")
    time.sleep(1)


while True:
    humidity = random.randint(30, 70)
    publish_humidity(client, "humidity", humidity )
    time.sleep(30)
