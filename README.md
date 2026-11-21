# A3 — Medir a latência do MQTT

Atividade A3 de Sistemas Distribuídos em Tempo Real (UMAIA, 2026-2027).
Mede a latência ponta a ponta de mensagens MQTT, com um broker Mosquitto local, em duas condições: **QoS 0** e **QoS 2**.

## Ficheiros

| Ficheiro                                                     | Para que serve                                                                                                                                          |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `publicador.py`                                              | Envia 1000 mensagens para o tópico `teste`, com uma pausa nominal de 10 ms entre envios. Cada mensagem tem o formato `sequência;hora_de_envio_ns`.      |
| `subscritor.py`                                              | Recebe as mensagens, regista a hora de receção, calcula a latência e grava um CSV (`seq`, `latencia_ns`, `hora_envio`). Pára ao receber 1000 mensagens. |
| `analise.py`                                                 | Lê os CSV e calcula mínimo, média, p99, máximo e jitter (desvio-padrão) por condição, e gera os histogramas.                                            |
| `qos0_run1.csv`, `qos2_run1.csv`                             | Medições de cada condição.                                                                                                                              |
| `HistogramaLatenciaQoS_0.png`, `HistogramaLatenciaQoS_2.png` | Histogramas das latências (30 caixas, eixo x de 0 a 3 ms).                                                                                              |
| `condicoes.md`                                               | Condições da medição.                                                                                                                                   |

## Requisitos

- Python 3 com `paho-mqtt` (versão 2.x) e `matplotlib` (`python -m pip install paho-mqtt matplotlib`).
- Broker Mosquitto a correr em `localhost`, porta 1883.

## Como repetir uma medição

1. Escolhe a condição (QoS 0 ou QoS 2) e define o mesmo `qos` nos dois sítios:
   - em `publicador.py`, no argumento `qos=` da chamada `publish`;
   - em `subscritor.py`, no argumento `qos=` da chamada `subscribe`.
2. Em `subscritor.py`, muda o nome do ficheiro CSV (por exemplo, `qos0_run1.csv`).
3. Fecha as outras aplicações. Num terminal, arranca o subscritor: `python subscritor.py`. Espera pela mensagem `Connected...`.
4. Noutro terminal, arranca o publicador: `python publicador.py`. A medição demora cerca de 10 a 11 segundos.
5. O subscritor termina sozinho e escreve o CSV. Repete para a outra condição.
6. Corre `python analise.py` para ver as estatísticas e gerar os histogramas.

## Notas

- As horas usam `time.perf_counter_ns()` (contador monotónico), no mesmo computador, por isso as duas leituras partilham o mesmo relógio.
- Medição em `localhost`, num computador Windows não dedicado: os valores não incluem rede real.
