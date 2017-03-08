# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app, jsonify, Response, abort
from flask_login import login_required
from .forms import PostForm
from . import main
from ..moudle import User, Post, db
import os


@main.route('/')
def index():
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    page = request.args.get('page', type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLOG_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination)


@main.route('/writer', methods=['GET', 'POST'])
@login_required
def writer():
    # 编写文章的路由
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    body=form.body.data,
                    short_title=form.short_title.data)
        db.session.add(post)
        flash(u'文章已保存.', 'success')
        return redirect(url_for('main.index'))
    return render_template('writer.html', form=form)


@main.route('/upload/', methods=['POST'])
def upload():
    # 图片上传处理路由.
    file = request.files.get('editormd-image-file')
    if not file:
        res = {
            'succss': 0,
            'message': u'图片格式异常'
        }
    else:
        ex = os.path.splitext(file.filename)[1]
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + ex
        file.save(os.path.join(current_app.config['SAVEPIC'], filename))
        res = {
            'success': 1,
            'message': u'图片上传成功',
            'url': url_for('.image', name=filename)
        }
    return jsonify(res)


@main.route('/image/<name>')
def image(name):
    with open(os.path.join(current_app.config['SAVEPIC'], name), 'rb') as f:
        resp = Response(f.read(), mimetype='image/jpeg')
    return resp


def check_post(start, end):
    # 判断时间段的是否有文章的函数.start是开始时间,end是结束时间
    posts = Post.query.filter(Post.timestamp.between(start, end)).first()
    if posts is None:
        # 尝试性查询文章,若为空值,则返回404
        abort(404)
    page = request.args.get('page', type=int)
    pagination = Post.query.filter(Post.timestamp.between(start, end)).order_by(
        Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLOG_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return pagination, posts


@main.route('/<int:year>/<int:month>/<int:day>/<short_title>')
def post(year, month, day, short_title):
    if year is not None and month is not None and day is not None and short_title is not None:
        # 路由 /2017/02/04/Python
        post = Post.query.filter_by(short_title=short_title).first()
        if post is None:
            # 尝试性查询文章,若为空值,则返回404
            return 'a'
        start_time = '{year}-{month:0>2d}-{day:0>2d} 00:00:00.000000'.format(year=year, month=month, day=day)
        end_time = '{year}-{month:0>2d}-{day:0>2d} 23:59:59.000000'.format(year=year, month=month, day=day)
        post = Post.query.filter(Post.timestamp.between(start_time, end_time)).filter_by(short_title=short_title).first()
        return render_template('post.html', post=post)




@main.route('/<int:year>/')
@main.route('/<int:year>/<int:month>/')
@main.route('/<int:year>/<int:month>/<int:day>/')
def post_all(year, month=None, day=None):
    if year is not None and month is None and day is None:
        # 路由/2017
        start_time = '{year}-00-00 00:00:00.000000'.format(year=year)
        end_time = '{year}-00-01 00:00:00.000000'.format(year=year+1)
        pagination, posts = check_post(start_time, end_time)
    elif year is not None and month is not None and day is None:
        # 路由 /2017/03
        start_time = '{year}-{month:0>2d}-00 00:00:00.000000'.format(year=year, month=month)
        end_time = '{year}-{month:0>2d}-00 23:59:59.000000'.format(year=year, month=month+1)
        pagination, posts = check_post(start_time, end_time)
    elif year is not None and month is not None and day is not None:
        # 路由 /2017/03/04
        start_time = '{year}-{month:0>2d}-{day:0>2d} 00:00:00.000000'.format(year=year, month=month, day=day)
        end_time = '{year}-{month:0>2d}-{day:0>2d} 23:59:59.000000'.format(year=year, month=month, day=day)
        pagination, posts = check_post(start_time, end_time)
    return render_template('post-all.html', posts=posts, pagination=pagination, year=year, month=month, day=day)


@main.route('/tech')
def tech():
    return current_app.config['SAVEPIC']


@main.route('/isay')
def isay():
    return 'isay'


@main.route('/music')
def music():
    return 'music'


@main.route('/about')
def about():
    return render_template('about.html', current_time=datetime.utcnow())


@main.route('/post_reproduced')
def post_reproduced():
    pass
