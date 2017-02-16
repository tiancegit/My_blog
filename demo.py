from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config["BOOTSTRAP_SERVE_LOCAL"] = True
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about_me/')
def about_me():
    return 'About_me'


@app.route('/post/')
def post():
    pass


@app.route('/post_reproduced')
def post_reproduced():
    pass

if __name__ == '__main__':
    app.run(debug=True)
