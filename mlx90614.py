import time
import csv
import board
import busio
from adafruit_mlx90614 import MLX90614

# I2Cバスの初期化
i2c = busio.I2C(board.SCL, board.SDA)
mlx = MLX90614(i2c)

# CSVファイルの設定
csv_file = "mlx90614_temperature_data.csv"
header = ["タイムスタンプ", "環境温度(C)", "対象物温度(C)"]

# CSVファイルを新規作成し、ヘッダーを追加（ファイルが存在しない場合のみ）
try:
    with open(csv_file, mode='x', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
except FileExistsError:
    pass  # すでにファイルが存在している場合はヘッダーを追加しない

# 現在の温度を測定
ambient_temp = mlx.ambient_temperature  # 環境温度
object_temp = mlx.object_temperature  # 対象物温度
current_time = time.strftime("%Y-%m-%d %H:%M:%S")  # タイムスタンプ

print(f"時刻: {current_time}, 環境温度: {ambient_temp:.2f} C, 対象物温度: {object_temp:.2f} C")

# CSVファイルに書き込み
with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([current_time, ambient_temp, object_temp])

print("データ収集が完了しました。")

