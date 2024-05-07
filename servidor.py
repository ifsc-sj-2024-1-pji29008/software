import socket
import threading

# Configurações do servidor
host = 'localhost'
port = 12345

# Função para lidar com cada conexão de cliente
def handle_client(client_socket):
    try:
        print("Cliente conectado.")

        # Recebendo dados do cliente
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print("Dados recebidos:", data.decode('utf-8'))

        client_socket.close()
    except Exception as e:
        print(f"Erro: {e}")

# Criando um socket TCP/IP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Evita o erro "Address already in use"
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Vincula o socket ao endereço e porta
server.bind((host, port))

# Começa a ouvir por conexões
server.listen(5)
print(f"Servidor ouvindo em {host}:{port}")

try:
    # Loop principal do servidor para aceitar conexões
    while True:
        client_sock, address = server.accept()
        print(f"Conexão aceita de {address}")

        # Cria uma thread para lidar com a conexão do cliente
        client_thread = threading.Thread(target=handle_client, args=(client_sock,))
        client_thread.start()
except KeyboardInterrupt:
    print("Servidor interrompido.")

finally:
    server.close()
