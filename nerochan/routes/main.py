from flask import Blueprint, render_template


bp = Blueprint('main', 'main')

@bp.route('/')
def index():
    feed = dict()
    return render_template(
        'index.html',
        feed=feed
    )

@bp.route('/about')
def about():
    return render_template('about.html')


# most tipped artworks
# most tipped artists