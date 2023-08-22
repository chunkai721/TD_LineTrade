import os
from dotenv import load_dotenv
from Tda.TDAAuthentication import TDAAuthentication

class TestTDAAuthentication:
    def __init__(self, client_id, redirect_uri, td_account_id, td_password):
        self.auth = TDAAuthentication(client_id, redirect_uri)
        self.td_account_id = td_account_id
        self.td_password = td_password

    def test_get_authentication_url(self):
        print("Testing get_authentication_url()...")
        url = self.auth.get_authentication_url()
        print(f"Authentication URL: {url}\n")
        assert "https://auth.tdameritrade.com/auth" in url

    def test_get_authentication_code(self):
        print("\nTesting get_authentication_code()...")
        self.auth_code = self.auth.get_authentication_code(self.td_account_id, self.td_password)
        print("Authentication Code:", self.auth_code)
        assert self.auth_code is not None, "Failed to retrieve authentication code"


    def test_get_tokens(self):
        print("\nTesting get_tokens()...\n")
        self.auth.get_tokens(self.auth_code)
        print("Access Token:", self.auth.access_token)
        print("Refresh Token:", self.auth.refresh_token)
        # Add the assertion here
        assert self.auth.access_token is not None, "Failed to retrieve access token"


    def test_refresh_access_token(self):
        print("Testing refresh_access_token()...")
        self.auth.refresh_access_token()
        print(f"Refreshed Access Token: {self.auth.access_token}\n")
        assert self.auth.access_token is not None

    def test_refresh_all_tokens(self):
        print("Testing refresh_all_tokens()...")
        self.auth.refresh_all_tokens()
        print(f"Refreshed Access Token: {self.auth.access_token}")
        print(f"Refreshed Refresh Token: {self.auth.refresh_token}\n")
        assert self.auth.access_token is not None
        assert self.auth.refresh_token is not None

    def run_tests(self):
        self.test_get_authentication_url()
        self.test_get_authentication_code()
        self.test_get_tokens()
        self.test_refresh_access_token()
        self.test_refresh_all_tokens()
        print("All tests passed!")

# 使用以下方式運行測試
if __name__ == "__main__":
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'config', '.env'))

    CLIENT_ID = os.environ.get("TDA_CLIENT_ID")
    REDIRECT_URI = os.environ.get("TDA_REDIRECT_URI")
    TD_ACCOUNT_ID = os.environ.get("TDA_ACCOUNT_ID")
    TD_PASSWORD = os.environ.get("TDA_PASSWORD")

    tester = TestTDAAuthentication(CLIENT_ID, REDIRECT_URI, TD_ACCOUNT_ID, TD_PASSWORD)
    tester.run_tests()
