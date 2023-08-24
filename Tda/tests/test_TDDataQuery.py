import sys
sys.path.append("D:/SRC/TD_LINETRADE")

import unittest
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from Tda.TDAAuthentication import TDAAuthentication
from Tda.TDDataQuery import TDDataQuery

class TestTDDataQuery(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load environment variables from .env file
        load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'config', '.env'))

        # Authenticate and get access token
        CLIENT_ID = os.getenv("TDA_CLIENT_ID")
        REDIRECT_URI = os.getenv("TDA_REDIRECT_URI")
        TD_ACCOUNT_ID = os.getenv("TDA_ACCOUNT_ID")
        TD_PASSWORD = os.getenv("TDA_PASSWORD")

        auth = TDAAuthentication(CLIENT_ID, REDIRECT_URI)
        
        # Check if the access token is expired or about to expire
        if auth.is_access_token_expired():
            print("Refreshing access token...")
            auth.refresh_access_token()
        else:
            print("Getting new tokens...")
            auth_code = auth.get_authentication_code(TD_ACCOUNT_ID, TD_PASSWORD)
            auth.get_tokens(auth_code)

        cls.access_token = auth.access_token

        # Initialize TDDataQuery instance with access_token and client_id
        cls.data_query = TDDataQuery(cls.access_token, CLIENT_ID)

    def test_search_instruments(self):
        result = self.data_query.search_instruments(symbol="AAPL")
        self.assertIsInstance(result, dict)  # 確保返回的是一個字典
        self.assertIn('AAPL', result.get('symbols', {}))  # 檢查字典中的內容

    def test_get_instrument_by_cusip(self):
        # Replace with a valid CUSIP for your test
        cusip = "YOUR_VALID_CUSIP"
        result = self.data_query.get_instrument_by_cusip(cusip)
        self.assertIsInstance(result, dict)

    def test_get_market_hours(self):
        markets = "EQUITY"
        result = self.data_query.get_market_hours(markets)
        self.assertIsInstance(result, dict)

    def test_get_market_hours_for_specific_market(self):
        market = "EQUITY"
        result = self.data_query.get_market_hours_for_specific_market(market)
        self.assertIsInstance(result, dict)

    def test_get_movers_for_index(self):
        index = "SPX.X"
        result = self.data_query.get_movers_for_index(index)
        self.assertIsInstance(result, dict)

    def test_get_option_chain(self):
        symbol = "AAPL"
        result = self.data_query.get_option_chain(symbol)
        self.assertIsInstance(result, dict)

    def test_get_price_history(self):
        symbol = "AAPL"
        result = self.data_query.get_price_history(symbol)
        self.assertIsInstance(result, dict)

    def test_get_quotes(self):
        symbols = ["AAPL", "MSFT"]
        result = self.data_query.get_quotes(symbols)
        self.assertIsInstance(result, dict)

    def test_get_quote(self):
        symbol = "AAPL"
        result = self.data_query.get_quote(symbol)
        self.assertIsInstance(result, dict)

if __name__ == '__main__':
    unittest.main()
