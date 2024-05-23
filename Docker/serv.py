from flask import Flask, jsonify
import csv

app = Flask(__name__)

# Função para ler dados do arquivo CSV
def read_csv_data():
    data = []
    try:
        with open("mqtt_data.csv", mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                data.append(row)
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
    return data

@app.route('/data', methods=['GET'])
def get_data():
    data = read_csv_data()
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
