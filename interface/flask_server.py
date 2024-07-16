import sys
import os
from datetime import datetime
from jpmsb import onewire
from flask import Flask, request, jsonify
import csv

sensor = onewire('software/interface/testes/python/sys/bus/w1/devices')

app = Flask(__name__)

# Função para escrever dados no arquivo CSV
def write_to_csv(data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('sensor_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        for sensor, value in data.items():
            writer.writerow([timestamp, sensor, value])

@app.route('/sensor_data', methods=['POST'])
def receive_sensor_data():
    data = request.json
    if not data:
        return jsonify({"error": "No data received"}), 400
    
    try:
        write_to_csv(data)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Lista todos os sensores conectados no barramento 1
@app.route('/barramento/1/sensores', methods=['GET'])
def get_barramento_1():
    try:
        sensors = sensor.list_sensors(1)
        return jsonify(sensors), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Lista o sensor 1 do barramento 1 com temperatura
@app.route('/barramento/1/sensor/1', methods=['GET'])
def get_barramento_1_sensor_1():
    try:
        address = sensor.get_address(1, 1)
        temperature = sensor.get_temperature(1, 1)
        return jsonify({'sensor_id': address, 'temperatura': temperature}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtém a temperatura do sensor 1 do barramento 2
@app.route('/barramento/2/sensor/1/temperatura', methods=['GET'])
def get_barramento_2_sensor_1_temperatura():
    try:
        temperature = sensor.get_temperature(2, 1)
        return jsonify({'temperatura': temperature}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Lista todos os sensores do barramento 2
@app.route('/barramento/2/sensores', methods=['GET'])
def get_barramento_2():
    try:
        sensors = sensor.list_sensors(2)
        return jsonify(sensors), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify('Interface WEB da Placa Raspberry'), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
