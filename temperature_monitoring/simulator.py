import time
import random
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# ==================================================
# НАСТРОЙКИ ПОДКЛЮЧЕНИЯ (должны совпадать с docker-compose.yml)
# ==================================================
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "my-super-token"      # Токен из docker-compose.yml
INFLUX_ORG = "myorg"                  # Организация
INFLUX_BUCKET = "temperature"         # Бакет для данных

# Создаём клиент для подключения к базе
client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

# ==================================================
# СПИСОК ДАТЧИКОВ
# ==================================================
sensors = [
    {"id": "oven_1", "name": "Печь №1", "mean": 180, "std": 5},
    {"id": "oven_2", "name": "Печь №2", "mean": 200, "std": 8},
    {"id": "cooler_1", "name": "Холодильник №1", "mean": 4, "std": 1},
    {"id": "workshop", "name": "Цех (общая)", "mean": 22, "std": 2},
    {"id": "outside", "name": "На улице", "mean": 10, "std": 5}
]

print("=" * 50)
print("Запуск симулятора датчиков")
print("Данные отправляются в InfluxDB каждые 2 секунды")
print("Нажми Ctrl+C для остановки")
print("=" * 50)

try:
    while True:
        for sensor in sensors:
            # Генерируем случайную температуру по нормальному распределению
            value = random.gauss(sensor["mean"], sensor["std"])
            value = round(value, 1)
            
            # Создаём точку данных (одно измерение)
            point = Point("temperature") \
                .tag("sensor_id", sensor["id"]) \
                .tag("sensor_name", sensor["name"]) \
                .field("value", value)
            
            # Отправляем в InfluxDB
            write_api.write(bucket=INFLUX_BUCKET, record=point)
            
            # Выводим в консоль для наглядности
            print(f"[{sensor['name']}] {value} °C")
        
        print("-" * 30)
        time.sleep(2)  # Пауза 2 секунды между циклами
        
except KeyboardInterrupt:
    print("\n🛑 Симулятор остановлен пользователем")
    client.close()
    print("Соединение с InfluxDB закрыто")