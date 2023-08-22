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
        driver = webdriver.Chrome(options=chrome_options)

        return display, driver

    def get_authentication_code(self, td_account_id, td_password):
        """Retrieve the authentication code using Selenium."""
        display, driver = self._initialize_selenium()

        # Construct the URL and open it
        url = self.get_authentication_url()
        driver.get(url)

        # Wait for the username input to be present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username0')))

        # Login process using Selenium
        driver.find_element(By.ID, 'username0').send_keys(td_account_id)
        time.sleep(3)
        driver.find_element(By.ID, 'password1').send_keys(td_password)
        time.sleep(3)
        driver.find_element(By.ID, 'accept').click()
        time.sleep(3)
        driver.find_element(By.ID, 'accept').click()
        time.sleep(3)

        # Extract the code from the URL
        new_url = driver.current_url
        auth_code = urllib.parse.unquote(new_url.split('code=')[1])
        
        driver.quit()
        if display:
            display.stop()

        return auth_code

    def _post_request(self, data):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(self.token_endpoint, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            error_msg = {
                400: "Validation problem with the request.",
                401: "Invalid credentials in the request body.",
                403: "Caller doesn't have access to the account in the request.",
                500: "Unexpected server error.",
                503: "Temporary problem responding."
            }.get(response.status_code, "Unknown error.")
            print("Error:", error_msg)
            return None

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
            self.access_token = tokens["access_token"]
            self.refresh_token = tokens["refresh_token"]
            self.expires_in = tokens["expires_in"]
            self.refresh_token_expires_in = tokens["refresh_token_expires_in"]
            self.scope = tokens["scope"]
            self.save_tokens_to_env()  # 保存 tokens 到 .env 文件

    def refresh_access_token(self):
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id
        }
        tokens = self._post_request(data)
        if tokens:
            self.access_token = tokens["access_token"]
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
            self.save_tokens_to_env()  # 保存 tokens 到 .env 文件
    
    def save_tokens_to_env(self):
        """Save tokens and their expiration times to .env."""
        env_path = os.path.join(os.path.dirname(__file__), 'config', '.env')

        # Check if .env file exists
        if not os.path.exists(env_path):
            print(f".env file not found at {env_path}")
            return
        
        # Read the existing content of the .env file
        with open(env_path, 'r') as f:
            content = f.readlines()

        # Create a dictionary to store the new token values
        new_values = {
            "TDA_ACCESS_TOKEN": self.access_token,
            "TDA_REFRESH_TOKEN": self.refresh_token,
            "TDA_ACCESS_TOKEN_EXPIRY": (datetime.now() + timedelta(seconds=self.expires_in)).isoformat(),
            "TDA_REFRESH_TOKEN_EXPIRY": (datetime.now() + timedelta(seconds=self.refresh_token_expires_in)).isoformat()
        }

        # Update the content with the new token values
        updated_content = []
        for line in content:
            key = line.split('=')[0]
            if key in new_values:
                updated_content.append(f"{key}={new_values[key]}\n")
                del new_values[key]
            else:
                updated_content.append(line)

        # Add any remaining new values
        for key, value in new_values.items():
            updated_content.append(f"{key}={value}\n")

        # Write the updated content back to the .env file
        with open(env_path, 'w') as f:
            f.writelines(updated_content)

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