import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 1. 下載數據 (以台積電為例)
# df = yf.download('2330.TW', start='2024-01-01')
df = yf.download('NVDA', start='2024-01-01', progress=False)

# 查看最後幾筆數據確認
print(df.tail())

# 2. 計算技術指標 (快線與慢線)
df['MA20'] = df['Close'].rolling(window=20).mean() # 短期均線
df['MA60'] = df['Close'].rolling(window=60).mean() # 長期均線

# 3. 產生交易訊號 (1=買入, -1=賣出)
# 當快線 > 慢線時，持有 (1)；反之不持有 (0)
df['Signal'] = 0
df.loc[df['MA20'] > df['MA60'], 'Signal'] = 1

# 計算訊號觸發的瞬間 (買點與賣點)
# diff() 能找出訊號從 0 變 1 (買入) 或 1 變 0 (賣出) 的時刻
df['Action'] = df['Signal'].diff()

# 4. 簡單回測：計算累積收益率
# 計算每日漲跌幅
df['Return'] = df['Close'].pct_change()
# 計算策略收益 (訊號是昨日的，所以要 shift)
df['Strategy_Return'] = df['Return'] * df['Signal'].shift(1)
# 計算累積收益
df['Cumulative_Return'] = (1 + df['Strategy_Return'].fillna(0)).cumprod()

# 5. 視覺化結果
plt.figure(figsize=(12, 6))
plt.plot(df['Close'], label='Price', alpha=0.5)
plt.plot(df['MA20'], label='MA20', color='orange')
plt.plot(df['MA60'], label='MA60', color='green')

# 標註買賣點
plt.scatter(df[df['Action'] == 1].index, df[df['Action'] == 1]['Close'], marker='^', color='red', label='Buy Signal')
plt.scatter(df[df['Action'] == -1].index, df[df['Action'] == -1]['Close'], marker='v', color='blue', label='Sell Signal')

plt.title('Nvidia Buy/Sell Signal Strategy')
plt.legend()
plt.show()

print(f"策略最終累積收益率: {df['Cumulative_Return'].iloc[-1]:.2f}")
