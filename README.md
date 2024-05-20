# software

## Tabela Dados do Sensor:

| Temperatura (°C) | Umidade (%) | Veredito | Tipo | Data e Hora | ID Serial | Número de Série | Descrição |
|------------------|--------------|----------|------|-------------|-----------|-----------------|-----------|

- **temperature**: Um valor de ponto flutuante que armazena a temperatura medida pela sonda.
- **humidity**: Outro valor de ponto flutuante que armazena a umidade medida pela sonda. Este valor é usado apenas para alguns tipos de sondas.
- **verdict**: Uma string que indica se a sonda foi aprovada, está em análise ou foi reprovada.
- **type**: Uma string que representa o tipo de dispositivo que está sendo utilizado.
- **dateTime**: Tipo timestamp que informa a data e o horário que ocorreram as coletas de dados.
- **idSerial**: Armazena um número de série em formato de inteiro. Cada sensor possui um código serial único de 64 bits, usado para identificar exclusivamente cada sonda.
- **serialNumber**: Armazena o número de série em formato de string. Após receber o identificador único de cada sensor em formato de hexadecimal, esta variável será utilizada para manipular esta informação, mas em formato de string.

## Comandos Docker:

```bash
docker build -t cliente -f Dockerfile_clienteMQTT .
docker build -t servidor-tcp -f Dockerfile_servidorTCP .

docker run -d --name cliente-mqtt cliente-mqtt
docker run -d --name servidor-tcp servidor-tcp

docker build -t servidor -f Dockerfile_servidorMQTT .
docker run -d --name servidor servidor
docker run -it --name servidor bash
