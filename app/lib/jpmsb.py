import os
import time

class onewire:
    # Construtor da classe
    def __init__(self, w1_system_path='/sys/bus/w1/devices', search_tries=20): 
        self._w1_system_path = w1_system_path
        self._search_tries = search_tries
        self._w1_buses = self.search_w1_buses(self._w1_system_path)
        self._w1_ds18b20_sensors = {}

        # Definindo o pull-up de todos os barramentos em zero
        for bus in self._w1_buses:
            self.set_pullup(bus, 0)

        # Procurando por sensores
        self.search_all_sensors()
        
    # Procura por barramentos 1-wire
    def search_w1_buses(self, w1_system_path):
        w1_buses = []
        for bus in os.listdir(w1_system_path):
            if bus.startswith('w1_bus_master'):
                w1_buses.append(bus)

        w1_buses.sort()
        return w1_buses

    # Procura por sensores em um barramento 1-wire específico
    def search_sensors(self, w1_bus):
        ds18b20_sensors = []

        for i in range(self._search_tries):
            self.set_search(w1_bus, 1)
            time.sleep(0.001)

        for sensor in os.listdir(os.path.join(self._w1_system_path, w1_bus)):
            if sensor.startswith('28-'):
                ds18b20_sensors.append(sensor)

        self._w1_ds18b20_sensors[w1_bus] = ds18b20_sensors

    # Procura por todos os sensores em todos os barramentos 1-wire
    def search_all_sensors(self):
        for bus in self._w1_buses:
            self.search_sensors(bus)

    # Define valores nos pseudo-arquivos de um barramento 1-wire
    def set_value(self, w1_bus, property_name, value):
        path = os.path.join(self._w1_system_path, w1_bus, property_name);
        with open(path, 'w') as f:
            f.write(str(value))

    # Define a busca de sensores em um barramento 1-wire
    def set_search(self, w1_bus, value):
        self.set_value(w1_bus, 'w1_master_search', value)

    # Define o pull-up de um barramento 1-wire
    def set_pullup(self, w1_bus, value):
        self.set_value(w1_bus, 'w1_master_pullup', value)

    # Retorna a lista de barramentos 1-wire
    def list_w1_buses(self):
        return self._w1_buses

    # Retorna uma lista de sensores DS18B20 em um barramento 1-wire
    def list_sensors(self, w1_bus_number):
        w1_bus_name = self._w1_buses[w1_bus_number-1]
        return self._w1_ds18b20_sensors[w1_bus_name]

    # Retorna o valor de temperatura de um sensor DS18B20 pelo ID
    def get_temperature(self, w1_bus_number, sensor_id):
        if w1_bus_number < 1 or w1_bus_number > len(self._w1_buses):
            return None
        elif sensor_id < 1 or sensor_id > len(self._w1_ds18b20_sensors[self._w1_buses[w1_bus_number-1]]):
            return None

        w1_bus_name = self._w1_buses[w1_bus_number-1]
        sensor_address = self._w1_ds18b20_sensors[w1_bus_name][sensor_id-1]
        path = os.path.join(self._w1_system_path, w1_bus_name, sensor_address, 'temperature')

        with open(path, 'r') as f:
            temperature = f.read()

            if temperature == '':
                return None
            temperature = float(temperature) / 1000.0

        return temperature

    # Obtém o endereco de um sensor DS18B20
    def get_address(self, w1_bus_number, sensor_id):
        if w1_bus_number < 1 or w1_bus_number > len(self._w1_buses):
            return None
        elif sensor_id < 1 or sensor_id > len(self._w1_ds18b20_sensors[self._w1_buses[w1_bus_number-1]]):
            return None

        w1_bus_name = self._w1_buses[w1_bus_number-1]
        return self._w1_ds18b20_sensors[w1_bus_name][sensor_id-1]

class sensor:
    def __init__(self, w1_system_path='/sys/bus/w1/devices'):
        self._w1 = onewire(w1_system_path)

    def get_temperature(self, w1_bus_number):
        return self._w1.get_temperature(w1_bus_number, 1)

    def get_address(self, w1_bus_number):
        return self._w1.get_address(w1_bus_number, 1)

    def list_w1_buses(self):
        return self._w1.list_w1_buses()

    def list_sensors(self):
        sensors = []
        for index, bus in enumerate(self.list_w1_buses()):
            sensors.append(self._w1.get_address(index + 1, 1))

        return sensors

    def get_sensor_amount():
        return len(self._w1.list_w1_buses())
