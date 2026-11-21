import csv
import statistics
import matplotlib.pyplot as plt

valoresQoS_0 = []
valoresQoS_2 = []
horaEnvioQoS_0 = []
horaEnvioQoS_2 = []
intervalos_qos0 = []
intervalos_qos2 = []
n_mensagens = 1000

with open("qos0_run1.csv") as a:
    leitor = csv.DictReader(a)
    for linha in leitor:
        numero = int(linha["latencia_ns"])
        valoresQoS_0.append(numero/1000000)

with open("qos2_run1.csv") as b:
    leitor = csv.DictReader(b)
    for linha in leitor:
        numero = int(linha["latencia_ns"])
        valoresQoS_2.append(numero/1000000)

with open("qos0_run1.csv") as a:
    leitor = csv.DictReader(a)
    for linha in leitor:
        numero = int(linha["hora_envio"])
        horaEnvioQoS_0.append(numero)

with open("qos2_run1.csv") as b:
    leitor = csv.DictReader(b)
    for linha in leitor:
        numero = int(linha["hora_envio"])
        horaEnvioQoS_2.append(numero)

for i in range(1, len(horaEnvioQoS_0)):
    intervalos_qos0.append((horaEnvioQoS_0[i] - horaEnvioQoS_0[i-1]) / 1000000)

for i in range(1, len(horaEnvioQoS_2)):
    intervalos_qos2.append((horaEnvioQoS_2[i] - horaEnvioQoS_2[i-1]) / 1000000)

valoresQoS_0.sort()
valoresQoS_2.sort()

p99_qos0 = valoresQoS_0[int(0.99 * (len(valoresQoS_0) - 1))]
p99_qos2 = valoresQoS_2[int(0.99 * (len(valoresQoS_2) - 1))]

jitter_qos0 = statistics.pstdev(valoresQoS_0)
jitter_qos2 = statistics.pstdev(valoresQoS_2)

print("Análise Latência")
print("Quantidade de valores QoS 0:", len(valoresQoS_0), "de", n_mensagens)
print("Quantidade de valores QoS 2:", len(valoresQoS_2), "de", n_mensagens)

print(f"Latência mín / média QoS 0: {valoresQoS_0[0]:.3f} / {statistics.mean(valoresQoS_0):.3f} ms")
print(f"Latência mín / média QoS2: {valoresQoS_2[0]:.3f} / {statistics.mean(valoresQoS_2):.3f} ms")

print(f"Latência p99 / máx  QoS 0: {p99_qos0:.3f} / {valoresQoS_0[-1]:.3f} ms")
print(f"Latência p99 / máx  QoS 2: {p99_qos2:.3f} / {valoresQoS_2[-1]:.3f} ms")

print(f"Jitter (desvio-pad.) QoS 0: {jitter_qos0:.3f} ms")
print(f"Jitter (desvio-pad.) QoS 2: {jitter_qos2:.3f} ms")


print("Período de Envio ")
print("Quantidade de intervalos QoS 0:", len(intervalos_qos0), "de", n_mensagens-1)
print("Quantidade de intervalos QoS 2:", len(intervalos_qos2), "de", n_mensagens-1)

print(f"Períodos de Envio mín / média / max QoS 0: {min(intervalos_qos0):.3f} / {statistics.mean(intervalos_qos0):.3f} / {max(intervalos_qos0):.3f} ms")
print(f"Períodos de Envio mín / média / max QoS 2: {min(intervalos_qos2):.3f} / {statistics.mean(intervalos_qos2):.3f} / {max(intervalos_qos2):.3f} ms")

plt.hist(valoresQoS_0, bins=30, range=(0,3))
plt.title("Histograma Latência QoS 0")
plt.xlabel ("Latência (ms)")
plt.ylabel ("Nº mensagens")
plt.ylim(0, 750)
plt.savefig("HistogramaLatenciaQoS_0.png")
plt.close()

plt.hist(valoresQoS_2, bins=30, range=(0,3))
plt.title("Histograma Latência QoS 2")
plt.xlabel ("Latência (ms)")
plt.ylabel ("Nº mensagens")
plt.ylim(0, 750)
plt.savefig("HistogramaLatenciaQoS_2.png")
plt.close()