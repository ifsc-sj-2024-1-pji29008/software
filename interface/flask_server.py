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

@app.route('/barramento=1', methods=['GET'])
def get_barramento():
    return jsonify(sensor.list_sensors(1)), 200

@app.route('/barramento=1&sensor=1', methods=['GET'])
def get_barramento_sensor1():
    return jsonify('temperatura:',sensor.get_temperature(1,1)), 200

@app.route('/barramento=2', methods=['GET'])
def get_data2():
    return jsonify(sensor.list_sensors(2)), 200

@app.route('/', methods=['GET'])
def get():
    return jsonify('Interface WEB da Placa Raspeberry'), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
