import peewee as pw
import playhouse.postgres_ext as pwpg
from monero.wallet import Wallet

from nerochan import config


def make_wallet_rpc(method, data={}):
    try:
        w = Wallet(
            port=config.XMR_WALLET_RPC_PORT,
            user=config.XMR_WALLET_RPC_USER,
            password=config.XMR_WALLET_RPC_PASS,
            timeout=3
        )
        res = w._backend.raw_request(method, data)
        return res
    except Exception as e:
        raise e