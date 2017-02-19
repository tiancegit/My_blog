# coding=utf-8
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
# 配置bootstrap是否使用本地的文件。
app.config["BOOTSTRAP_SERVE_LOCAL"] = True
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tech')
def tech():
    return 'tech'


@app.route('/isay')
def isay():
    return 'isay'


@app.route('/music')
def music():
    return 'music'


@app.route('/about')
def about():
    return 'About'


@app.route('/post/')
def post():
    pass


@app.route('/post_reproduced')
def post_reproduced():
    pass

if __name__ == '__main__':
    app.run(debug=True)
