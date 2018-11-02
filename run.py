# encoding: utf-8
from flask import render_template
from create_app import create_app
from werkzeug.contrib.fixers import ProxyFix

app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.route('/api_test/')
def index():

    return "hello" #render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
