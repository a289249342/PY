#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'ARASHI'

import hashlib
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if 1:
        try:
            signature = request.args.get('signature')
            timestamp = request.args.get('timestamp')
            nonce = request.args.get('nonce')
            echo = request.args.get('echostr')
            token = "Alex"
            l_hash = [str(token), str(timestamp), str(nonce)]
            l_hash.sort()
            sha1 = hashlib.sha1()
            for i in l_hash:
                sha1.update(i.encode('utf-8'))
            hashcode = sha1.hexdigest()
            print('4', hashcode)
            print("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                print(hashcode)
                return echo
        except TypeError as e:
            print(e)
    return render_template('temp.html')


@app.route('/sign', methods=['GET'])
def sign_form():
    return render_template('form.html')


@app.route('/sign', methods=['POST'])
def sign():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == '884443':
        return render_template('sign.html', username=username)
    return render_template('form.html', message='Bad username or password', username=username)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=1)
