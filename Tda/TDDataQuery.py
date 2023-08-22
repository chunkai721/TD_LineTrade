import requests

class TDDataQuery:
    BASE_URL = "https://api.tdameritrade.com/v1/marketdata"
    
    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

    def _make_request(self, url, params=None):
        """Helper method to make API requests and handle errors."""
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()

    # Instruments
    def search_instruments(self, searchText=None, symbol=None, projection=None):
        url = f"{self.BASE_URL}/instruments"
        params = {
            "searchText": searchText,
            "symbol": symbol,
            "projection": projection
        }
        return self._make_request(url, params)

    def get_instrument_by_cusip(self, cusip):
        url = f"{self.BASE_URL}/instruments/{cusip}"
        return self._make_request(url)

    # Market Hours
    def get_market_hours(self, markets, date=None):
        url = f"{self.BASE_URL}/marketdata/hours"
        params = {
            "markets": markets,
            "date": date
        }
        return self._make_request(url, params)

    def get_market_hours_for_specific_market(self, market, date=None):
        url = f"{self.BASE_URL}/marketdata/{market}/hours"
        params = {
            "date": date
        }
        return self._make_request(url, params)

    # Movers
    def get_movers_for_index(self, index, direction=None, change=None):
        url = f"{self.BASE_URL}/marketdata/{index}/movers"
        params = {
            "direction": direction,
            "change": change
        }
        return self._make_request(url, params)

    # Option Chains
    def get_option_chain(self, symbol, **kwargs):
        url = f"{self.BASE_URL}/marketdata/chains"
        params = {"symbol": symbol}
        params.update(kwargs)
        return self._make_request(url, params)

    # Price History
    def get_price_history(self, symbol, **kwargs):
        url = f"{self.BASE_URL}/marketdata/{symbol}/pricehistory"
        params = {"symbol": symbol}
        params.update(kwargs)
        return self._make_request(url, params)

    # Quotes
    def get_quotes(self, symbols):
        if isinstance(symbols, list):
            symbols = ','.join(symbols)
        url = f"{self.BASE_URL}/marketdata/quotes"
        params = {
            "symbol": symbols
        }
        return self._make_request(url, params)

    def get_quote(self, symbol):
        url = f"{self.BASE_URL}/marketdata/{symbol}/quotes"
        return self._make_request(url)
