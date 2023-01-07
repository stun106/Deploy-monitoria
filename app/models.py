from app import db,login_manager
from flask_login import UserMixin


@login_manager.user_loader
def current_user(user_id):
    return Login.query.get(user_id)

class Login(db.Model,UserMixin):
    __tablename__ = "logins"
    id = db.Column(db.Integer, primary_key= True)
    userName = db.Column(db.String(50), nullable = False, unique = True)
    nickName = db.Column(db.String(50), nullable = False, unique = True)
    passWord = db.Column(db.String(255), nullable = False)
    turMa = db.Column(db.String(50),nullable = False)
    moduLo = db.Column(db.String(50),nullable = False)
    profile = db.relationship('Alunos', backref='login', lazy=True)

    def __init__(self) -> None:
        return self.userName

class Alunos(db.Model):
    __tablename__ = "alunos"
    id = db.Column(db.Integer, primary_key= True)
    fdBack = db.Column(db.String(255))
    satisfacao = db.Column(db.String(3))
    nickinfo = db.Column(db.String(80))
    pbDate = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('logins.id'))
