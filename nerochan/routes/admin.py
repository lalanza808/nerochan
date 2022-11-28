from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user

from nerochan.forms import UserForm
from nerochan.decorators import admin_required
from nerochan.models import User


bp = Blueprint('admin', 'admin', url_prefix='/admin')

@bp.route('', methods=['GET', 'POST'])
@login_required
@admin_required
def main():
    user_form = UserForm()
    if user_form.validate_on_submit():
        u = User.select().where(User.handle == user_form.handle.data).first()
        u.is_admin = True
        u.save()
        return redirect(request.referrer)
    if request.args.get('remove'):
        a = User.select().where(User.handle == request.args.get('remove')).first()
        if a == current_user:
            flash('cannot delete yourself')
            return redirect(url_for('admin.main'))
        if a:
            a.is_admin = False
            a.save()
            return redirect(url_for('admin.main'))
    admins = User.select().where(User.is_admin == True).order_by(User.register_date.desc())
    return render_template(
        'admin/main.html',
        admins=admins,
        user_form=user_form
    )

# approve artwork
# ban user
# allow user
# hide artwork
# promote mod
# demote mod