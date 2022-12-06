import click
import lorem

from datetime import datetime, timedelta, timezone

from os import path, makedirs
from urllib.request import urlopen

from nerochan.helpers import make_wallet_rpc, get_daemon
from nerochan.models import User, Artwork, Transaction


def cli(app):
    @app.cli.command('init')
    def init():
        import peewee
        from nerochan.models import db
        model = peewee.Model.__subclasses__()
        db.create_tables(model)
    
    @app.cli.command('regenerate_thumbnails')
    def regenerate_thumbnails():
        for artwork in Artwork.select():
            print(f'regenerating thumbnail for artwork {artwork.id}')
            artwork.generate_thumbnail()
    
    @click.argument('handle')
    @app.cli.command('add_admin')
    def add_admin(handle):
        user = User.select().where(User.handle == handle).first()
        if not user:
            click.echo('user does not exist')
            return False
        user.is_admin = True
        user.save()
        click.echo(f'{handle} is now an admin')
    
    @click.argument('handle')
    @app.cli.command('remove_admin')
    def remove_admin(handle):
        user = User.select().where(User.handle == handle).first()
        if not user:
            click.echo('user does not exist')
            return False
        user.is_admin = False
        user.save()
        click.echo(f'{handle} is no longer an admin')
    
    @app.cli.command('verify_tips')
    def verify_tips():
        txes = Transaction.select().where(Transaction.verified == False)
        for tx in txes:
            data = {
                'txid': tx.tx_id,
                'tx_key': tx.tx_key,
                'address': tx.to_address
            }
            try:
                res = make_wallet_rpc('check_tx_key', data)
                if res['in_pool'] is False:
                    txdata = get_daemon().transactions([tx.tx_id])[0]
                    d = txdata.timestamp.astimezone(timezone.utc)
                    tx.atomic_xmr = res['received']
                    tx.tx_date = d
                    tx.verified = True
                    tx.save()
                    click.echo(f'[+] Found valid tip {tx.tx_id}')
            except Exception as e:
                # delete if it fails for over 8 hours
                if tx.create_date <= datetime.utcnow() - timedelta(hours=8):
                    pass

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
                    'https://www.monerochan.art/commissions/assaultrifle.png',
                    'https://www.monerochan.art/thumbnails/vtubing.png',
                    'https://www.monerochan.art/commissions/ribbons.jpg',
                    'https://www.monerochan.art/commissions/mining.jpg',
                    'https://www.monerochan.art/commissions/wownerochan_headpat.png',
                    'https://www.monerochan.art/commissions/wownerochan.jpg'
                ]
            },
            'gemini': {
                'wallet': '78TanhCTvw4V8HkY3vD49A5EiyeGCzCHQUm59sByukTcffZPf3QHoK8PDg8WpMUc6VGwqxTu65HvwCUfB2jZutb6NKpjArk',
                'art': [
                    'https://www.monerochan.art/commissions/cheerleader.jpg',
                    'https://www.monerochan.art/commissions/maidnero-chan.png',
                    'https://www.monerochan.art/commissions/dandelion.png',
                    'https://www.monerochan.art/commissions/volleyball_1.jpg',
                    'https://www.monerochan.art/commissions/volleyball_2.jpg',
                    'https://www.monerochan.art/commissions/virgin_killer.png',
                    'https://www.monerochan.art/commissions/mememe_bikini.gif',
                    'https://www.monerochan.art/commissions/lofi_monerochan.mp4',
                    'https://www.monerochan.art/commissions/Doompa.webm'
                ]
            }
        }
        for user in data:
            _user = User.select().where(User.handle == user).first()
            if not _user:
                u = User(
                    handle=user,
                    wallet_address=data[user]['wallet'],
                    is_verified=True
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
                if not Artwork.select().where(Artwork.image == bn).first():
                    artwork = Artwork(
                        user=_user,
                        image=bn,
                        approved=False,
                        title=lorem.sentence(),
                        description=lorem.sentence()
                    )
                    artwork.save()
                    click.echo(f'[+] Created artwork {artwork.id} for {bn}')
                if not path.exists(f'./data/uploads/thumbnail-{bn}'):
                    artwork = Artwork.select().where(Artwork.image == bn).first()
                    artwork.generate_thumbnail()
                    click.echo(f'[+] Generated thumbnail for {bn}')
    return app
