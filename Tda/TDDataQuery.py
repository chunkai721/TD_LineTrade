import requests
import json
import logging

class TDDataQuery:
    """A class to query TD Ameritrade's market data."""
    
    BASE_URL = "https://api.tdameritrade.com/v1/marketdata"
    
    def __init__(self, access_token, client_id):
        self.access_token = access_token
        self.client_id = client_id
        self._headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        # 初始化日誌
        self._logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def _make_request(self, url, params=None):
        if params is None:
            params = {}
        params["apikey"] = self.client_id  # 添加client_id到請求參數中
        response = requests.get(url, headers=self._headers, params=params)
        self._logger.info(f"狀態碼: {response.status_code}")
        response.raise_for_status()  # 對HTTP錯誤引發異常
        
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            self._logger.error(f"無法從回應中解碼JSON。回應內容: {response.text}")  # 打印出回應的內容
            return {"error": "無效的JSON回應"}

    def search_instruments(self, symbol, projection, apikey=None):
        # 檢查projection的有效性
        valid_projections = ["symbol-search", "symbol-regex", "desc-search", "desc-regex", "fundamental"]
        if projection not in valid_projections:
            self._logger.error(f"無效的'projection'值。有效的選項是: {', '.join(valid_projections)}")
            return {"error": "無效的'projection'值"}

        # 檢查是否提供了symbol
        if not symbol:
            self._logger.error("必須提供'symbol'。")
            return {"error": "缺少'symbol'參數"}

        url = f"{self.BASE_URL}/instruments"
        params = {
            "symbol": symbol,
            "projection": projection
        }

        # 如果提供了apikey，則將其添加到請求參數中
        if apikey:
            params["apikey"] = apikey

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
