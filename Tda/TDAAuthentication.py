import os
import time
import urllib.parse
import requests
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Check if we are in a Docker environment
IN_DOCKER = os.environ.get('IN_DOCKER', 'False').lower() == 'true'

if IN_DOCKER:
    from pyvirtualdisplay import Display

class TDAAuthentication:

    def __init__(self, client_id, redirect_uri):
        self.session = requests.Session()  # 使用Session來管理請求
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.base_url = "https://auth.tdameritrade.com"
        self.token_endpoint = "https://api.tdameritrade.com/v1/oauth2/token"
        self.load_tokens_from_env()
        if not self.access_token or self.is_access_token_expired():
            print("No valid access token found. Please authenticate.")
        else:
            print("Valid access token loaded.")

    def get_authentication_url(self):
        auth_url = f"{self.base_url}/auth?response_type=code&redirect_uri={self.redirect_uri}&client_id={self.client_id}%40AMER.OAUTHAP"
        return auth_url

    def _initialize_selenium(self):
        display = None
        if IN_DOCKER:
            display = Display(visible=0, size=(1600, 900))
            display.start()

        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-webgl')
        driver = webdriver.Chrome(options=chrome_options)

        return display, driver

    def get_authentication_code(self, td_account_id, td_password):
        display, driver = self._initialize_selenium()
        url = self.get_authentication_url()
        driver.get(url)
        
        # 使用WebDriverWait來等待元素出現
        username_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username0')))
        username_element.send_keys(td_account_id)
        
        password_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password1')))
        password_element.send_keys(td_password)
        
        accept_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'accept')))
        accept_button.click()
        
        # 等待第二次accept按鈕出現並點擊
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'accept'))).click()
        
        new_url = driver.current_url
        auth_code = urllib.parse.unquote(new_url.split('code=')[1])
        driver.quit()
        if display:
            display.stop()
        return auth_code

    def _post_request(self, data):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        try:
            response = self.session.post(self.token_endpoint, headers=headers, data=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error during request: {e}")
            return {}

    def get_tokens(self, authorization_code):
        data = {
            "grant_type": "authorization_code",
            "access_type": "offline",
            "code": authorization_code,
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri
        }
        tokens = self._post_request(data)
        if tokens:
            self.access_token = tokens.get("access_token")
            self.refresh_token = tokens.get("refresh_token")
            self.expires_in = tokens.get("expires_in")
            self.refresh_token_expires_in = tokens.get("refresh_token_expires_in")
            self.scope = tokens.get("scope")
            self.save_tokens_to_env()

    def refresh_access_token(self):
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id
        }
        tokens = self._post_request(data)
        if tokens:
            self.access_token = tokens["access_token"]
            self.expires_in = tokens["expires_in"]  # 更新expires_in屬性
            # 檢查API是否返回了refresh_token_expires_in
            if "refresh_token_expires_in" in tokens:
                self.refresh_token_expires_in = tokens["refresh_token_expires_in"]  # 更新refresh_token_expires_in屬性
            self.save_tokens_to_env()  # 保存 tokens 到 .env 文件

    def refresh_all_tokens(self):
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "access_type": "offline",
            "client_id": self.client_id
        }
        tokens = self._post_request(data)
        if tokens:
            self.access_token = tokens["access_token"]
            self.refresh_token = tokens["refresh_token"]
            self.expires_in = tokens["expires_in"]  # 更新expires_in屬性
            self.refresh_token_expires_in = tokens["refresh_token_expires_in"]  # 更新refresh_token_expires_in屬性
            self.save_tokens_to_env()  # 保存 tokens 到 .env 文件
    
    def save_tokens_to_env(self):
        """Save tokens and their expiration times to .env."""
        env_path = os.path.join(os.path.dirname(__file__), 'config', '.env')
        if not os.path.exists(env_path):
            print(f".env file not found at {env_path}")
            return

        # 讀取原始.env文件的內容
        with open(env_path, 'r') as f:
            lines = f.readlines()

        # 更新或添加新的token資訊
        new_content = []
        for line in lines:
            if line.startswith("TDA_ACCESS_TOKEN="):
                new_content.append(f"TDA_ACCESS_TOKEN={self.access_token}\n")
            elif line.startswith("TDA_REFRESH_TOKEN="):
                new_content.append(f"TDA_REFRESH_TOKEN={self.refresh_token}\n")
            elif line.startswith("TDA_ACCESS_TOKEN_EXPIRY="):
                new_content.append(f"TDA_ACCESS_TOKEN_EXPIRY={(datetime.now() + timedelta(seconds=self.expires_in)).isoformat()}\n")
            elif hasattr(self, 'refresh_token_expires_in') and line.startswith("TDA_REFRESH_TOKEN_EXPIRY="):
                new_content.append(f"TDA_REFRESH_TOKEN_EXPIRY={(datetime.now() + timedelta(seconds=self.refresh_token_expires_in)).isoformat()}\n")
            else:
                new_content.append(line)

        # 寫回.env文件
        with open(env_path, 'w') as f:
            f.writelines(new_content)

    def load_tokens_from_env(self):
        """Load tokens and their expiration times from .env."""
        env_path = os.path.join(os.path.dirname(__file__), 'config', '.env')
        # Check if .env file exists
        if not os.path.exists(env_path):
            print(f".env file not found at {env_path}")
            return

        load_dotenv(env_path)
        self.access_token = os.getenv("TDA_ACCESS_TOKEN")
        self.refresh_token = os.getenv("TDA_REFRESH_TOKEN")
        self.access_token_expiry = datetime.fromisoformat(os.getenv("TDA_ACCESS_TOKEN_EXPIRY", "1970-01-01T00:00:00"))
        self.refresh_token_expiry = datetime.fromisoformat(os.getenv("TDA_REFRESH_TOKEN_EXPIRY", "1970-01-01T00:00:00"))

    def is_access_token_expired(self):
        # 提前5分鐘刷新令牌
        return datetime.now() > self.access_token_expiry - timedelta(minutes=5)

    def is_refresh_token_expired(self):
        """Check if the refresh token is expired."""
        return datetime.now() > self.refresh_token_expiry

    def authenticate(self, td_account_id, td_password):
        """Authenticate and get tokens, either by refreshing or by logging in."""
        if self.refresh_token and not self.is_refresh_token_expired():
            if self.is_access_token_expired():
                print("Refreshing access token...")
                self.refresh_access_token()
        else:
            print("Getting new tokens...")
            auth_code = self.get_authentication_code(td_account_id, td_password)
            self.get_tokens(auth_code)
            self.save_tokens_to_env()