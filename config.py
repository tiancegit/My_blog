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
    # 启用记录查询统计数字功能
    SQLALCHEMY_RECORD_QUERIES = True
    # 缓慢查询的阀值为 0.5 秒
    MY_BLOG_SLOW_DB_QUERY_TIME = 0.5
    MY_BLOG_SUBJECT_PREFIX = '[宁缺の博客]'
    MY_BLOG_MAIL_SENDER = 'My_Blog Admin <tiance.1984@gmail.com>'

    MY_BLOG_ADMIN = "tiance.1984@gmail.com"

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True  # SMTP 服务器好像只需要TLS协议
    # MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # 千万不要把账户密码直接写入脚本,特别是准备开源的时候,为了保护账户信息,
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # 可以使用脚本从环境中导入敏感信息

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    # 开发配置子类
    DEBUG = True
    # 配置bootstrap是否使用本地的文件。
    BOOTSTRAP_SERVE_LOCAL = True
    # 全文搜索引擎配置 http://www.ctolib.com/topics-44521.html
    WHOOSH_BASE = os.path.join(basedir, 'data-dev.sqlite')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    # 测试配置子类
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    # 生成环境配置子类
    # 配置bootstrap是否使用本地的文件。
    BOOTSTRAP_SERVE_LOCAL = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # 把错误通过邮件发送给管理员
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None

        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.MY_BLOG_MAIL_SENDER,
            toaddrs=[cls.MY_BLOG_ADMIN],
            subject=cls.MY_BLOG_SUBJECT_PREFIX + " Application Error",
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # 写入系统日志
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'prouduction': ProductionConfig,
    'unix': UnixConfig,
    'default': DevelopmentConfig
}