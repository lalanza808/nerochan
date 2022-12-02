from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required

from nerochan.models import User


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
    return render_template(
        'user/show.html',
        user=user
    )

@bp.route('/profile')
@login_required
def edit():
    return render_template(
        'user/edit.html'
    )