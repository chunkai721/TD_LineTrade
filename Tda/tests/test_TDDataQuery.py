import unittest
import os
from dotenv import load_dotenv
from CK_td.TDAAuthentication import TDAAuthentication
from CK_td.TDDataQuery import TDDataQuery

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
        REFRESH_TOKEN = os.getenv("TDA_REFRESH_TOKEN")

        auth = TDAAuthentication(CLIENT_ID, REDIRECT_URI)

        # If we have a refresh token, use it to get a new access token
        if REFRESH_TOKEN:
            tokens = auth.refresh_tokens(REFRESH_TOKEN)
        else:
            auth_code = auth.get_authentication_code(TD_ACCOUNT_ID, TD_PASSWORD)
            tokens = auth.get_tokens(auth_code)
            # Save the refresh token to .env
            with open(os.path.join(os.path.dirname(__file__), '..', 'config', '.env'), 'a') as f:
                f.write(f"\nTDA_REFRESH_TOKEN={tokens['refresh_token']}\n")

        cls.access_token = tokens['access_token']

        # Initialize TDDataQuery instance
        cls.data_query = TDDataQuery(cls.access_token)

    def test_search_instruments(self):
        result = self.data_query.search_instruments(searchText="AAPL")
        self.assertIn('AAPL', result)

    # Add more tests for other methods in TDDataQuery class...

if __name__ == '__main__':
    unittest.main()
