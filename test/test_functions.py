import unittest
import pandas as pd
from data_analysis.functions import (
    download_data, load_data, calculate_moving_average,
    calculate_differential, calculate_autocorrelation, find_extrema, manual_moving_average
)

class TestTimeSeriesAnalysis(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ticker = 'AAPL'
        cls.start_date = "2023-01-01"
        cls.end_date = "2023-10-01"

        download_data(cls.ticker, cls.start_date, cls.end_date)
        cls.dataset = load_data(cls.ticker)

    def test_calculate_moving_average(self):
        dataset_with_sma = calculate_moving_average(self.dataset)
        self.assertIn('SMA_7', dataset_with_sma.columns)
        self.assertTrue(dataset_with_sma['SMA_7'].notna().sum() > 0, "Скользящее среднее не содержит не NaN значения")

    def test_calculate_differential(self):
        dataset_with_diff = calculate_differential(self.dataset)
        self.assertIn('Diff', dataset_with_diff.columns)
        self.assertIsNotNone(dataset_with_diff['Diff'].iloc[1], "Дифференциал не должен быть None")

    def test_calculate_autocorrelation(self):
        autocorr = calculate_autocorrelation(self.dataset, lag=1)
        self.assertIsInstance(autocorr, float, "Автокорреляция должна быть float значением")

    def test_find_extrema(self):
        dataset_with_extrema = find_extrema(self.dataset)
        self.assertIn('Maxima', dataset_with_extrema.columns)
        self.assertIn('Minima', dataset_with_extrema.columns)
        self.assertTrue(dataset_with_extrema['Maxima'].notna().sum() > 0 or
                        dataset_with_extrema['Minima'].notna().sum() > 0,
                        "Должен быть хотя бы один максимум или минимум")

    def test_manual_vs_library_moving_average(self):
        dataset_with_lib_sma = calculate_moving_average(self.dataset)
        dataset_with_manual_sma = manual_moving_average(self.dataset)
        differences = []
        for i in range(len(dataset_with_lib_sma)):
            lib_value = dataset_with_lib_sma['SMA_7'].iloc[i]
            manual_value = dataset_with_manual_sma['Manual_SMA_7'].iloc[i]
            if pd.notna(lib_value) and pd.notna(manual_value) and lib_value != manual_value:
                differences.append((i, lib_value, manual_value))

        self.assertEqual(len(differences), 0, f"Найдены различия в значениях скользящего среднего: {differences}")
    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()
