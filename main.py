import pandas as pd
import matplotlib.pyplot as plt


def ema(period, data):
    result = data.copy()
    alpha = 2 / (period + 1)

    for i in range(len(data)):
        ema_value = 0

        if i < period:
            for j in range(i + 1):
                ema_value += data.iloc[i - j] * (1 - alpha) ** j
        else:
            for j in range(period):
                ema_value += data.iloc[i - j] * (1 - alpha) ** j

        result.iloc[i] = ema_value / sum((1 - alpha) ** k for k in range(min(i + 1, period)))

    return result


def calculations(data):
    # Określ okres dla EMA12 i EMA26

    # EMA12
    ema12 = ema(12, data['Close'])

    # EMA26
    ema26 = ema(26, data['Close'])

    macd = ema12 - ema26

    signal_line = ema(9, macd)

    return macd, signal_line


def calculate_buy_sell_points(macd, signal_line):
    buy = [0]
    sell = [0]

    for i in range(1, len(macd)):
        if macd.iloc[i] <= signal_line.iloc[i] and macd.iloc[i - 1] > signal_line.iloc[i - 1]:
            sell.append(1)
            buy.append(0)
        elif macd.iloc[i] >= signal_line.iloc[i] and macd.iloc[i - 1] < signal_line.iloc[i - 1]:
            buy.append(-1)
            sell.append(0)
        else:
            buy.append(0)
            sell.append(0)

    return buy, sell


def calculate_portfolio_values(data, macd, signal, starting_stock_amount=1000):
    buy, sell = calculate_buy_sell_points(macd, signal)

    portfolio_value = data['Close'].copy()

    initial_stock_amount = starting_stock_amount
    initial_money = 0
    portfolio_value.iloc[0] = initial_stock_amount * data['Close'].iloc[0]
    counter = 0

    print("Poczatkowa wartosc portfela: ", round(portfolio_value.iloc[0], 2), ",liczba akcji: ", initial_stock_amount,
          ",cena za jedna akcje: ", round(data['Close'].iloc[0], 2))

    for i in range(len(portfolio_value)):
        current_money = initial_money + initial_stock_amount * data['Close'].iloc[i]
        portfolio_value.iloc[i] = current_money

        if sell[i] == 1:
            initial_money += initial_stock_amount * data['Close'].iloc[i]
            initial_stock_amount = 0
            counter += 1

        if buy[i] == -1:
            stock_bought = initial_money / data['Close'].iloc[i]
            initial_money -= stock_bought * data['Close'].iloc[i]
            initial_stock_amount += stock_bought
            counter += 1

    print("Portfel: ", round(portfolio_value.iloc[-1], 2), ",liczba akcji: ", round(initial_stock_amount, 2),
          ",cena za jedna akcje: ", round(data['Close'].iloc[-1], 2))
    print('\n')
    return portfolio_value


print('\n')

data_1000days = pd.read_csv("DaneApple2020_2024.csv")[0:1000]

data_last30days = data_1000days.iloc[970:1000]

data_first30days = data_1000days[0:30]

MACD_1000days, SIGNAL_LINE_1000days = calculations(data_1000days)
MACD_last30days, SIGNAL_LINE_last30days = calculations(data_last30days)
MACD_first30days, SIGNAL_LINE_first30days = calculations(data_first30days)

data_1000days['Date'] = pd.to_datetime(data_1000days['Date'])
data_1000days.set_index('Date', inplace=True)

plt.figure(figsize=(14, 7))
plt.title("Wykres notowań Apple Inc. (AAPL)")
plt.plot(data_1000days.index, data_1000days['Close'], label='Cena zamknięcia', color='blue')
plt.xlabel('Data')
plt.ylabel('Cena')
plt.legend()
plt.grid()

plt.show()

plt.figure(figsize=(14, 7))
plt.title("Wykres wskaźnika MACD i linii sygnałowej")
plt.plot(MACD_1000days, label='MACD')
plt.plot(SIGNAL_LINE_1000days, label='SIGNAL_LINE')
plt.xlabel('Dzień')
plt.ylabel('Wartość')
plt.legend()
plt.grid()
plt.savefig('MACD_SIGNAL.png')

portfolio_1000days = calculate_portfolio_values(data_1000days, MACD_1000days, SIGNAL_LINE_1000days)

plt.figure(figsize=(14, 7))
plt.subplot(2, 1, 1)
plt.title("Wykres wskaźnika MACD i linii sygnałowej")
plt.plot(MACD_1000days, label='MACD')
plt.plot(SIGNAL_LINE_1000days, label='SIGNAL_LINE')
plt.xlabel('Dzień')
plt.ylabel('Wartość')
plt.legend()
plt.grid()

plt.subplot(2, 1, 2)
plt.title('Portfolio Value for the 1000 days')
plt.plot(data_1000days.index, portfolio_1000days, label='Portfolio value', color='blue')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig('portfolio_1000.png')
plt.show()

portfolio_last30days = calculate_portfolio_values(data_last30days, MACD_last30days, SIGNAL_LINE_last30days)

plt.figure(figsize=(14, 7))
plt.subplot(2, 1, 1)
plt.title("Wykres wskaźnika MACD i linii sygnałowej")
plt.plot(MACD_last30days, label='MACD')
plt.plot(SIGNAL_LINE_last30days, label='SIGNAL_LINE')
plt.xlabel('Dzień')
plt.ylabel('Wartość')
plt.legend()
plt.grid()

plt.subplot(2, 1, 2)
plt.title('Portfolio Value for the 1000 days')
plt.plot(data_last30days.index, portfolio_last30days, label='Portfolio value', color='blue')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig('portfolio_last30.png')
plt.show()

portfolio_first30days = calculate_portfolio_values(data_first30days, MACD_first30days, SIGNAL_LINE_first30days)

plt.figure(figsize=(14, 7))
plt.subplot(2, 1, 1)
plt.title("Wykres wskaźnika MACD i linii sygnałowej")
plt.plot(data_first30days.index, MACD_first30days, label='MACD')
plt.plot(data_first30days.index, SIGNAL_LINE_first30days, label='SIGNAL_LINE')
plt.xlabel('Dzień')
plt.ylabel('Wartość')
plt.legend()
plt.grid()

plt.subplot(2, 1, 2)
plt.title('Portfolio Value for the 30 days')
plt.plot(data_first30days.index, portfolio_first30days, label='Portfolio value', color='blue')
plt.xlabel('Date')
plt.ylabel('Value')
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig('portfolio_first30.png')
plt.show()
