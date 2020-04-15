#!/usr/bin/env python

# -----------------------------------------------------------------------
# letterhandling.py
# Author:
# -----------------------------------------------------------------------

import os
from sys import argv
from time import localtime, asctime, gmtime
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template
from werkzeug.utils import secure_filename
from database import Database

UPLOAD_FOLDER = '/Users/hermanishengoma/Desktop'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# -----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# -----------------------------------------------------------------------

# checks if file is one of the allowed formats
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# get current time
def getCurrentTime():
    return asctime(gmtime())


# -----------------------------------------------------------------------

@app.route('/', methods=["GET", "POST"])
def main_page():
    database = Database()
    database.connect()
    database.send_out()
    database.disconnect()
    
    html = render_template('mainpage.html')
    response = make_response(html)
    return response


# -----------------------------------------------------------------------

@app.route('/submitted', methods=["GET", "POST"])
def handle_letter():
    # generate timestamp
    time_submitted = getCurrentTime()

    username = request.form.get('username')
    # connect to database
    database = Database()
    database.connect()

    # checks if username was submitted
    if username is None:
        return redirect('/')
    else:
        if not database.user_exist(username):
            return make_response(render_template('not_user.html'))

    # check if request has the file part
    if 'letter' not in request.files:
        return redirect('/')

    letter = request.files['letter']
    name = letter.filename

    # check if a file was submitted
    if name == '':
        return redirect('/')

    if letter and allowed_file(name):
        new_name = secure_filename(name)
        # letter.save(os.path.join(app.config['UPLOAD_FOLDER'], new_name))

        success = database.submit_letter(username, letter, new_name, time_submitted, UPLOAD_FOLDER + name)
        database.disconnect()

    html = render_template('confirm.html', username=username, lettername=new_name, success=success, time=time_submitted)
    response = make_response(html)
    return response


@app.route('/moderator', methods=["GET", "POST"])
def moderator():
    database = Database()
    database.connect()
    # letters = database.letter_queue()

    database.send_out()

    database.disconnect()
    html = render_template('moderator.html', letters=letters)
    response = make_response(html)
    return response


# -----------------------------------------------------------------------

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    
    database = Database()
    database.connect()
    database.send_out()
    database.disconnect()
    
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)

