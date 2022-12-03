from math import ceil

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from nerochan.models import User, Artwork, Transaction


bp = Blueprint('user', 'user')

@bp.route('/users')
def list():
    return 'users list'

@bp.route('/user/<handle>')
def show(handle: str):
    user = User.select().where(User.handle == handle).first()
    if not user:
        flash('That user does not exist.', 'warning')
        return redirect(url_for('main.index'))
    ipp = 20
    page = request.args.get("page", 1)
    try:
        page = int(page)
    except:
        flash('Invalid page number provided.', 'warning')
        page = 1
    artwork = Artwork.select().where(
        Artwork.user == user, 
        Artwork.approved == True, 
        Artwork.hidden == False
    ).order_by(Artwork.upload_date.desc())
    # tips = Transaction.select().where(
    #     Transaction.verified == True,
    # ) # need some join magic
    paginated_posts = artwork.paginate(page, ipp)
    total_pages = ceil(artwork.count() / ipp)
    return render_template(
        'user/show.html',
        user=user,
        artwork=paginated_posts,
        page=page,
        total_pages=total_pages
    )

@bp.route('/profile')
@login_required
def edit():
    return render_template(
        'user/edit.html'
    )