import paho.mqtt.client as mqtt 
import time
import random
import global_state


# Obtiene los parametros de configuración a través del fichero config.txt
with open("config.txt", "r") as f:
    BROKER = f.readline().strip()
    PORT = f.readline().strip()

client = mqtt.Client()
client.connect(BROKER, int(PORT), 60)

# Se suscribe al topic de humedad para verificar si la humedad ha bajado demasiado
def on_connect(client, userdata, flags, rc):
    print(f"Conectado con resultado {rc}")
    if rc == 0:
        print("Conexión exitosa")
        client.subscribe("humidity")

# Recibe los mensajes del topic de humedad y almacena el valor recibido en la variable global humidity_value_received
def on_message(client, userdata, msg):
    print(f"Mensaje recibido: {msg.topic} {msg.payload}")
    if msg.topic == "humidity":
        global humidity_value_received
        humidity_value_received = int(msg.payload)

client.on_connect = on_connect
client.on_message = on_message
client.loop_start()

# Función para activar el motor de agua
def activate_motion(client, topic, motion):
    client.publish(topic, str(motion))
    print("Motion activated")
    time.sleep(1)


# Bucle infinito de comprobación de la humedad y activación del motor de agua si la humedad ha bajado demasiado
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
