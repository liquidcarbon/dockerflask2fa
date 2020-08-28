# import pandas as pd
#
# df = pd.read_csv('../data/small.csv')
# print(df)

import os
from flask import Flask, current_app, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, anonymous_user_required

from flask_security.views import register
# from secret import create_totp_factory

# At top of file
from flask_mail import Mail


# Convenient references
from werkzeug.datastructures import MultiDict
from werkzeug.local import LocalProxy


_security = LocalProxy(lambda: current_app.extensions['security'])

_datastore = LocalProxy(lambda: _security.datastore)

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
# Generate a nice key using secrets.token_urlsafe()
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

app.config['SECURITY_TWO_FACTOR_ENABLED_METHODS'] = ['email',
  'authenticator']  # 'sms' also valid but requires an sms provider
app.config['SECURITY_TWO_FACTOR'] = True
app.config['SECURITY_TWO_FACTOR_RESCUE_MAIL'] = 'put_your_mail@gmail.com'

# Generate a good totp secret using: passlib.totp.generate_secret()
app.config['SECURITY_TOTP_SECRETS'] = {"1": "TjQ9Qa31VOrfEzuPy4VHQWPCTmRzCnFzMKLxXYiZu9B"}
app.config['SECURITY_TOTP_ISSUER'] = 'liqc'

# DEBUG
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_REGISTER_URL'] = '/register'
app.config['TWO_FACTOR_REQUIRED'] = True
print(app.config)

# Create database connection object
db = SQLAlchemy(app)

# Define models
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80), unique=True)
  description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    tf_totp_secret = db.Column(db.String(255))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

mail = Mail(app)

# Create a user to test with
@app.before_first_request
def create_user():
    db.create_all()
    user_datastore.create_user(
        email='gal@lp.com',
        password='password',
        username='gal',
        tf_totp_secret=None
    )
    db.session.commit()

# Views
@app.route('/')
@login_required
def home():
    return render_template('index.html')

@app.route('/register')
def new_user():
    register()
# @anonymous_user_required
# def register():
#     return render_template('security/two_factor_setup.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
