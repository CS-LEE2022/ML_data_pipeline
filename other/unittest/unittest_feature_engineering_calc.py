import unittest
import pandas as pd


class TestFeatureEngineering(unittest.TestCase):

    # Three test cases for volumn moving average: 
    # If the first, last, and NA values from the calculated results are correct
    def test_vol_moving_avg_calc_first(self):
        result = pd.read_parquet(f'./data/UNT_processed_feature_engineering.parquet')
        first_vol_ma = result['vol_moving_avg'].iloc[29]
        expected_value = 40060
        self.assertEqual(round(first_vol_ma, 2), expected_value)

    def test_vol_moving_avg_calc_last(self):
        result = pd.read_parquet(f'./data/UNT_processed_feature_engineering.parquet')
        first_vol_ma = result['vol_moving_avg'].dropna().iloc[-1]
        expected_value = 2739676.67
        self.assertEqual(round(first_vol_ma, 2), expected_value)

    def test_vol_moving_avg_calc_is_na(self):
        result = pd.read_parquet(f'./data/UNT_processed_feature_engineering.parquet')
        last_na = result['vol_moving_avg'].iloc[28]
        self.assertTrue(pd.isna(last_na))

    # Three test cases for close price rolling median
    # If the first, last, and NA values from the calculated results are correct
    def test_adj_price_rolling_med_calc_first(self):
        result = pd.read_parquet(f'./data/UNT_processed_feature_engineering.parquet')
        first_vol_ma = result['adj_close_rolling_med'].iloc[29]
        expected_value = 7.24
        self.assertEqual(round(first_vol_ma, 2), expected_value)

    def test_adj_price_rolling_med_calc_last(self):
        result = pd.read_parquet(f'./data/UNT_processed_feature_engineering.parquet')
        first_vol_ma = result['adj_close_rolling_med'].dropna().iloc[-1]
        expected_value = 0.31
        self.assertEqual(round(first_vol_ma, 2), expected_value)

    def test_adj_price_rolling_med_calc_is_na(self):
        result = pd.read_parquet(f'./data/UNT_processed_feature_engineering.parquet')
        last_na = result['adj_close_rolling_med'].iloc[28]
        self.assertTrue(pd.isna(last_na))


if __name__ == '__main__':
	
	unittest.main()