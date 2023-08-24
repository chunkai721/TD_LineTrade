import requests

class TDUserSettings:
    BASE_URL = "https://api.tdameritrade.com/v1"
    
    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def _refresh_access_token(self):
        # 使用TDA_REFRESH_TOKEN從API獲取新的訪問令牌
        # 更新self.access_token的值
        # 更新.env文件中的TDA_ACCESS_TOKEN和TDA_ACCESS_TOKEN_EXPIRY值
        pass

    def _handle_response(self, response):
        if response.status_code == 401:  # 令牌過期或無效
            self._refresh_access_token()
            # 重新嘗試API請求
        elif response.status_code != 200:
            error_msg = response.json().get("error", "Unknown error.")
            raise Exception(f"API Error: {error_msg}")
        return response.json()

    # Get Account Preferences
    def get_account_preferences(self, account_id):
        endpoint = f"{self.BASE_URL}/accounts/{account_id}/preferences"
        response = requests.get(endpoint, headers=self.headers)
        return self._handle_response(response)

    # Update Account Preferences
    def update_account_preferences(self, account_id, preferences_data):
        endpoint = f"{self.BASE_URL}/accounts/{account_id}/preferences"
        response = requests.put(endpoint, headers=self.headers, json=preferences_data)
        return self._handle_response(response)

    # Get User Principals
    def get_user_principals(self, fields=None):
        endpoint = f"{self.BASE_URL}/userprincipals"
        params = {}
        if fields:
            params["fields"] = fields
        response = requests.get(endpoint, headers=self.headers, params=params)
        return self._handle_response(response)

    # Get Streamer Subscription Keys
    def get_streamer_subscription_keys(self):
        endpoint = f"{self.BASE_URL}/userprincipals/streamersubscriptionkeys"
        response = requests.get(endpoint, headers=self.headers)
        return self._handle_response(response)

# Usage:
# user_settings = TDUserSettings(access_token)
# preferences = user_settings.get_account_preferences(account_id)
# user_principals = user_settings.get_user_principals(fields="streamerSubscriptionKeys,streamerConnectionInfo")
