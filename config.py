# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # 基类 Config中包含通用配置，子类分别专用的配置。如果需要。可以添加其他的配置类。
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'My_bolg'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SAVEPIC = basedir + '/image'
    # 首页文章每页显示的页数
    BLOG_POSTS_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    # 开发配置子类
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 配置bootstrap是否使用本地的文件。
    BOOTSTRAP_SERVE_LOCAL = True
    # 全文搜索引擎配置 http://www.ctolib.com/topics-44521.html
    WHOOSH_BASE = os.path.join(basedir, 'data-dev.sqlite')

    MY_BLOG_SUBJECT_PREFIX = '[宁缺の博客]'
    MY_BLOG_MAIL_SENDER = 'My_Blog Admin <tiance.1984@gmail.com>'

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = '587'
    MAIL_USE_TLS = True  # SMTP 服务器好像只需要TLS协议
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # 千万不要把账户密码直接写入脚本,特别是准备开源的时候,为了保护账户信息,
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # 可以使用脚本从环境中导入敏感信息
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    # 测试配置子类
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    # 生成环境配置子类
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'prouduction': ProductionConfig,

    'default': DevelopmentConfig
}