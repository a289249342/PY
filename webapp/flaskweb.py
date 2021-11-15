#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ARASHI'

# -*- coding: utf-8 -*-
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('temp.html')


@app.route('/signin', methods=['GET'])
def signin_form():
    return render_template('form.html')


@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == '884443':
        return render_template('sign.html', username=username)
    return render_template('form.html', message='Bad username or password', username=username)


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        password = request.form['password']
        if password == '884443':
            f = request.files['file']
            f.save(r'C:/PY/webapp/templates/temp.html')
        if password == '344488':
            f = request.files['file']
            f1 = request.files['file1']
            f2 = request.files['file2']
            f3 = request.files['file3']
            f4 = request.files['file4']
            f5 = request.files['file5']
            f6 = request.files['file6']
            f.save(r'C:/PY/webapp/templates/temp.html')
            f1.save(r'C:/PY/webapp/static/img/alla.png')
            f2.save(r'C:/PY/webapp/static/img/threea.png')
            f3.save(r'C:/PY/webapp/static/img/thisyeara.png')
            f4.save(r'C:/PY/webapp/static/img/allg.png')
            f5.save(r'C:/PY/webapp/static/img/threeg.png')
            f6.save(r'C:/PY/webapp/static/img/thisyearg.png')
        return render_template('temp.html')


if __name__ == '__main__':
    app.run(debug=1)
