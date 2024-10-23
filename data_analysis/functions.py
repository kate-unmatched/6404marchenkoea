import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame


def download_data(ticker: str, start_date: str, end_date: str) -> DataFrame:
    data = yf.download(ticker, start=start_date, end=end_date)
    data.to_csv(f'{ticker}_data.csv')
    return data


def load_data(ticker: str) -> DataFrame:
    dataset = pd.read_csv(f'{ticker}_data.csv', index_col='Date', parse_dates=True)
    return dataset


def calculate_moving_average(dataset: DataFrame, window: int = 7) -> DataFrame:
    dataset['SMA_7'] = dataset['Close'].rolling(window=window).mean()
    return dataset


def manual_moving_average(dataset: DataFrame, window: int = 7) -> DataFrame:
    sma_values = []

    for i in range(len(dataset)):
        if i < window - 1:
            window_values = dataset['Close'][:i + 1]
            sma = sum(window_values) / window
        else:
            window_values = dataset['Close'][i - window + 1: i + 1]
            sma = sum(window_values) / window
        sma_values.append(sma)

    dataset['Manual_SMA_7'] = sma_values
    return dataset


def manual_median_filter(dataset: DataFrame, window: int = 7) -> DataFrame:
    median_values = []

    for i in range(len(dataset)):
        if i < window - 1:
            window_values = dataset['Close'][:i + 1]
            median = window_values.median()
        else:
            window_values = dataset['Close'][i - window + 1: i + 1]
            median = window_values.median()
        median_values.append(median)

    dataset['Manual_Median_7'] = median_values
    return dataset


def calculate_differential(dataset: DataFrame) -> DataFrame:
    dataset['Diff'] = dataset['Close'].diff()
    return dataset


def calculate_autocorrelation(dataset: DataFrame, lag: int = 1) -> float:
    return dataset['Close'].autocorr(lag=lag)


def find_extrema(dataset: DataFrame) -> DataFrame:
    dataset['Maxima'] = dataset['Close'][
        (dataset['Close'].shift(1) < dataset['Close']) & (dataset['Close'].shift(-1) < dataset['Close'])]
    dataset['Minima'] = dataset['Close'][
        (dataset['Close'].shift(1) > dataset['Close']) & (dataset['Close'].shift(-1) > dataset['Close'])]
    return dataset


def save_to_excel(dataset: DataFrame, operation_name: str, ticker: str) -> str:
    filename = f"{operation_name}_{ticker}_results.xlsx"
    dataset.to_excel(filename)
    return filename


def plot_data(dataset: DataFrame, ticker: str) -> None:
    plt.figure(figsize=(14, 7))
    plt.plot(dataset.index, dataset['Close'], label='Цена закрытия')
    plt.plot(dataset.index, dataset['SMA_7'], label='Скользящее среднее (7 периодов)', linestyle='--')
    plt.plot(dataset.index, dataset['Manual_SMA_7'], label='Скользящее среднее ручное', linestyle='--')
    plt.scatter(dataset.index, dataset['Maxima'], color='red', label='Максимумы', marker='^', alpha=0.7)
    plt.scatter(dataset.index, dataset['Minima'], color='blue', label='Минимумы', marker='v', alpha=0.7)
    plt.title(f'Анализ временного ряда {ticker}')
    plt.legend()
    plt.show()


def main() -> None:
    ticker = 'AAPL'
    start_date = "2023-01-01"
    end_date = "2023-10-01"

    download_data(ticker, start_date, end_date)
    dataset = load_data(ticker)

    dataset = calculate_moving_average(dataset)
    dataset = manual_moving_average(dataset)
    dataset = manual_median_filter(dataset)

    dataset = calculate_differential(dataset)

    autocorr = calculate_autocorrelation(dataset)
    print(f"Автокорреляция: {autocorr}")

    dataset = find_extrema(dataset)
    save_to_excel(dataset, 'extrema', ticker)

    # Построение графика
    plot_data(dataset, ticker)


if __name__ == "__main__":
    main()
