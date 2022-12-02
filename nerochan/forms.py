from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from monero.address import address

from nerochan.models import User
from nerochan import config


def is_valid_xmr_address(form, field):
    try:
        # Ensure the provided address is valid address/subaddress/integrated address
        a = address(field.data)
        # Ensure the provided address matches the network that the application's wallet is using
        if not config.XMR_WALLET_NETWORK.startswith(a.net):
            raise ValidationError('Provided Monero address does not match the configured network. Application: {}. Provided: {}'.format(
                config.XMR_WALLET_NETWORK.replace('net', ''), a.net
            ))
    except ValueError:
        raise ValidationError('Invalid Monero address provided')

def is_valid_user(form, field):
    try:
        u = User.select().where(User.handle == field.data).first()
        if not u:
            raise ValidationError('User does not exist')
        return True
    except ValueError:
        raise ValidationError('Error looking up user')


class UserRegistration(FlaskForm):
    handle = StringField('Handle:', validators=[DataRequired()], render_kw={'placeholder': 'online handle', 'class': 'u-full-width', 'type': 'text'})
    wallet_address = StringField('Wallet Address:', validators=[DataRequired(), is_valid_xmr_address], render_kw={'placeholder': 'monero wallet address', 'class': 'u-full-width', 'type': 'text'})


class UserForm(FlaskForm):
    handle = StringField('Handle:', validators=[DataRequired(), is_valid_user], render_kw={'placeholder': 'handle', 'class': 'u-full-width', 'type': 'text'})


class UserChallenge(FlaskForm):
    signature = StringField('Signature:', validators=[DataRequired()], render_kw={'placeholder': 'signed data', 'class': 'u-full-width', 'type': 'text'})


class ConfirmTip(FlaskForm):
    tx_id = StringField('TX ID:', validators=[DataRequired()], render_kw={'placeholder': 'TX ID', 'class': 'u-full-width', 'type': 'text'})
    tx_key = StringField('TX Key:', validators=[DataRequired()], render_kw={'placeholder': 'TX Key', 'class': 'u-full-width', 'type': 'text'})


class CreateArtwork(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()], render_kw={'placeholder': 'Title', 'class': 'u-full-width', 'type': 'text'})
    description = StringField('Description:', validators=[], render_kw={'placeholder': 'Description', 'class': 'u-full-width', 'type': 'text'})
    nsfw = BooleanField('NSFW:')
    content = FileField('Upload:', validators=[FileRequired(), FileAllowed(config.ALLOWED_UPLOADS)])
