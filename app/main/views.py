from datetime import datetime
from flask import render_template

from . import main
from .. import db
from ..moudle import User


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/tech')
def tech():
    return 'tech'


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
