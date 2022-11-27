from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required

from nerochan.models import User


bp = Blueprint('admin', 'admin', url_prefix='/admin')

@bp.route('/')
def main(handle: str):
    user = User.select().where(User.handle == handle).first()
    if not user:
        flash('That user does not exist.', 'warning')
        return redirect(url_for('main.index'))
    return render_template(
        'user/show.html',
        user=user
    )

# approve artwork
# ban user
# hide artwork
# promote mod
# demote mod
# promote admin
# demote admin