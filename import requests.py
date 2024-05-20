import requests
import json
import time
import hmac
import hashlib
import pandas as pd
import os


def to_csv(df, csv_name):
    path = f"/Users/elab/Downloads/{csv_name}.csv"
    df.to_csv(path, mode='a', header=not os.path.exists(path), index=False)

def create_signature(query_string, secret):
    return hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def Option_Account_Information(api_key, api_secret):
    base_url = 'https://api.binance.com'
    endpoint = '/eapi/v1/marginAccount'
    api_key = 'vUUfFsfXMzJkZTaVpE84XZDMxIrHKkPoLtrRTR1rLzth6lZMQXjZE8ifokMjk6Mo'
    api_secret = 'Y3RHgdXuOajWtHEJNaNfSEOS0W0szSEQTPPbuTSs3AIlHnmc9EDZ0Zmh8ocsB4eJ'
    
    timestamp = int(time.time() * 1000)
    query_string = f'timestamp={timestamp)'
    signature = create_signature(query_string, api_secret)
    
    headers = {
        'X-MBX-APIKEY': api_key
    }
    
    url = f'{base_url}{endpoint}?{query_string}&signature={signature}'
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(data)  # Print data to understand the structure
        
        # Extract relevant data
        assets_info = data.get('userAssets', [])
        account_data = []
        
        for asset in assets_info:
            row = {
                'asset': asset.get('asset', ''),
                'Open_price': '',  # Placeholder, replace with actual data if needed
                'marginBalance': asset.get('marginBalance', ''),
                'equity': asset.get('equity', ''),
                'available': asset.get('availableBalance', ''),
                'locked': asset.get('locked', ''),
                'unrealizedPNL': asset.get('unrealizedProfit', ''),
                'time': data.get('updateTime', ''),
                'riskLevel': data.get('marginLevelStatus', '')
            }
            account_data.append(row)
        
        column_names = [
            'asset', 'Open_price', 'marginBalance', 'equity', 'available', 'locked',
            'unrealizedPNL', 'time', 'riskLevel'
        ]
        df = pd.DataFrame(account_data, columns=column_names)
        return df
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def apply_Option_Account_Information(api_key, api_secret, symbol):
    data = Option_Account_Information(api_key, api_secret)
    if data is not None:
        data["Symboles"] = symbol
        columns_new_order = [
            'Symboles', 'Open_price', 'marginBalance', 'equity', 'available', 'locked',
            'unrealizedPNL', 'time', 'riskLevel'
        ]
        data = data[columns_new_order]
        to_csv(data, "klines")

api_key = "YOUR_API_KEY"
api_secret = "YOUR_API_SECRET"
symbols = [
    "BTCFDUSD", "BTCUSDT", "ETHFDUSD", "USDCUSDT", "ETHUSDT", "SOLUSDT",
    "FDUSDUSDT", "PEPEUSDT", "SOLFDUSD", "WIFUSDT"
]

for s in symbols:
    apply_Option_Account_Information(api_key, api_secret, s)
