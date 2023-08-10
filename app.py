import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st
from forex_python.converter import CurrencyRates

currency_converter = CurrencyRates()
rate = currency_converter.get_rate('JPY', 'USD')

st.title('東証株価アプリ')

st.sidebar.write("""
# 東証株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
""")

st.sidebar.write("""
## 表示日数選択
""")

days = st.sidebar.slider('日数', 1, 20, 10)

st.write(f"""
### 過去 **{days}日間** の東証株価
""")

def get_dividends(tickers):
    dividends_data = {}
    for company in tickers.keys():
        ticker_data = yf.Ticker(tickers[company])
        dividends_data[company] = ticker_data.dividends
    return dividends_data

@st.cache_data
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        dividends_data = get_dividends(tickers)
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        ticker_info = yf.Ticker("9432.T")
        hist['Dividends'] = ticker_info.dividends.tail(2).sum()
        
        # hist['Dividends'] = dividends_data[company].sum() / rate # 配当金の合計を追加
        # hist['Dividends'] = dividends_data[company] / rate # 配当金の合計を追加
        # hist['Dividends'] = 120 # 配当金の合計を追加
        # hist['Dividends']に配当金を直接入力してもうまくいく
        hist['Close'] = hist['Close'] / rate  # 為替レートで価格を変換
        hist['test'] =  hist['Dividends'] / hist['Close'] * 100
        hist = hist[['Close', 'Dividends', 'test']]
        hist.columns = [f'{company} Price', f'{company} Dividends',f'{company} test']
        df = pd.concat([df, hist], axis=1)
    return df

try:
    st.sidebar.write("""
    ## 株価の範囲指定
    """)
    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください。',
        0.0, 50000.0, (0.0, 50000.0)
    )

    tickers = {
        # 'apple': 'AAPL',
        'NTT': 'NTTYY',
    }
    df = get_data(days, tickers)
    # companies = st.multiselect(
    # '会社名を選択してください。',
    # list(df.index),
    # [
    #     # 'google',
    #     # 'amazon',
    #     # 'apple',
    #     'NTT'
    # ])
    st.write("### 株価と配当金 (JPY)", df)

    # グラフ表示
    price_data = df[[col for col in df.columns if "Price" in col]].reset_index().rename(columns={"index": "Date"})
    price_data = price_data.melt('Date', var_name='Name', value_name='Stock Prices(JPY)')
    chart = (
        alt.Chart(price_data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
            x="Date:T",
            y=alt.Y("Stock Prices(JPY):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
            color='Name:N'
        )
    )
    st.altair_chart(chart, use_container_width=True)

except:
    st.error(
        "おっと！なにかエラーが起きているようです。"
    )
