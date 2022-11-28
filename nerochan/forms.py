from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired, ValidationError
from monero.address import address

from nerochan import config


def is_valid_xmr_address(form, field):
    try:
        # Ensure the provided address is valid address/subaddress/integrated address
        a = address(field.data)
        print(config.XMR_WALLET_NETWORK)
        # Ensure the provided address matches the network that the application's wallet is using
        if not config.XMR_WALLET_NETWORK.startswith(a.net):
            raise ValidationError('Provided Monero address does not match the configured network. Application: {}. Provided: {}'.format(
                config.XMR_WALLET_NETWORK.replace('net', ''), a.net
            ))
    except ValueError:
        raise ValidationError('Invalid Monero address provided')


class UserRegistration(FlaskForm):
    handle = StringField('Handle:', validators=[DataRequired()], render_kw={'placeholder': 'online handle', 'class': 'u-full-width', 'type': 'text'})
    wallet_address = StringField('Wallet Address:', validators=[DataRequired(), is_valid_xmr_address], render_kw={'placeholder': 'monero wallet address', 'class': 'u-full-width', 'type': 'text'})


class UserLogin(FlaskForm):
    handle = StringField('Handle:', validators=[DataRequired()], render_kw={'placeholder': 'online handle', 'class': 'u-full-width', 'type': 'text'})


class UserChallenge(FlaskForm):
    signature = StringField('Signature:', validators=[DataRequired()], render_kw={'placeholder': 'signed data', 'class': 'u-full-width', 'type': 'text'})


class ConfirmTip(FlaskForm):
    tx_id = StringField('TX ID:', validators=[DataRequired()], render_kw={'placeholder': 'TX ID', 'class': 'u-full-width', 'type': 'text'})
    tx_key = StringField('TX Key:', validators=[DataRequired()], render_kw={'placeholder': 'TX Key', 'class': 'u-full-width', 'type': 'text'})

