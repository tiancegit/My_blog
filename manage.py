# -*- coding: utf-8 -*-
import os
from app import create_app, db
from app.moudle import User, Post
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

# 暂时解决了表单项名不能为中文,  在中文字符串前添加 u 也可以解决问题.Mark一下
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = create_app(os.getenv('MY_BLOG_CONFIG') or 'default')
# 取消jinja2渲染时产生的空行
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
