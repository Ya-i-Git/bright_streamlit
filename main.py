# Добавить в streamlit гит репозиторий

import yfinance as yf
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time
import io

st.title('Данные о котировках компании Apple')

start = datetime.date(2025, 1, 1)
end = datetime.date.today()
dates = pd.date_range(start, end, freq='D').date

rename_dict ={
    'Date': 'Дата',
    'Open': 'Цена открытия',
    'High': 'Максимум',
    'Low': 'Минимум',
    'Close': 'Цена закрытия',
    'Volume': 'Объем торгов'
}

with st.sidebar:
    start_date, end_date = st.select_slider(
        'Выбери даты:',
        options=dates,
        value=[dates[0], dates[-1]]
    )
    
    st.write('__________')

ticker_symbol = 'aapl'
ticker_data = yf.Ticker(ticker_symbol)
tickers = ticker_data.history(start=start_date, end=end_date)

tickers.index = tickers.index.date
tickers.index.name='Дата'
tickers.rename(columns=rename_dict, inplace=True)
tickers.drop(['Dividends', 'Stock Splits'], axis=1, inplace=True)

with st.sidebar:
    option = st.selectbox(
        'Выбери по каким данным построить график:',
        (tickers.columns)
    )

    st.write('__________')
    
st.write(tickers)

st.subheader(f'{option}:')
st.line_chart(tickers[option])

with st.sidebar:

    def make_report():
        time.sleep(1)
        return tickers[option].to_csv()

    st.download_button(
        label=f"'{option}' - cкачать отчет в csv 📕",
        data=make_report,
        file_name="report.csv",
        mime="text/csv",
    )
    
    st.write('__________')

    fig, ax = plt.subplots(dpi=500)
    ax.plot(tickers.index, tickers[option])
    ax.set_xlabel('Дата')
    ax.set_ylabel(option)
    ax.set_title(f'{option}')
    plt.xticks(rotation=45)

    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)

    st.download_button(
        label=f"'{option}' - cкачать график 📉",
        data=buf,
        file_name="report.png",
        mime="image/png"
    )