import numpy as np
import pandas as pd

# 1. Đọc dữ liệu từ file log thô
try:
  df = pd.read_csv(
      "iot_data_log.csv",
      header=None,
      names=[
          "device_id",
          "seq",
          "ts",
          "temperature",
          "humidity",
          "latency_ms",
      ],
  )
except FileNotFoundError:
  print(
      "[LỖI] Không tìm thấy file iot_data_log.csv. Hãy chắc chắn bạn đã chạy"
      " phần thu thập dữ liệu trước!"
  )
  exit()

# Chuyển đổi timestamp sang định dạng thời gian chuẩn datetime
df["datetime"] = pd.to_datetime(df["ts"], unit="ms")
df.set_index("datetime", inplace=True)

print("=== 5 Dòng dữ liệu thô ban đầu ===")
print(df.head())


# 2. Phát hiện và xử lý Outlier bằng phương pháp IQR
def remove_outliers_iqr(series):
  Q1 = series.quantile(0.25)
  Q3 = series.quantile(0.75)
  IQR = Q3 - Q1
  lower_bound = Q1 - 1.5 * IQR
  upper_bound = Q3 + 1.5 * IQR
  return series.where((series >= lower_bound) & (series <= upper_bound))


df["temperature_clean"] = remove_outliers_iqr(df["temperature"])
df["humidity_clean"] = remove_outliers_iqr(df["humidity"])

# 3. Xử lý giá trị thiếu (Interpolate theo thời gian)
df["temperature_clean"] = df["temperature_clean"].interpolate(
    method="time"
)
df["humidity_clean"] = df["humidity_clean"].interpolate(method="time")

# 4. Resampling theo cửa sổ thời gian 10 giây (lấy trung bình)
df_resampled = df.resample("10s").mean(numeric_only=True)

# 5. Tạo đặc trưng mới (Rolling mean và Delta chênh lệch)
df_resampled["temp_roll6"] = (
    df_resampled["temperature_clean"].rolling(window=6).mean()
)
df_resampled["temp_delta"] = df_resampled["temperature_clean"].diff()

print("\n=== Dữ liệu sau khi tiền xử lý (Resampled & Feature Engineering) ===")
print(df_resampled.head(10))

# Lưu kết quả tiền xử lý ra file mới để làm minh chứng báo cáo
df_resampled.to_csv("iot_clean_data.csv")
print(
    "\n[THÀNH CÔNG] Đã lưu kết quả tiền xử lý vào file 'iot_clean_data.csv'."
)