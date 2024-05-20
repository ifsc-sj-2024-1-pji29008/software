import paho.mqtt.client as mqtt
import csv
from datetime import datetime

# Função chamada quando um cliente se conecta
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Cliente conectado com sucesso ao broker MQTT")
        client.subscribe("test/topic")
    else:
        print(f"Falha na conexão com o código de retorno {rc}")

# Função chamada quando uma mensagem é recebida do cliente
def on_message(client, userdata, msg):
    print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")

    # Decodificar a mensagem
    message = msg.payload.decode()
    # Obter o timestamp atual
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Escrever no arquivo CSV
    with open("mqtt_data.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, msg.topic, message])

# Configurações do servidor MQTT
broker_host = "localhost"
broker_port = 1883

# Criando um cliente MQTT que atua como servidor
server = mqtt.Client()

# Atribuindo as funções de callback
server.on_connect = on_connect
server.on_message = on_message

# Conectando ao broker MQTT
try:
    server.connect(broker_host, broker_port, 60)
except Exception as e:
    print(f"Erro ao conectar ao broker MQTT: {e}")
    exit(1)

# Iniciando o loop para manter a conexão
server.loop_forever()
