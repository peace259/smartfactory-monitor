import random
import httpx
import time

class Sensor:
    def __init__(self, sensor_id, sensor_type, unit, value_range):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.unit = unit
        self.value_range = value_range

    def generate_value(self) -> float:
        value = random.uniform(self.value_range[0], self.value_range[1])
        return round(value, 2)  # округлення до 2 знаків

    def to_payload(self) -> dict:
        return {
            "sensor_id": self.sensor_id,
            "value": self.generate_value(),
            "sensor_type": self.sensor_type,
            "unit": self.unit,
            "location": "Line A",
        }

def send_reading(sensor: Sensor):
    payload = sensor.to_payload()
    url = "http://localhost:8000/api/v1/sensors/"
    try:
        response = httpx.post(url, json=payload, headers={"X-API-Key": "change-me-in-production"})
        print(f"Sent: {response.status_code}")
    except httpx.RequestError as e:
        print(f"Error sending reading: {e}")

SENSORS = [
    Sensor("temp-001", "temperature", "°C", (60.0, 80.0)),
    Sensor("temp-002", "temperature", "°C", (55.0, 75.0)),
    Sensor("press-001", "pressure", "bar", (4.0, 7.0)),
    Sensor("vibr-001", "vibration", "mm/s", (0.5, 3.0)),
]

while True:
    for sensor in SENSORS:
        send_reading(sensor)
    time.sleep(10)
