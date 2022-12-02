from pathlib import Path

from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from nerochan.forms import ConfirmTip
from nerochan.decorators import admin_required
from nerochan.models import Artwork, Transaction
from nerochan import config


bp = Blueprint('artwork', 'artwork', url_prefix='/artwork')

@bp.route('')
def list():
    return 'show all artwork'

@bp.route('/pending')
@login_required
@admin_required
def pending():
    artwork = Artwork.select().where(
        Artwork.approved == False,
        Artwork.hidden == False
    ).order_by(Artwork.upload_date.asc())
    return render_template(
        'artwork/pending.html',
        artwork=artwork
    )

@bp.route('/hidden')
@login_required
@admin_required
def hidden():
    artwork = Artwork.select().where(
        Artwork.hidden == True
    ).order_by(Artwork.upload_date.asc())
    return render_template(
        'artwork/hidden.html',
        artwork=artwork
    )

@bp.route('/<int:id>/<action>')
@login_required
@admin_required
def manage(id, action):
    artwork = Artwork.get_or_none(id)
    if not artwork:
        flash('That artwork does not exist.', 'warning')
        return redirect(url_for('main.index'))
    if action == 'approve':
        artwork.approved = True
        artwork.hidden = False
        artwork.save()
        flash(f'Artwork {artwork.id} has been approved', 'success')
    elif action == 'reject':
        artwork.approved = False
        artwork.hidden = True
        artwork.save()
        flash(f'Artwork {artwork.id} has been rejected and hidden', 'success')
    elif action == 'delete':
        if artwork.approved:
            flash('Cannot delete an artwork that is already approved', 'warning')
            return redirect(url_for('artwork.show', id=artwork.id))
        elif not artwork.hidden:
            flash('Cannot delete an artwork unless it is hidden first', 'warning')
            return redirect(url_for('artwork.show', id=artwork.id))
        base = Path(config.DATA_PATH).joinpath('uploads')
        base.joinpath(artwork.image).unlink(missing_ok=True)
        base.joinpath(artwork.thumbnail).unlink(missing_ok=True)
        artwork.delete_instance()
        flash('Artwork has been deleted from the system.', 'success')
        return redirect(url_for('artwork.hidden'))
    return redirect(url_for('artwork.pending'))


@bp.route('/<int:id>', methods=['GET', 'POST'])
def show(id):
    form = ConfirmTip()
    artwork = Artwork.get_or_none(id)
    if not artwork:
        flash('That artwork does not exist.', 'warning')
        return redirect(url_for('main.index'))
    if not artwork.approved:
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('That artwork is pending approval.')
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