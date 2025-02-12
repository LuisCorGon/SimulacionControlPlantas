import paho.mqtt.client as mqtt 
import time
import random

# Obtiene los datos de configuración desde el fichero config.txt
with open("config.txt", "r") as f:
    BROKER = f.readline().strip()
    PORT = f.readline().strip()

client = mqtt.Client()
client.connect(BROKER, int(PORT), 60)

# Función para publicar un mensaje en un topic de temperatura
def publish_temperature(client, topic, temp):
    client.publish(topic, str(temp))
    print("Temperature published")
    time.sleep(1)


# Bucle infinito de publicación de mensajes en un topic de temperatura de la planta cada 30 segundos
while True:
    temperature = random.randint(15, 35)
    publish_temperature(client, "temperature", temperature)
    time.sleep(30)
