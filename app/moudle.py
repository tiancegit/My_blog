# -*- coding: utf-8 -*-
from . import db
from . import login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime
from markdown import markdown
import bleach
import hashlib
from flask import request


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        # 试图读取password属性的值,返回错误. 生成散列值之后无法还原原来的值.
        raise AttributeError('password in not readable attribute')

    @password.setter
    def password(self, password):
        # 注册时,输入密码,生成hash值再存储再数据库中.
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        # 传入用户输入的密码,与数据库中存储的hash值比对是否一直,一致返回True,反正返回False
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        # 生成一个令牌,有效期为expiration,单位是秒.
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        # 检验令牌,通过则把confirmed属性设为True
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            # 检查令牌的id是否和已登录的用户匹配
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        # 找回密码时生成的令牌, 失效时间一小时.
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        # 找回密码,验证令牌
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True


@login_manager.user_loader
def load_user(user_id):
    # 接收以 Unicode 字符串表示的用户标示符.找到用户,返回用户对象.否则,返回None
    return User.query.get(int(user_id))


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    short_title = db.Column(db.String(64))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body_html = db.Column(db.Text)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    # 处理body字段变化的函数
    @staticmethod
    def on_changed_post(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'pre',
                        'em', 'i', 'li', 'ol', 'code', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'img', 'hr']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_from='html'),
            tags=allowed_tags, strip=True,
            attributes={
                '*': ['class'],
                'a': ['href', 'rel'],
                'img': ['src', 'alt']
            }
        ))

# 注册监听事件. 当body字段发生变化时,触发函数,完成对应的html_body字段的更新.
db.event.listen(Post.body, 'set', Post.on_changed_post)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content_body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    author_name = db.Column(db.String(64))
    author_email = db.Column(db.String(64), default=None)
    author_website = db.Column(db.String(64), default=None)
    avatar_hash = db.Column(db.String(32))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __init__(self, **kwargs):
        super(Comment, self).__init__(**kwargs)
        if self.author_email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.author_email.encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='', rating=9):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'

        hash = self.avatar_hash or hashlib.md5(
            self.author_email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)