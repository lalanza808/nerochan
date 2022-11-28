from os import path
from datetime import datetime
from secrets import token_urlsafe

from PIL import Image, ImageSequence

import peewee as pw

from nerochan import config


db = pw.SqliteDatabase(
    config.DATA_PATH + '/sqlite.db'
)

def gen_challenge():
    return token_urlsafe().replace('-', '').replace('_', '')


class User(pw.Model):
    """
    User model is for base user management and reporting.
    """
    id = pw.AutoField()
    register_date = pw.DateTimeField(default=datetime.utcnow)
    last_login_date = pw.DateTimeField(default=datetime.utcnow)
    handle = pw.CharField(unique=True)
    wallet_address = pw.CharField(unique=True)
    challenge = pw.CharField(default=gen_challenge)
    is_admin = pw.BooleanField(default=False)
    is_mod = pw.BooleanField(default=False)
    is_approved = pw.BooleanField(default=False)
    is_banned = pw.BooleanField(default=False)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def regenerate_challenge(self):
        self.challenge = gen_challenge()
        self.save()

    class Meta:
        database = db


class Profile(pw.Model):
    """
    Profile model is for users to provide metadata about
    themselves; Creators for their fans or even just the general public.
    Links to social media, contact info, portfolio sites, etc
    should go in here.
    """
    id = pw.AutoField()
    user = pw.ForeignKeyField(User)
    create_date = pw.DateTimeField(default=datetime.utcnow)
    website = pw.CharField(unique=True, null=True)
    twitter_handle = pw.CharField(unique=True, null=True)
    bio = pw.CharField(null=True)
    email = pw.CharField(unique=True, null=True)
    verified = pw.CharField(default=False)

    class Meta:
        database = db


class Artwork(pw.Model):
    """
    Artwork model is any uploaded content from a creator.
    """
    id = pw.AutoField()
    creator = pw.ForeignKeyField(User)
    image = pw.CharField()
    thumbnail = pw.CharField(null=True)
    upload_date = pw.DateTimeField(default=datetime.utcnow)
    last_edit_date = pw.DateTimeField(default=datetime.utcnow)
    approved = pw.BooleanField(default=False)
    hidden = pw.BooleanField(default=False)
    title = pw.CharField()
    description = pw.TextField(null=True)
    
    def generate_thumbnail(self):
        is_gif = self.image.endswith('.gif')
        _t = f'thumbnail-{self.image}'
        i = f'{config.DATA_PATH}/uploads/{self.image}'
        t = f'{config.DATA_PATH}/uploads/{_t}'
        if path.exists(t):
            return True
        try:
            size = (150,150)
            image = Image.open(i)
            if is_gif:
                frames = ImageSequence.Iterator(image)
                def thumbnails(frames):
                    for frame in frames:
                        thumbnail = frame.copy()
                        thumbnail.thumbnail(size, Image.ANTIALIAS)
                        yield thumbnail
                _frames = thumbnails(frames)
                _image = next(_frames)
                _image.info = image.info
                _image.save(t, format=image.format, save_all=True, append_images=list(_frames), disposal=2)
            else:
                image.thumbnail(size, Image.ANTIALIAS)
                image.save(t, format=image.format, quality=75)
            image.close()
            self.thumbnail = _t
            self.save()
            return True
        except:
            return False

    class Meta:
        database = db


class Transaction(pw.Model):
    """
    Transaction model is a simple reference to a Monero transaction so that we can track
    which transactions have occurred on-chain and what content they correspond to.
    """
    id = pw.AutoField()
    tx_id = pw.CharField(unique=True)
    atomic_xmr = pw.BigIntegerField()
    to_address = pw.CharField()
    content = pw.ForeignKeyField(Artwork)

    class Meta:
        database = db
