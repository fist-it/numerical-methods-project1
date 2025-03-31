import pandas as pd
import matplotlib.pyplot as plt


# MACD/SIGNAL/EMA functions {{{
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

# }}}

# Trading simulation {{{


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
# }}}

# plotting functions {{{


def plot_MACD(data, buy_signals, sell_signals, output_filename, plot_title):
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

    plt.title(plot_title)
    plt.xlabel('Data')
    plt.ylabel('Wartość')
    plt.legend(loc='upper left')

    plt.tight_layout()
    # Zapisz wykres w formacie PNG
    plt.savefig("./figures/"+output_filename, dpi=300)
    # plt.show()
    plt.close('all')


def plot_buy_sell_close(data, buy_signals, sell_signals, output_filename,
                        plot_title):
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

    plt.title(plot_title)
    plt.xlabel('Data')
    plt.ylabel('Cena')
    plt.legend(loc='upper left')

    plt.tight_layout()
    # Zapisz wykres w formacie PNG
    plt.savefig("./figures/"+output_filename, dpi=300)
    # plt.show()
    plt.close('all')
# }}}

# Trade analysis {{{


def analyze_trades(buy_signals, sell_signals):
    good_trades = 0
    for i in range(len(buy_signals)):
        if buy_signals[i][2] < sell_signals[i][2]:
            good_trades += 1

    return good_trades


# Plot BUY/SELL results
def plot_transaction_result(transactions_data_path, output_filename, plot_title, starting_balance=1000):
    transactions = pd.read_csv(transactions_data_path, parse_dates=['Date'],
                               index_col='Date')
    sell_transactions = transactions[transactions['Type'] == 'SELL']
    plt.figure(figsize=(12, 6))
    plt.xticks(rotation=45)
    plt.plot(sell_transactions.index, sell_transactions['Balance'],
             label='Saldo')

    # starting balance line
    plt.plot(sell_transactions.index, [starting_balance] *
             len(sell_transactions), label='Saldo początkowe',
             linestyle='dashed')
    plt.title(plot_title)
    plt.xlabel('Data')
    plt.ylabel('Saldo')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(output_filename, dpi=300)
    # plt.show()
    plt.close('all')
# }}}


def main():

    # BTC data {{{
    dataBtc = pd.read_csv('./data/btd-2021-2024.csv',
                          parse_dates=['Date'], index_col='Date')
    dataBtc = getMACD(dataBtc, 12, 26, 9)

    buy_signals, sell_signals = find_crossovers(dataBtc)

    transactions, final_balance = simulate_trading(dataBtc, 1000)
    print(f"\nFinal balance with proper EMA starting values: {
          final_balance:.2f} (Start: 1000.00)")

    good_trades_btc = analyze_trades(buy_signals, sell_signals)
    print(f"Number of good trades (buy and sell) in BTC: {good_trades_btc}")
    print(f"Number of trades in BTC: {len(buy_signals)}")

    transactions_df = pd.DataFrame(transactions, columns=[
        'Date', 'Type', 'Price', 'Assets', 'Balance'])
    transactions_df.to_csv('./data/transactionsBtc.csv')


    plot_MACD(dataBtc, buy_signals, sell_signals,
              'BTCmacd.png', "Wykres MACD i SIGNAL dla Bitcoina 1.01.2021 - 19.01.2024")

    plot_buy_sell_close(dataBtc, buy_signals, sell_signals, 'BTCbuy_sell.png',
                        "Wykres sygnałów kupna i sprzedaży dla Bitcoina 1.01.2021 - 19.01.2024")

    plot_transaction_result('./data/transactionsBtc.csv', './figures/BTCtransaction_result.png',
                            'Rezultat transakcji BTC')

    # simulating trading with bad starting values {{{
    falseDataBtc = pd.read_csv('./data/btd-2021-2024.csv',
                               parse_dates=['Date'], index_col='Date')
    falseDataBtc = getFalseMACD(falseDataBtc, 12, 26, 9)
    bad_transactions, bad_final_balance = simulate_trading(falseDataBtc, 1000)
    print(f"\nFinal balance with improper EMA starting values: {
          bad_final_balance:.2f} (Start: 1000.00)")
    # }}}

    # }}}

    # Subset with bad transaction results {{{
    start_date = '2023-05-15'
    end_date = '2023-06-20'
    subset_data = dataBtc.loc[start_date:end_date]
    subset_data.to_csv('./data/BTC_subset_bad.csv')

    buy_signals, sell_signals = find_crossovers(subset_data)

    subsetTransactions, subsetResult = simulate_trading(subset_data, 1000)
    print(f"\nFinal balance for bad subset: {subsetResult:.2f} (Start: 1000.00)")

    plot_MACD(subset_data, buy_signals, sell_signals,
              'BTCmacd_subset_bad.png', "Wykres MACD i SIGNAL dla Bitcoina 15.05.2023 - 20.06.2023")
    plot_buy_sell_close(subset_data, buy_signals, sell_signals,
                        'BTCbuy_sell_subset_bad.png',
                        'Wykres sygnałów kupna i sprzedaży dla Bitcoina 15.05.2023 - 20.06.2023')
    # }}}

    # Subset with saved potential loss {{{
    start_date = '2022-04-17'
    end_date = '2022-07-16'
    subset_data = dataBtc.loc[start_date:end_date]
    subset_data.to_csv('./data/BTC_subset_saved.csv')

    buy_signals, sell_signals = find_crossovers(subset_data)

    subsetTransactions, subsetResult = simulate_trading(subset_data, 1000)
    print(f"\nFinal balance for saved subset: {subsetResult:.2f} (Start: 1000.00)")

    plot_MACD(subset_data, buy_signals, sell_signals,
              'BTCmacd_subset_saved.png', "Bitcoin MACD graph subset")
    plot_buy_sell_close(subset_data, buy_signals, sell_signals,
                        'BTCbuy_sell_subset_saved.png',
                        'Wykres sygnałów kupna i sprzedaży dla Bitcoina 17.04.2022 - 16.07.2022')
    # }}}

    # Subset with good transaction results {{{
    start_date = '2021-01-27'
    end_date = '2021-03-24'
    subset_data = dataBtc.loc[start_date:end_date]
    subset_data.to_csv('./data/BTC_subset_good.csv')

    buy_signals, sell_signals = find_crossovers(subset_data)

    subsetTransactions, subsetResult = simulate_trading(subset_data, 1000)
    print(f"\nFinal balance for good subset: {subsetResult:.2f} (Start: 1000.00)")

    plot_MACD(subset_data, buy_signals, sell_signals,
              'BTCmacd_subset_good.png', "Bitcoin MACD graph subset")
    plot_buy_sell_close(subset_data, buy_signals, sell_signals,
                        'BTCbuy_sell_subset_good.png',
                        'Wykres sygnałów kupna i sprzedaży dla Bitcoina 27.01.2021 - 24.03.2021')
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

    good_trades_nvda = analyze_trades(buy_signals, sell_signals)
    print(f"Number of good trades (buy and sell) in NVDA: {good_trades_nvda}")
    print(f"Number of trades in NVDA: {len(buy_signals)}")


    plot_MACD(dataNvda, buy_signals, sell_signals, 'NVDAmacd.png', "NVDA MACD")
    plot_buy_sell_close(dataNvda, buy_signals,
                        sell_signals, 'NVDAbuy_sell.png',
                        "NVDA buy and sell signals")
    plot_transaction_result('./data/transactionsNVDA.csv', './figures/NVDAtransaction_result.png',
                            'Rezultat transakcji NVDA')
    # }}}

    # NVDA subset data (2020-11-01 to 2021-01-12) {{{
    start_date = '2020-11-01'
    end_date = '2021-01-12'
    subset_data = dataNvda.loc[start_date:end_date]
    subset_data.to_csv('./data/NVDA_subset.csv')

    buy_signals, sell_signals = find_crossovers(subset_data)

    subsetTransactions, subsetResult = simulate_trading(subset_data, 1000)
    print(f"\nFinal balance for subset: {subsetResult:.2f} (Start: 1000.00)")

    plot_MACD(subset_data, buy_signals, sell_signals,
              'NVDAmacd_subset.png', "NVDA MACD subset")
    plot_buy_sell_close(subset_data, buy_signals, sell_signals,
                        'NVDAbuy_sell_subset.png',
                        'NVDA buy and sell signals subset')
    # }}}


if __name__ == '__main__':
    main()
