from datetime import datetime

import arrow
from monero.numbers import from_atomic
from flask import Blueprint

from nerochan import config


bp = Blueprint('filters', 'filters')


@bp.app_template_filter('humanize')
def humanize(d):
    return arrow.get(d).humanize()

@bp.app_template_filter('ts')
def from_ts(v):
    return datetime.fromtimestamp(v)

@bp.app_template_filter('xmr_block_explorer')
def xmr_block_explorer(v):
    if config.XMR_WALLET_NETWORK == 'stagenet':
        return f'https://stagenet.xmrchain.net/tx/{v}'
    else:
        return f'https://www.exploremonero.com/transaction/{v}'

@bp.app_template_filter('atomic')
def atomic(amt):
    return float(from_atomic(amt))

@bp.app_template_filter('shorten')
def shorten(s):
    return s[:4] + '...' + s[-5:]