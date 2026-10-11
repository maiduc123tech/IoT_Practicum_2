import json
import time
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "iot/lab2/esp32-01/telemetry"

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

print("Bắt đầu gửi dữ liệu giả lập thiết bị IoT...")
seq = 0

try:
  while True:
    seq += 1
    # Tạo dữ liệu giả lập chuẩn theo yêu cầu bài thực hành
    data = {
        "device_id": "esp32-01",
        "seq": seq,
        "ts": int(time.time() * 1000),
        "temperature": 25.5 + (seq % 3),  # Dao động nhiệt độ nhẹ
        "humidity": 60.0 + (seq % 5),  # Dao động độ ẩm nhẹ
        "light": 400 + seq * 10,
    }

    client.publish(TOPIC, json.dumps(data))
    print(f"[ĐÃ GỬI] Gói tin số {seq}: {data}")
    time.sleep(2)  # Gửi định kỳ mỗi 2 giây
except KeyboardInterrupt:
  print("Đã dừng chương trình giả lập.")