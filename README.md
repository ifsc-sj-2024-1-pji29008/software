# software

Tabela Dados do Sensor:

| Temperatura (°C) | Umidade (%) | Veredito     | Tipo       | Data e Hora           | ID Serial | Número de Série | Descriação |
|------------------|-------------|--------------|------------|-----------------------|-----------|-----------------|-----------------|

• float temperature : Um valor de ponto flutuante que armazena a temperatura medida
pela sonda;

• float humidity : Outro valor de ponto flutuante que armazena a umidade medida pela
sonda. Esse valor é usado apenas para alguns tipos de sondas;

• string verdict : Uma string que indica se a sonda foi aprovada, está em análise ou foi
reprovada;

• string type : Uma string que representa o tipo de dispositivo que está sendo utilizado;

• timestamp dateTime : Tipo timestamp que informa a data e o horário que ocorreram as
coletas de dados.

• int idSerial : Armazena um número de série em formato de inteiro. Cada sensor possui
um código serial único de 64 bits, usado para identificar exclusivamente cada sonda;

• string serialNumber : Armazena o número de série em formato de string. Após receber
o identificador único de cada sensor em formato de hexadecimal, esta variável será utilizada
para manipular esta informação mas em formato de string.


docker build -t cliente -f Dockerfile_clienteMQTT .
docker build -t servidortcp -f Dockerfile_servidorTCP .


docker run -d --name cliente-mqtt cliente-mqtt
docker run -d --name servidortcp servidortcp


docker build -t servidor -f Dockerfile_servidorMQTT .
docker run -d --name servidor servidor
docker run -it --name servidor /bin/bash
