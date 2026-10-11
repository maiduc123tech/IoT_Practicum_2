import json
import time
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "iot/lab2/+/telemetry"

stats = {"ok": 0, "lost": 0, "invalid": 0}
last_seq = {}


def validate_and_process(data, recv_ms):
  # Kiểm tra các trường bắt buộc theo đề bài
  required_fields = ["device_id", "seq", "ts", "temperature", "humidity"]
  if not all(field in data for field in required_fields):
    stats["invalid"] += 1
    print(f"[REJECT] Thiếu trường dữ liệu: {data}")
    return

  dev_id = data["device_id"]
  seq = data["seq"]
  ts = data["ts"]
  temp = data["temperature"]
  hum = data["humidity"]

  # Kiểm tra dải giá trị hợp lý
  if not (-40 <= temp <= 80) or not (0 <= hum <= 100):
    stats["invalid"] += 1
    print(f"[REJECT] Dữ liệu ngoài dải: {data}")
    return

  # Kiểm tra mất gói qua sequence (seq)
  if dev_id in last_seq:
    expected_seq = last_seq[dev_id] + 1
    if seq > expected_seq:
      lost_count = seq - expected_seq
      stats["lost"] += lost_count
      print(f"[WARNING] Mất {lost_count} gói từ {dev_id}!")

  last_seq[dev_id] = seq
  stats["ok"] += 1

  # Tính độ trễ end-to-end
  latency_ms = recv_ms - ts
  print(
      f"[VALID] Dev: {dev_id} | Seq: {seq} | Temp: {temp}°C | Hum: {hum}% |"
      f" Latency: {latency_ms}ms"
  )

  # Lưu dữ liệu vào file CSV để làm minh chứng báo cáo
  with open("iot_data_log.csv", "a", encoding="utf-8") as f:
    f.write(f"{dev_id},{seq},{ts},{temp},{hum},{latency_ms}\n")


def on_message(client, userdata, msg):
  recv_ms = int(time.time() * 1000)
  try:
    payload_str = msg.payload.decode("utf-8")
    data = json.loads(payload_str)
    validate_and_process(data, recv_ms)
  except json.JSONDecodeError:
    stats["invalid"] += 1
    print(f"[ERROR] Sai định dạng JSON: {msg.payload}")


def main():
  client = mqtt.Client()
  client.on_message = on_message
  client.connect(BROKER, PORT, 60)
  client.subscribe(TOPIC)
  print("Đang kết nối và lắng nghe dữ liệu MQTT cho Bài 2...")
  client.loop_forever()


if __name__ == "__main__":
  main()