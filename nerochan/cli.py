import click


def cli(app):
    @app.cli.command('init')
    def init():
        import peewee
        from nerochan.models import db
        model = peewee.Model.__subclasses__()
        db.create_tables(model)

    return app
