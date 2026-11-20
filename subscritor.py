import time
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("teste", qos=1)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    tempo_sub = time.perf_counter_ns()
    texto = msg.payload.decode()
    partes = texto.split(";")
    seq = int(partes[0])
    latencia_ms = (tempo_sub - int(partes[1])) / 1000000
    #print(msg.topic+" "+msg.payload.decode())
    print(seq, latencia_ms)
    
mqttc = mqtt.Client(CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_forever()