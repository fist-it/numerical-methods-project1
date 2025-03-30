import pandas as pd
import matplotlib.pyplot as plt


def EMAproper(data, period, starting_point=24):
    if len(data) > 0:
        ema = [None] * (starting_point-1)
        ema.append(data.iloc[0:starting_point].mean())
        multiplier = 2 / (period + 1)
        for i in range(starting_point, len(data)):
            ema.append(data.iloc[i] * multiplier +
                       ema[i - 1] * (1 - multiplier))
        return ema


def EMAnoskip(data, period):
    if len(data) > 0:
        ema = [data.iloc[0]]
        multiplier = 2 / (period + 1)
        for i in range(1, len(data)):
            ema.append(data.iloc[i] * multiplier +
                       ema[i - 1] * (1 - multiplier))
        return ema


def calculateEmaReference(data, period):
    return data.ewm(span=period, adjust=False).mean()


def getMACD(data, period1, period2, period_signal=9):
    data['EMA12'] = EMAproper(data['Close'], period1)
    data['EMA26'] = EMAproper(data['Close'], period2)
    data['MACD'] = data['EMA12'] - data['EMA26']
    data['SIGNAL'] = EMAproper(data['MACD'], period_signal)
    return data


def getFalseMACD(data, period1, period2, period_signal=9):
    data['EMA12'] = EMAnoskip(data['Close'], period1)
    data['EMA26'] = EMAnoskip(data['Close'], period2)
    data['MACD'] = data['EMA12'] - data['EMA26']
    data['SIGNAL'] = EMAnoskip(data['MACD'], period_signal)
    return data


def find_crossovers(data):
    buy_signals = []
    sell_signals = []

    for i in range(1, len(data)):
        if (data['MACD'].iloc[i - 1] < data['SIGNAL'].iloc[i - 1] and
                data['MACD'].iloc[i] > data['SIGNAL'].iloc[i]):
            buy_signals.append(
                (data.index[i], data['MACD'].iloc[i],
                 data['Close'].iloc[i]))

        elif (data['MACD'].iloc[i - 1] > data['SIGNAL'].iloc[i - 1] and
              data['MACD'].iloc[i] < data['SIGNAL'].iloc[i]):
            # Sygnał sprzedaży
            sell_signals.append(
                (data.index[i], data['MACD'].iloc[i],
                 data['Close'].iloc[i]))

    return buy_signals, sell_signals


def simulate_trading(data, initial_balance=1000):
    balance = initial_balance  # Gotówka w walucie (np. USD)
    asset_holdings = 0  # Liczba posiadanych aktywów (np. BTC)
    transactions = []  # Lista przechowująca historię transakcji

    prev_macd = data['MACD'].iloc[0]
    prev_signal = data['SIGNAL'].iloc[0]

    for i in range(1, len(data)):
        macd = data['MACD'].iloc[i]
        signal = data['SIGNAL'].iloc[i]
        price = data['Close'].iloc[i]

        # KUPNO - jeśli MACD przecina SIGNAL od dołu
        if prev_macd < prev_signal and macd > signal and balance > 0:
            asset_holdings = balance / price  # Kupujemy maksymalnie ile się da
            balance = 0
            transactions.append((data.index[i], 'BUY', price, asset_holdings,
                                 balance))

        # SPRZEDAŻ - jeśli MACD przecina SIGNAL od góry
        elif prev_macd > prev_signal and macd < signal and asset_holdings > 0:
            balance = asset_holdings * price  # Sprzedajemy wszystko
            asset_holdings = 0
            transactions.append(
                (data.index[i], 'SELL', price, asset_holdings, balance))

        prev_macd = macd
        prev_signal = signal

    # Obliczamy końcowy wynik
    # Wartość gotówki + posiadanych aktywów
    final_value = balance + (asset_holdings * data['Close'].iloc[-1])
    return transactions, final_value


def plot_MACD(data, buy_signals, sell_signals, output_filename):
    plt.figure(figsize=(12, 6))
    plt.xticks(rotation=45)
    # Wykres MACD
    plt.plot(data.index, data['MACD'], label='MACD',
             linewidth=1.5)
    plt.plot(data.index, data['SIGNAL'], label='SIGNAL',
             linestyle='dashed', linewidth=1.5)  # Neonowy fiolet

    if buy_signals:
        buy_dates, buy_macd_values, buy_values = zip(*buy_signals)
        plt.scatter(buy_dates, buy_macd_values, color='green',
                    label='Kupno', marker='^', s=100)

    if sell_signals:
        sell_dates, sell_macd_values, sell_values = zip(*sell_signals)
        plt.scatter(sell_dates, sell_macd_values, color='red',
                    label='Sprzedaż', marker='v', s=100)

    plt.title('MACD')
    plt.xlabel('Data')
    plt.ylabel('Wartość')
    plt.legend(loc='upper left')

    plt.tight_layout()
    plt.savefig("./figures/"+output_filename)  # Zapisz wykres w formacie PNG
    plt.show()
    plt.close('all')


def plot_buy_sell_close(data, buy_signals, sell_signals, output_filename):
    plt.figure(figsize=(12, 6))
    plt.xticks(rotation=45)
    # Wykres MACD
    plt.plot(data.index, data['Close'], label='Cena zamkniecia',
             color="gray", linewidth=1.5)

    if buy_signals:
        buy_dates, buy_macd_values, buy_values = zip(*buy_signals)
        plt.scatter(buy_dates, buy_values, color='green',
                    label='Kupno', marker='^', s=100)

    if sell_signals:
        sell_dates, sell_macd_values, sell_values = zip(*sell_signals)
        plt.scatter(sell_dates, sell_values, color='red',
                    label='Sprzedaż', marker='v', s=100)

    plt.title('Sygnały kupna i sprzedaży')
    plt.xlabel('Data')
    plt.ylabel('Cena')
    plt.legend(loc='upper left')

    plt.tight_layout()
    plt.savefig("./figures/"+output_filename)  # Zapisz wykres w formacie PNG
    plt.show()
    plt.close('all')


def main():

    # BTC data {{{
    dataBtc = pd.read_csv('./data/btd-2021-2024.csv',
                          parse_dates=['Date'], index_col='Date')
    dataBtc = getMACD(dataBtc, 12, 26, 9)

    buy_signals, sell_signals = find_crossovers(dataBtc)
    transactions, final_balance = simulate_trading(dataBtc, 1000)
    print(f"\nFinal balance with proper EMA starting values: {
          final_balance:.2f} (Start: 1000.00)")

    transactions_df = pd.DataFrame(transactions, columns=[
        'Date', 'Type', 'Price', 'Assets', 'Balance'])
    transactions_df.to_csv('./data/transactionsBtc.csv')

    plot_MACD(dataBtc, buy_signals, sell_signals, 'BTCmacd.png')
    plot_buy_sell_close(dataBtc, buy_signals, sell_signals, 'BTCbuy_sell.png')

    # simulating trading with bad starting values {{{
    falseDataBtc = pd.read_csv('./data/btd-2021-2024.csv',
                               parse_dates=['Date'], index_col='Date')
    falseDataBtc = getFalseMACD(falseDataBtc, 12, 26, 9)
    bad_transactions, bad_final_balance = simulate_trading(falseDataBtc, 1000)
    print(f"\nFinal balance with improper EMA starting values: {
          bad_final_balance:.2f} (Start: 1000.00)")
    # }}}

    # }}}

    # Subset of BTC data {{{
    start_date = '2023-05-15'
    end_date = '2023-06-20'
    subset_data = dataBtc.loc[start_date:end_date]
    subset_data.to_csv('./data/macd_subset.csv')

    buy_signals, sell_signals = find_crossovers(subset_data)

    subsetTransactions, subsetResult = simulate_trading(subset_data, 1000)
    print(f"\nFinal balance for subset: {subsetResult:.2f} (Start: 1000.00)")

    plot_MACD(subset_data, buy_signals, sell_signals, 'BTCmacd_subset.png')
    plot_buy_sell_close(subset_data, buy_signals, sell_signals,
                        'BTCbuy_sell_subset.png')
    # }}}

    # NVDA data {{{
    dataNvda = pd.read_csv('./data/nvda-2020-2024.csv',
                           parse_dates=['Date'], index_col='Date')
    dataNvda = getMACD(dataNvda, 12, 26)

    buy_signals, sell_signals = find_crossovers(dataNvda)
    nvdaTrades, nvdaResult = simulate_trading(dataNvda, 1000)

    transactions_df = pd.DataFrame(nvdaTrades, columns=[
        'Date', 'Type', 'Price', 'Assets', 'Balance'])
    transactions_df.to_csv('./data/transactionsNVDA.csv')
    print(f"\nFinal balance: {nvdaResult:.2f} (Start: 1000.00)")

    plot_MACD(dataNvda, buy_signals, sell_signals, 'NVDAmacd.png')
    plot_buy_sell_close(dataNvda, buy_signals,
                        sell_signals, 'NVDAbuy_sell.png')
    # }}}


if __name__ == '__main__':
    main()
