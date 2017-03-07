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
                    body=form.body.data)
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


# @main.route('/<int:year>/')
# @main.route('/<int:year>/<int:mouth>/')
# @main.route('/<int:year>/<int:mouth>/<int:day>/')
# @main.route('/<int:year>/<int:mouth>/<int:day>/<title>')
# def test(year, mouth=None, day=None, title=None):
#     if year != None and mouth is None and day is None and title is None:
#         now_year = '%s-00-00 00:00:00.000000' % str(year)
#         next_year = '%s-00-00 00:00:00.000000' % str(year + 1)
# #       posts = db.session.query(Post).filter(Post.timestamp.between(now_year, next_year)).order_by(Post.timestamp.desc()).all()
#         page = request.args.get('page', type=int)
#         pagination = db.session.query(Post).filter(Post.timestamp.between(now_year, next_year)).order_by(Post.timestamp.desc()).paginate(
#             page, per_page=current_app.config['BLOG_POSTS_PER_PAGE'],
#             error_out=False)
#         posts = pagination.items
#         return render_template('test.html', posts=posts, pagination=pagination)
#     else:
#         return '404'

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


@main.route('/<int:year>/')
@main.route('/<int:year>/<int:mouth>/')
@main.route('/<int:year>/<int:mouth>/<int:day>/')
@main.route('/<int:year>/<int:mouth>/<int:day>/<title>')
def test(year, mouth=None, day=None, title=None):
    if year is not None and mouth is None and day is None and title is None:
        # 路由/2017
        start_time = '{year}-00-00 00:00:00.000000'.format(year=year)
        end_time = '{year}-00-01 00:00:00.000000'.format(year=year+1)
        pagination, posts = check_post(start_time, end_time)
    elif year is not None and mouth is not None and day is None and title is None:
        # 路由 /2017/03
        start_time = '{year}-{mouth:0>2d}-00 00:00:00.000000'.format(year=year, mouth=mouth)
        end_time = '{year}-{mouth:0>2d}-00 23:59:59.000000'.format(year=year, mouth=mouth+1)
        pagination, posts = check_post(start_time, end_time)
    elif year is not None and mouth is not None and day is not None and title is None:
        # 路由 /2017/03/04
        start_time = '{year}-{mouth:0>2d}-{day:0>2d} 00:00:00.000000'.format(year=year, mouth=mouth, day=day)
        end_time = '{year}-{mouth:0>2d}-{day:0>2d} 23:59:59.000000'.format(year=year, mouth=mouth, day=day)
        pagination, posts = check_post(start_time, end_time)
    elif year is not None and mouth is not None and day is not None and title is not None:
        # 路由 /2017/02/04/Python
        posts = Post.query.filter_by(title=title).first()
        if posts is None:
            # 尝试性查询文章,若为空值,则返回404
            abort(404)
        start_time = '{year}-{mouth:0>2d}-{day:0>2d} 00:00:00.000000'.format(year=year, mouth=mouth, day=day)
        end_time = '{year}-{mouth:0>2d}-{day:0>2d} 23:59:59.000000'.format(year=year, mouth=mouth, day=day)
        post = Post.query.filter(Post.timestamp.between(start_time, end_time)).filter_by(title=title).first()
        return render_template('post.html', post=post)
    return render_template('post-all.html', posts=posts, pagination=pagination, year=year, mouth=mouth, day=day, title=title)


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


@main.route('/post/')
def post():
    pass


@main.route('/post_reproduced')
def post_reproduced():
    pass
