import requests
import time
import json
from tqdm import tqdm
import sys

def parse_markets():
    pass

def get_markets(series_ticker):
    valid_markets = []
    url = "https://api.elections.kalshi.com/trade-api/v2/markets"

    params = {
        "limit": 1000,
        "status": "open",
        "mve_filter": "exclude",
        "series_ticker": series_ticker
    }
    response = requests.get(url, params=params)
    data = response.json()
    cursor = data.get('cursor')

    while True:
        if 'markets' not in data:
            print(data)
            break
        for market in data['markets']:
            valid_markets.append({
                "ticker": market['ticker'],
                "rules_primary": market["rules_primary"],
                "rules_secondary": market["rules_secondary"]
            })
        if cursor == '':
            break
        
        params['cursor'] = cursor
        response = requests.get(url, params=params)
        data = response.json()
        cursor = data.get('cursor')
    
    return valid_markets

def get_series(ticker_check):
    url = "https://api.elections.kalshi.com/trade-api/v2/series?category=Sports"

    response = requests.get(url)
    data = response.json()
    series_tickers = []

    for series in data["series"]:
        if ticker_check in series["ticker"]:
            series_tickers.append(series["ticker"])
    return series_tickers

def get_all_markets(available_markets, ticker_idx, market_ticker):

    market_tickers = []
    print(f"Finding Series Markets: {available_markets[ticker_idx]['Name']}...")
    series_tickers = get_series(market_ticker)
    print("Finding All Markets...")
    for ticker in tqdm(series_tickers):
        market_tickers = market_tickers + get_markets(ticker)
        time.sleep(0.25)
    print()
    return market_tickers

def main():

    markets = sys.argv[1]
    if not markets:
        print("Usage: python scripts/kalshi_markets.py <MARKET_CODE_1> <MARKET_CODE_2> ...")
        print("Example: python scripts/kalshi_markets.py MPBK NHL")
        return

    with open("scripts/markets.json", "r") as f:
        available_markets = json.load(f)
    
    for market in markets:

        if market not in available_markets:
            print()
            print(f"{market} is not a supported market")
            print()
            continue

        game_market = available_markets[market]["Game"]
        futures_market = available_markets[market]["Futures"]
        
        game_markets = get_all_markets(available_markets, market, game_market)
        
        if game_market == futures_market:
            print("Game and Futures Markets are together")
            print("Game and Futures Markets Combined: ")
            print(json.dumps(game_markets, indent=2))
        else:
            print("Game Markets:")
            print(json.dumps(game_markets, indent=2))
            print()
            print("Futures Markets:")
            futures_markets = []
            if isinstance(futures_market, list):
                for futures_ticker in futures_market:
                    futures_markets += get_all_markets(available_markets, market, futures_ticker)
            else:
                futures_markets = get_all_markets(available_markets, market, futures_market)
            print(json.dumps(futures_markets, indent=2))



if __name__ == "__main__":
    main()
