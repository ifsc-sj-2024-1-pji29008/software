import os

class onewire:
    # Construtor da classe
    def __init__(self, w1_system_path='/sys/bus/w1/devices'):
        self._w1_system_path = w1_system_path
        self._w1_buses = self.search_w1_buses(self._w1_system_path)
        self._w1_ds18b20_sensors = {}

        # Definindo o pull-up de todos os barramentos em zero
        for bus in self._w1_buses:
            self.set_pullup(bus, 0)

        # Procurando por sensores
        for bus in self._w1_buses:
            self.set_search(bus, 1)
        
    # Procura por barramentos 1-wire
    def search_w1_buses(self, w1_system_path):
        w1_buses = []
        for bus in os.listdir(w1_system_path):
            if bus.startswith('w1_bus_master'):
                w1_buses.append(bus)

        w1_buses.sort()
        return w1_buses

    # Define valores nos pseudo-arquivos de um barramento 1-wire
    def set_value(self, w1_bus, property_name, value):
        path = os.path.join(self._w1_system_path, w1_bus, property_name);
        with open(path, 'w') as f:
            f.write(str(value))

    # Define a busca de sensores em um barramento 1-wire
    def set_search(self, w1_bus, value):
        self.set_value(w1_bus, 'w1_master_search', value)

        ds18b20_sensors = []
        for sensor in os.listdir(os.path.join(self._w1_system_path, w1_bus)):
            if sensor.startswith('28-'):
                ds18b20_sensors.append(sensor)
        
        self._w1_ds18b20_sensors[w1_bus] = ds18b20_sensors
 
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
