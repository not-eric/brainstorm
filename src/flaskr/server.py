'''
This file is what's called by Brainstorm.js. Hopefully?
'''
from generate import generate as create
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/generator')
def newPiece(userName):
    newPiece = create.newComposition(userName, 2)
    return newPiece

if __name__ == '__main__':
  app.run(debug=True)