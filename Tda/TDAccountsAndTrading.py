import requests

class TDAccountsAndTrading:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.tdameritrade.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def _handle_response(self, response):
        if response.status_code != 200:
            error_msg = response.json().get("error", "Unknown error.")
            raise Exception(f"API Error: {error_msg}")
        return response.json()

    # Account Information
    def get_account(self, account_id, fields=None):
        endpoint = f"{self.base_url}/accounts/{account_id}"
        params = {"fields": fields} if fields else {}
        response = requests.get(endpoint, headers=self.headers, params=params)
        return self._handle_response(response)

    def get_accounts(self, fields=None):
        endpoint = f"{self.base_url}/accounts"
        params = {"fields": fields} if fields else {}
        response = requests.get(endpoint, headers=self.headers, params=params)
        return self._handle_response(response)

    # Order Operations
    # ... [Other methods, all using _handle_response]

    def cancel_order(self, account_id, order_id):
        endpoint = f"{self.base_url}/accounts/{account_id}/orders/{order_id}"
        response = requests.delete(endpoint, headers=self.headers)
        return self._handle_response(response)

    # Saved Order Operations
    # ... [Other methods, all using _handle_response]

    def delete_saved_order(self, account_id, saved_order_id):
        endpoint = f"{self.base_url}/accounts/{account_id}/savedorders/{saved_order_id}"
        response = requests.delete(endpoint, headers=self.headers)
        return self._handle_response(response)

    # Transaction History
    def get_transaction(self, accountId, transactionId):
        endpoint = f"{self.base_url}/accounts/{accountId}/transactions/{transactionId}"
        response = requests.get(endpoint, headers=self.headers)
        return self._handle_response(response)

    def get_transactions(self, accountId, type=None, symbol=None, startDate=None, endDate=None):
        endpoint = f"{self.base_url}/accounts/{accountId}/transactions"
        params = {
            "type": type,
            "symbol": symbol,
            "startDate": startDate,
            "endDate": endDate
        }
        # Filter out None values
        params = {k: v for k, v in params.items() if v is not None}
        response = requests.get(endpoint, headers=self.headers, params=params)
        return self._handle_response(response)

# Usage Example
# auth = TDAAuthentication(client_id, redirect_uri)
# auth_code = auth.get_authentication_code(td_account_id, td_password)
# auth.get_tokens(auth_code)
# trading_api = TDAccountsAndTrading(auth.access_token)
