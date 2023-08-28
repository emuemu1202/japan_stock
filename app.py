import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st
from forex_python.converter import CurrencyRates

# 円/ドルの為替レート取得
currency_converter = CurrencyRates()
rate = currency_converter.get_rate('JPY', 'USD')

# タイトル
st.title('東証株価アプリ')

st.sidebar.write("""
# 東証株価
表示日数を指定できます。
""")

st.sidebar.write("""
## 表示日数選択
""")

days = st.sidebar.slider('日数', 1, 20, 10)

st.write(f"""
### 過去 **{days}日間** の東証株価
""")

@st.cache_data
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        ticker_info = yf.Ticker("9432.T")
        hist['Close'] = round(hist['Close'] / rate)  # 為替レートで価格を変換
        hist['Dividends'] = ticker_info.dividends.tail(2).sum()
        hist['dividend_yield'] =  round(hist['Dividends'] / hist['Close'] * 100,2)
        hist = hist[['Close', 'Dividends', 'dividend_yield']]
        hist.columns = ['株価', '配当金','配当利回り(%))']
        df = pd.concat([df, hist], axis=1)
    return df

try:
    st.sidebar.write("""
    ## 株価の範囲指定
    """)
    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください。',
        0, 10000, (0, 10000)
    )

    tickers = {
        'NTT': 'NTTYY',
    }
    df = get_data(days, tickers)
    st.write("### 株価と配当金 (円)", df)

    # グラフ表示
    price_data = df[[col for col in df.columns if "株価" in col]].reset_index().rename(columns={"index": "日付"})
    price_data = price_data.melt('日付', var_name='チャート名', value_name='株価(日本円)')
    chart = (
        alt.Chart(price_data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
            x="Date:T",
            y=alt.Y("株価(日本円):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
            color='チャート名:N'
        )
    )
    st.altair_chart(chart, use_container_width=True)

except Exception as e:
    st.error(
        e
    )
