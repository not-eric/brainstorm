# Flask backend start

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__, static_url_path='', static_folder='./')
CORS(app)


@app.route('/api', methods=['GET', 'POST'])
def api():
    # handle the POST request
    if request.method == 'POST':
        name = request.get_json().get('name')
        print("Request data: ", request.get_json().get('name'))
        return f'<h1>Received name {name}</h1>'

    # GET request (and others)
    return '<h1>This town ain\'t big enough for the two of us! Go on, git!</h1>'
