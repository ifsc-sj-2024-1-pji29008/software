# Criando um exemplo de comunicação MQTT com Python

import paho.mqtt.client as mqtt

# Função de callback que será chamada quando o cliente receber uma mensagem
def on_message(client, userdata, message):
    print("Mensagem recebida: " + str(message.payload.decode("utf-8")))
    print("Tópico: " + message.topic)
    print("QoS: " + str(message.qos))

# Função de callback que será chamada quando o cliente se conectar ao broker
def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker com código de resultado " + str(rc))
    client.subscribe("teste")

# Criando um cliente MQTT
client = mqtt.Client()

# Definindo as funções de callback
client.on_message = on_message
client.on_connect = on_connect

# Conectando ao broker
client.connect("test.mosquitto.org", 1883, 60)

# Iniciando o loop
client.loop_start()

# Publicando uma mensagem
client.publish("teste", "Olá, mundo!")

# Mantendo o programa rodando
while True:
    pass