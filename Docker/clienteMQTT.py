import paho.mqtt.client as mqtt
import datetime
import threading
import socket
import time

# Configurações do servidor MQTT
broker_host = "localhost"
broker_port = 1883
mqtt_topic = "test/topic"

# Configurações do servidor TCP/IP
server_host = 'localhost'
server_port = 12345

# Função chamada quando o cliente MQTT se conecta ao broker
def on_connect(client, userdata, flags, rc):
    print(f"Conectado com código de retorno {rc}")
    # Assina o tópico MQTT
    client.subscribe(mqtt_topic)

# Função chamada quando uma mensagem MQTT é recebida
def on_message(client, userdata, msg):
    print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")
    # Envia os dados para o servidor TCP/IP
    send_data_to_server(msg.payload.decode())

# Função para enviar dados para o servidor TCP/IP
def send_data_to_server(data):
    try:
        # Cria um socket TCP/IP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            print(f"Tentando conectar ao servidor {server_host}:{server_port}...")
            # Conecta ao servidor
            client_socket.connect((server_host, server_port))
            print("Conexão estabelecida com sucesso!")

            # Envia os dados para o servidor
            client_socket.sendall(data.encode('utf-8'))
            print("Dados enviados para o servidor com sucesso!")

    except Exception as e:
        print(f"Erro ao enviar dados para o servidor: {e}")

# Função para publicar dados MQTT periodicamente
def publish_mqtt_data_periodically(client, interval):
    while True:
        publish_mqtt_data(client)
        time.sleep(interval)

# Função para publicar dados MQTT
def publish_mqtt_data(client):
    # Exemplo de dados
    temperature = 23.5  # float
    humidity = 45.2     # float
    verdict = 'aprovada'  # string
    type = 'Tipo1'        # string
    dateTime = datetime.datetime.now()  # timestamp
    idSerial = 1234567890123456  # int (64 bits)
    serialNumber = hex(idSerial)[2:]  # string (hexadecimal)

    # Criando a string com os dados
    data_string = (f"Temperatura: {temperature}°C, "
                   f"Umidade: {humidity}%, "
                   f"Veredito: {verdict}, "
                   f"Tipo: {type}, "
                   f"Data e Hora: {dateTime.strftime('%Y-%m-%d %H:%M:%S')}, "
                   f"ID Serial: {idSerial}, "
                   f"Número de Série: {serialNumber}")

    # Publica os dados MQTT
    client.publish(mqtt_topic, data_string)

# Função para iniciar o loop MQTT em uma nova thread
def mqtt_loop(client):
    client.loop_forever()

# Criando um cliente MQTT
client = mqtt.Client()

# Atribuindo as funções de callback
client.on_connect = on_connect
client.on_message = on_message

# Conectando ao broker MQTT
client.connect(broker_host, broker_port, 60)

# Iniciando o loop MQTT em uma nova thread
mqtt_thread = threading.Thread(target=mqtt_loop, args=(client,))
mqtt_thread.start()

# Iniciando o envio periódico de dados MQTT a cada 15 segundos
publish_thread = threading.Thread(target=publish_mqtt_data_periodically, args=(client, 15))
publish_thread.start()
