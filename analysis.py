import matplotlib.pyplot as plt
import pandas as pd


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
