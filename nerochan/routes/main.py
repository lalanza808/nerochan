from os import path

from flask import Blueprint, render_template, send_from_directory

from nerochan.models import Artwork, User
from nerochan import config


bp = Blueprint('main', 'main')

@bp.route('/')
def index():
    users = User.select().where(
        User.is_approved == True
    ).order_by(User.register_date.desc()).limit(10)
    artwork = Artwork.select().where(
        Artwork.approved == True,
        Artwork.hidden == False
    ).order_by(Artwork.upload_date.desc()).limit(10)
    feed = {
        'users': users,
        'artwork': artwork
    }
    return render_template(
        'index.html',
        feed=feed
    )

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    file_path = path.join(config.DATA_PATH, 'uploads')
    return send_from_directory(file_path, filename)

# most tipped artworks
# most tipped artists

