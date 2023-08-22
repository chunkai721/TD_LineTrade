import os
from dotenv import load_dotenv
from Tda.TDAAuthentication import TDAAuthentication
from Tda.TDAccountsAndTrading import TDAccountsAndTrading

class TestTDAccountsAndTrading:
    def __init__(self, auth):
        self.trading_api = TDAccountsAndTrading(auth.access_token)

    def test_get_account(self, account_id):
        print("測試 get_account()...")
        account = self.trading_api.get_account(account_id)
        assert account, "無法取得帳戶資訊"
        print("取得帳戶資訊成功！\n")

    def test_get_accounts(self):
        print("測試 get_accounts()...")
        accounts = self.trading_api.get_accounts()
        assert accounts, "無法取得所有帳戶資訊"
        print("取得所有帳戶資訊成功！\n")

    # 這裡可以加入其他的測試方法...

    def run_tests(self, account_id):
        self.test_get_account('635067306')
        self.test_get_accounts()
        # 這裡可以加入其他的測試方法呼叫...
        print("所有測試均已通過！")

if __name__ == "__main__":
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'config', '.env'))

    CLIENT_ID = os.environ.get("TDA_CLIENT_ID")
    REDIRECT_URI = os.environ.get("TDA_REDIRECT_URI")
    TD_ACCOUNT_ID = os.environ.get("TDA_ACCOUNT_ID")
    TD_PASSWORD = os.environ.get("TDA_PASSWORD")

    print(f"CLIENT_ID: {CLIENT_ID}")
    print(f"REDIRECT_URI: {REDIRECT_URI}")

    auth = TDAAuthentication(CLIENT_ID, REDIRECT_URI)
    auth.authenticate(TD_ACCOUNT_ID, TD_PASSWORD)  # 使用 authenticate 方法，它會自動處理 token 的取得或刷新

    tester = TestTDAccountsAndTrading(auth)
    tester.run_tests(TD_ACCOUNT_ID)
