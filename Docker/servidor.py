import socket

server_host = 'localhost'
server_port = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((server_host, server_port))
    server_socket.listen()
    print(f"Servidor TCP/IP escutando em {server_host}:{server_port}...")

    while True:
        client_socket, addr = server_socket.accept()
        with client_socket:
            print(f"Conexão estabelecida com {addr}")
            data = client_socket.recv(1024)
            if data:
                print(f"Dados recebidos: {data.decode('utf-8')}")
                client_socket.sendall(b"Dados recebidos com sucesso")
