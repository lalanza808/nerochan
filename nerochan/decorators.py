from flask import session, redirect, url_for, flash
from flask_login import current_user
from functools import wraps
from nerochan.models import User, CreatorProfile, BackerProfile, Subscription


# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if "auth" not in session or not session["auth"]:
#             return redirect(url_for("auth.login"))
#         return f(*args, **kwargs)
#     return decorated_function

def subscription_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(current_user)
        # m = Moderator.filter(username=session["auth"]["preferred_username"])
        # if m:
        #     return f(*args, **kwargs)
        # else:
        #     flash("You are not a moderator")
        #     return redirect(url_for("index"))
    return decorated_function
