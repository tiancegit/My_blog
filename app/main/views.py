# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, flash, redirect, url_for
from flask_login import login_required
from .forms import PostForm
from . import main
from ..moudle import User, Post, db


@main.route('/')
def index():
    return render_template('index.html')

# mkd = '''
'''
# header
## header2
[picture](http://www.example.com)
* 1
* 2
* 3
**bold**
'''


@main.route('/writer')
@login_required
def writer():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    body=form.body.data)
        db.session.add(post)
        flash(u'文章已保存.', 'success')
        return redirect(url_for('main.index'))
    return render_template('writertest.html', form=form)


@main.route('/tech')
def tech():
    user = User.query.filter_by(email='tiance.1984@gmail.com').first()
    return user.username


@main.route('/isay')
def isay():
    return 'isay'


@main.route('/music')
def music():
    return 'music'


@main.route('/about')
def about():
    return render_template('about.html', current_time=datetime.utcnow())


@main.route('/post/')
def post():
    pass


@main.route('/post_reproduced')
def post_reproduced():
    pass
