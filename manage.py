# -*- coding: utf-8 -*-
import os
from app import create_app, db
from app.models import User, Post, Comment, Tags
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


Cov = None
if os.environ.get('MY_BLOG_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')

# # 暂时解决了表单项名不能为中文,  在中文字符串前添加 u 也可以解决问题.Mark一下
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

app = create_app(os.getenv('MY_BLOG_CONFIG') or 'default')
# 取消jinja2渲染时产生的空行
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Comment=Comment, Tags=Tags)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


@manager.command
def test(coverage=False):
    """Run unit tests"""
    if coverage and not os.environ.get("MY_BLOG_COVERAGE"):
        import sys
        os.environ["MY_BLOG_COVERAGE"] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    test = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(test)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version:file://%s/index.html' % covdir)
        COV.erase()


@manager.command
def profile(length=25, profile_dir=None):
    """Strat the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


@manager.command
def deploy():
    """Run deploy tasks."""
    from flask_migrate import upgrade
    from app.models import User

    # 把数据库迁移到最新版本
    upgrade()



if __name__ == '__main__':
    manager.run()
