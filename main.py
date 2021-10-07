# Raw Package
import numpy as np
import pandas as pd

#Data Source
import yfinance as yf


def SMA(array, period):
    return array.rolling(period).mean()

def main():
        
    # Get Bitcoin data
    data = yf.download(tickers='BTC-USD', period = '1y', interval = '1h')
    data['SMA20'] = SMA(data.Close, 20)
    data['SMA200'] = SMA(data.Close, 200)
    

    print(data.tail(10))

if __name__ == "__main__":
    main()