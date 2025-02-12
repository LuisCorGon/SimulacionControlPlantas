import paho.mqtt.client as mqtt 
import time
import random

# Obtiene los parametros de configuración a través del fichero config.txt
with open("config.txt", "r") as f:
    BROKER = f.readline().strip()
    PORT = f.readline().strip()

client = mqtt.Client()
client.connect(BROKER, int(PORT), 60)

# # Función para publicar un mensaje en un topic de la humedad
def publish_humidity(client, topic, humidity):
    result = client.publish(topic, str(humidity))
    if result.rc != mqtt.MQTT_ERR_SUCCESS:
        print(f"Error al publicar el mensaje: {result.rc}")
    else:
        print(f"Humedad {humidity} publicada correctamente.")
    time.sleep(1)

# Bucle infinito de publicación de mensajes en un topic de la humedad de la planta cada 30 segundos
while True:
    humidity = random.randint(30, 70)
    publish_humidity(client, "humidity", humidity )
    time.sleep(30)
