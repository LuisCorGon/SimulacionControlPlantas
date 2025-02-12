import paho.mqtt.client as mqtt 
import time
import random

# Obtiene los datos de configuración desde el fichero config.txt
with open("config.txt", "r") as f:
    BROKER = f.readline().strip()
    PORT = f.readline().strip()

client = mqtt.Client()
client.connect(BROKER, int(PORT), 60)

# Función para publicar un mensaje en un topic de color
def publish_color(client, topic, color):
    client.publish(topic, str(color))
    print("Color published")
    time.sleep(1)

# Bucle infinito de publicación de mensajes en un topic de color de la planta cada 30 segundos
while True:
    colors = ["Verde", "Verde Intenso", "Naranja", "Amarillo", "Blnaco", "Negro"]
    color = random.choice(colors)
    publish_color(client, "color", color )
    time.sleep(30)
