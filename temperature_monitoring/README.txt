Мониторинг температуры

Симулятор 5 датчиков температуры. Данные идут в InfluxDB, графики в Grafana.

Запуск

docker-compose up -d
pip install influxdb-client
python simulator.py

Grafana

http://localhost:3000
Логин: admin
Пароль: admin

Источник данных

URL: http://influxdb:8086
Organization: myorg
Token: my-super-token
Bucket: temperature

Запрос для графика

from(bucket: "temperature")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "temperature")
  |> aggregateWindow(every: 1m, fn: mean)
  |> yield(name: "mean")

Датчики

Печь №1 — 180°C
Печь №2 — 200°C
Холодильник — 4°C
Цех — 22°C
Улица — 10°C

Файлы

docker-compose.yml — запуск InfluxDB и Grafana
simulator.py — генерация данных