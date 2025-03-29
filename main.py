import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def calculateEma(data, period):
    if len(data) > 0:
        ema = [data[0]]
        multiplier = 2 / (period + 1)
        for i in range(1, len(data)):
            ema.append(data[i] * multiplier + ema[i - 1] * (1 - multiplier))
        return ema


def calculateEmaReference(data, period):
    return data.ewm(span=period, adjust=False).mean()


def main():
    # 1. Wczytanie danych z pliku CSV
    data = pd.read_csv('btd-2014-2024.csv',
                       parse_dates=['Date'], index_col='Date')

    # 3. Obliczanie MACD (EMA12 - EMA26)
    data['EMA12'] = calculateEma(data['Close'], 12)
    data['EMA26'] = calculateEma(data['Close'], 26)
    data['MACD'] = data['EMA12'] - data['EMA26']

    # MACD reference from pandas
    data['EMA12_ref'] = calculateEmaReference(data['Close'], 12)
    data['EMA26_ref'] = calculateEmaReference(data['Close'], 26)
    data['MACD_ref'] = data['EMA12_ref'] - data['EMA26_ref']

    data['SIGNAL'] = calculateEma(data['MACD'], 9)

    # SIGNAL reference from pandas
    data['SIGNAL_ref'] = calculateEmaReference(data['MACD'], 9)

    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    # Wykres MACD
    plt.plot(data.index, data['MACD'], label='MACD', color='blue')
    plt.plot(data.index, data['SIGNAL'], label='SIGNAL', color='red')

    # MACD reference from pandas
    # plt.plot(data.index, data['MACD_ref'], label='MACD_ref', color='green')
    plt.title('MACD')
    plt.xlabel('Data')
    plt.ylabel('Wartość')
    plt.legend(loc='upper left')

    # reference from pandas
    plt.subplot(2, 1, 2)
    plt.plot(data.index, data['MACD'] - data['MACD_ref'],
             label='MACD - MACD_ref', color='blue')
    plt.plot(data.index, data['SIGNAL'] - data['SIGNAL_ref'],
             label='SIGNAL - SIGNAL_ref', color='green')

    # Zapisz wykres do pliku PNG
    plt.savefig('macd_signal_plot.png')  # Zapisz wykres w formacie PNG
    plt.tight_layout()


if __name__ == '__main__':
    main()
