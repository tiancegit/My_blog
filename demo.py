# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
# 配置bootstrap是否使用本地的文件。
app.config["BOOTSTRAP_SERVE_LOCAL"] = True

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

manager = Manager(app)
migrate = Migrate(app, db)



def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tech')
def tech():
    return 'tech'


@app.route('/isay')
def isay():
    return 'isay'


@app.route('/music')
def music():
    return 'music'


@app.route('/about')
def about():
    return render_template('about.html', current_time=datetime.utcnow())


@app.route('/post/')
def post():
    pass


@app.route('/post_reproduced')
def post_reproduced():
    pass

if __name__ == '__main__':
#    app.run(debug=True)
    manager.run()
