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

        # Initialize TDDataQuery instance
        cls.data_query = TDDataQuery(cls.access_token)

    def test_search_instruments(self):
        result = self.data_query.search_instruments(searchText="AAPL")
        self.assertIsInstance(result, dict)  # 確保返回的是一個字典
        self.assertIn('AAPL', result.get('symbols', {}))  # 檢查字典中的內容

    # Add more tests for other methods in TDDataQuery class...

if __name__ == '__main__':
    unittest.main()
