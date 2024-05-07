import socket
import datetime

# Configurações do servidor
host = 'localhost'
port = 12345

def send_data_to_server(data):
    try:
        # Cria um socket TCP/IP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conecta ao servidor
        client_socket.connect((host, port))

        # Envia os dados para o servidor
        client_socket.sendall(data.encode('utf-8'))

        # Fecha a conexão
        client_socket.close()
    except Exception as e:
        print(f"Erro ao enviar dados para o servidor: {e}")

# Exemplo de dados
temperature = 23.5  # float
humidity = 45.2     # float
verdict = 'aprovada'  # string
type = 'Tipo1'        # string
dateTime = datetime.datetime.now()  # timestamp
idSerial = 1234567890123456  # int (64 bits)
serialNumber = hex(idSerial)[2:]  # string (hexadecimal)

# Criando a string com os dados
data_string = f"Temperatura: {temperature}°C, " \
              f"Umidade: {humidity}%, " \
              f"Veredito: {verdict}, " \
              f"Tipo: {type}, " \
              f"Data e Hora: {dateTime.strftime('%Y-%m-%d %H:%M:%S')}, " \
              f"ID Serial: {idSerial}, " \
              f"Número de Série: {serialNumber}"

# Envia os dados para o servidor
send_data_to_server(data_string)

print("Dados enviados para o servidor com sucesso!")
