import time
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

relatorio_msg = []

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("teste", qos=2)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    tempo_sub = time.perf_counter_ns()
    texto = msg.payload.decode()
    partes = texto.split(";")
    seq = int(partes[0])
    latencia_ns = (tempo_sub - int(partes[1]))
    hora_envio_ns = int(partes[1])
    relatorio_msg.append((seq, latencia_ns, hora_envio_ns))
    if (len(relatorio_msg) >= 1000):
        client.disconnect()
    
mqttc = mqtt.Client(CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
try:
    mqttc.loop_forever()
except KeyboardInterrupt:
    pass

ficheiro_csv = open("qos2_run1.csv", "w")
ficheiro_csv.write("seq,latencia_ns,hora_envio\n")
for seq, latencia_ns,hora_envio_ns in relatorio_msg:
    ficheiro_csv.write(f"{seq},{latencia_ns},{hora_envio_ns}\n")
ficheiro_csv.close()
print("Processo terminado. Foram entregues", len(relatorio_msg), "mensagens")
