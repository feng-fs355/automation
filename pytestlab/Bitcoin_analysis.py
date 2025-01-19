import pandas as pd
import requests
import matplotlib.pyplot as plt

# 從 CoinGecko API 獲取歷史價格數據
def fetch_historical_data(crypto_id, vs_currency, days):
    """
    從 CoinGecko 獲取加密貨幣的歷史價格數據。
    :param crypto_id: 加密貨幣名稱 (如 "dogecoin", "tether")
    :param vs_currency: 對應法幣 (如 "usd")
    :param days: 查詢的天數 (如 30)
    """
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
    params = {"vs_currency": vs_currency, "days": days}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return pd.DataFrame({
        "timestamp": [x[0] for x in data["prices"]],
        "price": [x[1] for x in data["prices"]]
    })

# 繪製價格趨勢圖
def plot_price_trend(data, crypto_id, save_path="price_trend.png"):
    """
    繪製價格趨勢圖，並保存為圖片。
    :param data: 處理後的數據框
    :param crypto_id: 加密貨幣名稱 (如 "dogecoin", "tether")
    :param save_path: 圖片保存路徑
    """
    plt.figure(figsize=(10, 6))
    plt.plot(data["formatted_datetime"], data["price"], label=f"{crypto_id.capitalize()} Price (USD)", marker='o')
    plt.title(f"{crypto_id.capitalize()} Price Trend", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Price (USD)", fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(save_path)  # 儲存圖片
    print(f"價格趨勢圖已保存到 {save_path}")
    plt.show()

# 基於技術指標的買點評估
def evaluate_buy_signals(data):
    """
    基於技術指標 (SMA 和 RSI) 評估買點。
    :param data: 數據框，包含價格數據
    """
    # 計算移動平均線
    data["SMA_10"] = data["price"].rolling(window=10).mean()
    data["SMA_20"] = data["price"].rolling(window=20).mean()

    # 計算 RSI
    def compute_rsi(data, window=14):
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    data["RSI"] = compute_rsi(data["price"])

    # 確定買點（SMA 黃金交叉 & RSI 超賣）
    buy_signals = data[
        (data["SMA_10"] > data["SMA_20"]) & (data["SMA_10"].shift(1) <= data["SMA_20"].shift(1)) & (data["RSI"] < 30)
    ]
    print(f"發現 {len(buy_signals)} 個買點：")
    print(buy_signals[["formatted_datetime", "price", "SMA_10", "SMA_20", "RSI"]])

    return buy_signals

# 主邏輯
def main():
    # 支持的加密貨幣
    crypto_ids = ["dogecoin", "tether"]  # 支持狗狗幣和泰達幣
    vs_currency = "usd"  # 貨幣對

    # 自定義日期範圍
    print("輸入查詢的日期範圍：")
    days = input("請輸入查詢天數（默認 30）：")
    if not days.isdigit():
        days = 30  # 默認查詢 30 天
    else:
        days = int(days)

    for crypto_id in crypto_ids:
        csv_file = f"{crypto_id}_prices.csv"  # CSV 檔案名稱
        trend_chart = f"{crypto_id}_price_trend.png"  # 趨勢圖檔案名稱

        # 獲取歷史價格數據
        print(f"正在查詢 {crypto_id.capitalize()} 的價格數據...")
        data = fetch_historical_data(crypto_id, vs_currency, days)

        # 將 timestamp 轉換為日期時間格式
        data["formatted_datetime"] = pd.to_datetime(data["timestamp"], unit="ms").dt.strftime("%Y-%m-%d %H:%M")

        # 刪除 timestamp 欄位
        data = data.drop(columns=["timestamp"])

        # 匯出 CSV 檔案
        data.to_csv(csv_file, index=False)
        print(f"{crypto_id.capitalize()} 數據已匯出到 {csv_file}")

        # 繪製價格趨勢圖
        plot_price_trend(data, crypto_id, save_path=trend_chart)

        # 評估買點
        buy_signals = evaluate_buy_signals(data)

        # 匯出買點數據
        if not buy_signals.empty:
            buy_signals_file = f"{crypto_id}_buy_signals.csv"
            buy_signals.to_csv(buy_signals_file, index=False)
            print(f"買點數據已匯出到 {buy_signals_file}")

# 執行主邏輯
if __name__ == "__main__":
    main()
