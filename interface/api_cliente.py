import requests
import RPi.GPIO as GPIO
import time

# Configuração das portas GPIO
sensor_pins = [4, 17, 27]  # Adicione as portas GPIO dos sensores

# Configuração da API REST
api_url = "http://<server_ip>:5000/sensor_data"  # Substitua <server_ip> pelo IP do servidor Flask

# Configuração do GPIO
GPIO.setmode(GPIO.BCM)
for pin in sensor_pins:
    GPIO.setup(pin, GPIO.IN)

def read_sensors():
    sensor_data = {}
    for pin in sensor_pins:
        sensor_data[f"sensor_{pin}"] = GPIO.input(pin)
    return sensor_data

def send_data_to_server(data):
    try:
        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            print("Dados enviados com sucesso!")
        else:
            print(f"Falha ao enviar dados: {response.status_code}")
    except Exception as e:
        print(f"Erro ao conectar ao servidor: {e}")

if __name__ == "__main__":
    try:
        while True:
            sensor_data = read_sensors()
            send_data_to_server(sensor_data)
            time.sleep(15)  # Intervalo de 15 segundos entre leituras
    except KeyboardInterrupt:
        print("Interrompido pelo usuário")
    finally:
        GPIO.cleanup()
