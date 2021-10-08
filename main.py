# Raw Package
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#Data Source
import yfinance as yf


def SMA(array, period):
    return array.rolling(period).mean()

def main():
        
    # Get Bitcoin data
    data = yf.download(tickers='BTC-USD', period = '1y', interval = '60m')
    data['SMA20'] = SMA(data.Close, 20) # media mobile a 20 periodi
    data['SMA200'] = SMA(data.Close, 200) # media movile a 200 periodi
    data["DeltaPerc"] = data.Close.pct_change() # variazion percentuale tra chiusura corrente e precedente
    data["BuyHold"] = (data.DeltaPerc + 1).cumprod() * 100  # cumulata variazioni percentuali da inizio serie  
    
    data["Position"] = np.where((data.SMA20 > data.SMA200),1,0) # aggiunge posizione dove SMA20 è maggiore di SMA200 - trend rialzista... va aggiunta anche la linea successiva dato che possiamo operare solo il giorno dopo
    data.Position = data.Position.shift(1)

    data["StrategyPercentage"] = data.DeltaPerc * data.Position # variazione % puntuale filtrata da Poisition per indicare quando operare o rimanere flat
    data["Strategy"] = (data.StrategyPercentage + 1).cumprod() *100#

    Statistics = pd.DataFrame(data.BuyHold.diff().resample("A").sum())#variazione percentuale cumulata per ciasun anno "A"
    Statistics["Strategy"] = pd.DataFrame(data.Strategy.diff().resample("A").sum())

    print(Statistics)

    plt.figure(figsize=(8,4), dpi=100)
    plt.plot(data.BuyHold, color='red', linewidth=1.0)
    plt.plot(data.Strategy, color='green', linewidth=1.0)
    plt.xlabel("Tempo")
    plt.ylabel("Prezzi")
    plt.title("Buy&Hold vs Strategy")
    plt.grid(True)
    plt.legend()
    plt.show()



    data.dropna(inplace = True)
    print(data)
    #print(data.tail(10))

if __name__ == "__main__":
    main()