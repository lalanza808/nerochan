from math import ceil

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from nerochan.forms import EditProfile
from nerochan.models import User, Artwork, Transaction


bp = Blueprint('user', 'user')

@bp.route('/users')
def list():
    ipp = 20
    page = request.args.get("page", 1)
    try:
        page = int(page)
    except:
        flash('Invalid page number provided.', 'warning')
        page = 1
    users = User.select().where(
        User.is_verified == True
    ).order_by(User.register_date.desc())
    paginated_users = users.paginate(page, ipp)
    total_pages = ceil(users.count() / ipp)
    return render_template(
        'user/list.html',
        users=paginated_users,
        total_users=users.count(),
        page=page,
        total_pages=total_pages
    )

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

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditProfile()
    if form.validate_on_submit():
        updated = False
        if current_user.handle != form.handle.data:
            if not User.select().where(User.handle == form.handle.data).first():
                current_user.handle = form.handle.data
                updated = True
            else:
                flash('That handle is in use.', 'is-error')
        if current_user.wallet_address != form.wallet_address.data:
            if not User.select().where(User.wallet_address == form.wallet_address.data).first():
                current_user.wallet_address = form.wallet_address.data
                updated = True
            else:
                flash('That wallet address is in use.', 'is-error')
        if current_user.email != form.email.data:
            if not User.select().where(User.email == form.email.data).first():
                current_user.email = form.email.data
                updated = True
            else:
                flash('That email address is in use.', 'is-error')
        if current_user.website != form.website.data:
            if not User.select().where(User.website == form.website.data).first():
                current_user.website = form.website.data
                updated = True
            else:
                flash('That website is in use.', 'is-error')
        if current_user.twitter_handle != form.twitter_handle.data:
            if not User.select().where(User.twitter_handle == form.twitter_handle.data).first():
                current_user.twitter_handle = form.twitter_handle.data
                updated = True
            else:
                flash('That Twitter handle is in use.', 'is-error')
        if current_user.bio != form.bio.data:
            current_user.bio = form.bio.data
            updated = True
        if updated:
            current_user.save()
            flash('Updated your profile.', 'is-success')
            return redirect(url_for('user.edit'))
    return render_template(
        'user/edit.html',
        form=form
    )