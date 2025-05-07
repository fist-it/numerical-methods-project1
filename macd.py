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
