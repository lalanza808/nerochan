from flask import Blueprint, render_template
from flask_login import current_user

from nerochan.models import *


bp = Blueprint('main', 'main')

@bp.route('/')
def index():
    feed = dict()
    # new_creators = User.select().where(
    #     User.roles.contains_any(UserRole.creator)
    # ).order_by(User.register_date.desc()).execute()
    # feed['new_creators'] = new_creators
    # if current_user.is_authenticated:
    #     active_subscriptions = Subscription.select().where(
    #         Subscription.is_active == True,
    #         Subscription.backer == current_user
    #     ).order_by(Subscription.subscribe_date.desc()).execute()
    #     feed['active_subscriptions'] = active_subscriptions
    #     new_posts = Post.select().where(
    #         Post.hidden == False,
    #         Post.creator in [c.creator for c in active_subscriptions]
    #     ).order_by(Post.post_date.desc()).execute()
    #     feed['new_posts'] = new_posts
    return render_template(
        'index.html',
        feed=feed
    )
