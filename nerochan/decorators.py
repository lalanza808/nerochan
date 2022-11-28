from flask import redirect, flash, request, url_for
from flask_login import current_user
from functools import wraps
from nerochan.models import User

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin:
            return f(*args, **kwargs)
        else:
            flash('Must be an admin to access that page.', 'warning')
            if request.referrer:
                u = request.referrer
            else:
                u = url_for('main.index')
            return redirect(u)
    return decorated_function
