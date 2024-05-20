# Use a imagem base do Python
FROM python:3.10-slim

# Instale o Mosquitto
RUN apt-get update && \
    apt-get install -y mosquitto mosquitto-clients && \
    rm -rf /var/lib/apt/lists/*

# Instale o módulo paho-mqtt
RUN pip install paho-mqtt

# Copie o código do servidor MQTT para o contêiner
COPY servidor.py /servidor.py

# Defina o diretório de trabalho
WORKDIR /servidor

# Execute o servidor MQTT
CMD ["python3", "servidor.py"]
