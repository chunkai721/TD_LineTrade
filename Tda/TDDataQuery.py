import requests
import json
import logging

class TDDataQuery:
    """A class to query TD Ameritrade's market data."""
    
    BASE_URL = "https://api.tdameritrade.com/v1/marketdata"
    
    def __init__(self, access_token):
        self.access_token = access_token
        self._headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        # 初始化日誌
        self._logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def _make_request(self, url, params=None):
        response = requests.get(url, headers=self._headers, params=params)
        self._logger.info(f"狀態碼: {response.status_code}")
        print(response.text)
        response.raise_for_status()  # 對HTTP錯誤引發異常
        
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            self._logger.error("無法從回應中解碼JSON。")
            return {"error": "無效的JSON回應"}

    def search_instruments(self, searchText=None, symbol=None, projection=None):
        if not searchText and not symbol:
            self._logger.error("必須提供'searchText'或'symbol'。")
            return {"error": "無效的參數"}
        
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
