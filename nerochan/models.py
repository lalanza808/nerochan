from os import path
from datetime import datetime
from secrets import token_urlsafe

from flask_login import login_user
from PIL import Image, ImageSequence, ImageFilter, ImageFont
from cv2 import VideoCapture

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
    wallet_address = pw.CharField(unique=True, null=False)
    challenge = pw.CharField(default=gen_challenge)
    is_admin = pw.BooleanField(default=False)
    is_mod = pw.BooleanField(default=False)
    is_verified = pw.BooleanField(default=False)
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
    
    def login(self):
        login_user(self)
        self.last_login_date = datetime.utcnow()
        self.save()

    class Meta:
        database = db


class Profile(pw.Model):
    """
    Profile model is for users to provide metadata about
    themselves; artists for their fans or even just the general public.
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
    Artwork model is any uploaded content from a user.
    """
    id = pw.AutoField()
    user = pw.ForeignKeyField(User)
    image = pw.CharField()
    upload_date = pw.DateTimeField(default=datetime.utcnow)
    last_edit_date = pw.DateTimeField(default=datetime.utcnow)
    approved = pw.BooleanField(default=False)
    hidden = pw.BooleanField(default=False)
    nsfw = pw.BooleanField(default=False)
    title = pw.CharField()
    description = pw.TextField(null=True)

    @property
    def thumbnail(self):
        res = f'thumbnail-{self.image}'
        if self.is_video:
            return f'{res[:-3]}.png'
        else:
            return res
    
    @property
    def is_video(self):
        if self.image.endswith('.mp4') or self.image.endswith('.webm'):
            return True
        else:
            return False
    
    def generate_thumbnail(self):
        _t = self.thumbnail
        i = f'{config.DATA_PATH}/uploads/{self.image}'
        t = f'{config.DATA_PATH}/uploads/{_t}'
        try:
            size = (150,150)
            if self.image.endswith('.gif'):
                image = Image.open(i)
                frames = ImageSequence.Iterator(image)
                def thumbnails(frames):
                    nsfw = Image.open('nerochan/static/images/nsfw.png')
                    for frame in frames:
                        thumbnail = frame.copy().convert('RGBA')
                        thumbnail.thumbnail(size, Image.ANTIALIAS)
                        if self.nsfw:
                            thumbnail = thumbnail.filter(ImageFilter.GaussianBlur(radius = 6))
                            thumbnail.paste(nsfw, (int(thumbnail.width / 2) - int(nsfw.width / 2), int(thumbnail.height / 2) - int(nsfw.height / 2)), nsfw)
                        yield thumbnail
                    nsfw.close()
                _frames = thumbnails(frames)
                _image = next(_frames)
                _image.info = image.info
                _image.save(t, save_all=True, append_images=list(_frames), disposal=2)
                _image.close()
                image.close()
            elif self.is_video:
                cap = VideoCapture(i)
                _, frame = cap.read()
                image = Image.fromarray(frame)
                if self.nsfw:
                    nsfw = Image.open('nerochan/static/images/nsfw.png')
                    image = image.filter(ImageFilter.GaussianBlur(radius = 6))
                    image.paste(nsfw, (int(image.width / 2) - int(nsfw.width / 2), int(image.height / 2) - int(nsfw.height / 2)), nsfw)
                    nsfw.close()
                pb = Image.open('nerochan/static/images/play.png')
                image.paste(pb, (int(image.width / 2) - int(pb.width / 2), int(image.height / 2) - int(pb.height / 2)), pb)
                pb.close()
                image.save(t, format=image.format)
                image.close()
            else:
                image = Image.open(i)
                image.thumbnail(size, Image.ANTIALIAS)
                if self.nsfw:
                    nsfw = Image.open('nerochan/static/images/nsfw.png')
                    image = image.filter(ImageFilter.GaussianBlur(radius = 6))
                    image.paste(nsfw, (int(image.width / 2) - int(nsfw.width / 2), int(image.height / 2) - int(nsfw.height / 2)), nsfw)
                    nsfw.close()
                image.save(t, format=image.format)
                image.close()
            self.save()
            return True
        except Exception as e:
            print(e)
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
    tx_key = pw.CharField(unique=True)
    atomic_xmr = pw.BigIntegerField(null=True)
    to_address = pw.CharField()
    artwork = pw.ForeignKeyField(Artwork)
    verified = pw.BooleanField(default=False)
    create_date = pw.DateTimeField(default=datetime.utcnow)
    tx_date = pw.DateTimeField(null=True)

    class Meta:
        database = db
