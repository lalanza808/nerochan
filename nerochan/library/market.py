from requests import get as r_get


def get_market_data(coin_name="monero"):
    data = {
        'localization': False,
        'tickers': False,
        'market_data': True,
        'community_data': False,
        'developer_data': False,
        'sparkline': False
    }
    headers = {'accept': 'application/json'}
    url = f'https://api.coingecko.com/api/v3/coins/{coin_name}'
    r = r_get(url, headers=headers, data=data)
    return r.json()
