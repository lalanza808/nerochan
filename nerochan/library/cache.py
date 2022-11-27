from json import loads as json_loads
from json import dumps as json_dumps
from datetime import timedelta

from redis import Redis

from nerochan.library.market import get_market_data
from nerochan import config


class Cache(object):
    def __init__(self):
        self.redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)

    def store_data(self, item_name, expiration_minutes, data):
        self.redis.setex(
            item_name,
            timedelta(minutes=expiration_minutes),
            value=data
        )

    def get_coin_price(self, coin_name):
        key_name = f'{coin_name}_price'
        data = self.redis.get(key_name)
        if data:
            return json_loads(data)
        else:
            d = get_market_data(coin_name)
            data = {
                key_name: d['market_data']['current_price'],
            }
            self.store_data(key_name, 4, json_dumps(data))
            return data

cache = Cache()
