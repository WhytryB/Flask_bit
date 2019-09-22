import datetime

from project import db, bcrypt, robohash

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    robohash_img = db.Column(db.String, nullable=False, default=False)
    balance = db.Column(db.Float, nullable=True, default=0.0)

    def __init__(self,login, email, password, paid=False, admin=False, robohash_img=""):
        self.login = login
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.robohash_img = robohash(login)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '{}'.format(self.login)


class Groups(db.Model):

    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String,  nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    cookie = db.Column(db.String,  nullable=False)
    Group_id = db.Column(db.String,  nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.ForeignKey(User.id))
    user = db.relationship(User, backref='paths')

    login_proxy = db.Column(db.String, nullable=True)
    password_proxy = db.Column(db.String, nullable=True)
    ip_proxy = db.Column(db.String, nullable=True)
    port = db.Column(db.String, nullable=True)

    def __init__(self, status, amount, cookie, Group_id, user_id, login_proxy, password_proxy, ip_proxy, port):
        self.status = status
        self.amount = amount
        self.cookie = cookie
        self.Group_id = Group_id
        self.date = datetime.datetime.now()
        self.user_id = user_id

        self.login_proxy = login_proxy
        self.password_proxy = password_proxy
        self.ip_proxy = ip_proxy
        self.port = port

    def get_id(self):
        return self.id

    def __repr__(self):
        return '{}'.format(self.Group_id)


class Wallet(db.Model):

    __tablename__ = "wallet"

    id = db.Column(db.Integer, primary_key=True)
    wallet = db.Column(db.String,  nullable=False)
    sum = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.ForeignKey(User.id))
    user = db.relationship(User, backref='pathss')
    status = db.Column(db.String, nullable=False)


    def __init__(self, wallet, sum, user_id, status):
        self.wallet = wallet
        self.sum = sum
        self.date = datetime.datetime.now()
        self.user_id = user_id
        self.status = status

    def get_id(self):
        return self.id

    def __repr__(self):
        return '{}'.format(self.wallet)

