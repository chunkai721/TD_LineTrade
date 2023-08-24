import requests

class TDWatchlist:
    BASE_URL = "https://api.tdameritrade.com/v1"
    
    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def _handle_response(self, response):
        if response.status_code == 401:  # Token expired or invalid
            # TODO: Refresh the access token
            pass
        elif response.status_code != 200:
            error_msg = response.json().get("error", "Unknown error.")
            raise Exception(f"API Error: {error_msg}")
        return response.json()

    # Get all watchlists for a specific account
    def get_watchlists_by_account(self, account_id):
        endpoint = f"accounts/{account_id}/watchlists"
        response = requests.get(f"{self.BASE_URL}/{endpoint}", headers=self.headers)
        return self._handle_response(response)

    # Get a specific watchlist for a specific account
    def get_specific_watchlist(self, account_id, watchlist_id):
        endpoint = f"accounts/{account_id}/watchlists/{watchlist_id}"
        response = requests.get(f"{self.BASE_URL}/{endpoint}", headers=self.headers)
        return self._handle_response(response)

    # Get all watchlists for all linked accounts
    def get_all_watchlists(self):
        endpoint = "accounts/watchlists"
        response = requests.get(f"{self.BASE_URL}/{endpoint}", headers=self.headers)
        return self._handle_response(response)

    # Create a new watchlist for a specific account
    def create_watchlist(self, account_id, watchlist_data):
        endpoint = f"accounts/{account_id}/watchlists"
        response = requests.post(f"{self.BASE_URL}/{endpoint}", headers=self.headers, json=watchlist_data)
        return self._handle_response(response)

    # Update a specific watchlist for a specific account
    def update_watchlist(self, account_id, watchlist_id, watchlist_data):
        endpoint = f"accounts/{account_id}/watchlists/{watchlist_id}"
        response = requests.put(f"{self.BASE_URL}/{endpoint}", headers=self.headers, json=watchlist_data)
        return self._handle_response(response)

    # Partially update a specific watchlist for a specific account
    def partial_update_watchlist(self, account_id, watchlist_id, watchlist_data):
        endpoint = f"accounts/{account_id}/watchlists/{watchlist_id}"
        response = requests.patch(f"{self.BASE_URL}/{endpoint}", headers=self.headers, json=watchlist_data)
        return self._handle_response(response)

    # Delete a specific watchlist for a specific account
    def delete_watchlist(self, account_id, watchlist_id):
        endpoint = f"accounts/{account_id}/watchlists/{watchlist_id}"
        response = requests.delete(f"{self.BASE_URL}/{endpoint}", headers=self.headers)
        return self._handle_response(response)
