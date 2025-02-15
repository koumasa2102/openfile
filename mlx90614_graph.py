# plot_temperature_data_recent.py

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 日本語フォントの設定
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'  # Notoフォントのパス
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

# CSVファイルの読み込み
csv_file = "mlx90614_temperature_data.csv"
data = pd.read_csv(csv_file, parse_dates=["タイムスタンプ"], index_col="タイムスタンプ")

# 直近100個のデータを抽出
recent_data = data.tail(100)

# グラフ描画
plt.figure(figsize=(14, 7))  # グラフのサイズを設定
plt.plot(recent_data.index, recent_data["環境温度(C)"], label="環境温度(C)", color="blue", marker="o")
plt.plot(recent_data.index, recent_data["対象物温度(C)"], label="対象物温度(C)", color="red", marker="o")

# グラフのタイトルとラベル
plt.title("MLX90614温度測定データ（直近100件）")
plt.xlabel("タイムスタンプ")
plt.ylabel("温度(C)")
plt.xticks(rotation=45)  # x軸のラベルを45度傾ける
plt.legend()  # 凡例を表示
plt.grid(True)  # グリッドを表示
plt.tight_layout()  # 余白を自動調整

# グラフを画像ファイルとして保存
plt.savefig("mlx90614_temperature_graph_recent.png")
plt.show()

