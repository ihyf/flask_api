from util.ext import db


class User(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class Apps(db.Model):
    __tablename__ = 'apps'
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(200))
    app_desc = db.Column(db.String(200))
    app_ip = db.Column(db.JSON)
    app_ns = db.Column(db.JSON)
    app_publickey = db.Column(db.Text)
    app_privateKey = db.Column(db.Text)
    app_function = db.Column(db.JSON)
    app_status = db.Column(db.Integer)
