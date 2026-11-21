import time
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

mqttc = mqtt.Client(CallbackAPIVersion.VERSION2)

mqttc.connect("localhost")
mqttc.loop_start()

#envio de 1000 mensagens numeradas
for i in range (1000):
  tempo_pub = time.perf_counter_ns()
  msg10 = mqttc.publish("teste", (str(i) + ";" + str(tempo_pub)), qos=2)
  time.sleep (0.01)
msg10.wait_for_publish()  

mqttc.disconnect()
mqttc.loop_stop()