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
