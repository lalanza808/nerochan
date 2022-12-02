from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from nerochan.helpers import make_wallet_rpc
from nerochan.forms import ConfirmTip
from nerochan.models import Artwork, Transaction


bp = Blueprint('artwork', 'artwork', url_prefix='/artwork')

@bp.route('')
def list():
    return 'show all artwork'

@bp.route('/pending')
def pending():
    return 'show pending artwork'


@bp.route('/<int:id>', methods=['GET', 'POST'])
def show(id):
    form = ConfirmTip()
    artwork = Artwork.get_or_none(id)
    if not artwork:
        flash('That artwork does not exist.', 'warning')
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        # Create a tx object to verify later
        try:
            tx = Transaction(
                tx_id=form.tx_id.data,
                tx_key=form.tx_key.data,
                to_address=artwork.user.wallet_address,
                artwork=artwork.id
            )
            tx.save()
        except Exception as e:
            pass
        return redirect(url_for('artwork.show', id=artwork.id))
    txes_pending = Transaction.select().where(
        Transaction.artwork == artwork,
        Transaction.verified == False
    ).count()
    txes = Transaction.select().where(
        Transaction.artwork == artwork,
        Transaction.verified == True
    ).order_by(Transaction.tx_date.desc())
    total = sum([i.atomic_xmr for i in txes])
    return render_template(
        'artwork/show.html', 
        artwork=artwork,
        txes_pending=txes_pending,
        txes=txes,
        total=total,
        form=form
    )

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    return 'upload your artwork'