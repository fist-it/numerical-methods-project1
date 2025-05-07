import pandas as pd
from analysis import *
from macd import *
from plotting import *
from simulation import *


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
    print(f"\nFinal balance for bad subset: {
          subsetResult:.2f} (Start: 1000.00)")

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
    print(f"\nFinal balance for saved subset: {
          subsetResult:.2f} (Start: 1000.00)")

    plot_MACD(subset_data, buy_signals, sell_signals,
              'BTCmacd_subset_saved.png', "Wykres MACD i SIGNAL dla Bitcoina 17.04.2022 - 16.07.2022")
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
    print(f"\nFinal balance for good subset: {
          subsetResult:.2f} (Start: 1000.00)")

    plot_MACD(subset_data, buy_signals, sell_signals,
              'BTCmacd_subset_good.png', "Wykres MACD i SIGNAL dla Bitcoina 27.01.2021 - 24.03.2021")
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

    plot_MACD(dataNvda, buy_signals, sell_signals, 'NVDAmacd.png',
              "Wykres MACD i SIGNAL dla NVDA 2020-06-29 - 03.12.2024")
    plot_buy_sell_close(dataNvda, buy_signals,
                        sell_signals, 'NVDAbuy_sell.png',
                        "Wykres sygnałów kupna i sprzedaży dla NVDA 2020-06-29 - 03.12.2024")
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
