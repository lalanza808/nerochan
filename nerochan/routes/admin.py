from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user

from nerochan.forms import UserForm
from nerochan.decorators import admin_required
from nerochan.models import User, Artwork, Transaction


bp = Blueprint('admin', 'admin', url_prefix='/admin')

@bp.route('', methods=['GET', 'POST'])
@login_required
@admin_required
def dashboard():
    artists = User.select().where(User.is_verified == True).count()
    admins = User.select().where(User.is_admin == True).count()
    active_artworks = Artwork.select().where(Artwork.approved == True).count()
    pending_artworks = Artwork.select().where(Artwork.approved == False).count()
    confirmed_tips = Transaction.select().where(Transaction.verified == True).count()
    pending_tips = Transaction.select().where(Transaction.verified == False).count()
    # 
    # artist_form = UserForm()
    
    # if artist_form.validate_on_submit():
    #     u = User.select().where(User.handle == artist_form.handle.data).first()
    #     u.is_verified = True
    #     u.save()
    #     return redirect(request.referrer)
    
    
    # admins = User.select().where(User.is_admin == True).order_by(User.register_date.desc())
    # artists = User.select().where(User.is_verified == True).order_by(User.register_date.desc())
    return render_template(
        'admin/dashboard.html',
        artists=artists,
        admins=admins,
        active_artworks=active_artworks,
        pending_artworks=pending_artworks,
        confirmed_tips=confirmed_tips,
        pending_tips=pending_tips,
    )

@bp.route('/<item>', methods=['GET', 'POST'])
@login_required
@admin_required
def manage(item):
    form = None
    items = None
    action = None
    if item == 'admins':
        form = UserForm()
        action = 'remove'
        _action = request.args.get(action)
        items = User.select().where(User.is_admin == True).order_by(User.register_date.desc())
        if form.validate_on_submit():
            u = User.select().where(User.handle == form.handle.data).first()
            u.is_admin = True
            u.save()
            return redirect(request.referrer)
        elif _action:
            a = User.select().where(User.handle == _action).first()
            if a == current_user:
                flash('cannot remove yourself')
                return redirect(request.referrer)
            if a:
                a.is_admin = False
                a.save()
                return redirect(request.referrer)
    elif item == 'artists':
        form = UserForm()
        action = 'unverify'
        _action = request.args.get(action)
        items = User.select().where(User.is_verified == True).order_by(User.register_date.desc())
        if form.validate_on_submit():
            u = User.select().where(User.handle == form.handle.data).first()
            u.is_verified = True
            u.save()
            return redirect(request.referrer)
        elif _action:
            a = User.select().where(User.handle == _action).first()
            if a:
                a.is_verified = False
                a.save()
                return redirect(request.referrer)
    return render_template(
        'admin/manage.html',
        item=item,
        items=items,
        action=action,
        form=form
    )

def artists():
    pass

def users():
    pass

# approve artwork
# ban user
# unban user
# hide artwork
# promote mod
# demote mod