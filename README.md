# Brainstorm

A tool for generating random music based off of a variety of inputs -- throw in some data and inspire your next big music project!

Brainstorm is built with a responsive React frontend, with a Flask instance handling the backend operations.

## Installation instructions

For the frontend, simply run `npm install` in the main directory, and finally

To set up the backend, run `pip install -r requirements.txt` in order to install Flask and its dependencies.

The simplest way to view a live demo of both the front- and backend is to run both scripts in development mode.  
This requires no additional routing or server set up, so you can view it running immediately.

From the main directory, you'll start Flask with:

**Unix**

    $ export FLASK_APP=hello  
    $ flask run

**Windows**  

    > set FLASK_APP=hello 
    > flask run

To launch the React instance, in the same directory as the Flask instance, run:

    $ npm start

The node.js server will launch at `localhost:3000`, and the app will be ready!
