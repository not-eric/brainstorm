# Flask backend start

from flask import Flask, request, redirect, jsonify, url_for
from flask_cors import CORS
import sys
import os


app = Flask(__name__, static_url_path='', static_folder='./')
CORS(app)

sys.path.append('./src/generator')


@app.route('/api', methods=['GET', 'POST'])
def api():
    # handle the POST request
    if request.method == 'POST':
        name = request.get_json().get('name')
        # print("Request data: ", request.get_json().get('name'))

        from wrapper import gen
        title, abc = gen(name)
        print(f'Generated \"{title}\" for input {name}')
        #import generate
        #exec(open('src/generator/test.py').read(), globals())
        return jsonify(
            midititle=title,
            sheetmusic=abc
        )

    # GET request (and others)
    return '<h1>This town ain\'t big enough for the two of us! Go on, git!</h1>'


@app.errorhandler(404)
def internal_error(error):
    return redirect(url_for('index'))
