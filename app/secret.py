from passlib.totp import TOTP
import os

SECRET = os.environ['SECRET_TOTP']
SECRET_KEY = SECRET.split(':')[0]
SECRET_VAL = SECRET.split(' ')[1]

def create_totp_factory():
    return TOTP.using(secrets={SECRET_KEY:SECRET_VAL})
