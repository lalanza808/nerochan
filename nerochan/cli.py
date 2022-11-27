import click
from os import path, makedirs
from urllib.request import urlopen

from nerochan.models import User, Artwork


def cli(app):
    @app.cli.command('init')
    def init():
        import peewee
        from nerochan.models import db
        model = peewee.Model.__subclasses__()
        db.create_tables(model)

    @app.cli.command('generate_data')
    def generate_data():
        data = {
            'nerodude': {
                'wallet': '797P5cwQA2LHxPqfnsMgPwbfTGk6JAcibSPo6jV75uGx4Am7sZRbE1R5HJ7urWCDWNV51tPWtzyY1JMiUTXrXdu93YfjrdH',
                'art': [
                    'https://www.monerochan.art/commissions/monerochan-beach.jpg',
                    'https://www.monerochan.art/commissions/mememe.gif',
                    'https://www.monerochan.art/commissions/iwantyou.jpg'
                ]
            },
            'weedburpz': {
                'wallet': '77toDDnVmSrWMZ5tS17UWXcxQVkD6LtNSArVwzsWdE176oDbYtPTiAqExjDZWGE5KwKPY7Kd1BcWYfCnJuL2RfcqA1gzoEj',
                'art': [
                    'https://www.monerochan.art/commissions/hammock.png',
                    'https://www.monerochan.art/commissions/assaultrifle.png'
                ]
            }
        }
        for user in data:
            _user = User.select().where(User.handle == user).first()
            if not _user:
                u = User(
                    handle=user,
                    wallet_address=data[user]['wallet']
                )
                u.save()
                _user = u
                click.echo(f'[+] Created user {user}')
            
            for art in data[user]['art']:
                makedirs('./data/uploads', exist_ok=True)
                bn = path.basename(art)
                fp = f'./data/uploads/{bn}'
                if not path.exists(fp):
                    with urlopen(art) as img:
                        content = img.read()
                        with open(fp, 'wb') as download:
                            download.write(content)
                    click.echo(f'[+] Downloaded {art}')
                if not Artwork.select().where(Artwork.path == bn).first():
                    artwork = Artwork(
                        creator=_user,
                        path=bn,
                        approved=True,
                        title=f'i made {bn}',
                        description=''
                    )
                    artwork.save()
                    click.echo(f'[+] Created artwork {artwork.id} for {bn}')
    
    return app
