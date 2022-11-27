from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user

# from nerochan.models import Content, User


bp = Blueprint('post', 'post')

# @bp.route('/post/<int:post_id>')
# def show(post_id):
#     post = TextPost.get_or_none(post_id)
#     if post:
#         if current_user.is_anonymous:
#             flash('You must login to view this post.')
#             return redirect(url_for('creator.show', username=post.creator.user.username))
#         user_subscriptions = Subscription.select().where(
#             Subscription.active == True,
#             Subscription.backer == current_user.backer_profile.first()
#         )
#         if user_subscriptions:
#             return render_template('post/show.html', post=post)
#         else:
#             flash('Viewing posts requires a subscription.')
#             return redirect(url_for('creator.subscription', username=post.creator.user.username))
#     else:
#         flash('That post does not exist.')
#         return redirect(url_for('meta.index'))
