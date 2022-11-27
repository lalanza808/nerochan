from datetime import datetime

import arrow
from monero import numbers
from flask import Blueprint, current_app


bp = Blueprint('filters', 'filters')


@bp.app_template_filter('humanize')
def humanize(d):
    return arrow.get(d).humanize()

@bp.app_template_filter('ts')
def from_ts(v):
    return datetime.fromtimestamp(v)

@bp.app_template_filter('xmr_block_explorer')
def xmr_block_explorer(v):
    return f'https://www.exploremonero.com/transaction/{v}'

@bp.app_template_filter('from_atomic')
def from_atomic(amt):
    return numbers.from_atomic(amt)
