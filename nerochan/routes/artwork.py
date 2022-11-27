from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from nerochan.models import Artwork, User


bp = Blueprint('artwork', 'artwork', url_prefix='/artwork')

@bp.route('/<int:artwork_id>')
def show(artwork_id):
    artwork = Artwork.get_or_none(artwork_id)
    if not artwork:
        flash('That artwork does not exist.', 'warning')
        return redirect(url_for('main.index'))
    return render_template('artwork/show.html', artwork=artwork)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    return 'upload your artwork'