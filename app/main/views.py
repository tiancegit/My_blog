# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, flash, redirect, url_for
from flask_login import login_required
from .forms import PostForm
from . import main
from ..moudle import User, Post, db
import markdown


@main.route('/')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts)


@main.route('/writer', methods=['GET', 'POST'])
@login_required
def writer():
    # 编写文章的路由
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    body=form.body.data)
        db.session.add(post)
        flash(u'文章已保存.', 'success')
        return redirect(url_for('main.index'))
    return render_template('writertest.html', form=form, markdown=markdown)


@main.route('/upload/', methods=['POST'])
def upload():
    pass



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
