from monero.wallet import Wallet
from monero.daemon import Daemon

from nerochan import config


daemon = Daemon(
    host=config.XMR_DAEMON_HOST,
    port=config.XMR_DAEMON_PORT,
    timeout=3
)

wallet = Wallet(
    port=config.XMR_WALLET_RPC_PORT,
    user=config.XMR_WALLET_RPC_USER,
    password=config.XMR_WALLET_RPC_PASS,
    timeout=3
)

def make_wallet_rpc(method, data={}):
    try:
        w = wallet
        res = w._backend.raw_request(method, data)
        return res
    except Exception as e:
        raise e

def make_daemon_rpc(method, data={}):
    try:
        d = daemon
        res = d._backend.raw_request(method, data)
        return res
    except Exception as e:
        raise e
