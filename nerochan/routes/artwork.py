from math import ceil
from pathlib import Path
from secrets import token_urlsafe

from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from nerochan.forms import ConfirmTip, CreateArtwork
from nerochan.decorators import admin_required
from nerochan.models import Artwork, Transaction
from nerochan import config


bp = Blueprint('artwork', 'artwork', url_prefix='/artwork')

@bp.route('')
def list():
    ipp = 20
    page = request.args.get("page", 1)
    try:
        page = int(page)
    except:
        flash('Invalid page number provided.', 'warning')
        page = 1
    artwork = Artwork.select().where(
        Artwork.approved == True,
        Artwork.hidden == False
    ).order_by(Artwork.upload_date.desc())
    paginated_posts = artwork.paginate(page, ipp)
    total_pages = ceil(artwork.count() / ipp)
    return render_template(
        'artwork/list.html',
        artwork=paginated_posts,
        page=page,
        total_pages=total_pages
    )

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
        base = Path(config.DATA_PATH, 'uploads')
        base.joinpath(artwork.image).unlink(missing_ok=True)
        base.joinpath(artwork.thumbnail).unlink(missing_ok=True)
        artwork.delete_instance()
        flash('Artwork has been deleted from the system.', 'success')
        return redirect(url_for('artwork.hidden'))
    elif action == 'regenerate_thumbnail':
        artwork.generate_thumbnail()
        flash(f'Generated new thumbnail for artwork {artwork.id}', 'success')
        return redirect(url_for('artwork.show', id=artwork.id))
    elif action == 'toggle_nsfw':
        artwork.nsfw = not artwork.nsfw
        artwork.save()
        artwork.generate_thumbnail()
        flash(f'Toggled NSFW status for artwork {artwork.id} and regenerated thumbnail.', 'success')
        return redirect(url_for('artwork.show', id=artwork.id))
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

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateArtwork()
    if form.validate_on_submit():
        rand = token_urlsafe(12)
        f = form.content.data
        filename = secure_filename(f'{rand}-{f.filename}')
        try:
            f.save(Path(config.DATA_PATH, 'uploads', filename))
        except Exception as e:
            flash(f'There was an issue saving the file: {e}')
            return redirect(request.referrer)

        artwork = Artwork(
            user=current_user,
            image=filename,
            approved=current_user.is_verified,
            nsfw=form.nsfw.data,
            title=form.title.data,
            description=form.description.data
        )
        artwork.save()
        artwork.generate_thumbnail()
        if current_user.is_verified:
            return redirect(url_for('artwork.show', id=artwork.id))
        else:
            flash('Artwork has been posted! Please wait for an admin to review and approve it.', 'success')
            return redirect(url_for('main.index'))

    return render_template(
        'artwork/create.html',
        form=form
    )