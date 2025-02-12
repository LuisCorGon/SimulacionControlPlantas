import streamlit as st
import paho.mqtt.client as mqtt
import numpy as np
import time
import global_state
import matplotlib.pyplot as plt

def init_session_state():
    if "pagina" not in st.session_state:
        st.session_state.pagina = "Configuración"

    if "mqtt_client_started" not in st.session_state:
        st.session_state.mqtt_client_started = True
        start_mqtt_client()

def get_values(topic):
    if topic == "temperature":
        return global_state.temperature_values
    elif topic == "humidity":
        return global_state.humidity_values
    elif topic == "color":
        return global_state.color_values
    elif topic == "motion":
        return global_state.motion_values

def set_values(topic, value_received):
    if topic == "temperature":
        global_state.temperature_values.append(value_received)
    elif topic == "humidity":
        global_state.humidity_values.append(value_received)
    elif topic == "color":
        global_state.color_values.append(value_received)
    elif topic == "motion":
        global_state.motion_values.append(value_received)

def show_graph(tittle, values, x_label, y_label):
    fig, ax = plt.subplots()
    ax.plot(values, marker="o", linestyle="-", color="b")
    ax.set_title(tittle)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)


def start_mqtt_client():
    try:
        with open("config.txt", "r") as f:
            BROKER = f.readline().strip()
            PORT = int(f.readline().strip())

        def on_connect(client, userdata, flags, rc):
            print(f"Conectado con resultado {rc}")
            if rc == 0:
                print("Conexión exitosa")
                client.subscribe("temperature")
                client.subscribe("humidity")
                client.subscribe("color")
                client.subscribe("motion")
            else:
                print("Error de conexión")

        def on_message(client, userdata, msg):
            print(f"Mensaje recibido: {msg.topic} {msg.payload}")
            if msg.topic == "temperature":
                temperature_value_received = int(msg.payload)
                print(f"Temperatura recibida: {temperature_value_received}")
                set_values("temperature", temperature_value_received)
            elif msg.topic == "humidity":
                humidity_value_received = int(msg.payload)
                print(f"Humedad recibida: {humidity_value_received}")
                set_values("humidity", humidity_value_received)
            elif msg.topic == "color":
                color_value_received = msg.payload
                print(f"Color recibido: {color_value_received}")
                set_values("color", color_value_received)
            elif msg.topic == "motion":
                motion_value_received = msg.payload
                print(f"Movimiento recibido: {motion_value_received}")
                set_values("motion", motion_value_received)

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(BROKER, PORT, 60)

        client.loop_start()
    except Exception as e:
        st.error("Error al conectar al broker" + str(e))
        st.stop()

def on_page_change(pagina):
    st.session_state.pagina = pagina

def show_sidebar():
    st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            min-width: 200px;
            max-width: 200px;
        }
    </style>
    """,
    unsafe_allow_html=True
    )
    st.sidebar.title("Monitor")
    st.sidebar.button("Temperatura", on_click=on_page_change, args=("Temperatura",))
    st.sidebar.button("Humedad", on_click=on_page_change, args=("Humedad",))
    st.sidebar.button("Color", on_click=on_page_change, args=("Color",))

init_session_state()
st.title("Control de dispositivos IoT")
motion_values = get_values("motion")
print(motion_values)
if motion_values != []:
    motion = motion_values[-1]
    if motion == b'True':
        st.success("La humedad ha bajado demasiado, se ha activado el motor de agua")

if st.session_state.pagina == "Configuración":
    st.header("Configuración")
    st.subheader("Configuración del broker")
    st.text("Dirección del broker")
    broker = st.text_input("Broker", placeholder="localhost")
    st.text("Puerto del broker")
    puerto = st.text_input("Puerto", placeholder="1883")
    
    
    if st.button("Guardar configuración"):
        if not broker:
            st.error("Dirección del broker no puede estar vacía")
            st.stop()
        if not puerto:
            st.error("Puerto del broker no puede estar vacío")
            st.stop()
        with st.spinner("Guardando configuración"):
            BROKER = broker
            PORT = puerto
            with open("config.txt", "w") as f:
                f.write(BROKER)
                f.write("\n")
                f.write(PORT)
                f.write("\n")
        
        st.success("Configuración guardada")
        on_page_change("Monitor")
        st.rerun()

elif st.session_state.pagina == "Monitor":
    init_session_state()
    show_sidebar()
    st.header("Monitor")
    st.subheader("Monitor de los dispositivos IoT")
    
elif st.session_state.pagina == "Temperatura":
    show_sidebar()
    st.header("Monitor de temperatura")
    col1, col2 = st.columns(2)
    while True: 
        temperature_values = get_values("temperature")
        if temperature_values != []:
            with col1:
                print(temperature_values)
                print("MOSTRANDO VALORES DE LA TEMPERATURA")
                last_value = temperature_values[-1]
                st.subheader("Último valor recibido:")
                st.text(f"{last_value} ºC")
                
                avg_temperature = np.mean(temperature_values)
                st.subheader("Promedio de temperatura:")
                st.text(f"{avg_temperature:.2f} ºC")
            with col2:
                show_graph("Temperatura", temperature_values, "Tiempo", "Temperatura")
        else:
            st.text("Esperando datos...")
        time.sleep(5)
        st.rerun()

elif st.session_state.pagina == "Humedad":
    show_sidebar()
    st.header("Monitor de humedad")
    col1, col2 = st.columns(2)
    while True: 
        humidity_values = get_values("humidity")
        if humidity_values != []:
            with col1:
                print(humidity_values)
                print("MOSTRANDO VALORES DE LA HUMEDAD")
                last_value = humidity_values[-1]
                st.subheader("Último valor recibido:")
                st.text(f"{last_value} %")
                
                avg_humidity = np.mean(humidity_values)
                st.subheader("Promedio de humedad:")
                st.text(f"{avg_humidity:.2f} %")   
            with col2:
                show_graph("Humedad", humidity_values, "Tiempo", "Humedad")
        else:
            st.text("Esperando datos...")
        time.sleep(5)
        st.rerun()

elif st.session_state.pagina == "Color":
    show_sidebar()
    st.header("Monitor de color")
    col1, col2 = st.columns(2)
    while True: 
        color_values = get_values("color")
        if color_values != []:
            with col1:
                print(color_values)
                print("MOSTRANDO VALORES DE COLOR")
                last_value = color_values[-1]
                st.subheader("Último valor recibido:")
                st.text(last_value)
                
                #Contar el número de veces que aparece cada color, el que aparece más veces es el color más común
                color_count = {}
                for color in color_values:
                    if color in color_count:
                        color_count[color] += 1
                    else:
                        color_count[color] = 1
                most_common_color = max(color_count, key=color_count.get)
                st.subheader("Color más común:")
                st.text(most_common_color)
            with col2:
                show_graph("Color", color_values, "Tiempo", "Color")
        else:
            st.text("Esperando datos...")
        time.sleep(5)
        st.rerun()

