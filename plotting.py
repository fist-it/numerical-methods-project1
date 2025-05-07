import matplotlib.pyplot as plt


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
