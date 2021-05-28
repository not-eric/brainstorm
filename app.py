# Flask backend start

from flask import Flask
from flask_cors import CORS

app = Flask(__name__, static_url_path='', static_folder='./')
CORS(app)


@app.route('/api')
def api():
    return '<h1>API Page</h1>'
