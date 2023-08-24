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
        # TODO: 使用TDA_REFRESH_TOKEN從API獲取新的訪問令牌
        # 更新self.access_token的值
        # 更新.env文件中的TDA_ACCESS_TOKEN和TDA_ACCESS_TOKEN_EXPIRY值
        pass

    def _handle_response(self, response):
        if response.status_code == 401:  # 令牌過期或無效
            self._refresh_access_token()
            # TODO: 重新嘗試API請求
        elif response.status_code != 200:
            error_msg = response.json().get("error", "Unknown error.")
            raise Exception(f"API Error: {error_msg}")
        return response.json()

    def _api_request(self, method, endpoint, data=None, params=None):
        url = f"{self.BASE_URL}/{endpoint}"
        response = requests.request(method, url, headers=self.headers, json=data, params=params)
        return self._handle_response(response)

    # Get Account Preferences
    def get_account_preferences(self, account_id):
        return self._api_request("GET", f"accounts/{account_id}/preferences")

    # Update Account Preferences
    def update_account_preferences(self, account_id, preferences_data):
        return self._api_request("PUT", f"accounts/{account_id}/preferences", data=preferences_data)

    # Get User Principals
    def get_user_principals(self, fields=None):
        params = {"fields": fields} if fields else None
        return self._api_request("GET", "userprincipals", params=params)

    # Get Streamer Subscription Keys
    def get_streamer_subscription_keys(self):
        return self._api_request("GET", "userprincipals/streamersubscriptionkeys")
