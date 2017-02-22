# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
login_manage = LoginManager()
login_manage.session_protection = 'strong'  # 设置Flask_Login的安全等级
login_manage.login_view = 'auth.login'  # 设置登录页面的端点,用户未登录访问就跳回这里用于登录.


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manage.init_app(app)


    # 附加路由和自定义的错误页面。
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')  # 注册后,蓝本中定义的所有路由会添加指定的前缀,如/auth


    return app