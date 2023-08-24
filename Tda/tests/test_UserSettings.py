import os
import unittest
from dotenv import load_dotenv
from Tda.TDUserSettings import TDUserSettings
from Tda.TDAAuthentication import TDAAuthentication

# 載入環境變數
load_dotenv(os.path.join(os.path.dirname(__file__), '../config/.env'))

class TestTDUserSettings(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.auth = TDAAuthentication(os.getenv('TDA_CLIENT_ID'), os.getenv('TDA_REDIRECT_URI'))
        if cls.auth.is_access_token_expired():
            cls.auth.refresh_access_token()

    def setUp(self):
        self.access_token = os.getenv('TDA_ACCESS_TOKEN')
        self.user_settings = TDUserSettings(self.access_token)

    def test_get_account_preferences(self):
        account_id = os.getenv('TDA_ACCOUNT_ID')
        response = self.user_settings.get_account_preferences(account_id)
        self.assertIn('expressTrading', response)

    def test_get_user_principals(self):
        fields = "streamerSubscriptionKeys,streamerConnectionInfo"
        response = self.user_settings.get_user_principals(fields=fields)
        self.assertIn('streamerInfo', response)

    def test_get_streamer_subscription_keys(self):
        response = self.user_settings.get_streamer_subscription_keys()
        self.assertIn('keys', response)

    # 注意: 這個測試會修改您的帳戶設定，請在運行前確認
    def test_update_account_preferences(self):
        account_id = os.getenv('TDA_ACCOUNT_ID')
        preferences_data = {
            "expressTrading": False,
            "directOptionsRouting": False,
            "directEquityRouting": False,
            "defaultEquityOrderLegInstruction": "BUY",  # 可選: 'BUY', 'SELL', 'BUY_TO_COVER', 'SELL_SHORT', 'NONE'
            "defaultEquityOrderType": "LIMIT",  # 可選: 'MARKET', 'LIMIT', 'STOP', 'STOP_LIMIT', 'TRAILING_STOP', 'MARKET_ON_CLOSE', 'NONE'
            "defaultEquityOrderPriceLinkType": "VALUE",  # 可選: 'VALUE', 'PERCENT', 'NONE'
            "defaultEquityOrderDuration": "DAY",  # 可選: 'DAY', 'GOOD_TILL_CANCEL', 'NONE'
            "defaultEquityOrderMarketSession": "NORMAL",  # 可選: 'AM', 'PM', 'NORMAL', 'SEAMLESS', 'NONE'
            "defaultEquityQuantity": 1,
            "mutualFundTaxLotMethod": "FIFO",  # 可選: 'FIFO', 'LIFO', 'HIGH_COST', 'LOW_COST', 'MINIMUM_TAX', 'AVERAGE_COST', 'NONE'
            "optionTaxLotMethod": "FIFO",  # 同上
            "equityTaxLotMethod": "FIFO",  # 同上
            "defaultAdvancedToolLaunch": "NONE",  # 可選: 'TA', 'N', 'Y', 'TOS', 'NONE', 'CC2'
            "authTokenTimeout": "FIFTY_FIVE_MINUTES"  # 可選: 'FIFTY_FIVE_MINUTES', 'TWO_HOURS', 'FOUR_HOURS', 'EIGHT_HOURS'
        }
        response = self.user_settings.update_account_preferences(account_id, preferences_data)
        self.assertIn('expressTrading', response)

if __name__ == '__main__':
    unittest.main()
