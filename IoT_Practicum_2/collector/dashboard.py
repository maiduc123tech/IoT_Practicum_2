import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="IoT Dashboard", layout="wide")

st.title("📊 IoT Practicum 2 - Real-time & Cleaned Data Dashboard")

# Kiểm tra và tìm file iot_clean_data.csv ở thư mục gốc hoặc thư mục collector
file_path = "iot_clean_data.csv"
if not os.path.exists(file_path):
  file_path = "collector/iot_clean_data.csv"

if not os.path.exists(file_path):
  st.error(
      "⚠️ Không tìm thấy file 'iot_clean_data.csv'. Hãy đảm bảo bạn đã chạy"
      " file preprocess.py thành công!"
  )
  st.stop()

df = pd.read_csv(file_path, index_col="datetime", parse_dates=True)

st.subheader("1. Thống kê tổng quan dữ liệu")
st.metric(
    label="Tổng số bản ghi sau tiền xử lý", value=f"{len(df)} bản ghi"
)

st.subheader("2. Biểu đồ Nhiệt độ và Độ ẩm theo thời gian")
if "temperature_clean" in df.columns and "humidity_clean" in df.columns:
  st.line_chart(df[["temperature_clean", "humidity_clean"]])
else:
  st.line_chart(df)

st.subheader("3. Bảng chi tiết dữ liệu sạch")
st.dataframe(df)