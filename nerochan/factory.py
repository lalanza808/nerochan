from flask import Flask
from flask_login import LoginManager

from nerochan.cli import cli
from nerochan.routes import artwork


def setup_db(app: Flask):
    import peewee
    models = peewee.Model.__subclasses__()
    for m in models:
        m.create_table()


def create_app():
    app = Flask(__name__)
    app = cli(app)
    app.config.from_envvar('FLASK_SECRETS')

    # Login manager
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.logout_view = 'auth.logout'

    @login_manager.user_loader
    def load_user(user_id):
        from nerochan.models import User
        return User.get_or_none(user_id)

    with app.app_context():
        from nerochan.routes import api, auth, main, artwork, user
        from nerochan import filters
        app.register_blueprint(main.bp)
        app.register_blueprint(api.bp)
        app.register_blueprint(auth.bp)
        app.register_blueprint(artwork.bp)
        app.register_blueprint(user.bp)
        app.register_blueprint(filters.bp)

    return app
