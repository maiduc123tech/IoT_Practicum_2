# IoT Practicum 2: Thu thập, Lưu trữ và Tiền xử lý dữ liệu IoT

Kho lưu trữ mã nguồn và kết quả thực hành môn **IoT và Ứng dụng (INT14149)**.

## Cấu trúc thư mục
- `simulator.py`: Mô phỏng thiết bị IoT (ESP32) phát bản tin JSON chứa cảm biến lên MQTT Broker.
- `mqtt_collector.py`: Thu thập bản tin từ MQTT, kiểm tra tính hợp lệ, phát hiện mất gói và đo độ trễ `latency_ms`.
- `iot_data_log.csv`: Tệp lưu trữ dữ liệu thô thu thập được.
- `preprocess.py`: Tiền xử lý dữ liệu (lọc ngoại lai IQR, nội suy theo thời gian, resampling 10s, tạo đặc trưng).
- `iot_clean_data.csv`: Tệp lưu trữ dữ liệu sau khi đã làm sạch.
- `dashboard.py`: Giao diện trực quan hóa dữ liệu thời gian thực xây dựng bằng Streamlit.

## Hướng dẫn chạy hệ thống (Python 3.11)
1. **Cài đặt thư viện phụ thuộc:**
2. **Chạy thiết bị giả lập (Simulator):**
3. **Chạy chương trình thu thập dữ liệu (Collector):**
4. **Chạy chương trình tiền xử lý dữ liệu:**
5. **Khởi chạy Dashboard trực quan hóa:**
