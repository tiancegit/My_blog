# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app, jsonify, Response
from flask_login import login_required
from .forms import PostForm
from . import main
from ..moudle import User, Post, db
import markdown
import os


@main.route('/')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
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


@main.route('/test/<yera>/<mouth>')
def test(yera, mouth):
    return yera, mouth


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
