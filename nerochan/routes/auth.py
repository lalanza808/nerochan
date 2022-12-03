from flask import Blueprint, render_template
from flask import flash, redirect, url_for
from flask_login import logout_user, current_user

from nerochan.forms import UserForm, UserRegistration, UserChallenge
from nerochan.helpers import make_wallet_rpc
from nerochan.models import User


bp = Blueprint('auth', 'auth')

@bp.route("/register", methods=["GET", "POST"])
def register():
    form = UserRegistration()
    if current_user.is_authenticated:
        flash('Already registered and authenticated.')
        return redirect(url_for('main.index'))

    if form.validate_on_submit():
        # Check if handle already exists
        user = User.select().where(
            User.handle == form.handle.data
        ).first()
        if user:
            flash('This handle is already registered.')
            return redirect(url_for('auth.login'))

        # Save new user
        user = User(
            handle=form.handle.data,
            wallet_address=form.wallet_address.data,
        )
        user.save()
        user.login()
        return redirect(url_for('main.index'))

    return render_template("auth/register.html", form=form)

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = UserForm()
    if current_user.is_authenticated:
        flash('Already logged in.')
        return redirect(url_for('main.index'))

    if form.validate_on_submit():
        # Check if user doesn't exist
        user = User.select().where(
            User.handle == form.handle.data
        ).first()
        if not user:
            flash('That handle does not exist.')
            return redirect(url_for('auth.login'))
        return redirect(url_for('auth.challenge', handle=user.handle))

    return render_template("auth/login.html", form=form)

@bp.route("/login/challenge/<handle>", methods=["GET", "POST"])
def challenge(handle):
    form = UserChallenge()
    user = User.select().where(User.handle == handle).first()
    if not user:
        flash('User does not exist.')
        return redirect(url_for('main.index'))

    if current_user.is_authenticated:
        flash('Already logged in.')
        return redirect(url_for('main.index'))

    if form.validate_on_submit():
        data = {
            'data': user.challenge,
            'address': user.wallet_address,
            'signature': form.signature.data
        }
        try:
            res = make_wallet_rpc('verify', data)
            if res['good']:
                user.regenerate_challenge()
                user.login()
                flash('Successful login!')
                return redirect(url_for('main.index'))
            else:
                flash('Invalid signature. Try again.')
                return redirect(url_for('auth.challenge', handle=handle))
        except Exception as e:
            flash(f'Issue with checking the signature provided: {e}')
            return redirect(url_for('auth.challenge', handle=handle))
            
    return render_template(
        'auth/challenge.html', 
        user=user,
        form=form
    )

@bp.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    else:
        flash('Not authenticated!')
    return redirect(url_for('main.index'))
