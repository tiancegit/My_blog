# -*- coding: utf-8 -*-
from . import db
from . import login_manage
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        # 试图读取password属性的值,返回错误. 生成散列值之后无法还原原来的值.
        raise AttributeError('password in not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manage.user_loader
def load_user(user_id):
    # 接收以 Unicode 字符串表示的用户标示符.找到用户,返回用户对象.否则,返回None
    return User.query.get(int(user_id))
