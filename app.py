# Flask backend start

from flask import Flask, request
# from flask_cors import CORS
import sys
import os


app = Flask(__name__, static_url_path='', static_folder='./')
# CORS(app)

sys.path.append('./src/generator')


@app.route('/api', methods=['GET', 'POST'])
def api():
    # handle the POST request
    if request.method == 'POST':
        name = request.get_json().get('name')
        # print("Request data: ", request.get_json().get('name'))

        from wrapper import gen
        title = gen(name)
        print(f'Generated \"{title}\" for input {name}')
        #import generate
        #exec(open('src/generator/test.py').read(), globals())
        return title

    # GET request (and others)
    return '<h1>This town ain\'t big enough for the two of us! Go on, git!</h1>'
