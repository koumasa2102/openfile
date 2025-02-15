import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yfinance as yf
import time
from datetime import datetime
import os  # 環境変数を扱うモジュール

# Gmail設定（環境変数から取得）
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')

# 環境変数が未設定の場合にエラーを出す
if not GMAIL_USER or not GMAIL_PASSWORD:
    raise EnvironmentError("環境変数 'GMAIL_USER' または 'GMAIL_PASSWORD' が設定されていません。")

# Gmail送信関数
def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = GMAIL_USER  # 必要に応じて他のアドレスに変更可能
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.send_message(msg)
            print(f"メールが送信されました: {subject}")
    except Exception as e:
        print(f"メール送信中にエラーが発生しました: {e}")

# シンボルと監視条件の設定
stock_symbol = "^VIX"  # VIX指数
price_threshold = 20  # 通知を送るしきい値
interval_seconds = 3600  # データ取得間隔（1時間）

# フラグ: 現在の価格状態を追跡
price_above_threshold = False  # 初期状態（20未満）

# リアルタイム監視の設定
def monitor_stock_price():
    print(f"リアルタイム監視を1時間間隔で開始します ({stock_symbol})")
    global price_above_threshold

    while True:
        # データ取得
        try:
            data = yf.download(tickers=stock_symbol, period="1d", interval="1m", progress=False)
            latest_price = data['Close'].iloc[-1]  # 最新価格
        except Exception as e:
            print(f"データ取得中にエラーが発生しました: {e}")
            time.sleep(interval_seconds)
            continue

        # 現在の時刻と価格を表示
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] 現在の価格: {latest_price:.2f} USD")

        # 条件: 価格が20以上
        if latest_price >= price_threshold and not price_above_threshold:
            subject = f"【通知】{stock_symbol}の価格が20以上になりました！"
            body = f"現在の価格は {latest_price:.2f} USD です。ご確認ください。"
            send_email(subject, body)
            price_above_threshold = True  # フラグ更新

        # 条件: 価格が20未満
        elif latest_price < price_threshold and price_above_threshold:
            subject = f"【通知】{stock_symbol}の価格が20未満になりました！"
            body = f"現在の価格は {latest_price:.2f} USD です。ご確認ください。"
            send_email(subject, body)
            price_above_threshold = False  # フラグ更新

        # 1時間待機
        print(f"次のチェックは1時間後です...")
        time.sleep(interval_seconds)

# リアルタイム監視を開始
monitor_stock_price()

