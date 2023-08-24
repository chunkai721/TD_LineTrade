# CK_TD Project

This project is designed to interact with TD Ameritrade's API for authentication and trading functionalities.

## Directory Structure

├── TD_LINETRADE/
│   ├── Tda/
│   │   ├── __init__.py
│   │   ├── TDAAuthentication.py       # 包含 TDAAuthentication 類別，用於身份驗證
│   │   ├── TDAccountsAndTrading.py    # 包含 TDAccountsAndTrading 類別，用於帳戶和交易功能
│   │   ├── TDDataQuery.py             # 包含 TDDataQuery 類別，用於查詢市場數據
│   │   ├── TDUserSettings.py          # 包含 TDUserSettings 類別，用於管理用戶設定
│   │   ├── TDWatchlist.py             # 包含 TDWatchlist 類別，用於管理觀察列表
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   └── .env                    # 包含環境變數，例如 CLIENT_ID, REDIRECT_URI 等
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_Auth.py            # 測試 TDAAuthentication 的功能
│   │   │   ├── test_AccountsAndTrading.py  # 測試 TDAccountsAndTrading 的功能
│   │   │   ├── test_TDDataQuery.py     # 測試 TDDataQuery 的功能
│   │   │   ├── test_UserSettings.py    # 測試 TDUserSettings 的功能
│   │   │   └── test_TDWatchlist.py     # 測試 TDWatchlist 的功能
│   │   └── utils/
│   │       └── __init__.py
│   └── main.py                         # 主要的執行檔，可以用來啟動整個應用程式
└── README.md                           # 說明文件，描述如何設定和運行程式

## Getting Started

1. **Setup Environment Variables**: Populate the `.env` file inside the `config` directory with the necessary environment variables.
2. **Run Tests**: Navigate to the `tests` directory and run the test scripts to ensure everything is set up correctly.
3. **Start the Application**: Execute the `main.py` script to start the application.

## Contributing

If you wish to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.
